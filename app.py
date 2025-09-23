from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# --- MySQL Configuration ---
# IMPORTANT: Update these details with your own MySQL server credentials.
# --- MySQL Configuration (Updated for Docker) ---
app.config['MYSQL_HOST'] = 'db' # <-- IMPORTANT: Use the service name from docker-compose.yml
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass' # Use a strong password here
app.config['MYSQL_DB'] = 'flask_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    """
    Fetches all users from the database and displays them on the homepage.
    """
    # Create a cursor
    cur = mysql.connection.cursor()
    
    # Execute a query to get all users
    cur.execute("SELECT * FROM users")
    
    # Fetch all the results
    users = cur.fetchall()
    
    # Close the cursor
    cur.close()
    
    # Render the template with the users data
    return render_template('index.html', users=users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    """
    Handles adding a new user to the database via a form.
    """
    if request.method == 'POST':
        # Get form data
        user_details = request.form
        name = user_details['name']
        email = user_details['email']
        
        # Create a cursor
        cur = mysql.connection.cursor()
        
        # Execute the insert query
        cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)", (name, email))
        
        # Commit the transaction
        mysql.connection.commit()
        
        # Close the cursor
        cur.close()
        
        # Redirect to the homepage to see the new user
        return redirect(url_for('index'))
        
    # If it's a GET request, just show the form
    return render_template('add.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
