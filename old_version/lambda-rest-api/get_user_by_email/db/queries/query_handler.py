from db.sql_statements import select_app_user
from db.queries.app_user_query_response import AppUserQueryResponse

class QueryHandler():
    def __init__(self, conn):
        self.conn = conn

    def query_app_user(self, email) -> AppUserQueryResponse:
        query = { 'email': email }
        with self.conn.cursor() as curs:
            curs.execute(select_app_user, query)
            if curs.rowcount == 1:
                entry = curs.fetchone()
                return AppUserQueryResponse(
                    app_user_id=entry[0], 
                    user_type_code=entry[1],
                    email=entry[2]
                )
        return None