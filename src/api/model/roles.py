from api.utils.database import db
from api.utils.database import ma
from api.model.privilege import ColorPrivilege

role_privilege = db.Table('color_role_privilege',
                          db.Column('role_id', db.Integer, db.ForeignKey('color_role.id'), primary_key=True),
                          db.Column('privilege_id', db.Integer, db.ForeignKey('color_privilege.id'), primary_key=True)
                          )

class ColorRole (db.Model):
    __tablename__ = 'color_role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20))

    privileges = db.relationship("ColorPrivilege", lazy='dynamic', secondary=role_privilege)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return '<Role %d>' % self.id + '|' + 'role_name %s' % self.role_name

class ColorRoleSchema (ma.SQLAlchemySchema):
    class Meta:
        model = ColorRole
    id = ma.auto_field()
    role_name = ma.auto_field()
    privileges = ma.auto_field()

