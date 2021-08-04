# model.py
from wtforms import SubmitField, BooleanField, IntegerField, StringField,PasswordField, validators, TextAreaField
from flask_wtf import Form
class AuditRegForm(Form):
    account_number =  StringField('Account count', [validators.DataRequired()])
    name_first = StringField('First Name', [validators.DataRequired()])
    name_last = StringField('Last Name', [validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired(), 
    validators.Email(), validators.Length(min=6, max=35)])
    employee_id = StringField('Unique Employee ID', [validators.DataRequired()])
    password = PasswordField('New Password', [
    validators.DataRequired(),
    validators.EqualTo('confirm', 
    message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')
class PatientRegForm(Form):
    account_number =  StringField('Account count', [validators.DataRequired()])
    name_first = StringField('First Name', [validators.DataRequired()])
    name_last = StringField('Last Name', [validators.DataRequired()])
    email = StringField('Email Address', [validators.DataRequired(), 
    validators.Email(), validators.Length(min=6, max=35)])
    phone = StringField('Phone Number', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    zip_code = StringField('Zipcode', [validators.DataRequired()])
    insurance = StringField('Insurance #', [validators.DataRequired()])
    password = PasswordField('New Password', [
    validators.DataRequired(),
    validators.EqualTo('confirm', 
    message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')
class LogForm(Form):
    user_name = StringField('Account Address', [validators.DataRequired()])
    contract_address = StringField('Contract Address (If Audit put 0)', [validators.DataRequired()])
    password = PasswordField('Your Password', [validators.DataRequired()])
    submit = SubmitField('Submit')
class PatientActions(Form):
    start_visit = StringField('Get an Appointment (Starts a new Medical Record)', [validators.DataRequired()])
    add_doctors = StringField('Add doctor audits', [validators.DataRequired()])
    remove_doctors = StringField('Remove doctor audits', [validators.DataRequired()])
    add_audits = StringField('Add other audits', [validators.DataRequired()])
    remove_audits = StringField('Remove other audits', [validators.DataRequired()])
    print_record = StringField('Print Medical Records', [validators.DataRequired()])
    delete_record = StringField('Delete Medical Records', [validators.DataRequired()])
class AuditActions(Form):
    contract_address =  StringField('Patient Contract Address (QR code in registration)', [validators.DataRequired()])
    print_record = StringField('Print Medical Records', [validators.DataRequired()])
    update_record_id = StringField('Update Medical Records', [validators.DataRequired()])
    update_record_rec = TextAreaField('New Record', [validators.DataRequired()],render_kw={"rows": 10, "cols": 11})
    query = StringField('Query Medical Records')
    copy_record = StringField('Copy Medical Records', [validators.DataRequired()])
    delete_record = StringField('Delete Medical Records', [validators.DataRequired()])



