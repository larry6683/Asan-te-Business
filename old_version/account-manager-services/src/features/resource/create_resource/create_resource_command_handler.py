from psycopg import Cursor
from config.config import Config
from database.db_utils import DBUtils

import json
import uuid

from api.handler.request_handler import RequestHandler
from domain.entity import EntityType
from error.error_utils import ErrorUtils

from database.models.resource import ResourceDbo
from database.db_data.resources import resources, query_resource_by_name

from .create_resource_command import CreateResourceCommand, CreateResourceCommandResult
from codegen.error.account_error_code_pb2 import AccountErrorCode

class CreateResourceCommandHandler(
    RequestHandler[CreateResourceCommand, CreateResourceCommandResult]
):
    def __init__(self):
        pass

    def handle(self, request: CreateResourceCommand) -> CreateResourceCommandResult:
        """
        if performing pre-flight check, this is where to do it.
        if multiple validations, collect errors and return at end.

        if there is domain validation, do it in the appropriate method.

        example:

        if not request.entity.entity_type == EntityType.BUSINESS:
            return CreateResourceCommandResult(
                errors=[
                    ErrorUtils.create_error(
                        AccountErrorCode.ERROR_INVALID_ENTITY_TYPE, 
                        "Only businesses can create resources"
                    )
                ]
            )
        """

        if not Config.use_db():
            return self.handle_mock(request)
        
        try:
            with DBUtils.get_connection() as conn:
                with conn.cursor() as cursor:
                    return self.handle_with_db(cursor, request)
        except Exception as e:
            # TODO: add specific database error handling
            raise e
        
        return CreateResourceCommandResult(
            resource_id=str(uuid.uuid4())
        )
    
    def handle_with_db(self, cursor: Cursor, request: CreateResourceCommand) -> CreateResourceCommandResult:
        """
        example of implementation:
        NOTE: I am asking you to use sql alchemy NOT raw sql queries!

        result = cursor.execute(insert_resource_sql, {
            "resource_id": request.entity.id,
            "resource_name": request.resource_name,
            "resource_category": request.resource_category,
        }).fetchone()

        if not result:
            raise Exception("Failed to insert resource into database")

        return CreateResourceCommandResult(
            resource_id=str(result[0])
        )
        """

        raise NotImplementedError("handle_with_db not implemented for CreateResourceCommandHandler")
        
    def handle_mock(self, request: CreateResourceCommand) -> CreateResourceCommandResult:
        if query_resource_by_name(request.name):
            return CreateResourceCommandResult(
                errors=[
                    ErrorUtils.create_enforce_parameter_uniqueness_error("resource.name", request.name)
                ]
            )

        resource = ResourceDbo(
            resource_id=str(uuid.uuid4()),
            name=request.name,
            description=request.description,
            category=request.category
        )
        
        resources.append(resource)

        self.print_json(resource)

        return CreateResourceCommandResult(
            resource_id=resource.resource_id
        )
    
    def print_json(self, request: ResourceDbo):
        print("Resource:")
        print(json.dumps({
            "resource_id": request.resource_id,
            "name": request.name,
            "description": request.description,
            "category": request.category
        }, indent=4, default=str))