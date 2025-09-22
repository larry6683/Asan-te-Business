from dataclasses import dataclass
from enum import Enum

class BusinessUserPermissionRoleCode(Enum):
    ADMIN = 1
    TEAM_MEMBER = 2
    
@dataclass(slots=True)
class BusinessUserDbo:
    business_user_id: str
    business_id: str
    app_user_id: str
    business_user_permission_role: BusinessUserPermissionRoleCode