#VZI - Huffman coding
#---------------------------
#Nodes
class Node:
    def __init__(self, freq, char = None, leafLeft = None, leafRight = None):
        self.freq = freq
        self.char = char
        self.prev = None
        self.next = None
        self.huffCode = ""
        self.leafLeft = leafLeft
        self.leafRight = leafRight

    #Getters
    def get_freq(self):
        return self.freq

    def get_char(self):
        return self.char

    def get_prev(self):
        return self.prev

    def get_next(self):
        return self.next

    def get_huffCode(self):
        return self.huffCode

    def get_leafLeft(self):
        return self.leafLeft

    def get_leafRight(self):
        return self.leafRight

    #Setters
    def set_prev(self, prev):
        self.prev = prev

    def set_next(self, nextN):
        self.next = nextN

    def set_huffCode(self, prefix):
        self.huffCode = prefix

    def set_leafLeft(self, leafLeft):
        self.leafLeft = leafLeft

    def set_leafRight(self, leafRight):
        self.leafRight = leafRight
#---------------------------
#List
class DoubleListChar:
    def __init__(self):
        #List
        self.head = None
        self.tail = None
        self.size = 0

    #Getters
    def get_head(self):
        return self.head

    def get_tail(self):
        return self.tail

    def get_size(self):
        return self.size

    #Adding/removing members
    def append(self, node):         #Adds node to the end of a list
        new_node = node

        if self.head == None:       #the first node
            self.head = new_node
            self.tail = self.head
        else:
            self.tail.set_next(new_node)
            new_node.set_prev(self.tail)
            self.tail = new_node

        self.size += 1

    def remove_first(self):         #Removes the first node in a list
        current_node = self.head

        if current_node != None:
            if current_node == self.tail:
                self.head = None
                self.tail = None
            else:
                next_node = current_node.get_next()
                next_node.set_prev(None)
                self.head = next_node

            self.size -= 1

    def insert(self, node):         #Inserts node into a list so it's in increasing order of frequency of char
        new_node = node   
        compare_node = self.head

        if compare_node != None:
            while compare_node.get_freq() < new_node.get_freq():
                compare_node = compare_node.get_next()
                if compare_node == None:
                    break
        
        if compare_node == None:
            self.append(new_node)
        else:
            if compare_node == self.head:
                next_node = self.head
                next_node.set_prev(new_node)
                new_node.set_next(next_node)
                self.head = new_node
            else:
                prev_node = compare_node.get_prev()
                prev_node.set_next(new_node)
                new_node.set_prev(prev_node)
                new_node.set_next(compare_node)
                compare_node.set_prev(new_node)
            self.size += 1

    def print_List(self):
        current_node = self.head
        while current_node != None:
            print("Char: ", current_node.char," Freq: ", current_node.freq)
            current_node = current_node.get_next()
    def print_ListRev(self):
        current_node = self.tail
        while current_node != None:
            print("Char: ", current_node.char," Freq: ", current_node.freq)
            current_node = current_node.get_prev()
#---------------------------
#Tree
class BinaryTreeHuff:
    def __init__(self, root = None):
        self.root = root
        self.huffDict = dict()

    #Getters
    def get_root(self):
        return self.root

    def get_huffDict(self):
        return self.huffDict

    #Setters
    def set_tail(self, tail):
        self.tail = tail

    def create_Huffman_Code(self):
        self.traverse_NLR(self.root, huffWrite=True)    #Traverses the tree and during it creates the HuffCodes for all chars
        self.traverse_NLR(self.root)                    #Traverses the tree and during it adds chars and their HuffCodes to Dict

    #Traverse
    def traverse_NLR(self, current_node, huffCodePrefix = "", huffWrite = False):   #Pre-order depth traversal
        if current_node == None:
            return None
        
        if huffWrite == True:       #Encoding Huffman
            current_node.set_huffCode(huffCodePrefix)
            self.traverse_NLR(current_node.get_leafLeft(), huffCodePrefix + "0", huffWrite=True)
            self.traverse_NLR(current_node.get_leafRight(), huffCodePrefix + "1", huffWrite=True)
        else:                       #Reading Huffman into a dictionary
            letter = current_node.char
            huffCode = current_node.get_huffCode()
            if letter != None:
                self.huffDict[letter] = huffCode
            self.traverse_NLR(current_node.get_leafLeft())
            self.traverse_NLR(current_node.get_leafRight())

    #Print
    def print_HuffCodeDict(self):
        print("The Huffman Coding: ")
        for letter, huffCode in self.huffDict.items():
            print(letter,":", huffCode)
#---------------------------
#MAIN()
#Getting text to encode
while True:
    print("What text do you want to encode?", end=" ")
    while True:
        print("The text must contain at least 2 different characters.")
        textToEncode = input("Enter the text to be encoded: ")

        #Frequency analysis
        freqDict = dict()
        for letter in textToEncode:
            if not(letter in freqDict):
                freqDict[letter] = 0
            freqDict[letter] += 1 

        if len(freqDict) >= 2:
            break

    #Creating a list to hold CharNodes (char and its frequency)
    charList = DoubleListChar()
    for letter, freq in freqDict.items():
        charNode = Node(freq,char = letter)
        charList.insert(charNode)

    #Converting charList into a Huffman Tree
    Alphabet = 2     #binary alphabet
    while (charList.size != 1):
        #Sum of first 2 members
        sumFreq = 0
        i = 0
        charNode = charList.get_head()
        while i < Alphabet:
            sumFreq += charNode.freq
            charNode = charNode.get_next()
            i += 1

        #Creating a new Huffman Node and inserting it into list
        huffN = Node(sumFreq, leafLeft = charList.get_head(), leafRight = charList.get_head().get_next())
        charList.insert(huffN)

        #Removing no longer needed members from the charList
        for i in range(0, Alphabet):
            charList.remove_first()
    huffmanTree = BinaryTreeHuff(charList.get_head())

    #Creating Huffman encoding
    huffmanTree.create_Huffman_Code()

    #Printing Huffman Encoding
    huffmanTree.print_HuffCodeDict()

    #Translate chars to Huffman codes
    transTable = textToEncode.maketrans(huffmanTree.get_huffDict())
    huffText= textToEncode.translate(transTable)
    print("The text encoded with Huffman coding is: ", huffText)

    if input("Press 1 to continue or press 0 to quit: \n") == "0":
        break

    print("\n")
