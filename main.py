import sys
import re
import PyPDF2
import logging
import io
logging.basicConfig(filename="log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

regexPatternToFind = "\d*"
regexGroupNumber = 0
regexInLine = True


def extensionFromPdfToTxt(filenamePdf):
    filenameToTxt = filenamePdf
    filenameToTxt = filenameToTxt.replace(".pdf",".txt")
    return filenameToTxt
def createAndSaveTxtFileFromOpenedPdf(text, filenameToTxt):
    fileTxt = open(filenameToTxt, "w")
    fileTxt.write(text)
    fileTxt.write("\n")
    fileTxt.close()

def isFileTypePdf(filename):
    return filename.endswith(".pdf")
def isFileTypeTxt(filename):
    return filename.endswith(".txt")
def appendCsvFindToFilename(filename):
    filenameCsvWithFind = filename[:len(filename) - 4]
    filenameCsvWithFind = filenameCsvWithFind + "_CsvFind.txt"
    return filenameCsvWithFind

def writeCsvWithRegexMatch_RegexInLine(fileCsvWithFind, text):
    bufText = io.StringIO(text)
    for line in bufText.readlines():
        regexMatches = re.finditer(regexPatternToFind,line)
        for regexMatch in regexMatches:
            if(regexMatch):
                foundRegexGroup = regexMatch.group(regexGroupNumber)
                if(foundRegexGroup):
                    stringToWrite = foundRegexGroup + " \t " + line
                    fileCsvWithFind.write(stringToWrite)

def writeCsvWithRegexMatch_RegexNotInLine(fileCsvWithFind, text):
    regexMatches = re.finditer(regexPatternToFind,text)
    for regexMatch in regexMatches:
        if(regexMatch):
            foundRegexGroup = regexMatch.group(regexGroupNumber)
            if(foundRegexGroup):
                fileCsvWithFind.write(foundRegexGroup + "\n")

def extractTextFromPdf(reader):
    text = ""
    for page in reader.pages:
        text = text + page.extract_text()
    return text

def main():
    filename = sys.argv[1]
    if( not(isFileTypePdf(filename) or isFileTypeTxt(filename)) ):
        logging.error("tried to open a non supported file: ",filename)
        sys.exit("Error: This script only accepts file ending with .pdf or .txt")
    if(isFileTypePdf(filename)):
        try:
            reader = PyPDF2.PdfReader(filename)
            logging.info("opened file: "+ filename)
            text = extractTextFromPdf(reader)
            logging.info("file " + filename + " is pdf and is going to be converted to txt")
            createAndSaveTxtFileFromOpenedPdf(text, extensionFromPdfToTxt(filename))
            logging.info("file " + filename + " converted into " + extensionFromPdfToTxt(filename))
        except Exception:
            logging.error(sys.exc_info()[1])
            sys.exit(print(sys.exc_info()[1]))
    elif(isFileTypeTxt(filename)):
        try:
            txtFile = open(filename, "r")
            text=txtFile.read()
            txtFile.close()
            logging.info("opened file: "+ filename)
        except Exception:
            logging.error(sys.exc_info()[1])
            sys.exit(print(sys.exc_info()[1]))

    fileCsvWithFind = open(appendCsvFindToFilename(filename), "w")
    logging.info("opened file where the regex match will be written with name: "+appendCsvFindToFilename(filename))
    if(regexInLine):
        fileCsvWithFind.write("MATCH \t CONTEXT \n")
        writeCsvWithRegexMatch_RegexInLine(fileCsvWithFind, text)
    else:
        fileCsvWithFind.write("MATCH \n")
        writeCsvWithRegexMatch_RegexNotInLine(fileCsvWithFind, text)
    fileCsvWithFind.close()


if __name__ == '__main__':
    sys.exit(main())
