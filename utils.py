import yaml

class QuotedString(str):
    """A custom string subclass to be used with pyYaml to dump values with double quotes"""

    @staticmethod
    def quoted_string_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')


class FlowStyleList(list):
    """
    A custom list type for lists that should be dumped in flow style.
    Flow style: [1, 2, 3]
    Block style:
        - 1
        - 2
        - 3
    """

    @staticmethod
    def flow_style_representer(dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

class ListIndentDumper(yaml.Dumper):
    """
    A custom dumper to force having an indentation before the items of a list with block style.
    Default behavior:
        block-style-list:
        - 1
        - 2
    Desired behavior after using this dumper:
        block-style-list:
          - 1
          - 2
    """
    def increase_indent(self, flow=False, indentless=False):
        return super(ListIndentDumper, self).increase_indent(flow, False)  # Forces proper list indentation



def convert_str_values_to_quoted_strings(in_yaml_data):
    """
    Modify the input YAML data to ensure all string values are double-quoted.
    It does that by adding a custom string subclass for values that should be quoted.
    Note that a custom representer should be added to the yaml object dumping the file
    like `yaml.add_representer(QuotedString, QuotedString.quoted_string_representer)`
    """


    if isinstance(in_yaml_data, dict):
        return {k: convert_str_values_to_quoted_strings(v) for k, v in in_yaml_data.items()}
    elif isinstance(in_yaml_data, list):
        return [convert_str_values_to_quoted_strings(v) for v in in_yaml_data]
    elif isinstance(in_yaml_data, str):
        return QuotedString(in_yaml_data)
    return in_yaml_data


def test_dumping_yaml_data():
    import yaml
    import os
    with open("./input/api-docs-product-env-dev.yaml", 'r') as file:
        in_data = yaml.safe_load(file)

    # Define a correct relative output path
    output_path = "./output/utils-output.yaml"  # Fixed path to be relative

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    yaml.add_representer(QuotedString, QuotedString.quoted_string_representer)
    in_data = convert_str_values_to_quoted_strings(in_data)

    # Write the cleaned output YAML
    with open(output_path, 'w') as file:

        yaml.dump(in_data, file, sort_keys=False, Dumper=ListIndentDumper)

    # Print the full absolute path
    print(f"YAML data dumped to: {os.path.abspath(output_path)}")





if __name__ == "__main__":
    test_dumping_yaml_data()
