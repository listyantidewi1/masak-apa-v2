from flask import redirect, render_template, session
from functools import wraps

# handle login as member, adapted from CS50 finance
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# handle login as admin, adapted from CS50 finance
def login_admin_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != 'admin':
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# apology, adopted from cs50 finance
def apology(message, code=400):
    # komentar 1 baris
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    if session.get("role") == 'admin':
        return render_template("/admin/apology_admin.html", top=code, bottom=escape(message)), code
    else:
        return render_template("apology.html", top=code, bottom=escape(message)), code