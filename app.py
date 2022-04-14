import os
import urllib.parse as urlparse

from cgitb import text
import string
from flask import Flask, render_template, request, redirect, url_for, abort

import psycopg2
from psycopg2 import pool

import toml

import math

from models import Page

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
    ps_connection = postgreSQL_pool.getconn()
    cursor = ps_connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    cursor.close()
    postgreSQL_pool.putconn(ps_connection)
    return result


def fetchall(query, params):
    ps_connection = postgreSQL_pool.getconn()
    cursor = ps_connection.cursor()
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
        ps_connection.rollback()
    finally:
        cursor.close()
        postgreSQL_pool.putconn(ps_connection)
    return results


def fetchpage(query, page_number, params):
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
    return Page(page_content, math.ceil(count/10), page_number)


@app.context_processor
def inject_stage_and_region():
    return dict(fetchone=fetchone, fetchall=fetchall, fetchpage=fetchpage)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/test', methods=['GET'])
def test():
    page = request.args.get('page', default = 1, type = int)
    template = request.args.get('template', default = "space/index.html.j2")
    frame = request.args.get('frame')
    return render_template("pages/" + template, page = page, math = math, frame = frame)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True)
