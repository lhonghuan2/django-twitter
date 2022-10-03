from accounts.models import UserProfile
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import caches
from twitter.cache import USER_PATTEN, USER_PROFILE_PATTEN

cache = caches['testing'] if settings.TESTING else caches['default']

class UserService:
    @classmethod
    def get_user_through_cache(cls, user_id):
        key = USER_PATTEN.format(user_id=user_id)

        # read from cache first
        user = cache.get(key)
        if user is not None:
            return user

        # cache missed, read from db
        try:
            user = User.objects.get(id=user_id)
            cache.set(key, user)
        except User.DoesNotExist:
            user = None
        return user

    @classmethod
    def invalidate_user(cls, user_id):
        key = USER_PATTEN.format(user_id=user_id)
        cache.delete(key)

    @classmethod
    def get_profile_through_cache(cls, user_id):
        key = USER_PROFILE_PATTEN.format(user_id=user_id)

        # read from cache first
        profile = cache.get(key)
        if profile is not None:
            return profile

        # cache missed, read from db
        profile, _ = UserProfile.objects.get_or_create(user_id=user_id)
        cache.set(key, profile)
        return profile

    @classmethod
    def invalidate_profile(cls, user_id):
        key = USER_PROFILE_PATTEN.format(user_id=user_id)
        cache.delete(key)

