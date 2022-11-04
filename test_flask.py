from unittest import TestCase

from app import app
from models import db, Pet


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class PetViewsTestCase(TestCase):
  """Tests for views for Pets"""

  def setUp(self):
    """Add sample pet"""

    Pet.query.delete()
    pet1 = Pet(name="TestPet1", species="dog", hunger=20)
    pet2 = Pet(name="TestPet2", species="cat", hunger=20)
    db.session.add(pet1)
    db.session.add(pet2)
    db.session.commit()

    # add this here so that we can reference self.pet1_id for all of the tests without having to create a new pet for each test
    self.pet1_id = pet1.id
    self.pet2_id = pet2.id

    self.pet1 = pet1
    self.pet2 = pet2

  def tearDown(self):
    """Clean up any fouled transaction"""

    db.session.rollback()

  def test_list_pets(self):
    """Testing root route"""

    with app.test_client() as client:
      #make a fake request
      resp = client.get("/")
      #get data from request and return it as text
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code,200)

      #checks to see if the string "TestPet" is in the html 
      self.assertIn("TestPet1", html)
      self.assertIn("TestPet2", html)

  def test_show_pet(self):
    with app.test_client() as client:
      resp = client.get(f"/{self.pet1_id}")
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code,200)
      self.assertIn('<h1>TestPet1 Details</h1>', html)

      #checks to see if the species for pet1 is included in the html
      self.assertIn(self.pet1.species, html)

      #pet2
      resp = client.get(f"/{self.pet2_id}")
      html = resp.get_data(as_text=True)
      self.assertIn('<h1>TestPet2 Details</h1>', html)
      self.assertIn(self.pet2.species, html)

  def test_add_pet(self):
    """Test to see if post request to add new pet works"""
    with app.test_client() as client:
      d = {"name": "TestPet3", "species": "cat", "hunger": 55}
      resp = client.post("/", data=d, follow_redirects=True)
      html = resp.get_data(as_text=True)

      self.assertEqual(resp.status_code, 200)
      self.assertIn("<h1>TestPet3 Details</h1>",html)
