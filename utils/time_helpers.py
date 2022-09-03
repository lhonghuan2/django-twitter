from datetime import datetime
import pytz

def utc_now():
    return datetime.now().replace(tzinfo=pytz.utc)

@property
def hours_to_now(self):
    return (utc_now() - self.created_at).seconds // 3600