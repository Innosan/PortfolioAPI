from flask import render_template
from flask_restful import Resource
from markupsafe import Markup

from db.db_connect import query_db


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