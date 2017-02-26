import random
import re
class markov(object):
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words - 1)
        self.database()

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
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

	def generate_markov_text(self, size=25):
		begin = random.randint(0, self.word_size-2)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []
		for i in xrange(size):
			gen_words.append(w1)
			w1, w2 = w2, random.choice(self.cache[(w1, w2)])
		gen_words.append(w2)
		return ' '.join(gen_words)
