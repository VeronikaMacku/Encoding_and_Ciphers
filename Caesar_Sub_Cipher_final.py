#Monoalphabetic substitution cipher
#-------------------------------------
import string
import copy
#-------------------------------------
#CIPHER ALPHABET - EN
origAlphabet = string.ascii_uppercase
#-------------------------------------
#LANGUAGES
class Language:
    def __init__(self, lang, freq, bigram = None, trigram = None):
        self.lang = lang
        self.bigram = bigram
        self.trigram = trigram

        #Letters sorted by frequency before assigning to the object
        myLettersSorted = list()
        for letter, freq in freq.items():
            myLettersSorted.append((freq,letter))
        myLettersSorted.sort(reverse=True)

        sortedDict = dict()
        for freq, letter in myLettersSorted:
            sortedDict[letter.upper()] = freq
        self.freq = sortedDict

        #Alphabet sorted by decreasing frequency
        alphabetLANG = ""
        for letter, freq in self.freq.items():
            alphabetLANG += letter
        self.alphabetFreqDec = alphabetLANG

#FREQUENCY of letters + most common bigrams and trigrams    
#CZ - From: https://nlp.fi.muni.cz/cs/FrekvenceSlovLemmat
freqCZ = {"E":10.396,"A":8.74,"O":8.233,"I":7.597,"N":6.683,"T":5.537,"S":5.383,"R":5.113,"V":4.335,"L":4.056,"U":3.808,"K":3.715,"D":3.596,"C":3.589,"P":3.42,"M":3.23,"Z":3.114,"Y":2.667,"H":2.28,"J":1.963,"B":1.649,"F":0.39,"G":0.339,"X":0.092,"W":0.071,"Q":0.006}
biCZ = ["st","pr","ne","ni","po","ov","ro","en","na","je","te","le","ko","od","ra","to","ou","no","la","li","ho","do","os","se","ta","al","ed","an","ce","va","at","re","er","ti","em","in","sk","lo"]
triCZ = ["pro","ova","ost","pri","sta","pre","ter","eni","pod","kte","pra","eho","sti","red","kon","nos","ick","sou","ist","edn","ske","odn","tel","ani","ent","str","ove","nov","pol","spo","vat","nim","jak","val","dni","sto","tak","lov"]
langCZ = Language("CZ",freqCZ,biCZ,triCZ)
#EN - From: https://www3.nd.edu/~busiforc/handouts/cryptography/Letter%20Frequencies.html
freqEN = {"e":12.576,"t":9.085,"a":8.000,"o":7.591,"i":6.920,"n":6.904,"s":6.341,"h":6.237,"r":5.959,"d":4.318,"l":4.057,"u":2.842,"c":2.576,"m":2.561,"f":2.350,"w":2.225,"g":1.983,"y":1.901,"p":1.796,"b":1.536,"v":0.982,"k":0.740,"x":0.180,"j":0.145,"q":0.118,"z":0.079}
biEN = ["th","he","in","er","an","re","nd","on","en","at","ou","ed","ha","to","or","it","is","hi","es","ng"]
triEN = ["the","and","ing","her","hat","his","tha","ere","for","ent","ion","ter","was","you","ith","ver","all","wit","thi","tio"]
langEN = Language("EN",freqEN,biEN,triEN)
#-------------------------------------
#FUNCTIONS
#Text Manipulation
def translateText(origText, transDict):
    transTable = origText.maketrans(transDict)
    origText = origText.translate(transTable)

    return origText

def formatTextForCipher(sourceText):
    """Capitalizes all letters of the source text, stripts it of all punctuation and converts any CZ characters to ASCII."""
    
    #Capitalize all letters
    readyText = sourceText.upper()

    #Convert to ASCII characters
    czechCharstoASCIIdict={"Á":"A","Č":"C","Ď":"D","Ě":"E","É":"E","Í":"I","Ň":"N","Ó":"O","Ř":"R","Š":"S","Ť":"T","Ú":"U","Ů":"U","Ý":"Y","Ž":"Z"}
    readyText = translateText(readyText, czechCharstoASCIIdict)

    #Strip of everything but ASCII uppercase letters and space
    charsToDelete = ""
    for char in readyText:
        if not((char.isupper()and char.isascii()) or char == " "):
            charsToDelete += char
    for charD in charsToDelete:
        readyText = readyText.replace(charD,"")

    return readyText

def printPeek(origText, wholeText = False):
    if wholeText == True:
        print(origText)
    elif len(origText) > 2000:
        print(origText[0:2000],"\n")
    else:
        print(origText,"\n")

#MappingDict
def createMappingDict(origAlphabet, substWithAlphabet):
    """Returns a dictionary that maps two alphabets against each other mapDict = {origLetter : substLetter}."""
    mapDict = dict()
    for i in range(0,len(origAlphabet)):
        origLetter = origAlphabet[i]
        substLetter = substWithAlphabet[i]
        mapDict[origLetter] = substLetter

    return copy.deepcopy(mapDict)

def printMappingDict(mappingDict):
    """Prints the Mapping dictionary."""
    for origLetter, cipherLetter in mappingDict.items():
        print(f"Original:{origLetter}, Substitution:{cipherLetter}")
       
#Ciphering
def CaesarCipher(origAlphabet):
    """Returns the origAlphabet shifted by the given value."""
    while True:
        shiftBy = input("Enter the value to shift by: ")
        if shiftBy.isdecimal():
            shiftByValue = int(shiftBy)
            break
        else:
            print("Not a number.")

    #In case the entered number exceeds the length of the alphabet
    shiftByValue = shiftByValue % len(origAlphabet)

    shiftedAlphabet = origAlphabet[shiftByValue:] + origAlphabet[:shiftByValue]

    return shiftedAlphabet

def monoalphaSubstCipher(origAlphabet):
    """Returns the substitution Alphabet."""

    print("The original aplhabet is 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'. Enter the substitution alphabet as a string where the letters are in the order you want them to be mapped to the original alphabet, e.g. 'ZYXWVUTSRQPONMLKJIHGFEDCBA'.")
    while True: 
        substAlphabet = input("Enter the substitution alphabet: ")
        substAlphabet.upper()
        if (substAlphabet.isupper()) and (len(substAlphabet)==len(origAlphabet)):
            break
        else:
            print("The substitutive alphabet must consist of only letters and contain 26 of them.")

    return substAlphabet

def cipher(origAlphabet):
    """Acquires text from the user, prepares it for encryption, chooses a cypher and encrypts the source text."""
    #Acquiring text to be encrypted
    while True:
        sourceText = input("Enter text to be encrypted: ")
        if  0 < len(sourceText):
            break
    readyText = formatTextForCipher(sourceText)

    #Choosing the Cipher substition method
    while True:
        print("Choose encoding method. Enter '1' for Ceasar cipher. Enter '2' for Monoalphabetic substitution cipher.")
        userInput = input("Enter choice: ")
        if (userInput == "1"):      #Caesar
            substWithAlphabet = CaesarCipher(origAlphabet)
            break
        elif (userInput == "2"):    #Monoalphabetic substitution
            substWithAlphabet = monoalphaSubstCipher(origAlphabet)
            break

    #Generating the cipherDict = {originalLetter:substitutiveLetter}
    cipherDict = dict()
    cipherDict = createMappingDict(origAlphabet, substWithAlphabet)

    #Substituting all original characters with the cipher ones
    cipheredText = translateText(readyText,cipherDict)
    print(cipheredText)

#Deciphering
def freqAnalysis(theCipheredText):
    """Performs frequency analysis on the encrypted text.

    Creates dict = {letter : its relative frequency in %}, dictBiTOP20 = {bigram : frequency},dictTriTOP20 = {trigram : frequency} and returns the langCipher object to hold them."""
    cipherLetterFreq = dict()

    #Finding Bigrams and trigrams
    theCipheredTextSplitList = theCipheredText.split(' ')
    cipherBigram = dict()
    cipherTrigram = dict()
    for polyGram in theCipheredTextSplitList:
        for i in range(0,(len(polyGram) - 1)):
            gram = polyGram[i] + polyGram[i+1]
            if not(gram in cipherBigram):
                cipherBigram[gram] = 0
            cipherBigram[gram] += 1
        for i in range(0,(len(polyGram) - 2)):
            gram = polyGram[i] + polyGram[i+1] + polyGram[i+2]
            if not(gram in cipherTrigram):
                cipherTrigram[gram] = 0
            cipherTrigram[gram] += 1

    #Getting rid of all but 20 most frequent bigrams and trigrams
    for i in range (0,2):
        if i == 0:
            cipherGram = cipherBigram
        else:
            cipherGram = cipherTrigram

        myGramsSorted = list()
        for letters, freq in cipherGram.items():
            myGramsSorted.append((freq,letters.upper()))
        myGramsSorted.sort(reverse=True)

        if len(myGramsSorted) >=20:
            myGramsSorted = myGramsSorted[0:20]

        if i == 0:
            cipherBigram = myGramsSorted
        else:
            cipherTrigram = myGramsSorted

    #Strips text of spaces
    theCipheredText = theCipheredText.replace(" ","")

    #Finds absolute frequency
    sumOfLetters = 0
    for letter in theCipheredText:
        if not(letter in cipherLetterFreq):
            cipherLetterFreq[letter] = 0
        cipherLetterFreq[letter] += 1 
        sumOfLetters += 1

    #Calculates relative frequency (%)
    for letter, count in cipherLetterFreq.items():
        cipherLetterFreq[letter] = round(count/sumOfLetters*100, 3)

    langCIPHER = Language("CIPHER", copy.deepcopy(cipherLetterFreq), copy.deepcopy(cipherBigram), copy.deepcopy(cipherTrigram))
    return copy.deepcopy(langCIPHER)

def manualDecipher(theCipheredText, origAlphabet, langLANG, langCIPHER, decipherDict = None):
    """Has the user choose every letter swap."""
    print("You've entered the manual decipher mode. You can manually correct any errors here.\n")

    #To initialize swapping dictionary
    swapLettersDict = dict()
    if (decipherDict == None):
        swapLettersDict = createMappingDict(origAlphabet,origAlphabet)
    else:
        swapLettersDict = decipherDict

    #Manual decipher
    while True:
        #Frequency analysis
        #of Original language
        print(langLANG.lang, " - Alphabet letters, bigrams and trigrams ordered from most frequent to least frequent.")
        print("Alphabet: ", langLANG.freq)
        print("Alphabet: ", langLANG.alphabetFreqDec)
        print("Bigrams = ", langLANG.bigram)
        print("Trigrams = ", langLANG.trigram,"\n")
        #of Cipher text
        print(langCIPHER.lang, " - Alphabet letters, bigrams and trigrams ordered from most frequent to least frequent.")
        print("Alphabet: ", langCIPHER.freq)
        print("Alphabet: ", langCIPHER.alphabetFreqDec)
        print("Bigrams = ", langCIPHER.bigram)
        print("Trigrams = ", langCIPHER.trigram,"\n")

        #Deciphered text
        printPeek(translateText(theCipheredText, swapLettersDict))

        #User input
        print("To swap letters enter first the Cipher letter and right after the assumed Original letter, e.g. 'Ac' to swap all A's for c's. To undo a swap, enter a single letter, e.g. enter 'c' to swap back to 'A'.")
        print("To return to main menu enter 0.")
        userChoice = input("Enter choice: ")
        print("\n")
        if userChoice == "0":
            break
        elif (userChoice.isascii() and len(userChoice) == 1):
            for cipherLetter,origLetter in swapLettersDict.items():
                if (origLetter == userChoice.lower()):
                    swapLettersDict[cipherLetter] = cipherLetter
        elif (userChoice.isascii() and len(userChoice) == 2):
            swapLettersDict[userChoice[0].upper()] = userChoice[1].lower()
        else:
            print("Invalid input.")

    #The entire text is
    print("The whole deciphered text is: ")
    printPeek(translateText(theCipheredText, swapLettersDict), True)

def isCaesar(origAlphabet, alphabetLANG, alphabetCIPHER):
    """Tries to determine whether the original cipher might have been the Caesar cipher."""
    #Generates all possible alphabets and catalogues for each the shiftValue and how many pairs of n-th frequent chars are at the same index position in the original Alphabet and the shifted Alphabet
    shiftList = list()
    for shiftValue in range(0,len(origAlphabet)):
        shiftedAlphabet = origAlphabet[shiftValue:] + origAlphabet[:shiftValue]
        modus = 0
        for i in range(0, len(alphabetCIPHER)):
            indexCipherL = shiftedAlphabet.find(alphabetCIPHER[i])
            indexOrigL = origAlphabet.find(alphabetLANG[i])
            if indexCipherL == indexOrigL:
                modus += 1
        shiftList.append((modus, shiftValue))
    
    #Looks for the shiftValue with the highest amount of matches
    shiftValue = 0
    shiftModus = 0
    for item in shiftList:
        if item[0] > shiftModus:
            shiftModus = item[0]
            shiftValue = item[1]

    #If at least over 25 % of letter pairs have the same distance, function returns this shift value, otherwise 0 as FALSE
    if (shiftModus >= (0.25*len(alphabetCIPHER))):
        return shiftValue
    else:
        return 0

def monoAlphaSubReorder(langLANG, langCIPHER):
    """Tries to reordered the Alphabet according to the decreasing frequency of letters and common bigrams and trigrams."""
    langAlphabetFreqDec = (langLANG.alphabetFreqDec).lower()
    reorderedCiAL = ""
    reorderedLangAl = ""
    bigramLangPart = []
    trigramLangPart = []
    bigramCiPart = []
    trigramCiPart = []
    step = 4
    for i in range(0,(4*step+1),step):
        #Studies 8 letters at a time
        langPartAl = langAlphabetFreqDec[i:(i+step*2)]
        if len(langCIPHER.alphabetFreqDec) >= (step*2):
            cipherPartAl = langCIPHER.alphabetFreqDec[i:(i+step*2)]
        else:
            cipherPartAl = langCIPHER.alphabetFreqDec

        #Starts with 8 bigrams and trigrams to study adds 4 in each step
        if i == 0:
            startV = 0
            endV = step*2
        else:
            startV = i+step
            endV = i+2*step
        for j in range(startV,endV):
            if len(langCIPHER.bigram) > j:
                bigramCiPart.append(langCIPHER.bigram[j][1])
            if len(langCIPHER.trigram) > j:    
                trigramCiPart.append(langCIPHER.trigram[j][1])
            if len(langLANG.bigram) > j:
                bigramLangPart.append(langLANG.bigram[j])
            if len(langLANG.trigram) > j:    
                trigramLangPart.append(langLANG.trigram[j])
        
        #Studying  polygrams
        for m in range(0,2):    #Switchign between bigrams and trigrams
            for k in range(0,endV):
                if m == 1:      #Studying bigrams
                    if len(bigramCiPart) > k:
                        polyGramCi = bigramCiPart[k]
                    if len(bigramLangPart) > k:
                        polyGramLang = bigramLangPart[k]
                else:            #Studying Trigrams
                    if len(trigramCiPart) > k:
                        polyGramCi = trigramCiPart[k]
                    if len(trigramLangPart) > k:
                        polyGramLang = trigramLangPart[k]
                for l in range(0,len(polyGramCi)):
                    #If the polygram letter is in the taken part of Alphabet (for both Cipher and Lang) maps it
                    if not(cipherPartAl.find(polyGramCi[l]) == -1 or langPartAl.find(polyGramLang[l]) == -1):
                        #Given it's not already been mapped
                        if (reorderedCiAL.find(polyGramCi[l]) == -1 and reorderedLangAl.find(polyGramLang[l]) == -1):
                            reorderedCiAL += polyGramCi[l]
                            reorderedLangAl += polyGramLang[l]
    
    #Ordering the rest of alphabet by decreasing frequency
    for i in range(0,len(langAlphabetFreqDec)):
        if (reorderedLangAl.find(langAlphabetFreqDec[i]) == -1):
            reorderedLangAl += langAlphabetFreqDec[i]
    for i in range(0,len(langCIPHER.alphabetFreqDec)):
        if (reorderedCiAL.find(langCIPHER.alphabetFreqDec[i]) == -1):
            reorderedCiAL += langCIPHER.alphabetFreqDec[i]

    return (reorderedLangAl,reorderedCiAL)

def semiautomaticDecipher(theCipheredText, origAlphabet, langLANG, langCIPHER):
    """Tries to determine whether the used Cipher is Caesar or random Monoalphabetic subsitution and aid the user with deciphering the text."""
    #Creates language alphabet and cipher alphabet in which the letters are ordered from the most frequent to the least frequent
    alphabetLANG = langLANG.alphabetFreqDec
    alphabetCIPHER = langCIPHER.alphabetFreqDec

    #Is Caesar?
    shiftDist = isCaesar(origAlphabet, alphabetLANG, alphabetCIPHER)
    if shiftDist != 0 :
        print("The cipher used for this text was likely a Ceaser Cipher with a shift of: ", shiftDist,".")
    else:
        print("The program has concluded that Caesar Cipher likely wasn't used to encrypt the text.")

    #Caesar or Monoalphabetic Substitution? 
    print("Press 1 if you want to try to decipher as Caesar Cipher or 0 if you wish to decipher as Monoalphabetic substitution Cipher.")
    userChoice = input("Enter your choice: ")

    #Caesar
    if userChoice == "1":
        while True:
            substAlphabet = CaesarCipher(origAlphabet)
            decipherDict = createMappingDict(substAlphabet,origAlphabet.lower())
            printPeek(translateText(theCipheredText, decipherDict))
            userChoice = input("Enter 2 if the substitution has been performed correctly, 1 if you wish to try another shift or 0 if not: ")
            if userChoice == "2":
                print("The whole deciphered text is: ")
                printPeek(translateText(theCipheredText, decipherDict), True)
                return None
            elif userChoice == "0":
                break
    
    #Monoalphabetic Substitution
    if (langLANG.lang == "EN"):     #EN considers both relative frequency and common polygrams
        (reorderedLangAl,reorderedCiAL) = monoAlphaSubReorder(langLANG, langCIPHER)
        decipherDict = createMappingDict(reorderedCiAL, reorderedLangAl.lower())
    elif (langLANG.lang == "CZ"):   #CZ considers only relative frequency of letters
        decipherDict = createMappingDict(alphabetCIPHER,alphabetLANG.lower())
    printPeek(translateText(theCipheredText, decipherDict))

    print("Monoalphabetic substitution has been performed on the basis of frequency analysis. Has the substitution been performed correctly? Enter 'YES' or 'NO'.")
    userChoice = input("Enter your choice: ")
    if userChoice.upper() == "YES":
        print("The whole deciphered text is: ")
        printPeek(translateText(theCipheredText, decipherDict), True)
        return None
    else:
        manualDecipher(theCipheredText, origAlphabet, langLANG, langCIPHER, decipherDict)
    
def decipher(theCipheredText, origAlphabet, langLANG):
    """Performs decryption of the given text on the basis of frequency cryptoanalysis and the given language frequency analysis, and asks the user in which mode they want to decipher."""

    #Stripping all characters that are not ASCII or spaces
    theCipheredText = formatTextForCipher(theCipheredText)

    #Frequency Analysis of the Cipher (cipherLetterFreq = {Cipherletter : percentage}), the frequency is saved inside the LangCIPHER object
    langCIPHER = freqAnalysis(theCipheredText)

    #Working Mode
    print("Do you want to decipher the text manually or use semiautomatic mode? Enter 1 for manual or 2 for semiautomatic.")
    userInput = input("Enter choice: ")
    print("\n")
    if (userInput =="1"):       #Cipher
        manualDecipher(theCipheredText, origAlphabet, langLANG, langCIPHER)
    elif (userInput =="2"):     #Decipher
        semiautomaticDecipher(theCipheredText, origAlphabet, langLANG, langCIPHER)
#-------------------------------------
#MAIN()
while True:
    print("\nDo you want to cipher or decipher text? Enter 1 to cipher or 2 to decipher. Enter 0 to quit the program.")
    userInput = input("Enter choice: ")
    if (userInput =="1"):       #Cipher
        cipher(origAlphabet)
    elif (userInput =="2"):     #Decipher
        theCipheredText = input("Enter the text to be deciphered: ")
        while True:
            userChoice = input("In which language is the cipher text written? Enter 'CZ' or 'EN': ")
            if userChoice.upper() == "CZ":
                decipher(theCipheredText, origAlphabet, langCZ)
                break
            elif userChoice.upper() == "EN":
                decipher(theCipheredText, origAlphabet, langEN)
                break
    elif(userInput =="0"):
        break