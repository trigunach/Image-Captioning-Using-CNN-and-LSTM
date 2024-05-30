import pandas as pd
from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm  
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, session
from forms import RegistrationForm, LoginForm
import mysql.connector
import os
from PIL import Image
import generate  
import os
os.environ['TF_KERAS'] = '1'
#import onnx
def Xception(image_path):
    caption = generate.runModel(image_path)
    return caption



APP_ROOT=os.path.dirname(os.path.abspath(__file__))
app=Flask(__name__)
#app.secret_key="from infinity to beyond"
app.config['UPLOAD_FOLDER']=os.path.join(APP_ROOT, 'static/image/')
app.config['SECRET_KEY']='b0b4fbefdc48be27a6123605f02b6b86'
db = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database="image_caption")
cur = db.cursor()


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

@app.route("/ourproject")
def ourproject():
    return render_template('ourproject.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email,password)
        if email == 'admin@test.com' and password == "admin":
            session['loggedin'] = True
            session['admin'] = True
            flash("You have been logged in as the Administrator!", 'success')
            return redirect(url_for('ourproject'))
        else:
            # database logic here
            # query the database to retrieve user information
            sql = "select * from register where email = '"+email+"' and password = '"+password+"' and status = 'accepted' "
            cur.execute(sql)
            data = cur.fetchall()
            db.commit()
            print(data)
            print("==================================")
            # Check if the user exists and the password is correct
            if len(data)>0:
                flash(f"Welcome {email}! You have been logged in.", 'success')
                return redirect(url_for('ourproject'))
            else:
                flash(f"No account with the email id {email} exists. Please register now.", 'info')
                return redirect(url_for('register'))

    return render_template('login.html', form=form)





@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/users')
def users():
    
    #Database connections
    db=mysql.connector.connect(host="localhost", port=3306, user="root", password="", db="image_caption")
    #Table as a data frame
    register=pd.read_sql_query('select * from {}'.format('register'), db)
    #Remove the password column
    register.drop(['password'], axis=1, inplace=True)

    return render_template('users.html', column_names=register.columns.values, row_data=list(register.values.tolist()))

@app.route("/users2/<int:id>", methods=['GET','POST'])
def users2(id=0):
    user_id=str(id)
    sql = "update register set status = 'accepted' where id = '%s'"%(user_id)
    cur.execute(sql)
    db.commit()
    return redirect(url_for('users'))

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    #Database connection

    #Table as a data frame
    register=pd.read_sql_query('select * from {}'.format('register'), db)

    if form.validate_on_submit():
        email=form.email.data
        username = form.username.data
        password = form.password.data
        all_emails=register['email']
        if email in list(all_emails):
            flash('Account already exists with this Email Id! Please Log In.','warning')
            db.close()
            return redirect(url_for('login'))
        else:
            
            cur = db.cursor()
            sql = "INSERT INTO `register` (`username`,`email`,`password`) VALUES (%s, %s, %s)"
            val= (username,email,password)
            cur.execute(sql, val)
            db.commit()

            flash(f'Account Created for {form.username.data} Sucessfully! Please wait for the admin to verify your account.','success')

            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/upload", methods=["POST"])
def upload():
    target=os.path.join(APP_ROOT, 'static/image/')

    if not os.path.isdir(target):
        os.mkdir(target)
    file=request.files["myimage"]
    filename=file.filename
    if filename=="":
        flash('No File Selected','danger')
        return redirect(url_for('ourproject'))

    destination="/".join([target, filename])
    #Extension check
    ext = os.path.splitext(destination)[1]
    if (ext==".jpg") or (ext==".png"):
        pass
    else:
        flash("Invalid Extenstions! Please select a .jpg or a .png file only.", category="danger")
        return redirect(url_for('ourproject'))

    if not os.path.isfile(destination):
        file.save(destination)

    result=Xception(destination)
    return render_template("upload.html", img_name=filename, cap=result)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__=="__main__":
    app.run(debug=True)
