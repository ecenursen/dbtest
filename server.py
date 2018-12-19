from flask import Flask, render_template, redirect, url_for, flash, request, session,abort
from forms import *
import datetime
import os
import psycopg2 as db
from dbinit import initialize, drop_table
from classes.hospital import *
from classes.hospital_personnel import *
from classes.shift_data import *
app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW'

'''
connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
cursor = connection.cursor()
for statement in INIT_STATEMENTS:
	cursor.execute(statement)
connection.commit()
cursor.close()
'''
DEBUG = False
# LIVE ICIN
#DEBUG=True
if(DEBUG == False):
	url = os.getenv("DATABASE_URL")
else:
	# DENEME ICIN
	url = "dbname='postgres' user='postgres' host='localhost' password='hastayimpw'"
	initialize(url)
	# drop_table(url)

@app.route("/insert", methods=['GET', 'POST'])
def insert_page():
    form = InsertForm()
    if form.validate_on_submit():
        commands = form.input.data
        commands = commands.split("/")
        connection = db.connect(url)
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
            connection.commit()
    return render_template("insert.html",form = form)

@app.route("/")
@app.route("/home")
def home_page():
	logged = True if session.get('logged_in') == True else False
	return render_template('home_page.html', logged=logged)


@app.route("/about")
def about_page():
	return render_template('about_page.html')


@app.route("/patients_page", methods=['GET', 'POST'])
def patients_page():
    form = PatientForm()
    patients = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = "SELECT PATIENTS.NAME,AGE,SEX,TCKN,PHONE,CUR_COMPLAINT,INSURANCE.INSURANCE_NAME,PATIENTS.ID FROM PATIENTS,INSURANCE WHERE PATIENTS.INSURANCE = INSURANCE.INSURANCE_ID ORDER BY PATIENTS.NAME ASC"
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        patients.append(row)
    if form.validate_on_submit():
        name = form.name.data
        age = form.age.data
        sex = form.sex.data
        tckn = form.tckn.data
        phone = form.phone.data
        complaint = form.complaint.data
        insurance = form.insurance.data
        if form.validate_on_submit():
            
            if form.search.data == True:
                return redirect(url_for("patients_search_page"))
            elif form.submit.data == True:
                if(name == "" or age == "" or tckn == "" or phone == "" or complaint == "" or insurance ==""):
                    flash("Fill in the boxes")
                    return redirect(url_for("patients_page"))
                else:
                    insurance = "SELECT * FROM INSURANCE WHERE INSURANCE_NAME = \'{}\'".format(insurance)
                    cursor.execute(insurance)
                    connection.commit()
                    result = cursor.fetchone()
                    print(insurance)
                    print(result)
                    if not result == None and len(result) > 0:
                        insurance_id = result[0]
                        sex = True if sex == "Male" else False
                        insert = "INSERT INTO PATIENTS(NAME,AGE,SEX,TCKN,PHONE,CUR_COMPLAINT,INSURANCE) VALUES(\'{}\',{},{},\'{}\',\'{}\',\'{}\',{});".format(
                            name,age,sex,tckn,phone,complaint,insurance_id
                            )
                        cursor.execute(insert)
                        connection.commit()
                        return redirect(url_for("patients_page"))
                    else:
                        flash("Insurance company is unknown.",'warning')
                        return redirect(url_for("patients_page"))
                return redirect(url_for("patients_page"))
    cursor.close()
    return render_template('patients_page.html',Patients=patients,form=form)

@app.route("/patients_search_page", methods=['GET', 'POST'])
def patients_search_page():
    patients = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = "SELECT PATIENTS.NAME,AGE,SEX,TCKN,PHONE,CUR_COMPLAINT,INSURANCE.INSURANCE_NAME FROM PATIENTS,INSURANCE WHERE PATIENTS.INSURANCE = INSURANCE.INSURANCE_ID ORDER BY PATIENTS.NAME ASC"
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        patients.append(row)
    cursor.close()
    form = PatientSearchForm()
    if form.validate_on_submit():
        attr = form.select.data
        key = form.search.data
        result = []
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = "SELECT PATIENTS.NAME,AGE,SEX,TCKN,PHONE,CUR_COMPLAINT,INSURANCE.INSURANCE_NAME FROM PATIENTS,INSURANCE WHERE PATIENTS.INSURANCE = INSURANCE.INSURANCE_ID AND CAST({} AS TEXT) ILIKE {} ORDER BY {} ASC".format(
            attr, "\'%" + key + "%\'", attr)
        #statement = """SELECT * FROM PATIENTS WHERE CAST({} AS TEXT) ILIKE {} ORDER BY {} ASC""".format(attr,"\'%" + key + "%\'", attr)
        cursor.execute(statement)
        connection.commit()
        for row in cursor:
            result.append(row)
        cursor.close()
        return render_template('patients_search_page.html', Patients=result, form=form,filtered=True)
    return render_template('patients_search_page.html', Patients=patients, form=form,filtered=False)

@app.route("/drugs",methods=['GET', 'POST'])
def drugs_page():
    drugs = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement= "SELECT DRUGS.name,DRUG_COMPANIES.name,size,shelf_life,price,DRUG_TYPE.name FROM DRUGS,DRUG_COMPANIES,DRUG_TYPE WHERE company_id=DRUG_COMPANIES.id AND type=DRUG_TYPE.id ORDER BY drugs.NAME ASC"
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        drugs.append(row)
    cursor.close()

    form = Drugs_Form()
    if form.validate_on_submit():
        connection = db.connect(url)
        cursor = connection.cursor()
        select = form.select.data
        name=form.name.data
        company=form.company.data
        size=form.size.data
        shelf=form.shelf.data
        typ =form.typ.data
        price = form.price.data
        if(form.delete.data == True):
            statement= "select * from drugs where name = \'{}\'".format(name)
            cursor.execute(statement)
            connection.commit()
            result = cursor.fetchone()
            if result == None:
                flash("The drug does not exists. Cannot be deleted",'warning')
                return redirect(url_for("drugs_page"))
            else:
                statement = "DELETE FROM DRUGS WHERE NAME = \'{}\'".format(name)
                cursor.execute(statement)
                connection.commit()
                return redirect(url_for("drugs_page"))
        if(form.submit.data == True):
            if select == "insert":
                if(name=="" or company == "" or shelf =="" or size =="" or typ =="" or price == ""):
                    flash("Please fill in all the boxes.",'warning')
                    return redirect(url_for('drug_companies_page'))

                statement="SELECT * FROM DRUGS WHERE NAME= \'{}\'".format(name)
                print(statement)
                cursor.execute(statement)
                connection.commit()
                result = cursor.fetchone()
                print(result)
                if not result == None and len(result)>0:
                    flash("The drug already exists, cannot insert.",'warning')
                    cursor.close()
                    return redirect(url_for("drugs_page"))
                else:
                    statement = "SELECT * from drug_companies where NAME = \'{}\'".format(company)
                    cursor.execute(statement)
                    connection.commit()
                    result = cursor.fetchone()
                    if not result == None and len(result) > 0:
                        company_id = result[0]
                        statement = "SELECT * FROM DRUG_TYPE WHERE NAME = \'{}\'".format(typ)
                        cursor.execute(statement)
                        connection.commit()
                        result = cursor.fetchone()
                        if not result == None and len(result)>0:
                            drug_type = result[0]
                            statement = "INSERT INTO public.DRUGS(name,company_id,size,shelf_life,price,type) VALUES (\'{}\',{},{},{},\'{}\',{});".format(name,company_id,size,shelf,price,typ)
                            print(statement)
                            cursor.execute(statement)
                            connection.commit()
                            return redirect(url_for("drugs_page"))
                        else:
                            flash("Drug type is unknown. Please check again",'warning')
                            return redirect(url_for("drugs_page"))
                    else:
                        flash("The Drug Company does not exists.",'warning')          
                        return redirect(url_for("drugs_page"))
            elif select == 'update':
                statement="SELECT * FROM DRUGS WHERE NAME= \'{}\'".format(name)
                cursor.execute(statement)
                connection.commit()
                result = cursor.fetchone()
                if not result == None and len(result)==0:
                    print("The drug does not exists, cannot update.")
                    cursor.close()
                    return redirect(url_for("drugs_page"))
                else:
                    drug_id = result[0]
                    statement = "SELECT * from drug_companies where NAME = \'{}\'".format(company)
                    cursor.execute(statement)
                    connection.commit()
                    result = cursor.fetchone()
                    if not result == None and len(result) > 0:
                        company_id = result[0]
                        statement = "SELECT * FROM DRUG_TYPE WHERE TYPE = \'{}\'".format(typ)
                        cursor.execute(statement)
                        connection.commit()
                        result = cursor.fetchone()
                        if not result == None and len(result)>0:
                            drug_type = result[0]
                            statement = "UPDATE public.drugs SET name=\'{}\',company_id={},size={},shelf_life={},price=\'{}\',type={} WHERE id = {};".format(name,company_id,size,shelf,price,typ,drug_id)
                            cursor.execute(statement)
                            connection.commit()
                            return redirect(url_for("drugs_page"))
                        else:
                            flash("Drug type is unknown.",'warning')
                            return redirect(url_for("drugs_page"))
                    else:
                        flash("The company does not exists.",'warning')
            return redirect(url_for("drugs_page"))
    return render_template('drugs_page.html', Drugs=drugs,form=form)


@app.route("/drug_companies",methods=['GET', 'POST'])
def drug_companies_page():
    companies = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT * FROM DRUG_COMPANIES"""""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        companies.append(row)
    cursor.close()

    form = DrugCompanies_Form()
    if form.validate_on_submit():
        connection = db.connect(url)
        cursor = connection.cursor()
        if(form.delete.data == True):
            name = form.name.data
            if name=="":
                flash("Please write the name of the company to be deleted...",'info')
                return redirect(url_for('drug_companies_page'))
            else:
                statement = "DELETE FROM DRUG_COMPANIES WHERE NAME = \'{}\'".format(name)
                cursor.execute(statement)
                connection.commit()
                return redirect(url_for('drug_companies_page'))
        if(form.submit.data == True):
            select = form.select.data
            name=form.name.data
            year=form.year.data
            founder=form.founder.data
            country=form.country.data
            workers =form.workers.data
            factories = form.factories.data
            if(name=="" or year =="" or founder =="" or country == "" or factories ==""):
                flash("Please fill in all the boxes.",'warning')
                return redirect(url_for('drug_companies_page'))
            if select == "insert":
                checkIfExist = "SELECT * FROM PUBLIC.DRUG_COMPANIES WHERE NAME = \'{}\'".format(name)
                print(checkIfExist)
                cursor.execute(checkIfExist)
                connection.commit()
                result = cursor.fetchone()
                print(result)
                if not result == None and len(result)>0:
                    print("Company already exists. Cannot insert")
                else:
                    statement = "INSERT INTO PUBLIC.DRUG_COMPANIES(NAME,FOUNDATION_YEAR,FOUNDER,COUNTRY,WORKER_NUM,FACTORY_NUM) VALUES(\'{}\',{},\'{}\',\'{}\',{},{});".format(
                        name,year,founder,country,workers,factories
                    )
                    print(statement)
                    cursor.execute(statement)
                    connection.commit()
                    cursor.close()
                return redirect(url_for('drug_companies_page'))
            elif select == "update":
                statement = "SELECT * FROM DRUG_COMPANIES WHERE NAME = \'{}\'".format(name)
                cursor.execute(statement)
                connection.commit()
                result = cursor.fetchone()
                if not result == None and len(result)>0:
                    statement = "update public.drug_companies SET name=\'{}\',foundation_year={},FOUNDER=\'{}\',COUNTRY=\'{}\',WORKER_NUM={},FACTORY_NUM={}".format(
                    name,year,founder,country,workers,factories 
                    )
                    cursor.execute(statement)
                    connection.commit()
                    cursor.close()
                return redirect(url_for('drug_companies_page'))

    return render_template('drug_companies_page.html', DrugCompanies=companies,form=form)



@app.route("/pharmacy", methods=['GET', 'POST'])
def pharmacy_page():
    add_form = PharPersonelAdd()
    delete_form=delete_pharmacy_form()
    date = str(datetime.datetime.now().date())
    print(date)
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT name,location,tel_num FROM pharmacies WHERE next_night_shift = '{}' """.format(date)
    cursor.execute(statement)
    connection.commit
    on_duty = cursor.fetchall()
    cursor.close()
	#id = session.get('id') # =pharmacy id
	#stat = session.get('status')
	#if (stat == 4):
    form1 = G_PharmacySearchForm()
    logged_in = session.get('logged_in')
	#print(logged_in)
    s = (session.get('status') == 4)
	#for debug
    #logged_in = s=True
    #phar_id =11
	#
    if form1.validate_on_submit():
        attr = form1.select.data
        key = form1.search.data
        results=[]
        connection =db.connect(url)
        cursor = connection.cursor()
        statement = """SELECT pharmacies.name,location,next_night_shift,pharmacies.tel_num,pharmacy_personel.name,pharmacies.id FROM pharmacies,pharmacy_personel WHERE """"" + "CAST(pharmacies.{} AS TEXT) ILIKE  \'%{}%\' AND pharmacies.pharmacist = pharmacy_personel.id ORDER BY pharmacies.{} ASC".format(attr,key,attr)
        #print(statement)
        cursor.execute(statement)
        connection.commit()
        for row in cursor:
            results.append(row)
        cursor.close()
        return render_template('pharmacy_page.html', on_duty = on_duty,   search_form = form1,logged_in=False, results = results,searched = True,add_form=add_form,delete_form=delete_form)
	
    if ((logged_in) and ( s )):
        phar_id = session.get('id')
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """SELECT name,location,next_night_shift,tel_num,pharmacist,helper FROM pharmacies
                        WHERE id = '{}' """.format(phar_id) 
        cursor.execute(statement)
        connection.commit()
        phar_detail = cursor.fetchone()
        pharmacist_id=phar_detail[4]
        helper_id=phar_detail[5]
        statement = """ SELECT name,tel_num FROM pharmacy_personel
                        WHERE (id ={} or id={})""".format(pharmacist_id,helper_id)
        cursor.execute(statement)
        connection.commit()
        employees = cursor.fetchall() 
        cursor.close()
        return render_template('pharmacy_page.html',on_duty = on_duty , id = phar_id,Pharma = phar_detail,Employees = employees,search_form = form1,logged_in=logged_in,add_form=add_form,delete_form=delete_form)
    return render_template('pharmacy_page.html' , on_duty = on_duty , search_form = form1,logged_in=False,searched = False,add_form=add_form,delete_form=delete_form)
	
@app.route("/inventory/<id>/<mode>",methods=['GET', 'POST'])
def inventory_page(id,mode):
	#logged_in = session.get('logged_in') and (session.get('status')==4 or session.get('status')==5)
	logged_in = True  # test

	connection = db.connect(url)
	cursor = connection.cursor()
	if (logged_in):  # pharma or pwarehouse
		if (mode == 'p'):
			statement = "select name from pharmacies where id={} ".format(id)
			cursor.execute(statement)
			connection.commit()
			name = cursor.fetchone()[0]

			self = (session.get('status')==4 and session.get('id')==id)
			#self = True
			if (self):
				forms = inventory_change_form()
				i = []
				statement = "select NAME , number, drugs_id from DRUGS,pharmacy_inventory where pharmacy_inventory.pharmacy_id = {} and drugs_id = ID".format(id)
				cursor.execute(statement)
				connection.commit()
				inventory = cursor.fetchall()
				for k in range(0, len(inventory)):
					i.append(k)

				
				if forms.validate_on_submit():
					k = int(forms.request_id.data)
					if forms.bought.data:
						new_value = 1
					elif forms.sold.data:
						new_value = -1

					new_value = int(inventory[k][1]) + new_value
					if new_value == 0:
						statement = "DELETE FROM public.pharmacy_inventory WHERE drugs_id={} and pharmacy_id = {};".format(inventory[k][2], id)
						del i[-1]
					else:
						#print ("aaaaaaaa")
						statement = "UPDATE public.pharmacy_inventory SET number={} WHERE drugs_id={} and pharmacy_id = {};".format(new_value, inventory[k][2], id)

				cursor.execute(statement)
				connection.commit()
				statement = "select NAME , number from DRUGS,pharmacy_inventory where pharmacy_inventory.pharmacy_id = {} and drugs_id = ID".format(id)
				cursor.execute(statement)
				connection.commit()
				i=[]
				inventory = cursor.fetchall()
				cursor.close()

				return render_template('inventory_page.html', self=True, name=name, results=inventory, i=i, forms=forms)
			else:
				statement = "select NAME from DRUGS,pharmacy_inventory where pharmacy_inventory.pharmacy_id = {} and drugs_id = ID".format(id)
				cursor.execute(statement)
				connection.commit()
				i=[]
				inventory = cursor.fetchall()
				for k in range(0,len(inventory)):
					i.append(k)
				cursor.close()
				return render_template('inventory_page.html', self=False, name=name, results=inventory)

		elif (mode == 'w'):
			if (self):
				forms = inventory_change_form()
				i = []
				statement = "select NAME , number, drugs_id from DRUGS,warehouse_inventory where warehouse_inventory.warehouse_id = {} and drugs_id = ID".format(id)
				cursor.execute(statement)
				connection.commit()
				inventory = cursor.fetchall()
				for k in range(0, len(inventory)):
					i.append(k)

				
				if forms.validate_on_submit():
					k = int(forms.request_id.data)
					if forms.bought.data:
						new_value = 1
					elif forms.sold.data:
						new_value = -1

					new_value = int(inventory[k][1]) + new_value
					if new_value == 0:
						statement = "DELETE FROM public.warehouse_inventory WHERE drugs_id={} and warehouse_id = {};".format(inventory[k][2], id)
						del i[-1]
					else:
						#print ("aaaaaaaa")
						statement = "UPDATE public.warehouse_inventory SET number={} WHERE drugs_id={} and warehouse_id = {};".format(new_value, inventory[k][2], id)

				cursor.execute(statement)
				connection.commit()
				statement = "select NAME , number from DRUGS,warehouse_inventory where warehouse_inventory.warehouse_id = {} and drugs_id = ID".format(id)
				cursor.execute(statement)
				connection.commit()
				inventory = cursor.fetchall()
				cursor.close()

				return render_template('inventory_page.html', self=True, name=name, results=inventory, i=i, forms=forms)
			else:
				statement = "select name from pharmaceutical_warehouse where id={} ".format(id)
				cursor.execute(statement)
				connection.commit()
				name = cursor.fetchone()[0]
				statement = "select NAME , number from DRUGS,warehouse_inventory where warehouse_inventory.id = {} and drugs_id = ID".format(id)
				cursor.execute(statement)
				connection.commit()
				inventory = cursor.fetchall()
				cursor.close()
				return render_template('inventory_page.html', self=True, name=name, results=inventory)
		else:
			return redirect(url_for('home_page'))

	else:
		return redirect(url_for('home_page'))
	return redirect(url_for('home_page'))


@app.route("/pharmaceutical_warehouse", methods=['GET', 'POST'])
def pharmaceutical_warehouse_page():

	logged_in = session.get('logged_in')
	status = session.get('status')
	if (logged_in):
		id = session.get('id')  # =warehouse id
	#logged_in = True
	if (logged_in and (status == 5 or status == 4)):
		form = G_WarehouseSearchForm()
		if form.validate_on_submit():
			attr = form.select.data
			key = form.search.data
			results = []
			connection = db.connect(url)
			cursor = connection.cursor()
			statement = """SELECT id, name, tel_num, years_worked, adress, region, carriers FROM public.pharmaceutical_warehouse WHERE """"" + \
				"CAST(pharmaceutical_warehouse.{} AS TEXT) ILIKE  \'%{}%\' ORDER BY pharmaceutical_warehouse.{} ASC".format(
					attr, key, attr)
			cursor.execute(statement)
			connection.commit()
			for row in cursor:
				results.append(row)
			cursor.close()
			return render_template('pharmaceutical_warehouse_page.html', logged_in=False, searched=True, results=results, search_form=form)
		elif (logged_in and status == 5):
			connection = db.connect(url)
			cursor = connection.cursor()
			statement = "SELECT id, name, tel_num, years_worked, adress, region, carriers FROM public.pharmaceutical_warehouse WHERE id = {}".format(
				id)
			cursor.execute(statement)
			connection.commit()
			info = cursor.fetchone
			return render_template('pharmaceutical_warehouse_page.html', logged_in=True, searched=False, ware=info, search_form=form)
		elif (logged_in and status == 5):
			return render_template('pharmaceutical_warehouse_page.html', logged_in=False, searched=False, results=results, search_form=form)

	else:
		return redirect(url_for('home_page'))
	return redirect(url_for('home_page'))


@app.route("/edit_p_personel", methods=['GET', 'POST'])
def edit_p_personel_page():
	per_id = session['per_id']
	if (per_id):
		connection = db.connect(url)
		cursor = connection.cursor()
		statement = """SELECT name,tel_num,years_worked FROM pharmacy_personel WHERE id = '{}' """.format(per_id)
		cursor.execute(statement)
		connection.commit()
		person = cursor.fetchone()
		form = PharPersonelEditForm()
		if form.validate_on_submit():
			print("hops")
			tel = form.tel.data
			years = form.years.data
			statement = "UPDATE public.pharmacy_personel SET tel_num={}, years_worked={}	WHERE id = {};".format(tel,years,per_id)
			cursor.execute(statement)
			connection.commit()
			session['per_id'] = None
			cursor.close()
			return  redirect(url_for('pharmacy_page'))
		cursor.close()
		return render_template('edit_p_personel_page.html',per=person,form=form)
	else: 
		return redirect(url_for('home_page'))
	return

def hospital_page():
    hospitals = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ SELECT * FROM HOSPITAL ORDER BY HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    rows=cursor.fetchall()
    for db_hosp in rows:
        hospitals.append(hospital(db_hosp[0],db_hosp[1],db_hosp[2],db_hosp[3],db_hosp[4],db_hosp[5],db_hosp[6]))
    cursor.close()
    form=HospitalSearchForm()
    status = session.get('status')
    #status=1
    delform=HospitalDeleteForm()
    if(request.method=='POST'):
        if form.validate_on_submit() and form.submit.data:
            selection=form.selection.data
            data=form.search.data
            button=form.publicHos.data
            hospital_form=[]
            connection=db.connect(url)
            cursor =connection.cursor()
            if(button=='*'):
                statement="""SELECT * FROM HOSPITAL WHERE CAST({} AS TEXT) ILIKE  \'%{}%\' ORDER BY {} ASC """.format(selection, data , selection)
            else:
                statement="""SELECT * FROM HOSPITAL WHERE CAST({} AS TEXT) ILIKE  \'%{}%\' AND IS_PUBLIC={} ORDER BY {} ASC """.format(selection, data ,button, selection)
    #        print(statement)
            cursor.execute(statement)
            connection.commit()
            rows=cursor.fetchall()
            for db_hosp in rows:
                hospital_form.append(hospital(db_hosp[0],db_hosp[1],db_hosp[2],db_hosp[3],db_hosp[4],db_hosp[5],db_hosp[6]))
            cursor.close()
            return render_template('hospital_page.html', hospital=hospital_form, form=form,delform=delform, stat=status, len=len(hospital_form))
        if delform.validate_on_submit() and delform.delete.data:
            del_list=request.form.getlist("del_hospitals")
            connection=db.connect(url)
            cursor=connection.cursor()
            if(len(del_list)>1):
                del_hospitals=tuple(del_list)
                statement="DELETE FROM hospital WHERE hospital_id IN {}".format(del_hospitals)
            else:
                del_hospitals=''.join(str(e) for e in del_list)
                statement="DELETE FROM hospital WHERE hospital_id ={}".format(del_hospitals)
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('hospital_page'))
    return render_template('hospital_page.html', hospital=hospitals, form=form,delform=delform, stat=status, len=len(hospitals))
app.add_url_rule("/hospital", view_func=hospital_page, methods=['GET', 'POST'])

def add_hospital():
    status=session.get('status')
    #status=1
    if status not in (1,7):
        return redirect(url_for('home_page'))
    hospitals=[]
    connection=db.connect(url)
    cursor=connection.cursor()
    statement = """ SELECT * FROM HOSPITAL ORDER BY HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        hospitals.append(row)
    cursor.close()
    hosAddForm=HospitalAddForm()
    if hosAddForm.validate_on_submit():
        hospital_name=hosAddForm.hospital_name.data
        is_public=hosAddForm.is_public.data
        location=hosAddForm.location.data
        administrator=hosAddForm.administrator.data
        telephone_number=hosAddForm.telephone_number.data
        ambulance_count=hosAddForm.ambulance_count.data
        connection = db.connect(url)
        cursor=connection.cursor()
        statement="""INSERT INTO HOSPITAL(HOSPITAL_NAME,IS_PUBLIC,LOCATION,ADMINISTRATOR,TELEPHONE_NUMBER, AMBULANCE_COUNT) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""".format(hospital_name,is_public,location,administrator,telephone_number,ambulance_count)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('hospital_page'))
    return render_template('hospital_add_page.html',hospital=hospitals,form=hosAddForm )
app.add_url_rule('/hospital/add_hospital',view_func=add_hospital, methods=['GET','POST'])

def edit_hospital(hospital_id):
    status = session.get('status')
    #status=1

    if status not in (1,7):
        return redirect(url_for('home_page'))
    connection=db.connect(url)
    cursor=connection.cursor()
    statement = """ SELECT * FROM HOSPITAL WHERE HOSPITAL_ID={}""".format(hospital_id)
    cursor.execute(statement)
    connection.commit()
    db_hosp=cursor.fetchone()
    if db_hosp==None:
        abort(404)
    hospitalToedit=hospital(db_hosp[0],db_hosp[1],db_hosp[2],db_hosp[3],db_hosp[4],db_hosp[5],db_hosp[6])
    cursor.close()
    form=HospitalAddForm()
    if request.method=='POST':
        if form.validate_on_submit():
            hospital_name=form.hospital_name.data
            is_public=form.is_public.data
            location=form.location.data
            administrator=form.administrator.data
            telephone_number=form.telephone_number.data
            ambulance_count=form.ambulance_count.data
            connection = db.connect(url)
            cursor=connection.cursor()
            statement="""UPDATE HOSPITAL SET hospital_name='{}', is_public='{}', location='{}', administrator='{}', telephone_number='{}', ambulance_count='{}' WHERE HOSPITAL_ID={}""".format(hospital_name,is_public,location,administrator,telephone_number,ambulance_count, hospital_id)
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('hospital_page'))
    return render_template('hospital_edit_page.html',hospital=hospitalToedit,form=form)      
app.add_url_rule('/<int:hospital_id>/edit_hospital',view_func=edit_hospital, methods=['GET','POST'])

def single_personnel_page(personnel_id):
    status = session.get('status')
    #status=1
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM, WORKING_FIELD, HOSPITAL_WORKED, TCKN,  HOSPITAL_NAME FROM HOSPITAL_PERSONNEL JOIN HOSPITAL ON HOSPITAL_WORKED=HOSPITAL_ID WHERE PERSONNEL_ID ='{}'""".format(
        personnel_id)
    cursor.execute(statement)
    connection.commit()
    db_person = cursor.fetchone()
    if db_person==None:
         abort(404)
    person = hospital_personnel(db_person[0], db_person[1], db_person[2], db_person[3],
                                db_person[4], db_person[5], db_person[6], db_person[7], db_person[8], db_person[9])
    cursor.close()
    form=PersonnelAddForm()
    if form.validate_on_submit():
        worker_name=form.worker_name.data
        job_title=form.job_title.data
        job_experience=form.job_experience.data
        work_days=form.work_days.data
        phone_num=form.phone_num.data
        working_field=form.working_field.data
        hospital_worked=form.hospital_worked.data
        tckn=form.tckn.data
        connection = db.connect(url)
        cursor=connection.cursor()
        statement="""UPDATE hospital_personnel SET worker_name='{}', job_title='{}', job_experience={}, work_days={}, phone_num='{}', working_field='{}', hospital_worked='{}', tckn='{}'
         WHERE personnel_id={}""".format(worker_name,job_title,job_experience,work_days,phone_num,working_field,hospital_worked,tckn,personnel_id)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('hospital_personnel_sheet'))
    return render_template('single_personnel_page.html', personnel=person,form=form, stat=status,personnel_id=personnel_id)
app.add_url_rule("/emergency_shift/<int:personnel_id>",view_func=single_personnel_page, methods=['GET','POST'])


def hospital_personnel_sheet():
    status = session.get('status')
    #status=1
    workers = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM,WORKING_FIELD, HOSPITAL_WORKED, TCKN,  HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID GROUP BY PERSONNEL_ID, HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    data=cursor.fetchall()
    for db_hosp_personnel in data:
        workers.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
    cursor.close()
    searchForm=PersonnelSearchForm()
    delForm=PersonnelDeleteForm()
    if request.method=='POST':
        if searchForm.validate_on_submit():
            selection=searchForm.selection.data
            search=searchForm.search.data
            connection=db.connect(url)
            cursor =connection.cursor()
            personnel_form=[]
            statement="""SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM, WORKING_FIELD, HOSPITAL_WORKED,TCKN, HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID AND CAST({} AS TEXT) ILIKE  \'%{}%\' ORDER BY {} ASC """.format(selection, search ,selection)
            cursor.execute(statement)
            connection.commit()
            rows=cursor.fetchall()
            for db_hosp_personnel in rows:
                personnel_form.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
            cursor.close()
            return render_template('hospital_personnel_page.html',hospital_personnel=personnel_form, searchForm=searchForm,delForm=delForm,stat=status)
        if delForm.validate_on_submit() and delForm.delete.data:
            del_list=request.form.getlist("del_personnel")
            connection=db.connect(url)
            cursor=connection.cursor()
            if(len(del_list)>1):
                del_personnel=tuple(del_list)
                statement="""DELETE FROM HOSPITAL_PERSONNEL WHERE PERSONNEL_ID IN {}""".format(del_personnel)
                print(statement)
            else:
                del_personnel=''.join(str(e) for e in del_list)
                statement="""DELETE FROM HOSPITAL_PERSONNEL WHERE PERSONNEL_ID = {}""".format(del_personnel)
                print(statement)
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('hospital_personnel_sheet'))
    return render_template('hospital_personnel_page.html', hospital_personnel=workers,searchForm=searchForm,delForm=delForm,stat=status)
app.add_url_rule("/hospital_personnel",
                 view_func=hospital_personnel_sheet, methods=['GET','POST'])

def add_personnel():
    status=session.get('status')
    #status=1
    if status not in (1,6,7):
        return redirect(url_for('home_page'))
    personnel=[]
    connection=db.connect(url)
    cursor=connection.cursor()
    statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM,WORKING_FIELD, HOSPITAL_WORKED, TCKN,  HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID GROUP BY PERSONNEL_ID, HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    data=cursor.fetchall()
    for db_hosp_personnel in data:
        personnel.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
    cursor.close()
    addForm=PersonnelAddForm()
    if addForm.validate_on_submit():
        worker_name=addForm.worker_name.data
        job_title=addForm.job_title.data
        job_experience=addForm.job_experience.data
        work_days=addForm.work_days.data
        phone_num=addForm.phone_num.data
        working_field=addForm.working_field.data
        hospital_worked=addForm.hospital_worked.data
        tckn=addForm.tckn.data
        connection = db.connect(url)
        cursor=connection.cursor()
        statement="""INSERT INTO public.hospital_personnel(worker_name, job_title, job_experience, work_days, phone_num, working_field, hospital_worked, tckn)
	VALUES (\'{}\',\'{}\',\'{}\',\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')""".format(worker_name,job_title,job_experience,work_days,phone_num,working_field,hospital_worked,tckn)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('hospital_personnel_sheet'))
    return render_template('personnel_add_page.html',personnel=personnel,form=addForm, stat=status)
app.add_url_rule('/hospital_personnel/add_personnel',view_func=add_personnel, methods=['GET','POST'])

def hospital_personnel_page(hospital_id):
    status=session.get('status')
    #status=1
    workers =[]
    connection = db.connect(url)
    cursor=connection.cursor()
    statement = statement = """SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE,
        JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM,WORKING_FIELD, HOSPITAL_WORKED, TCKN , HOSPITAL_NAME FROM HOSPITAL_PERSONNEL RIGHT JOIN HOSPITAL ON HOSPITAL_WORKED=HOSPITAL_ID WHERE HOSPITAL_WORKED =%s"""
    cursor.execute(statement,[hospital_id])
    connection.commit()
    data=cursor.fetchall()
    for db_hosp_personnel in data:
        workers.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
    cursor.close()
    searchForm=PersonnelSearchForm()
    delForm=PersonnelDeleteForm()
    if request.method=='POST':
        if searchForm.validate_on_submit():
            selection=searchForm.selection.data
            search=searchForm.search.data
            connection=db.connect(url)
            cursor =connection.cursor()
            personnel_form=[]
            statement="""SELECT PERSONNEL_ID, WORKER_NAME, JOB_TITLE, JOB_EXPERIENCE, WORK_DAYS, PHONE_NUM, WORKING_FIELD, HOSPITAL_WORKED,TCKN, HOSPITAL_NAME FROM HOSPITAL_PERSONNEL, HOSPITAL WHERE HOSPITAL_WORKED=HOSPITAL_ID AND CAST({} AS TEXT) ILIKE  \'%{}%\' ORDER BY {} ASC """.format(selection, search ,selection)
            cursor.execute(statement)
            connection.commit()
            rows=cursor.fetchall()
            for db_hosp_personnel in rows:
                personnel_form.append(hospital_personnel(db_hosp_personnel[0],db_hosp_personnel[1],db_hosp_personnel[2],db_hosp_personnel[3],db_hosp_personnel[4],db_hosp_personnel[5],db_hosp_personnel[6],db_hosp_personnel[7],db_hosp_personnel[8],db_hosp_personnel[9]))
            cursor.close()
        if delForm.validate_on_submit() and delForm.delete.data:
            del_list=request.form.getlist("del_personnel")
            connection=db.connect(url)
            cursor=connection.cursor()
            if(len(del_list)>1):
                del_personnel=tuple(del_list)
                statement="""DELETE FROM HOSPITAL_PERSONNEL WHERE personnel_id IN {}""".format(del_personnel)
            else:
                del_personnel=''.join(str(e) for e in del_list)
                statement="""DELETE FROM HOSPITAL_PERSONNEL WHERE personnel_id = {}""".format(del_personnel)
            connection.commit()
            cursor.close()
            return redirect(url_for('hospital_personnel_sheet'))
        return render_template('hospital_personnel_page.html',hospital_personnel=personnel_form, searchForm=searchForm,delForm=delForm,stat=status)
    return render_template('hospital_personnel_page.html',hospital_personnel=workers, searchForm=searchForm, delForm=delForm, stat=status)
app.add_url_rule("/<int:hospital_id>/hospital_personnel",view_func=hospital_personnel_page,methods=["GET","POST"])


def emergency_shift_page():
    data = []
    status = session.get('status')
    #status=1
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT GENERATED_KEY,HOSPITAL_PERSONNEL.PERSONNEL_ID, SHIFT_BEGIN_DATE,SHIFT_REPEAT_INTERVAL,SHIFT_HOURS,DAYSHIFT ,EMERGENCY_AREA_ASSIGNED, WORKER_NAME FROM DAY_TABLE LEFT JOIN HOSPITAL_PERSONNEL ON DAY_TABLE.PERSONNEL_ID=HOSPITAL_PERSONNEL.PERSONNEL_ID ORDER BY SHIFT_BEGIN_DATE"""
    cursor.execute(statement)
    connection.commit()
    fetcheddata=cursor.fetchall()
    for row in fetcheddata:
        data.append(shift_data(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
    cursor.close()
    form=ShiftAddForm()
    if form.validate_on_submit():
        personnel_id=form.personnel_id.data
        shift_begin_date=form.shift_begin_date.data
        shift_repeat_interval=form.shift_repeat_interval.data
        shift_hours=form.shift_hours.data
        dayshift=form.dayshift.data
        emergency_area_assigned=form.emergency_area_assigned.data
        connection =db.connect(url)
        cursor = connection.cursor()
        statement="""INSERT INTO day_table(
	personnel_id, shift_begin_date, shift_repeat_interval, shift_hours, dayshift, emergency_area_assigned)
	VALUES ( \'{}\',\'{}\',\'{}\', \'{}\', \'{}\', \'{}\')""".format(personnel_id,shift_begin_date,shift_repeat_interval,shift_hours,dayshift,emergency_area_assigned)
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return redirect(url_for('emergency_shift_page'))
    delform=HospitalDeleteForm()
    if delform.validate_on_submit():
            del_list=request.form.getlist("del_shift")
            connection=db.connect(url)
            cursor=connection.cursor()
            if(len(del_list)>1):
                del_intro=tuple(del_list)
                statement="""DELETE FROM DAY_TABLE WHERE GENERATED_KEY IN {}""".format(del_intro)
            else:
                del_intro=''.join(str(e) for e in del_list)
                statement="""DELETE FROM DAY_TABLE WHERE GENERATED_KEY ={}""".format(del_intro)
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return redirect(url_for('emergency_shift_page'))
    return render_template('emergency_shift_page.html',form=form,delform=delform, data=data,stat=status)
app.add_url_rule("/emergency_shift",
                 view_func=emergency_shift_page, methods=['GET','POST'])

@app.route("/policlinics/")
def choose_hospital():
    log_id = session.get("status")
    hospitals = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ SELECT * FROM HOSPITAL ORDER BY HOSPITAL_NAME"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        hospitals.append(row)
    cursor.close()
    return render_template('choose_hospital.html',hospital = hospitals,log_id = log_id)

@app.route("/policlinics/<hospital_id>")
def all_policlinics(hospital_id):
    log_id = session.get("status")
    policlinics = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ SELECT POLICLINICS.*,HOSPITAL.HOSPITAL_NAME,HOSPITAL_PERSONNEL.WORKER_NAME FROM POLICLINICS,HOSPITAL,HOSPITAL_PERSONNEL
        WHERE POLICLINICS.HOSPITAL_ID="""+"CAST("+hospital_id+"AS INTEGER)""" + """
        AND POLICLINICS.HOSPITAL_ID = HOSPITAL.HOSPITAL_ID
        AND POLICLINICS.RECEPTIONIST_ID = HOSPITAL_PERSONNEL.PERSONNEL_ID
    """
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        policlinics.append(row)
    cursor.close()
    return render_template('policlinics.html',policlinics = policlinics ,hospital_id = hospital_id,log_id = log_id)

@app.route("/add_policlinics/<hospital_id>",methods=['GET', 'POST'])
def add_pol(hospital_id):
    log_id = session.get("status")
    if(request.method == 'GET'):
        return render_template('pol_add.html', hospital_id = hospital_id, log_id = log_id)
    else:
        connection = db.connect(url)
        cursor = connection.cursor()
        r_id = int(request.form['r_id'])
        name = request.form['name']
        ex_room = request.form['ex_room']
        if ex_room == "":
            ex_room = 0
        op_room = request.form['op_room']
        if op_room == "" :
            op_room = 0
        if request.form.get('private') :
            private = True
        else:
            private = False

        if request.form.get('pedi') :
            pedi = True
        else:
            pedi = False
        
        statement = """INSERT INTO POLICLINICS (HOSPITAL_ID,RECEPTIONIST_ID,NAME,NUMBER_OF_EXAMINATION_ROOMS,NUMBER_OF_OPERATION_ROOMS,PRIVATE,IS_PEDIATRICS) VALUES (
            """ +"CAST("+str(hospital_id)+" AS INTEGER)""" + """,
            """ +"CAST("+str(r_id)+" AS INTEGER)""" + """,
            """ +"CAST('"+ str(name)+"' AS VARCHAR) """ + """,
            """ +"CAST("+str(ex_room)+" AS INTEGER)""" + """,
            """ +"CAST("+str(op_room)+" AS INTEGER)""" + """,
            """ +"CAST('"+ str(private)+"' AS BOOL) """ + """,
            """ +"CAST('"+ str(pedi)+"' AS BOOL) """ + """
        );
        """
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return all_policlinics(hospital_id)

@app.route("/edit_pol/<hospital_id>/<id>/",methods=['GET', 'POST'])
def edit_pol(hospital_id,id):
    log_id = session.get("status")
    if(request.method == 'GET'):
        return render_template('edit_policlinics.html', id = id,hospital_id = hospital_id, log_id = log_id)
    else:
        flag = True
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """UPDATE POLICLINICS """

        if request.form.get('r_id'):
            flag = False
            r_id = int(request.form['r_id'])
            statement = statement + """SET RECEPTIONIST_ID = """ +"CAST("+str(r_id)+" AS INTEGER)""" 

        if request.form.get('name'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            name = request.form['name']
            statement = statement + """NAME = """ +"CAST("+str(name)+" AS VARCHAR)"""

        if request.form.get('ex_room'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            ex_room = int(request.form['ex_room'])
            statement = statement + """NUMBER_OF_EXAMINATION_ROOMS = """ +"CAST("+str(ex_room)+" AS INTEGER)"""

        if request.form.get('op_room'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            op_room = int(request.form['op_room'])
            statement = statement + """NUMBER_OF_OPERATION_ROOMS = """ +"CAST("+str(op_room)+" AS INTEGER)"""

        if request.form.get('private'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            private = request.form['private']
            statement = statement + """PRIVATE = """ +"CAST("+str(private)+" AS BOOL)""" 

        if request.form.get('pedi'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            pedi = request.form['pedi']
            statement = statement + """IS_PEDIATRICS = """ +"CAST("+str(pedi)+" AS BOOL)"""
        
        statement = statement + """WHERE ID = """+"CAST('"+str(id)+"'AS INTEGER)"""
        if flag:
            cursor.close()
            return all_policlinics(hospital_id)
        else:
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return all_policlinics(hospital_id)

@app.route("/pol_del/<id>")
def pol_del(id):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ DELETE FROM POLICLINICS
        WHERE ID="""+"CAST("+id+"AS INTEGER)""" + """
    """
    print(statement)
    cursor.execute(statement)
    connection.commit()
    cursor.close()
    return choose_hospital()

@app.route("/policlinics/<hospital_id>/<pol_id>") 
def det_policlinic(hospital_id,pol_id):
    log_id = session.get("status")
    policlinic = []
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ SELECT DETAILED_POLICLINICS.*,HOSPITAL.HOSPITAL_NAME,POLICLINICS.NAME,HOSPITAL_PERSONNEL.WORKER_NAME FROM DETAILED_POLICLINICS,POLICLINICS,HOSPITAL,HOSPITAL_PERSONNEL 
        WHERE DETAILED_POLICLINICS.HOSPITAL_ID="""+"CAST("+hospital_id+"AS INTEGER)""" + """
        AND DETAILED_POLICLINICS.POLICLINIC_ID="""+"CAST("+pol_id+"AS INTEGER)""" + """
        AND DETAILED_POLICLINICS.HOSPITAL_ID = HOSPITAL.HOSPITAL_ID
        AND DETAILED_POLICLINICS.POLICLINIC_ID = POLICLINICS.ID
        AND DETAILED_POLICLINICS.DOCTOR_ID = HOSPITAL_PERSONNEL.PERSONNEL_ID
    """
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        policlinic.append(row)
    cursor.close()
    return render_template('det_policlinic.html',policlinic = policlinic,hospital_id = hospital_id, pol_id = pol_id,log_id = log_id)

@app.route("/add_policlinics/<hospital_id>/<pol_id>",methods=['GET', 'POST'])
def add_pol_det(hospital_id,pol_id):
    log_id = session.get("status")
    if(request.method == 'GET'):
        return render_template('det_pol_add.html', hospital_id = hospital_id, pol_id = pol_id,log_id = log_id)
    else:
        connection = db.connect(url)
        cursor = connection.cursor()
        d_id = int(request.form['d_id'])
        work = request.form['work_hours']
        result = request.form['result_hours']
        statement = """INSERT INTO DETAILED_POLICLINICS (HOSPITAL_ID,POLICLINIC_ID,DOCTOR_ID,WORKING_HOURS,RESULT_HOURS) VALUES (
            """ +"CAST("+str(hospital_id)+" AS INTEGER)""" + """,
            """ +"CAST("+str(pol_id)+" AS INTEGER)""" + """,
            """ +"CAST("+str(d_id)+" AS INTEGER)""" + """,
            """ +"CAST('"+ str(work)+"' AS VARCHAR) """ + """,
            """ +"CAST('"+str(result)+"' AS VARCHAR)""" + """
        );
        """
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return det_policlinic(hospital_id,pol_id)

@app.route("/delete_policlinics/<id>")
def det_pol_del(id):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ DELETE FROM DETAILED_POLICLINICS
        WHERE ID="""+"CAST("+id+"AS INTEGER)""" + """
    """
    print(statement)
    cursor.execute(statement)
    connection.commit()
    cursor.close()
    return choose_hospital()

@app.route("/Prescription/<id>/", methods=['GET'])
def prescription_page(id):
    log_id = session.get("status")
    prescriptions = []
    date = datetime.datetime.now().date()
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """SELECT * FROM PRESCRIPTION 
		WHERE PATIENT_ID="""+"CAST("+id+"AS INTEGER)""" + """
		ORDER BY PRESCRIPTION_DATE DESC
	"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        prescriptions.append(row)
    cursor.close()
    return render_template('prescription.html', Prescriptions=prescriptions, id=id,log_id = log_id)


@app.route("/Prescription_Add/<id>/", methods=['GET', 'POST'])
def prescription_add_page(id):
    log_id = session.get("status")
    if(request.method == 'GET'):
        return render_template('prescription_add.html', id=id,log_id = log_id)
    else:
        try:
            connection = db.connect(url)
            cursor = connection.cursor()

            h_a_name =[]
            dr_a_name = []
            p_a_name = []
        
            h_id = int(request.form['h_id'])
            dr_id = int(request.form['dr_id'])
            date = datetime.datetime.now().date()
            valid = request.form['validity']
            if valid == "":
                valid = 3


            statement = """SELECT HOSPITAL_NAME FROM HOSPITAL
            WHERE HOSPITAL_ID="""+"CAST("+ str(h_id)+" AS INTEGER)""" + """
            GROUP BY HOSPITAL_NAME"""
            cursor.execute(statement)
            for row in cursor:
                h_a_name.append(row)
            for name in h_a_name[0]:
                h_name = name

            statement = """SELECT WORKER_NAME FROM HOSPITAL_PERSONNEL
            WHERE PERSONNEL_ID="""+"CAST("+ str(dr_id)+" AS INTEGER)""" + """
            GROUP BY WORKER_NAME"""
            cursor.execute(statement)
            for row in cursor:
                dr_a_name.append(row)
            for name in dr_a_name[0]:
                dr_name = name

            statement = """SELECT NAME FROM PATIENTS
            WHERE ID = """+"CAST("+ str(id)+" AS INTEGER)""" + """
            GROUP BY NAME"""
            cursor.execute(statement)
            for row in cursor:
                p_a_name.append(row)
            for name in p_a_name[0]:
                p_name = name
        
            statement = """INSERT INTO PRESCRIPTION (HOSPITAL_ID,DOCTOR_ID, PATIENT_ID, HOSPITAL_NAME, DOCTOR_NAME, PATIENT_NAME ,PRESCRIPTION_DATE,VALIDATION) VALUES (
                """ +"CAST("+str(h_id)+" AS INTEGER)""" + """,
                """ +"CAST("+str(dr_id)+" AS INTEGER)""" + """,
                """ +"CAST("+str(id)+" AS INTEGER)""" + """,
                """ +"CAST('"+ str(h_name)+"' AS VARCHAR) """ + """,
                """ +"CAST('"+str(dr_name)+"' AS VARCHAR)""" + """,
                """ +"CAST('"+str(p_name)+"' AS VARCHAR)""" + """,
                """ +"CAST('"+str(date)+" 'AS DATE)""" + """,
                """ +"CAST("+str(valid)+" AS INTEGER)""" + """
            );
            """
            
            cursor.execute(statement)
            connection.commit()
        except db.DatabaseError:
            connection.rollback()
            flash('Something Went Wrong', 'danger')
        finally:
            cursor.close()
        return prescription_page(id)

@app.route("/edit_pres/<id>/<pid>", methods=['GET', 'POST'])
def edit_pres(id,pid):
    log_id = session.get("status")
    if(request.method == 'GET'):
        return render_template('edit_pres.html', id=id,pid=pid,log_id = log_id)
    else:
        flag = True
        h_a_name = []
        dr_a_name = []
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """UPDATE PRESCRIPTION """

        if request.form.get('h_id'):
            flag = False
            h_id = int(request.form['h_id'])
            statement1 = """SELECT HOSPITAL_NAME FROM HOSPITAL
                WHERE HOSPITAL_ID ="""+"CAST("+ str(h_id)+" AS INTEGER)""" + """
                GROUP BY HOSPITAL_NAME"""
            cursor.execute(statement1)
            for row in cursor:
                h_a_name.append(row)
            for name in h_a_name[0]:
                h_name = name

            statement = statement + """SET HOSPITAL_ID = """ +"CAST("+str(h_id)+" AS INTEGER),""" +"""
                HOSPITAL_NAME = """ +"CAST('"+ str(h_name)+"' AS VARCHAR) """

        if request.form.get('dr_id'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            dr_id = int(request.form['dr_id'])
            statement1 = """SELECT WORKER_NAME FROM HOSPITAL_PERSONNEL
                WHERE PERSONNEL_ID ="""+"CAST("+ str(dr_id)+" AS INTEGER)""" + """
                GROUP BY WORKER_NAME"""
            cursor.execute(statement1)
            for row in cursor:
                dr_a_name.append(row)
            for name in dr_a_name[0]:
                dr_name = name

            statement = statement + """DOCTOR_ID = """ +"CAST("+str(dr_id)+" AS INTEGER),""" +"""
                DOCTOR_NAME = """ +"CAST('"+ str(dr_name)+"' AS VARCHAR) """

        
        if request.form.get('validity'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            validity = int(request.form['validity'])
            statement = statement + """VALIDATION = """ +"CAST("+str(validity)+" AS INTEGER)"""

        
        statement = statement + """WHERE ID = """+"CAST('"+str(pid)+"'AS INTEGER)"""
        if flag:
            cursor.close()
            return prescription_page(id)
        else:
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return prescription_page(id)


        try:
            connection = db.connect(url)
            cursor = connection.cursor()

            h_a_name =[]
            dr_a_name = []
            p_a_name = []
        
            h_id = int(request.form['h_id'])
            dr_id = int(request.form['dr_id'])
            date = datetime.datetime.now().date()
            valid = request.form['validity']
            if valid == "":
                valid = 3


            statement = """SELECT HOSPITAL_NAME FROM HOSPITAL
            WHERE HOSPITAL_ID="""+"CAST("+ str(h_id)+" AS INTEGER)""" + """
            GROUP BY HOSPITAL_NAME"""
            cursor.execute(statement)
            for row in cursor:
                h_a_name.append(row)
            for name in h_a_name[0]:
                h_name = name

            statement = """SELECT WORKER_NAME FROM HOSPITAL_PERSONNEL
            WHERE PERSONNEL_ID="""+"CAST("+ str(dr_id)+" AS INTEGER)""" + """
            GROUP BY WORKER_NAME"""
            cursor.execute(statement)
            for row in cursor:
                dr_a_name.append(row)
            for name in dr_a_name[0]:
                dr_name = name

            statement = """SELECT NAME FROM PATIENTS
            WHERE ID = """+"CAST("+ str(id)+" AS INTEGER)""" + """
            GROUP BY NAME"""
            cursor.execute(statement)
            for row in cursor:
                p_a_name.append(row)
            for name in p_a_name[0]:
                p_name = name
        
            statement = """INSERT INTO PRESCRIPTION (HOSPITAL_ID,DOCTOR_ID, PATIENT_ID, HOSPITAL_NAME, DOCTOR_NAME, PATIENT_NAME ,PRESCRIPTION_DATE,VALIDATION) VALUES (
                """ +"CAST("+str(h_id)+" AS INTEGER)""" + """,
                """ +"CAST("+str(dr_id)+" AS INTEGER)""" + """,
                """ +"CAST("+str(id)+" AS INTEGER)""" + """,
                """ +"CAST('"+ str(h_name)+"' AS VARCHAR) """ + """,
                """ +"CAST('"+str(dr_name)+"' AS VARCHAR)""" + """,
                """ +"CAST('"+str(p_name)+"' AS VARCHAR)""" + """,
                """ +"CAST('"+str(date)+" 'AS DATE)""" + """,
                """ +"CAST("+str(valid)+" AS INTEGER)""" + """
            );
            """
            
            cursor.execute(statement)
            connection.commit()
        except db.DatabaseError:
            connection.rollback()
            flash('Something Went Wrong', 'danger')
        finally:
            cursor.close()
        return prescription_page(id)

@app.route("/pres_del/<id>/<pid>/")
def pres_del(id,pid):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ DELETE FROM PRESCRIPTION
        WHERE ID="""+"CAST("+pid+"AS INTEGER)""" + """
    """
    print(statement)
    cursor.execute(statement)
    connection.commit()
    cursor.close()
    return prescription_page(id)


@app.route("/Prescription/<id>/<pid>/", methods=['GET'])
def det_prescription_page(id, pid):
    log_id = session.get("status")
    drug = []
    examination = []
    date = datetime.datetime.now().date()
    connection = db.connect(url)
    cursor = connection.cursor()
    statement1 = """SELECT * FROM DETAILED_PRESCRIPTION
		WHERE PRESCRIPTION_ID="""+"CAST("+pid+"AS INTEGER)""" + """
		GROUP BY ID
	"""
    cursor.execute(statement1)
    connection.commit()
    for row in cursor:
        drug.append(row)
    cursor.close()
    connection = db.connect(url)
    cursor = connection.cursor()
    statement2 = """SELECT * FROM EXAMINATION
		WHERE PRESCRIPTION_ID="""+"CAST("+pid+"AS INTEGER)""" + """        
		GROUP BY ID
	"""
    cursor.execute(statement2)
    connection.commit()
    for row in cursor:
        examination.append(row)
    cursor.close()
    return render_template('detail_prescription.html', P_Drugs=drug, P_Examination=examination, id=id, pid=pid, log_id = log_id)

@app.route("/add_drug_pres/<id>/<pid>/",methods=['GET', 'POST'])
def add_drug_pres(id,pid):
    log_id = session.get("status")
    if(request.method == 'GET'):
        return render_template('add_drug_pres.html', id=id,pid=pid,log_id = log_id)
    else:
        connection = db.connect(url)
        cursor = connection.cursor()

        drug_a_name = []

        drug_id = int(request.form['drug_id'])
        
        statement = """SELECT NAME FROM DRUGS
            WHERE ID="""+"CAST("+ str(drug_id)+" AS INTEGER)""" + """
            GROUP BY NAME"""
        cursor.execute(statement)

        for row in cursor:
            drug_a_name.append(row)
        for name in drug_a_name[0]:
            drug_name = name

        print(drug_name)

        dosage = request.form['dosage']
        if dosage == "":
            dosage = 1
            
        times = request.form['times']
        if times == "":
            times = 1

        duration = request.form['duration']
        if duration == "":
            duration= 3

        if request.form.get('regular') :
            regular = True
        else:
            regular = False
        
        statement = """INSERT INTO DETAILED_PRESCRIPTION (PRESCRIPTION_ID,DRUG_ID,DRUG_NAME,DOSAGE_PER_TAKE,TIMES_PER_DAY,DURATION,REGULAR) VALUES (
            """ +"CAST("+str(pid)+" AS INTEGER)""" + """,
            """ +"CAST("+str(drug_id)+" AS INTEGER)""" + """,
            """ +"CAST('"+ str(drug_name)+"' AS VARCHAR) """ + """,
            """ +"CAST("+str(dosage)+" AS INTEGER)""" + """,
            """ +"CAST("+str(times)+" AS INTEGER)""" + """,
            """ +"CAST("+str(duration)+" AS INTEGER)""" + """,
            """ +"CAST('"+ str(regular)+"' AS BOOL) """ + """
        );
        """
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return det_prescription_page(id, pid)

@app.route("/edit_drug_pres/<id>/<pid>/<did>/",methods=['GET', 'POST'])
def edit_drug_pres(id,pid,did):
    log_id = session.get("status")
    if(request.method == 'GET'):
        return render_template('edit_drug_pres.html', id=id,pid=pid,did=did,log_id = log_id)
    else:
        flag = True
        drug_a_name = []
        connection = db.connect(url)
        cursor = connection.cursor()
        statement = """UPDATE DETAILED_PRESCRIPTION """

        if request.form.get('drug_id'):
            flag = False
            drug_id = int(request.form['drug_id'])
            statement1 = """SELECT NAME FROM DRUGS
                WHERE ID="""+"CAST("+ str(drug_id)+" AS INTEGER)""" + """
                GROUP BY NAME"""
            cursor.execute(statement1)
            for row in cursor:
                drug_a_name.append(row)
            for name in drug_a_name[0]:
                drug_name = name

            statement = statement + """SET DRUG_ID = """ +"CAST("+str(drug_id)+" AS INTEGER),""" +"""
                DRUG_NAME = """ +"CAST('"+ str(drug_name)+"' AS VARCHAR) """

        if request.form.get('dosage'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            dosager_id = int(request.form['dosage'])
            statement = statement + """SET DOSAGE_PER_TAKE = """ +"CAST("+str(dosage)+" AS INTEGER)""" 

        if request.form.get('times'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            times = request.form['times']
            statement = statement + """TIMES_PER_DAY = """ +"CAST("+str(times)+" AS VARCHAR)"""

        if request.form.get('duration'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            duration = int(request.form['duration'])
            statement = statement + """DURATION = """ +"CAST("+str(duration)+" AS INTEGER)"""

        if request.form.get('regular'):
            if flag ==False:
                statement = statement + ""","""
            else:
                statement = statement + """SET """
            flag = False
            regular = request.form['regular']
            statement = statement + """REGULAR = """ +"CAST("+str(regular)+" AS BOOL)"""
        
        statement = statement + """WHERE ID = """+"CAST('"+str(did)+"'AS INTEGER)"""
        if flag:
            cursor.close()
            return det_prescription_page(id, pid)
        else:
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            return det_prescription_page(id, pid)

@app.route("/drug_pres_del/<id>/<pid>/<did>")
def drug_pres_del(id,pid,did):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ DELETE FROM DETAILED_PRESCRIPTION
        WHERE ID="""+"CAST("+did+"AS INTEGER)""" + """
    """
    print(statement)
    cursor.execute(statement)
    connection.commit()
    cursor.close()
    return det_prescription_page(id, pid)

@app.route("/add_exam_pres/<id>/<pid>/",methods=['GET', 'POST'])
def add_exam_pres(id,pid):
    log_id = session.get("status")
    if(request.method == 'GET'):
        return render_template('add_exam_pres.html', id=id,pid=pid,log_id = log_id)
    else:
        connection = db.connect(url)
        cursor = connection.cursor()

        exam_type = request.form['exam_type']

        duration = request.form['duration']

        place = request.form['place']

        
        statement = """INSERT INTO EXAMINATION (PRESCRIPTION_ID,TYPE,DURATION,PLACE) VALUES (
            """ +"CAST("+str(pid)+" AS INTEGER)""" + """,
            """ +"CAST('"+ str(exam_type)+"' AS VARCHAR) """ + """,
            """ +"CAST("+str(duration)+" AS INTEGER)""" + """,
            """ +"CAST('"+ str(place)+"' AS VARCHAR) """ + """
        );
        """
        print(statement)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        return det_prescription_page(id, pid)

@app.route("/exam_pres_del/<id>/<pid>/<did>")
def exam_pres_del(id,pid,did):
    connection = db.connect(url)
    cursor = connection.cursor()
    statement = """ DELETE FROM EXAMINATION
        WHERE ID="""+"CAST("+did+"AS INTEGER)""" + """
    """
    print(statement)
    cursor.execute(statement)
    connection.commit()
    cursor.close()
    return det_prescription_page(id, pid)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
	if session.get('logged_in'):
		return redirect(url_for('home_page'))
	else:
		form = LoginForm()
		if form.validate_on_submit():
			id = form.id.data
			pw = form.password.data
			try:
				connection = db.connect(url)
				cursor = connection.cursor()
				statement = """SELECT * FROM USERS WHERE ID = '%s'
						""" % id
				cursor.execute(statement)
				result = cursor.fetchone()
				if(result[1] == pw):
					flash('You have been logged in!', 'success')
					session['logged_in'] = True
					session['id'] = id
					session['status'] = result[2]
					return redirect(url_for('home_page'))
				else:
					flash(
						'Login Unsuccessful. Please check username and password', 'danger')
			except db.DatabaseError:
				connection.rollback()
				flash('Login Unsuccessful. Please check username and password', 'danger')
			finally:
				connection.close()
		return render_template('login_page.html', title='Login', form=form)


@app.route("/logout")
def logout_page():
	session.pop('id', None)
	session['logged_in'] = False
	return redirect(url_for('home_page'))


if __name__ == "__main__":
	if(DEBUG):
		app.run(debug='True')
	else:
		app.run()
