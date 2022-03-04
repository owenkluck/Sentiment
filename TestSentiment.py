from unittest import TestCase
import sentiment


class TestMakeTokenSet(TestCase):
    def test_tokens_length(self):
        reviews = sentiment.make_review_list()
        tokens = sentiment.make_token_set(reviews)
        self.assertEqual(len(tokens), 16444)


class TestGetTokenFrequency(TestCase):
    def test_too(self):
        reviews = sentiment.make_review_list()
        self.assertEqual(sentiment.get_token_frequency(reviews, 'too'), 314)

    def test_unmentioned(self):
        reviews = sentiment.make_review_list()
        self.assertEqual(sentiment.get_token_frequency(reviews, 'unmentioned'), 0)
