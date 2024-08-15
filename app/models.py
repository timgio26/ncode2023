from app import db

class userName(db.Model):
    __tablename__ = 'username'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(20))
    username = db.Column(db.String(10))
    password = db.Column(db.String(10))
    kode = db.Column(db.String(200))
    bingodate=db.Column(db.String(75))
    # reqstat= db.Column(db.String(10))