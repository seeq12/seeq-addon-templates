#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_TOOL_PYTHON = Path.home() / ".sq-addon" / ".venv" / "bin" / "python"

if ADDON_TOOL_PYTHON.exists() and ".sq-addon/.venv/" not in sys.executable:
    os.execv(str(ADDON_TOOL_PYTHON), [str(ADDON_TOOL_PYTHON), __file__, *sys.argv[1:]])

sys.path.insert(0, str(REPO_ROOT))

from addon_template.generator import render_template
from scripts._addon_support import (
    AddonValidationError,
    dump_json,
    extract_company_name,
    extract_dlf_kernel_name,
    get_first_dlf,
    get_first_plugin,
    load_and_validate_addon,
    pythonize,
    resolve_template_license,
    slugify,
)


def ensure_supported_first_slice(payload: dict) -> None:
    plugin_elements = [e for e in payload["elements"] if e["type"] == "Plugin"]
    dlf_elements = [e for e in payload["elements"] if e["type"] == "DataLabFunctions"]

    if len(plugin_elements) != 1:
        raise AddonValidationError("First implementation slice supports exactly one Plugin element")
    if len(dlf_elements) > 1:
        raise AddonValidationError("First implementation slice supports at most one DataLabFunctions element")
    if plugin_elements[0].get("category") != "DisplayPane":
        raise AddonValidationError("First implementation slice supports only DisplayPane plugins")


def build_copier_data(payload: dict) -> dict:
    ensure_supported_first_slice(payload)

    plugin = get_first_plugin(payload)
    dlf = get_first_dlf(payload)
    company_name = extract_company_name(payload["identifier"])
    project_license, custom_license = resolve_template_license(payload["license"])

    data = {
        "project_name": payload["name"],
        "project_description": payload["description"],
        "project_version": payload["version"],
        "project_icon": payload.get("icon", "fa-bar-chart"),
        "project_maintainer": payload["maintainer"],
        "company_name": company_name,
        "project_license": project_license,
        "custom_license": custom_license,
        "elements_to_include": ["DisplayPanePlugin"] + (["DataLabFunctions"] if dlf else []),
        "addon_identifier_override": payload["identifier"],
        "plugin_identifier_override": plugin["identifier"],
        "plugin_name_override": plugin["name"],
        "plugin_path_override": plugin["path"],
        "python_package_name_override": pythonize(payload["name"]),
        "python_project_name_override": slugify(payload["name"]),
        "dlf_kernel_name_override": extract_dlf_kernel_name(payload),
    }

    if dlf:
        data.update(
            {
                "dlf_identifier_override": dlf["identifier"],
                "dlf_name_override": dlf["name"],
                "dlf_path_override": dlf["path"],
            }
        )

    return data


def instantiate_project(payload: dict, output_dir: Path) -> None:
    render_template(output_dir, data=build_copier_data(payload))
    dump_json(output_dir / "addon.json", payload)

    if not get_first_dlf(payload):
        pyright_config = output_dir / "pyrightconfig.json"
        if pyright_config.exists():
            pyright_config.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="Instantiate a Seeq add-on project from addon.json")
    parser.add_argument("--addon", required=True, help="Path to addon.json")
    parser.add_argument("--output", required=True, help="Output directory for the instantiated add-on")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output directory")
    args = parser.parse_args()

    payload = load_and_validate_addon(Path(args.addon).resolve())
    output_dir = Path(args.output).resolve()

    if output_dir.exists():
        if not args.force:
            raise SystemExit(f"Output directory already exists: {output_dir}. Use --force to overwrite.")
        shutil.rmtree(output_dir)

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    instantiate_project(payload, output_dir)
    print(f"Created add-on at {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
