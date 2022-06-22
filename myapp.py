"""Import modules"""
from threading import Thread
from flask import Flask, render_template, request, session, copy_current_request_context
from searchletters import searchletters
from checker import check_logged_in
from DBcm import UseDatabase, ConnectionsError, CredentialsError, SQLError

#pylint: disable=W0703

app = Flask(__name__)

client = app.test_client()

app.config['dbconfig'] = { 'host': 'dbflask.cpovql6hlxi2.eu-central-1.rds.amazonaws.com',
                           'user': 'admin',
                           'password': 'Ad123456',
                           'database': 'flask_db', }

@app.route('/login')
def do_login():
    """A dummy docstring."""
    session['logged_in'] = True
    return 'You are now logged in.'

@app.route('/logout')
def do_logout():
    """A dummy docstring."""
    session.pop('logged_in')
    return 'You are now logged out.'

# def log_request(req: 'str', res: str):
#     """A dummy docstring."""
#     with UseDatabase(app.config['dbconfig']) as cursor:
#         sql = """insert into log
#                 (phrase, letters, ip, browser_string, results)
#                 values
#                 (%s, %s, %s, %s, %s)"""
#         cursor.execute(sql, (req.form['phrase'],
#                     req.form['letters'],
#                     req.remote_addr,
#                     req.headers.get('User-Agent'),
#                     res, ))

@app.route('/search4', methods=['POST'])
def do_search():
    """A dummy docstring."""
    @copy_current_request_context
    def log_request(req: 'str', res: str):
        with UseDatabase(app.config['dbconfig']) as cursor:
            sql = """insert into log
                    (phrase, letters, ip, browser_string, results)
                    values
                    (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (req.form['phrase'],
                        req.form['letters'],
                        req.remote_addr,
                        req.headers.get('User-Agent'),
                        res, ))
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(searchletters(phrase, letters))
    try:
        thread = Thread(target=log_request, args=(request, results))
        thread.start()
    except Exception as err:
        print('***** Logging failed with this error:', str(err))
    return render_template('results.html',
                        the_title=title,
                        the_phrase=phrase,
                        the_letters=letters,
                        the_results=results,)

@app.route('/')
@app.route('/entry')
def entry_page():
    """A dummy docstring."""
    return render_template('entry.html',
                    the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
@check_logged_in
def view_the_log():
    """A dummy docstring."""
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            sql = """select phrase, letters, ip, browser_string, results
                    from log"""
            cursor.execute(sql)
            contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                            the_title='View Log',
                            the_row_titles=titles,
                            the_data=contents,)
    except ConnectionsError as err:
        print('Is your database switched on? Error:', str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


app.secret_key = 'ItisMySecretKey '

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
