from Markov import Markov, Word
import generate
import tweets
from wordToSyl import sylco

tweets.init()

statuses = tweets.get_statuses("realDonaldTrump")

tweetWords = []
for status in statuses:
    tweetWord = []
    for word in status:
        tweetWord.append(Word(word, sylco(word)))
    tweetWords.append(tweetWord)


markov = Markov()

for tweet in tweetWords:
    if len(tweet) == 0:
        continue
    markov.add_to_chain(tweet)

songText = generate.read_song()

output = generate.generate(songText, markov)

outputStrings = []
for word in output:
    outputStrings.append(word.wordstr)

print(outputStrings)