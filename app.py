from flask import Flask, jsonify
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


@app.route('/api/projects', methods=['GET'])
def getProjects():
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

        return jsonify(items_list)
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/projects/<string:project_id>', methods=['GET'])
def getProject(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM {} WHERE project_id = {}".format("projects", project_id)
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
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

        return jsonify(items_list)
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/categories/<string:project_id>', methods=['GET'])
def getCategories(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT c.* FROM {} p INNER JOIN {} c ON c.project_id = p.project_id WHERE p.project_id = {}"\
            .format("projects", "categories", project_id)
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'category_id': item[0],
                'name': item[2],
                'confidence': item[3]
            }
            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/requirements/<string:project_id>', methods=['GET'])
def getRequirements(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT r.* FROM {} r WHERE r.project_id = {}"\
            .format("requirements", project_id)
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'requirement_id': item[0],
                'title': item[2],
                'description': item[3],
                'type': item[4],
                'rat': item[5],
                'language': item[6],
                'user_modified_at': str(item[7]),
                'bot_modified_at': str(item[8]),
                'created_at': str(item[9])
            }
            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    app.run(debug=True)