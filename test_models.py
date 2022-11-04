from unittest import TestCase

from app import app
from models import db, Pet

# create a seperate database for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class PetModelTestCase(TestCase):
  """Tests for model for Pets."""

  def setUp(self):
    """Delete existing pets before each test runs. The pets being deleted are the ones created in each test"""

    Pet.query.delete()

  def tearDown(self):
    """Clean up fouled transaction"""

    db.session.rollback()

  def test_greet(self):
    pet = Pet(name="TestPet",species='dog', hunger=30)
    self.assertEqual(pet.greet(), "Hi, I am TestPet the dog")

  def test_feed(self):
    pet = Pet(name="TestPet", species="dog", hunger=30)
    pet.feed(5)
    self.assertEqual(pet.hunger, 25)

    pet.feed(200)
    self.assertEqual(pet.hunger,0)

  def test_get_by_species(self):
    pet = Pet(name="TestPet", species="dog", hunger=30)
    db.session.add(pet)
    db.session.commit()

    dogs = Pet.get_by_species('dog')
    self.assertEqual(dogs, [pet])

