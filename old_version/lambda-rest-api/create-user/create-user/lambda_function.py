import json
import os
import psycopg2
import boto3
from enum import Enum

from log_utils import LogUtils, logger
from errors.error import Error, ErrorCode
from api_request import ApiRequest
from api_response import ApiResponse
from db.sql_statements import insert_user_sql, select_existing_user_sql
from db.codes.user_type_code import UserTypeCode

client = boto3.client('cognito-idp')

# NB: Environment variables need to be declared in template.yaml to be visible
# DB Variables
conn_params = {
    'user': os.environ.get("DB_USER", ''),
    'password': os.environ.get("DB_PASSWORD", '') ,
    'host': os.environ.get("DB_HOST", ''),
    'dbname': os.environ.get("DB_NAME", ''),
}

cogntio_params = {
    'user_pool_id': os.environ.get('user_pool_id', '')
}

def lambda_handler(event, context):
    logger.info("Incoming event: %s", json.dumps(event))
    try:
        logger.info("get body information")
        request_data = ApiRequest.extract_body(event)
        if request_data is None:
            logger.error('unable to extract request body')
            return ApiResponse.create_internal_error_response()
        logger.info('request body', request_data)
    except Exception as e:
        LogUtils.log_exception("reading body", e)
        return ApiResponse.create_internal_error_response()
    
    params = {
        'email': request_data.get('email', '')
    }
    
    try:
        LogUtils.log_object('validating params', params)
        validation_errors = []
        email = params['email']
        if not email:
            validation_errors.append(
                Error.create_invalid_parameter_error("user.email", 'email field required')
            )
        if len(validation_errors) > 0:
            logger.info(f'invalid parameters: {validation_errors}')
            return ApiResponse.create_error_list_response(400, validation_errors)
    except Exception as e:
        LogUtils.log_exception('validating params', e)

    try:
        
        logger.info('getting user from cognito')
        user = client.admin_get_user(
            UserPoolId=cogntio_params['user_pool_id'],
            Username=email
        )
    except client.exceptions.UserNotFoundException as e:
        logger.info('cognito user not found')
        return ApiResponse.create_error_response(
            404, 
            Error.create_error(
                ErrorCode.USER_EMAIL_NOT_FOUND, 
                "user.email",
                ErrorCode.USER_EMAIL_NOT_FOUND.to_message(value=email)
            )
        )
    except Exception as e:
        LogUtils.log_exception('getting user from cognito', e)
        return ApiResponse.create_internal_error_response()

    try:
        logger.info('validating user')
        user_attributes = user.get("UserAttributes", {})
        logger.info('user attributes %s: %s', email, user_attributes)
        user_errors = []
        (
            email_verified,
            mailing_list_signup,
            user_type,
        ) = (None, None, None)
        
        for attribute in user_attributes:
            (name, value) = (attribute.get("Name", ""), attribute.get("Value"))
            match(name):
                case 'email_verified':
                    email_verified = bool(value)
                case 'custom:user_type':
                    user_type = value
                case 'custom:mailing_list_signup':
                    mailing_list_signup = bool(value)
                case _:
                    pass
                
        logger.info('validating attribute existance')
        if (email_verified is None):
            logger.error('invalid value in user attributes! key: %s, value:', 'email_verified', email_verified)
            user_errors.append(
                    Error.create_error(
                        error_code,
                        None,
                        error_code.to_message(key='email_verified', value=email_verified)
                    )
                )
        if (mailing_list_signup is None):
            logger.error('invalid value in user attributes! key: %s, value:', 'mailing_list_signup', str(mailing_list_signup))
            user_errors.append(
                    Error.create_error(
                        error_code,
                        None,
                        error_code.to_message(key='mailing_list_signup', value=mailing_list_signup)
                    )
                )
        logger.info('user_type %s', user_type)
        if (user_type is None):
            logger.error('invalid value in user attributes! key: %s, value:', 'user_type', user_type)
            user_errors.append(
                    Error.create_error(
                        error_code,
                        None,
                        error_code.to_message(key='user_type', value=user_type)
                    )
                )
                
        logger.info('validating user attribute values')
        if not email_verified:
            error_code = ErrorCode.USER_EMAIL_NOT_VERIFIED
            user_errors.append(
                Error.create_error(
                    error_code,
                    None,
                    error_code.to_message(email)
                )
            )
        user_type = UserTypeCode.from_str(user_type.split(' ')[0])
        if user_type is None:
            error_code = ErrorCode.INVALID_USER_TYPE
            user_errors.append(
                Error.create_error(
                    error_code,
                    None,
                    error_code.to_message(value=user_type)
                )
            )
        if len(user_errors) > 0:
            return ApiResponse.create_error_list_response(400, user_errors)
    except Exception as e:
        LogUtils.log_exception('validating user', e)
        return ApiResponse.create_internal_error_response()
        
    try:
        logger.info("signing up user with email")
        params['mailing_list_signup'] = mailing_list_signup
        params['user_type_code'] = user_type
        result = process_user_signup(params)
        if result == ErrorCode.INTERNAL_ERROR:
            logger.error('unable to create app user - internal error. email: %s', email)
            return ApiResponse.create_internal_error_response()
        elif result == ErrorCode.USER_EMAIL_NOT_UNIQUE:
            logger.info('user cannot be created - email is not unique')
            return ApiResponse.create_error_response(
                400,
                Error.create_error(
                    result,
                    None,
                    result.to_message(params['email'])
                )
            )
        elif not isinstance(result, dict):
            # unexpected but...
            logger.error('unable to create user due to unexpected result. email: %s', email)
            return ApiResponse.create_internal_error_response()
        # successfully created user
        logger.info('successfully created user. email: %s, id: %s', email, result)
        return ApiResponse.create_response(
            201,
            {
                'data': {
                    'type': 'user',
                    'id': result['user_id'],
                    'attributes': {
                        'email': result['email'],
                        'userType': result['user_type'].name
                    }
                }
            }
        )
    except Exception as e:
        LogUtils.log_exception("signing up user with email", e)
        return ApiResponse.create_internal_error_response()

def process_user_signup(params):
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = False
        logger.info("successfully connected to database")
    except Exception as e:
        LogUtils.log_exception(f"Error connecting to the database - psycopg2.connect", e)
        return ErrorCode.INTERNAL_ERROR
    
    try:
        email_exists = check_user_email_unique(conn, params['email'])
        if (email_exists == ErrorCode.INTERNAL_ERROR):
            return ErrorCode.INTERNAL_ERROR
        elif (email_exists):
            return ErrorCode.USER_EMAIL_NOT_UNIQUE

        result = insert_user_into_db(conn, params)
        if result == ErrorCode.INTERNAL_ERROR:
            conn.rollback()
        
        conn.commit()
        return result
    except Exception as e:
        LogUtils.log_exception("process_user_signup", e)
    finally:
        conn.close()

def check_user_email_unique(conn, email) -> bool:
    try:
        logger.info('checking for email uniqueness')
        command = { 'email': email }
        with conn.cursor() as curs:
            curs.execute(select_existing_user_sql, command)
            return curs.rowcount > 0
        return False
    except Exception as e:
        LogUtils.log_exception('check for email uniqueness', e)
        return ErrorCode.INTERNAL_ERROR

def insert_user_into_db(conn, params):
    try:
        command = {
            'email': params['email'],
            'mailing_list_signup': str(params['mailing_list_signup']),
            'user_type_code': params['user_type_code'].value
        }
        with conn.cursor() as curs:
            # all of this may be better sever by a procedure or function, but this is fine for now.
            # select_registration_type_sql = "select registration_type_id from registration_type where registration_type_name = %s"
            curs.execute(insert_user_sql, command)
            if (curs.rowcount > 0):
                entry = curs.fetchone()
                return {
                    'user_id': entry[0],
                    'email': entry[1],
                    'user_type': UserTypeCode.from_int(entry[2])
                }
            logger.error('app user not created!')
            return ErrorCode.INTERNAL_ERROR
    except Exception as e:
        LogUtils.log_exception('inserting app user into db', e)
        return ErrorCode.INTERNAL_ERROR