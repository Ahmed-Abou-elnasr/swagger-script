def add_gateway_responses_and_validators():
    """
    Returns a dictionary containing the `x-amazon-apigateway-gateway-responses`
    and `x-amazon-apigateway-request-validators` configurations.
    """
    gateway_responses = {
        "WAF_FILTERED": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201021",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "ACCESS_DENIED": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201001",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "INVALID_API_KEY": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201012",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "QUOTA_EXCEEDED": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201015",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "DEFAULT_4XX": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status": $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201007",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "API_CONFIGURATION_ERROR": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201002",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "INTEGRATION_FAILURE": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201010",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "BAD_REQUEST_PARAMETERS": {
            "statusCode": 400,
            "responseTemplates": {
                "application/json": (
                    '{\n  "status": $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201006",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "THROTTLED": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201018",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "AUTHORIZER_CONFIGURATION_ERROR": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201003",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "AUTHORIZER_FAILURE": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201004",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "MISSING_AUTHENTICATION_TOKEN": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201014",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "RESOURCE_NOT_FOUND": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201017",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "UNSUPPORTED_MEDIA_TYPE": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201020",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "INVALID_SIGNATURE": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201013",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "DEFAULT_5XX": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201008",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "REQUEST_TOO_LARGE": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201016",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "BAD_REQUEST_BODY": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201005",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "EXPIRED_TOKEN": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201009",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "INTEGRATION_TIMEOUT": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201011",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
        "UNAUTHORIZED": {
            "responseTemplates": {
                "application/json": (
                    '{\n  "status":  $context.status,\n  "title": $context.error.messageString,\n'
                    '  "code": "E201019",\n  "detail": $context.error.messageString\n}'
                )
            }
        },
    }

    request_validators = {
        "Validate body, query string parameters, and headers": {
            "validateRequestParameters": True,
            "validateRequestBody": True,
        }
    }

    return {
        "x-amazon-apigateway-gateway-responses": gateway_responses,
        "x-amazon-apigateway-request-validators": request_validators,
    }


def get_security_schemas():
    """
    Fetches default security schemas to be in this format.
      securitySchemes:
        api_key:
          type: "apiKey"
          name: "x-api-key"
          in: "header"
    :return:
    """
    security_schemas = {
        "securitySchemes": {
            "api_key": {
                "type": "apiKey",
                "name": "x-api-key",
                "in": "header"
            }
        }
    }
    return security_schemas
