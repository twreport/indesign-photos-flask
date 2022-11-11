from api.utils.database import db
from api.utils.database import ma
from api.model.roles import ColorRole

user_role = db.Table('color_user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('color_user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('color_role.id'), primary_key=True)
                     )

class ColorUser (db.Model):
    __tablename__ = 'color_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    openid = db.Column(db.String(100))
    status = db.Column(db.Integer)

    roles = db.relationship('ColorRole', secondary=user_role)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, email, password, openid, status):
        self.name = name
        self.email = email
        self.password = password
        self.openid = openid
        self.status = status

    def __repr__(self):
        return '<User %d>' % self.id + '|' + 'name %s' % self.name

class ColorUserSchema (ma.SQLAlchemySchema):
    class Meta:
        model = ColorUser
    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    openid = ma.auto_field()
    status = ma.auto_field()
    roles = ma.auto_field()

