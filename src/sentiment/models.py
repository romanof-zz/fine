class Tweet:
    def __init__(self, id, source, time, text, lang, retweet_count, tags):
        self.id = id
        self.source = source
        self.time = time
        self.text = text
        self.lang = lang
        self.rt_count = retweet_count
        self.tags = tags
