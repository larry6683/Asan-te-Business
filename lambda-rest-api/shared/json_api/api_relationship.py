from json_api.api_links import ApiLinks
from json_api.api_resource_reference import ApiResourceReference

class ApiRelationship():
    def __init__(self, 
                links: ApiLinks, 
                data: ApiResourceReference | list[ApiResourceReference]):
        self.links = links
        self.data = data

    @staticmethod
    def create_api_relationship(
        base_url, 
        resource_type: str,
        resource_id: str, 
        relationship_type: str, 
        relationship_ids: list[str]
    ):
        return ApiRelationship(
        ApiLinks.create_relationship_links(
            base_url, f'{resource_type}/{resource_id}/{relationship_type}', resource_id, relationship_type
        ),
        [ApiResourceReference(relationship_type, id)for id in relationship_ids]
    )