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


# Projects
@app.route('/api/projects', methods=['GET'])
def getProjects():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM projects_get_all ORDER BY name ASC;"
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'projectId': item[0],
                'name': item[1],
                'description': item[2],
                'size': item[3],
                'methodology': item[4],
                'translated': item[5],
                'classified': item[6],
                'userModifiedAt': str(item[7]),
                'botModifiedAt': str(item[8]),
                'createdAt': str(item[9]),
                'categoriesCount': item[10],
                'requirementsCount': item[11],
                'tasksCount': str(item[12]),
                'percentageCompleted': str(item[13])
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
                'size': item[3],
                'methodology': item[4],
                'translated': item[5],
                'classified': item[6],
                'userModifiedAt': str(item[7]),
                'botModifiedAt': str(item[8]),
                'createdAt': str(item[9]),
                'categoriesCount': item[10],
                'requirementsCount': item[11],
                'tasksCount': str(item[12]),
                'percentageCompleted': str(item[13])
            }

            if i['percentageCompleted'] == 'None':
                i['percentageCompleted'] = 0;

            items_list.append(i)

        return jsonify(items_list[0])
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/projects', methods=['POST'])
def postProject():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `projects` (`name`, `description`, `size`, `methodology`, `user_modified_at`, `created_at`) " \
            u"VALUES (%s, %s, %s, %s, now(), now())"

        cursor.execute(q, (data['name'], data['description'], data['size'], data['methodology']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/projects/<string:project_id>', methods=['DELETE'])
def deleteProject(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" DELETE FROM `projects` WHERE `project_id` = %s"

        cursor.execute(q, (project_id))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/projects/<string:project_id>', methods=['PUT'])
def putProject(project_id):
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" UPDATE `projects` SET `name`=%s, `description`=%s, `size`=%s, " \
            u" `methodology`=%s, `user_modified_at`=now()" \
            u" WHERE `project_id` = %s"

        cursor.execute(q, (data['name'], data['description'], data['size'], data['methodology'], data['projectId']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/projects/requirements/<string:project_id>', methods=['GET'])
def getRequirementsByProjectId(project_id):
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
                'projectId': item[1],
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

@app.route('/api/projects/categories/<string:project_id>', methods=['GET'])
def getCategoriesByProjectId(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = u"SELECT    c.* FROM {} p " \
                u"INNER JOIN {} c ON c.project_id = p.project_id " \
                u"WHERE     p.project_id = {} " \
                .format("projects", "categories", project_id)
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'categoryId': item[0],
                'name': item[2],
                'confidence': item[3]
            }
            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return {'error': str(e)}


# Categories
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


# Requirements
@app.route('/api/requirements/<string:requirement_id>', methods=['GET'])
def getRequirement(requirement_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM requirements_get_all WHERE requirement_id = {}"\
            .format(requirement_id)
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'requirementId': item[0],
                'projectId': item[1],
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

        return jsonify(items_list[0])
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/requirements', methods=['POST'])
def postRequirement():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `requirements` (`title`, `description`, `project_id`, `type`, `rat`, `user_modified_at`, `created_at`) " \
            u"VALUES (%s, %s, %s, %s, %s, now(), now())"

        cursor.execute(q, (data['title'], data['description'], data['projectId'], data['type'], data['rat']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/requirements/<string:requirement_id>', methods=['PUT'])
def putRequirement(requirement_id):
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" UPDATE `requirements` SET `title`=%s, `description`=%s, `project_id`=%s, " \
            u" `type`=%s, `rat`=%s, `user_modified_at`=now()" \
            u" WHERE `requirement_id` = %s"

        cursor.execute(q, (data['title'], data['description'], data['projectId'], data['type'],
                           data['rat'], data['requirementId']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/requirements/<string:requirement_id>', methods=['DELETE'])
def deleteRequirement(requirement_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" DELETE FROM `requirements` WHERE `requirement_id` = %s"

        cursor.execute(q, (requirement_id))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)


# Recommendations
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
                'projectAPercentageCompleted': str(item[4]),
                'requirementADescription': item[5],
                'requirementBId': item[6],
                'projectBId': item[7],
                'projectBName': item[8],
                'projectBPercentageCompleted': str(item[9]),
                'requirementBDescription': item[10],
                'distance': str(item[11]),
                'createdAt': str(item[12]),
                'createdAtDays': item[13]
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
                'projectAPercentageCompleted': str(item[4]),
                'requirementADescription': item[5],
                'requirementBId': item[6],
                'projectBId': item[7],
                'projectBName': item[8],
                'projectBPercentageCompleted': str(item[9]),
                'requirementBDescription': item[10],
                'distance': str(item[11]),
                'createdAt': str(item[12]),
                'createdAtDays': item[13]
            }
            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/recommendations/projects', methods=['POST'])
def postRecommendation():
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


# Tasks
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

            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/tasks', methods=['POST'])
def postTask():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `tasks` (`name`, `requirement_id`, `percentage_completed`, `created_at`) " \
            u"VALUES (%s, %s, %s, now())"

        cursor.execute(q, (data['name'], data['requirementId'], data['percentageCompleted']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/tasks/<string:task_id>', methods=['PUT'])
def putTask(task_id):
    data = request.json

    print(data)

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" UPDATE `tasks` SET `name`=%s, `percentage_completed`=%s, `user_modified_at`=now() " \
            u" WHERE `task_id` = %s"

        cursor.execute(q, (data['name'], data['percentageCompleted'], data['taskId']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/tasks/<string:task_id>', methods=['DELETE'])
def deleteTask(task_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" DELETE FROM `tasks` WHERE `task_id` = %s"

        cursor.execute(q, (task_id))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)


#Settings
@app.route('/api/settings', methods=['GET'])
def getSettings():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM settings;"
        cursor.execute(query)
        data = cursor.fetchall()

        items_list = [];

        for item in data:
            i = {
                'onlyProjectsSameSize': item[0],
                'onlyProjectsSameMethodology': item[1],
                'distanceAcceptedBetweenRequirements': str(item[2]),
                'differenceAcceptedBetweenProjectsPercentage': str(item[3])
            }

            if i['distanceAcceptedBetweenRequirements'] == 'None':
                i['distanceAcceptedBetweenRequirements'] = 0;

            if i['differenceAcceptedBetweenProjectsPercentage'] == 'None':
                i['differenceAcceptedBetweenProjectsPercentage'] = 0;

            items_list.append(i)

        return jsonify(items_list)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/settings', methods=['POST'])
def postSettings():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `settings` (`only_projects_same_size`, `only_projects_same_methodology`, " \
            u"`distance_accepted_between_requirements`, `difference_accepted_between_projects_percentage`) " \
            u"VALUES (%s, %s, %s, %s)"

        cursor.execute(q, (data['onlyProjectsSameSize'], data['onlyProjectsSameMethodology'],
                           data['distanceAcceptedBetweenRequirements'],
                           data['differenceAcceptedBetweenProjectsPercentage']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)

@app.route('/api/settings', methods=['PUT'])
def putSettings():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" UPDATE `settings` SET `only_projects_same_size`=%s, `only_projects_same_methodology`=%s, " \
            u"`distance_accepted_between_requirements`=%s, `difference_accepted_between_projects_percentage`=%s "

        cursor.execute(q, (data['onlyProjectsSameSize'], data['onlyProjectsSameMethodology'],
                           data['distanceAcceptedBetweenRequirements'],
                           data['differenceAcceptedBetweenProjectsPercentage']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify(request.json)


if __name__ == '__main__':
    app.run(debug=True, port=5000)