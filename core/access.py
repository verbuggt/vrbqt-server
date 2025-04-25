from fastapi import Depends, HTTPException

import core.crud
import core.database
from core.auth import get_user_from_jwt
from core.models import User


class PermissionChecker:
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
        self.permission = core.crud.get_permission(db=next(core.database.get_db()), permission_name=required_permission)

    def __call__(self, user: User = Depends(get_user_from_jwt)):
        if self.required_permission not in user.permissions:
            raise HTTPException(status_code=403, detail="permission required")

    def __str__(self):
        print(self.required_permission)
        return self.required_permission


debug_access = PermissionChecker("core.debug")

user_create_access = PermissionChecker("core.user.create")
user_modify_access = PermissionChecker("core.user.modify")
user_delete_access = PermissionChecker("core.user.delete")

permissions = [
    debug_access,
    user_create_access,
    user_modify_access,
    user_delete_access,
]
