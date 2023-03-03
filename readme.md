# Application Description

Hi! I'm your first Markdown file in **StackEdit**. If you want to learn about StackEdit, you can read me. If you want to play with Markdown, you can edit me. Once you have finished with me, you can create new files by opening the **file explorer** on the left corner of the navigation bar.


# Softwares/Modules/Libraries

To use `Masak Apa?`, you need to have the following software installed in your local computer. 

 1. Python 3.11 https://www.python.org/downloads/
 2. CS50 Library for Python https://cs50.readthedocs.io/libraries/cs50/python/.
 4. Flask-Session https://flask-session.readthedocs.io/en/latest/

## Install Python
Refer to this article to install and configure Python: https://realpython.com/installing-python/

## Install CS50 for Python
Use the following command in your terminal to install CS50 for Python:

    $  pip3  install  cs50
The command will also install all other modules used in this project. 

## Install Flask-Session

Use the following command in your terminal to install Flask-Session:

    $  pip  install  Flask-Session

# Clone and Launch The Application

 1. Navigate to the project repository using the following link:
https://github.com/listyantidewi1/masak-apa-v2
2. Open terminal window, and change directory to your own choice
3. Use the following command to clone the project:

    `$  git  clone  https://github.com/listyantidewi1/masak-apa-v2.git`
   
    Make sure the clone process is finished before proceeding to the next step. The following screenshot shows the completed clone.
    ![completed clone process](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/git-clone.png)
  4. Change directory to application directory.

		  $  cd  masak-apa-v2
4. Launch the application
	
	    $  flask  run
	The application run on http://127.0.0.1:5000/ by default. The following landing page should appear:
	![Application landing page](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/landing-page.png)
	
# Using The Application

## As Member
To use as member, you must first register for an account. Navigate to http://127.0.0.1:5000/register, and complete the registration process by providing username, name, password, and email correctly.  You will be logged-in automatically to the member dashboard after a successfull registration.

[insert dashboard screenshot here]

To search for recipe(s), check the ingredient(s) of your choice and then click `search`. You will be redirected to a result page displaying recipe(s) which use the ingredient(s) you provided.

[insert search recipe screenshot here]

[insert search result page screenshot here]

You can also browse for recipes, view latest recipes, and change your current password.
## As Administrator
You cannot register yourself as administrator. But to get a taste of what the application's administrator can do, navigate to login page via using the navbar, and use the following credential:

    username: dewi
    password: 12345
As an administrator, you can do the following:

 1. Add, view, edit, or delete recipes
 2. Add, view, edit, or delete ingredients
 3. Add, view, edit, or delete ingredient categories
 4. Add, view, edit, or delete recipe/ingredient origin
 5. Add, view, edit, or delete measurement units used by recipe
 6. Delete user(s)

### Work With Ingredient Categories
### Work With Ingredient/Recipe Origins
### Work With Measurement Units
### Work With Recipe Ingredients
### Work With Recipes
### Manage User(s)

# FAQs

[provide FAQS here]
