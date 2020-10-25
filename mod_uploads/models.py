from app import db
import datetime


class File(db.Model):
    id=db.Column(db.Integer ,primary_key=True)
    file_name=db.Column(db.String(256),nullable=False)
    upload_date=db.Column(db.DateTime(),nullable=False,default=datetime.datetime.utcnow)