from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


#!login
@auth.route("/login", methods=["GET", "POST"])
def login():
   
   if request.method == "POST":
      email = request.form.get("email")
      password = request.form.get("password")


      user = User.query.filter_by(email=email).first() 
      if user:
         if check_password_hash(user.password, password):      # type: ignore
            flash("Logged In successfully!", category="success")  
            login_user(user, remember = True)
            return redirect(url_for("views.home")) 
         else:
            flash("Incorrect Password. Try again", category="error")
      else:
         flash("Email does not exist.", category="error")
            
      
            
   
   return render_template("login.html", user=current_user)
   


#!logout
@auth.route("/logout")
@login_required
def logout():
   logout_user()
   return redirect(url_for("auth.login"))


#!sign-up
@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
   if request.method == "POST":
      email = request.form.get("email")
      first_name = request.form.get("firstName")
      password1 = request.form.get("password1")
      password2 = request.form.get("password2")


      user = User.query.filter_by(email=email).first() 

      if user:
         flash("Email already taken. Please try again", category="error")
      elif len(email) < 4: #type: ignore
         flash("Email must be greater than 3 characters.", category="error")
      elif len(first_name) < 2: #type: ignore
         flash("First Name must be greater than one character.", category="error")
      elif password1 != password2:
         flash("Passwords don't match.", category="error")
      elif len(password1) < 4: #type: ignore
         flash("Password must be at least 4 characters.", category="error")
      else:
         new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="sha256"))  #type: ignore
         db.session.add(new_user)
         db.session.commit()
         
         login_user(new_user, remember = True)
         
         flash("Account created!", category="success")
         
         return redirect(url_for("views.home"))
         
         
         
    
   return render_template("sign_up.html", user=current_user)