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

class TestGetTokenStatistics(TestCase):
    def test_positive(self):
        reviews = sentiment.make_review_list()
        review_type_appearances = sentiment.get_review_type_appearances('good', reviews)
        self.assertEquals(review_type_appearances["positive"], 129)

    def test_negative(self):
        reviews = sentiment.make_review_list()
        review_type_appearances = sentiment.get_review_type_appearances('good', reviews)
        self.assertEquals(review_type_appearances["negative"], 85)

    def test_neutral(self):
        reviews = sentiment.make_review_list()
        review_type_appearances = sentiment.get_review_type_appearances('good', reviews)
        self.assertEquals(review_type_appearances["neutral"], 50)


