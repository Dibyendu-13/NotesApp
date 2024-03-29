**Note Taking Application**
This is a RESTful API for a simple note-taking application built using Django.

**Requirements**
Python 3.x
Django
Django REST Framework

**Installation**
Clone this repository to your local machine.
Navigate to the project directory.
Install the required dependencies using the following command:
Copy code
pip install -r requirements.txt
Run the migrations to set up the database:
Copy code
python manage.py migrate
Start the development server:
Copy code
python manage.py runserver
Usage
Endpoints
POST /signup: User registration. Allows users to create an account.
POST /login: User login. Allows users to log in to their account.
POST /notes/create: Create a new note.
GET /notes/{id}: Retrieve a specific note by its ID.
POST /notes/share: Share a note with other users.
PUT /notes/{id}: Update an existing note.
GET /notes/version-history/{id}: Get all the changes associated with the note.
Testing
You can test the API endpoints using tools like Postman or cURL. Make sure to authenticate users appropriately and handle errors gracefully.

**Sample cURL Commands**
User Registration:

bash
Copy code
curl -X POST http://localhost:8000/api/signup -d "username=test&email=test@example.com&password=123456"
User Login:

bash
Copy code
curl -X POST http://localhost:8000/api/login -d "username=test&password=123456"
Create a Note:

bash
Copy code
curl -X POST http://localhost:8000/api/notes/create -H "Authorization: Token <token>" -d "title=Sample&content=Sample content"
Retrieve a Note:

bash
Copy code
curl -X GET http://localhost:8000/api/notes/<id> -H "Authorization: Token <token>"
Share a Note:

bash
Copy code
curl -X POST http://localhost:8000/api/notes/share -H "Authorization: Token <token>" -d "note_id=<id>&users=user1,user2"
Update a Note:

bash
Copy code
curl -X PUT http://localhost:8000/api/notes/<id> -H "Authorization: Token <token>" -d "content=Updated content"
Get Note Version History:

bash
Copy code
curl -X GET http://localhost:8000/api/notes/version-history/<id> -H "Authorization: Token <token>"
