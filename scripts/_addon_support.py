#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT_REQUIRED_FIELDS = [
    "identifier",
    "name",
    "description",
    "version",
    "maintainer",
    "license",
    "elements",
]

ELEMENT_REQUIRED_FIELDS = [
    "identifier",
    "name",
    "type",
    "path",
]

SUPPORTED_ELEMENT_TYPES = {"Plugin", "DataLabFunctions"}
SUPPORTED_PLUGIN_CATEGORIES = {"DisplayPane"}
SUPPORTED_TEMPLATE_LICENSES = {
    "No license",
    "Apache License 2.0",
    "MIT License",
    "GNU General Public License",
    "3-clause BSD License",
    "Custom License",
}


class AddonValidationError(Exception):
    pass


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AddonValidationError(f"File not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AddonValidationError(f"Invalid JSON in {path}: {exc}") from exc


def dump_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-") or "seeq-addon"


def pythonize(value: str) -> str:
    value = slugify(value).replace("-", "_")
    if value and value[0].isdigit():
        value = f"addon_{value}"
    return value


def extract_company_name(identifier: str) -> str:
    parts = identifier.split(".")
    if len(parts) >= 2 and parts[0] == "com":
        return parts[1]
    if parts:
        return parts[0]
    return "company"


def resolve_template_license(license_name: str) -> tuple[str, str]:
    if license_name in SUPPORTED_TEMPLATE_LICENSES:
        return license_name, ""
    return "Custom License", license_name


def extract_dlf_kernel_name(payload: dict) -> str:
    dlf = get_first_dlf(payload)
    if not dlf:
        return "python311"
    schema = dlf.get("configuration_schema", {})
    properties = schema.get("properties", {})
    advanced = properties.get("advanced_project_configuration", {})
    advanced_properties = advanced.get("properties", {})
    kernel = advanced_properties.get("kernel_name", {})
    default = kernel.get("default")
    return default if isinstance(default, str) and default else "python311"


def validate_addon_payload(payload: dict) -> list[str]:
    errors: list[str] = []

    for field in ROOT_REQUIRED_FIELDS:
        if field not in payload:
            errors.append(f"Missing required root field: {field}")

    if "elements" in payload and not isinstance(payload["elements"], list):
        errors.append("Root field 'elements' must be a list")
        return errors

    elements = payload.get("elements", [])
    if not elements:
        errors.append("At least one element must be declared")

    seen_paths: set[str] = set()
    seen_identifiers: set[str] = set()

    for index, element in enumerate(elements):
        prefix = f"elements[{index}]"
        if not isinstance(element, dict):
            errors.append(f"{prefix} must be an object")
            continue

        for field in ELEMENT_REQUIRED_FIELDS:
            if field not in element:
                errors.append(f"{prefix} missing required field: {field}")

        element_type = element.get("type")
        if element_type not in SUPPORTED_ELEMENT_TYPES:
            errors.append(
                f"{prefix}.type must be one of {sorted(SUPPORTED_ELEMENT_TYPES)}, got {element_type!r}"
            )

        path_value = element.get("path")
        if isinstance(path_value, str):
            if path_value in seen_paths:
                errors.append(f"Duplicate element path: {path_value}")
            seen_paths.add(path_value)

        identifier = element.get("identifier")
        if isinstance(identifier, str):
            if identifier in seen_identifiers:
                errors.append(f"Duplicate element identifier: {identifier}")
            seen_identifiers.add(identifier)

        if element_type == "Plugin":
            category = element.get("category")
            if category not in SUPPORTED_PLUGIN_CATEGORIES:
                errors.append(
                    f"{prefix}.category must be one of {sorted(SUPPORTED_PLUGIN_CATEGORIES)}, got {category!r}"
                )

    return errors


def load_and_validate_addon(path: Path) -> dict:
    payload = load_json(path)
    errors = validate_addon_payload(payload)
    if errors:
        raise AddonValidationError("\n".join(errors))
    payload.setdefault("icon", "fa-bar-chart")
    payload.setdefault("previews", [])
    payload.setdefault("tags", {})
    return payload


def get_first_plugin(payload: dict) -> dict | None:
    for element in payload["elements"]:
        if element["type"] == "Plugin":
            return element
    return None


def get_first_dlf(payload: dict) -> dict | None:
    for element in payload["elements"]:
        if element["type"] == "DataLabFunctions":
            return element
    return None
