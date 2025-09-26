from api.mapper.response_mapper import ResponseMapper
from api.mapper.command_mapper import CommandMapper
from converters.business_converter import BusinessConverter

from codegen.business.create_business_pb2 import CreateBusinessRequest, CreateBusinessResponse

from .create_business_command import CreateBusinessCommand, CreateBusinessCommandResult

class CreateBusinessMapper(
    CommandMapper[CreateBusinessRequest, CreateBusinessCommand],
    ResponseMapper[CreateBusinessCommandResult, CreateBusinessResponse]
):
    @classmethod
    def to_command(cls, request: CreateBusinessRequest) -> CreateBusinessCommand:
        return CreateBusinessCommand(
            business_name=request.business.business_name,
            email=request.business.email,
            website_url=request.business.website_url if request.business.website_url else None,
            phone_number=request.business.phone_number if request.business.phone_number else None,
            location_city=request.business.location_city if request.business.location_city else None,
            location_state=request.business.location_state if request.business.location_state else None,
            ein=request.business.ein if request.business.ein else None,
            business_description=request.business.business_description if request.business.business_description else "",
            business_size=request.business.business_size if request.business.business_size else "SMALL",
            user_email=request.user_email if request.user_email else None
        )

    @classmethod
    def to_response(cls, result: CreateBusinessCommandResult) -> CreateBusinessResponse:
        if result.errors:
            return CreateBusinessResponse(
                errors=result.errors
            )

        return CreateBusinessResponse(
            business=CreateBusinessResponse.Business(
                id=result.business.id,
                business_name=result.business.business_name,
                email=result.business.email,
                website_url=result.business.website_url or "",
                phone_number=result.business.phone_number or "",
                location_city=result.business.location_city or "",
                location_state=result.business.location_state or "",
                ein=result.business.ein or "",
                business_description=result.business.business_description,
                business_size=BusinessConverter.business_size_to_string(result.business.business_size)
            )
        )
