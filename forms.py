from wtforms import Form, TextField, TextAreaField, PasswordField, HiddenField, validators, IntegerField, SelectField

class LoginForm(Form):
    email = TextField("Email", [validators.Required(), validators.Email()])
    password = PasswordField("Password", [validators.Required()])

class RegisterForm(Form):
    email = TextField("Email", [validators.Required(), validators.Email()])
    first_name = TextField("First Name", [validators.Required()])
    last_name = TextField("Last Name", [validators.Required()])
    password = PasswordField("Password", [validators.Required()])

class NewTripForm(Form):
    title = TextField("title", [validators.Required()])
    destination = TextField("destination", [validators.Required()])
    start_date = TextField("start_date", [validators.Required()])
    end_date = TextField("end_date", [validators.Required()])
    activity = SelectField("activity", coerce=int, [validators.Required()])