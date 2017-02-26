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
    print(text_new)
    print(splitedSong)
    return splitedSong

splitWord()