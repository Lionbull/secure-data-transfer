# Secure Data Transfer
This is a system for secure text transferring.

User inputs text and select the expiration time for the shared link. After that, receives a Key and URL that can be provided to the second party of the transfer. User opens the URL with a browser, types in the Key and gets the text from the database.

Only the text ciphertext is stored in the database, while key, iv, and tag are only displayed to the user once.

## Installation instructions

### Database

1. Install **PostgreSQL** to your machine
2. Enter the psql console by typing ```psql``` in terminal
3. Create a user and database (you can choose any database name, but one used during developement is named **SDT**)
    
    1. ```CREATE USER "SDT" with password 'SDT';```
    2. ```ALTER USER "SDT" CREATEDB;```
    3. ```CREATE DATABASE "SDT" owner "SDT";```

4. Exit psql console 

### Backend

You should have Python version **3.10.x** installed on your machine to run the backend.

Install dependencies using **Poetry** (Poetry installation instructions: https://python-poetry.org/docs/#installation):

1. Open the ```backend-sdt``` folder with your terminal
2. Run ```poetry install```
3. Enter virtual environment by running ```poetry shell```
4. Initialize database and migrations:
```
flask db init
flask db migrate -m "Create message table"
flask db upgrade
```

### Frontend

You need to have Node and npm installed.

1. Navigate to the ```frontend-sdt``` folder in your terminal
2. Run ```npm install```

## Running the dev version

1. Navigate to the ```backend-sdt``` folder
2. Enter the virtual environment by running ```poetry shell```
3. Start the server with ```python app.py``` (might by ```python3``` depending on the system)
4. **In separate terminal**, navigate to the ```frontend-sdt``` folder
5. Run ```npm run dev```

The server should run on **localhost:5000** and the frontend on **localhost:5173**. 

### Checking the database table
1. Enter the psql console by running ```psql````
2. Execute ```\c SDT``` (or whatever database name you used)
3. Execute ```SELECT * FROM message;```

## Considerations

This is a very plain version of the system, and it can be improved by various features.

Currently, the database doesn't erase expired messages, but for optimization, the expired messages should be deleted. This can be done in the production environment by scheduled checks for any expired messages and deleting them.

In the current version, it is not to hard to access user's encrypted messages if the user's internet traffic is recorded/tracked. Since the system is about security, the communication between frontend and the backend could be complicated further. 

If the purpose of the system is to be used in within some company's internal network, it could be useful to give more control to the system administrator. Currently, it might be complicated for the system administrator to decrypt any stored messages. Right now, the only way for doing it would be logging all the requests to the backend and decrypting one message at a time. Then, if message is expired, the only way accessing it would be changing the code in a way that it allows giving out expired messages as well. 