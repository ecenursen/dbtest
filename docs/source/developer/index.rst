Developer Guide
===============

Database Design
---------------

The open source database management system used in this project is PostgreSQL. It is a DBMS
with a diverse community which helps a lot in development phase. It also supports ACID (Atomicity,
Consistency, Isolation, Durability). It supports multiple indexing techniques such as GIN (Generalized Inverted Index)
 or GiST (Generealized Search Tree).

.. image:: postgresql.png
	:scale: 40 %
	:alt: Patient Page
	:align: center
	
Code
----

1. Database Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

	def initialize(url):
		with dbapi2.connect(url) as connection:
			cursor = connection.cursor()
			for statement in INIT_STATEMENTS:
				cursor.execute(statement)
			cursor.close()

	if __name__ == "__main__":
		url = os.getenv("DATABASE_URL")
		if url is None:
			print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
			sys.exit(1)
		initialize(url)

2. Sample Database Query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's imagine a scenario where the user wants to see everything from SAMPLE_TABLE with
a given ID number. A typical SQL query can be accomplished via the snippet below.

.. code-block:: python

	result = []
	connection = db.connect(url)
    cursor = connection.cursor()
    statement = "SELECT * FROM SAMPLE_TABLE WHERE ID={}".format(id)
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        result.append(row)
	cursor.close()
	
At the end of the execution, if successful, result list will be populated with the 
set of rows that satisfy the given query.

.. toctree::

   goktug
   member2
   member3
   member4
   member5
