import yaml


def load_template(file_path):
    """Load a YAML template file into a Python dictionary."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def save_yaml(file_path, data):
    """Save a Python dictionary as a YAML file."""
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)


def replace_placeholders(template_data, placeholders, query_params, path_param):
    """
    Replace placeholders in the template data with provided values.
    Add query parameters and path parameters dynamically.
    """
    # Convert the template to a string for placeholder replacement
    template_str = yaml.dump(template_data)

    # Replace general placeholders
    for placeholder, value in placeholders.items():
        template_str = template_str.replace(f"<{placeholder}>", value)

    # Convert back to a dictionary
    filled_template = yaml.safe_load(template_str)

    # Add query parameters to the parameters section
    if query_params:
        for param_name, param_details in query_params.items():
            param_entry = {
                "name": param_name,
                "in": "query",
                "schema": {
                    "type": param_details["type"]
                }
            }
            if "required" in param_details:
                param_entry["required"] = param_details["required"]
            filled_template[
                placeholders["put the new endpoint path here as per the swagger, same as swagger, no changes"]][
                placeholders[
                    "here put the endpoint http method e.g. get, post or put - Make sure all lowercase letter"]][
                "parameters"].append(param_entry)

    # Add query parameters to requestParameters
    if query_params:
        for param_name in query_params.keys():
            filled_template[
                placeholders["put the new endpoint path here as per the swagger, same as swagger, no changes"]][
                placeholders[
                    "here put the endpoint http method e.g. get, post or put - Make sure all lowercase letter"]][
                "x-amazon-apigateway-integration"]["requestParameters"][
                f"integration.request.querystring.{param_name}"] = f"method.request.querystring.{param_name}"

    # Add path parameter to requestParameters
    if path_param:
        filled_template[placeholders["put the new endpoint path here as per the swagger, same as swagger, no changes"]][
            placeholders["here put the endpoint http method e.g. get, post or put - Make sure all lowercase letter"]][
            "x-amazon-apigateway-integration"]["requestParameters"][
            f"integration.request.path.{path_param}"] = f"method.request.path.{path_param}"

    return filled_template


def generate_yaml_from_template(template_file, output_file, placeholders, query_params=None, path_param=None):
    """
    Generate a YAML file by replacing placeholders in a template.

    :param template_file: Path to the input YAML template file.
    :param output_file: Path to the output YAML file.
    :param placeholders: A dictionary of placeholder-value pairs to replace in the template.
    :param query_params: A dictionary of query parameters to add (e.g., {"filter": {"type": "string", "required": True}}).
    :param path_param: The name of the path parameter (e.g., "resourceId").
    """
    # Load the template as a YAML dictionary
    template_data = load_template(template_file)

    # Replace placeholders and add query/path parameters
    filled_template = replace_placeholders(template_data, placeholders, query_params, path_param)

    # Save the filled template as a YAML file
    save_yaml(output_file, filled_template)
    print(f"Template filled and saved to {output_file}")


# Example usage
if __name__ == "__main__":
    # Define the input template file and output file
    template_file = "template.yaml"
    output_file = "filled_template.yaml"

    # Define the placeholders and their values
    placeholders = {
        "put the new endpoint path here as per the swagger, same as swagger, no changes": "/api/v1/resource",
        "here put the endpoint http method e.g. get, post or put - Make sure all lowercase letter": "get",
        "put the operation id for the endpoint same as swagger": "getResource",
        "Put the name of the resource defined in $root.components.schemas that maps the endpoint request body": "RequestResource",
        "Put the name of the resource defined in $root.components.schemas that maps the endpoint response body": "ResponseResource",
        "Put the vpc connection ID here as per the stage used": "vpc-12345678",
        "here put the endpoint http method e.g. GET, POST or PUT - Make sure all uppercase letters": "GET",
        "put the backend API URL here": "https://backend.example.com/api",
        "put the front end-url here as per stage": "https://frontend.example.com",
        "if any, add the query parameter name here and replicate this parameter entry for as many parameters the endpoint have": "queryParam",
        "query parameter type e.g. string or integer": "string",
        "Path parameter field name": "resourceId",
        "Query string field name": "filter"
    }

    # Define query parameters (name: {type: <type>, required: <true/false>})
    query_params = {
        "filter": {"type": "string", "required": True},
        "sort": {"type": "string", "required": False}
    }

    # Define the path parameter
    path_param = "resourceId"

    # Generate the YAML file
    generate_yaml_from_template(template_file, output_file, placeholders, query_params, path_param)
