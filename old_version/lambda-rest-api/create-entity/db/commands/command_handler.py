from ..sql_statements import (
    insert_org_sql, 
    insert_cause_preference_sql, 
    insert_social_media_sql,
    insert_org_user_sql,
    insert_org_shop_sql
)
from psycopg2 import sql

class CommandHandler():
    # db connection
    def __init__ (self, conn):
        self.conn = conn
        
    def create_business(self, command_params: dict) -> str:
        with self.conn.cursor() as curs:
            sql_template = insert_org_sql['business']
            curs.execute(sql_template, command_params)
            if (curs.rowcount == 1):
                return curs.fetchone()[0]
            else:
                return None

    def create_beneficiary(self, command_params: dict) -> str:
        with self.conn.cursor() as curs:
            sql_template = insert_org_sql['beneficiary']
            curs.execute(sql_template, command_params)
            if (curs.rowcount == 1):
                return curs.fetchone()[0]
            else:
                return None

    def create_business_user(self, command_params: dict):
        with self.conn.cursor() as curs:
            sql_template = insert_org_user_sql['business']
            curs.execute(sql_template, command_params)
            return curs.rowcount > 0

    def create_beneficiary_user(self, command_params: dict):
        with self.conn.cursor() as curs:
            sql_template = insert_org_user_sql['beneficiary']
            curs.execute(sql_template, command_params)
            return curs.rowcount > 0

    def create_business_cause_code_preferences(self, command_params: dict):
        with self.conn.cursor() as curs:
            sql_template = insert_cause_preference_sql['business']
            updates = 0
            for param_entry in command_params:
                curs.execute(sql_template, param_entry)
                updates += curs.rowcount
            return updates

    def create_beneficiary_cause_code_preferences(self, command_params: dict):
        with self.conn.cursor() as curs:
            sql_template = insert_cause_preference_sql['beneficiary']
            updates = 0
            for param_entry in command_params:
                curs.execute(sql_template, param_entry)
                updates += curs.rowcount
            return updates

    def create_business_shop(self, command_params: dict):
        with self.conn.cursor() as curs:
            sql_template = insert_org_shop_sql['business']
            curs.execute(sql_template, command_params)
            return curs.rowcount > 0

    def create_beneficiary_shop(self, command_params: dict):
        with self.conn.cursor() as curs:
            sql_template = insert_org_shop_sql['beneficiary']
            curs.execute(sql_template, command_params)
            return curs.rowcount > 0
    
    def create_business_social_medias(self, command_params: dict):
        with self.conn.cursor() as curs:
            sql_template = insert_social_media_sql['business']
            updates = 0
            for param_entry in command_params:
                curs.execute(sql_template, param_entry)
                updates += curs.rowcount
            return updates

    def create_beneficiary_social_medias(self, command_params: dict):
        with self.conn.cursor() as curs:
            sql_template = insert_social_media_sql['business']
            updates = 0
            for param_entry in command_params:
                curs.execute(sql_template, param_entry)
                updates += curs.rowcount
            return updates