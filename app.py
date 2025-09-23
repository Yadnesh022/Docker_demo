from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# --- MySQL Configuration ---
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass'
app.config['MYSQL_DB'] = 'flask_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# ✅ UPDATE user
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    # For GET request → fetch existing user details
    cur.execute("SELECT * FROM users WHERE id=%s", [id])
    user = cur.fetchone()
    cur.close()
    return render_template('update.html', user=user)

# ✅ DELETE user
@app.route('/delete/<int:id>', methods=['GET'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
