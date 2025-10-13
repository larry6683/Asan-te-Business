from typing import Self

from json_api.api_resource import ApiResource
from json_api.api_links import ApiLinks
from json_api.api_error import ApiError
from utils import Utils

class ApiDocument:
    """
        data may be a dict or a ApiResource object
        meta may contain any properties
        included must be a list of dicts or api resources
        errors must be a list of errors
    """
    def __init__(self, 
                data: ApiResource | list[ApiResource] | dict = None,
                links: ApiLinks | dict = None,
                meta:dict=None,
                included: list[ApiResource]=None,
                errors:list=None):
        self.data = data
        self.links = links
        self.meta = meta
        self.included = included
        self.errors = errors

    def to_dict(self):
        doc_dict = {}
        # ensure to validate! Errors + data/meta is not allowed!
        # this method is dumb!
        if self.links is not None: doc_dict['links'] = self.links
        if self.data is not None: doc_dict['data'] = self.data
        if self.meta is not None: doc_dict['meta'] = self.meta
        if self.included is not None: doc_dict['included'] = self.included
        if self.errors is not None: doc_dict['errors'] = self.errors
        return Utils.obj_to_dict(doc_dict)
    
    def from_dict(document_dict: dict) -> Self:
        return ApiDocument(
            document_dict.get('data'),
            document_dict.get('links'),
            document_dict.get('meta'),
            document_dict.get('included'),
            document_dict.get('errors'),
        )
    
    @staticmethod
    def from_obj(document_obj) -> Self:
        return ApiDocument.from_dict(Utils.obj_to_dict(document_obj))

    # to call this method from a list, do: create_error_api_document(*list)
    @staticmethod
    def create_error_api_document(*errors: ApiError) -> Self:
        return ApiDocument(errors=[errors])