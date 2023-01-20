from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from markupsafe import Markup

app = Flask(__name__)
app.app_context().push()
CORS(app)
api = Api(app)


def make_svg(file_url):
    svg = open(file_url).read()
    return render_template('test.html', svg=Markup(svg))


projects = {
    '1': {
        'title': "Figma React",
        'description': "Comprehensive collection of little projects based on React, starring: Weather App, "
                       "Emoji Search App, Harry Potter char search app and much more!",
        'dateCreated': "September 23, 2021",
        'mainLanguage': "JavaScript",
        'tagIcons': {
            '1': make_svg("static/TagIcons/JavaScript.svg"),
            '2': make_svg("static/TagIcons/Kotlin.svg"),
        }
    },
    '2': {
        'title': "Daily Routine",
        'description': "Simple ToDo app with registration and authorization, based on React and Redux for state "
                       "management!",
        'dateCreated': "April 23, 2022",
        'mainLanguage': "JavaScript",
        'tagIcons': {
            '1': make_svg("static/TagIcons/JavaScript.svg"),
        }
    },
    '3': {
        'title': "This Site",
        'description': "Yep, this site is also a pet project, based on beautiful Svelte!",
        'dateCreated': "January 18, 2023",
        'mainLanguage': "TypeScript",
        'tagIcons': {
            '1': make_svg("static/TagIcons/TypeScript.svg")
        }
    }
}


class Project(Resource):
    def get(self):
        return jsonify(projects)


api.add_resource(Project, "/api/projects")

if __name__ == '__main__':
    app.run()
