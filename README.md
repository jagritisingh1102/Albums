# Spotify Assignment
1. Clone the projet using below command:
    git clone https://github.com/jagritisingh1102/NuageAssignment.git
2. Open the project in any python editor
NOTE: Before doing below steps please check you are or correct path i.e., ../NuageAssignment
4. create virtual environment for the project using below command:
     python3 -m virtualenv venv
4. Select the correct interpreter for the project
5. Activate the virtual environment using below command:
     source venv/bin/activate
6. Install all the project requirements using below command:
      pip install -r requirements.txt
7. Check whether project is running or not with any of the below commands:
    i) python manager.py list_routes  (This will return the path of the APIs)
    ii) python manager.py runderver -p 5001 (This will return Running on http://127.0.0.1:5001)
8. Setup postgres on your local system.
9. Once postgres setup is done, create a superuser as well as database with name spotify or any name of your choice.
10. Inside spotify database create below extensions using following commands, these extensions are required for migrating models from the code to the postgres database:
      create extension postgis;
      create extension "uuid-ossp"
11. Go to .env file and update the database uri with your username, password and database name.
12. Use the below commands to migrate the models from code to the database
       flask db init
       flask db migrate
       flask db upgrade
13. All setup is done now we can hit the APIs on postman (You can use python manager.py list_routes to check all the API paths)

