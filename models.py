from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  """Connect database to flask app. Example: connect_db(name_of_flask_app)"""
  db.app = app
  db.init_app(app)


  # MODELS GO BELOW

class Pet(db.Model):
  """Pet"""
  # dunder property __tablename__ is used to specify the name of the table
  __tablename__ = 'pets'


  # __repr__ method is used to represent a class's objects as a string which makes it easier to see the values of each Pet instance without having to check the database each time. This is mainly used to help you as you code.
  def __repr__(self):
    p = self
    return f"<Pet id={p.id} name={p.name} species={p.species} hunger={p.hunger}>"

  # Column and Integer needs to be capitalized. It is the format under SQLAlchemy. Autoincrement is the same as SERIAL in postgre sql
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)

  name = db.Column(db.String(50), nullable=False, unique=True)

  species = db.Column(db.String(30), nullable=True)

    # the default value will only be added after db.session.commit() is ran,
  # because it will check to see if there is a value for hunger first and if there is none then it will add 20 when updating the table
  hunger = db.Column(db.Integer, nullable=False, default=20) 

  @classmethod
  def get_by_species(cls,species):
    """Filter by specifed species"""
    return cls.query.filter_by(species=species).all()

  @classmethod
  def get_all_hungry(cls):
    """Filter for hunger greater than 20"""
    return cls.query.filter(Pet.hunger > 20).all()

  def greet(self):
    return f'Hi, I am {self.name} the {self.species}'

  def feed(self, amt=20):
    """Update hunger base off of amt"""
    self.hunger -= amt
    self.hunger = max(self.hunger, 0)