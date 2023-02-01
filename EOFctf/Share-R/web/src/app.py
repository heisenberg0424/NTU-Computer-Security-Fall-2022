from flask import Flask, g, request, redirect, render_template, session
from sqlite3 import connect
from subprocess import run
from os import path, urandom, mkdir

_DATABASE = '/app/database.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(32)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = connect(_DATABASE)
  return db

with app.app_context():
  db = get_db()
  db.cursor().execute("""
    CREATE TABLE IF NOT EXISTS users(
      id Integer PRIMARY KEY,
      username String NOT NULL UNIQUE,
      password String,
      count Integer DEFAULT 0
    );
  """)
  db.commit()

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

def safeJoin(_dir, _sub):
  filepath = path.join(_dir, _sub)
  realpath = path.realpath(filepath)
  if not _dir in path.commonpath((_dir, realpath)):
    return None
  return realpath

@app.route('/', methods=['GET'])
def index():
  if 'user' in session:
    return render_template('index.html', name=session['user'])
  return render_template('login.html')
  
@app.route('/login', methods=['POST'])
def login():
  username = request.form.get('username', '')
  password = request.form.get('password', '')
  if not get_db().execute("SELECT * FROM users WHERE username=? and password=?", [username, password]).fetchone():
    return 'Wrong username or password'
  session['user'] = username
  return redirect("/", code=302)

@app.route('/register', methods=['POST'])
def register():
  username = request.form.get('username', '')
  password = request.form.get('password', '')
  db = get_db()
  if db.execute("SELECT * FROM users WHERE username=? LIMIT 1", [username]).fetchone():
    return 'User already exist'
  db.execute("INSERT INTO users (username, password) VALUES (?, ?)", [username, password])
  db.commit()
  session['user'] = username
  return redirect("/", code=302)

@app.route('/upload', methods=['POST'])
def upload_file():
  if 'user' not in session:
    return 'Login first'
  if 'file' not in request.files or not request.files['file'].filename:
    return 'Missing file'

  _sub = session['user']
  file = request.files['file']
  tmppath = path.join('/tmp', urandom(16).hex())
  realpath = safeJoin('/app/static', _sub)
  if not realpath:
    return 'No path traversal'
  if not path.exists(realpath):
    mkdir(realpath)

  file.save(tmppath)
  returncode = run(['unzip', '-qo', tmppath, '-d', realpath]).returncode
  if returncode != 0:
    return 'Not a zip file'
  if not path.isfile(path.join(realpath, 'index.html')):
    return '"index.html" not found'
  return redirect(realpath[4:]+'/index.html', code=302)
  
if __name__ == "__main__":
  app.run(host="0.0.0.0")
