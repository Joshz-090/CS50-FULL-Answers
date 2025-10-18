import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get user's stocks and shares
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"]
    )

    # Get user's cash balance
    cash = db.execute(
        "SELECT cash FROM users WHERE id = :user_id",
        user_id=session["user_id"]
    )[0]["cash"]

    # Initialize totals
    grand_total = cash

    # Calculate stock values
    for stock in stocks:
        quote = lookup(stock["symbol"])
        if quote:
            stock["name"] = quote["name"]
            stock["price"] = quote["price"]
            grand_total += quote["price"] * stock["total_shares"]

    return render_template(
        "index.html",
        stocks=stocks,
        cash=cash,  # Remove usd() here since we'll format in template
        grand_total=grand_total  # Remove usd() here
    )



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Validation
        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive integer shares", 400)

        shares = int(shares)
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        total_cost = shares * quote["price"]
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        if cash < total_cost:
            return apology("can't afford", 400)

        # Debug output
        print(f"DEBUG: Buying {shares} shares at {quote['price']}")
        print(f"DEBUG: Total cost before formatting: {total_cost}")
        print(f"DEBUG: Formatted total cost: {usd(total_cost)}")

        # Update database
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                  total_cost, session["user_id"])

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            session["user_id"], symbol, shares, quote["price"]
        )

        flash(f"Bought {shares} share(s) of {symbol} for {usd(total_cost)}.")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC",
        user_id = session["user_id"]
    )

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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        return render_template("quoted.html",
                           name=quote["name"],
                           symbol=quote["symbol"],
                           price=usd(quote["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Clear any existing session
    session.clear()

    if request.method == "POST":
        # Validate inputs
        if not request.form.get("username"):
            return apology("Username is required", 400)
        elif not request.form.get("password"):
            return apology("Password is required", 400)
        elif not request.form.get("confirmation"):
            return apology("You must confirm your password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)  # Fixed error message

        # Check if username exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))  # Fixed "excute" to "execute" and "usename" to "username"

        if len(rows) != 0:
            return apology("Username already exists", 400)  # Fixed "Usemane" typo

        # Insert new user
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password"))  # Fixed "generate_passord_hash" to "generate_password_hash"
            )
        # Get new user's id
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))  # Fixed typo again

        # Remember user session
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Get user's stocks
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"]
    )

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Validate input
        if not symbol:
            return apology("Symbol is required")
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must be a positive number of shares")
        else:
            shares = int(shares)

        # Check if user owns the stock
        for stock in stocks:
            if stock["symbol"] == symbol:
                if stock["total_shares"] < shares:
                    return apology("You don't have enough shares")
                else:
                    quote = lookup(symbol)
                    if quote is None:
                        return apology("Symbol not found")

                    price = quote["price"]
                    total_sale = shares * price

                    # Update user cash
                    db.execute(
                        "UPDATE users SET cash = cash + :total_sale WHERE id = :user_id",
                        total_sale=total_sale,
                        user_id=session["user_id"]
                    )

                    # Record transaction
                    db.execute(
                        "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                        user_id = session["user_id"],
                        symbol = symbol,
                        shares = -shares,  # Negative shares for selling
                        price = price
                    )

                    flash(f"Sold {shares} shares of {symbol} for {usd(total_sale)}!")
                    return redirect("/")

        return apology("Symbol not found")
    else:
        return render_template("sell.html", stocks = stocks)

#check50 cs50/problems/2025/x/finance

