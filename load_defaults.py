from sqlalchemy.orm import Session

import core.access
import core.crud
import core.database
import dropi.access
import watchy.access
import bike.access
from core.models import Group, Permission

default_groups = [
    Group(group_id=1, group_name="admin", group_description="administrators - all privileges"),
    Group(group_id=2, group_name="dev", group_description="developers - debug privileges"),
    Group(group_id=3, group_name="mod", group_description="moderators - management privileges"),
    Group(group_id=4, group_name="user", group_description="default group - basic privileges"),
]

core_permissions = [x.permission for x in core.access.permissions]
dropi_permissions = [x.permission for x in dropi.access.permissions]
watchy_permissions = [x.permission for x in watchy.access.permissions]
bike_permissions = [x.permission for x in bike.access.permissions]

default_permissions = [Permission(permission_id=1, app_name="*", permission_name="*")] + core_permissions + dropi_permissions + watchy_permissions + bike_permissions


def create_default_permissions():
    db: Session = next(core.database.get_db())
    for p in default_permissions:
        if isinstance(p, core.access.PermissionChecker):
            if p.permission:
                db.add(p.permission)
        elif isinstance(p, Permission):
            print(p)
            p_ex = core.crud.get_permission(db=db, permission_name=p.permission_name)
            print(p_ex)
            if p_ex:
                db.add(p)
    db.commit()


def create_default_groups():
    db: Session = next(core.database.get_db())
    for g in default_groups:
        db.add(g)
    db.commit()

