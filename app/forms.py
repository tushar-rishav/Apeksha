from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField
import wtforms.validators as validators
from models import db, User


class SigninForm(Form):
    reg = TextField("Text",  [validators.Required(
        "Please enter your Registration ID")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.get(self.reg.data)
        if user:
            return True
        else:
            self.reg.errors.append("Invalid Registration")
            return False
