import math
from enum import Enum


class MenuOption(Enum):
    SHOW_REVIEWS = 'Show reviews'
    CHECK_TOKEN = 'Check if a token is present'
    SHOW_DOCUMENT_FREQUENCY = 'Show the document frequency for a particular token'
    SHOW_TOKEN_STATISTICS = 'Show all statistics for a particular token'
    SHOW_SENTENCE_STATISTICS = 'Show the statistics for a sentence'
    SAVE_STOP_WORD_LIST = 'Save the list of stop words to a file'
    SHOW_ADJUSTED_SENTENCE_STATISTICS = 'Show the statistics for a sentence with stop words ignored'
    EXIT = 'Exit the program'


def make_review_list(file):
    with open(file, "r") as sentiment_text:
        reviews = []
        for line in sentiment_text:
            reviews.append(line.strip())
    return reviews


def make_token_dictionary(reviews):
    tokens = dict()
    for review in reviews:
        for token in review[1:].split():
            if token in tokens:
                tokens[token] += 1
            else:
                tokens[token] = 1
    return tokens


def get_stop_words(reviews, tokens):
    total_tokens = 0
    stop_words = []
    for review in reviews:
        for token in review[1:].split():
            total_tokens += 1
    for token in tokens:
        if tokens[token] / total_tokens >= 0.002 and token not in stop_words:
            stop_words.append(token)
    return sorted(stop_words, key=len)


def get_input_number(input_prompt, smallest_value, collection):
    while True:
        try:
            input_number = int(input(input_prompt))
            if input_number <= smallest_value or input_number > len(collection):
                raise IndexError
            return input_number
        except IndexError:
            print('Please enter a valid, in-range number')
        except ValueError:
            print('Please enter a valid, in-range number')


def show_reviews(reviews):
    beginning_review_number = get_input_number(f'Enter a beginning review number from 1 to {len(reviews)}: ', 0,
                                               reviews)
    ending_review_number = get_input_number(
        f'Enter a ending review number from {beginning_review_number} to {len(reviews)}: ',
        beginning_review_number - 1, reviews)
    for review in reviews[beginning_review_number - 1:ending_review_number]:
        print(f'Review #{reviews.index(review) + 1}: {review}')


def check_token(tokens):
    input_token = input("Enter a token: ").lower()
    if input_token in tokens:
        print(f'The token "{input_token}" is one of the {len(tokens)} unique tokens that appear in the training data.')
    else:
        print(
            f'The token "{input_token}" is not one of the {len(tokens)} unique tokens that appear in the training data.')


def get_token_frequency(tokens, input_token):
    if input_token in tokens:
        return tokens[input_token]
    else:
        return 0


def show_document_frequency(tokens):
    input_token = input("Enter a token: ").lower()
    number_of_appearances = get_token_frequency(tokens, input_token)
    print(f'The training data contains {number_of_appearances} appearance(s) of the token "{input_token}".')


def get_review_type_appearances(input_token, reviews):
    review_type_appearances = {'positive': 0, 'negative': 0, 'neutral': 0}
    for review in reviews:
        for token in review[1:].split():
            if token == input_token:
                if review[0] == '+':
                    review_type_appearances['positive'] += 1
                if review[0] == '-':
                    review_type_appearances['negative'] += 1
                if review[0] == '0':
                    review_type_appearances['neutral'] += 1
    return review_type_appearances


def compute_differential_score(review_type_appearances, reviews):
    all_tokens_in_positives = 0
    all_tokens_in_negatives = 0
    for review in reviews:
        for token in review[1:].split():
            if review[0] == '+':
                all_tokens_in_positives += 1
            if review[0] == '-':
                all_tokens_in_negatives += 1
    differential_score = (math.log(1 + review_type_appearances['positive']) - math.log(1 + all_tokens_in_positives)) - (
            math.log(1 + review_type_appearances['negative']) - math.log(1 + all_tokens_in_negatives))
    return differential_score


def compute_token_classification(differential_score):
    if differential_score < -0.1:
        return 'negative'
    elif differential_score > 0.1:
        return 'positive'
    else:
        return 'neutral'


def show_token_statistics(reviews, tokens):
    input_token = input("Enter a token: ").lower()
    if input_token in tokens:
        review_type_appearances = get_review_type_appearances(input_token, reviews)
        differential_score = compute_differential_score(review_type_appearances, reviews)
        token_classification = compute_token_classification(differential_score)
        print(
            f'The token "{input_token}" has {review_type_appearances["negative"]} negative, {review_type_appearances["neutral"]} '
            f'neutral, and {review_type_appearances["positive"]} positive appearance(s) in the training data.')
        print(
            f'The token "{input_token}" is classified as {token_classification} because it has has a differential tf-idf '
            f'score of {differential_score}')
    else:
        print(f'The token "{input_token}" does not appear in the training data.')


def get_score_and_token_type(input_token, reviews, score_sum, token_types):
    review_type_appearances = get_review_type_appearances(input_token, reviews)
    score = compute_differential_score(review_type_appearances, reviews)
    token_types[compute_token_classification(score)] += 1
    score_sum += score
    return score_sum, token_types


def calculate_average_score_and_token_types(token_types, tokens, input_tokens, reviews, stop_words):
    score_sum = 0
    for input_token in input_tokens:
        if 'stop_words' in token_types:
            if input_token in tokens and input_token not in stop_words:
                score_sum, token_types = get_score_and_token_type(input_token, reviews, score_sum, token_types)
            if input_token in stop_words:
                token_types["stop_words"] += 1
            else:
                token_types['unknown'] += 1
        else:
            if input_token in tokens:
                score_sum, token_types = get_score_and_token_type(input_token, reviews, score_sum, token_types)
            else:
                token_types['unknown'] += 1
    if score_sum != 0:
        average_differential_score = score_sum / (
                token_types['positive'] + token_types['negative'] + token_types['neutral'])
    else:
        average_differential_score = None
    return average_differential_score, token_types


def show_sentence_statistics(tokens, reviews, stop_words):
    input_tokens = input('Enter a sentence as space-separated tokens: ').lower().split()
    token_types = {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}
    average_score, token_types = calculate_average_score_and_token_types(token_types, tokens, input_tokens, reviews,
                                                                         stop_words)
    if average_score is not None:
        print(
            f'The sentence has {token_types["negative"]} negative, {token_types["neutral"]} neutral, {token_types["positive"]} '
            f'positive, and {token_types["unknown"]} unknown token(s).')
        print(f'The sentence has an average tf-idf score of {average_score}.')
    else:
        print('The sentence contains only unknown tokens; therefore, its average tf-idf score is undefined.')


def save_stop_word_list(stop_words):
    with open('output.txt', 'w') as output_txt:
        for stop_word in stop_words:
            output_txt.write(f'{stop_word}\n')
    print('Stop word list saved to "output.txt".')


def show_adjusted_sentence_statistics(tokens, reviews, stop_words):
    input_tokens = input('Enter a sentence as space-separated tokens: ').lower().split()
    token_types = {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0, 'stop_words': 0}
    average_score, token_types = calculate_average_score_and_token_types(token_types, tokens, input_tokens, reviews,
                                                                         stop_words)
    if average_score is not None:
        print(
            f'The sentence has {token_types["stop_words"]} stop-word token(s), and it has {token_types["negative"]} negative, {token_types["neutral"]} neutral, {token_types["positive"]} '
            f'positive, and {token_types["unknown"]} unknown non-stop-word tokens(s).')
        print(f'The sentence has an average tf-idf score of {average_score}.')
    else:
        print(
            f'The sentence contains only {token_types["stop_words"]} stop-word token(s) and {token_types["unknown"]} unknown non-stop-word token(s).')
        print('Therefore, its average tf-idf score is undefined.')


def main():
    try:
        reviews = make_review_list("sentiment.txt")
    except FileNotFoundError:
        print("This file does not exist")
        return
    tokens = make_token_dictionary(reviews)
    stop_words = get_stop_words(reviews, tokens)
    options = tuple(MenuOption)
    while True:
        print('Choose an option:')
        for i in range(len(options)):
            print(f'\t{i + 1}. {options[i].value}')
        input_option = options[get_input_number('Enter a number from 1 to 8: ', 0, options) - 1]
        if input_option == MenuOption.EXIT:
            return
        elif input_option == MenuOption.SHOW_REVIEWS:
            show_reviews(reviews)
        elif input_option == MenuOption.CHECK_TOKEN:
            check_token(tokens)
        elif input_option == MenuOption.SHOW_DOCUMENT_FREQUENCY:
            show_document_frequency(tokens)
        elif input_option == MenuOption.SHOW_TOKEN_STATISTICS:
            show_token_statistics(reviews, tokens)
        elif input_option == MenuOption.SHOW_SENTENCE_STATISTICS:
            show_sentence_statistics(tokens, reviews, stop_words)
        elif input_option == MenuOption.SAVE_STOP_WORD_LIST:
            save_stop_word_list(stop_words)
        elif input_option == MenuOption.SHOW_ADJUSTED_SENTENCE_STATISTICS:
            show_adjusted_sentence_statistics(tokens, reviews, stop_words)
        else:
            print(f'{input_option}\n')


if __name__ == '__main__':
    main()
