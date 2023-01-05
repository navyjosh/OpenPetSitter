from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, HiddenField, FieldList, IntegerField, TimeField, TextAreaField

from wtforms.validators import DataRequired, Length
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    pettype = SelectField('Pet Type', validators=[DataRequired()], choices=['dog', 'cat'])    
    submit = SubmitField('Submit')

class DeletePetForm(FlaskForm):    
    submit = SubmitField('Delete Pet')

class AddNewJobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 30, message='Title must be between 1 and 30 characters of length.')])
    description = TextAreaField('Description', validators=[Length(max=5000, message='Maximum Length of 5000 characters')])
    pets = FieldList(IntegerField('Pets'))
    date = DateField('Date', validators=[DataRequired()])
    scheduled_time = TimeField('Time', validators=[DataRequired()])
    
