from flask_wtf import FlaskForm
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField
import wtforms.validators as validators
from models import db, User


class SigninForm(FlaskForm):
    reg = TextField("Text",  [validators.Required(
        "Please enter your Registration ID")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate_form(self):
        if not self.validate():
            return False

        user = User.query.get(self.reg.data)
        print user
        if user:
            return True
        else:
            self.reg.errors.append("Invalid Registration")
            return False
