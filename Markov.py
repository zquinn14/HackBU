import random
import re
from Tester import splitWord
class Word:
    def __init__(self, wordstr, syllables):
        self.wordstr = wordstr
        self.syllables = syllables

    def __eq__(self, other):
        return self.wordstr == other.wordstr and self.syllables == other.syllables

    def __hash__(self):
        return hash(self.wordstr) + 31*hash(self.syllables)

class markov(object):
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.firstWords = []
        #self.words = self.file_to_words()
        #self.word_size = len(self.words - 1)
        #self.database()

    def add_to_chain(self, words):
        self.firstWords.append(words[0])
        for x in range(len(words)-1):
            if x in self.cache:
                self.cache[words[x]].append[words[x+1]]
            else:
                self.cache[words[x]] = [words[x]]

    def start_chain(self, syllables):
       matching_syllable = []
       for x in range(len(self.firstWords)-1):
           if self.firstWords[x].syllables == syllables:
               matching_syllable.append(self.firstWords[x])
       retWord = random.choice(matching_syllable)
       return retWord

    def update_chain(self, word, syllables):
        matching_syllables = []
        for x in range(len(self.cache[word])-1):
            if self.cache[word].syllables == syllables:
                matching_syllables.append(self.cache[word])
        if len(matching_syllables) != 0:
            retWord = random.choice(matching_syllables)
            return retWord
        else:
            retWord = random.choice(self.cache[word])
            return retWord






'''
    def file_to_words(self):
        self.open_file.seek(0)
        data = self.splitWord()
        words = data.split()    #list of words
        return words

   def doubles(self):
        if len(self.words) < 2:
            return
        for i in range(len(self.words) - 1):
            yield(self.words[i], self.words[i + 1])

    def dataset(self):
        for w1, w2 in self.doubles():
            start = (w1)
            if start in self.cache:
                self.cache[start].append(w2)
            else:
                self.cache[start] = [w1]

    def generate_markov_text(self):
        begin = random.randint(0, self.word_size-2)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
	gen_words = []
	for i in range(len(self.words) - 1):
		gen_words.append(w1)
		w1, w2 = w2, random.choice(self.cache[(w1, w2)])
	gen_words.append(w2)
	return ' '.join(gen_words)

    def start_chain(syllables):'''


words1 = ["hey", " i "]
print(words1)
d = markov("Data.txt")
d.add_to_chain(words1)
