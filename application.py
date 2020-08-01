import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

numppl=0

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get a list of all the distinct companies user has bought from
    complist = db.execute("SELECT DISTINCT company FROM purchases WHERE buyer_id = :thisid", thisid = session["user_id"])

    #if len(complist)==0:
        #return render
    # Get a list of how many shares from each company this user has
    sharelist = list()

    if len(complist) == 0:
        cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        return render_template("index.html", shares = sharelist, cash=cash[0]["cash"])

    grandtotal=0

    for company in complist:

        # Empty list
        thissum = list()

        # dict with "company":<company symbol>
        symboldict = db.execute("SELECT company FROM purchases WHERE company = :compname AND buyer_id = :thisid", compname = company["company"], thisid = session["user_id"])
        thissum.append(symboldict)

        # dict with "name":<company full name>
        namedict = {"name": lookup(symboldict[0]["company"])["name"]}
        thissum.append(namedict)

        # dict with "SUN(shares)":<number of shares>
        sharesdict = db.execute("SELECT SUM(shares) FROM purchases WHERE company = :compname AND buyer_id = :thisid AND bought=1", compname = company["company"], thisid = session["user_id"])
        thissum.append(sharesdict)

        # dict with "SUM(shares)":>number of sold shares>
        solddict = db.execute("SELECT SUM(shares) FROM purchases WHERE company = :compname AND buyer_id = :thisid AND bought=0", compname = company["company"], thisid = session["user_id"])

        if solddict[0]["SUM(shares)"] != None:
            thissum.append(solddict)
        else:
            solddict = [{"SUM(shares)": 0}]
            thissum.append(solddict)

        # dict with "price":<current price of company share>
        price = lookup(symboldict[0]["company"])["price"]
        pricedict = {"price": usd(price)}
        thissum.append(pricedict)

        # dict with "total":<total cost>
        totalcost = float((sharesdict[0]["SUM(shares)"] - solddict[0]["SUM(shares)"]) * price)
        totaldict = {"total": usd(totalcost)}

        if sharesdict[0]["SUM(shares)"] - solddict[0]["SUM(shares)"] == 0:
            continue
        thissum.append(totaldict)

        grandtotal += totalcost



        #thissum = db.execute("SELECT SUM(shares), company FROM purchases WHERE company = :compname", compname = company["company"])

        sharelist.append(thissum)

    #return render_template("index.html", shares = sharelist, fullname = lookup(thissum["company"])["name"], price = lookup(thissum["company"]))
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    grandtotal += cash[0]["cash"]
    dollarcash = usd(cash[0]["cash"])

    return render_template("index.html", shares = sharelist, cash=dollarcash, grandtotal=usd(grandtotal))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # If user is submitting the form
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        elif lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol", 400)

        elif int(request.form["shares"]) <= 0:
            return apology("please input a positive integer", 400)

        #db.execute("IF NOT EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'purchases') BEGIN CREATE TABLE purchases (purchase_id INTEGER, timestamp TEXT, buyer_id INTEGER, company TEXT, shares INTEGER, price NUMERIC, UNIQUE(purchase_id)); END")


        # Check if table of purchase records already exists
        #exists = db.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'purchases'")

        #if(exists==None):
            #db.execute("CREATE TABLE purchases (purchase_id INTEGER, timestamp TEXT, buyer_id INTEGER, company TEXT, shares INTEGER, price NUMERIC, UNIQUE(purchase_id));")

        now = datetime.datetime.now()
        thistime = now.strftime('%Y-%m-%d %H:%M:%S')

        thisid = session["user_id"]
        thiscompany = request.form.get("symbol")
        thisshares = request.form.get("shares")

        result = lookup(thiscompany)
        thisprice = result["price"]

        cost = float(thisshares) * thisprice
        thisuser = db.execute("SELECT cash FROM users WHERE id=:current", current=thisid)
        #balance = thisuser["cash"]

        if cost > thisuser[0]["cash"]:
            return apology("can't afford", 400)

        db.execute("INSERT INTO purchases (timestamp, buyer_id, company, shares, price, bought) VALUES(:timestamp, :buyer_id, :company, :shares, :price, :bought);", timestamp = thistime, buyer_id = thisid, company = thiscompany, shares = thisshares, price = thisprice, bought = True)
        db.execute("UPDATE users SET cash = :new WHERE id = :id", new = thisuser[0]["cash"]-cost, id = thisid)
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT * FROM purchases WHERE buyer_id=:thisuser", thisuser=session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User is submitting a form
    if request.method == "POST":

        symbolthis = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbolthis:
            return apology("missing symbol", 400)

        # Ensure the symbol is valid
        elif lookup(symbolthis) == None:
            return apology("invalid symbol", 400)

        # Show results of quote
        result = lookup(symbolthis)
        return render_template("quoted.html", name=result["name"], symbol=result["symbol"], price=result["price"])

    # User is on the form page
    else:
        return render_template("quote.html")

    #return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (they submitted a form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure passwork was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure that confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username is not already taken
        if len(rows) == 1:
            return apology("username is already taken", 403)

        # Ensure that the passwords match
        if request.form["password"] != request.form["confirmation"]:
            return apology("passwords must match", 403)

        #count = 0
        #count = db.execute("SELECT COUNT(*) FROM users;")
        #print(f"{count}")

        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))


        # Sign in this user
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username", username = request.form.get("username"))

        # Redirect user to home page
        return redirect("/login")

    else:
        return render_template("register.html")

    #return apology("TODO")


@app.route("/password", methods=["GET", "POST"])
@login_required
def changepass():
    """Change password"""

    if request.method == "POST":

        if not request.form.get("newpass"):
            return apology("must provide new password", 403)

        elif not request.form.get("newconfirm"):
            return apology("must provide confirmation", 403)

        elif request.form["newpass"] != request.form["newconfirm"]:
            return apology("passwords must match", 403)

        current_user = session["user_id"]

        rows = db.execute("SELECT * FROM users WHERE id = :username", username=current_user)
        password = request.form["newpass"]

        db.execute("UPDATE users SET hash=:newhash WHERE id = :username", newhash=generate_password_hash(password), username=current_user)

        return redirect("/")

    else:
        return render_template("changepass.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # when submitting form
    if request.method == "POST":

        # Ensure company symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)

        # Ensure number of shares was submitted
        elif not request.form.get("shares"):
            return apology("missing shares", 400)

        elif int(request.form["shares"]) <= 0:
            return apology("please input a positive integer", 400)

        # Ensure that user has the specified number of shares on hand
        wanttosell = request.form.get("shares")
        available = db.execute("SELECT SUM(shares) FROM purchases WHERE company=:company AND buyer_id=:user AND bought=1", company=request.form.get("symbol"), user=session["user_id"])
        na = db.execute("SELECT SUM(shares) FROM purchases WHERE company=:company AND buyer_id=:user AND bought=0", company=request.form.get("symbol"), user=session["user_id"])

        if na[0]["SUM(shares)"] == None:
            na = [{"SUM(shares)": 0}]

        if available[0]["SUM(shares)"]-na[0]["SUM(shares)"] < int(wanttosell):
            return apology("too many shares", 400)

        # inserting this transaction into the 'purchases table' (it's actually a sell though)

        now = datetime.datetime.now()
        thistime = now.strftime('%Y-%m-%d %H:%M:%S')

        thisid = session["user_id"]
        thiscompany = request.form.get("symbol")
        thisshares = request.form.get("shares")

        result = lookup(thiscompany)
        thisprice = result["price"]

        cost = float(thisshares) * thisprice
        thisuser = db.execute("SELECT cash FROM users WHERE id=:current", current=thisid)

        db.execute("INSERT INTO purchases (timestamp, buyer_id, company, shares, price, bought) VALUES(:timestamp, :buyer_id, :company, :shares, :price, :bought);", timestamp = thistime, buyer_id = thisid, company = thiscompany, shares = thisshares, price = thisprice, bought = False)
        db.execute("UPDATE users SET cash = :new WHERE id = :id", new = thisuser[0]["cash"]+cost, id = thisid)

        return redirect("/")
    # getting the submit page
    else:

        # get a list of all the companies this user has stocks of
        stocks = db.execute("SELECT DISTINCT company FROM purchases WHERE buyer_id=:id", id=session["user_id"])
        for stock in stocks:
            bought = db.execute("SELECT SUM(shares) FROM purchases WHERE company=:comp AND bought=1", comp=stock["company"])
            sold = db.execute("SELECT SUM(shares) FROM purchases WHERE company=:comp AND bought=0", comp=stock["company"])

            if sold[0]["SUM(shares)"] == None:
                sold = [{"SUM(shares)": 0}]

            if bought[0]["SUM(shares)"]-sold[0]["SUM(shares)"] == 0:
                stocks.remove(stock)
                #print(f"{bought[0]['SUM(shares)']-sold[0]['SUM(shares)']}")

        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
