from enum import Enum


class MenuOption(Enum):
    SHOW_REVIEW = 'Show a review'
    SAVE_TOKEN_LIST = 'Save the token list to a file'
    SHOW_DOCUMENT_FREQUENCY = 'Show the document frequency for a particular token'
    SHOW_TOKEN_STATISTICS = 'Show all statistics for a particular token'
    SHOW_SENTENCE_STATISTICS = 'Show the statistics for a sentence'
    SAVE_STOP_WORD_LIST = 'Save the list of stop words to a file'
    SHOW_ADJUSTED_SENTENCE_STATISTICS = 'Show the statistics for a sentence with stop words ignored'
    EXIT = 'Exit the program'


def main():
    pass


if __name__ == '__main__':
    main()
