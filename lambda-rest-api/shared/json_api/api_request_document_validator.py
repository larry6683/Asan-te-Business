from json_api.api_document import ApiDocument
from json_api.api_resource import ApiResource
from utils import Utils

# todo: add relevant error codes...
class ApiRequestDocumentValidator():
    """
        this validator will return a list of error messages
    """
    @staticmethod
    def validate_request(document) -> list[str]:
        validation_errors: list[str] = []
        document = Utils.obj_to_dict(document)
        
        # see if 'data' field exists. stop here if it does not
        if 'data' not in document:
            validation_errors.append("api request: document must include a data object")
            return validation_errors
        
        data = document.get('data')
        if data is None:
            validation_errors.append("api request: data field may not be null. try using a delete request")
            return validation_errors
        
        invalid_keys = set(document) - set(['data'])
        if len(invalid_keys):
            validation_errors.append(f'api request: document keys not supported: {invalid_keys}')

        if isinstance(data, list):
            for resource in data:
                if resource is None:
                    validation_errors.append('api request: resource lists may not contain null values')
                else:
                    validation_errors.extend(ApiRequestDocumentValidator.validate_api_resource(resource))
            else:
                error = ApiRequestDocumentValidator.validate_api_resource(data)
                if error: validation_errors.append(error)
        
        return []
    
    # yes this is duplicated from api_response_document_validator
    # but different rules may apply here.
    @staticmethod
    def validate_api_resource(resource: dict) -> list[str]:
        validation_errors = [str]
        
        if 'type' not in resource:
            validation_errors.append("api request: resource in 'data' must include a type")
        elif not resource.get('type'):
            validation_errors.append("api request: resource in 'data' must have a type value")

        if 'id' in resource:
            validation_errors.append("api request: resource in 'data' may not specify an id manually")

        if 'relationships' in resource:
            validation_errors.append('api request: updating resource relationships not supported')

        return validation_errors