from unittest import TestCase
import sentiment


class TestSentiment(TestCase):
    def test_tokens_length(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        tokens = sentiment.make_token_dictionary(reviews)
        self.assertEqual(len(tokens), 16444)

    def test_get_token_frequency_too(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        tokens = sentiment.make_token_dictionary(reviews)
        frequency = sentiment.get_token_frequency(tokens, 'too')
        self.assertEqual(frequency, 314)

    def test_get_token_frequency_unmentioned(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        tokens = sentiment.make_token_dictionary(reviews)
        frequency = sentiment.get_token_frequency(tokens, 'unmentioned')
        self.assertEqual(frequency, 0)

    def test_get_review_type_appearances(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        review_type_appearances = sentiment.get_review_type_appearances('too', reviews)
        self.assertEqual(review_type_appearances, {'positive': 49, 'negative': 200, 'neutral': 65})

    def test_compute_differential_score(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        review_type_appearances = sentiment.get_review_type_appearances('too', reviews)
        score = sentiment.compute_differential_score(review_type_appearances, reviews)
        self.assertEqual(score, -1.4990477543373988)

    def test_compute_token_classification_negative(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        review_type_appearances = sentiment.get_review_type_appearances('too', reviews)
        score = sentiment.compute_differential_score(review_type_appearances, reviews)
        classification = sentiment.compute_token_classification(score)
        self.assertEqual(classification, 'negative')

    def test_compute_token_classification_positive(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        review_type_appearances = sentiment.get_review_type_appearances('good', reviews)
        score = sentiment.compute_differential_score(review_type_appearances, reviews)
        classification = sentiment.compute_token_classification(score)
        self.assertEqual(classification, 'positive')

    def test_compute_token_classification_neutral(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        review_type_appearances = sentiment.get_review_type_appearances('the', reviews)
        score = sentiment.compute_differential_score(review_type_appearances, reviews)
        classification = sentiment.compute_token_classification(score)
        self.assertEqual(classification, 'neutral')

    def test_save_stop_word_list(self):
        reviews = sentiment.make_review_list('test_sentiment.txt')
        tokens = sentiment.make_token_dictionary(reviews)
        stop_words = sentiment.get_stop_words(tokens)
        sentiment.save_stop_word_list(stop_words)
        with open('output.txt', 'r') as output_text:
            number_of_lines = 0
            for line in output_text:
                number_of_lines += 1
        self.assertEqual(number_of_lines, 51)
