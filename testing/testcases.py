from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet

class TestCase(DjangoTestCase):
    def create_user(self, username, email, password=None):
        if not password:
            password = 'generic password'

        return User.objects.create_user(username, email, password)

    def create_tweet(self, user, content=None):
        if not content:
            content = 'default tweet content'
        return Tweet.objects.create(user=user, content=content)