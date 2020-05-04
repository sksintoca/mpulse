from . import db
from dataclasses import dataclass
from sqlalchemy_serializer import SerializerMixin
from marshmallow import Schema, fields, ValidationError, pre_load

@dataclass
class Member(db.Model, SerializerMixin):
    id: int
    firstname: str
    lastname: str
    phone: str
    client_member_id: str
    account_id:  int

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


class MemberSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.Str()
    lastname = fields.Str()
    phone = fields.Str()
    client_member_id = fields.Str()
    account_id = fields.Int()
