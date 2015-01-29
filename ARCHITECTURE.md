How BallotAPI works.

At the bottom of the stack is a PostgreSQL database with the PostGIS spatial extension.

Above that is a Flask based Python application that accepts GET requests, queries the database, and returns results.

That application is designed as follows:

The top level of the program is ballotapi.py.  Under that there is a file for each of the three API endpoints: precincts.py, elections.py, and measures.py.  There is also a queries.py that contains the parts of the database queries that are common between the three endpoint files.  Exception.py contains the custom exceptions for the application.

Ballotapi.py creates a flask instance, sets up the routes (urls) that flask will respond to, and sets up top level error handling.  It imports all three endpoint files and the exception.py file.  Each route calls its respective endpoint file.  Each endpoint file has the code unique to that endpoint but they mostly rely on the shared queries.py file to do the heavy lifting of querying the database. Queries.py also sets up the database connections.

Future additions: Output is currently not formatted.  The plan is to have the functions that do output formatting in their own files. Ballotapi.py will pass the desired output to the endpoint function, which will call the indicated output functions before returning the then formatted data.

The database is created with the create_database.sql file. 
