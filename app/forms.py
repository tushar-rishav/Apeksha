from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField
import wtforms.validators as validators
from models import db, User


class SigninForm(Form):
    Email = TextField("Email",  [validators.Required(
        "Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField(
        'Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email=self.Email.data).first()
        print vars(user)
        if user and user.check_password(self.password.data):
            return True
        else:
            self.Email.errors.append("Invalid e-mail or password")
            return False
