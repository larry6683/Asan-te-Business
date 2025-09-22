from api.api_converter import ApiConverter
from domain import entity
from codegen.auth import entity_type_pb2

class EntityTypeConverter(ApiConverter[entity.EntityType, entity_type_pb2.EntityType]):
    """
    Converter for EntityType domain enum and EntityType protobuf enum.
    """

    def to_domain(input: entity_type_pb2.EntityType) -> entity.EntityType:
        match input:
            case entity_type_pb2.EntityType.ENTITY_BUSINESS:
                return entity.EntityType.BUSINESS
            
            case entity_type_pb2.EntityType.ENTITY_BENEFICIARY:
                return entity.EntityType.BENEFICIARY
            
            case entity_type_pb2.EntityType.ENTITY_CONSUMER:
                return entity.EntityType.CONSUMER
            
            case _:
                return None

    def to_api(input: entity.EntityType) -> entity_type_pb2.EntityType:
        match input:
            case entity.EntityType.BUSINESS:
                return entity_type_pb2.EntityType.ENTITY_BUSINESS

            case entity.EntityType.BENEFICIARY:
                return entity_type_pb2.EntityType.ENTITY_BENEFICIARY

            case entity.EntityType.CONSUMER:
                return entity_type_pb2.EntityType.ENTITY_CONSUMER

            case _:
                return None
