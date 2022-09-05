from friendships.models import Friendship
from rest_framework.test import APIClient
from testing.testcases import TestCase

FOLLOW_URL = '/api/friendships/{}/follow/'
UNFOLLOW_URL = '/api/friendships/{}/unfollow/'
FOLLOWERS_URL = '/api/friendships/{}/followers/'
FOLLOWINGS_URL = '/api/friendships/{}/followings/'

class FriendshipApiTests(TestCase):
    def setUp(self):
        self.linghu = self.create_user('linghu')
        self.linghu_client = APIClient()
        self.linghu_client.force_authenticate(self.linghu)

        self.dongxie = self.create_user('dongxie')
        self.dongxie_client = APIClient()
        self.dongxie_client.force_authenticate(self.dongxie)

        for i in range(2):
            user = 'dongxie_follower{}'.format(i)
            follower = self.create_user(user)
            Friendship.objects.create(from_user=follower, to_user=self.dongxie)
        for i in range(3):
            user = 'dongxie_following{}'.format(i)
            following = self.create_user(user)
            Friendship.objects.create(from_user=self.dongxie, to_user=following)

    def test_follow(self):
        ur1 = FOLLOW_URL.format(self.linghu.id)

        # login is required to follow others
        response = self.anonymous_client.post(ur1)
        self.assertEqual(response.status_code, 403)

        # should use get to follow
        response = self.dongxie_client.get(ur1)
        self.assertEqual(response.status_code, 405)

        # cannot follow yourself
        response = self.linghu_client.post(ur1)
        self.assertEqual(response.status_code, 400)

        # follow successfully
        response = self.dongxie_client.post(ur1)
        self.assertEqual(response.status_code, 201)
        # repeated follow
        response =  self.dongxie_client.post(ur1)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['duplicate'], True)

        count = Friendship.objects.count()
        response = self.linghu_client.post(FOLLOW_URL.format(self.dongxie.id))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Friendship.objects.count(), count + 1)

    def test_unfollow(self):
        ur1 = UNFOLLOW_URL.format(self.linghu.id)

        # login is required to unfollow others
        response = self.anonymous_client.post(ur1)
        self.assertEqual(response.status_code, 403)

        # should use get to unfollow
        response = self.dongxie_client.get(ur1)
        self.assertEqual(response.status_code, 405)

        # cannot unfollow yourself
        response = self.linghu_client.post(ur1)
        self.assertEqual(response.status_code, 400)

        # unfollow successfully
        Friendship.objects.create(from_user=self.dongxie, to_user=self.linghu)
        count = Friendship.objects.count()
        response = self.dongxie_client.post(ur1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['deleted'], 1)
        self.assertEqual(Friendship.objects.count(), count-1)

        # unfollow the user without follow first
        count = Friendship.objects.count()
        response = self.dongxie_client.post(ur1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['deleted'], 0)
        self.assertEqual(Friendship.objects.count(), count)

    def test_followings(self):
        ur1 = FOLLOWINGS_URL.format(self.dongxie.id)

        # post is not allowed
        response = self.anonymous_client.post(ur1)
        self.assertEqual(response.status_code, 405)

        # get is OK
        response = self.anonymous_client.get(ur1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['followings']), 3)

        # make sure followings are ordered by decreasing time
        ts0 = response.data['followings'][0]['created_at']
        ts1 = response.data['followings'][1]['created_at']
        ts2 = response.data['followings'][2]['created_at']
        self.assertEqual(ts0 > ts1, True)
        self.assertEqual(ts1 > ts2, True)
        self.assertEqual(
            response.data['followings'][0]['user']['username'],
            'dongxie_following2',
        )
        self.assertEqual(
            response.data['followings'][1]['user']['username'],
            'dongxie_following1',
        )
        self.assertEqual(
            response.data['followings'][2]['user']['username'],
            'dongxie_following0',
        )

    def test_followers(self):
        ur1 = FOLLOWERS_URL.format(self.dongxie.id)

        # post is not allowed
        response = self.anonymous_client.post(ur1)
        self.assertEqual(response.status_code, 405)

        # get is OK
        response = self.anonymous_client.get(ur1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['followers']), 2)

        # make sure followings are ordered by decreasing time
        ts0 = response.data['followers'][0]['created_at']
        ts1 = response.data['followers'][1]['created_at']
        self.assertEqual(ts0 > ts1, True)
        self.assertEqual(
            response.data['followers'][0]['user']['username'],
            'dongxie_follower1',
        )
        self.assertEqual(
            response.data['followers'][1]['user']['username'],
            'dongxie_follower0',
        )
