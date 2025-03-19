
import yaml

import utils as utils


def format_swagger_to_template(input_yaml_path, output_path, frontend_url, vpc_connection_id, info_title,
                               info_description, info_version, servers_url, base_path_default):
    """
    Transforms a Swagger YAML file into AWS API Gateway format using a template.
    Args:
        input_yaml_path (str): Path to the input Swagger YAML file
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

    # Add custom representers (converters)
    yaml.add_representer(utils.QuotedString, utils.QuotedString.quoted_string_representer)
    yaml.add_representer(utils.FlowStyleList, utils.FlowStyleList.flow_style_representer)


    swagger_data = process_components(swagger_data)



    output_data = {
        'openapi': swagger_data.get('openapi', '3.0.1'),
        'info': {
            k: v for k, v in {
                'title': info_title,
                'description': info_description,
                'version': info_version
            }.items() if v
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
        'components': swagger_data.get('components', {}),
        'x-amazon-apigateway-gateway-responses': {
            "AUTHORIZER_CONFIGURATION_ERROR": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201003\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "EXPIRED_TOKEN": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201009\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "MISSING_AUTHENTICATION_TOKEN": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201014\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "BAD_REQUEST_PARAMETERS": {
                "statusCode": 400,
                "responseTemplates": {
                    "application/json": "{\n  \"status\": $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201006\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "DEFAULT_4XX": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\": $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201007\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "WAF_FILTERED": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201021\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "AUTHORIZER_FAILURE": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201004\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "RESOURCE_NOT_FOUND": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201017\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "THROTTLED": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201018\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "UNAUTHORIZED": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201019\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "REQUEST_TOO_LARGE": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201016\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "INVALID_SIGNATURE": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201013\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "API_CONFIGURATION_ERROR": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201002\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "UNSUPPORTED_MEDIA_TYPE": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201020\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "INTEGRATION_FAILURE": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201010\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "QUOTA_EXCEEDED": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201015\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "ACCESS_DENIED": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201001\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "INVALID_API_KEY": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201012\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "BAD_REQUEST_BODY": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201005\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "DEFAULT_5XX": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201008\",\n  \"detail\": $context.error.messageString\n}"
                }
            },
            "INTEGRATION_TIMEOUT": {
                "responseTemplates": {
                    "application/json": "{\n  \"status\":  $context.status,\n  \"title\": $context.error.messageString,\n  \"code\": \"E201011\",\n  \"detail\": $context.error.messageString\n}"
                }
            }
        },
        'x-amazon-apigateway-request-validators': {
            'Validate body, query string parameters, and headers': {
                'validateRequestParameters': True,
                'validateRequestBody': True
            }
        }
    }


    output_data = process_paths(swagger_data, output_data, frontend_url, vpc_connection_id)

    output_data = utils.convert_str_values_to_quoted_strings(output_data)
    with open(output_path, 'w') as file:
        yaml.dump(output_data, file, sort_keys=False, Dumper=utils.ListIndentDumper)

    print(f"Output YAML file saved to: {output_path}")

def process_paths(swagger_data: dict, output_data: dict, frontend_url: str, vpc_connection_id: str):
    to_be_deleted_schemas = set()
    for path, methods in swagger_data['paths'].items():
        output_data['paths'][path] = {}

        path_parameters = {}
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
                    swagger_data,
                    to_be_deleted_schemas
                )
                output_data['paths'][path][method] = method_config

                for param in operation.get('parameters', []):
                    if param['in'] == 'path':
                        path_param = {
                            'name': param['name'],
                            'in': 'path',
                            'required': True,
                            'schema': {
                                'type': param['schema']['type']  # Add the corresponding type if present
                            }
                        }
                        path_parameters[param['name']] = path_param

        path_methods = [key.upper() for key in methods.keys() if key.lower() != "options"]
        # Add OPTIONS method with path variables dynamically fetched from path parameters
        options_config = create_options_method(path_methods, frontend_url)

        if len(path_parameters) != 0:
            options_config = {"parameters": list(path_parameters.values()),
                              **{k: v for k, v in options_config.items() if k != 'parameters'}}

        output_data['paths'][path]['options'] = options_config

    output_data = delete_unused_schemas(to_be_deleted_schemas, output_data)

    return output_data

def process_components(swagger_data: dict) -> dict:
    add_security_schemes(swagger_data['components'])
    modified_data = modify_x_prefixed_fields(swagger_data)

    return modified_data

def add_security_schemes(components_dict: dict) -> dict:
    components_dict['securitySchemes'] = {
        'api_key': {
            'type': 'apiKey',
            'name': 'x-api-key',
            'in': 'header'
        }
    }

    return components_dict


def delete_unused_schemas(to_be_deleted_schemas: set[str], swagger_data: dict):
    def is_schema_used(schema_name: str, data: dict) -> bool:
        """
        Recursively search the dictionary for references to the given schema.
        """
        ref_string = f"#/components/schemas/{schema_name}"

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and ref_string in value:
                    return True
                if isinstance(value, (dict, list)) and is_schema_used(schema_name, value):
                    return True
        elif isinstance(data, list):
            for item in data:
                if is_schema_used(schema_name, item):
                    return True

        return False

    print(f"Deleting {len(to_be_deleted_schemas)} marked as unused schemas(s) but will be checked first.")
    print(to_be_deleted_schemas)
    for schema_component in to_be_deleted_schemas.copy():
        if not is_schema_used(schema_component, swagger_data):
            swagger_data["components"]["schemas"].pop(schema_component, None)
            to_be_deleted_schemas.remove(schema_component)

    if len(to_be_deleted_schemas) > 0:
        print(f"There is {len(to_be_deleted_schemas)} detected as unused schema(s) that haven't been deleted")
        print(to_be_deleted_schemas)
    return swagger_data


def modify_x_prefixed_fields(data):
    remove_x_prefix_from_fields = {"x-minLength", "x-maxLength", "x-minimum", "x-maximum", "x-min", "x-max"}
    discarded_fields = {"x-message", "example"}

    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if k in discarded_fields:
                continue
            if k.startswith("x-"):
                if k in remove_x_prefix_from_fields:
                    new_key = k[2:]  # Remove "x-" prefix
                    if new_key in ["min", "max"]:
                        new_key += "imum" # change "min" to "minimum" and "max" to "maximum"
                    new_data[new_key] = v
                elif k == "x-allowedStrings" or k == "enum": # modify to flow style list
                    new_data["enum"] = v if not isinstance(v, list) else utils.FlowStyleList(v)
                elif k not in discarded_fields:
                    new_data[k] = modify_x_prefixed_fields(v)
            elif k not in discarded_fields:
                new_data[k] = modify_x_prefixed_fields(v)

        return new_data
    elif isinstance(data, list):
        return [modify_x_prefixed_fields(v) for v in data]
    else:
        return data


def create_method_config(path, operation, method, frontend_url, vpc_connection_id, swagger_data,
                         to_be_deleted_schemas: set[str]):
    """Creates the method configuration based on the template."""
    is_empty_success_response = is_empty_response(operation)
    method_config = {
        'operationId': operation.get('operationId', ''),
        'parameters': [],
        'requestBody': operation.get('requestBody', {}),
        'responses': {
            utils.QuotedString("404"): create_error_response("404"),
            utils.QuotedString("200"): create_success_response(operation, is_empty_success_response),
            utils.QuotedString("400"): create_error_response("400"),
            utils.QuotedString("401"): create_error_response("401"),
            utils.QuotedString("500"): create_error_response("500"),
            utils.QuotedString("403"): create_error_response("403")
        },
        'security': [{'api_key': []}],
        'x-amazon-apigateway-request-validator': 'Validate body, query string parameters, and headers'
    }

    # Add standard headers
    standard_headers = [
        {'name': 'x-trace-id', 'in': 'header', 'required': True, 'schema': {'type': 'string'}},
        {'name': 'Content-Type', 'in': 'header', 'schema': {'type': 'string'}},
        {'name': 'Accept-Language', 'in': 'header', 'schema': {'type': 'string'}},
        {'name': 'User-Agent', 'in': 'header', 'schema': {'type': 'string'}},
        {'name': 'Authorization', 'in': 'header', 'required': True, 'schema': {'type': 'string'}},
        {'name': 'cookie', 'in': 'header', 'schema': {'type': 'string'}},
        {'name': 'x-forward-for', 'in': 'header', 'schema': {'type': 'string'}}
    ]
    method_config['parameters'].extend(standard_headers)

    path_parameters = []
    # Add any additional parameters from the operation
    if 'parameters' in operation:
        for param in operation['parameters']:
            if param['in'] == 'query':
                if 'schema' in param and '$ref' in param['schema']:
                    ref = param['schema']['$ref']
                    resolved_params = resolve_ref(ref, swagger_data, to_be_deleted_schemas)
                    method_config['parameters'].extend(resolved_params)
            if param['in'] == 'path':
                path_parameters.append(param)

    if 'requestBody' not in operation:
        method_config.pop('requestBody', None)

    # Add integration configuration
    method_config['x-amazon-apigateway-integration'] = create_integration_config(
        path,
        method,
        frontend_url,
        vpc_connection_id,
        path_parameters,
        is_empty_success_response
    )
    return method_config


def create_integration_config(path, method, frontend_url, vpc_connection_id, parameters, is_empty_success_response: bool):
    """Creates the API Gateway integration configuration."""
    integration = {
        'connectionId': vpc_connection_id,
        'httpMethod': method.upper(),
        'uri': 'https://${stageVariables.url}' + path[:3] + "/api" + path[3:],  # This will be set by the API Gateway
        'responses': {
            '^200$': {
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Credentials': '\'true\'',
                    'method.response.header.Access-Control-Allow-Origin': f"{frontend_url}"
                },
                'responseTemplates': {
                    'application/json': "#set($inputRoot = $input.path('$'))"
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

    if not is_empty_success_response:
        integration['responses']['^200$'].pop("responseTemplates", None)

    error_response_regex_to_status_code_dict = {
        "^500$": "500",
        "^400$": "400",
        "^401$|^302$": "401",
        "^404$": "404",
        "^403$": "403"
    }
    for regex, code in error_response_regex_to_status_code_dict.items():
        integration['responses'][regex] = {
            'statusCode': code,
            'responseParameters': {
                'method.response.header.Access-Control-Allow-Credentials': '\'true\'',
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


def create_options_method(allowed_methods: list[str], frontend_url: str):
    """Creates the OPTIONS method configuration for CORS."""
    return {
        'responses': {
            utils.QuotedString("200"): {
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
                        'method.response.header.Access-Control-Allow-Credentials': '\'true\'',
                        'method.response.header.Access-Control-Allow-Methods': f"\'{",".join(allowed_methods)},OPTIONS\'",
                        'method.response.header.Access-Control-Allow-Headers': "\'x-trace-id,x-api-key,Authorization,"
                                                                               "Cache-Control,Content-Type\'",
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


def create_error_response(status_code: str):
    """Creates a standard error response configuration."""
    return {
        'description': f"{status_code} response",
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


def create_success_response(operation, is_empty_success_response: bool):
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
        if 'content' in response_200 and not is_empty_success_response:
            response['content'] = response_200['content']

    return response


def is_empty_response(operation: dict) -> bool:
    """
    Checks if the 200 response is an EmptyResponse or not.
    Expected structure:
        operation =  {
            "responses : {
                "200" : {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/EmptyResponse"
                            }
                        }
                    }
                }
            }
        }

    :param operation: The operation dictionary.
    :return: True if the response references EmptyResponse, otherwise False.
    """
    try:
        return (
                "#/components/schemas/EmptyResponse" in
                operation.get("responses", {})
                .get("200", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema", {})
                .get("$ref", "")
        )
    except AttributeError:
        return False



def resolve_ref(ref, swagger_data, to_be_deleted_schemas: set[str]):
    """Resolves a $ref in the Swagger data."""
    ref_path = ref.split('/')[1:]  # Split and remove the initial '#'
    ref_data = swagger_data
    for part in ref_path:
        ref_data = ref_data[part]

    # Transform the resolved reference to only include parts in quotes
    transformed_ref = []
    required_fields = ref_data.get('required', [])

    def resolve_nested_schema(prefix: str, schema: dict):
        """ Recursively resolve nested schemas."""
        if "$ref" in schema:
            nested_schema_name = schema["$ref"].split("/")[-1]
            nested_schema = swagger_data["components"]["schemas"].get(nested_schema_name, {})
            for nested_key, nested_value in nested_schema.get("properties", {}).items():
                resolve_nested_schema(f"{prefix}.{nested_key}", nested_value)
            to_be_deleted_schemas.add(nested_schema_name)
        else:
            param = {
                'name': prefix,
                'in': 'query',
                'schema': {
                    'type': schema.get('type', 'string')  # Default type is string if missing
                }
            }
            if prefix.split(".")[-1] in required_fields:
                param['required'] = True
            transformed_ref.append(param)

    for key, value in ref_data.get('properties', {}).items():
        resolve_nested_schema(key, value)

    to_be_deleted_schemas.add(ref_path[-1])

    return transformed_ref

if __name__ == "__main__":
    input_yaml_path = "./input/product-env-dev-swagger.yaml"
    output_path = "./output/test-newgateway-generator.yaml"
    frontend_url = "'http://localhost:5173'"
    vpc_connection_id = "k7rzkd"
    info_title = "backoffice-products-configurations-api"
    info_description = ""
    info_version = "1.0"
    servers_url = "https://alrajhi.api-gateway.api.dev-arbm.com/{basePath}"
    base_path_default = "boproduct-dev"
    format_swagger_to_template(
        input_yaml_path=input_yaml_path,
        output_path=output_path,
        frontend_url=frontend_url,
        vpc_connection_id=vpc_connection_id,
        info_title=info_title,
        info_description=info_description,
        info_version=info_version,
        servers_url=servers_url,
        base_path_default=base_path_default
    )



