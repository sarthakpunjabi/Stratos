In this particular app you can Create quiz from the best sourced questions online for checking the knowledge of the interviewer regarding any subject

To run the app clone the repo and run the following command . Create db.sqlite3 file . python3 manage.py collectstatic . python3 manage.py makemigrations . python3 manage.py migrate

Create a super user with following command . python3 manage.py createsuperuser . Fill the credentials and add superuser to database . Now add /admin to the current url to access the admin

Stratos eliminates the need for manual examinations, which saves time and effort.
Apart from that, in the existing system, reviewing the answer sheets after taking the test wastes the examiners' time; however, this application will check the right response and save the examiners' time, allowing them to carry out the examination in a more efficient fashion.
It is an application that was created with time restrictions in mind.
The quizzes can be accessed by entering the username and password that have been saved in the database.
New users can access the quizes by creating a new account.

The application is deployed on the following link:
https://quizforum.herokuapp.com
