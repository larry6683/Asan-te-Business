from api.handler.request_handler import RequestHandler
from error.error_utils import ErrorUtils

from codegen.error.account_error_pb2 import AccountError
from codegen.resource.create_resource_pb2 import CreateResourceRequest

class CreateResourceValidationHandler(
    RequestHandler[CreateResourceRequest, list[AccountError]],
):
    def __init__(self):
        pass

    def handle(self, request: CreateResourceRequest) -> list[AccountError]:
        errors = []

        if not request.resource.name:
            errors.append(ErrorUtils.create_required_parameter_error("resource.name"))
            
        if not request.resource.description:
            errors.append(ErrorUtils.create_required_parameter_error("resource.description"))
            
        if not request.resource.category:
            errors.append(ErrorUtils.create_required_parameter_error("resource.category"))
            
        return errors