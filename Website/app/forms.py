from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class PlaceBetForm(FlaskForm):
    bet_id = HiddenField('Bet ID')
    team1 = HiddenField('Team 1')
    team2 = HiddenField('Team 2')
    line1 = StringField('Line 1')
    line2 = StringField('Line 2')
    odds1 = StringField('Odds 1')
    odds2 = StringField('Odds 1')
    bet = IntegerField('Bet Amount', validators=[DataRequired()])
    team = SelectField('Team', validators=[DataRequired()])#, choices = [('left', 'Left'), ('right', 'Right')], validators=[DataRequired()])
    placeBet = SubmitField('Place Bet')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # Check for duplicates
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
