from bisect import bisect_left
from pyvi import ViUtils

MAX_LENGTH = 5


def count_word(s):
    s = s + ' '
    cnt = 0
    for i in range(len(s)):
        if s[i] == ' ' and i > 0 and s[i - 1] != ' ':
            cnt += 1
    return cnt


def replaceWord(sentences, listS, sReplace):
    s2 = sentences
    for ch in ['.', ',', '?']:
        s2 = s2.replace(ch, '')
    listWords = s2.split()
    for i in range(MAX_LENGTH, 0, -1):
        listA = listS[i - 1]
        if len(listA) == 0:
            continue
        for j in range(len(listWords) - i + 1):
            word = listWords[j]
            for k in range(j + 1, j + i):
                word = word + ' ' + listWords[k]
            x = bisect_left(listA, word)
            if x != len(listA) and listA[x] == word:
                listWords[j] = sReplace
                for k in range(j + 1, j + i):
                    listWords[k] = ''

    s2 = ''
    for word in listWords:
        if word is not None and word != '':
            s2 = s2 + ' ' + word
    return s2[1:]


def fileToList(fileName):
    fileStopWord = open(fileName, encoding='utf8')
    listS = [[] for i in range(MAX_LENGTH)]
    while True:
        s = fileStopWord.readline().replace('\n', '').lower()
        if s is None or s == '':
            break
        listS[count_word(s) - 1].append(s)

    for i in range(MAX_LENGTH):
        listS[i].sort()
    return listS


def replaceWordRemoveAccents(sentences, listS, sReplace):
    s2 = sentences
    for ch in ['.', ',', '?']:
        s2 = s2.replace(ch, '')
    listWords = s2.split()
    for i in range(MAX_LENGTH, 0, -1):
        listA = listS[i - 1]
        if len(listA) == 0:
            continue
        for j in range(len(listWords) - i + 1):
            word = listWords[j]
            for k in range(j + 1, j + i):
                word = word + ' ' + listWords[k]
            word = ViUtils.remove_accents(word).decode('utf8')
            x = bisect_left(listA, word)
            if x != len(listA) and listA[x] == word:
                listWords[j] = sReplace
                for k in range(j + 1, j + i):
                    listWords[k] = ''

    s2 = ''
    for word in listWords:
        if word is not None and word != '':
            s2 = s2 + ' ' + word
    return s2[1:]


def fileToListRemoveAccents(fileName):
    fileStopWord = open(fileName, encoding='utf8')
    listS = [[] for i in range(MAX_LENGTH)]
    while True:
        s = fileStopWord.readline().replace('\n', '').lower()
        s = ViUtils.remove_accents(s).decode('utf8')
        if s is None or s == '':
            break
        listS[count_word(s) - 1].append(s)

    for i in range(MAX_LENGTH):
        listS[i].sort()
    return listS


def getPrepare(sentence):
    sentence = sentence.lower()
    s2 = replaceWord(sentence, listStopWord, '')
    s2 = replaceWord(s2, list2, '')
    s3 = replaceWordRemoveAccents(s2, listLocation, 'hà nội')
    s3 = replaceWordRemoveAccents(s3, listTime, 'hôm nay')
    return s3


if __name__ == '__main__':
    listStopWord = fileToList('vietnamese_stopwords.txt')
    list2 = fileToList('loaibo2.txt')
    listLocation = fileToListRemoveAccents('data.txt')
    listTime = fileToListRemoveAccents('homnay.txt')
    with open('a.txt', encoding='utf8') as file:
        data = file.read().splitlines()

    for sentence in data:
        # sentence = sentence.replace('\n', '')
        if sentence is None or sentence == '':
            continue
        # print(getPrepare(sentence))
    for s in listStopWord[0]:
        print(s)
