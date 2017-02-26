import random
import re

def splitWord():
    file = open("Data.txt", "r")
    text = file.read()
    #print(text)
    text = re.sub('\(|\)' , ' ', text)
    text = re.sub(',', ' ', text)
    splitedSong = text.split()

    writtenfile = open("Edited.txt", "w")
    writtenfile.write(' '.join(splitedSong))
    writtenfile.close()
    file_new = open("Edited.txt", "r")
    text_new = file_new.read()
    return splitedSong


class Markov(object):
    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.dataset()

    def file_to_words(self):
        self.open_file.seek(0)
        words = splitWord()
        return words

    def doubles(self):
        if len(self.words) < 2:
            return
        for i in range(len(self.words) - 1):
            yield(self.words[i], self.words[i + 1])

    def dataset(self):
        for w1, w2 in self.doubles():
            start = w1
            if start in self.cache:
                self.cache[start].append(w2)
            else:
                self.cache[start] = [w2]

    def generate_markov_text(self):
        begin = random.randint(0, self.word_size)
        seed_word = self.words[begin]
        w1 = seed_word
        gen_words = [w1]
        for i in range(10):
            w2 = random.choice(self.cache[w1])
            gen_words.append(w2)
            w1 = w2
        return ' '.join(gen_words)

def main():
    file_ = open('Data.txt')
    test = Markov(file_)
    print(test.generate_markov_text())
main()
