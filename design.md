

# Overview
 `Masak Apa?` is a web-based application developed with Python, HTML, CSS, and JavaScript. The main modules used to develop `Masak Apa?` is Flask (https://palletsprojects.com/p/flask/) and CS50 Library for Python (https://cs50.readthedocs.io/libraries/cs50/python/), while the database engine used in `Masak Apa?` is SQLite (https://www.sqlite.org/index.html). The application is free for use and is available in https://github.com/listyantidewi1/masak-apa-v2.

Link to the video: https://youtu.be/U0YIYFc36x8

# Database Schema
The database is designed using relational model because for a single recipe, there maybe many ingredients needed. Also, a recipe or an ingredient has certain origin and category. Foreign key constraint is used to keep the database integrity.

`categories` table: to store each ingredient's category. It's related to `ingredients` table, referenced by the `id`.

    CREATE TABLE "categories" (
    	"id"	integer NOT NULL,
    	"category"	varchar NOT NULL,
    	"created_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"updated_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	PRIMARY KEY("id" AUTOINCREMENT)
    )
`ingredients` table: to store ingredients which are used as keywords and ingredients for the recipes. It is related to `origins` and `categories`, all referenced by the `id`.

    CREATE TABLE "ingredients" (
    	"id"	integer NOT NULL,
    	"image"	varchar,
    	"name"	varchar NOT NULL,
    	"origin_id"	integer NOT NULL,
    	"category_id"	integer NOT NULL,
    	"description"	text NOT NULL,
    	"created_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"updated_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"img_src"	TEXT,
    	PRIMARY KEY("id" AUTOINCREMENT),
    	FOREIGN KEY("category_id") REFERENCES "categories"("id") on delete cascade on update cascade,
    	FOREIGN KEY("origin_id") REFERENCES "origins"("id") on delete cascade on update cascade
    )

`origins` table: to store ingredient's and recipe's origin 

    CREATE TABLE "origins" (
    	"id"	integer NOT NULL,
    	"origin"	varchar NOT NULL,
    	"created_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"updated_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	PRIMARY KEY("id" AUTOINCREMENT)
    )

`units` table: to store measurement units. It is related to `recipe_ingredients` to provide measurement unit for each ingredient and the quantity of a recipe.

    CREATE TABLE "units" (
    	"id"	integer NOT NULL,
    	"name"	varchar NOT NULL,
    	"created_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"updated_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	PRIMARY KEY("id" AUTOINCREMENT)
    )
`recipes` table: to store details of recipes. It's related to `origins` to define the origins of the recipes.

    CREATE TABLE "recipes" (
    	"id"	integer NOT NULL,
    	"name"	TEXT NOT NULL,
    	"origin_id"	integer NOT NULL,
    	"image"	varchar,
    	"created_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"updated_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"description"	TEXT,
    	"img_src"	TEXT,
    	"recipe_src"	TEXT,
    	PRIMARY KEY("id" AUTOINCREMENT),
    	FOREIGN KEY("origin_id") REFERENCES "origins"("id") on delete cascade on update cascade
    )
    
`recipes_submitted` table: to store users' submitted recipes. `status` defines the status of the submitted recipe. `0` = in review, `1` = approved, `2` = rejected.

    CREATE TABLE "recipes_submitted" (
    	"id"	integer NOT NULL,
    	"name"	TEXT NOT NULL,
    	"origin_id"	integer NOT NULL,
    	"image"	varchar,
    	"created_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"updated_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"description"	TEXT,
    	"img_src"	TEXT,
    	"recipe_src"	TEXT,
    	"status"	integer DEFAULT 0,
    	"user_id"	INTEGER,
    	FOREIGN KEY("origin_id") REFERENCES "origins"("id") on delete cascade on update cascade,
    	PRIMARY KEY("id" AUTOINCREMENT)
    )

`recipe_ingredients` table: to store ingredients of recipes. It needs a separate table because a recipe will have more than one ingredients. Hence, one to many relationship.

    CREATE TABLE "recipe_ingredients" (
    	"id"	INTEGER NOT NULL,
    	"recipe_id"	INTEGER NOT NULL,
    	"ingredients_id"	TEXT NOT NULL,
    	"qty"	REAL NOT NULL,
    	"unit_id"	INTEGER NOT NULL,
    	PRIMARY KEY("id" AUTOINCREMENT),
    	FOREIGN KEY("recipe_id") REFERENCES "recipes"("id"),
    	FOREIGN KEY("ingredients_id") REFERENCES "ingredients"("id")
    )


`recipe_ingredients_submitted` table: to store ingredients for the submitted recipes. 


    CREATE TABLE "recipe_ingredients_submitted" (
    	"id"	INTEGER NOT NULL,
    	"recipe_id"	INTEGER NOT NULL,
    	"ingredients_id"	TEXT NOT NULL,
    	"qty"	REAL NOT NULL,
    	"unit_id"	TEXT NOT NULL,
    	FOREIGN KEY("recipe_id") REFERENCES "recipes_submitted"("id"),
    	PRIMARY KEY("id" AUTOINCREMENT),
    	FOREIGN KEY("ingredients_id") REFERENCES "ingredients"("id")
    )

`instructions` table: to store instructions of recipes. It's related to `recipes` referenced by the `id`.

    CREATE TABLE "instructions" (
    	"id"	INTEGER NOT NULL,
    	"recipe_id"	INTEGER NOT NULL,
    	"instructions"	TEXT NOT NULL,
    	PRIMARY KEY("id" AUTOINCREMENT),
    	FOREIGN KEY("recipe_id") REFERENCES "recipes"("id")
    )

`instructions_submitted` table: to store instructions for the users submitted recipes.

    CREATE TABLE "instructions_submitted" (
    	"id"	INTEGER NOT NULL,
    	"recipe_id"	INTEGER NOT NULL,
    	"instructions"	TEXT NOT NULL,
    	FOREIGN KEY("recipe_id") REFERENCES "recipes_submitted"("id"),
    	PRIMARY KEY("id" AUTOINCREMENT)
    )

`users` table: to store users credentials

    CREATE TABLE "users" (
    	"id"	integer NOT NULL,
    	"name"	varchar NOT NULL,
    	"email"	varchar NOT NULL,
    	"password"	varchar NOT NULL,
    	"created_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"updated_at"	datetime DEFAULT CURRENT_TIMESTAMP,
    	"username"	TEXT NOT NULL, role text,
    	PRIMARY KEY("id" AUTOINCREMENT)
    )

# Structure
![website structure](https://raw.githubusercontent.com/listyantidewi1/masak-apa-v2/main/screenshots/structure.png)

All the assets and resources used in this application are located inside the `static` folder. Meanwhile `templates` keep all the HTML files which renders results returned by `app.py`.
The backbone of `Masak Apa?` is in `app.py`, where records from the database are retrieved and modified, user inputs are processed, and results are rendered to the templates.
`helpers.py` provides several functions to help with multi-level authentication and the adaptation of the famous CS50's apology from `finance`.

