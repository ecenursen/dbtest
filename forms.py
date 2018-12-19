from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, FloatField, SelectMultipleField,widgets,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
class InsertForm(FlaskForm):
    input = StringField('Scripts')
    submit = SubmitField('Submit')
class LoginForm(FlaskForm):
    id = StringField('ID',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
class PatientForm(FlaskForm):
    choices = [('insert','Insert'),('update','Update')]
    select = RadioField('Choose an operation',choices=choices,default='insert')
    name=StringField('Name')
    age=StringField('Age')
    sexChoices = [('male','Male'),('female','Female')]
    sex=SelectField('Sex',choices=sexChoices)
    tckn=StringField('TCKN')
    phone = StringField('Phone')
    complaint = StringField('Current Complaint')
    insurance = StringField('Insurance')
    submit = SubmitField('Submit')
    search = SubmitField('Search')
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

class delete_pharmacy_form(FlaskForm):
    submit = SubmitField('DELETE PHARMACY')

class create_pharmacy_form(FlaskForm):
    submit = SubmitField('CREATE NEW PHARMACY')

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
class Drugs_Form(FlaskForm):
    choices = [('insert','Insert'),('update','Update')]
    select = RadioField('Choose an operation',choices=choices,default='insert')
    name=StringField('Name')
    company=StringField('Company')
    size=StringField('Size')
    shelf=StringField('Shelf life')
    typ = StringField('Type')
    price = StringField('Price')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

class DrugCompanies_Form(FlaskForm):
    choices = [('insert','Insert'),('update','Update')]
    select = RadioField('Choose an operation',choices=choices,default='insert')
    name=StringField('Name')
    year=StringField('Foundation Year')
    founder=StringField('Founder')
    country=StringField('Country')
    workers=StringField('Worker Number')
    factories=StringField('Factory Number')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

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

class ShiftAddForm(FlaskForm):
    personnel_id=StringField('Personnel Id ',validators=[DataRequired()])
    shift_begin_date=StringField('Shift Begin Date YYYY-MM-DD')
    shift_repeat_interval=StringField('Shift Repeat Interval')
    shift_hours=StringField('Shift length -hours-')
    dayshift=RadioField('Shift in daytime?',choices=[('True','Daytime'),('False','Nighttime')],validators=[DataRequired()])
    emergency_area_assigned=StringField('Emergency area(Green, Yellow, Red)')
    submit=SubmitField('Insert')
