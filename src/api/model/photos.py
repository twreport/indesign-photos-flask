from api.utils.database import db
from api.utils.database import ma
from api.model.tag import ColorTag

photos_tag = db.Table('color_photos_tag',
                          db.Column('photos_id', db.Integer, db.ForeignKey('color_photos.id'), primary_key=True),
                          db.Column('tag_id', db.Integer, db.ForeignKey('color_tag.id'), primary_key=True)
                          )

class ColorPhotos(db.Model):
    __tablename__ = 'color_photos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    alt = db.Column(db.String(1000))
    save_name = db.Column(db.String(200))
    url = db.Column(db.String(200))
    m_url = db.Column(db.String(200))
    sm_url = db.Column(db.String(200))
    ext = db.Column(db.String(200))
    crawl_url = db.Column(db.String(500))
    crawl_m_url = db.Column(db.String(500))
    crawl_sm_url = db.Column(db.String(500))
    add_time = db.Column(db.Integer)
    photoset_id = db.Column(db.Integer)
    target_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    ai_parse = db.Column(db.Integer)
    status = db.Column(db.Integer)
    tags = db.relationship("ColorTag", lazy='dynamic', secondary=photos_tag)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, alt, save_name, url, m_url, sm_url, ext, crawl_url, crawl_m_url, crawl_sm_url,
                 add_time, photoset_id, target_id, author_id, ai_parse, status):
        self.name = name
        self.alt = alt
        self.save_name = save_name
        self.url = url
        self.m_url = m_url
        self.sm_url = sm_url
        self.ext = ext
        self.crawl_url = crawl_url
        self.crawl_m_url = crawl_m_url
        self.crawl_sm_url = crawl_sm_url
        self.add_time = add_time
        self.photoset_id = photoset_id
        self.target_id = target_id
        self.author_id = author_id
        self.ai_parse = ai_parse
        self.status = status

    def __repr__(self):
        return '<Photos %d>' % self.id + '|' + 'name %s' % self.name



class ColorPhotosSchema (ma.SQLAlchemySchema):
    class Meta:
        model = ColorPhotos
    id = ma.auto_field()
    name = ma.auto_field()
    alt = ma.auto_field()
    save_name = ma.auto_field()
    url = ma.auto_field()
    m_url = ma.auto_field()
    sm_url = ma.auto_field()
    ext = ma.auto_field()
    crawl_url = ma.auto_field()
    crawl_m_url = ma.auto_field()
    crawl_sm_url = ma.auto_field()
    crawl_sm_url = ma.auto_field()
    add_time = ma.auto_field()
    photoset_id = ma.auto_field()
    target_id = ma.auto_field()
    author_id = ma.auto_field()
    ai_parse = ma.auto_field()
    status = ma.auto_field()
    tags = ma.auto_field()
