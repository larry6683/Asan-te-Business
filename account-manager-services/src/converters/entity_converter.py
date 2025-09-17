from api.api_converter import ApiConverter
from .entity_type_converter import EntityTypeConverter
from domain.entity import Entity
from codegen.auth.auth_pb2 import Auth

class EntityConverter(ApiConverter[Entity, Auth]):
    """
    Converter for Entity domain type and Auth protobuf message.
    """

    def to_domain(input: Auth) -> Entity:
        return Entity(
            id=input.entity.id,
            type=EntityTypeConverter.to_domain(input.entity.entity_type),
        )