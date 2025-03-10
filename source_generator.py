import json

import yaml
import re
import amazon_gateway_statics as amz_statics


def wrap_values_in_quotes(data):
    if isinstance(data, dict):
        return {k: wrap_values_in_quotes(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [wrap_values_in_quotes(v) for v in data]
    elif isinstance(data, (int, float)):
        return data
    elif isinstance(data, str):
        return f'"{data}"'
    else:
        return data


def modify_x_prefixed_fields(data):
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if k.startswith("x-"):
                if k in ["x-minLength", "x-maxLength", "x-minimum", "x-maximum", "x-min", "x-max"]:
                    new_key = k[2:]  # Remove "x-" prefix
                    if new_key in ["min", "max"]:
                        new_key += "imum"
                    new_data[new_key] = v
                elif k == "x-allowedStrings":
                    new_data["enum"] = v if not isinstance(v, list) else f"[{', '.join(map(repr, v))}]"
                # Ignore/discard x-message and example keys
                elif k not in ["x-message", "example"]:
                    new_data[k] = modify_x_prefixed_fields(v)
            elif k not in ["x-message", "example"]:
                new_data[k] = modify_x_prefixed_fields(v)
        return new_data
    elif isinstance(data, list):
        return [modify_x_prefixed_fields(v) for v in data]
    else:
        return data


def format_swagger_to_template(input_yaml_path, template_path, output_path, frontend_url, vpc_connection_id, info_title,
                               info_description, info_version, servers_url, base_path_default):
    """
    Transforms a Swagger YAML file into AWS API Gateway format using a template.
    Args:
        input_yaml_path (str): Path to the input Swagger YAML file
        template_path (str): Path to the template YAML file
        output_path (str): Path where the output YAML file will be saved
        frontend_url (str): Frontend URL to be used in CORS configurations
        vpc_connection_id (str): VPC Connection ID for API Gateway integration
        info_title (str): Title for the API (used in the `info` section)
        info_description (str): Description for the API (used in the `info` section)
        info_version (str): Version of the API (used in the `info` section)
        servers_url (str): Base URL for the API (used in the `servers` section)
        base_path_default (str): Default base path for the API (used in the `servers` section)
    """
    # Read the input Swagger YAML
    with open(input_yaml_path, 'r') as file:
        swagger_data = yaml.safe_load(file)

    # Read the template YAML
    with open(template_path, 'r') as file:
        template_data = yaml.safe_load(file)

    # Modify components by removing "message" and "example" keys, transforming "x-" prefixed keys
    if "components" in swagger_data:
        swagger_data["components"] = modify_x_prefixed_fields(wrap_values_in_quotes(swagger_data["components"]))

    # Initialize the output dictionary with the passed parameters
    output_data = {
        'openapi': swagger_data.get('openapi', '3.0.1'),
        'info': {
            'title': info_title,  # Use the passed info_title
            'description': info_description,  # Use the passed info_description
            'version': info_version  # Use the passed info_version
        },
        'servers': [
            {
                'url': servers_url,  # Use the passed servers_url
                'variables': {
                    'basePath': {
                        'default': base_path_default  # Use the passed base_path_default
                    }
                }
            }
        ],
        'paths': {},
        'components': swagger_data.get('components', {})
    }

    # Process each path in the swagger file
    for path, methods in swagger_data['paths'].items():
        output_data['paths'][path] = {}
        # Process each HTTP method
        for method, operation in methods.items():
            if method.lower() != 'options':  # Skip options method as it will be added later
                # Create the method configuration using the template
                method_config = create_method_config(
                    path,
                    operation,
                    method,
                    frontend_url,
                    vpc_connection_id,
                    swagger_data
                )
                output_data['paths'][path][method] = method_config

        # Add OPTIONS method with path variables dynamically fetched from path parameters
        options_config = create_options_method(method.upper(), frontend_url)

        path_parameters = []
        for param in operation.get('parameters', []):
            if param['in'] == 'path':
                path_param = {
                    'name': param['name'],
                    'in': 'path',
                    'required': 'true',
                    'schema': {
                        'type': param['schema']['type']  # Add the corresponding type if present
                    }
                }
                path_parameters.append(path_param)

        if len(path_parameters) != 0:
            options_config = {"parameters": path_parameters,
                              **{k: v for k, v in options_config.items() if k != 'parameters'}}

        output_data['paths'][path]['options'] = options_config

    # Add security schemes and gateway responses from the original swagger
    if 'securitySchemes' in swagger_data.get('components', {}):
        if 'bearerAuth' in swagger_data.get('components').get('securitySchemes'):
            swagger_data.get('components').get('securitySchemes').pop('bearerAuth')
        if 'apiKeyHeader' in swagger_data.get('components').get('securitySchemes'):
            output_data['components']['securitySchemes']['apiKeyHeader'] = \
                swagger_data['components']['securitySchemes']['apiKeyHeader']
        elif 'api_key' in swagger_data.get('components').get('securitySchemas'):
            output_data.get('components').pop('securitySchemes')
            output_data['components']['securitySchemes']['api_key'] = swagger_data['components']['securitySchemes'][
                'api_key']
    else:
        output_data['components']['securitySchemes'] = amz_statics.get_security_schemas()

    if 'x-amazon-apigateway-gateway-responses' in swagger_data:
        output_data['x-amazon-apigateway-gateway-responses'] = swagger_data['x-amazon-apigateway-gateway-responses']
    else:
        output_data['x-amazon-apigateway-gateway-responses'] = amz_statics.add_gateway_responses_and_validators()[
            'x-amazon-apigateway-gateway-responses']
    # Add request validators if present
    if 'x-amazon-apigateway-request-validators' in swagger_data:
        output_data['x-amazon-apigateway-request-validators'] = swagger_data['x-amazon-apigateway-request-validators']
    else:
        output_data['x-amazon-apigateway-request-validators'] = amz_statics.add_gateway_responses_and_validators()[
            'x-amazon-apigateway-request-validators']

    # Clean the output data
    cleaned_output_data = clean_yaml_file(output_data)

    # Write the cleaned output YAML
    with open(output_path, 'w') as file:
        yaml.dump(cleaned_output_data, file, sort_keys=False)

    print(f"Cleaned YAML file saved to: {output_path}")


def resolve_ref(ref, swagger_data):
    """Resolves a $ref in the Swagger data."""
    ref_path = ref.split('/')[1:]  # Split and remove the initial '#'
    ref_data = swagger_data
    for part in ref_path:
        ref_data = ref_data[part]

    # Transform the resolved reference to only include parts in quotes
    transformed_ref = []
    required_fields = ref_data.get('required', [])

    for key, value in ref_data.get('properties', {}).items():
        param = {
            'name': key,
            'in': 'query',
            'schema': {
                'type': value.get('type').replace("'\"", '').replace("\"'",'')  # Add the corresponding type if present
            }
        }
        if key in required_fields:
            param['required'] = 'true'
        transformed_ref.append(param)

    return transformed_ref


def create_method_config(path, operation, method, frontend_url, vpc_connection_id, swagger_data):
    """Creates the method configuration based on the template."""
    method_config = {
        'operationId': operation.get('operationId', ''),
        'parameters': [],
        'responses': {
            '404': create_error_response(),
            '200': create_success_response(operation),
            '400': create_error_response(),
            '401': create_error_response(),
            '500': create_error_response(),
            '403': create_error_response()
        },
        'security': [{'api_key': []}],
        'x-amazon-apigateway-request-validator': 'Validate body, query string parameters, and headers'
    }

    # Add standard headers
    standard_headers = [
        {'name': 'x-trace-id', 'in': 'header', 'required': 'true', 'schema': {'type': 'string'}},
        {'name': 'Content-Type', 'in': 'header', 'schema': {'type': 'string'}},
        {'name': 'Accept-Language', 'in': 'header', 'schema': {'type': 'string'}},
        {'name': 'User-Agent', 'in': 'header', 'schema': {'type': 'string'}},
        {'name': 'Authorization', 'in': 'header', 'required': 'true', 'schema': {'type': 'string'}},
        {'name': 'cookie', 'in': 'header', 'schema': {'type': 'string'}},
        {'name': 'x-forward-for', 'in': 'header', 'schema': {'type': 'string'}}
    ]
    method_config['parameters'].extend(standard_headers)

    # Add any additional parameters from the operation
    if 'parameters' in operation:
        for param in operation['parameters']:
            if param['in'] in ['query', "path"]:
                if 'schema' in param and '$ref' in param['schema']:
                    ref = param['schema']['$ref']
                    resolved_params = resolve_ref(ref, swagger_data)
                    method_config['parameters'].extend(resolved_params)
                else:
                    path_key = {'name': param['name'], 'in': 'path', 'required': 'true',
                                'schema': {'type': param['schema']['type']}}
                    method_config['parameters'].append(path_key)

    # Add request body if present
    if 'requestBody' in operation:
        method_config['requestBody'] = operation['requestBody']

    # Add integration configuration
    method_config['x-amazon-apigateway-integration'] = create_integration_config(
        path,
        method,
        frontend_url,
        vpc_connection_id,
        method_config['parameters']
    )
    return method_config


def create_integration_config(path, method, frontend_url, vpc_connection_id, parameters):
    """Creates the API Gateway integration configuration."""
    integration = {
        'connectionId': vpc_connection_id,
        'httpMethod': method.upper(),
        'uri': 'https://${stageVariables.url}' + path[:3] + "/api" + path[3:],  # This will be set by the API Gateway
        'responses': {
            '^200$': {
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Credentials': 'true',
                    'method.response.header.Access-Control-Allow-Origin': f"{frontend_url}"
                }
            }
        },
        'requestParameters': {
            'integration.request.header.Content-Type': 'method.request.header.Content-Type',
            'integration.request.header.x-forward-for': 'method.request.header.x-forward-for',
            'integration.request.header.x-trace-id': 'method.request.header.x-trace-id',
            'integration.request.header.cookie': 'method.request.header.cookie',
            'integration.request.header.Accept-Language': 'method.request.header.Accept-Language',
            'integration.request.header.Authorization': 'method.request.header.Authorization',
            'integration.request.header.User-Agent': 'method.request.header.User-Agent'
        },
        'connectionType': 'VPC_LINK',
        'passthroughBehavior': 'when_no_templates',
        'type': 'http'
    }

    # Add error responses
    error_codes = ['500', '400', '401', '404', '403']
    for code in error_codes:
        integration['responses'][f'^{code}$'] = {
            'statusCode': code,
            'responseParameters': {
                'method.response.header.Access-Control-Allow-Credentials': 'true',
                'method.response.header.Access-Control-Allow-Origin': f"{frontend_url}"
            }
        }

        # Add query string and path parameter mappings
        for param in parameters:
            if param['in'] == 'query':
                integration['requestParameters'][
                    f"integration.request.querystring.{param['name']}"] = f"method.request.querystring.{param['name']}"
            elif param['in'] == 'path':
                integration['requestParameters'][
                    f"integration.request.path.{param['name']}"] = f"method.request.path.{param['name']}"

    return integration


def create_options_method(allowed_method, frontend_url):
    """Creates the OPTIONS method configuration for CORS."""
    return {
        'responses': {
            '200': {
                'description': '200 response',
                'headers': {
                    'Access-Control-Allow-Origin': {'schema': {'type': 'string'}},
                    'Access-Control-Allow-Methods': {'schema': {'type': 'string'}},
                    'Access-Control-Allow-Credentials': {'schema': {'type': 'string'}},
                    'Access-Control-Allow-Headers': {'schema': {'type': 'string'}}
                },
                'content': {}
            }
        },
        'x-amazon-apigateway-integration': {
            'responses': {
                'default': {
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Credentials': 'true',
                        'method.response.header.Access-Control-Allow-Methods': f"{allowed_method},OPTIONS",
                        'method.response.header.Access-Control-Allow-Headers': "x-trace-id,x-api-key,Authorization,"
                                                                               "Cache-Control,Content-Type",
                        'method.response.header.Access-Control-Allow-Origin': f"{frontend_url}"
                    }
                }
            },
            'requestTemplates': {
                'application/json': '{"statusCode": 200}'
            },
            'passthroughBehavior': 'when_no_match',
            'type': 'mock'
        }
    }


def create_error_response():
    """Creates a standard error response configuration."""
    return {
        'description': 'error response',
        'headers': {
            'x-trace-id': {'schema': {'type': 'string'}},
            'Access-Control-Allow-Origin': {'schema': {'type': 'string'}},
            'Access-Control-Allow-Credentials': {'schema': {'type': 'string'}}
        },
        'content': {
            'application/json': {
                'schema': {'$ref': '#/components/schemas/ResponseHeader'}
            }
        }
    }


def create_success_response(operation):
    """Creates a success response configuration."""
    response = {
        'description': '200 response',
        'headers': {
            'x-trace-id': {'schema': {'type': 'string'}},
            'Access-Control-Allow-Origin': {'schema': {'type': 'string'}},
            'Access-Control-Allow-Credentials': {'schema': {'type': 'string'}}
        }
    }

    # Add response content if defined in the operation
    if 'responses' in operation and '200' in operation['responses']:
        response_200 = operation['responses']['200']
        if 'content' in response_200:
            response['content'] = response_200['content']

    return response


def clean_value(value):
    """
    Cleans a value by removing extra quotes, double quotes, or triple quotes,
    and adds double quotes if necessary.
    """
    if isinstance(value, str):
        #         # Step 1: Remove leading/trailing single or double quotes
        #         value = value.strip("'\"")
        #
        #         # Step 2: Replace ''' or '' with '
        #         value = value.replace("'''", "'").replace("''", "'")
        #
        #         # Step 3: Replace """ or "" with "
        #         value = value.replace('"""', '"').replace('""', '"')
        #
        #         Step 4: Replace '" or "' with "
        value = value.replace('"\'', '')
        value = value.replace('\'"', '')
        #
        #         # Step 5: Replace '[ or "[ with [
        value = value.replace("'[", '[')
        value = value.replace("\"[", '[')
        #
        #         # Step 6: Replace ]' or ]" with ]
        value = value.strip().replace("]'", "]")
        value = value.strip().replace("]\"", "]")
    #
    return value


def clean_yaml_file(data):
    """
    Cleans the values in the YAML data.
    """
    try:
        # Clean the values in the YAML data
        def clean_dict(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    clean_dict(value)  # Recursively clean nested dictionaries
                elif isinstance(value, list):
                    d[key] = [clean_value(item) for item in value]  # Clean list items
                else:
                    d[key] = clean_value(value)  # Clean scalar values

        if isinstance(data, dict):
            clean_dict(data)
        else:
            raise ValueError("The YAML file must contain a dictionary at the root level.")

        print("Cleaned YAML data.")
        return data

    except Exception as e:
        print(f"An error occurred: {e}")
