from flask import render_template
from flask_restful import Resource, reqparse, abort
from markupsafe import Markup

from db.db_connect import query_db

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('created_at')
parser.add_argument('thumbnail_url')
parser.add_argument('is_highlighted')
parser.add_argument('tags')


def make_svg(file_url):
    svg = open(file_url).read()
    return render_template('svg.html', svg=Markup(svg))


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

    def post(self):
        args = parser.parse_args()

        title = args['title']
        description = args['description']
        created_at = args['created_at']
        tags = args['tags']

        is_highlighted = args['is_highlighted']
        if is_highlighted == 'False':
            is_highlighted = 0
        else:
            is_highlighted = 1

        thumbnail_url = args['thumbnail_url']

        params = (
            title, description, created_at, tags, is_highlighted, thumbnail_url
        )

        query_db('INSERT INTO project (title, description, created_at, tags, is_highlighted, thumbnail_url) VALUES ( '
                 '?, ?, ?, ?, ?, ?)', params)

        return 'Project added successfully', 201
