from flask_restful import Resource, reqparse, fields
from app.helpers.rest import *
# from app.helpers.memcache import *
from app.middlewares.auth import jwt_required
from flask_jwt_extended import get_jwt_identity
import datetime
from app.models import model as db
import werkzeug, os
from app import APP_ROOT
from app.libs import utils


BLESS_FOLDER = '/static/bless'

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
        project_id = None

        id_userdata = db.get_by_id("tb_user","username", c_user)
        id_userdata = id_userdata[0]['id_userdata']
        obj_insert = {
            "id_userdata": str(id_userdata),
            "nm_project_app": app_name,
            "nm_project_port":app_port
        }
        try:
            project_id = db.insert(table="tb_project_app", data=obj_insert)
        except Exception as e:
            return response(401, message=str(e))
        if project_id:
            upload_folder = APP_ROOT+BLESS_FOLDER+"/"+project_id+"/"
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
                bless_file.save(upload_folder+"bless.yml")
            else:
                bless_file.save(upload_folder+"bless.yml")
            
            url_ops = os.getenv("OPENSTACK_URL")+":"+os.getenv("OPENSTACK_PORT")
            url_create = url_ops+"/api/create"

            headers ={
                "Access-Token": os.getenv("TOKEN_OPENSTACK")
            }
            send_to_openstack={
                "instances": {
                    app_name: {
                        "parameters": {
                            "project_id": project_id,
                            "app_name": app_name,
                            "app_port":app_port,
                            "private_network": "vm-net",
                            "key_name": "vm-key",
                            "username": username
                        },
                        "template": "bless"
                    }
                }
            }
            res_fix = dict()
            data_create = list()
            data_respon = list()
            data_pemkey = ""
            try:
                data_create = utils.send_http(url_create, data=send_to_openstack, headers=headers)
                url_vm = url_ops+"/api/list/vm"
                url_pemkey = url_ops+"/api/list/pemkey/"+app_name
                c_limit = True;
                while c_limit:
                    data_vm = utils.get_http(url_vm, headers=headers)
                    for i in data_vm['data']:
                        if i['name'] == app_name:
                            res_fix = i
                            c_limit = False
                    data_pemkey = utils.get_http(url_pemkey, headers=headers)
            except Exception as e:
                return response(401, message=str(e))
            else:
                data_respon.append({
                    "create": data_create['data'],
                    "vm": res_fix,
                    "pemkey": data_pemkey
                })
                return response(200, data=data_respon)

