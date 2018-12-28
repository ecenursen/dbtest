Parts Implemented by Ece Nur Şen
================================

.. note:: All table creations exist in db_init.py file.

**************
Policlinics
**************

1. Table
~~~~~~~~

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS POLICLINICS (
        ID SERIAL PRIMARY KEY,
        HOSPITAL_ID INTEGER,
        RECEPTIONIST_ID INTEGER,
        NAME VARCHAR(50) NOT NULL,
        NUMBER_OF_EXAMINATION_ROOMS INTEGER DEFAULT 0,
        NUMBER_OF_OPERATION_ROOMS INTEGER DEFAULT 0,
        PRIVATE BOOL DEFAULT FALSE,
        IS_PEDIATRICS BOOL DEFAULT FALSE,
        FOREIGN KEY (HOSPITAL_ID) 
            REFERENCES HOSPITAL(HOSPITAL_ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (RECEPTIONIST_ID) 
            REFERENCES HOSPITAL_PERSONNEL(PERSONNEL_ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )

HOSPITAL_ID is referencing HOSPITAL_ID from HOSPITAL table. When a hospital got deleted or updated, it will affect Policlinics Table. Policlinics with given hospital id will be deleted or updated accordingly.
RECEPTIONIST_ID is referencing PERSONNEL_ID from HOSPITAL_PERSONNEL table. When a hospital personnel got deleted or updated, it will affect Policlinics Table. Policlinics with given receptionist id will be deleted or updated accordingly.

2. Reading Policlinics
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function gets id of hospital and returns the all policlinics with given hospital id through html to user.

3. Adding Policlinics
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function insert new policlinic to policlinics table. When the method is 'GET', it returns html of adding page. When the method is 'POST', it creates a sql statement for inserting new entry and executes accordingly.

4. Editing Policlinics
~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

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

This function updates a policlinic from Policlinics table. When the method is 'GET', it returns html of editing page. When method is 'POST', it generates an sql statement for updating table and it executes statement.

5. Deleting Policlinics
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::python

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

This function deletes choosen policlinic with given policlinics id from Policlinics Table.


**********************
Detailed Policlinics
**********************

1. Table
~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS DETAILED_POLICLINICS (
		ID  SERIAL PRIMARY KEY,
		HOSPITAL_ID INTEGER,
		POLICLINIC_ID INTEGER,
		DOCTOR_ID INTEGER,
		WORKING_HOURS VARCHAR(50),
		RESULT_HOURS VARCHAR(50),
		FOREIGN KEY (POLICLINIC_ID) 
			REFERENCES POLICLINICS(ID)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY (DOCTOR_ID) 
			REFERENCES HOSPITAL_PERSONNEL(PERSONNEL_ID)
			ON DELETE CASCADE
			ON UPDATE CASCADE,
		FOREIGN KEY (HOSPITAL_ID) 
			REFERENCES HOSPITAL(HOSPITAL_ID)
			ON DELETE CASCADE
			ON UPDATE CASCADE
	)

HOSPITAL_ID is referencing HOSPITAL_ID from HOSPITAL table. When a hospital got deleted or updated, it will affect Detailed_Policlinics Table. Detailed_Policlinics with given hospital id will be deleted or updated accordingly.
POLICLINIC_ID is referencing ID from POLICLINICS table. When a policlinics got deleted or updated, it will affect Detailed_Policlinics Table. Detailed_Policlinics with given policlinics id will be deleted or updated accordingly.
DOCTOR_ID is referencing PERSONNEL_ID from HOSPITAL_PERSONNEL table. When a hospital personnel got deleted or updated, it will affect Detailed_Policlinics Table. Detailed_Policlinics with given doctor id will be deleted or updated accordingly.

2. Reading Detailed_Policlinics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function gets id of hospital and id of policlinics, returns the detailed_policlinics with given hospital id and policlinics id through html to user.

3. Adding Detailed_Policlinics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function insert new detailed_policlinic to detailed_policlinics table. When the method is 'GET', it returns html of adding page. When the method is 'POST', it creates a sql statement for inserting new entry and executes accordingly.

4. Deleting Detailed_Policlinics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function deletes choosen detailed_policlinic with given id from Detailed_Policlinics Table.


**************
Prescription
**************

1. Table
~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS PRESCRIPTION (
		ID SERIAL PRIMARY KEY,
		HOSPITAL_ID INTEGER,
		DOCTOR_ID INTEGER,
		PATIENT_ID INTEGER,
		HOSPITAL_NAME VARCHAR,
		DOCTOR_NAME VARCHAR,
		PATIENT_NAME VARCHAR,
		PRESCRIPTION_DATE DATE NOT NULL,
		VALIDATION INTEGER DEFAULT 3,
		FOREIGN KEY (HOSPITAL_ID)  
			REFERENCES HOSPITAL(HOSPITAL_ID)
			ON DELETE SET NULL
			ON UPDATE SET NULL,
		FOREIGN KEY (DOCTOR_ID) 
			REFERENCES HOSPITAL_PERSONNEL(PERSONNEL_ID)
			ON DELETE SET NULL
			ON UPDATE SET NULL,
		FOREIGN KEY (PATIENT_ID) 
			REFERENCES PATIENTS(ID)
			ON DELETE CASCADE
			ON UPDATE SET NULL
    	)

HOSPITAL_ID is referencing HOSPITAL_ID from HOSPITAL table. When a hospital got deleted or updated, it will affect Prescription Table. Prescription with given hospital id will be set as NULL. Because when a hospital got destroyed or changed, we don't want prescription data to change.
DOCTOR_ID is referencing PERSONNEL_ID from HOSPITAL_PERSONNEL table. When a hospital personnel got deleted or updated, it will affect Prescription Table. Prescription with given doctor id will be set as NULL. Because when a doctor got died or changed, we don't want prescription data to change.
PATIENT_ID is referencing ID from PATIENTS table. When a patient got deleted or updated, it will affect Prescription Table. Prescription with given patient id will be deleted when a patient id wanted to be deleted. But when patient id wanted to be updated, patient id in prescription it will set as NULL.

2. Reading Prescription
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function gets id of patients and returns the all prescriptions with given patient id through html to user.

3. Adding Prescription
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function insert new prescription to prescription table. When the method is 'GET', it returns html of adding page. When the method is 'POST', it creates a sql statement for inserting new entry and executes accordingly.


4. Editing Prescription
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function updates a prescription from Prescription table. When the method is 'GET', it returns html of editing page. When method is 'POST', it generates an sql statement for updating table and it executes statement.


5. Deleting Prescription
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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


This function deletes choosen prescription with given prescription id from PRESCRIPTION Table.


***********************
Detailed Prescription
***********************

1. Table
~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS DETAILED_PRESCRIPTION(
		ID SERIAL PRIMARY KEY,
		PRESCRIPTION_ID INTEGER,
		DRUG_ID INTEGER,
		DRUG_NAME VARCHAR,
		DOSAGE_PER_TAKE INTEGER DEFAULT 1,
		TIMES_PER_DAY INTEGER DEFAULT 1, 
		DURATION INTEGER DEFAULT 3,
		REGULAR BOOL DEFAULT FALSE,
		FOREIGN KEY (PRESCRIPTION_ID) 
			REFERENCES PRESCRIPTION(ID)
			ON DELETE CASCADE
			ON UPDATE RESTRICT,
		FOREIGN KEY (DRUG_ID) 
			REFERENCES DRUGS(ID)
			ON DELETE SET NULL
			ON UPDATE SET NULL
    	)
	    
PRESCRIPTION_ID is referencing ID from PRESCRIPTION table. When a prescription got deleted or updated, it will affect Detailed_Prescription Table. Detailed_Prescription with given prescription id will be deleted when a prescription id wanted to be deleted. But when prescription id wanted to be updated, it will be restricted.
DRUG_ID is referencing ID from DRUGS table. When a drug got deleted or updated, it will affect Detailed_Prescription Table. Detailed_Prescription's drug id will be set as NULL. Because when a drug got no longer produced or changed, we don't want detailed_prescription data to change.

2. Reading Detailed_Prescription(Drugs) and Examination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function gets id of prescription and returns the drug and examination detailes of given prescription through html to user.

3. Adding Detailed_Prescription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function insert new detailed_prescription(drug) to detailed_prescription table. When the method is 'GET', it returns html of adding page. When the method is 'POST', it creates a sql statement for inserting new entry and executes accordingly.

4. Editing Detailed_Prescription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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
				dosage = int(request.form['dosage'])
				statement = statement + """ DOSAGE_PER_TAKE = """ +"CAST("+str(dosage)+" AS INTEGER)""" 

			if request.form.get('times'):
				if flag ==False:
					statement = statement + ""","""
				else:
					statement = statement + """SET """
				flag = False
				times = request.form['times']
				statement = statement + """TIMES_PER_DAY = """ +"CAST("+str(times)+" AS INTEGER)"""

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

This function updates a detail_prescription from Detailed_Prescription table. When the method is 'GET', it returns html of editing page. When method is 'POST', it generates an sql statement for updating table and it executes statement.

5. Deleting Detailed_Prescription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function deletes choosen detailed_prescription with given id from Detailed_Prescription Table.


**************
Examination
**************

1. Table
~~~~~~~~

.. code-block:: sql

	CREATE TABLE IF NOT EXISTS EXAMINATION(
		ID SERIAL PRIMARY KEY,
		PRESCRIPTION_ID INTEGER,
		TYPE VARCHAR(30) NOT NULL,
		DURATION INTEGER,
		PLACE VARCHAR(30),
		FOREIGN KEY (PRESCRIPTION_ID) 
			REFERENCES PRESCRIPTION(ID)
			ON DELETE CASCADE
			ON UPDATE RESTRICT
	)

PRESCRIPTION_ID is referencing ID from PRESCRIPTION table. When a prescription got deleted or updated, it will affect Examination Table. Examination with given prescription id will be deleted when a prescription id wanted to be deleted. But when prescription id wanted to be updated, it will be restricted.

2. Adding Examination
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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


This function insert new examination to examination table. When the method is 'GET', it returns html of adding page. When the method is 'POST', it creates a sql statement for inserting new entry and executes accordingly.

3. Deleting Examination
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

This function deletes choosen examination with given id from Examination Table.
