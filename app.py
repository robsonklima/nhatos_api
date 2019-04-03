#region Imports

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
import json, re, simplejson, decimal, datetime

from camel_encoder import CamelEncoder
from decimal_encoder import DecimalJSONEncoder
from datetime_encoder import DatetimeEncoder

#endregion

#region Configuration

with open('config/config.json') as json_data_file:
    config = json.load(json_data_file)

mysql = MySQL()
app = Flask(__name__)
app.config[u"DEBUG"] = config["DEBUG"]
app.config[u'MYSQL_DATABASE_HOST'] = config["HOST"]
app.config[u'MYSQL_DATABASE_DB'] = config["DB"]
app.config[u'MYSQL_DATABASE_USER'] = config["USER"]
app.config[u'MYSQL_DATABASE_PASSWORD'] = config["PASS"]
mysql.init_app(app)
api = Api(app)

#endregion

#region Methods

def camel_to_underscore(name):
    return re.compile(r'([A-Z])').sub(lambda x: '_' + x.group(1).lower(), name)

def underscore_to_camel(name):
    return re.compile(r'_([a-z])').sub(lambda x: x.group(1).upper(), name)

def datetime_encoder(o):
    if isinstance(o, datetime.datetime):
        return (o.isoformat())
    else:
        TypeError("Unknown serializer")

#endregion

#region Classes

class DecimalEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalJSONEncoder, self).default(o)

#endregion

#region Resource Projects

@app.route('/api/projects', methods=['GET'])
def getProjects():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM projects_get_all ORDER BY name ASC;"
        cursor.execute(query)
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/projects/<string:project_id>', methods=['GET'])
def getProject(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM projects_get_all WHERE project_id = {};".format(project_id)
        cursor.execute(query)
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/projects', methods=['POST'])
def postProject():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `projects` (`name`, `description`, `size`, `methodology`) " \
            u"VALUES (%s, %s, %s, %s)"

        cursor.execute(q, (data['name'], data['description'], data['size'], data['methodology']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify([data])

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
            u" `methodology`=%s" \
            u" WHERE `project_id` = %s"

        cursor.execute(q, (data['name'], data['description'], data['size'], data['methodology'], data['projectId']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify([data])

@app.route('/api/projects/requirements/<string:project_id>', methods=['GET'])
def getRequirementsByProjectId(project_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM requirements_get_all WHERE project_id = {}"\
            .format(project_id)
        cursor.execute(query)
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
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
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
    except Exception as e:
        return {'error': str(e)}

#endregion

#region Resource Categories

@app.route('/api/categories', methods=['GET'])
def getCategories():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM categories_get_all;"
        cursor.execute(query)
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
    except Exception as e:
        return jsonify({'error': str(e)})

#endregion

#region Resource Requirements

@app.route('/api/requirements/<string:requirement_id>', methods=['GET'])
def getRequirement(requirement_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM requirements_get_all WHERE requirement_id = {}".format(requirement_id)
        cursor.execute(query)
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/requirements', methods=['POST'])
def postRequirement():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `requirements` (`title`, `description`, `project_id`, `type`, `rat`) " \
            u"VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(q, (data['title'], data['description'], data['projectId'], data['type'], data['rat']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify([data])

@app.route('/api/requirements/<string:requirement_id>', methods=['PUT'])
def putRequirement(requirement_id):
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" UPDATE `requirements` SET `title`=%s, `description`=%s, `project_id`=%s, " \
            u" `type`=%s, `rat`=%s" \
            u" WHERE `requirement_id` = %s"

        cursor.execute(q, (data['title'], data['description'], data['projectId'], data['type'],
                           data['rat'], data['requirementId']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify([data])

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

#endregion

#region Resource Recommendations

@app.route('/api/recommendations/requirements/<string:requirement_id>', methods=['GET'])
def getRecommendationsByRequirementId(requirement_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM recommendations_get_all " \
                u"WHERE requirement_a_id = {} ORDER BY {} ASC;".format(requirement_id, "distance")
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
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
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/recommendations/projects', methods=['POST'])
def postRecommendation():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `requirements_recommendations` " \
            u"(`project_id`, `recommendation_id`, `accepted`) " \
            u"VALUES (%s, %s, %s)"

        cursor.execute(q, (data['projectAId'], data['recommendationId'], data['accepted']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify([data])

#endregion

#region Resource Tasks

@app.route('/api/tasks/<string:requirement_id>', methods=['GET'])
def getTasksByRequirementId(requirement_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM tasks_get_all " \
                u"WHERE requirement_id = {} " \
                u"ORDER BY {} ASC;".format(requirement_id, "name")
        cursor.execute(query)
        row_headers = [CamelEncoder.underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/tasks', methods=['POST'])
def postTask():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `tasks` (`name`, `requirement_id`, `percentage_completed`) " \
            u"VALUES (%s, %s, %s)"

        cursor.execute(q, (data['name'], data['requirementId'], data['percentageCompleted']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify([data])

@app.route('/api/tasks/<string:task_id>', methods=['PUT'])
def putTask(task_id):
    data = request.json

    print(jsonify(data))

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        q = u" UPDATE `tasks` SET `name`=%s, `percentage_completed`=%s" \
            u" WHERE `task_id` = %s"

        cursor.execute(q, (data['name'], data['percentageCompleted'], data['taskId']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify([data])

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

#endregion

#region Resource Settings

@app.route('/api/settings', methods=['GET'])
def getSettings():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query = u"SELECT * FROM settings ORDER BY 1 DESC LIMIT 1;"
        cursor.execute(query)
        row_headers = [underscore_to_camel(x[0]) for x in cursor.description]
        data = cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))

        return simplejson.dumps(json_data, default=datetime_encoder, cls=DecimalEncoder, sort_keys=True, indent=4)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/settings', methods=['POST'])
def postSettings():
    data = request.json

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        q = u"INSERT INTO `settings` (`only_projects_same_size`, `only_projects_same_methodology`, " \
            u"`distance_accepted_between_requirements`, `difference_accepted_between_projects_percentage`)" \
            u"VALUES (%s, %s, %s, %s);"

        cursor.execute(q, (data['onlyProjectsSameSize'], data['onlyProjectsSameMethodology'],
                           data['distanceAcceptedBetweenRequirements'],
                           data['differenceAcceptedBetweenProjectsPercentage']))
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return jsonify([data])

#endregion

#region Init

if __name__ == '__main__':
    app.run(debug=True, port=5000)

#endregion