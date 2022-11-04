# Everything from line 3 to 17 is a typical boiler plate for using SQLAlchemy on a flask application

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet 
#Pet is a class on models.py


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_pets():
  """shows list of all pets in database"""

  # We have access to Pet which was imported, and can store a list of all of the pets
  pets = Pet.query.all()
  return render_template('list.html', pets=pets )

@app.route('/', methods=["POST"])
def create_pet():
  name = request.form["name"]
  species = request.form["species"]
  hunger = request.form["hunger"]
  # Set hunger to int because request.form returns a string
  hunger = int(hunger) if hunger else None

  # make new instance of Pet
  new_pet = Pet(name=name, species=species, hunger=hunger)
  db.session.add(new_pet)
  db.session.commit()

  # Rember that we want to redirect for POST requests, if not the same form can be resubmitted and will cause duplicate data
  # Redirecting to details page, where the info of the new pet being added will be displayed
  return redirect(f"/{new_pet.id}")

@app.route('/<int:pet_id>')
def show_pet(pet_id):
  """Show details about a single pet"""
  # pet = Pet.query.get(pet_id)

  # If we try to access a pet id that does not exist it will return pet will equal "none" which we do not want, 
  # Use get_or_404, which will throw a 404 error instead of returning none
  pet = Pet.query.get_or_404(pet_id)
  return render_template("details.html",pet=pet )

@app.route("/species/<species_id>")
def show_pets_by_species(species_id):
  pets = Pet.get_by_species(species_id)
  return render_template('species.html', pets=pets, species=species_id)






  