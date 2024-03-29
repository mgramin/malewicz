import os
import urllib.parse as urlparse

from query import Query

from cgitb import text
from flask import Flask, render_template, request, Response, redirect, url_for, abort

from flask_accept import accept


import psycopg2
from psycopg2 import pool

import toml

import math

from models import Page, Data

from psycopg2.extras import DictCursor

from jinja2 import Template


app = Flask(__name__)

config = toml.load("config.toml")

try:
    DATABASE_URL = os.environ['DATABASE_URL']
    url = urlparse.urlparse(DATABASE_URL)
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port
except KeyError:
    dbname = config["database"]
    user = config["user"]
    password = config["password"]
    host = config["host"]
    port = config["port"]


postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user=user,
                                                         password=password,
                                                         host=host,
                                                         port=port,
                                                         database=dbname,
                                                         cursor_factory=DictCursor)




def fetchone(query, params):
    try:
        ps_connection = postgreSQL_pool.getconn()
        cursor = ps_connection.cursor()
        cursor.execute(str(query), params)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(e)
        print(query)
        ps_connection.rollback()
    finally:
        cursor.close()
        postgreSQL_pool.putconn(ps_connection)


def fetchall(query, params):
    ps_connection = postgreSQL_pool.getconn()
    cursor = ps_connection.cursor()
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        fields = [i[0] for i in cursor.description]
    except Exception as e:
        ps_connection.rollback()
    finally:
        cursor.close()
        postgreSQL_pool.putconn(ps_connection)
    return Data(results, fields) 


def fetchpage(query, page_number, params):
    try:
        query_test = Query(query)
        query_test.parse()

        # 1. get rows count (with count.sql.j2 template)
        with open('templates/sql/count.sql.j2', 'r') as file:
            data = file.read().rstrip()
        count_template = Template(data)
        result = count_template.render(query_text=query)
        count = fetchone(result, params)["result"]
        
        # 2. get rows for page (with pageable.j2.sql template)
        with open('templates/sql/pageable.sql.j2', 'r') as file:
            data = file.read().rstrip()
        page_template = Template(data)
        result = page_template.render(query_text=query, page=page_number)
        page_content = fetchall(result, params)

        # 3. responce with object { rows, total_pages, current_page, next_page, prev_page }
        # TODO put in page size in params file
        new_page = Page(page_content.rows, math.ceil(count/15), page_number, query_test.columns, query_test)
        return new_page

    except Exception as err:
        print(err)
        print(query)
    


def fetchcount(query, params):
    with open('templates/sql/count.sql.j2', 'r') as file:
        data = file.read().rstrip()
    count_template = Template(data)
    result = count_template.render(query_text=query)
    count = fetchone(result, params)["result"]
    return count


@app.context_processor
def inject_stage_and_region():
    return dict(fetchone=fetchone, fetchall=fetchall, fetchpage=fetchpage, fetchcount=fetchcount)


@app.route('/', methods=['GET', 'POST'])
def index():
    template = request.args.get('template', default = "overview")
    return render_template('index.html', template = template)


@app.route('/test', methods=['GET'])
def test():
    page = request.args.get('page', default = 1, type = int)
    template = request.args.get('template', default = "overview/index.html.j2")
    frame = request.args.get('frame')

    params = request.args.to_dict()
    x = '&'.join('='.join((key,val)) for (key,val) in params.items())

    return render_template("pages/" + template, template=template, page = page, math = math, frame = frame, params = params, params_str = x)


@app.route('/<section>', methods=['GET'])
def test2(section):
    try:
        assert section == request.view_args['section']
        page = request.args.get('page', default = 1, type = int)

        params = request.args.to_dict()
        x = '&'.join('='.join((key,val)) for (key,val) in params.items())

        val = render_template('index.html', template = section, page = page, params = params, params_str = x)
        return Response(val, mimetype='text/html')
    except Exception as e:
        print(e)


@app.route('/test_part/<section>', methods=['GET'])
def test_part(section):
    assert section == request.view_args['section']
    page = request.args.get('page', default = 1, type = int)
    template = section + "/index.html.j2"
    frame = request.args.get('frame')

    params = request.args.to_dict()
    x = '&'.join('='.join((key,val)) for (key,val) in params.items())

    return render_template("pages/" + template, template = section, page = page, math = math, frame = frame, params = params, params_str = x)



@app.route('/api/query/<query_name>', methods=['GET'])
@accept('text/csv')
def test_test(query_name):
    with open('templates/sql/' + query_name + '.sql', 'r') as file:
        query = file.read().replace('\n', '')

    data = fetchall(query, [])
    keys = data[0].keys()
    result = [list(keys)] + [list(row.values()) for row in data]
    str_result = '\n'.join([';'.join(str(val) for val in row) for row in result])
    return str_result



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
