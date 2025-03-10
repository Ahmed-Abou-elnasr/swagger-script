import yaml
from collections.abc import MutableMapping


def deep_merge(d1, d2):
    """
    Recursively merge two dictionaries.

    Args:
        d1 (dict): The first dictionary.
        d2 (dict): The second dictionary.

    Returns:
        dict: The merged dictionary.
    """
    for key, value in d2.items():
        if key in d1:
            if isinstance(d1[key], MutableMapping) and isinstance(value, MutableMapping):
                deep_merge(d1[key], value)
            else:
                d1[key] = value
        else:
            d1[key] = value
    return d1


def merge_yaml(remote_api, new_api):
    """
    Merge two YAML files (remote_api and new_api) while ensuring the resulting YAML
    structure is similar to the skeleton of the provided YAML file.

    Args:
        remote_api (dict): The remote API YAML content as a dictionary.
        new_api (dict): The new API YAML content as a dictionary.

    Returns:
        dict: The merged YAML content as a dictionary.
    """
    # Merge components and paths from new_api into remote_api
    if 'components' in new_api:
        if 'components' in remote_api:
            deep_merge(remote_api['components'], new_api['components'])
        else:
            remote_api['components'] = new_api['components']

    if 'paths' in new_api:
        if 'paths' in remote_api:
            deep_merge(remote_api['paths'], new_api['paths'])
        else:
            remote_api['paths'] = new_api['paths']

    return remote_api


def load_yaml(file_path):
    """
    Load a YAML file into a Python dictionary.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: The YAML content as a dictionary.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def save_yaml(data, file_path):
    """
    Save a Python dictionary to a YAML file.

    Args:
        data (dict): The dictionary to save as YAML.
        file_path (str): Path to save the YAML file.
    """
    with open(file_path, 'w') as file:
        yaml.dump(data, file, sort_keys=False)
