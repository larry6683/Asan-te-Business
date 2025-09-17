from database.models.business_user import BusinessUserDbo, BusinessUserPermissionRoleCode

# simulating query selection from database.
# In real implementation, this would be replaced with actual database queries.
def get_business_user(business_id, app_user_id) -> BusinessUserDbo:
    return next((
        business_user for business_user in business_users
        if (business_user.business_id == business_id
            and business_user.app_user_id == app_user_id
        )), 
        None
    )

def query_business_user_permission(business_id, app_user_id) -> BusinessUserPermissionRoleCode:
    business_user = get_business_user(business_id, app_user_id)
    if business_user:
        return business_user.business_user_permission_role
    return None

business_users: list[BusinessUserDbo] = [
    #
    # business_id: 04de82a4-b19c-45da-8251-7f6e6bc00503
    #
    BusinessUserDbo(
        business_user_id = "7736cc50-3c5b-40e7-b647-67da17b2d995",
        business_id = "04de82a4-b19c-45da-8251-7f6e6bc00503",
        app_user_id = "2e779286-c1a4-462d-9897-3ffedbe4261f",
        business_user_permission_role = BusinessUserPermissionRoleCode.ADMIN
    ),
    BusinessUserDbo(
        business_user_id = "7736cc50-3c5b-40e7-b647-67da17b2d995",
        business_id = "04de82a4-b19c-45da-8251-7f6e6bc00503",
        app_user_id = "f1a21dfc-5ea5-4e52-8f6f-2295dc5482fa",
        business_user_permission_role = BusinessUserPermissionRoleCode.ADMIN
    ),
    BusinessUserDbo(
        business_user_id = "e39086cf-2948-4fa8-958b-8f6998e6e09f",
        business_id = "04de82a4-b19c-45da-8251-7f6e6bc00503",
        app_user_id = "dbe288cb-a588-4014-8083-3da9d95125a8",
        business_user_permission_role = BusinessUserPermissionRoleCode.TEAM_MEMBER
    ),

    #
    # business_id: 204e76e7-7fb4-4b39-8379-1ba1ec9b7863
    #
    BusinessUserDbo(
        business_user_id = "7fcdff67-4286-4168-8d9b-882dba441543",
        business_id = "204e76e7-7fb4-4b39-8379-1ba1ec9b7863",
        app_user_id = "1d1575f0-9766-4eb3-a65b-9f99d2bd21c5",
        business_user_permission_role = BusinessUserPermissionRoleCode.ADMIN
    ),
    BusinessUserDbo(
        business_user_id = "fb5bcd7d-cae3-430e-aad6-676d195d5693",
        business_id = "204e76e7-7fb4-4b39-8379-1ba1ec9b7863",
        app_user_id = "4402fff3-d5a0-4f7a-a58e-f85be397f4a6",
        business_user_permission_role = BusinessUserPermissionRoleCode.ADMIN
    ),
    BusinessUserDbo(
        business_user_id = "e4468cc8-6418-463e-a1d6-6b9e770abf04",
        business_id = "204e76e7-7fb4-4b39-8379-1ba1ec9b7863",
        app_user_id = "25607395-1eca-41cf-ae80-561c58111bce",
        business_user_permission_role = BusinessUserPermissionRoleCode.TEAM_MEMBER
    ),

    #
    # business_id: 341b5a4a-e75e-41a0-94d8-d75c9839f30d
    #
    BusinessUserDbo(
        business_user_id = "ce10a967-21bf-4db9-88c2-44b359e16094",
        business_id = "341b5a4a-e75e-41a0-94d8-d75c9839f30d",
        app_user_id = "fd7815f5-be31-4dcc-bce1-b4942a142f11",
        business_user_permission_role = BusinessUserPermissionRoleCode.ADMIN
    ),
    BusinessUserDbo(
        business_user_id = "0157885f-f29a-4beb-803e-7e5f59395468",
        business_id = "341b5a4a-e75e-41a0-94d8-d75c9839f30d",
        app_user_id = "d7815f5-be31-4dcc-bce1-b4942a142f11",
        business_user_permission_role = BusinessUserPermissionRoleCode.ADMIN
    ),
    BusinessUserDbo(
        business_user_id = "f473af94-b887-40a8-acb3-a85f7cbde09e",
        business_id = "341b5a4a-e75e-41a0-94d8-d75c9839f30d",
        app_user_id = "25b6ffe3-7c69-49b2-a870-7b48116be3d2",
        business_user_permission_role = BusinessUserPermissionRoleCode.TEAM_MEMBER
    )
]