import json
import os
import psycopg2

from enum import Enum
from errors.error import Error, ErrorCode
from log_utils import LogUtils, logger
from api_request import ApiRequest
from api_response import ApiResponse
from db.queries.app_user_query_response import AppUserQueryResponse
from db.queries.query_handler import QueryHandler
# NB: Environment variables need to be declared in template.yaml to be visible
# DB Variables
conn_params = {
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD") ,
    'host': os.environ.get("DB_HOST"),
    'dbname': os.environ.get("DB_NAME"),
}

def lambda_handler(event, context):
    logger.info("Incoming event: %s", json.dumps(event))
    try:
        logger.info("Get Query Params")
        query_params = ApiRequest.extract_query_parameters(event)
        email = query_params.get("email", "")
        if not email:
            return ApiResponse.create_error_response(
                400, 
                Error(
                    ErrorCode.MISSING_QUERY_PARAMETER, 
                    None, 
                    "Missing 'email' Query Parameter"
                )
            )
    except Exception as e:
        LogUtils.log_exception("Get email Query Param", e)
        return ApiResponse.create_internal_error_response()
    
    logger.info("incoming email query param: %s", email)
    logger.info('calling get_app_user')

    result = process_get_app_user(email)
    if result == ErrorCode.INTERNAL_ERROR:
        return ApiResponse.create_internal_error_response()
    elif result == ErrorCode.USER_EMAIL_NOT_FOUND:
        return ApiResponse.create_error_response(
            404,
            Error.create_error(
                result,
                None,
                result.to_message(email)
            )
        )
    # only possible results are:
    # INTERNAL_ERROR, USER_NOT_FOUND, AppUserQueryResponse
    result: AppUserQueryResponse
    return ApiResponse.create_response(
            200,
            {
                'data': {
                    'type': 'user',
                    'id': result.app_user_id,
                    'attributes': {
                        'email': result.email,
                        'userType': result.user_type_code.name
                    }
                }
            }
        )
    
def process_get_app_user(email):
    try:
        logger.info('connecting to database')
        conn = psycopg2.connect(**conn_params)
        logger.info("successfully connected to database")
    except Exception as e:
        LogUtils.log_exception(f"Error connecting to the database - psycopg2.connect", e)
        return ErrorCode.INTERNAL_ERROR
    
    try:
        return get_user_id_from_db(conn, email) 
    except psycopg2.DatabaseError as e:
        LogUtils.log_exception("process_get_user_id", e)
        logger.error('database error in process_get_user_id')
        return ErrorCode.INTERNAL_ERROR
    except Exception as e:
        LogUtils.log_exception("exception in process_get_user_id", e)
        return ErrorCode.INTERNAL_ERROR
    finally:
        conn.close()

def get_user_id_from_db(conn, email):
    query_handler: QueryHandler = QueryHandler(conn)
    try:
        logger.info(f'querying for app_user with email: {email}')
        app_user = query_handler.query_app_user(email)
        if app_user is None:
            return ErrorCode.USER_EMAIL_NOT_FOUND
        return app_user
    except Exception as e:
        LogUtils.log_exception("query app user by email", e)
        return ErrorCode.INTERNAL_ERROR
