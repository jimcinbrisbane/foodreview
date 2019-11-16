from flask import Blueprint,render_template, redirect, url_for, request, flash
from flask_login import LoginManager,login_user,current_user,logout_user, login_required
from .models import *
from .forms import *
import datetime
from sqlalchemy import or_
from . import db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from . import create_app

mainbp = Blueprint('main',__name__)
############################################
# homepage route
@mainbp.route('/')
def index():
    tag_line='Food For Kidz'
    restaurant = Restaurant.query.order_by(Restaurant.id.desc()).all()
    return render_template('homepage.html', restaurant = restaurant, tag_line=tag_line)

############################################
#admin form route
@mainbp.route('/supersecrectadminpage')
def post():
    if current_user.is_anonymous:
        return flash("ERROR: 418, coffee is not allowed to brew in a teapot")
    else:
        print(current_user.name)
    tag_line="This is us"
    aform = restaurantForm()
    return render_template('index_reuse.html', tag_line=tag_line ,aform=aform)



@mainbp.route('/remove/<id>')
def commentdelete(id):
    #Delete Details
    try:
     Comment.query.filter_by(id=id,user_name=current_user.name).delete()
     db.session.commit()
     flash("comment deleteted")
    except:
        flash("you're not the user, admin had been notified")    
        print("illegal action of comment deletion has been detected, the user name is :  ", current_user.name)
    return redirect('/')

#############################################
#         D A T A B A S E - P A T H         #                
#############################################

def check_upload_file(form):
          # get file data from form
          fp = form.image.data
          filename= fp.filename
          # get the current path of the module file... store file relative to this path
          BASE_PATH= os.path.dirname(__file__)
          #uploadfilelocation – directory of this file/static/image
          upload_path= os.path.join(BASE_PATH,'static/img', secure_filename(filename))
          # store relative path in DB as image location in HTML is relative
          db_upload_path= '/static/img/'+ secure_filename(filename)
          # save the file and return the dbupload path
          fp.save(upload_path)
          return db_upload_path

#############################################
#           C R E A T E - I T E M           #                
#############################################
#fetch item form and insert it to database

@mainbp.route('/create', methods = ['GET','POST'])
def create_item():
  aform = restaurantForm()
  if aform.validate_on_submit():
    db_file_path=check_upload_file(aform)
    print(db_file_path)
    # a simple function: doesnot handle errors in file types and file not being uploaded
    
    # if the form was successfully submitted, access the values in the form data
    
    #insert restraunt into database
    newr = Restaurant(id = datetime.datetime.now().isoformat(),#as you can see I used datetime as Primary Key
                title=aform.title.data, 
                description=aform.description.data,
                image= db_file_path,
                address=aform.address.data,
                mobile = aform.mobile.data,
                admin_id = current_user.name,
                )

    #add the object to the db session
    db.session.add(newr)
    
    #commit to the database
    db.session.commit()
    flash('Successfully created new restraunt', 'success')
    print('Successfully created new restraunt', 'success')
    return redirect(url_for('main.index'))


#############################################
#           U P D A T E - I T E M           #                
#############################################
#fetch item form and insert it to database

@mainbp.route('/update', methods = ['GET','POST'])
def update_item():
  id =  request.args.get('id', None)
  aform = restaurantForm()
  if aform.validate_on_submit():
    db_file_path=check_upload_file(aform)
    print(db_file_path)
    # a simple function: doesnot handle errors in file types and file not being uploaded
    
    # if the form was successfully submitted, access the values in the form data
    
    #insert item into database
    #add the object to the db session
    
    
    data = {Restaurant.title:aform.title.data, 
                Restaurant.description:aform.description.data,
                Restaurant.image: db_file_path,
                Restaurant.address:aform.address.data,
                Restaurant.mobile : aform.mobile.data}
    db.session.query(Restaurant).filter_by(id=id).update(data)
    
    #commit to the database
    db.session.commit()
    flash('Successfully created new travel destination', 'success')
    print('Successfully created new room info', 'success')
    return redirect('/landlordlist')




#############################################
#           ADD COMMENT                      #
#############################################
@mainbp.route('/write_comment/<id>')
def comment():
    commentF = commentForm()
    id = id
    return render_template('comment.html',commentF = commentF, id=id)
@mainbp.route('/post_comment/<id>', methods = ['GET','POST'])
def new_comment(id):
    commentF = commentForm()
    if commentF.validate_on_submit():
        img=check_upload_file(comment)
        newcomment=Comment(date=datetime.datetime.now(),
            restaurant_id=id,
            user_id=current_user.name,
            comment= comment.comment.data,
            rate= comment.rate.data,
            image = img

            )
        print(datetime.datetime.now(),id,current_user.id)
        db.session.add(newcomment)
        db.session.commit()
        flash('comment had post')
        print('comment', comment)
    return redirect(url_for('main.index'), commentF=commentF)
    
#############################################
#           R E G I S T R A T I O N         #                
#############################################

@mainbp.route('/reg')
def reg():
    registerform = RegestierForm()
    return render_template('register.html',registerform = registerform)

@mainbp.route('/register', methods = ['POST'])
def register():
    registerform = RegestierForm()
    if registerform.validate_on_submit():
        print('Register Form Submitted')
        #get username,password and email from the form
        username = registerform.user_name.data
        pass_word = registerform.password.data
        email = registerform.email.data
        id=datetime.datetime.now().isoformat()


        #create password hash, salted for security
        hashWord = generate_password_hash(pass_word+username)

        #create a new user account
        try: 
            newUser = User(name=username, emailid=email,id=id, password_hash=hashWord)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('main.login'))
        except:
            flash("Looks like the user name had been used, try another one!" )
            print("username duplcated")
            return redirect(url_for('main.reg'))

#############################################
#                 L O G I N                 #                
#############################################
#initialize login management
login_manager = LoginManager()

#create name of the login function that lets users login
login_manager.login_view ='auth.login'

#create a user load in function that goes by userID
@login_manager.user_loader
def load_user(user_id):
    return User.get(u1)

#routing for login
@mainbp.route('/login')
def login():
    login_form = LoginForm()
    return render_template('login.html', login_form = login_form)

@mainbp.route('/log', methods = ['GET','POST'])
def log():
    login_form=LoginForm()
    error=None
    if(login_form.validate_on_submit()):
        username = login_form.user_name.data
        pass_word = login_form.pass_word.data
        u1 = User.query.filter_by(name = username).first()

        if u1 is None:
            error='Incorrect Username'
            flash(error)
            print(error)
        elif not check_password_hash(u1.password_hash,pass_word+username):
            error='Incorrect Password'
            flash(error)
            print(error)
        if error is None:
            print(u1)
            login_user(u1)
            print(u1)
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('main.login'))
            print(error)
           #create a login failed page

   # return redirect(url_for('main.index'))

@mainbp.route("/logout")
def logout():
    if current_user.is_anonymous:
        return redirect('/login')
    else:
        print(current_user)

    logout_user()
    return redirect(url_for('main.index'))