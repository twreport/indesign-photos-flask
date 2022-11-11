from api.utils.database import db
from api.utils.database import ma

class ColorTag (db.Model):
    __tablename__ = 'color_tag'
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100))
    row_id = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, table_name, row_id, weight):
        self.table_name = table_name
        self.row_id = row_id
        self.weight = weight

    def __repr__(self):
        return '<Tag %d>' % self.id + '|' + 'table_name %s' % self.table_name

class ColorRoleSchema (ma.SQLAlchemySchema):
    class Meta:
        model = ColorTag
    id = ma.auto_field()
    table_name = ma.auto_field()
    row_id = ma.auto_field()
    weight = ma.auto_field()