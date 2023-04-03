from flask import Flask, render_template, g, request, json, jsonify
from flask_restful import Api
from flask_cors import CORS

from resources.Project import Project

app = Flask(__name__)

app.app_context().push()

CORS(app)
api = Api(app)

# API Endpoints ------------
api.add_resource(Project, "/projects")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/emojis')
def emojis():
    with open('static/emojis.json', encoding="utf-8") as file:
        return jsonify(json.load(file))


@app.route('/harry-potter')
def harry_potter():
    with open('static/harry.json', encoding="utf-8") as file:
        return jsonify(json.load(file))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
