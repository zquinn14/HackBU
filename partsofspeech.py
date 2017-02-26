import tweets
import nltk
import re
import random

from wordToSyl import sylco

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

tweets.init()

statuses = tweets.get_statuses("realDonaldTrump")


tweet_sn = set()
tweet_pn = set()
tweet_a = set()

for status in statuses:
    tags = nltk.pos_tag(status)

    for tag in tags:
        word, part = tag

        if word[0].isupper(): continue

        if part.startswith("N"):
            if part.endswith("S"):
                tweet_pn.update({word})
            else:
                tweet_sn.update({word})
        elif part.startswith("J"):
            tweet_a.update({word})

sf = open("Data2.txt", "r")

songContents = sf.read()

sf.close()

songWords = []

for match in re.finditer(r"[a-zA-Z0-9'-]+", songContents):
    songWords.append(match.group())


tags = nltk.pos_tag(songWords)

song_pn = set()
song_sn = set()
song_a  = set()

for tag in tags:
    word, part = tag

    if word[0].isupper(): continue

    if part.startswith("N"):
        if part.endswith("S"):
            song_pn.update({word})
        else:
            song_sn.update({word})
    elif part.startswith("J"):
        song_a.update({word})

finalLines = []

for line in songContents.split("\n"):
    if not line:
        finalLines.append("")
        continue

    finalLine = []
    for word in re.split(r"\s+", line):
        match = re.match(r"\W*([a-zA-Z0-9'-]+)\W*", word)
        real_word = match.group(1)

        scount = sylco(real_word)

        replacement = real_word

        if real_word in song_pn:
            matching_syllables = []

            for tword in tweet_pn:
                if sylco(tword) == scount:
                    matching_syllables.append(tword)

            replacement = random.choice(matching_syllables)
        if real_word in song_sn:
            matching_syllables = []

            for tword in tweet_sn:
                if sylco(tword) == scount:
                    matching_syllables.append(tword)

            replacement = random.choice(matching_syllables)
        if real_word in song_a:
            matching_syllables = []

            for tword in tweet_a:
                if sylco(tword) == scount:
                    matching_syllables.append(tword)

            replacement = random.choice(matching_syllables)

        replacement = word.replace(real_word, replacement)

        finalLine.append(replacement)
    
    finalLines.append(" ".join(finalLine))


for line in finalLines:
    print(line)