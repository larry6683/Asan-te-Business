from api.mapper.response_mapper import ResponseMapper
from api.mapper.command_mapper import CommandMapper
from converters.entity_converter import EntityConverter
from converters.resource_category_converter import ResourceCategoryConverter

from codegen.resource.create_resource_pb2 import CreateResourceRequest, CreateResourceResponse

from .create_resource_command import CreateResourceCommand, CreateResourceCommandResult

class CreateResourceMapper(
    CommandMapper[CreateResourceRequest, CreateResourceCommand],
    ResponseMapper[CreateResourceCommandResult, CreateResourceResponse]
):
    def to_command(request: CreateResourceRequest) -> CreateResourceCommand:
        return CreateResourceCommand(
            entity=EntityConverter.to_domain(request.auth),
            name=request.resource.name,
            description=request.resource.description,
            category=ResourceCategoryConverter.to_domain(request.resource.category)
        )

    def to_response(result: CreateResourceCommandResult) -> CreateResourceResponse:
        if result.errors:
            return CreateResourceResponse(
                errors=result.errors
            )

        return CreateResourceResponse(
            resource=CreateResourceResponse.Resource(
                id=result.resource_id
            )
        )