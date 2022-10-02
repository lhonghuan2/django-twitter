from django.core.cache import caches
from django.conf import settings
from friendships.models import Friendship
from twitter.cache import FOLLOWINGS_PATH

cache = caches['testing'] if settings.TESTING else caches['default']

class FriendshipService(object):

    @classmethod
    def get_followers(cls, user):
        friendships = Friendship.objects.filter(
            to_user=user,
        ).prefetch_related('from_user')
        return [friendship.from_user for friendship in friendships]


    @classmethod
    def get_following_user_id_set(cls, from_user_id):
        key = FOLLOWINGS_PATH.format(user_id = from_user_id)
        user_id_set = cache.get(key)
        if user_id_set is not None:
            return  user_id_set

        friendships = Friendship.objects.filter(from_user_id=from_user_id)
        user_id_set = set([fs.to_user_id for fs in friendships])
        cache.set(key, user_id_set)
        return user_id_set

    @classmethod
    def invalidate_followings_cache(cls, from_user_id):
        key = FOLLOWINGS_PATH.format(user_id=from_user_id)
        cache.delete(key)


