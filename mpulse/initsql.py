from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

file_path = os.path.abspath(os.getcwd())+"/mpulse.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    client_member_id = db.Column(db.String(120), unique=True, nullable=False)
    account_id = db.Column(db.Integer, unique=False, nullable=False)
 
    def __init__(self, firstname, lastname, phone, client_member_id, account_id):
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.client_member_id = client_member_id
        self.account_id = account_id

    def __repr__(self):
        return '<Member %r>' % (self.firstname + " " + self.lastname)

db.create_all()
# db.drop_all()
# steve = Member('Steve', 'Schiller', '805-217-8702', '12345', 1)
# db.session.add(steve)
# db.session.commit()
newrec = Member.query.all()
print (newrec)
