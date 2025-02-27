import pandas as pd
import time

language = 'Italian'
path = 'C:\\Users\\Admin\\Documents\\Personal Documents\\Miscellaneous\\Wordle\\%s\\%s' % (language, '%s')


def letterfrequency(wordlist, letterlist=None):
    if language == 'Mandarin':
        letterlist_full = ['ㄅ', 'ㄆ', 'ㄇ', 'ㄈ', 'ㄉ', 'ㄊ', 'ㄋ', 'ㄌ', 'ㄍ', 'ㄎ', 'ㄏ', 'ㄐ', 'ㄑ', 'ㄒ', 'ㄓ', 'ㄔ',
                           'ㄕ', 'ㄖ', 'ㄗ', 'ㄘ', 'ㄙ', 'ㄧ', 'ㄨ', 'ㄩ', 'ㄚ', 'ㄛ', 'ㄜ', 'ㄝ', 'ㄞ', 'ㄟ', 'ㄠ', 'ㄡ',
                           'ㄢ', 'ㄣ', 'ㄤ', 'ㄥ', 'ㄦ']
    else:
        letterlist_full = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                           's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if letterlist is None:
        letterlist = letterlist_full
    dfletters = pd.DataFrame(index=letterlist_full)
    dfletters['Total'] = 0
    dfletters['Position 1'] = 0
    dfletters['Position 2'] = 0
    dfletters['Position 3'] = 0
    dfletters['Position 4'] = 0
    dfletters['Position 5'] = 0

    for letter in letterlist:
        for word in wordlist:
            if letter in word:
                dfletters.at[letter, 'Total'] += 1
            for pos in range(1, 6):
                if letter == word[pos - 1]:
                    dfletters.at[letter, 'Position %d' % pos] += 1

    return dfletters


def positions(word, letter):
    letter_pos = []
    if letter in word:
        counter = 0
        for i in word:
            if i == letter:
                letter_pos.append(counter)
            counter = counter + 1

    return letter_pos


def wordranking(df, answerlist=None):
    dfwords = df
    wordlist = dfwords.index.values
    if answerlist == None:
        answerlist = dfwords[dfwords['Answer'] == True].index.values
    length = len(answerlist)
    # if length <= 10:
    #     dfselection = letterfrequency(answerlist)
    #     dfselection = dfselection[dfselection['Total'] >= 1]
    #     dfselection = dfselection[dfselection['Total'] < length]
    #     selected_letters = dfselection.index.values
    #     print(selected_letters)
    #     dfletters = letterfrequency(answerlist, selected_letters)
    # else:
    dfletters = letterfrequency(answerlist)
    # else:
    for word in wordlist:
        # total_occurrence = 0
        # total_green = 0
        # total_yellow = 0
        total_score = 0
        for letter in set(word):
            occurrence = dfletters.at[letter, 'Total']
            # total_occurrence += occurrence
            if word.count(letter) == 1:
                pos = word.index(letter)
                green = dfletters.at[letter, 'Position %d' % (pos + 1)]
                # total_green += green
                # yellow = occurrence - green
                # total_yellow += yellow
                score = length * occurrence + occurrence * green - occurrence ** 2 - green ** 2
                total_score += score
            else:
                letter_green = 0
                for pos in positions(word, letter):
                    green = dfletters.at[letter, 'Position %d' % (pos + 1)]
                    letter_green += green
                    # total_green += green
                    score = 0.5 * green * (length + occurrence) - green ** 2
                    total_score += score
                # total_yellow += occurrence - letter_green
                total_score += 0.5 * (length - occurrence) * occurrence

        dfwords.at[word, 'Score'] = total_score
        # dfwords.at[word, 'Occurrence'] = total_occurrence
        # dfwords.at[word, 'Green'] = total_green
        # dfwords.at[word, 'Yellow'] = total_yellow

    # dfwords['Weighted Sum'] = dfwords['Green'] + 0.5 * dfwords['Yellow']
    return dfwords


def topword(dfwords, method, answerlist=None):
    dfwords = wordranking(dfwords, answerlist)
    if method in dfwords.columns:
        column = method
    else:
        dfwords['New Weighted Sum'] = dfwords['Green'] + method * dfwords['Yellow']
        column = 'New Weighted Sum'
    dfcolumn = dfwords[column]
    top = dfcolumn.astype(float).idxmax()

    return top


if __name__ == '__main__':
    df = pd.read_csv(path % 'Wordle.csv', index_col=0)
    wordlist = df.index.values
    answerlist = df[df['Answer'] == True].index.values
    dfletters = letterfrequency(answerlist)
    dfletters.to_csv(path % "WordleLetters_Answer_List.csv", encoding='utf_8_sig')
    # testlist = ['match', 'watch', 'hatch', 'batch', 'catch']
    starttime = time.time()
    dfwords = wordranking(df)
    dfwords.to_csv(path % "WordsRanking.csv", encoding='utf_8_sig')
    print(topword(df, 'Score'))
    # dftest = wordranking(df, testlist)
    # print(topword(df, 'Score', testlist))
    # print(df)
    # dftest = wordranking(df, testlist)
    # dftest.to_csv(path % "WordsTest.csv")
    endtime = time.time()

    print(endtime - starttime)
