#Testing for the HB yelp project
import unittest 
from model import User, Business, Category, Location,  Attribute, Review, Tip, Keyword, BusinessKeyword, connect_to_db, db, example_data
from model import BusinessCategoryLocation as BCL
from server import app
# import server

class Flasktests(unittest.TestCase):
    """Runs at the start of each test below"""
    def setUp(self):

        self.client=app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()


    def tearDown(self):
        "Runs at the end of every test"

        db.session.close()
        db.drop_all()

    def test_find_business(self):
        """See if we can query the database and get our sample data"""
        dena_deli=Business.query.filter(business_name=="Dena's Deli").first()
        self.assertEqual(dena_deli.name, "Dena's Deli")


if __name__ == "__main__":
    import unittest

    unittest.main()
