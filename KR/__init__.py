from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
#init database
db=SQLAlchemy()


def create_app():
    #init app   
    app=Flask(__name__)
    app.debug=True
    app.secret_key='Super_Hero_Squad'
    #the folder to store images
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #connectdb
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///kidzbekidz.sqlite'
    #initialize db with flask app
    db.init_app(app)
    # error handler
    @app.errorhandler(404)
    def not_found(e):
       return render_template('404.html'),404
   # get bootstrap init
    boostrap = Bootstrap(app)
    #initialize the login manager
    #add login manager support
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(id):
        print(id)
        return User.query.get(id)

    from .views import mainbp
    app.register_blueprint(mainbp)

    

    return app




    

