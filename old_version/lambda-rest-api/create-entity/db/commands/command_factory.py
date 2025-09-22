from db.codes.social_media_type_code import SocialMediaTypeCode
from db.codes.cause_preference_rank_code import CausePreferenceRankCode
from db.codes.cause_code import CauseCode

class CommandFactory:
    @staticmethod
    def create_insert_business_command_params(params):
        return {
            'business_name': params['name'],
            'email': params['email'],
            'phone_number': params['phone_number'],
            'location_city': params['location_city'],
            'location_state': params['location_state'],
            'website_url': params['website_url'],
            'business_size_code': params['size']
        }
        
    @staticmethod
    def create_insert_beneficiary_command_params(params):
        return {
            'beneficiary_name': params['name'],
            'email': params['email'],
            'phone_number': params['phone_number'],
            'location_city': params['location_city'],
            'location_state': params['location_state'],
            'website_url': params['website_url'],
            'beneficiary_size_code': params['size']
        }
    
    @staticmethod
    def create_insert_entity_user_command_params(entity_id: str, user_id: str, entity_permission_role_code_value: int):
        return {
            'entity_id': entity_id,
            'app_user_id': user_id,
            'user_permission_role_code': entity_permission_role_code_value
        }

    @staticmethod
    def create_insert_entity_shop_command_params(entity_id, shop_type_code_value, shop_url):
        return {
            'entity_id': entity_id,
            'shop_type_code': shop_type_code_value,
            'shop_url': shop_url
        }
    
    @staticmethod
    def create_insert_cause_preference_command_params(entity_id, causes):
        # this is ok because lists have a max size of 20 something
        return [
            { 
                'entity_id': entity_id, 
                'cause_code': CauseCode.from_str(cause["name"]).value,
                'cause_preference_rank_code': CausePreferenceRankCode.from_str(cause["rank"]).value
            } for cause in causes
        ]
        
    @staticmethod
    def create_insert_social_media_command_params(entity_id, urls):
        return [
            { 
                'entity_id': entity_id, 
                'social_media_url': url.strip(), 
                'social_media_type_code': CommandFactory.get_social_network_type_code(url.strip()).value 
            } for url in urls if url
        ]

    @staticmethod
    def get_social_network_type_code(url: str):
        if 'instagram.com' in url.lower():
            return SocialMediaTypeCode.INSTAGRAM
        elif 'facebook.com' in url.lower():
            return SocialMediaTypeCode.FACEBOOK
        elif 'linkdin' in url.lower():
            return SocialMediaTypeCode.LINKDIN
        else:
            return SocialMediaTypeCode.UNSPECIFIED