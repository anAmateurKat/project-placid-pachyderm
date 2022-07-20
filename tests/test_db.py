#test_db.py

import unittest
from peewee import *
from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of all models,
        # we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live for the duration
        # of the connection, and in the next step the connection is closed.
        test_db.drop_tables(MODELS)

        # Close connection to db
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello World, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello World, I\'m Jane!')
        assert second_post.id == 2
        
        get_first_post = TimelinePost.get(TimelinePost.id == 1)
        assert get_first_post.name == 'John Doe'
        assert get_first_post.email == 'john@example.com'
        assert get_first_post.content == 'Hello World, I\'m John!'

        get_second_post = TimelinePost.get(TimelinePost.id == 2)
        assert get_second_post.name == 'Jane Doe'
        assert get_second_post.email == 'jane@example.com'
        assert get_second_post.content == 'Hello World, I\'m Jane!'

        
