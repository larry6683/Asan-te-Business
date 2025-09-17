from db.codes.user_type_code import UserTypeCode

class AppUserQueryResponse():
    def __init__(self, app_user_id: str, user_type_code: int):
        self.app_user_id = app_user_id
        self.user_type_code = UserTypeCode.from_int(user_type_code)