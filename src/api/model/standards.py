from api.utils.database import db
from api.utils.database import ma

class ColorStandard(db.Model):
    __tablename__ = 'color_standard'

    id = db.Column(db.Integer, primary_key=True)
    ncd_id = db.Column(db.Integer)
    ncd_name = db.Column(db.String(20))
    red = db.Column(db.Integer)
    green = db.Column(db.Integer)
    blue = db.Column(db.Integer)
    hue = db.Column(db.Float)
    saturation = db.Column(db.Float)
    value = db.Column(db.Float)
    adj_name = db.Column(db.String(20))
    tone_name = db.Column(db.String(20))
    tone_code = db.Column(db.String(20))
    color_name = db.Column(db.String(20))
    color_code = db.Column(db.String(20))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    z = db.Column(db.Integer)
    w16_id = db.Column(db.Integer)
    z40_id = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, ncd_id, ncd_name, red, green, blue, hue, saturation, value, adj_name,
                 tone_name, tone_code, color_name, color_code, x, y, z, w16_id, z40_id):
        self.ncd_id = ncd_id
        self.ncd_name = ncd_name
        self.red = red
        self.green = green
        self.blue = blue
        self.hue = hue
        self.saturation = saturation
        self.value = value
        self.adj_name = adj_name
        self.tone_name = tone_name
        self.tone_code = tone_code
        self.color_name = color_name
        self.color_code = color_code
        self.x = x
        self.y = y
        self.z = z
        self.w16_id = w16_id
        self.z40_id = z40_id

    def __repr__(self):
        return '<Standard Color %d>' % self.id + '|' + 'name %s' % self.ncd_name

class ColorStandardSchema (ma.SQLAlchemySchema):
    class Meta:
        model = ColorStandard
    id = ma.auto_field()
    ncd_id = ma.auto_field()
    ncd_name = ma.auto_field()
    red = ma.auto_field()
    green = ma.auto_field()
    blue = ma.auto_field()
    hue = ma.auto_field()
    saturation = ma.auto_field()
    value = ma.auto_field()
    adj_name = ma.auto_field()
    tone_name = ma.auto_field()
    tone_code = ma.auto_field()
    color_name = ma.auto_field()
    color_code = ma.auto_field()
    x = ma.auto_field()
    y = ma.auto_field()
    z = ma.auto_field()
    w16_id = ma.auto_field()
    z40_id = ma.auto_field()


