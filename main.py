from flask import Flask, render_template, Response,redirect,request
from camera import VideoCamera
import os
import sys
app = Flask(__name__)

CART=[]

@app.route('/checkOut', methods=['POST', 'GET'])
def checkOut():
    return render_template('checkout.html')

@app.route('/tryon/<file_path>',methods = ['POST', 'GET'])   
def tryon(file_path):
    file_path = file_path.replace(',','/')
    os.system('python tryOn.py ' + file_path)
    return redirect('http://127.0.0.1:5000/',code=302, Response=None)
    #return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
    
@app.route('/login', methods = ['GET',"POST"])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM people WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            global Id
            session['Id'] = account['Id']
              
            Id = session['Id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password! Please login with correct credentials')
            return redirect(url_for('login'))
    # Show the login form with message (if any)

    return render_template('login.html', msg=msg)

@app.route('/register',methods= ['GET',"POST"])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'age' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        age = request.form['age']
        
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,10}$"
        pattern = re.compile(reg)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Check if account exists using MySQL)
        cursor.execute('SELECT * FROM people WHERE Username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.search(pattern,password):
            msg = 'Password should contain atleast one number, one lower case character, one uppercase character,one special symbol and must be between 6 to 10 characters long'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute('INSERT INTO people VALUES (NULL, %s, %s, %s, %s)', (username, password, email, age))
            mysql.connection.commit()
            flash('You have successfully registered! Please proceed for login!')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return msg
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/tryall',methods = ['POST', 'GET'])
def tryall():
    print("YESSS")
    if request.method == 'POST':
        cart = request.form['mydata'].replace(',', '/')
        print("tryall cart type= ", type(cart))
        print("tryall cart= ", cart)
        os.system('python test.py ' + cart)
        return redirect('http://127.0.0.1:5000/',code=302, Response=None)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        #print("frame= ", frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/cart/<file_path>",methods = ['POST', 'GET'])
def cart(file_path):
    global CART
    file_path = file_path.replace(',','/')
    print("ADDED", file_path)
    CART.append(file_path)
    return render_template("checkout.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
  