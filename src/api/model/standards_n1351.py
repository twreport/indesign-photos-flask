from api.utils.database import db
from api.utils.database import ma

class ColorStandardN1351(db.Model):
    __tablename__ = 'color_standard_n1351'

    id = db.Column(db.Integer, primary_key=True)
    red = db.Column(db.Integer)
    green = db.Column(db.Integer)
    blue = db.Column(db.Integer)
    hue = db.Column(db.Float)
    saturation = db.Column(db.Float)
    value = db.Column(db.Float)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    z = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, red, green, blue, hue, saturation, value, x, y, z):
        self.red = red
        self.green = green
        self.blue = blue
        self.hue = hue
        self.saturation = saturation
        self.value = value
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '<Standard Color %d>' % self.id

class ColorStandardN1351Schema (ma.SQLAlchemySchema):
    class Meta:
        model = ColorStandardN1351
    id = ma.auto_field()
    red = ma.auto_field()
    green = ma.auto_field()
    blue = ma.auto_field()
    hue = ma.auto_field()
    saturation = ma.auto_field()
    value = ma.auto_field()
    x = ma.auto_field()
    y = ma.auto_field()
    z = ma.auto_field()


