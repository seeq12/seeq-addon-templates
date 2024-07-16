import glob
import os
import pathlib
import zipfile
from .build import build

from .utils import (
    PROJECT_PATH,
    get_add_on_package_name,
    get_element_paths_with_type,
    get_module,
    get_files_to_package
)


DIST_FOLDER = PROJECT_PATH / 'dist'
ADD_ON_EXTENSION = '.addon'
ADD_ON_METADATA_EXTENSION = '.addonmeta'


def package(args=None):
    print("Packaging")
    if not args.skip_build:
        build()
    file_name = get_add_on_package_name()

    if DIST_FOLDER.exists():
        for file in glob.glob(f"{DIST_FOLDER}/*"):
            os.remove(file)
    else:
        os.makedirs(DIST_FOLDER)

    artifact_file_name = DIST_FOLDER / f"{file_name}{ADD_ON_EXTENSION}"
    metadata_file_name = DIST_FOLDER / f"{file_name}{ADD_ON_METADATA_EXTENSION}"

    with zipfile.ZipFile(
            artifact_file_name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as add_on_file:
        for filename in get_files_to_package():
            add_on_file.write(filename, filename)
        for element_path, element_type in get_element_paths_with_type().items():
            for filename in get_module(element_path, element_type).get_files_to_package(pathlib.Path(element_path)):
                full_path = PROJECT_PATH / element_path / filename
                archive_path = pathlib.Path(element_path) / filename
                add_on_file.write(full_path, archive_path)

    with zipfile.ZipFile(
            metadata_file_name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as metadata_file:
        for filename in get_files_to_package():
            metadata_file.write(filename, filename)

    print("Done packaging")