from wtforms import Form, StringField, PasswordField

class LoginForm(Form):
    username = StringField('Username')
    password = StringField('Password')
    redirect = StringField('Redirect')