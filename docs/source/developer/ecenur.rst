Parts Implemented by Ece Nur Şen
================================

All table creations are exist in db_init.py file.

**************
Policlinics
**************

Table
-----

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

Reading Policlinics
~~~~~~~~~~~~~~~~~~~

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

Adding Policlinics
~~~~~~~~~~~~~~~~~~

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

Editing Policlinics
~~~~~~~~~~~~~~~~~~~


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

This function updates a policlinic from Policlinics table. When the method is 'GET', it returns html of editing page. When method is 'POST', it generates an sql statement for updating table and is executes it.

Deleting Policlinics
~~~~~~~~~~~~~~~~~~~~

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

Table
-----

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

Reading Detailed_Policlinics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Adding Detailed_Policlinics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Deleting Detailed_Policlinics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Table
-----

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




