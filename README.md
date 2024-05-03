# Cooking app for Cybersecurity final project
For this project I created a social media cooking app using flask and sqlite. 

## I have four html pages that can be used:

index.html: login page, if you don't have an account you can click register and it'll go to register.html

register.html: register page, can generate a password that fits the criteria, also if no username is inputted or username is taken displays an error. If the password doesn't meet the requirements an error is also displayed.

user_home: this is the main page jand a navbar is displayed as well as the user, the only navbar that works is for you and account

account.html: this is a form that allows the user to change their level. All users are automatically set at the basic user (level 0), but anyone can change


## I have a few python files that are used:

config.py contains my secret key 

db.py contains all the functions that allow me to update sqlite database by adding users checking accounts that log in, and changing levels

server.py is where all the app routes are and the flask app is mainly used here

password.py contains the hash password function, authenticates passwords and also checks if a password is valid


## CSS

I have only one css file that styles my website


# Running my program
To run the program in terminal run ' python server.py ' then click on the link outputted it should be localhost:8000
You will be prompted to login if you have an account and if not you can create your own
