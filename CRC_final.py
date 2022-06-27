# CRC coding and decoding
#------------------------------------------------
from enum import Enum
import copy
#------------------------------------------------
class polyType(Enum):
    generator = 1
    message = 2
    transmitted = 3
    received = 4
#------------------------------------------------
#Functions()
def enterPoly(enumPolyType):
    '''Takes a polynomial from the user and returns it as a string.'''

    print("Enter the polynomial in the binary format, e.g. enter P(x) = x^3 + x + 1 as 1011.")
    userInput = None
    polyEntered = False

    if enumPolyType == polyType.generator:
        print("Some common generator polynomials are G1(x) = 11, G2(x) = 1011, G3(x) = 1101, G4(x) = 11101, G5(x) = 10111. Or you can enter another." )

    while not(polyEntered):  
        userInput = input("Enter the polynomial: ")
        for i in range (0, len(userInput)):
            if not(userInput[i] == "0" or userInput[i] == "1"):
                print("You've entered invalid characters. Please, try again.") 
                break
            if (enumPolyType == polyType.generator):
                if (userInput[0] != "1" or userInput[-1] != "1"):
                    print("The generator polynomial must start and end with '1'.") 
                    break
            if i == (len(userInput) - 1):
                polyEntered = True
    
    return userInput

def printPoly(poly, enumPolyType):
    '''Accepts a string and prints it as P(x) = x^n + ... + x^2 + x + 1, where n is the degree of the polynomial.'''
    
    if enumPolyType == polyType.generator:
        print("The generator polynomial is g(x) = ", end="")
    elif enumPolyType == polyType.message:
        print("The mesage polynomial is m(x) = ", end="")
    elif enumPolyType == polyType.transmitted:
        print("The transmitted polynomial is t(x) = ", end="")
    elif enumPolyType == polyType.received:
        print("The received polynomial is r(x) = ", end="")

    for i in range(0, (len(poly))):
        if (poly[i] == "1"):
            if (i > 0):
                print(" + ", end="")
            if (i == (len(poly)-1)):
                print("1", end="")
            else:
                power = len(poly) - i - 1
                print(f"x^{power}", end="")
    print("\n")

def getPoly(enumPolyType):
    '''Returns the polynomial as a string.'''
    poly = None
    
    if enumPolyType == polyType.generator:
        print("Enter the generator polynomial g(x).")
    elif enumPolyType == polyType.message:
        print("Enter the message polynomial m(x).")
    elif enumPolyType == polyType.received:
        print("Enter the received polynomial r(x).")

    poly = enterPoly(enumPolyType)
    printPoly(poly, enumPolyType)

    return poly

def dividePoly(dividentPoly, divisorPoly):
    """Returns the quotient and the remainder of the division of dividentPoly by divisorPoly."""
    lenDifference = len(dividentPoly) - len(divisorPoly)
    quotientPoly =""

    for j in range(0,(lenDifference+1)):   #removes leading zeros
        if (dividentPoly[j] == "1"):       
            dividentPoly = dividentPoly[j:]
            break
        if (j == lenDifference):   #in case no break occurs in previous if (dividentPoly cannot be divided)
            remainderPoly = dividentPoly[(j+1):]
            quotientPoly ="0"
            return (quotientPoly, remainderPoly)

    while(len(divisorPoly) <= len(dividentPoly)):
        rPoly=""
        if (dividentPoly[0]=="1"):
            for i in range(0,len(divisorPoly)):       #bitwise XOR
                if (divisorPoly[i]!=dividentPoly[i]):
                    rPoly += "1"
                else:
                    rPoly += "0"
                
                if(i == (len(divisorPoly)-1)):   #replaces the summed part of dividentPoly with remainder
                    dividentPoly = rPoly + dividentPoly[(i+1):]
                    quotientPoly += "1"
                    dividentPoly = dividentPoly[1:]     #removes leading zero
        else:
            dividentPoly = dividentPoly[1:]     #removes leading zero
            quotientPoly += "0"

    remainderPoly = dividentPoly

    return (quotientPoly, remainderPoly)

def getTransmittedPoly(mesPoly, generPoly):
    '''Converts the message polynomial mesPoly into the transmitted polynomial tPoly.
    
    Shifts mesPoly by the degree of the generator polynomial generPoly, adds the remainder of mesPoly % generPoly to mesPoly forming tPoly and returns tPoly as a string.'''
    #Shifting the messagePoly by the degree of the generator Poly
    tPoly = mesPoly
    i = 0
    while i < (len(generPoly)-1):
        tPoly += "0"
        i += 1

    #Getting the remainder to add to the message
    (quoPoly,rPoly) = dividePoly(tPoly, generPoly)
    print(f"The CRC safety bits {rPoly} have been added to the message bits.")
    tPoly = mesPoly + rPoly

    return tPoly

def getControlPoly(mesPoly, generPoly):
    """Returns either the control polynomial or value None in case it cannot be created."""
    degreePoly = "1"
    i = 0
    while i < (len(mesPoly)-1):
        degreePoly += "0"
        i += 1
    degreePoly += "1"
    (controlPoly, remainderPoly) = dividePoly(degreePoly, generPoly)

    if (int(remainderPoly) > 0):
        print(f"Invalid combination of a generator polynomial and a received polynomial. This generator polynomial cannot produce a codeword of length n = {len(mesPoly)}. It does not meet the requirement of (x^n - 1) mod g(x) = 0.")
        return None
    return controlPoly

def correctErrors(recPoly, generPoly, controlPoly):
    '''Checks the received poynomial recPoly for errors and (if there are any) attempts to correct them.'''
    #Generating the Error Syndrome
    numOfRows = len(recPoly) - (len(controlPoly)-1)
    (syndromePoly, pos) = getSyndrome(recPoly, controlPoly, numOfRows)

    print(f"Syndrome:[{syndromePoly}]'. The position of the affected bit:{pos}. (The leftmost bit is considered to be at postion 0.)")

    if (int(syndromePoly,2) == 0):
        print("The information arrived without a mistake. No correction must be done.")
    else:
        print(f"The information arrived with a mistake.", end=" ")
        
        #Flipping the affected bit
        fixedPoly = ""
        for i in range(0,len(recPoly)):
            if (i == pos):
                if (recPoly[pos] == "0"):
                    fixedPoly += "1"
                else:
                    fixedPoly += "0"
            else:
                fixedPoly += recPoly[i]

        recPoly = fixedPoly
        print(f"The correct codeword is: {recPoly}")
    
    return recPoly

def getSyndrome(recPoly, cPoly, numOfRows):
    "Accepts received polynomial, control Polynomial, the number of rows in the matrix and returns the error syndrome and the affected bit position."
    
    #Creating the control matrix
    matrixH = list()
    matrixRow = list()

    print("ControlMatrix:")
    for i in range(0, numOfRows):
        for j in range(0,len(recPoly)):
            matrixRow.append("0")
        for k in range(0,len(cPoly)):
            matrixRow[-(i+k+1)] = cPoly[k]
        print(matrixRow)

        matrixH.append(copy.deepcopy(matrixRow))
        matrixRow.clear()

    #Calculating the Syndrome
    syndrome = list()
    for i in range(0, numOfRows):
        sumRow = 0
        for j in range(0,len(recPoly)):
            if ((matrixH[i][j] == "1") and (recPoly[j] == "1")):
                sumRow += 1
        
        syndRow = (sumRow % 2)
        syndrome.append(str(syndRow))

    #Determining which column the syndrome is identical too
    pos = None
    isPos = False
    for j in range(0,len(recPoly)):
        for i in range(0, numOfRows):
            if (syndrome[i] == matrixH[i][j]):
                if (i == (numOfRows-1)):
                    isPos = True
                continue
            else:
                break
        
        if (isPos):
            pos = j
            break

    #Converting syndrome into a string
    syndromePoly = ""
    for row in syndrome:
        syndromePoly += row
        
    return (syndromePoly, pos)

def codeCRC(mPoly, gPoly, enumPolyType):
    '''Encodes the message with CRC.'''
    tPoly = getTransmittedPoly(mPoly, gPoly) 
    print("The transmitted codeword is:", tPoly,"\n")

def decodeCRC(mPoly, gPoly, enumPolyType):
    '''Decodes the message with CRC.'''
    #Finding control Polynomial
    controlPoly = getControlPoly(mPoly, gPoly)
    if (controlPoly == None):  #Invalid combination of mPoly and gPoly, Fails the condition (x^n-1) mod g(x) = 0
        return None
    else:   #Valid combination of mPoly and gPoly
        recPoly = correctErrors(mPoly, gPoly, controlPoly)
        print("The received codeword is:", recPoly,"\n")
#------------------------------------------------
#main()
while True:
    #Code or Decode?
    print("Press 1 to encode m(x). Press 2 to decode m(x). Press 0 to quit the program.")
    choice = int(input())
    if (choice == 1):
        #Getting user input
        gPoly = getPoly(polyType.generator) #generator polynomial g(x)
        mPoly = getPoly(polyType.message)   #message polynomial m(x)

        #Forming Codeword
        codeCRC(mPoly, gPoly, polyType.transmitted)
    elif (choice == 2):
        #Getting user input
        gPoly = getPoly(polyType.generator) #generator polynomial g(x)
        while True:
            mPoly = getPoly(polyType.received)  #message polynomial m(x)
            if (len(mPoly) >= len(gPoly)):
                break
            else:
                print("The received polynomial must not be smaller than the generator polynomial.")
        
        #Checking codeword
        decodeCRC(mPoly, gPoly, polyType.received)
    else:
        break