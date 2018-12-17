from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, FloatField, SelectMultipleField,widgets,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    id = StringField('ID',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class PatientSearchForm(FlaskForm):
    choices = [('Name','Name'),
    ('Age','Age'),
    ('Phone','Phone'),
    ('TCKN','TCKN'),
    ('Insurance','Insurance'),
    ('cur_complaint','Current Complaint'),
    ]
    select = SelectField('Filter Patients:',choices=choices)
    search = StringField('')
    submit = SubmitField('Filter')

class G_PharmacySearchForm(FlaskForm):
    c = [('name','Name'),
    ('location','Location'),
    ]
    select = RadioField('Search for Pharmacies' , choices = c)
    search = StringField('')
    submit = SubmitField('Search') 

class inventory_change_form(FlaskForm):
    sold = SubmitField('Sold a Drug')
    bought = SubmitField('Bought a Drug')
    request_id = HiddenField('Request ID')

class G_WarehouseSearchForm(FlaskForm):
    c = [('name','Name'),
    ('region','Region'),
    ]
    select = RadioField('Search for Pharmaceutical Warehouses' , choices = c)
    search = StringField('')
    submit = SubmitField('Search')

class PharmacyPersonelForm(FlaskForm):
    delete = SubmitField('Delete')
    edit = SubmitField('Edit')
    request_id = HiddenField('Request ID')

class PharPersonelAdd(FlaskForm):
	request_id = HiddenField('Request ID')
	tckn = IntegerField('')
	name = StringField('')
	tel_num =IntegerField('')
	school = StringField('')
	graduation_year = IntegerField('')
	years_worked = IntegerField('')
	submit = SubmitField('Save Changes')

class PharPersonelEditForm(FlaskForm):
	tel = IntegerField('123')
	years = IntegerField('')
	submit = SubmitField('Save Changes')

class HospitalSearchForm(FlaskForm):
    choices=[('HOSPITAL_NAME','Hospital Name'),
    ('LOCATION', 'Location'),
    ('ADMINISTRATOR','Administrator'),
    ('TELEPHONE_NUMBER','Phone Number')]
    selection=SelectField('Hospital Filter:',choices=choices)
    search=StringField('Keyword')
    publicHos=RadioField('Public Hospital? ',choices=[('True','Public'),('False','Private'),('*','Both')],validators=[DataRequired()])
    submit=SubmitField('Search')

class HospitalAddForm(FlaskForm):
    hospital_name=StringField('Hospital Name',validators=[DataRequired()])
    is_public=RadioField('Public Hospital?',choices=[('True','Public'),('False','Private')],validators=[DataRequired()])
    location=StringField('Location')
    administrator=StringField('Administrator Name')
    telephone_number=StringField('Phone Number, 11 digit required')#,validators=[Length(min=11,max=11)])
    ambulance_count= StringField('Number of ambulances')
    submit=SubmitField('Insert')

class HospitalDeleteForm(FlaskForm):
    delete=SubmitField('Delete')

class PersonnelSearchForm(FlaskForm):
    choices=[('WORKER_NAME','Personnel Name'),
    ('JOB_TITLE', 'Job Title'),
    ('JOB_EXPERIENCE','Job Experience'),
    ('WORK_DAYS','# of Days Worked'),
    ('PHONE_NUM','Contact Number'),
    ('WORK_DAYS','# of Days Worked'),
    ('WORKING_FIELD', 'Work Field')]
    selection=SelectField('Personnel Filter:', choices=choices)
    search=StringField('Keyword')
    submit=SubmitField('Search')

class PersonnelAddForm(FlaskForm):
    worker_name=StringField('Personnel Name',validators=[DataRequired()])
    job_title=StringField('Job Title',validators=[DataRequired()])
    job_experience=StringField('Job Experience')
    work_days=StringField('Work Days')
    phone_num=StringField('Contact Number')
    working_field=StringField('Work Field')
    hospital_worked=StringField('Hospital Id')
    tckn=StringField('Tckn')
    submit=SubmitField('Insert')

class PersonnelDeleteForm(FlaskForm):
    delete=SubmitField('Delete')
