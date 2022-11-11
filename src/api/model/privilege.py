from api.utils.database import db
from api.utils.database import ma

class ColorPrivilege(db.Model):
    __tablename__ = 'color_privilege'

    id = db.Column(db.Integer, primary_key=True)
    privilege_name = db.Column(db.String(30))
    controller_name = db.Column(db.String(20))
    module_name = db.Column(db.String(20))
    action_name = db.Column(db.String(50))
    parent_id = db.Column(db.Integer)
    is_menu = db.Column(db.Integer)
    nav = db.Column(db.String(30))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, privilege_name, controller_name, module_name, action_name, parent_id, is_menu, nav):
        self.privilege_name = privilege_name
        self.controller_name = controller_name
        self.module_name = module_name
        self.action_name = action_name
        self.parent_id = parent_id
        self.is_menu = is_menu
        self.nav = nav

    def __repr__(self):
        return '<Privilege %d>' % self.id + '|' + 'privilege_name %s' % self.privilege_name

class ColorPrivilegeSchema (ma.SQLAlchemySchema):
    class Meta:
        model = ColorPrivilege
    id = ma.auto_field()
    privilege_name = ma.auto_field()
    controller_name = ma.auto_field()
    module_name = ma.auto_field()
    action_name = ma.auto_field()
    parent_id = ma.auto_field()
    is_menu = ma.auto_field()
    nav = ma.auto_field()

