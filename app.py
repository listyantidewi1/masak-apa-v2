# import all the required modules and libraries
from cs50 import SQL
import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import login_required, login_admin_required, apology

# configure directory for uploaded files
UPLOAD_FOLDER = 'static/uploads'

# configure allowed file extensions to be uploaded
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///masakapa.sqlite")

# global variabel to store temporary recipe search result
search_result = []

# handle file upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# handle edit profile for member
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # get the logged in user id
    id = session["user_id"] 
    if request.method == "GET":
        # display the user profile
        user = db.execute("select * from users where id = ?", id)[0]
        return render_template("profile.html", id=id, user=user)
    elif request.method == "POST":
        # get the new password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # hash the password
        hash = generate_password_hash(password)
        # only update the profile if the password matches the confirmation
        if password == confirmation:
            # get all other data
            username = request.form.get("username")
            email = request.form.get("email")
            name = request.form.get("name")
            # if not changing password
            if not request.form.get("password"):
                db.execute("update users set username = ?, name=?, email = ? where id = ?", username, name, email, id)
                flash("Profile updated")
                return redirect("/admin/users")
            else:
                # if changing password
                db.execute("update users set password=?, username=?, name=?, email=? where id = ?", hash, username, name, email, id)
                flash("Profile updated")
                return redirect("/admin/users")
        else:
            flash("Profile update failed")
            return redirect("/admin/users")


# admin dashboard                       
@app.route("/admin")
@login_admin_required
def admin_dashboard():
    # get the user id
    id = session["user_id"]
    # count the number of users, recipes, ingredients, ingredient origins, categories, and units
    n_users = db.execute("select count(id) as n_users from users where role = 'member'")
    n_recipes = db.execute("select count(id) as n_recipes from instructions")
    n_ingr = db.execute("select count(id) as n_ingr from ingredients")
    n_ori = db.execute("select count(id) as n_ori from origins")
    n_cat = db.execute("select count(id) as n_cat from categories")
    n_unit = db.execute("select count(id) as n_unit from units")
    # get the user's name
    name = db.execute("select name from users where id = ?", id)
    return render_template("/admin/admin.html", users = n_users[0], recipes=n_recipes[0], ingredients = n_ingr[0], origins=n_ori[0], categories=n_cat[0], unit =n_unit[0], name=name[0])



''' handle CRUD for table: units
'''

# view all and add new unit
@app.route("/admin/units", methods=["GET", "POST"])
@login_admin_required
def units():
    if request.method == "GET":
        units = db.execute("select id, name from units")
        return render_template("/admin/units.html", units = units)
    elif request.method == "POST":
        if not request.form.get("unit"):
            return apology("Unit belum diisi?", 400)
        else:
            unit = request.form.get("unit")
            db.execute("insert into units (name) values(?)", unit)
            return redirect("/admin/units")

# edit unit
@app.route("/admin/units/<id>/edit", methods=["GET", "POST"])
@login_admin_required
def units_edit(id):
    if request.method == "GET":
        unit = db.execute("select * from units where id = ?", id)[0]
        print(unit)
        return render_template("/admin/units_edit.html", unit = unit)
    elif request.method == "POST":
        unit = request.form.get("unit")
        print(unit)
        db.execute("update units set name = ? where id = ?", unit, id)
        flash("The measurement unit has been successfully edited")
        return redirect("/admin/units")

# delete unit
@app.route("/admin/units/<id>/delete", methods=["GET"])
@login_admin_required
def units_delete(id):
    db.execute("delete from units where id = ?", id)
    flash("The measurement unit has been successfully deleted")
    return redirect("/admin/units")


'''CRUD for table: ingredients'''

# view all and add new ingredients
@app.route("/admin/ingredients", methods=["GET", "POST"])
@login_admin_required
def ingredients():
    if request.method == 'GET':
        # implementation of RDMS data retrieval from several related tables
        listCat = db.execute("select * from categories")
        listOri = db.execute("select * from origins")
        ingredients = db.execute("select ingredients.id, image, name, origin, category, description from ingredients inner join origins on ingredients.origin_id = origins.id inner join categories on ingredients.category_id = categories.id")
        return render_template("/admin/ingredients.html", ingredients = ingredients, listCats = listCat, listOris = listOri)
    elif request.method == "POST":
        if not request.form.get("name"):
            return apology("name belum diisi")
        elif not request.form.get("origin"):
            return apology("origin belum diisi")
        elif not request.form.get("category"):
            return apology("category belum diisi")
        elif not request.form.get("description"):
            return apology("description belum diisi")
        name = request.form.get("name")
        origin = request.form.get("origin")
        category = request.form.get("category")
        img_src = request.form.get("img_src")
        f = request.files['file']
        # upload file
        if f.filename == '':
            return apology('No selected file')
        description = request.form.get("description")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.execute("insert into ingredients(image, name, origin_id, category_id, description, img_src) values(?,?,?,?,?,?)", filename, name, origin, category, description, img_src)
            return redirect("/admin/ingredients")
        else:
            return apology("pilih file dulu")

# view an ingredient
@app.route("/admin/ingredients/<id>/view", methods=["GET"])
@login_admin_required
def admin_view_ingredient(id):
    # retrieve the ingredient from ingredient table and the ingredient origin from origins table
    ingredient = db.execute("select * from ingredients where id = ?",id)[0]
    origin = db.execute("select origin from origins inner join ingredients on origins.id = ingredients.origin_id where ingredients.id = ?", id)[0]
    return render_template("/admin/admin_view_ingredient.html", ingredient=ingredient, origin=origin)

# edit an ingredient
@app.route("/admin/ingredients/<id>/edit", methods=["GET", "POST"])
@login_admin_required
def ingredients_edit(id):
    if request.method == "GET":
        listCat = db.execute("select * from categories")
        listOri = db.execute("select * from origins")
        ingredients = db.execute("select ingredients.id, image, name, origin, category, ingredients.description from ingredients inner join origins on ingredients.origin_id = origins.id inner join categories on ingredients.category_id = categories.id where ingredients.id = ?", id)[0]
        print(listCat, listOri, ingredients)
        return render_template("/admin/ingredients_edit.html", ingredients = ingredients, listCats = listCat, listOris = listOri)
    elif request.method == "POST":
        if not request.form.get("name"):
            return apology("name belum diisi")
        elif not request.form.get("origin"):
            return apology("origin belum diisi")
        elif not request.form.get("category"):
            return apology("category belum diisi")
        elif not request.form.get("description"):
            return apology("description belum diisi")
        name = request.form.get("name")
        origin = request.form.get("origin")
        category = request.form.get("category")
        f = request.files['file']
        print(f)
        if f.filename == '':
            return apology('No selected file')
        description = request.form.get("description")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.execute("update ingredients set image = ?, name = ?, origin_id = ?, category_id = ?, description = ? where id = ?", filename, name, origin, category, description, id)
            flash("The ingredient has been sucessfully edited")
            return redirect("/admin/ingredients")
        else:
            return apology("pilih file dulu")

# delete an ingredient
@app.route("/admin/ingredients/<id>/delete", methods=["GET"])
@login_admin_required
def ingredient_delete(id):
    db.execute("delete from ingredients where id = ?", id)
    flash("The ingredient has been successfully deleted")
    return redirect("/admin/ingredients")


'''CRUD for table: origins'''

# view all and add new ingredient origin
@app.route("/admin/origins", methods=["GET", "POST"])
@login_admin_required
def origins():
    if request.method=="GET":
        origins = db.execute("select id, origin from origins")
        return render_template("/admin/origins.html", origins = origins)
    elif request.method=="POST":
        if not request.form.get("origin"):
            return apology("origin belum diisi", 400)
        else:
            neworigin = request.form.get("origin")
            db.execute("insert into origins (origin) values(?)", neworigin)
            return redirect("/admin/origins")

# edit an ingredient origin
@app.route("/admin/origins/<id>/edit", methods=["GET", "POST"])
@login_admin_required
def origins_edit(id):
    if request.method == "GET":
        origin = db.execute("select * from origins where id = ?", id)[0]
        print(origin)
        return render_template("/admin/origins_edit.html", origins=origin)
    elif request.method == "POST":
        origin = request.form.get("origin")
        print(origin)
        db.execute("update origins set origin = ? where id = ?", origin, id)
        flash("The ingredient origin has been sucessfully edited")
        return redirect("/admin/origins")

# delete an ingredient origin
@app.route("/admin/origins/<id>/delete", methods=["GET"])
@login_admin_required
def origins_delete(id):
    db.execute("delete from origins where id = ?", id)
    flash("The ingredient origin has been successfully deleted")
    return redirect("/admin/origins")


'''CRUD for table: categories'''

# view all and add new category
@app.route("/admin/categories", methods=["GET", "POST"])
@login_admin_required
def categories():
    if request.method=="GET":
        cat = db.execute("select id, category from categories")
        return render_template("/admin/categories.html", categories=cat)
    elif request.method=="POST":
        if not request.form.get("category"):
            return apology("Category belum diisi?", 400)
        else:
            newcat = request.form.get("category")
            db.execute("insert into categories (category) values (?)", newcat)
            return redirect("/admin/categories")

# edit a category
@app.route("/admin/categories/<id>/edit", methods=["GET", "POST"])
@login_admin_required
def categories_edit(id):
    if request.method == "GET":
        cat = db.execute("select * from categories where id = ?", id)[0]
        print(cat)
        return render_template("/admin/categories_edit.html", categories=cat)
    elif request.method == "POST":
        category = request.form.get("category")
        print(category)
        db.execute("update categories set category = ? where id = ?", category, id)
        flash("The category has been successfully edited")
        return redirect("/admin/categories")

# delete a category
@app.route("/admin/categories/<id>/delete", methods=["GET"])
@login_admin_required
def categories_delete(id):
    db.execute("delete from categories where id = ?", id)
    flash("The category has been successfully deleted")
    return redirect("/admin/categories")


'''CRUD for recipes'''

# view all recipes
@app.route("/admin/recipes", methods=["GET"])
@login_admin_required
def show_recipes_admin():
    if request.method == 'GET':
        recipes = db.execute("select recipes.id, recipes.name as recipe_name, recipes.image, recipes.description, recipe_ingredients.qty, instructions.instructions, units.name as unit_name from recipes inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id inner join units on recipe_ingredients.unit_id = units.id inner join instructions on recipes.id = instructions.recipe_id group by recipes.id order by recipes.created_at desc")
        return render_template("/admin/show_recipes_admin.html", recipes = recipes)


# add a new recipe
@app.route("/admin/recipe/add/", methods=["GET", "POST"])
@login_admin_required
def add_recipes_2():
    if request.method == "GET":
        ingredients = db.execute("SELECT * from ingredients order by name ASC")
        units = db.execute("select * from units order by name ASC")
        origins = db.execute("SELECT * from origins order by origin ASC")
        return render_template('/admin/add_recipe_admin.html', ingredients=ingredients, units=units, origins=origins)
    elif request.method == "POST":
        # retrieve the inputted ingredients as a list
        ingredients = request.form.getlist("ingredients")
        # remove empty ingredients
        while("" in ingredients):
            ingredients.remove("")

        # retrieve quantities as a list    
        quantities = request.form.getlist("quantity")
        # remove empty quantities
        while("" in quantities):
            quantities.remove("")

        # retrieve units as a list
        units = request.form.getlist("unit")
        # remove empty units
        while("" in units):
            units.remove("")

        # retrieve all other inputs
        instruction = request.form.get("instruction")
        name = request.form.get("name")
        origin = request.form.get("origin")
        description = request.form.get("description")
        img_src = request.form.get("img_src")
        recipe_src = request.form.get("recipe_src")
        f = request.files['file']
        if f.filename == '':
            return apology("No selected file")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # insert recipe data into recipe table
            db.execute("insert into recipes(name, origin_id, image, description, img_src, recipe_src) values(?,?,?,?,?,?)", name, origin, filename, description, img_src, recipe_src)
            current_recipe = db.execute("select id from recipes order by id desc limit 1")[0]
            print(current_recipe['id'])
            current_recipe_id = str(current_recipe['id'])
            # insert ingredients into recipe_ingredients table
            for (ingredient, quantity, unit) in zip(ingredients, quantities, units):
                db.execute("insert into recipe_ingredients(recipe_id, ingredients_id, qty, unit_id) values(?,?,?,?)",current_recipe_id, ingredient, quantity, unit)
            db.execute("insert into instructions(recipe_id, instructions) values(?,?)", current_recipe_id, instruction)
            return redirect('/admin/recipe/show/'+current_recipe_id)
        else:
            return apology("pilih file dulu")
        

# show a recipe detail
@app.route("/admin/recipe/show/<id>", methods=["GET"])
@login_admin_required
def show_recipe_admin(id):
    recipe = db.execute("select * from recipes where id = ?", id)[0]
    ingredients = db.execute("select * from recipe_ingredients inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id where recipe_id = ?", id)
    instructions = db.execute("select * from instructions where recipe_id = ?", id)[0]
    units = db.execute("select units.name from units inner join recipe_ingredients on units.id = recipe_ingredients.unit_id where recipe_id = ?", id)
    origin = db.execute("select origins.origin from origins inner join recipes on origins.id = recipes.origin_id where recipes.id = ?", id)[0]
    print(units)
    full_recipe = db.execute("select recipes.name as recipename, recipes.description, recipes.image, recipes.recipe_src, recipes.img_src as imgsrc, origins.origin, recipe_ingredients.qty, instructions.instructions, units.name as unitname, ingredients.name as ingredientname from recipes inner join origins on recipes.origin_id = origins.id inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join instructions on recipes.id = instructions.recipe_id inner join units on recipe_ingredients.unit_id = units.id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id where recipes.id = ?", id)
    source = db.execute("select img_src, recipe_src from recipes where id = ?",id)[0]
    return render_template("/admin/show_recipe_admin.html", recipe=recipe, ingredients=ingredients, instructions=instructions, units=units, origin=origin, full_recipe=full_recipe, source=source)


# show a submitted recipe detail
@app.route("/admin/recipe/show/submitted/<id>", methods=["GET"])
@login_admin_required
def show_submitted_recipe_admin(id):
    recipe = db.execute("select * from recipes_submitted where id = ?", id)[0]
    ingredients = db.execute("select * from recipe_ingredients_submitted inner join ingredients on recipe_ingredients_submitted.ingredients_id = ingredients.id where recipe_id = ?", id)
    instructions = db.execute("select * from instructions_submitted where recipe_id = ?", id)[0]
    units = db.execute("select units.name from units inner join recipe_ingredients_submitted on units.id = recipe_ingredients_submitted.unit_id where recipe_id = ?", id)
    origin = db.execute("select origins.origin from origins inner join recipes_submitted on origins.id = recipes_submitted.origin_id where recipes_submitted.id = ?", id)[0]
    print(units)
    full_recipe = db.execute("select recipes_submitted.name as recipename, recipes_submitted.description, recipes_submitted.image, recipes_submitted.recipe_src, recipes_submitted.img_src as imgsrc, origins.origin, recipe_ingredients_submitted.qty, instructions_submitted.instructions, units.name as unitname, ingredients.name as ingredientname from recipes_submitted inner join origins on recipes_submitted.origin_id = origins.id inner join recipe_ingredients_submitted on recipes_submitted.id = recipe_ingredients_submitted.recipe_id inner join instructions_submitted on recipes_submitted.id = instructions_submitted.recipe_id inner join units on recipe_ingredients_submitted.unit_id = units.id inner join ingredients on recipe_ingredients_submitted.ingredients_id = ingredients.id where recipes_submitted.id = ?", id)
    source = db.execute("select img_src, recipe_src from recipes_submitted where id = ?",id)[0]
    return render_template("/admin/show_recipe_admin.html", recipe=recipe, ingredients=ingredients, instructions=instructions, units=units, origin=origin, full_recipe=full_recipe, source=source)


# edit recipe as admin
@app.route("/admin/recipe/<id>/edit", methods=["GET","POST"])
@login_admin_required
def recipe_edit(id):
    if request.method == "GET":
        origins = db.execute("select * from origins")
        recipe = db.execute("select * from recipes where id = ?", id)[0]
        ingredients = db.execute("select * from ingredients order by name asc")
        instruction = db.execute("select * from instructions where recipe_id = ?", id)[0]
        units = db.execute("select * from units order by name asc")
        return render_template("/admin/edit_recipe.html", origins=origins, recipe=recipe, ingredients=ingredients, instruction=instruction, units=units)
    elif request.method == "POST":

        # delete ingredients first to bypass foreign key constraints
        db.execute("delete from recipe_ingredients where recipe_id = ?", id)
        if not request.form.get("name"):
            return apology("")
        elif not request.form.get("origin"):
            return apology("")

        name = request.form.get("name")
        origin = request.form.get("origin")
        description = request.form.get("description")
        f = request.files['file']
        if f.filename == '':
            return apology("")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # update recipe data
            db.execute("update recipes set name = ?, origin_id = ?, description = ?, image = ? where recipes.id = ?", name, origin, description, filename, id)
        
        # get list of ingredients and remove empty ones
        ingredients = request.form.getlist("ingredients") 
        while("" in ingredients):
            ingredients.remove("")

        # get list of quantities and remove empty ones    
        quantities = request.form.getlist("quantity")
        while("" in quantities):
            quantities.remove("")

        # get list of units and remove empty ones 
        units = request.form.getlist("unit")
        while("" in units):
            units.remove("")

        # get instructions
        instruction = request.form.get("instruction")

        # insert edited ingredients into the table
        for (ingredient, quantity, unit) in zip(ingredients, quantities, units):
            db.execute("insert into recipe_ingredients(recipe_id, ingredients_id, qty, unit_id) values(?,?,?,?)",id, ingredient, quantity, unit)

        # update the instructions
        db.execute("update instructions set instructions = ? where recipe_id = ?", instruction, id)
        return redirect('/admin/recipe/show/'+id)

# delete recipe as admin
@app.route("/admin/recipe/<id>/delete", methods=["GET"])
@login_admin_required
def recipe_delete(id):
    db.execute("delete from recipe_ingredients where recipe_id=?", id)
    db.execute("delete from instructions where recipe_id=?", id)
    db.execute("delete from recipes where id=?", id)
    return redirect("/admin/recipes")

# view all submitted recipes as admin
@app.route("/admin/recipes/submitted", methods=["GET"])
@login_admin_required
def show_recipes_submitted_admin():
    if request.method == 'GET':
        recipes = db.execute("select recipes_submitted.status, recipes_submitted.id, recipes_submitted.name as recipe_name, recipes_submitted.image, recipes_submitted.description, recipe_ingredients_submitted.qty, instructions_submitted.instructions, units.name as unit_name from recipes_submitted inner join recipe_ingredients_submitted on recipes_submitted.id = recipe_ingredients_submitted.recipe_id inner join ingredients on recipe_ingredients_submitted.ingredients_id = ingredients.id inner join units on recipe_ingredients_submitted.unit_id = units.id inner join instructions_submitted on recipes_submitted.id = instructions_submitted.recipe_id group by recipes_submitted.id order by recipes_submitted.created_at desc")
        return render_template("/admin/show_submitted_recipes_admin.html", recipes = recipes)


# approve a submitted recipe as admin
@app.route("/admin/recipe/<id>/approve",  methods=["GET"])
@login_admin_required
def approve_recipe(id):
    submitted_recipe = db.execute("SELECT * FROM recipes_submitted WHERE id = ?", id)[0]
    submitted_ingredients = db.execute("SELECT * FROM recipe_ingredients_submitted WHERE recipe_id = ?", id)
    submitted_instruction = db.execute("Select * from instructions_submitted WHERE recipe_id = ?", id)[0]
    db.execute("update recipes_submitted set status = 1 where id = ?", id)
    db.execute("insert into recipes(name, origin_id, image, description, img_src, recipe_src) values(?,?,?,?,?,?)", submitted_recipe['name'], submitted_recipe['origin_id'], submitted_recipe['image'], submitted_recipe['description'], submitted_recipe['img_src'], submitted_recipe['recipe_src'])
    current_recipe = db.execute("select id from recipes order by id desc limit 1")[0]
    print(current_recipe['id'])
    current_recipe_id = str(current_recipe['id'])
    for i in submitted_ingredients:
        db.execute("insert into recipe_ingredients(recipe_id, ingredients_id, qty, unit_id) values(?,?,?,?)", current_recipe_id, i['ingredients_id'], i['qty'], i['unit_id'])
    db.execute("insert into instructions(recipe_id, instructions) values(?,?)", current_recipe_id, submitted_instruction['instructions'])
    flash("Recipe has been approved successfully")
    return redirect("/admin/recipes/submitted")


# reject a submitted recipe as admin
@app.route("/admin/recipe/<id>/reject",  methods=["GET"])
@login_admin_required
def reject_recipe(id):
    db.execute("update recipes_submitted set status = 2 where id = ?", id)
    flash("Recipe has been rejected successfully")
    return redirect("/admin/recipes/submitted")


# view all members and edit profile as admin
@app.route("/admin/users", methods=["GET", "POST"])
@login_admin_required
def users():
    user_id = session["user_id"]
    if request.method == "GET":
        users = db.execute("select id, name, username, email from users where role = 'member'")
        admins = db.execute("select id, name, email from users where role = 'admin'")
        my_account = db.execute ("select * from users where id = ?", user_id)[0]
        return render_template("/admin/users.html", users = users, admins=admins, my_account=my_account)
    elif request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)
        if password == confirmation:
            username = request.form.get("username")
            email = request.form.get("email")
            name = request.form.get("name")
            db.execute("update users set password=?, username=?, name=?, email=? where id = ?", hash, username, name, email, user_id)
            flash("Profile updated")
            return redirect("/admin/users")
        else:
            flash("Profile update failed")
            return redirect("/admin/users")


'''functions for members and public'''

# recipe search for public
@app.route("/recipe/search", methods=["GET", "POST"])
def recipe_search():
    global search_result
    if request.method == "GET":
        ingredients = db.execute("select * from ingredients")
        # get latest recipes
        latest_recipes = db.execute("select recipes.id, recipes.name as recipe_name, recipes.image, recipes.description, recipe_ingredients.qty, instructions.instructions, units.name as unit_name from recipes inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id inner join units on recipe_ingredients.unit_id = units.id inner join instructions on recipes.id = instructions.recipe_id group by recipes.id order by recipes.created_at desc limit 4")
        search_result.clear()
        return render_template("search_recipes.html", ingredients=ingredients, latest_recipes=latest_recipes)
    elif request.method == "POST":
        if not request.form.get("ingredients"):
            return apology("pilih dulu minimal 1 ingredients")
        keywords = request.form.getlist("ingredients")
  
        # search for recipes according to ingredients
        where_clause = ""
        for i in range(1, len(keywords)):
            where_clause += " or recipe_ingredients.ingredients_id = " + keywords[i]
        where_clause = "where recipe_ingredients.ingredients_id = " +keywords[0] + where_clause
       
       # retrieving results
        results = db.execute("select recipes.id, recipes.name as recipe_name, recipes.image, recipes.description, recipe_ingredients.qty, instructions.instructions, units.name as unit_name from recipes inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id inner join units on recipe_ingredients.unit_id = units.id inner join instructions on recipes.id = instructions.recipe_id "+ where_clause + " group by recipes.id")

        # handle empty result
        if not results:
            flash("No recipes found")
            return redirect("/recipe/search")
        
        # render results
        search_result = results
        prompt ="Here are some recipes for you!"
        return render_template("search_result.html", results=results, prompt=prompt)


# member dashboard
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard():
    global search_result
    id = session["user_id"]
    name = db.execute("select name from users where id = ?", id)
    if request.method == "GET":
        ingredients = db.execute("select * from ingredients")
        latest_recipes = db.execute("select recipes.id, recipes.name as recipe_name, recipes.image, recipes.description, recipe_ingredients.qty, instructions.instructions, units.name as unit_name from recipes inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id inner join units on recipe_ingredients.unit_id = units.id inner join instructions on recipes.id = instructions.recipe_id group by recipes.id order by recipes.created_at desc limit 4")
        search_result.clear()
        return render_template("dashboard.html", name=name[0], ingredients=ingredients, latest_recipes=latest_recipes)
    elif request.method == "POST":
        if not request.form.get("ingredients"):
            return apology("pilih dulu minimal 1 ingredients")
        keywords = request.form.getlist("ingredients")
   
        # handle recipe search from dashboard
        where_clause = ""
        for i in range(1, len(keywords)):
            where_clause += " or recipe_ingredients.ingredients_id = " + keywords[i]
        where_clause = "where recipe_ingredients.ingredients_id = " +keywords[0] + where_clause
        print(where_clause)

        results = db.execute("select recipes.id, recipes.name as recipe_name, recipes.image, recipes.description, recipe_ingredients.qty, instructions.instructions, units.name as unit_name from recipes inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id inner join units on recipe_ingredients.unit_id = units.id inner join instructions on recipes.id = instructions.recipe_id "+ where_clause + " group by recipes.id")
            
        # handle empty results
        if not results:
            flash("No recipes found")
            return redirect("/dashboard")
        
        # render search results
        search_result = results
        prompt ="Here are some recipes for you!"
        return render_template("search_result.html", results=results, prompt=prompt)


# show search results
@app.route('/show_search_results', methods=['GET', 'POST'])
def show_search_results():
    prompt ="Here are some recipes for you!"
    return render_template("search_result.html", results=search_result, prompt=prompt)

# show a recipe for public
@app.route("/recipe/show/<id>", methods=["GET"])
def show_recipe(id):
    recipe = db.execute("select * from recipes where id = ?", id)[0]
    ingredients = db.execute("select * from recipe_ingredients inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id where recipe_id = ?", id)
    instructions = db.execute("select * from instructions where recipe_id = ?", id)[0]
    units = db.execute("select units.name from units inner join recipe_ingredients on units.id = recipe_ingredients.unit_id where recipe_id = ?", id)
    origin = db.execute("select origins.origin from origins inner join recipes on origins.id = recipes.origin_id where recipes.id = ?", id)[0]
    full_recipe = db.execute("select recipes.name as recipename, recipes.description, recipes.image, recipes.img_src as imgsrc, recipes.recipe_src, origins.origin, recipe_ingredients.qty, instructions.instructions, units.name as unitname, ingredients.name as ingredientname from recipes inner join origins on recipes.origin_id = origins.id inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join instructions on recipes.id = instructions.recipe_id inner join units on recipe_ingredients.unit_id = units.id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id where recipes.id = ?", id)
    source = db.execute("select img_src, recipe_src from recipes where id = ?",id)[0]
    print(units)
    is_search = len(search_result)
    return render_template("show_recipe.html", is_search=is_search, results=search_result, recipe=recipe, ingredients=ingredients, instructions=instructions, units=units, origin = origin, full_recipe = full_recipe, source = source)


# show a submitted recipe detail for a member
@app.route("/recipe/submitted/show/<id>", methods=["GET"])
@login_required
def show_submitted_recipe(id):
    recipe = db.execute("select * from recipes_submitted where id = ?", id)[0]
    ingredients = db.execute("select * from recipe_ingredients_submitted inner join ingredients on recipe_ingredients_submitted.ingredients_id = ingredients.id where recipe_id = ?", id)
    instructions = db.execute("select * from instructions_submitted where recipe_id = ?", id)[0]
    units = db.execute("select units.name from units inner join recipe_ingredients_submitted on units.id = recipe_ingredients_submitted.unit_id where recipe_id = ?", id)
    origin = db.execute("select origins.origin from origins inner join recipes_submitted on origins.id = recipes_submitted.origin_id where recipes_submitted.id = ?", id)[0]
    full_recipe = db.execute("select recipes_submitted.name as recipename, recipes_submitted.description, recipes_submitted.image, recipes_submitted.img_src as imgsrc, recipes_submitted.recipe_src, origins.origin, recipe_ingredients_submitted.qty, instructions_submitted.instructions, units.name as unitname, ingredients.name as ingredientname from recipes_submitted inner join origins on recipes_submitted.origin_id = origins.id inner join recipe_ingredients_submitted on recipes_submitted.id = recipe_ingredients_submitted.recipe_id inner join instructions_submitted on recipes_submitted.id = instructions_submitted.recipe_id inner join units on recipe_ingredients_submitted.unit_id = units.id inner join ingredients on recipe_ingredients_submitted.ingredients_id = ingredients.id where recipes_submitted.id = ?", id)
    source = db.execute("select img_src, recipe_src from recipes_submitted where id = ?",id)[0]
    print(units)
    is_search = len(search_result)
    flash("You have successfully submitted a recipe! We will get into it soon!")
    return render_template("show_recipe.html", is_search=is_search, results=search_result, recipe=recipe, ingredients=ingredients, instructions=instructions, units=units, origin = origin, full_recipe = full_recipe, source = source)


# show all recipe for public
@app.route("/recipe/show/all", methods=["GET", "POST"])
def show_recipes():
    global search_result
    if request.method == "GET":
        search_result.clear()
        recipes = db.execute("select recipes.id, recipes.name as recipe_name, recipes.image, recipes.description, recipe_ingredients.qty, instructions.instructions, units.name as unit_name from recipes inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id inner join units on recipe_ingredients.unit_id = units.id inner join instructions on recipes.id = instructions.recipe_id group by recipes.id order by recipes.created_at desc")
        return render_template("show_recipes.html", recipes=recipes)


# show all submitted recipes 
@app.route("/recipe/show/submitted", methods=["GET"])
@login_required
def show_submitted_recipes():
    user_id = session["user_id"]
    global search_result
    if request.method == "GET":
        search_result.clear()
        recipes = db.execute("select recipes_submitted.status, recipes_submitted.id, recipes_submitted.name as recipe_name, recipes_submitted.image, recipes_submitted.description, recipe_ingredients_submitted.qty, instructions_submitted.instructions, units.name as unit_name from recipes_submitted inner join recipe_ingredients_submitted on recipes_submitted.id = recipe_ingredients_submitted.recipe_id inner join ingredients on recipe_ingredients_submitted.ingredients_id = ingredients.id inner join units on recipe_ingredients_submitted.unit_id = units.id inner join instructions_submitted on recipes_submitted.id = instructions_submitted.recipe_id where recipes_submitted.user_id = ? group by recipes_submitted.id order by recipes_submitted.created_at desc", user_id)
        print(recipes)
        return render_template("show_submitted_recipes.html", recipes=recipes)
    

# handle submit recipe for members
@app.route("/recipe/submit", methods=["GET", "POST"])
@login_required
def submit_recipe():
    user_id = session["user_id"]
    if request.method == "GET":
        ingredients = db.execute("SELECT * from ingredients order by name ASC")
        units = db.execute("select * from units order by name ASC")
        origins = db.execute("SELECT * from origins order by origin ASC")
        return render_template('add_recipe.html', ingredients=ingredients, units=units, origins=origins)
    elif request.method == "POST":
        ingredients = request.form.getlist("ingredients") #this will return a list / dictionary

        # removing empty data
        while("" in ingredients):
            ingredients.remove("")
            
        quantities = request.form.getlist("quantity")
        print(quantities)
        while("" in quantities):
            quantities.remove("")

        units = request.form.getlist("unit")
        print(units)
        while("" in units):
            units.remove("")

        instruction = request.form.get("instruction")
        name = request.form.get("name")
        origin = request.form.get("origin")
        description = request.form.get("description")
        img_src = request.form.get("img_src")
        recipe_src = request.form.get("recipe_src")
        f = request.files['file']
        if f.filename == '':
            return apology("No selected file")
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.execute("insert into recipes_submitted(name, origin_id, image, description, img_src, recipe_src, user_id) values(?,?,?,?,?,?,?)", name, origin, filename, description, img_src, recipe_src, user_id)
            current_recipe = db.execute("select id from recipes_submitted order by id desc limit 1")[0]
            print(current_recipe['id'])
            current_recipe_id = str(current_recipe['id'])
            for (ingredient, quantity, unit) in zip(ingredients, quantities, units):
                db.execute("insert into recipe_ingredients_submitted(recipe_id, ingredients_id, qty, unit_id) values(?,?,?,?)",current_recipe_id, ingredient, quantity, unit)
            db.execute("insert into instructions_submitted(recipe_id, instructions) values(?,?)", current_recipe_id, instruction)
            return redirect('/recipe/submitted/show/'+current_recipe_id)
        else:
            return apology("pilih file dulu")


# render landing page    
@app.route('/', methods=["GET"])
def landingpage():
    latest_recipes = db.execute("select recipes.id, recipes.name as recipe_name, recipes.image, recipes.description, recipe_ingredients.qty, instructions.instructions, units.name as unit_name from recipes inner join recipe_ingredients on recipes.id = recipe_ingredients.recipe_id inner join ingredients on recipe_ingredients.ingredients_id = ingredients.id inner join units on recipe_ingredients.unit_id = units.id inner join instructions on recipes.id = instructions.recipe_id group by recipes.id order by recipes.created_at desc limit 4")
    return render_template("index.html", latest_recipes=latest_recipes)


# register a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method=="POST":
        if not request.form.get("username"):
            return apology("belum ngisi username?", 400)
        elif not request.form.get("password"):
            return apology("belum ngisi password?", 400)
        elif not request.form.get("email"):
            return apology("belum ngisi email?", 400)
        elif not request.form.get("name"):
            return apology("belum ngisi nama?", 400)

        rows = db.execute("select * from users where username = ? or email = ?", request.form.get("username"), request.form.get("email"))

        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        email = request.form.get("email")
        password_repeat = request.form.get("confirmation")

        hash = generate_password_hash(password)
        if len(rows) == 1:
            return apology("Gak pilih username yang lain?")
        if password == password_repeat:
            db.execute("insert into users (username, name, password, email, role) values (?, ?, ?, ?, ?)", username, name, hash, email, "member")

            registered_user = db.execute("select * from users where username = ?", username)
            session["user_id"] = registered_user[0]["id"]
            session["role"] = registered_user[0]["role"]
            session["name"] = registered_user[0]["name"]
            flash("You were sucessfully registered")
            return redirect("/dashboard")
        else:
            return apology("Konfirmasi password nggak sama?", 400)
    else:
        return render_template("register.html")


# login user
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("belum ngisi username?", 403)
        elif not request.form.get("password"):
            return apology("belum ngisi password", 403)
        rows = db.execute("SELECT * from users where username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("Password/username salah?", 403)
        elif len(rows) == 1:
            # handle multi level authentication
            if rows[0]["role"] == "member":
                session["user_id"] = rows[0]["id"]
                session["role"] = rows[0]["role"]
                session["name"] = rows[0]["name"]
                flash("You were sucessfully logged in")
                return redirect("/dashboard")
            elif rows[0]["role"] == "admin":
                session["user_id"] = rows[0]["id"]
                session["role"] = rows[0]["role"]
                session["name"] = rows[0]["name"]
                flash("You were sucessfully logged in")
                return redirect("/admin")
            else:
                return render_template("login.html")
    else:
        return render_template("login.html")

# logout
@app.route("/logout")
def logout():
    session.clear
    return redirect("/login")