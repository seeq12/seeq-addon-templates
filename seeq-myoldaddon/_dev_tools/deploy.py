from .utils import (
    DEPLOY_JSON_FILE,
    filter_element_paths,
    get_folders_from_args,
    get_element_paths_with_type,
    get_module,
    save_json
)


def deploy(args):
    save_json(DEPLOY_JSON_FILE, {'username': args.username, 'password': args.password, 'url': args.url})

    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    for element_path, element_type in target_elements.items():
        print(f'Deploying element: {element_path}')
        get_module(element_path, element_type).deploy(args)
