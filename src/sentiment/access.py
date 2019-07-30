from datetime import datetime
import yaml
import twitter
from botocore.exceptions import ClientError
from util import DATE_FORMAT

from .models import Tweet

class TwitterDataAccess:
    DIR = "tweets"
    LAST_POINTER = "$LAST"
    TIME_FORMAT = '%a %b %d %H:%M:%S %z %Y'

    def __init__(self, storage, logger, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.storage = storage
        self.logger = logger
        self.api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                               access_token_key=access_token_key, access_token_secret=access_token_secret)

    def update_all(self):
        users = self.api.GetFriends()
        self.logger.info(f"updating {len(users)} users.")
        [self.update(user) for user in users]

    def update(self, user):
        # get all new statuses
        statuses = self.api.GetUserTimeline(screen_name=user.screen_name,
                                            since_id=self.__last_updated(user.screen_name),
                                            count=200)

        tweets = map(lambda s: Tweet(s.id_str, s.user.screen_name, datetime.strptime(s.created_at, self.TIME_FORMAT), s.text, s.lang, s.retweet_count, s.hashtags), statuses)
        tweets = sorted(tweets, key=lambda x: x.time)
        self.logger.info("{} new tweets loaded for {}".format(len(tweets), user.screen_name))

        tweets_date_map = {}
        for tweet in tweets:
            date_key = tweet.time.strftime(DATE_FORMAT)
            if not date_key in tweets_date_map: tweets_date_map[date_key] = self.__load_date(tweet.source, date_key)
            tweets_date_map[date_key].append(tweet)

        for date in tweets_date_map:
            key = self.__key(user.screen_name, date)
            self.storage.put(key, yaml.dump(tweets_date_map[date]))
            self.logger.info("updated {}".format(key))

        if len(tweets): self.storage.put(self.__key(user.screen_name, self.LAST_POINTER), tweets[-1].id)

    def load(self, users=None, date_key=None):
        if users is None: users = map(lambda u: u.screen_name, self.api.GetFriends())
        if date_key is None: date_key = datetime.now().strftime(DATE_FORMAT)
        tweets = []
        for user in users:
            tweets += self.__load_date(user, date_key)
        return tweets

    def __load_date(self, username, date_key):
        data = self.__load(username, date_key)
        return yaml.load(data, Loader=yaml.FullLoader) if data else []

    def __last_updated(self, dir):
        return self.__load(dir, self.LAST_POINTER)

    def __load(self, username, filename):
        key = self.__key(username, filename)
        try:
            return self.storage.get(key)
        except ClientError:
            self.logger.error(f"failed to load '{key}'")
            return None

    def __key(self, username, date):
        return f"{self.DIR}/{username}/{date}"
