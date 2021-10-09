from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateTimeField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from chillin.models import User


class RegisterForm(FlaskForm):
    name = StringField(label="Name: ", validators=[Length(min=1, max=30, message="Name must be between 1 to 30 characters long."), DataRequired()])
    email_address = StringField(label="Email Address: ", validators=[Email(message="Email address is invalid."), DataRequired()])
    password1 = PasswordField(label="Password: ", validators=[Length(min=6, message="Password must be at least 6 characters long."), DataRequired()])
    password2 = PasswordField(label="Confirm Password: ", validators=[EqualTo(fieldname="password1", message="Passwords do not match."), DataRequired()])
    submit = SubmitField(label="Create Account")

    # def validate_username(self, username_to_check):
    #     user = User.query.filter_by(username=username_to_check.data).first()
    #     if user:
    #         raise ValidationError("Username already exists! Please try a different username")

    def validate_email_address(self, email_address_to_check):
        user = User.query.filter_by(email_address=email_address_to_check.data).first()
        if user:
            raise ValidationError("Email already exists! Please try a different email")


class LoginForm(FlaskForm):
    email = StringField(label="Email: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")

class CreateEventForm(FlaskForm):
    title = StringField(label="Title: ", validators=[DataRequired()])
    description = StringField(label="Description: ", validators=[DataRequired()])
    location = StringField(label="Location: ", validators=[DataRequired()])
    time = DateTimeField(label="Time: ", format='%Y-%m-%d %H:%M:%S')
    group_size = IntegerField(label="Group Size: ", validators=[DataRequired()])
    mode = SelectField(label="Mode: ", validators=[DataRequired()], choices=[("inperson", "In Person"), ("virtual", "Virtual") ])
    submit = SubmitField(label="Host Event")

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item")


class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item")
