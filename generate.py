import re

from Markov import Markov
from wordToSyl import sylco

def read_song():
    songfile = open("Data.txt", "r")

    song = songfile.read()

    songfile.close()

    return song


def generate(song, markov):
    output = []

    testbreak = True

    # @Incomplete: put punctuation back
    for line in song.split("\n"):
        start = True

        for word in re.split(r"\s+", line):
            scount = sylco(word)
            if start:
                print("Got a first word, with scount ", scount)
                first = markov.start_chain(scount)
                print(first.wordstr)
                output.append(first)

                start = False
            else:
                if testbreak:
                    print("Updating. Last word:", output[len(output)-1].wordstr, "syllable count:", scount)
                n = markov.update_chain(output[len(output)-1], scount)
                if testbreak:
                    print(n.wordstr)
                    testbreak = True
                output.append(n)
    
    return output
