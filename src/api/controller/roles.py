from api.utils.database import db
from api.model.roles import ColorRole
from api.model.roles import ColorRoleSchema

class Roles:
    def get_all_roles(self):
        fetched = ColorRole.query.all()
        roles_schema = ColorRoleSchema(many=True)
        roles = roles_schema.dump(fetched)
        return roles