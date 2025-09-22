from db.sql_statements import (
    select_app_user, 
    select_business_user_info, 
    select_beneficiary_user_info,
    select_business_name,
    select_beneficiary_name,
    select_business_email
)

from db.queries.app_user_query_response import AppUserQueryResponse
from db.queries.beneficiary_user_info_query_response import BeneficiaryUserInfoQueryResponse
from db.queries.beneficiary_name_query_response import BeneficiaryNameQueryResponse
from db.queries.business_user_info_query_response import BusinessUserInfoQueryResponse
from db.queries.business_name_query_response import BusinessNameQueryResponse

class QueryHandler():
    # db connection
    def __init__ (self, conn):
        self.conn = conn

    def query_app_user(self, app_user_id) -> AppUserQueryResponse:
        query = { 'app_user_id': app_user_id}
        with self.conn.cursor() as curs:
            curs.execute(select_app_user, query)
            if (curs.rowcount == 1):
                entry = curs.fetchone()
                return AppUserQueryResponse(
                    app_user_id=entry[0], 
                    user_type_code=entry[1]
                )
        return None
    
    def query_business_user_info(self, app_user_id) -> BusinessUserInfoQueryResponse:
        query = { 'app_user_id': app_user_id }
        with self.conn.cursor() as curs:
            curs.execute(select_business_user_info, query)
            if (curs.rowcount == 1):
                entry = curs.fetchone()
                return BusinessUserInfoQueryResponse(
                    app_user_id=entry[0],
                    business_id=entry[1],
                    business_name=entry[2]
                )
        return None

    def query_beneficiary_user_info(self, app_user_id) -> BeneficiaryUserInfoQueryResponse:
        query = { 'app_user_id': app_user_id }
        with self.conn.cursor() as curs:
            curs.execute(select_beneficiary_user_info, query)
            if (curs.rowcount == 1):
                entry = curs.fetchone()
                return BeneficiaryUserInfoQueryResponse(
                    app_user_id=entry[0],
                    beneficiary_user_id=entry[1],
                    beneficiary_id=entry[2],
                    beneficiary_name=entry[3]
                )
        return None
    
    def query_business_name(self, business_name) -> BusinessNameQueryResponse:
        query = { 'business_name': business_name }
        with self.conn.cursor() as curs:
            curs.execute(select_business_name, query)
            if curs.rowcount > 0:
                entry = curs.fetchone()
                return BusinessNameQueryResponse(business_id=entry[0], business_name=entry[1])
            
    def query_beneficiary_name(self, beneficiary_name) -> BeneficiaryNameQueryResponse:
        query = { 'beneficiary_name': beneficiary_name }
        with self.conn.cursor() as curs:
            curs.execute(select_beneficiary_name, query)
            if curs.rowcount > 0:
                entry = curs.fetchone()
                return BeneficiaryNameQueryResponse(beneficiary_id=entry[0], beneficiary_name=entry[1])
    
    def query_business_email_in_use(self, email) -> bool:
        query = { 'email': email }
        with self.conn.cursor() as curs:
            curs.execute(select_business_email, query)
            return curs.rowcount > 0