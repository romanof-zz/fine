from nltk.util import ngrams

class Tweet:
    def __init__(self, id, source, time, text, lang, retweet_count, tags):
        self.id = id
        self.source = source
        self.time = time
        self.text = text
        self.lang = lang
        self.rt_count = retweet_count
        self.tags = tags

    def to_ngram(self, n=3):
        tokens = [token for token in self.text.lower().split(" ") if token != ""]
        ngs = []
        for i in range(2,n+1):
            ngs += map(lambda ngram: " ".join(ngram), list(ngrams(tokens, i)))
        term_map = {}
        for term in (tokens + ngs):
            if term in term_map.keys():
                term_map[term] += 1
            else:
                term_map[term] = 1
        return term_map
