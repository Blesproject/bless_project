from flask_restful import Resource, reqparse, fields
from app.helpers.rest import *
# from app.helpers.memcache import *
from app.middlewares.auth import jwt_required
from flask_jwt_extended import get_jwt_identity
import datetime
from app.models import model as db
import werkzeug, os
from app import APP_ROOT


BLESS_FOLDER = '/static/bless/'


class ProjectCreate(Resource):
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('app_name', type=str, required=True)
        parser.add_argument('app_port', type=str, required=True)
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('bless_file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        bless_file = args['bless_file']
        username =args['username']
        app_port = args['app_port']
        app_name = args['app_name']
        
        c_user = get_jwt_identity()
        upload_folder = APP_ROOT+BLESS_FOLDER+"/"+c_user+"/"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        bless_f_check = None
        try:
            bless_file.save(upload_folder+"bless.yml")
        except Exception as e:
            raise e
        else:
            bless_f_check = True
        if bless_f_check:
            id_userdata = db.get_by_id("tb_user","username", c_user)
            id_userdata = id_userdata[0]['id_userdata']
            obj_insert = {
                "id_userdata": str(id_userdata),
                "nm_project_app": app_name,
                "nm_project_port":app_port
            }
            try:
                db.insert(table="tb_project_app", data=obj_insert)
            except Exception as e:
                raise e
        
