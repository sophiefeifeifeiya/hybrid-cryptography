import base64
from PIL import Image


def fileToBase64(filename):
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')


def base64ToFile(encoded_string, outputFileName):
    data64decode = base64.decodebytes(encoded_string.encode('utf-8'))
    data_result = open(outputFileName, "wb")
    data_result.write(data64decode)


def makeSingleString(bigList):
    retData = ""
    dollar = "$$$$$$$$$$$$$$$$$$$$$$$$$"
    for listEle in bigList:
        msg = str(listEle)
        msg = msg + dollar
        msg = msg[0:42]
        retData = retData + msg
    return retData


def makeListFromString(longString):
    retData = []
    data = longString.split('$')
    for item in data:
        if len(item) > 0:
            retData.append(int(item))
    return retData


def encodeStringinImage(data, output_file, type, width=512, height=512):
    data = data.encode('utf-8')
    print("This is lenght of the data in image:", len(data))
    image_data = []
    i = 0

    for y in range(height):
        for x in range(width):
            if(i+2 < len(data)):
                temp = (4*data[i], 2*data[i+1], 2*data[i+2])
                i = i+3
                image_data.append(temp)
            else:
                image_data.append((255, 255, 255))

    # print(image_data)
    img = Image.new('RGB',  (width, height))
    img_data = img.load()

    index = 0
    for y in range(height):
        for x in range(width):
            img_data[x, y] = image_data[index]
            index += 1

    img.save(output_file, type)

def base64ToValue(data):
    AplhaTable = {"A": "00", "B": "01", "C": "02", "D": "03", "E": "04", "F": "05", "G": "06",
                  "H": "07", "I": "08", "J": "09", "K": "10", "L": "11", "M": "12", "N": "13",
                  "O": "14", "P": "15", "Q": "16", "R": "17", "S": "18", "T": "19", "U": "20",
                  "V": "21", "W": "22", "X": "23", "Y": "24", "Z": "25", "a": "26", "b": "27",
                  "c": "28", "d": "29", "e": "30", "f": "31", "g": "32", "h": "33", "i": "34",
                  "j": "35", "k": "36", "l": "37", "m": "38", "n": "39", "o": "40", "p": "41",
                  "q": "42", "r": "43", "s": "44", "t": "45", "u": "46", "v": "47", "w": "48",
                  "x": "49", "y": "50", "z": "51", "0": "52", "1": "53", "2": "54", "3": "55",
                  "4": "56", "5": "57", "6": "58", "7": "59", "8": "60", "9": "61", "+": "62",
                  "/": "63", "=": "64"}
    key = ""
    for i in data:
        key = key + AplhaTable[i]

    return key

