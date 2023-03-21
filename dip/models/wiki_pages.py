from dip.extensions import db

class WikiPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)

    md_page_path = db.Column(db.String(255))

    owner_id = db.Column(db.ForeignKey('users.id'))
    owner = db.relationship('User', back_populates='wiki_pages')