import pandas as pd
import statistics as st
from main import topword, positions, path

dfwordsfull = pd.read_csv(path % 'Wordle.csv', index_col=0)
dfwords = dfwordsfull[dfwordsfull['Answer'] == True].copy()
answerlist = dfwords.index.values

# methods = [0.1, 0.2, 0.5, 1, 2, 5, 10]
# methods = ['Score', 'Weighted Sum', 'Occurrence']
methods = ['Score']
indices = []
for method in methods:
    for counter in range(1, 2):
        indices.append('%s %d' % (method, counter))
dfdistribution = pd.DataFrame(index=indices)


for method in methods:
    for counter in range(1, 2):
        numbers = []
        starting_guess = topword(dfwordsfull, method)
        dfanswers = pd.DataFrame(index=answerlist)
        dfanswers['Number'] = ''
        for i in range(2, 10):
            dfanswers['After %d' % (i - 1)] = ''
            dfanswers['%d' % i] = ''
        for answer in answerlist:
            dfguess = dfwordsfull
            guess = starting_guess
            number = 1
            while guess != answer:
                for letter in set(guess):
                    letter_positions = positions(guess, letter)
                    answer_letter_count = answer.count(letter)
                    guess_letter_count = guess.count(letter)
                    if guess_letter_count > answer_letter_count:
                        dfguess = dfguess[dfguess.index.str.count(letter) == answer_letter_count]
                    else:
                        dfguess = dfguess[dfguess.index.str.count(letter) >= guess_letter_count]
                    for pos in letter_positions:
                        if letter == answer[pos]:
                            dfguess = dfguess[dfguess.index.str[pos] == letter]
                        else:
                            dfguess = dfguess[dfguess.index.str[pos] != letter]
                if number == counter:
                    dfguess = dfguess[dfguess['Answer'] == True]
                if (1 <= number < 4) and (len(dfguess) + number) > 5:
                    guess = topword(dfwordsfull, method, list(dfguess.index))
                else:
                    guess = topword(dfguess, method)
                number += 1
                dfanswers.at[answer, 'After %d' % (number-1)] = len(dfguess)
                dfanswers.at[answer, str(number)] = guess
            numbers.append(number)
            dfanswers.at[answer, 'Number'] = number
            print(answer, number)

        dfdistribution.at['%s %d' % (method, counter), 'Mean'] = st.mean(numbers)
        dfdistribution.at['%s %d' % (method, counter), 'Median'] = st.median(numbers)
        dfdistribution.at['%s %d' % (method, counter), 'Mode'] = st.mode(numbers)
        dfdistribution.at['%s %d' % (method, counter), 'Std'] = st.pstdev(numbers)
        dfdistribution.at['%s %d' % (method, counter), 'Min'] = min(numbers)
        dfdistribution.at['%s %d' % (method, counter), 'Max'] = max(numbers)

        for i in range(min(numbers), max(numbers)+1):
            dfdistribution.at['%s %d' % (method, counter), i] = numbers.count(i)
        dfanswers.to_csv(path % ("Distribution\\Distribution by word test %s %d.csv" % (method, counter)), encoding='utf_8_sig')

dfdistribution.to_csv(path % "Distribution\\Distribution_Test.csv")

