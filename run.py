import random
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hangman')
# read the list of words from google sheets

word_list = []
words = SHEET.worksheet("words")
word_list = words.col_values(1)


def get_word():
    """
    this is to get the word from our sheets above and randomly
    select the words in no particular order, also to make the user's
    input uppercase for easy visual.
    """

    word = random.choice(word_list)
    return word.upper()


def play(word):
    """
    show letter when user choosed correct letter
    when correct letters are made and
    under-score when user choose wrong letters are made
    """

    word_completion = "_" * len(word)
    choosed = False
    choosed_letters = []
    choosed_words = []
    # number of try the user have until the complete hangman is shown.
    tries = 6
    print("Let's play Hangman!!!")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")
    while not choosed and tries > 0:
        choose = input("Please choose a letter or word:\n").upper()
        if len(choose) == 1 and choose.isalpha():
            if choose in choosed_letters:
                print("You already choosed the letter", choose)
            elif choose not in word:
                """
                if user choose the wrong letter/words then this is printed
                """

                print(choose, "is not in the word.")
                tries -= 1
                choosed_letters.append(choose)
            else:
                """
                if user choose the right letter/words then this is printed
                """

                print("Good job,", choose, "is in the word!")
                choosed_letters.append(choose)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(
                    word) if letter == choose]
                for index in indices:
                    word_as_list[index] = choose
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    choosed = True
        elif len(choose) == len(word) and choose.isalpha():
            if choose in choosed_words:
                print("You already choosed the word", choose)
            elif choose != word:
                print(choose, "is not the word.")
                tries -= 1
                choosed_words.append(choose)
            else:
                choosed = True
                word_completion = word
        else:
            print("Not a valid choice.")
        print(display_hangman(tries))
        print(word_completion)
        print("\n")
    if choosed:
        print("Congrats, you choosed the word! You win!")
    else:
        print("Sorry, you ran out of chances. The word was " + word + ". try again next time!")


def display_hangman(tries):
    """
    hangman image design for every score/points scored
    """
    stages = [  # complete score: head, torso, both arms, and both legs
                """
                   ---------
                   ||      |
                   ||      o
                   ||     \|/
                   ||      |
                   ||     / \
                """,
                # almost complete: head, torso, both arms, and one leg
                """
                   --------
                   ||      |
                   ||      O
                   ||     \|/
                   ||      |
                   ||     /
                """,
                # two more to go: head, torso, and both arms
                """
                   ---------
                   ||      |
                   ||      O
                   ||     \|/
                   ||      |
                   ||
                """,
                # impressive: head, torso, and one arm
                """
                   ---------
                   ||      |
                   ||      O
                   ||     \|
                   ||      |
                   ||
                """,
                # improving: head and torso
                """
                   ---------
                   ||      |
                   ||      O
                   ||      |
                   ||     |
                   ||
                """,
                # good job: head
                """
                   ---------
                   ||      |
                   ||      O
                   ||
                   ||
                   ||
                """,
                #  empty state
                """
                   --------
                   ||      |
                   ||
                   ||
                   ||
                   ||
                """
    ]
    return stages[tries]


def play_onceagain():
    """
    for options to play again or to stop game
    Y = yes and N = no
    """

    while True:
        choice = input("Play Again? (Y/N)\n").upper()
        if choice == "Y":
            return True
        elif choice == "N":
            exit()
        else:
            print("Yes or No :-)")


def main():
    """
    main function to put everything together
    with options to play once and again if needed
    """

    word = get_word()
    play(word)
    while play_onceagain():
        word = get_word()
        play(word)


if __name__ == "__main__":
    main()
