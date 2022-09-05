from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from tweets.models import Tweet
from comments.models import Comment

class TestCase(DjangoTestCase):

    @property
    def anonymous_client(self):
        if hasattr(self, '_anonymous_cliet'):
            return self.anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client

    def create_user(self, username, email=None, password=None):
        if email is None:
            email = '{}@jiuzhang.com'.format(username)
        if not password:
            password = 'generic password'
        return User.objects.create_user(username, email, password)

    def create_tweet(self, user, content=None):
        if not content:
            content = 'default tweet content'
        return Tweet.objects.create(user=user, content=content)

    def create_comment(self, user, tweet, content=None):
        if not content:
            content = 'default tweet content'
        return Comment.objects.create(user=user, tweet=tweet, content=content)