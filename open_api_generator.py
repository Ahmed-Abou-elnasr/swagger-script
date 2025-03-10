import json
import yaml


def add_headers_and_security_to_swagger(swagger_data):
    # Define the headers to be added
    headers = [
        {"name": "x-trace-id", "in": "header", "required": True, "schema": {"type": "string"}},
        {"name": "User-Agent", "in": "header", "schema": {"type": "string"}},
        {"name": "Content-Type", "in": "header", "schema": {"type": "string"}},
        {"name": "Accept-Language", "in": "header", "schema": {"type": "string"}},
        {"name": "x-forward-for", "in": "header", "schema": {"type": "string"}}
    ]
    # Add headers and security to each endpoint
    for path, path_item in swagger_data["paths"].items():
        for operation, operation_item in path_item.items():
            if operation in ["get", "post", "put", "delete", "patch"]:
                if "parameters" not in operation_item:
                    operation_item["parameters"] = []
                operation_item["parameters"].extend(headers)
                operation_item["security"] = [{"bearerAuth": []}, {"apiKeyHeader": []}]
    # Add security schemes to components
    swagger_data["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        },
        "api_key": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key"
        }
    }


def remove_empty_responses(swagger_data):
    # Remove 200 OK responses with EmptyResponse
    for path, path_item in swagger_data["paths"].items():
        for operation, operation_item in path_item.items():
            if operation in ["get", "post", "put", "delete", "patch"]:
                if 'responses' in operation_item and '200' in operation_item['responses']:
                    response_200 = operation_item['responses']['200']
                    if 'content' in response_200:
                        if 'application/json' in response_200['content']:
                            schema_ref = response_200['content']['application/json'].get('schema', {}).get('$ref', '')
                            if schema_ref == '#/components/schemas/EmptyResponse':
                                del response_200['content']

    # Remove EmptyResponse from components
    if 'EmptyResponse' in swagger_data['components']['schemas']:
        del swagger_data['components']['schemas']['EmptyResponse']
    # Remove components prefixed with ResponseMessage
    response_message_keys = [key for key in swagger_data['components']['schemas'] if key.startswith('ResponseMessage')]
    for key in response_message_keys:
        del swagger_data['components']['schemas'][key]


def replace_aliases_with_names(swagger_data):
    # Replace aliases with names
    def replace_alias(item):
        if isinstance(item, list):
            return [replace_alias(i) for i in item]
        elif isinstance(item, dict):
            return {k.replace('&id', 'name'): replace_alias(v) for k, v in item.items()}
        else:
            return item

    return replace_alias(swagger_data)


def process_swagger_file(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r') as f:
        swagger_data = yaml.safe_load(f)
    # Add headers and security to the swagger data
    add_headers_and_security_to_swagger(swagger_data)
    # Remove empty responses from the swagger data
    remove_empty_responses(swagger_data)
    # Replace aliases with names
    swagger_data = replace_aliases_with_names(swagger_data)
    # Write the modified swagger data to the output YAML file
    with open(output_file, 'w') as f:
        yaml.dump(swagger_data, f, sort_keys=False)