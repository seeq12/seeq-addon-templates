from _dev_tools.utils import (
    filter_element_paths,
    get_element_paths_with_type,
    get_folders_from_args,
    get_module,
    topological_sort
)


def build(args=None):
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    build_dependencies = {element_path: get_module(element_path, element_type).get_build_dependencies()
                          for element_path, element_type in target_elements.items()}
    sorted_elements = topological_sort(build_dependencies)
    sorted_elements_with_types = {element_path: target_elements[element_path] for element_path in sorted_elements}
    for element_path, element_type in sorted_elements_with_types.items():
        print(f'Building element: {element_path}')
        get_module(element_path, element_type).build()
