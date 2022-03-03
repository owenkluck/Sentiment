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


def option_input(options):

    while True:
        try:
            chosen_option = int(input('Enter a number from 1 to 8:'))
            if chosen_option <= 0:
                raise IndexError
            return options[chosen_option - 1]
        except IndexError:
            print('Please enter a valid, in-range number')


def main():

    with open("sentiment.txt", "r") as sentiment_text:
        reviews: []
        try:
            for a_line in sentiment_text:
                strip_lines = a_line.strip()
                reviews = strip_lines.split()
                print(reviews)
                m = reviews.append(reviews)
                values = a_line.split()
            print(values)
        except FileExistsError:
            print("This file does not exist")

    options = tuple(MenuOption)
    while True:
        print('Choose an option:')
        for i in range(len(options)):
            print(f'\t{i + 1}. {options[i].value}')
        input_option = option_input(options)
        if input_option == MenuOption.EXIT:
            return
        else:
            print(f'{input_option}\n')

        value1 = input('Enter a beginning review number from 1 to 8529: ')
        value2 = input('Enter a ending review number from ' + value1 + ' to 8529: ')
        converted_value1 = int(value1)
        converted_value2 = int(value2)
        if input_option == MenuOption.SHOW_REVIEWS:
            print('Enter a beginning review number from 1 to 8529: ')
        if 1 <= converted_value1 <= 8529:
            print('Enter a ending review number from ' + value1 + ' to 8529: ')
        if converted_value1 <= converted_value2 <= 8529:
            print(reviews[converted_value1 - 1:converted_value2 - 1])



if __name__ == '__main__':
    main()
