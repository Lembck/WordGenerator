import json
import random
import timeit


words = []
sequences = {}
parts = {}

with open("words.txt", "r") as f:
    words = list(map(str.rstrip, f.readlines()))

with open("sequences.txt", "r") as g:
    sequences = json.loads(g.read())


with open("parts.txt", "r") as h:
    parts = json.loads(h.read())

vowels = "aeiouy"
consons = "bcdfghjklmnpqrstvwxz"

#conditional upper.()
def makeUpper(char, yes):
    if yes:
        return char.upper()
    return char

#converts "hello" to "Cvccv."
def convertToCV(word):
    seq = ""
    first = True
    for letter in word:
        if letter.lower() in vowels:
            seq += makeUpper("v", first or letter.isupper())
        elif letter.lower() in consons:
            seq += makeUpper("c", first or letter.isupper())
        else:
            seq += letter
        first = False
    return seq + "."

#sort for efficient weighted-random finding
def sortbyValue(given):
    return dict(sorted(given.items(), key=lambda item: item[1], reverse=True))

#update sequences.txt based on the words
def updateSequences(write):
    sequences = {}
    for word in words:
        word = word.rstrip()
        seq = convertToCV(word)
        if seq in sequences.keys():
            sequences[seq] += 1
        else:
            sequences[seq] = 1

    sequences = sortbyValue(sequences)

    if write:
        with open("sequences.txt", "w") as f:
            f.write(json.dumps(sequences))
    return sequences

#chooses a weighted-random sequence
def getRandomSequence():
    r = random.randint(0, len(words))
    chosenSeq = ""
    
    for seq in sequences.keys():
        if r <= 0:
            chosenSeq = seq
            break
        else:
            r -= sequences[seq]
    return(chosenSeq)


#outputs a random letter or group of letters that match the given format
#receives inputs like "V", "Cc", "vvv", or "cccc."
def getRandomLettersFromFormat(part):
    pair = parts[part]
    r = random.randint(0, pair[0])
    chosen = ""
    
    for part in pair[1].keys():
        if r <= pair[1][part]:
            chosen = part
            break
        else:
            r -= pair[1][part]

    return(chosen)

#Turns "hello" into ['h', 'e', 'll', 'o']
def getParts(word, partsSoFar):
    if partsSoFar == []:
        partsSoFar = [word[0]]
    elif word == "":
        return partsSoFar
    elif word[0] == partsSoFar[-1][0].lower() or word[0] == ".":
        partsSoFar[-1] += word[0]
    else:
        partsSoFar.append(word[0])
    return getParts(word[1:], partsSoFar)

#separate a word into its
#Converts "hello" -> (['C', 'v', 'cc', 'v.'], ['h', 'e', 'll', 'o.'])
def getLetterParts(word):
    parts = getParts(convertToCV(word), [])
    letterParts = []
    for part in parts:
        letterParts.append(word[:len(part)])
        word = word[len(part):]
    letterParts[-1] += "."
    return (parts, letterParts)


#update parts.txt with the current words
def updateParts(write):
    myDict = {}

    for word in words:
        sParts, lParts = getLetterParts(word)
        for (a, b) in zip(sParts, lParts):
            if a == "Ccc.":
                print(word)
            try:
                myDict[a][1][b] += 1
                myDict[a][0] += 1
            except KeyError:
                try:
                    myDict[a][1][b] = 1
                    myDict[a][0] += 1
                except KeyError:
                    myDict[a] = [1, {b : 1}]

    for seq in myDict.keys():
        myDict[seq][1] = sortbyValue(myDict[seq][1])

    myDict = dict(sorted(myDict.items(), key=lambda item: item[1][0], reverse=True))

    if write:
        with open("parts.txt", "w") as f:
            f.write(json.dumps(myDict))
    return myDict


#Generate one word
def getWord():
    seq = getRandomSequence()
    seqParts = getParts(seq, [])
    word = ""
    for part in seqParts:
        letter = getRandomLettersFromFormat(part)
        word += letter
    return(word[:-1])

#Generate multiple words
def getWords(num):
    for i in range(num):
        print(getWord())
