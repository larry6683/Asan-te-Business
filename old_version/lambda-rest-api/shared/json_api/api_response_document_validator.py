from json_api.api_document import ApiDocument
from json_api.api_resource import ApiResource
from json_api.api_links import ApiLinks
from utils import Utils

# todo: add relevant error codes...
class ApiResponseDocumentValidator():
    """
        this validator will return a list of error messages
    """
    @staticmethod
    def validate_api_response_document(document: ApiDocument | dict) -> list[str]:
        document = Utils.obj_to_dict(document)
        validation_errors: list[str] = []

        data = document.get('data')
        meta = document.get('meta')
        links = document.get('links')
        errors = document.get('errors')
        included = document.get('included')

        if data is None and meta is None and errors is None:
            validation_errors.append("api response: one of the following fields must be included: 'data', 'meta', 'errors'")
        
        if (data is not None and errors is not None):
            validation_errors.append("api response: both 'data' and 'errors cannot be supplied in the same document")
        
        if included is not None and data is None:
            validation_errors.append("api response: having an 'included' object requires a 'data' object")

        if meta is not None and not meta:
            validation_errors.append("api response: meta is defined but contains no information.")
        
        if 'links' in document and not document.get('links'):
            validation_errors.append("api response: links object present but it includes no information")

        if links and (not data and not meta and not errors):
            validation_errors.append('api response: links object present but no other document info present')
        
        if "data" in document:
            if isinstance(data, list):
                for resource in data:
                    if resource is None:
                        validation_errors.append('api response: resource lists may not contain null values')
                    else:
                        validation_errors.extend(ApiResponseDocumentValidator.validate_api_resource(resource))
            elif data is not None:
                error = ApiResponseDocumentValidator.validate_api_resource(data)
                if (error): validation_errors.extend(error)
            
            # this is our rule, not necessarily a specification rule.
            # even null data must have a self-link
            if links is None:
                validation_errors.append('api response: api: responses with data must include a link')
            elif not links.get('self'):
                # this is our rule, not a rule of json:api
                # there is no pagination validation: be careful.
                validation_errors.append('api response: resource linkage response must include a self attribute')
        
        return validation_errors

    # yes this is duplicated from api_request_document_validator
    # but different rules may apply here.
    @staticmethod
    def validate_api_resource(resource: ApiResource | dict) -> list[str]:
        resource: dict = Utils.obj_to_dict(resource)
        validation_errors: list[str] = []
        
        if 'type' not in resource:
            validation_errors.append("api response: resource in 'data' must include a type")
        elif not resource.get('type'):
            validation_errors.append("api response: resource in 'data' must have a type value")

        if 'id' not in resource:
            validation_errors.append("api response: resource in 'data' must include an id")
        if not resource.get('id'):
            validation_errors.append("api response: resource in 'data' must have an id value")

        if 'attributes' in resource and not resource.get('attributes'):
            validation_errors.append("api response: resource in data has attributes but no information")

        # I don't quite understand the relationships object right now
        # please be careful if you are it in your response!
        # TODO: write relationships validation

        return validation_errors
