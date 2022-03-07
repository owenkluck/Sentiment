from unittest import TestCase
import sentiment


class TestSentiment(TestCase):
    reviews = sentiment.make_review_list('test_sentiment.txt')
    tokens = sentiment.make_token_dictionary(reviews)
    stop_words = sentiment.get_stop_words(tokens)

    def test_tokens_length(self):
        self.assertEqual(len(self.tokens), 16444)

    def test_get_token_frequency_too(self):
        frequency = sentiment.get_token_frequency(self.tokens, 'too')
        self.assertEqual(frequency, 314)

    def test_get_token_frequency_unmentioned(self):
        frequency = sentiment.get_token_frequency(self.tokens, 'unmentioned')
        self.assertEqual(frequency, 0)

    def test_get_review_type_appearances(self):
        review_type_appearances = sentiment.get_review_type_appearances('too', self.reviews)
        self.assertEqual(review_type_appearances, {'positive': 49, 'negative': 200, 'neutral': 65})

    def test_compute_differential_score(self):
        review_type_appearances = sentiment.get_review_type_appearances('too', self.reviews)
        score = sentiment.compute_differential_score(review_type_appearances, self.reviews)
        self.assertEqual(score, -1.4990477543373988)

    def test_compute_token_classification_negative(self):
        review_type_appearances = sentiment.get_review_type_appearances('too', self.reviews)
        score = sentiment.compute_differential_score(review_type_appearances, self.reviews)
        classification = sentiment.compute_token_classification(score)
        self.assertEqual(classification, 'negative')

    def test_compute_token_classification_positive(self):
        review_type_appearances = sentiment.get_review_type_appearances('good', self.reviews)
        score = sentiment.compute_differential_score(review_type_appearances, self.reviews)
        classification = sentiment.compute_token_classification(score)
        self.assertEqual(classification, 'positive')

    def test_compute_token_classification_neutral(self):
        review_type_appearances = sentiment.get_review_type_appearances('the', self.reviews)
        score = sentiment.compute_differential_score(review_type_appearances, self.reviews)
        classification = sentiment.compute_token_classification(score)
        self.assertEqual(classification, 'neutral')

    def test_save_stop_word_list(self):
        sentiment.save_stop_word_list(self.stop_words)
        with open('output.txt', 'r') as output_text:
            number_of_lines = 0
            for line in output_text:
                number_of_lines += 1
        self.assertEqual(number_of_lines, 51)

    def test_calculate_average_score_and_token_types_including_stop_words(self):
        average_score, token_types = sentiment.calculate_average_score_and_token_types(
            {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}, self.tokens,
            'absolutely detestable ; would not watch again'.split(), self.reviews, self.stop_words)
        self.assertEqual(token_types, {'positive': 1, 'negative': 5, 'neutral': 0, 'unknown': 1})
        self.assertEqual(average_score, -0.18812093738509109)

    def test_calculate_average_score_and_token_types_ignoring_stop_words(self):
        average_score, token_types = sentiment.calculate_average_score_and_token_types(
            {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0, 'stop_words': 0}, self.tokens,
            'absolutely detestable ; would not watch again'.split(), self.reviews, self.stop_words)
        self.assertEqual(token_types, {'positive': 1, 'negative': 4, 'neutral': 0, 'unknown': 1, 'stop_words': 1})
        self.assertEqual(average_score, -0.17687684751966531)

    def test_average_idf_score_of_sentence_none(self):
        average_score, token_types = sentiment.calculate_average_score_and_token_types(
            {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0, 'stop_words': 0}, self.tokens, 'igloo'.split()
            , self.reviews, self.stop_words)
        self.assertEqual(token_types, {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 1, 'stop_words': 0})
        self.assertEqual(average_score, None)
