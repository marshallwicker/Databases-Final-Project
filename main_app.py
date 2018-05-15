import json
import MySQLdb
import MySQLdb.cursors
from functools import wraps
import flask
app = flask.Flask(__name__, static_folder='static', static_url_path='')


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = flask.request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs)) + ')'
            return flask.current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('mainpage.html', title='Search')


@app.route('/advancedsearch/')
def advanced_search():
    return flask.render_template('advancedsearch.html', title='Advanced Search')


@app.route('/compare/', methods=['GET', 'POST'])
def compare():
    if flask.request.method == 'GET':
        return flask.render_template('compare.html', title='Compare')
    else:
        return ''


@app.route('/about/')
def about():
    return flask.redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


@app.route('/search', methods=['POST'])
def basic_search():
    search_value = flask.request.form['searchInput']
    search_type = flask.request.form['searchon']
    query_string = ""
    columns = []
    if search_type == 'cname':
        columns = ['title', 'full_name', 'website', 'ticker', 'industry', 'sector']
        query_string = ("SELECT * FROM (company NATURAL JOIN alias NATURAL JOIN industry NATURAL JOIN sector)"
                        " WHERE title LIKE %s;")
    elif search_type == 'ceo':
        columns = ['title', 'ceo', 'employees']
        query_string = ("SELECT * FROM (company INNER JOIN ceotitle c ON company.ceo_title_ID = c.ceo_title_ID)"
                        " WHERE ceo LIKE %s;")
    elif search_type == 'state':
        columns = ['title', 'hq_state', 'street', 'city', 'zip']
        query_string = ("SELECT * FROM (company NATURAL JOIN hq)"
                        " WHERE hq_state LIKE %s;")
    elif search_type == 'ticker':
        columns = ['title', 'year', 'revenues', 'assets', 'ticker']
        query_string = ("SELECT * FROM (company NATURAL JOIN alias NATURAL JOIN yearrank)"
                        " WHERE ticker LIKE %s;")
    conn = MySQLdb.connect(host='localhost',
                           user='searchquery',
                           passwd='',
                           db='companyDB',
                           cursorclass=MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute(query_string, [search_value + '%'])
    rs = c.fetchall()
    return flask.render_template('company.html', title='Results', columns=columns, data=[r for r in rs])


@app.route('/json/company/<title>')
@support_jsonp
def json_company(title):
    conn = MySQLdb.connect(host='localhost',
                           user='searchquery',
                           passwd='',
                           db='companyDB',
                           cursorclass=MySQLdb.cursors.DictCursor)
    c = conn.cursor()
    c.execute('SELECT title, full_name, website, ticker, industry, sector FROM '
              '(company NATURAL JOIN alias NATURAL JOIN industry NATURAL JOIN sector) '
              'WHERE title LIKE %s', [title + '%'])
    if c.rowcount > 0:
        rs = c.fetchall()
        result_list = [r for r in rs]
    s = json.dumps({'companies': result_list})
    return s


if __name__ == '__main__':
    app.run(port=42069, debug=True)
