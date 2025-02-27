import pandas as pd
from main import path

# dfanswers = pd.read_csv(path % 'Answerlist.txt', sep=' ', lineterminator=',', index_col=0, skipinitialspace=True)
# dfanswers['Answer'] = True
# dfnonanswers = pd.read_csv(path % 'Nonanswerlist.txt', sep=' ', lineterminator=',', index_col=0, skipinitialspace=True)
# dfnonanswers['Answer'] = False
# dfwords = pd.concat([dfanswers, dfnonanswers])
# # dfwords.index = dfwords.index.str.lower()
# dfwords.to_csv(path % "Wordle.csv")

dfwords = pd.read_csv(path % 'Wordlist.txt', sep=' ', lineterminator=',', index_col=0, header=None)
dfwords['Answer'] = False
wordlist = list(dfwords.index)
dfanswers = pd.read_csv(path % 'Answerlist.txt', sep=' ', lineterminator=',', index_col=0, header=None)
answerlist = list(dfanswers.index)
for answer in answerlist:
    dfwords.at[answer, 'Answer'] = True
    dfcopy = dfwords[dfwords['Answer']==True]
# dfanswers['Answer'] = True
dfwords.to_csv(path % "Wordle.csv")


# dfwords = pd.read_csv(path % 'Wordlist.txt', sep=':', index_col=0, names=['Characters'])
# dfwords['Characters'] = dfwords['Characters'].str.replace(',', '')
# dfwords['Answer'] = False
# wordlist = list(dfwords.index)
# dfanswers = pd.read_csv(path % 'Answerlist.txt', comment='/', index_col=0)
# answerlist = list(dfanswers.index)
# for answer in answerlist:
#     dfwords.at[answer, 'Answer'] = True
#     dfcopy = dfwords[dfwords['Answer']==True]
# # dfanswers['Answer'] = True
# dfwords.to_csv(path % "Wordle.csv", encoding='utf_8_sig')
