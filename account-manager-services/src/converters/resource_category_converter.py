from api.api_converter import ApiConverter
from database.models.resource import ResourceCategoryCode
from codegen.resource.resource_category_pb2 import ResourceCategory

class ResourceCategoryConverter(
    ApiConverter[ResourceCategoryCode, ResourceCategory]
):
    """
    Converter for ResourceCategoryCode domain enum and ResourceCategory protobuf enum.
    """

    def to_domain(input: ResourceCategory) -> ResourceCategoryCode:
        match input:
            case ResourceCategory.RESOURCE_CATEGORY_HARDWARE:
                return ResourceCategoryCode.HARDWARE
            
            case ResourceCategory.RESOURCE_CATEGORY_SOFTWARE:
                return ResourceCategoryCode.SOFTWARE
            
            case ResourceCategory.RESOURCE_CATEGORY_SERVICE:
                return ResourceCategoryCode.SERVICE
            
            case _:
                return None

    def to_api(input: ResourceCategoryCode) -> ResourceCategory:
        match input:
            case ResourceCategoryCode.HARDWARE:
                return ResourceCategory.RESOURCE_CATEGORY_HARDWARE

            case ResourceCategoryCode.SOFTWARE:
                return ResourceCategory.RESOURCE_CATEGORY_SOFTWARE

            case ResourceCategoryCode.SERVICE:
                return ResourceCategory.RESOURCE_CATEGORY_SERVICE

            case _:
                return ResourceCategory.RESOURCE_CATEGORY_UNSPECIFIED