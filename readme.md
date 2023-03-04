# 1. Application Description

We as mothers -and maybe it also happens to other mothers- every morning we often feel confused about what to serve for breakfast. When see ingredients we have in the refrigerator, we have no idea what to cook. At the end, we only often serve simple fried dishes, such as fried chicken, fried tofu, fried eggs or fried fish.

Link to the video: https://youtu.be/U0YIYFc36x8

Aim of the project:
1. Make ourself and others easier to find the right recipe according to the ingredients available in the refrigerator.
2. Reducing stress levels in the morning just because thinking about what to cook for breakfast. We believe, if the morning starts with enthusiasm, then we'll run all the day with enthusiasm too. And that can start from the kitchen. Vice versa

Creators of the project are 3 super moms :
1. Listyanti Dewi Astuti
2. Ni'mah Faadlilah
3. Wilujeng Jatiningsih

# 2. Softwares/Modules/Libraries

To use `Masak Apa?`, you need to have the following softwares installed in your local computer. 

 1. Python 3.11 https://www.python.org/downloads/
 2. PIP https://pip.pypa.io/en/stable/
 3. CS50 Library for Python https://cs50.readthedocs.io/libraries/cs50/python/.
 4. Flask-Session https://flask-session.readthedocs.io/en/latest/
 5. Git https://git-scm.com/doc

## 2.1 Install Python
Refer to this article to install and configure Python: https://realpython.com/installing-python/

## 2.2 Install PIP
Refer to this documentation to install PIP:
https://pip.pypa.io/en/stable/installation/

## 2.3 Install CS50 for Python
Use the following command in your terminal to install CS50 for Python:

    $  pip3 install cs50
The command will also install all other modules used in this project. 

## 2.4 Install Flask-Session

Use the following command in your terminal to install Flask-Session:

    $  pip3 install Flask-Session
## 2.5 Install and Configure Git
Refer to this documentation to install and configure Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

# 3. Clone and Launch The Application

 1. Navigate to the project repository using the following link:
https://github.com/listyantidewi1/masak-apa-v2
2. Open terminal window, and change directory to your own choice
3. Use the following command to clone the project:

    `$  git clone https://github.com/listyantidewi1/masak-apa-v2.git`
   
    Make sure the clone process is finished before proceeding to the next step. The following screenshot shows the completed clone.
    ![completed clone process](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/git-clone.png)
  4. Change directory to the application directory.

		  $  cd masak-apa-v2
4. Launch the application
	
	    $  flask run
	The application run on http://127.0.0.1:5000/ by default. The following landing page should appear:
	
	![Application landing page](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/landing-page.png)
	
# 4. Using The Application

## 4.1 As member
To use as member, you must first register for an account. Navigate to http://127.0.0.1:5000/register, and complete the registration process by providing username, name, password, and email correctly.  You will be logged-in automatically to the member dashboard after a successful registration.

![Member Dashboard](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/member-dashboard.png)

To search for recipe(s), check the ingredient(s) of your choice and then click `search`. You will be redirected to a result page displaying recipe(s) which use the ingredient(s) you provided.

![Input Ingredients](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/input-ingredients.png)

![\[Search result\]](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/search-result.png)

As a member, you can submit a recipe which will be subject to the administrator's approval.

![Submitted recipe](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/submitted-recipe.png)

To submit for recipe(s), you need to be logged in as member, and navigate to the `submit recipe` menu on the top navbar. You will be provided with a form, on wich you can feel the recipe's details, including ingredients, quantity and measurement units used, photo, instruction, and sources.

![Add new recipe](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/add-recipe-1.png)
![Add ingredients and instructions](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/add-ingredients.png)

You can also browse for recipes, view latest recipes, and change your current password.

![View recipe](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/view-recipe.png)
## 4.2 As administrator
You cannot register yourself as administrator. But to get a taste of what the application's administrator can do, navigate to login page, and use the following credential:

    username: dewi
    password: 12345
As an administrator, you can do the following:

 1. Add, view, edit, or delete recipes
 2. Add, view, edit, or delete ingredients
 3. Add, view, edit, or delete ingredient categories
 4. Add, view, edit, or delete recipe/ingredient origin
 5. Add, view, edit, or delete measurement units used by recipe
 6. Delete user(s)
 
 All the above features can simply be accessed using the navigation bar on top of the page.
 
![Admin Dashboard](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/admin-dashboard.png)

# 5. FAQs

 1. ****Q:** Do I need to register before searching for recipe?** *A: No, you can search for recipe and browse the recipe without creating an account. But in order to submit recipe(s), you need to register and logged in.*
 2. **Q: How to be an administrator?** ***A: You cannot register as an administrator. You will have to input your username, name, hashed password, email, and set the role as `admin` by yourself to the `users` table in the provided database. The best way is use the provided credential mentioned in section 4.2, and change the username and password* **
