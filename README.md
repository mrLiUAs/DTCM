# DTCM
## Getting started
### set up MongoDB
install it on your computer. follow this [doc](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)

then, the default port should be "mongodb://localhost:27017"

install [MongeDB Compass](https://www.mongodb.com/products/tools/compass), this is a beautiful UI tool.
connect to "mongodb://localhost:27017"

add a new database, whatever you call it ("DTCM" suggested), and a example collection

then, click the collection you just created, then click "Collection > Import Data". import [the two json files](https://drive.google.com/drive/folders/1KvMet6hMvOzgV-peEV0Ec9-CzA_0BrT7) i wrote as example.

go to the collection "users" and change the email to yours

back to the project folder, create a .env file in the root folder in this project
add "MONGO_URI" and "MAILGUN_API" (the email server) in it
it should be something like this:
```
MONGO_URI=mongodb://localhost:27017/DTCM
MAILGUN_API=blahblahblah
```

### set up Python environment
open your terminal, go to the project root folder and run
```
pip install -r requirements.txt
```
wait until it's finished

### run
run
```
python main.py
```

## enjoy
### how to use
go to your Google Chrome or whatever, type the following url:
patient login: "127.0.0.1:3000/login"
doctor login: "127.0.0.1:3000/doctor_login"

the name of the patient is "jason", and the name of the doctor is "koala"

"sign up" is not supported

follow the instructions.
enjoy!

