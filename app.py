from flask import Flask, render_template, g
from flask_restful import Resource, Api
from flask_cors import CORS
from markupsafe import Markup

from db.db_connect import query_db

app = Flask(__name__)
app.app_context().push()
CORS(app)
api = Api(app)


def make_svg(file_url):
    svg = open(file_url).read()
    return render_template('test.html', svg=Markup(svg))


# API Methods ------------
class Project(Resource):

    def get(self):
        my_projects = query_db('select * from project')

        # Transforming string with indexes of Icons
        # into actual array of indexes
        for project in my_projects:
            tags = project['tags'].split(', ')
            project['tags'] = tags

            i = 0
            # Getting icons and transforming
            # path to the file to SVG tags
            while i < len(project['tags']):
                project['tags'][i] = query_db('select * from tag where id = {}'.format(i + 1), one=True)
                project['tags'][i]['path'] = make_svg(project['tags'][i]['path'])
                i += 1

        return my_projects


# API Endpoints ------------
api.add_resource(Project, "/projects")

@app.route('/')
def index():
    return render_template(main.html)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()
