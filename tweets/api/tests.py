from rest_framework.test import APIClient
from testing.testcases import TestCase
from tweets.models import Tweet

TWEET_LIST_API = '/api/tweets/'
TWEET_CREATE_API = '/api/tweets/'

class TweetApiTests(TestCase):

    def setUp(self):
        self.user1 = self.create_user('user1')
        self.tweet1 = [self.create_tweet(self.user1) for i in range(3)]

        self.user1_client = APIClient()
        self.user1_client.force_authenticate(self.user1)

        self.user2 = self.create_user('user2')
        self.tweet2 = [self.create_tweet(self.user2) for i in range(2)]

    def test_list_api(self):
        # check if there is a user_id
        response = self.anonymous_client.get(TWEET_LIST_API)
        self.assertEqual(response.status_code, 400)

        # normal request
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 3)
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user2.id})
        self.assertEqual(len(response.data['tweets']), 2)

        #test if the accounts are ranked based on create time
        self.assertEqual(response.data['tweets'][0]['id'], self.tweet2[1].id)
        self.assertEqual(response.data['tweets'][1]['id'], self.tweet2[0].id)

    def test_create_api(self):
        # must login
        response = self.anonymous_client.get(TWEET_LIST_API)
        self.assertEqual(response.status_code, 400)

        # must have content
        response = self.user1_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 400)
        # content could not be too short
        response = self.user1_client.post(TWEET_CREATE_API, {'content': 1})
        self.assertEqual(response.status_code, 400)
        # content could not be too long
        response = self.user1_client.post(TWEET_CREATE_API, {'content': '0'*141})
        self.assertEqual(response.status_code, 400)

        # normal posts
        tweets_count = Tweet.objects.count()
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': "Hello World, this is my first tweet"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.user1.id)
        self.assertEqual(Tweet.objects.count(), tweets_count + 1)
