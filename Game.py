import pandas as pd
import random as rd
from termcolor import colored
from main import positions, path


df = pd.read_csv(path % 'Wordle.csv', index_col=0)
wordlist = df.index.values
answerlist = df[df['Answer'] == True].index.values
answer = answerlist[rd.randint(0, len(answerlist) - 1)]
# answer = 'savvy'
print(colored(answer, 'white', 'on_white'))


def colourguess(guess, colours):
    for i in range(0, 5):
        if colours[i] == 'b':
            print(colored(guess[i], 'white', 'on_grey'), end='')
        elif colours[i] == 'g':
            print(colored(guess[i], 'grey', 'on_green'), end='')
        elif colours[i] == 'y':
            print(colored(guess[i], 'grey', 'on_yellow'), end='')


def checkallowed(entry):
    while entry not in wordlist:
        entry = input("Invalid entry. Please try again: \n")
    return entry


guess = checkallowed(input("Please enter a five letter word: \n"))
number = 1
while guess != answer:
    colours = [None] * 5
    for letter in set(guess):
        letter_positions = positions(guess, letter)
        if guess.count(letter) <= answer.count(letter):
            for pos in letter_positions:
                if letter == answer[pos]:
                    colours[pos] = 'g'
                else:
                    colours[pos] = 'y'
        else:
            green_count = 0
            non_green = letter_positions
            for pos in letter_positions:
                if letter == answer[pos]:
                    colours[pos] = 'g'
                    green_count += 1
                    non_green.remove(pos)
            for i in range(len(non_green)):
                if (i + 1) > answer.count(letter) - green_count:
                    colours[non_green[i]] = 'b'
                else:
                    colours[non_green[i]] = 'y'
    colourguess(guess, colours)
    guess = checkallowed(input("\nPlease enter a five letter word: \n"))
    number += 1
print(colored(guess, 'grey', 'on_green'))
print('You won the game in %d attempt(s)!' % number)
