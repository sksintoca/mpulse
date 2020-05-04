from flask import Flask, current_app, render_template, request, g, jsonify, Blueprint, url_for, make_response
from markupsafe import escape
import json, os, csv
from mpulse.models import Member, MemberSchema
from datetime import datetime
from mpulse import db
from werkzeug.utils import secure_filename
from sqlalchemy import exc

app = Flask(__name__)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

bp = Blueprint('members', __name__, template_folder='templates')

@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Read member by record id (Primary key)
@bp.route('/member/<int:id>')
@bp.route('/member/id/<int:id>')
def get_member(id):
    current_app.logger.debug('get_member by id: %d', id)
    m = Member.query.get(id)
    result = member_schema.dump(m)
    return jsonify(result) 

# Read member by phone number
@bp.route('/members/phone/<phone>')
def get_member_by_phone(phone):
    current_app.logger.debug('get_member by phone: %s', phone)
    m = Member.query.filter_by(phone=phone)
    result = members_schema.dump(m)
    return jsonify(result)

# Read member by client member id
@bp.route('/members/clientid/<clientid>')
def get_member_by_clientid(clientid=None):
    if (clientid == None):
       clientid = "1"
    current_app.logger.debug('get_member by client_member_id: %s', clientid)
    m = Member.query.filter_by(client_member_id=clientid)
    result = members_schema.dump(m)
    return jsonify(result)


# Delete one record or all records
@bp.route("/members/clear", methods=["DELETE"])
@bp.route("/members/clear/<clientid>", methods=["DELETE"])
def delete_member(clientid=None):
    num_rows_deleted = 0
    try:
        if (clientid != None):
            num_rows_deleted = Member.query.filter_by(client_member_id=clientid).delete()
            db.session.commit()
        else:
            num_rows_deleted = Member.query(Member).delete()
            db.session.commit()
    except:
        db.session.rollback()
    return {"message": "Deleted " + str(num_rows_deleted) + " rows"}

# Add new member from json 
@bp.route("/member", methods=["POST"])
def new_member():
    json_data = request.get_json(silent=True)
    if not json_data:
        return {"message": "Failed, No input data provided"}
    first = json_data["firstname"]
    last = json_data["lastname"]
    phone = json_data["phone"]
    clientid = json_data["client_member_id"]
    accountid = json_data["account_id"]
    member_existing = Member.query.filter_by(client_member_id=clientid).first()
    if member_existing is None:
        # Create a new member
        new_member = Member(firstname=first, lastname=last, phone=phone, client_member_id=clientid, account_id=accountid)
        try:
            db.session.add(new_member)
            db.session.commit()
            result =  {
                "message": "Member Id " + str(new_member.id) + " created",
                "data": member_schema.dump(new_member)
            }
        except exc.IntegrityError:
            result =  { "message": "Member Id " + str(new_member.id) + " already exists"}
        except exc.DBAPIError as e:
            result =  {"message": "Failed to add new Member due to error: " + str(e)}
        else:
            pass
        finally:
            pass
    else:
        result =  {"message": "Member Id " + str(member_existing.id) + " already exists"}

    return jsonify(result)    
 

# Read list of members, either all or for selected account
@bp.route("/members/")
@bp.route("/members/account/<int:account_id>")
def get_account_members(account_id=None):
    if (account_id == None):
        m = Member.query.all()
        result = members_schema.dump(m)
    else:
        current_app.logger.debug('get_account_members: %d', account_id)
        m = Member.query.filter_by(account_id=account_id)
        result = members_schema.dump(m)
    return jsonify(result)    

# Home page shows our documentation about api
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file_path = os.path.abspath(os.getcwd())
    if request.method == 'POST':
        f = request.files['file']
        f.save(file_path + secure_filename(f.filename)) 
        import_csv(f.filename)
    result = {"message": "imported " + str(f.filename)}
    return jsonify(result)


def import_csv(csvfile):
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                columns = {", ".join(row)}
                line_count += 1
            else:
                columns = {"', '".join(row[1:])}
                fields = (row[1:])
                line_count += 1
                # # Insert a row of data
                # insertsql = "INSERT INTO members (first_name, last_name, phone_number,client_member_id, account_id) VALUES (?, ?, ?, ?, ?)"
                new_member = Member(firstname=row[1], lastname=row[2], phone=row[3], client_member_id=row[4], account_id=row[5])
                try:
                    db.session.add(new_member)
                    db.session.commit()
                except exc.IntegrityError:
                    # click.echo(f'Line {line_count} was not unique {fields}')
                    pass
                except:
                    # click.echo(f'Line {line_count} failed insert {fields}')
                    pass
                else:
                    # click.echo(f'Line {line_count} sucess {fields}')
                    pass
                finally:
                    pass
 
