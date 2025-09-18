from api.mapper.response_mapper import ResponseMapper
from api.mapper.query_mapper import QueryMapper
from converters.user_converter import UserConverter

from codegen.user.get_user_by_email_pb2 import GetUserByEmailRequest, GetUserByEmailResponse

from .get_user_by_email_query import GetUserByEmailQuery, GetUserByEmailQueryResult

class GetUserByEmailMapper(
    QueryMapper[GetUserByEmailRequest, GetUserByEmailQuery],
    ResponseMapper[GetUserByEmailQueryResult, GetUserByEmailResponse]
):
    @classmethod
    def to_query(cls, request: GetUserByEmailRequest) -> GetUserByEmailQuery:
        return GetUserByEmailQuery(
            email=request.email
        )

    @classmethod
    def to_response(cls, result: GetUserByEmailQueryResult) -> GetUserByEmailResponse:
        if result.errors:
            return GetUserByEmailResponse(
                errors=result.errors
            )

        return GetUserByEmailResponse(
            user=GetUserByEmailResponse.User(
                id=result.user.id,
                email=result.user.email,
                user_type=UserConverter.user_type_to_string(result.user.user_type)
            )
        )
