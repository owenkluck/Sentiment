from unittest import TestCase
import sentiment


class TestMakeTokenSet(TestCase):
    def test_tokens_length(self):
        reviews = sentiment.make_review_list()
        tokens = sentiment.make_token_set(reviews)
        self.assertEqual(len(tokens), 16444)
