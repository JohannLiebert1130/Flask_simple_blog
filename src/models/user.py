import uuid

import datetime
from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def register(cls, email, password):
        user = User.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            print("User already exists!")
            return False

    @staticmethod
    def login(email):
        session['email'] = email

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            # check the password
            return user.password == password
        return False

    def logout(self):
        session['email'] = None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, created_date=datetime.datetime.utcnow()):
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      created_date=created_date)

    def json(self):
        return {
            'email': self.email,
            'password': self.password,
            '_id': self._id
        }

    def save_to_mongo(self):
        Database.insert('users', self.json())


# Database.initialize()
#
# user = User.get_by_email('test@test.com')
# print(user.email)
#
# user.get_blogs()
# blog = Blog.from_mongo("ceec0bf855ef42c09e79e519de46d955")
# user.get_blogs()
# print(blog)
