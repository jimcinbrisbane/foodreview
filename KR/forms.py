from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField, PasswordField, IntegerField, validators, FileField, BooleanField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed



# register form
class RegestierForm(FlaskForm):

    #get user data
    user_name = StringField('Username*', validators=[InputRequired()])
    email = StringField('Email Address*', validators=[InputRequired()])
    password = PasswordField('Enter a Password*', validators = [InputRequired()])
    confirm = PasswordField('Confirm Password*', validators=[InputRequired()])
    submit = SubmitField("Submit")

# login form
class LoginForm(FlaskForm):
    user_name = StringField('Username', validators=[InputRequired()] )
    pass_word = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField("Submit")


# item form
class restaurantForm(FlaskForm):

    title = StringField('Fancy Title', validators=[InputRequired()],render_kw={"placeholder": "Get an eye tracking title"})
    description = StringField('Room Description', validators=[InputRequired()],render_kw={"placeholder": "What makes your properity stand out?"})
    image = FileField('Image (png,jpeg,jpg only)', validators=[FileRequired(),FileAllowed({ 'jpg', 'JPG', 'png', 'PNG','JPEG'}, 'Images only!')])
    address = StringField('Address', validators=[InputRequired()],render_kw={"placeholder": "2 George Street, Brisbane, 4000"})
    mobile = IntegerField('Contact Number', validators=[InputRequired()])
    submit= SubmitField("Create")

# Search form
class commentForm(FlaskForm):
    image = FileField('Image (png,jpeg,jpg only)', validators=[FileRequired(),FileAllowed({ 'jpg', 'JPG', 'png', 'PNG','JPEG'}, 'Images only!')])
    comment = StringField('Room Description', validators=[InputRequired()],render_kw={"placeholder": "What makes your properity stand out?"})
    rate = StringField('Rating', validators=[InputRequired()],render_kw={"placeholder": "0-5"})
    submit = SubmitField('Search')