from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

def many_to_many(name, fromtable, totable):
    lfromtable = fromtable.lower()
    ltotable = totable.lower()
    table = db.Table(name,
        db.Column(ltotable + '_id', db.Integer, db.ForeignKey(lltotable + '.id')),
        db.Column(lfromtalbe + '_id', db.Integer, db.ForeignKey(fromtable + '.id'))
    )
    
    return db.relationship(totable, secondary=table,
        backref=db.backref(lfromtable+'s', lazy='dynamic'))
    
class Base(db.Model):
    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,  
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
        
    def __repr__(self):
        return '<'+self.__class__.__name__+': {}>'.format(self.id)

