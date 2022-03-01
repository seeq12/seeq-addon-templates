#!/usr/bin/env python
import os, shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_dir(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    if '{{ cookiecutter.include_tests }}' != 'y':
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'test'))

    if '{{ cookiecutter.include_docs }}' != 'y':
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'docs_src'))
        remove_dir('docs_src')

    if '{{ cookiecutter.docs_only }}' == 'y':
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'seeq'))
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'tests'))
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'development'))

    if '{{ cookiecutter.project_license }}' == 'marketplace':
        files_to_delete = ['github.md', 'docstrings.rst', 'add_on_installation.rst', 'backend_calculations.rst',
                           'seeq_server_interactions.rst', 'user_interface.rst']
        for f in files_to_delete:
            remove_file(os.path.join(PROJECT_DIRECTORY, 'docs_src', 'source', f))

