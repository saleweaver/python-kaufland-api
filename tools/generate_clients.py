#!/usr/bin/env python3
import argparse
import json
import keyword
import re
from pathlib import Path


def snake_case(name: str) -> str:
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    name = name.lower().strip("_")
    return safe_name(name)


def pascal_case(value: str) -> str:
    parts = re.split(r"[^0-9a-zA-Z]+", value)
    return "".join(p.capitalize() for p in parts if p)


def safe_name(name: str) -> str:
    if not name:
        return name
    name = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    if re.match(r"^[0-9]", name):
        name = f"_{name}"
    if keyword.iskeyword(name):
        name = f"{name}_"
    return name


def unique_name(name: str, used: set[str]) -> str:
    if name not in used:
        used.add(name)
        return name
    i = 2
    while f"{name}_{i}" in used:
        i += 1
    unique = f"{name}_{i}"
    used.add(unique)
    return unique


def has_storefront_param(op: dict) -> bool:
    for param in op.get("parameters", []) or []:
        if param.get("in") == "query" and param.get("name") == "storefront":
            return True
    return False


def get_path_params(path: str) -> list[str]:
    return re.findall(r"{([^}]+)}", path)


def _split_lines(text: str) -> list[str]:
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def build_docstring(summary: str | None, description: str | None) -> list[str]:
    doc = []
    text = (summary or "").strip()
    desc = (description or "").strip()
    if not text and not desc:
        return doc
    doc.append('"""')
    if text:
        doc.extend(_split_lines(text))
    if desc:
        if text:
            doc.append("")
        doc.extend(_split_lines(desc))
    doc.append('"""')
    return doc


def schema_type(schema: dict | None) -> str:
    if not schema:
        return "object"
    if "$ref" in schema:
        return schema["$ref"].split("/")[-1]
    if "oneOf" in schema:
        return " | ".join(schema_type(item) for item in schema["oneOf"])
    if "anyOf" in schema:
        return " | ".join(schema_type(item) for item in schema["anyOf"])
    schema_type_name = schema.get("type")
    if schema_type_name == "array":
        item_type = schema_type(schema.get("items"))
        return f"list[{item_type}]"
    if schema_type_name == "integer":
        return "int"
    if schema_type_name == "number":
        return "float"
    if schema_type_name == "string":
        return "str"
    if schema_type_name == "boolean":
        return "bool"
    return schema_type_name or "object"


def collect_args(op: dict) -> list[str]:
    args = []
    for param in op.get("parameters", []) or []:
        name = param.get("name", "")
        location = param.get("in", "")
        if not name:
            continue
        type_name = schema_type(param.get("schema"))
        required = "required" if param.get("required") else "optional"
        description = " ".join((param.get("description") or "").split())
        line = f"{name}: {type_name} | {required}"
        if location:
            line += f" ({location})"
        if description:
            line += f" {description}"
        args.append(line)

    request_body = op.get("requestBody")
    if request_body:
        required = "required" if request_body.get("required") else "optional"
        description = " ".join((request_body.get("description") or "").split())
        content = request_body.get("content") or {}
        schema = None
        if content:
            content_schema = next(iter(content.values()), {})
            schema = content_schema.get("schema")
            if not description:
                description = " ".join(
                    ((schema or {}).get("description") or "").split()
                )
        type_name = schema_type(schema)
        line = f"body: {type_name} | {required} (body)"
        if description:
            line += f" {description}"
        args.append(line)

    return args


def generate_class_code(
    class_name: str, operations: list[dict], *, async_mode: bool
) -> str:
    lines = []
    if async_mode:
        lines.append("from kaufland.asyncio import Client")
    else:
        lines.append("from kaufland import Client")
    lines.append(
        "from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint"
    )
    lines.append("")
    lines.append("")
    lines.append(f"class {class_name}(Client):")
    lines.append(f'    """{class_name} Kaufland API Client."""')
    lines.append("")

    used_method_names: set[str] = set()
    for op in operations:
        method = op["method"].upper()
        path = op["path"]
        op_id = op.get("operationId")
        method_name = snake_case(op_id or f"{method}_{path}")
        method_name = unique_name(method_name, used_method_names)
        path_params = op["path_params"]
        param_names = [safe_name(snake_case(p)) for p in path_params]
        signature_params = ", ".join(param_names)
        if signature_params:
            signature = f"(self, {signature_params}, **kwargs) -> ApiResponse"
        else:
            signature = "(self, **kwargs) -> ApiResponse"

        lines.append(
            f'    @kaufland_endpoint("{op["decorator_path"]}", method="{method}")'
        )
        lines.append(
            f"    {'async ' if async_mode else ''}def {method_name}{signature}:"
        )

        doc_lines = build_docstring(op.get("summary"), op.get("description"))
        args = collect_args(op.get("raw", {}))
        if args:
            if doc_lines:
                doc_lines = doc_lines[:-1]
                if len(doc_lines) > 1:
                    doc_lines.append("")
            else:
                doc_lines = ['"""']
            doc_lines.append("Args:")
            for line in args:
                doc_lines.append(f"{line}")
            doc_lines.append('"""')
        if doc_lines:
            for doc_line in doc_lines:
                lines.append(f"        {doc_line}")
        else:
            lines.append('        """""')

        if path_params:
            path_expr = (
                f"fill_query_params(kwargs.pop('path'), {', '.join(param_names)})"
            )
        else:
            path_expr = "kwargs.pop('path')"

        add_storefront = "True" if op["add_storefront"] else "False"
        has_body = op["has_body"]
        if has_body:
            lines.append("        body = kwargs.pop('body', None)")
            request = f"{path_expr}, data=body, params=kwargs, add_storefront={add_storefront}"
        else:
            request = f"{path_expr}, params=kwargs, add_storefront={add_storefront}"

        if async_mode:
            lines.append(f"        return await self._request({request})")
        else:
            lines.append(f"        return self._request({request})")
        lines.append("")

    if len(lines) == 5:
        lines.append("    pass")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Kaufland API clients from swagger.json"
    )
    parser.add_argument("--swagger", default="swagger.json")
    parser.add_argument("--sync-out", default="kaufland/api")
    parser.add_argument("--async-out", default="kaufland/asyncio/api")
    args = parser.parse_args()

    swagger_path = Path(args.swagger)
    data = json.loads(swagger_path.read_text(encoding="utf-8"))

    groups: dict[str, list[dict]] = {}
    for path, ops in data.get("paths", {}).items():
        segment = path.strip("/").split("/")[0] or "root"
        for method, op in ops.items():
            if method.lower() not in {"get", "post", "put", "patch", "delete"}:
                continue
            entry = {
                "method": method,
                "path": path,
                "decorator_path": re.sub(r"{[^}]+}", "{}", path),
                "operationId": op.get("operationId"),
                "summary": op.get("summary"),
                "description": op.get("description"),
                "path_params": get_path_params(path),
                "has_body": "requestBody" in op,
                "add_storefront": has_storefront_param(op),
                "raw": op,
            }
            groups.setdefault(segment, []).append(entry)

    sync_out = Path(args.sync_out)
    async_out = Path(args.async_out)
    sync_out.mkdir(parents=True, exist_ok=True)
    async_out.mkdir(parents=True, exist_ok=True)

    sync_init_lines = []
    async_init_lines = []

    used_modules: set[str] = set()
    for segment, ops in sorted(groups.items()):
        ops = sorted(ops, key=lambda item: (item["path"], item["method"]))
        class_name = pascal_case(segment) or "Root"
        module_name = unique_name(snake_case(segment) or "root", used_modules)
        file_path = sync_out / f"{module_name}.py"
        async_file_path = async_out / f"{module_name}.py"

        sync_code = generate_class_code(class_name, ops, async_mode=False)
        async_code = generate_class_code(class_name, ops, async_mode=True)
        file_path.write_text(sync_code, encoding="utf-8")
        async_file_path.write_text(async_code, encoding="utf-8")

        sync_init_lines.append(f"from .{module_name} import {class_name}")
        async_init_lines.append(f"from .{module_name} import {class_name}")

    sync_init_lines.append("")
    sync_init_lines.append("__all__ = [")
    for line in sync_init_lines[:-2]:
        name = line.split()[-1]
        sync_init_lines.append(f"    '{name}',")
    sync_init_lines.append("]")

    async_init_lines.append("")
    async_init_lines.append("__all__ = [")
    for line in async_init_lines[:-2]:
        name = line.split()[-1]
        async_init_lines.append(f"    '{name}',")
    async_init_lines.append("]")

    (sync_out / "__init__.py").write_text(
        "\n".join(sync_init_lines) + "\n", encoding="utf-8"
    )
    (async_out / "__init__.py").write_text(
        "\n".join(async_init_lines) + "\n", encoding="utf-8"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
