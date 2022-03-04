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


def make_review_list():
    with open("sentiment.txt", "r") as sentiment_text:
        reviews = []
        for line in sentiment_text:
            reviews.append(line.strip())
    return reviews


def make_token_set(reviews):
    tokens = []
    for review in reviews:
        tokens.extend(review[1:].split())
    return set(tokens)


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


def get_token_frequency(reviews, input_token):
    number_of_appearances = 0
    for review in reviews:
        for token in review[1:].split():
            if token == input_token:
                number_of_appearances += 1
    return number_of_appearances


def main():
    try:
        reviews = make_review_list()
    except FileNotFoundError:
        print("This file does not exist")
        return
    tokens = make_token_set(reviews)
    options = tuple(MenuOption)
    while True:
        print('Choose an option:')
        for i in range(len(options)):
            print(f'\t{i + 1}. {options[i].value}')
        input_option = options[get_input_number('Enter a number from 1 to 8: ', 0, options) - 1]
        if input_option == MenuOption.EXIT:
            return
        elif input_option == MenuOption.SHOW_REVIEWS:
            beginning_review_number = get_input_number(f'Enter a beginning review number from 1 to {len(reviews)}: ', 0,
                                                       reviews)
            ending_review_number = get_input_number(
                f'Enter a ending review number from {beginning_review_number} to {len(reviews)}: ',
                beginning_review_number - 1, reviews)
            for review in reviews[beginning_review_number - 1:ending_review_number]:
                print(f'Review #{reviews.index(review) + 1}: {review}')
        elif input_option == MenuOption.CHECK_TOKEN:
            input_token = input("Enter a token: ").lower()
            if input_token in tokens:
                print(f'The token "{input_token}" is one of the 16444 unique tokens that appear in the training data.')
            else:
                print(
                    f'The token "{input_token}" is not one of the 16444 unique tokens that appear in the training data.')
        elif input_option == MenuOption.SHOW_DOCUMENT_FREQUENCY:
            input_token = input("Enter a token: ").lower()
            number_of_appearances = get_token_frequency(reviews, input_token)
            print(f'The training data contains {number_of_appearances} appearance(s) of the token "unmentioned".')
        else:
            print(f'{input_option}\n')


if __name__ == '__main__':
    main()
