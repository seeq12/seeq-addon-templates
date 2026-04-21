#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _addon_support import AddonValidationError, load_and_validate_addon


def validate_project_structure(project_root: Path, payload: dict) -> list[str]:
    errors: list[str] = []
    for element in payload["elements"]:
        element_path = project_root / element["path"]
        if not element_path.exists():
            errors.append(f"Missing element path: {element['path']}")

    plugin = next((e for e in payload["elements"] if e["type"] == "Plugin"), None)
    if plugin:
        plugin_file = project_root / plugin["path"] / "plugin.json"
        package_file = project_root / plugin["path"] / "package.json"
        if not plugin_file.exists():
            errors.append(f"Missing plugin manifest: {plugin['path']}/plugin.json")
        if not package_file.exists():
            errors.append(f"Missing frontend package file: {plugin['path']}/package.json")

    dlf = next((e for e in payload["elements"] if e["type"] == "DataLabFunctions"), None)
    if dlf:
        api_notebook = project_root / dlf["path"] / "API.ipynb"
        if not api_notebook.exists():
            errors.append(f"Missing DLF notebook: {dlf['path']}/API.ipynb")

    return errors


def format_project_structure_errors(errors: list[str]) -> list[str]:
    if not errors:
        return []

    return [
        "Project structure validation failed.",
        "This check expects an instantiated add-on project with generated element files.",
        "Run `python3 scripts/create_addon.py --addon <addon.json> --output <project-dir>` first,",
        "or validate only the canonical contract with `python3 scripts/validate_addon.py --mode contract --addon <addon.json>`.",
        *errors,
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate addon.json as a contract or as an instantiated project.")
    parser.add_argument("--addon", required=True, help="Path to addon.json")
    parser.add_argument(
        "--project-root",
        default=None,
        help="Project root to validate against. Defaults to the directory containing addon.json.",
    )
    parser.add_argument(
        "--mode",
        choices=("contract", "project"),
        default="project",
        help="Validation mode. `contract` validates only addon.json semantics. `project` also validates generated files.",
    )
    args = parser.parse_args()

    addon_path = Path(args.addon).resolve()
    project_root = Path(args.project_root).resolve() if args.project_root else addon_path.parent

    try:
        payload = load_and_validate_addon(addon_path)
    except AddonValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.mode == "contract":
        print(f"Validated contract {addon_path}")
        return 0

    errors = validate_project_structure(project_root, payload)
    if errors:
        print("ERROR:", file=sys.stderr)
        for error in format_project_structure_errors(errors):
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated project {addon_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
