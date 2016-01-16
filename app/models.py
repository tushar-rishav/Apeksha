from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    reg_id = db.Column(db.String(40), primary_key=True)
    def __init__(self, reg_id):
        self.reg_id = reg_id.upper()

class Respon(db.Model):
    __tablename__ = 'response'
    reg_id = db.Column(db.String(40), primary_key=True)
    Mathematics = db.Column(db.String(100))
    Physics = db.Column(db.String(100))
    Chemistry = db.Column(db.String(100))
    
    def __init__(self, reg_id, Physics,Chemistry,Mathematics):
        self.reg_id = reg_id.upper()
        self.Physics = Physics.upper()
        self.Chemistry = Chemistry.upper()
        self.Mathematics = Mathematics.upper()
        

