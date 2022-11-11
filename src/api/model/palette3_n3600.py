from api.utils.database import db
from api.utils.database import ma

class ColorPalette3N3600(db.Model):
    __tablename__ = 'color_palette3_n3600'

    id = db.Column(db.Integer, primary_key=True)
    c1 = db.Column(db.Integer)
    c2 = db.Column(db.Integer)
    c3 = db.Column(db.Integer)
    c1_red = db.Column(db.Integer)
    c1_green = db.Column(db.Integer)
    c1_blue = db.Column(db.Integer)
    c2_red = db.Column(db.Integer)
    c2_green = db.Column(db.Integer)
    c2_blue = db.Column(db.Integer)
    c3_red = db.Column(db.Integer)
    c3_green = db.Column(db.Integer)
    c3_blue = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    z = db.Column(db.Integer)
    word_n360_id = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, c1, c2, c3, c1_red, c1_green, c1_blue,
                 c2_red, c2_green, c2_blue, c3_red, c3_green, c3_blue,
                 x, y, z, word_n360_id):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c1_red = c1_red
        self.c1_green = c1_green
        self.c1_blue = c1_blue
        self.c2_red = c2_red
        self.c2_green = c2_green
        self.c2_blue = c2_blue
        self.c3_red = c3_red
        self.c3_green = c3_green
        self.c3_blue = c3_blue
        self.x = x
        self.y = y
        self.z = z
        self.word_n360_id = word_n360_id

    def __repr__(self):
        return '<Palette Color %d>' % self.id

class ColorPalette3N3600Schema (ma.SQLAlchemySchema):
    class Meta:
        model = ColorPalette3N3600
    id = ma.auto_field()
    c1 = ma.auto_field()
    c2 = ma.auto_field()
    c3 = ma.auto_field()
    c1_red = ma.auto_field()
    c1_green = ma.auto_field()
    c1_blue = ma.auto_field()
    c2_red = ma.auto_field()
    c2_green = ma.auto_field()
    c2_blue = ma.auto_field()
    c3_red = ma.auto_field()
    c3_green = ma.auto_field()
    c3_blue = ma.auto_field()
    x = ma.auto_field()
    y = ma.auto_field()
    z = ma.auto_field()
    word_n360_id = ma.auto_field()