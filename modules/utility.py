from colored import fg,bg,stylize, attr
import pickle
import datetime

def convertLabelToNumber(label):
    if label == "interesting":
        return 1
    elif label == "boring":
        return 0
    else:
        raise ValueError(label + 'is not one of the predefined labels (interesting / boring)')


def convertNumberToLabel(number):
    if number == 1:
        return "interesting"
    elif number == 0:
        return "boring"
    else:
        raise ValueError(str(number) + 'is not one of the predefined numbers (0 / 1)')

def calculateAverage(list_of_numbers):
    return sum(list_of_numbers)/len(list_of_numbers)

def removeTrailingZero(decimalNumber):
    s = str(decimalNumber)
    return s.rstrip('0').rstrip('.') if '.' in s else s

def logStartOfScript():
    date_string = datetime.datetime.now().strftime("%d.%b.%Y - %H:%M:%S %z")
    print(stylize("START@ " + date_string, bg('dark_blue')+fg('white')+attr("bold") ))

def cPrint(text,color="blue"):
    print(stylize(text, fg(color)))

def printSeperator(color="red"):
    print(stylize("                                                        ",fg(color)+attr("reverse")))

def logWithTitle(title, text="noTextSet"):
    print("")
    print( stylize("------------- " + title + " -----------", bg("grey_42")+fg("white")+attr("bold")) )
    if(str(text) != "noTextSet"):
        print(text)


def logCommaSeparatedList(list):
    print(",".join(list))

def readFileContent(filepath):
    return open(filepath, "r").read()

def extendFilenameToFullFilepath(filepath, pathextension):
    return pathextension + filepath

def extendFilenameListToFullFilepathsList(filenames, pathextension):
    return list((map(lambda filename: extendFilenameToFullFilepath(filename, pathextension), filenames)))

def concatFileContentIntoList(filepaths):
    return list(map(readFileContent, filepaths))

def buildListOfSentences(text):
    return text.split("\n")

def save_classifier(path, classifier):
    file_pointer = open(path, 'wb')
    pickle.dump(classifier, file_pointer)
    file_pointer.close()

def load_classifier(path):
    file_pointer = open(path, 'rb')
    classifier = pickle.load(file_pointer)
    file_pointer.close()
    return classifier
