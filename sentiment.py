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


if __name__ == '__main__':
    main()
