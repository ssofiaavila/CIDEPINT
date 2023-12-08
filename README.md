## About
The project entails the development of a web application tailored for Research and Development institutions specializing in Paint Technology. The system provides an efficient environment for registering and managing services offered by these institutions, covering the entire process from request to service delivery.
Developed for the course "Software Project" at the UNLP Computer Science Faculty, 2023

## Contributors
- **Avila Sofia**
- **Cametho Federico**
- **Carrera Ignacio**
- **Castillo Franco**

## Stack
- Flask
- Vue.js
- PostgreSQL


## Local execution of Flask project "Admin"
The following details what is necessary to execute the Admin project locally, for which you must have some requirements

### Previous installations
- [Git](https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Instalaci%C3%B3n-de-Git): necessary to clone the repository.
- [Python](https://www.python.org/downloads/): Make sure Python is installed on the system. It can be verified by running `python --version` on the command line.
- Database engine, [PostgresSQL](https://www.postgresql.org/download/).

### Steps to follow
1. **Clone the repository:**
2. **Check if I have PIP installed**: running ```pip --version```

3. **Configure the virtual environment**: It is recommended to create a virtual environment to isolate dependencies.
- 3.1. Install virtualenv by running ```pip install virtualenv```
- 3.2. Go to the ``admin`` folder of the project.
- 3.3. Initialize the virtual environment by running ``virtualenv environmentName`` where ``environmentName`` is the name of what our environment will be called.
- 3.4. Activate the virtual environment by running ``sourceEnvironmentName/Scripts/activate``
4. **Install Poetry**:
4.1. Running ``python get-poetry.py`` and then we can verify its installation by running ``poetry --version``.
	
5. **Install Flask**
- 5.1: Install the new package to the virtual environment by running `poetry add flask`
6. **Configure the database**: once the database has been created in our database engine such as MySQL or PostgresSQL, the connection must be established.
- 6.1 From the terminal, the parameters for the connection must be indicated, which will be DB_USER, DB_PASS, DB_HOST and DB_NAME. Therefore from the command line positioned at ``../grupo19/admin/src`` execute
- `export DB_USER=username`
- `export DB_PASS=DBAccessPassword`
- `export DB_HOST=hostDeLaBD`
- `export DB_NAME=DBName`
Where each of the data is taken from the server properties and database created from the engine.
- 6.2. Run `Flask resetdb` to create the tables in our database.
- 6.3. Run `Flask populatedb` to generate content in our tables.

7. **Run application**: on the command line you must execute `poetry run flask run`

	

## Local execution of "Portal" Vue.js project
The following details what is necessary to execute the Portal project locally, for which you must have some requirements
#### Pre-installation
  - [Node.js](https://nodejs.org/en/download): you must choose the version that best suits the machine you are using, you can check if it is already installed by running `node -v` in our terminal .

### Steps to follow

Clarification: since the "Portal" project was developed in the same repository as the Flask application, the following step by step assumes that the installation of the back-end project was previously carried out, if not, start from Local execution of " Admin" Flask project and then continue with the instructions below.

1. **Add environment variables**: in the path *grupo19/portal* create a file called `.env` and add the following content `VITE_BACKEND_BASE_URL=http://localhost:5000`. It will be necessary for the URLs of the APIs that our project has.

2. **Dependencies**: it was necessary to add dependencies in both the Flask and Vue.js projects, therefore new ones will have to be updated or installed.
- 2.1. In the path *grupo19/admin* run `poetry update` to update dependencies of the back-end project.
- 2.2. In the path *grupo19/portal* run `npm install` to install the dependencies of our Vue.js project. It will take time due to the number of dependencies that are instantiated for the first time.

3. **Execution**: it will be necessary to execute both projects locally.
- 3.1. From the path *grupo19/admin* run `poetry run Flask run` to run the backend project.
- 3.2. Open another terminal type `Git bash` and from the path *grupo19/portal* execute `npm run dev`, which command will execute the front-end project locally. We can access the portal by pasting the URL returned by the indicated command into our browser.

---




	
	



