class SentimentAnalyzer:
    def __init__(self, access):
        self.access = access

    def extract_terms(self, date_key):
        terms = {}
        for tweet in self.access.load(None, date_key):
            term_map = tweet.to_ngram()
            for key in term_map:
                if key in terms.keys():
                    terms[key] += term_map[key]
                else:
                    terms[key] = term_map[key]

        # remove singles
        terms = {term: terms[term] for term in terms if terms[term] > 1}
        return terms
