import json
import os
import psycopg2
import logging
import enum

from log_utils import logger, LogUtils
from api_response import ApiResponse
from api_request import ApiRequest

from db.queries.query_handler import QueryHandler
from db.queries.app_user_query_response import AppUserQueryResponse

from db.commands.command_handler import CommandHandler
from db.commands.command_factory import CommandFactory

from validation.request_validation_handler import RequestValidationHandler
# from validation.auth_validation_handler import AuthValidationHandler

from errors.error_code import ErrorCode
from errors.error import Error
from db.codes.user_type_code import UserTypeCode
from db.codes.business_size_code import BusinessSizeCode
from db.codes.beneficiary_size_code import BeneficiarySizeCode
from db.codes.cause_code import CauseCode
from db.codes.business_user_permission_role_code import BusinessUserPermissionRoleCode
from db.codes.beneficiary_user_permission_role_code import BeneficiaryUserPermissionRoleCode
from db.codes.shop_type_code import ShopTypeCode

conn_params = {
    'user': os.environ.get("DB_USER", ''),
    'password': os.environ.get("DB_PASSWORD", '') ,
    'host': os.environ.get("DB_HOST", ''),
    'dbname': os.environ.get("DB_NAME", ''),
}
cogntio_params = {
    'user_pool_id': os.environ.get('user_pool_id', ''),
    'region': os.environ.get('user_pool_region', ''),
    'client_id': os.environ.get('client_id', '')
}

def lambda_handler(event, context):
    logger.info("Incoming event: %s", json.dumps(event))
    try:
        # extract body, handling str vs dict errors
        request_data = ApiRequest.extract_body(event)
        if request_data is None:
            logger.error('unable to extract request body')
            return ApiResponse.create_internal_error_response()
        logger.info('request body', request_data)
        request_headers = ApiRequest.extract_headers(event)
    except json.JSONDecodeError as e:
        LogUtils.log_exception(f"Failed to parse request body", e)
        return ApiResponse.create_error_response(400, Error.create_error(400, None, "Invalid JSON format"))
    except Exception as e:
        LogUtils.log_exception("reading event", e)
        return ApiResponse.create_internal_error_response()

    # Parse the incoming request data
    try:
        # collect parameters
        registration = request_data.get("registration", {})
        profile = registration.get("profile", {})
        location = profile.get("location", {})
        params = {
            'user_id': request_data.get("user", {}).get("id", "").strip(),
            'entity_type': registration.get("entityType", "").strip(),
            'name': profile.get('name', '').strip(),
            'email': profile.get('email', '').strip(),
            'phone_number': profile.get('phone', '').strip(),
            'location_city': location.get('city', '').strip(),
            'location_state': location.get('state', '').strip(),
            'website_url': profile.get('website', '').strip(),
            'size': profile.get('size', '').strip(),
            'causes': registration.get('causes', []),
            'social_media_urls': [url.strip() for url in profile.get('socialMediaUrls', [])],
            'shop_url': profile.get('shopUrl', '').strip(),
            'team_member_emails': [email.strip() for email in profile.get('teamMemberEmails', [])]
        }
        LogUtils.log_object('params', params)
    except Exception as e:
        LogUtils.log_exception("extracting parameters from body", e)
        return ApiResponse.create_internal_error_response()
    
    try:
        # validate parameters
        validation_handler: RequestValidationHandler = RequestValidationHandler()
        validation_errors = validation_handler.validate_params(params)
        if len(validation_errors) > 0:
            return ApiResponse.create_error_list_response(400, validation_errors)
    except Exception as e:
        LogUtils.log_exception("validating parameters", e)
        return ApiResponse.create_internal_error_response()

    try:
        user_id = params['user_id']
        entity_type = params['entity_type']
        create_entity_response = process_create_entity(user_id, entity_type, params)
        if isinstance(create_entity_response, str):
            logger.info('returning ssuccessful response')
            response = ApiResponse.create_response(201, {
                f"{entity_type}": {
                    "id": create_entity_response
                }
            })
            logger.info('successful response', response)
            return response
        elif (create_entity_response in [None, ErrorCode.INTERNAL_ERROR]):
            logger.info('returning internal error response')
            return ApiResponse.create_internal_error_response()
        elif isinstance(create_entity_response, dict):
            # must be dict with error info!
            logger.info('returning error response')
            error_code: ErrorCode = create_entity_response.get('error', ErrorCode.INTERNAL_ERROR)
            # oops?
            if (error_code == ErrorCode.INTERNAL_ERROR): 
                return ApiResponse.create_internal_error_response()
            error_id = create_entity_response.get('id', '')
            error_name = create_entity_response.get('name', '')
            error_message = None
            match(error_code):
                case ErrorCode.USER_NOT_FOUND:
                    error_message = error_code.to_message(error_id)
                case ErrorCode.INVALID_USER_TYPE:
                    error_message = error_code.to_message(error_name)
                case ErrorCode.ALREADY_REGISTERED_TO_BUSINESS | ErrorCode.ALREADY_REGISTERED_TO_BENEFICIARY:
                    error_message = error_code.to_message(key=error_id, value=error_name)
                case ErrorCode.NAME_TAKEN:
                    error_message = error_code.to_message(value=error_name, entity_type=entity_type)
                case ErrorCode.EMAIL_IN_USE:
                    error_message = error_code.to_message(value=error_name)
                case ErrorCode.UNSUPPORTED_ENTITY_TYPE:
                    error_message = error_code.to_message(entity_type=entity_type)
                case _:
                    error_message = error_code.to_message()
                    
            return ApiResponse.create_error_response(400, Error.create_error(error_code, None, error_message))
        else:
            logger.error("unexpected format for entityId")
            return ApiResponse.create_internal_error_response()
    except Exception as e:
        LogUtils.log_exception("process_create_entity", e)
        return ApiResponse.create_internal_error_response()

def process_create_entity(user_id, entity_type, params):
    try:
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = False
        logger.info("successfully connected to database")
    except Exception as e:
        LogUtils.log_exception(f"Error connecting to the database - psycopg2.connect", e)
        return ErrorCode.INTERNAL_ERROR

    try:
        logger.info("validating database")
        validation_response = validate_registration_with_conn(conn, user_id, entity_type, params)
        if validation_response:
            logger.info("Invalid registration")
            return validation_response
        
        create_entity_result = create_entity_with_conn(conn, user_id, entity_type, params)
        if create_entity_result == ErrorCode.INTERNAL_ERROR:
            conn.rollback()
            logger.error(f'Error creating {entity_type}. Error: {create_entity_result.name} - rolling back changes')
            
        conn.commit()
        return create_entity_result
    except psycopg2.DatabaseError as e:
        LogUtils.log_exception("database error", e)
        logger.error('database error - rolling back changes')
        conn.rollback()
        return ErrorCode.INTERNAL_ERROR
    except Exception as e:
        LogUtils.log_exception("process_create_entity", e)
        logger.error('exception - rolling back changes')
        conn.rollback()
        return ErrorCode.INTERNAL_ERROR
    finally:
        conn.close()

def validate_registration_with_conn(conn, user_id, entity_type, params) -> dict:
    query_handler = QueryHandler(conn)
    
    if entity_type not in ['business', 'beneficiary']:
        LogUtils.log_unsupported_operation(f'create {entity_type}')
        return {
            'error': ErrorCode.UNSUPPORTED_ENTITY_TYPE,
            'name': entity_type
        }

    try:
        logger.info('querying app user')
        app_user: AppUserQueryResponse = query_handler.query_app_user(user_id)
        if app_user is None:
            logger.error(f"Error querying app user - app_user not found. app_user_id: {user_id}")
            return {
                'error': ErrorCode.USER_NOT_FOUND,
                'id': user_id,
                'name': None
            }
        elif ((app_user.user_type_code == UserTypeCode.BUSINESS and entity_type == 'beneficiary')
            or (app_user.user_type_code == UserTypeCode.BENEFICIARY and entity_type == 'business')):
            logger.info(f'unable to register a {entity_type}, incoming user belongs to a {app_user.user_type_code}')
            return {
                'error': ErrorCode.INVALID_USER_TYPE,
                'id': None,
                'name': 'business' if entity_type == 'beneficiary' else 'beneficiary'
            }
    except Exception as e:
        LogUtils.log_exception("query_app_user", e)
        return ErrorCode.INTERNAL_ERROR

    try:
        logger.info(f'querying {entity_type} user')
        if entity_type == 'business':
            business_user_info = query_handler.query_business_user_info(user_id)
            if (business_user_info is not None):
                return {
                    'error': ErrorCode.ALREADY_REGISTERED_TO_BUSINESS,
                    'id': business_user_info.business_id,
                    'name': business_user_info.business_name
                }
        elif entity_type == 'beneficiary':
            beneficiary_user_info = query_handler.query_beneficiary_user_info(user_id)
            if (beneficiary_user_info is not None):
                return {
                    'error': ErrorCode.ALREADY_REGISTERED_TO_BENEFICIARY,
                    'id': beneficiary_user_info.beneficiary_id,
                    'name': beneficiary_user_info.beneficiary_name
                }
    except Exception as e:
        LogUtils.log_exception(f'query {entity_type} user info', e)
        return ErrorCode.INTERNAL_ERROR

    try:
        name = params['name']
        entity_id = None
        entity_name = None
        logger.info(f"Check if a {entity_type} with name {name} already exists")
        if entity_type == 'business':
            query_name_response = query_handler.query_business_name(name)
            if (query_name_response is not None):
                entity_id = query_name_response.business_id
                entity_name = query_name_response.business_name
        elif entity_type == 'beneficiary':
            query_name_response = query_handler.query_beneficiary_name(name)
            if (query_name_response is not None):
                entity_id = query_name_response.business_id
                entity_name = query_name_response.business_name
        if entity_id is not None and entity_name is not None:
            logger.info(f"a {entity_type} already exists with the name {name}")
            return {
                'error': ErrorCode.NAME_TAKEN,
                'id': entity_id,
                'name': entity_name
            }
    except Exception as e:
        LogUtils.log_exception(f'query {entity_type} name', e)
        return ErrorCode.INTERNAL_ERROR
        
    try:
        email = params['email']
        logger.info(f'query for used email: {email}')
        query_email_in_use_response = query_handler.query_business_email_in_use(email)
        if (query_email_in_use_response):
            logger.info('email is use!')
            return {
            'error': ErrorCode.EMAIL_IN_USE,
            'id': None,
            'name': email
        }
    except Exception as e:
        LogUtils.log_exception(f'query {entity_type} email', e)
        return ErrorCode.INTERNAL_ERROR
    
    return None
        
def create_entity_with_conn(conn, app_user_id, entity_type, params):
    command_handler = CommandHandler(conn)
    entity_id = None
    try:
        if (entity_type == 'business'):
            params['size'] = BusinessSizeCode.from_str(params['size']).value
            insert_business_params = CommandFactory.create_insert_business_command_params(params)
            entity_id = command_handler.create_business(insert_business_params)
        elif (entity_type == 'beneficiary'):
            params['size'] = BeneficiarySizeCode.from_str(params['size']).value
            insert_beneficiary_params = CommandFactory.create_insert_business_command_params(params)
            entity_id = command_handler.create_beneficiary(insert_beneficiary_params)
        if (entity_id is None or len(entity_id) == 0):
            logger.error(f'error creating {entity_type}')
            return ErrorCode.INTERNAL_ERROR
    except Exception as e:
        LogUtils.log_exception(f'create {entity_type}', e)
        return ErrorCode.INTERNAL_ERROR
        
    logger.info(f'successfully created {entity_type}. id: {entity_id}')
    
    try:
        logger.info(f'creating {entity_type} user')
        entity_user_created = False
        user_permission_role_code = BusinessUserPermissionRoleCode.ADMIN if entity_type == 'business' else BeneficiaryUserPermissionRoleCode.ADMIN
        create_entity_user_command = CommandFactory.create_insert_entity_user_command_params(
            entity_id, app_user_id, user_permission_role_code.value
        )
        if (entity_type == 'business'):
            entity_user_created = command_handler.create_business_user(create_entity_user_command)
        else:
            entity_user_created = command_handler.create_beneficiary_user(create_entity_user_command)
        if not entity_user_created:
            logger.error(f'unable to create {entity_type} user')
            return ErrorCode.INTERNAL_ERROR
    except Exception as e:
        LogUtils.log_exception(f'create {entity_type}', e)
        return ErrorCode.INTERNAL_ERROR

    logger.info(f'successfully created {entity_type} user')

    try:
        causes = params['causes']
        logger.info(f'creating {entity_type} cause preferences')
        logger.info(f'number of cause codes to insert: {len(causes)}')
        cause_insert_length = 0

        insert_cause_preferences_command_params = CommandFactory.create_insert_cause_preference_command_params(entity_id, causes)
        logger.info(f'cause_preference params: insert_cause_preferences_command_params')
        if (entity_type == 'business'):
            cause_insert_length = command_handler.create_business_cause_code_preferences(insert_cause_preferences_command_params)
        elif (entity_type == 'beneficiary'):
            cause_insert_length = command_handler.create_beneficiary_cause_code_preferences(insert_cause_preferences_command_params)

        logger.info(f'causes inserted: {cause_insert_length}')
        if (len(causes) != cause_insert_length):
            logger.error(f'error inserting cause preferences for {entity_type}_id: {entity_id}. expected length: {len(causes)}. inserted length: {cause_insert_length}')
            return ErrorCode.INTERNAL_ERROR
        else:
            logger.info(f'inserted cause preference entries for {entity_type}_id: {entity_id}. causes inserted: {cause_insert_length}')
    except Exception as e:
        LogUtils.log_exception(f'create {entity_type} cause preferences', e)
        return ErrorCode.INTERNAL_ERROR
    
    try:
        shop_url = params['shop_url']
        if (shop_url):
            logger.info(f'creating {entity_type} shop')
            shop_type_code = ShopTypeCode.SHOPIFY
            entity_shop_created = False
            insert_shop_command = CommandFactory.create_insert_entity_shop_command_params(entity_id, shop_type_code.value, shop_url)
            if entity_type == 'business':
                entity_shop_created = command_handler.create_business_shop(insert_shop_command)
            else:
                entity_shop_created = command_handler.create_beneficiary_shop(insert_shop_command)
            if not entity_shop_created:
                logger.error(f'unable to create {entity_type} shop')
                return ErrorCode.INTERNAL_ERROR
    except Exception as e:
        LogUtils.log_exception(f'create {entity_type} shop', e)
        return ErrorCode.INTERNAL_ERROR

    try:
        social_media_command_params = CommandFactory.create_insert_social_media_command_params(entity_id, params['social_media_urls'])
        if (len(social_media_command_params) > 0):
            social_media_insert_length: int = 0
            LogUtils.log_object('social_media_command_params', social_media_command_params)
            if (entity_type == 'business'):
                social_media_insert_length = command_handler.create_business_social_medias(social_media_command_params)
            elif (entity_type == 'beneficiary'):
                social_media_insert_length = command_handler.create_beneficiary_social_medias(social_media_command_params)
            if len(social_media_command_params) != social_media_insert_length:
                logger.error(f'error inserting social media links for {entity_type}_id: {entity_id}. expected length:{len(social_media_command_params)}. insert length: {social_media_insert_length}')
                return ErrorCode.INTERNAL_ERROR
            else:
                logger.info(f'inserted social media link entries for {entity_type}_id: {entity_id}. links inserted: {social_media_insert_length}')
    except Exception as e:
        LogUtils.log_exception(f'create_{entity_type}_social_media_urls', e)
        return ErrorCode.INTERNAL_ERROR

    logger.info(f'{entity_type} with id: {entity_id} and applicable information successfully created')
    return entity_id