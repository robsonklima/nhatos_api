from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config["DEBUG"] = False
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_DB'] = 'nhatos'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Mysql@2018'
mysql.init_app(app)
api = Api(app)


class Project(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "SELECT * FROM {} ORDER BY {} ASC".format("projects", "project_id")
            cursor.execute(query)
            data = cursor.fetchall()

            items_list = [];

            for item in data:
                #print(item[5])

                i = {
                    'project_id': item[0],
                    'name': item[1],
                    'description': item[2],
                    'language': item[3],
                    'user_modified_at': str(item[4]),
                    'bot_modified_at': str(item[5]),
                    'created_at': str(item[6])
                }
                items_list.append(i)

            return items_list
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Project, '/api/projects')

if __name__ == '__main__':
    app.run(debug=True)