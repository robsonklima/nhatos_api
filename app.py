from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
import json


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
        query = u"SELECT * FROM projects_get_all;"
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'projectId': item[0],
                'name': item[1],
                'description': item[2],
                'translated': item[3],
                'classified': item[4],
                'userModifiedAt': str(item[5]),
                'botModifiedAt': str(item[6]),
                'createdAt': str(item[7]),
                'categoriesCount': item[8],
                'requirementsCount': item[9],
                'tasksCount': str(item[10]),
                'percentageCompleted': str(item[11]),
                'size': item[12],
                'methodology': item[13],
                'recommendationsCount': item[14]
            }

            if i['percentageCompleted'] == 'None':
                i['percentageCompleted'] = 0;

            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/projects/<string:project_id>', methods=['GET'])
def getProject(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM projects_get_all WHERE project_id = {};".format(project_id)
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'projectId': item[0],
                'name': item[1],
                'description': item[2],
                'translated': item[3],
                'classified': item[4],
                'userModifiedAt': str(item[5]),
                'botModifiedAt': str(item[6]),
                'createdAt': str(item[7]),
                'categoriesCount': item[8],
                'requirementsCount': item[9],
                'tasksCount': str(item[10]),
                'percentageCompleted': str(item[11]),
                'size': item[12],
                'methodology': item[13],
                'recommendationsCount': item[14]
            }

            if i['percentageCompleted'] == 'None':
                i['percentageCompleted'] = 0;

            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/categories', methods=['GET'])
def getCategories():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM categories_get_all;"

        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'title': item[0],
                'projectsCount': item[1]
            }
            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/categories/<string:project_id>', methods=['GET'])
def getCategoriesByProjectId(project_id):
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

        query = "SELECT * FROM requirements_get_all WHERE project_id = {}"\
            .format(project_id)
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'requirementId': item[0],
                'title': item[2],
                'description': item[3],
                'type': item[4],
                'rat': item[5],
                'translated': item[6],
                'userModifiedAt': str(item[7]),
                'botModifiedAt': str(item[8]),
                'createdAt': str(item[9]),
                'tasksCount': str(item[10]),
                'percentageCompleted': str(item[11])
            }

            if i['percentageCompleted'] == 'None':
                i['percentageCompleted'] = 0;

            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/recommendations/requirements/<string:requirement_id>', methods=['GET'])
def getRecommendationsByRequirementId(requirement_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM recommendations_get_all WHERE requirement_a_id = {} ORDER BY {} ASC;"\
            .format(requirement_id, "distance")

        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'recommendationId': item[0],
                'requirementAId': item[1],
                'projectAId': item[2],
                'projectAName': item[3],
                'requirementADescription': item[4],
                'requirementBId': item[5],
                'projectBId': item[6],
                'projectBName': item[7],
                'requirementBDescription': item[8],
                'distance': str(item[9]),
                'createdAt': str(item[10]),
                'createdAtDays': item[11]
            }
            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/recommendations/projects/<string:project_id>', methods=['GET'])
def getRecommendationsByProjectId(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM recommendations_get_all WHERE project_a_id = {} ORDER BY {};"\
            .format(project_id, "distance")

        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'recommendationId': item[0],
                'requirementAId': item[1],
                'projectAId': item[2],
                'projectAName': item[3],
                'requirementADescription': item[4],
                'requirementBId': item[5],
                'projectBId': item[6],
                'projectBName': item[7],
                'requirementBDescription': item[8],
                'distance': str(item[9]),
                'createdAt': str(item[10]),
                'createdAtDays': item[11]
            }
            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/recommendations/projects', methods=['POST'])
def post():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `requirements_recommendations` (`project_id`, `recommendation_id`, `accepted`, `created_at`) " \
            u"VALUES (%s, %s, %s, now())"

        cursor.execute(q, (data['projectAId'], data['recommendationId'], data['accepted']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/tasks/<string:requirement_id>', methods=['GET'])
def getTasksByRequirementId(requirement_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM tasks_get_all WHERE requirement_id = {} ORDER BY {} ASC;"\
            .format(requirement_id, "name")

        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'taskId': item[0],
                'name': item[1],
                'requirementId': item[2],
                'percentageCompleted': str(item[3])
            }

            if i['percentageCompleted'] == 'None':
                i['percentageCompleted'] = 0;

            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)