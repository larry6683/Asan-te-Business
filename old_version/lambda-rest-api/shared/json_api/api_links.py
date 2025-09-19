from typing import Self
from urllib.parse import urljoin
from functools import reduce

class ApiLinks():
    @staticmethod
    def create_pagination_links(self_link, first=None, last=None, prev=None, next=None) -> Self:
        return {
            'self': self_link,
            'first': first,
            'last': last,
            'prev': prev,
            'next': next
        }
    
    @staticmethod
    def create_relationship_links(base_url, route: str, id: str, related_resource_type: str, pagination_params=None):
        # pagination not supported
        return {
            'self': ApiLinks.format_relationship_self_link(base_url, route, id, related_resource_type),
            'related': ApiLinks.format_relationship_related_link(base_url, route, id, related_resource_type)
        }
    
    @staticmethod
    def create_included_self_link(base_url, route: str, id: str, related_resource_type: str, related_resource_id: str):
        # this method exists to eliminate confusion with calling format_relationship_related_link
        return {
            'self': ApiLinks.format_relationship_related_link(base_url, route, id, related_resource_type)
        }
    
    @staticmethod
    def format_self_link(base_url, route: str, id: str = None):
        if id: route = "/".join((route.strip("/"), id))
        return urljoin(base_url, route)
    
    @staticmethod
    def format_relationship_self_link(base_url, route: str, id: str, related_resource_type: str):
        route = "/".join((route.strip("/"), id, "relationship", related_resource_type))
        return urljoin(base_url, route)
    
    @staticmethod
    def format_relationship_related_link(base_url, route: str, id: str, related_resource_type: str):
        route = "/".join((route.strip("/"), id, related_resource_type))
        return urljoin(base_url, route)