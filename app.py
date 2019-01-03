from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'beratbozkurt1999@gmail.com'
app.config['MAIL_PASSWORD'] = '[password]'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
posta = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/bozkurt/Desktop/forgot-password/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
app.secret_key = 'some_secret'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    mail = db.Column(db.String(120))
    password = db.Column(db.String(80))
    hashCode = db.Column(db.String(120))

@app.route('/',methods=["POST","GET"])
def index():
    if request.method=="POST":
        mail = request.form['mail']
        check = User.query.filter_by(mail=mail).first()

        if check:
            def get_random_string(length=24,allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
                return ''.join(random.choice(allowed_chars) for i in range(length))
            hashCode = get_random_string()
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'berat@github.com', recipients = [mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hashCode
            posta.send(msg)
            return '''
                <form action="/" method="post">
                    <small>enter the email address of the account you forgot your password</small> <br>
                    <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return '''
            <form action="/" method="post">
                <small>enter the email address of the account you forgot your password</small> <br>
                <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
                <input type="submit" value="Submit">
            </form>
        '''
    
@app.route("/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = User.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('yanlış girdin')
                return '''
                    <form method="post">
                        <small>enter your new password</small> <br>
                        <input type="password" name="passw" id="passw" placeholder="password"> <br>
                        <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                        <input type="submit" value="Submit">
                    </form>
                '''
        else:
            return '''
                <form method="post">
                    <small>enter your new password</small> <br>
                    <input type="password" name="passw" id="passw" placeholder="password"> <br>
                    <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return render_template('/')

@app.route('/createUser')
def createUser():
    newUser = User(username='berat',mail='beratbozkurt1999@gmail.com',password='123456')
    db.session.add(newUser)
    db.session.commit()
    return "Created user"
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
