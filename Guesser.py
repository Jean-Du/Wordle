import pandas as pd
from main import topword, positions, path

dfwordsfull = pd.read_csv(path % 'Wordle.csv', index_col=0)
dfwords = dfwordsfull[dfwordsfull['Answer'] == True].copy()
dfguess = dfwords
method = 'Score'


def checkallowed(entry):
    allowed = ['b', 'y', 'g']
    while (not (set(entry) <= set(allowed))) or len(entry) != 5:
        entry = input("Invalid entry. Please try again: \n")
    return entry


guess = topword(dfwordsfull, method)
# guess = 'irate'
# guess = 'shily'
print(guess)
number = 1
clue = checkallowed(input("Please enter the colours, using the letters b, y and g: \n"))
while clue != 'ggggg':
    for letter in set(guess):
        letter_positions = positions(guess, letter)
        letter_count = 0
        black = False
        for pos in letter_positions:
            if clue[pos] == 'g':
                dfguess = dfguess[dfguess.index.str[pos] == letter]
                letter_count += 1
            elif clue[pos] == 'y':
                dfguess = dfguess[dfguess.index.str[pos] != letter]
                letter_count += 1
            elif clue[pos] == 'b':
                dfguess = dfguess[dfguess.index.str[pos] != letter]
                black = True
        if black:
            dfguess = dfguess[dfguess.index.str.count(letter) == letter_count]
        else:
            dfguess = dfguess[dfguess.index.str.count(letter) >= letter_count]
    # if number == 1:
    #     dfguess = dfguess[dfguess['Answer'] == True]
    if (1 <= number < 4) and (len(dfguess) + number) > 5:
        guess = topword(dfwordsfull, method, list(dfguess.index))
    else:
        guess = topword(dfguess, method)
    # dftemprank = wordranking(dfwordsfull, list(dfguess.index))
    # dftemprank.to_csv(path % ("Test rank %d.csv" % number))
    print(guess)
    number += 1
    clue = checkallowed(input("Please enter the colours, using the letters b, y and g: \n"))
print("Congratulations for winning in %d attempt(s)!" % number)
