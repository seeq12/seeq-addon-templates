import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_dir(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


def remove_file(filepath):
    if os.path.isfile(filepath):
        os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    if '{{ cookiecutter.include_tests }}' not in ['yes', 'y']:
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'tests'))

    if '{{ cookiecutter.template_type }}' == 'add-on_code_only':
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'docs_src'))

    if '{{ cookiecutter.template_type }}' == 'documentation_only':
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'seeq'))
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'tests'))
        remove_dir(os.path.join(PROJECT_DIRECTORY, 'development'))
        root_files_to_delete = ['.gitignore', 'developer_notebook.ipynb', 'LICENSE', 'MANIFEST.in', 'NOTICE',
                                'pytest.ini', 'README.md', 'requirements.txt', 'setup.py']
        for f in root_files_to_delete:
            remove_file(os.path.join(PROJECT_DIRECTORY, f))

    if '{{ cookiecutter.project_license }}' == 'marketplace':
        doc_files_to_delete = ['github.md', 'docstrings.rst', 'add_on_installation.rst', 'backend_calculations.rst',
                               'seeq_server_interactions.rst', 'user_interface.rst']
        for f in doc_files_to_delete:
            remove_file(os.path.join(PROJECT_DIRECTORY, 'docs_src', 'source', f))


