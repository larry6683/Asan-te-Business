from error.error_utils import ErrorUtils

from auth.auth_handler import AuthHandler
from auth.auth_mapper import AuthMapper

from database.models.business_user import BusinessUserPermissionRoleCode

from codegen.resource.create_resource_pb2 import CreateResourceRequest, CreateResourceResponse
from codegen.resource.create_resource_service_pb2_grpc import CreateResourceServiceServicer

from .create_resource_validation_handler import CreateResourceValidationHandler
from .create_resource_command_handler import CreateResourceCommandHandler
from .create_resource_mapper import CreateResourceMapper as Mapper

class CreateResourceService(CreateResourceServiceServicer):
    def __init__ (self):
        self.auth_handler = AuthHandler()
        self.validation_handler = CreateResourceValidationHandler()
        self.command_handler = CreateResourceCommandHandler()

    def CreateResource(self, request: CreateResourceRequest, context):
        try:
            auth_request = AuthMapper.to_auth_request(
                request.auth, 
                BusinessUserPermissionRoleCode.TEAM_MEMBER,
                self.CreateResource
            )
            if auth_errors := self.auth_handler.handle(auth_request):
                return CreateResourceResponse(errors=auth_errors)
            
            if errors := self.validation_handler.handle(request):
                return CreateResourceResponse(errors=errors)
            
            command = Mapper.to_command(request)

            result = self.command_handler.handle(command)

            return Mapper.to_response(result)
        
        except Exception as e:
            return CreateResourceResponse(errors=[ErrorUtils.create_operation_failed_error(self.CreateResource, e)])