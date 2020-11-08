import doctext # used to handle docx files
import operator 
import time
import os # handles our files

CONVERSATIONS_FILE_DIRECTORY = "./Conversations_V3"
CONVERSATIONS_TEXT_FILE_DIRECTORY = "./Conversations_Text"

def openDocxFile(filename: str):
    doc_text = doctext.DocFile(doc=filename)
    text = doc_text.get_text() 
    return text


def openTextFile(filename: str):
    file = open(filename, 'r')
    return file.read()


def getFilesForPath(path: str):
    f = []
    count = 0
    for (dirpath, dirnames, filenames) in os.walk(path):
        count += 1
        f.extend(filenames)
        return(f)


def getDirectories(path: str):
    directories = [x[1] for x in os.walk(path)]
    non_empty_dirs = [x for x in directories if x] # filter out empty lists
    return [item for subitem in non_empty_dirs for item in subitem]


def filterOutStringsFromDocxFile(docx):
    for word in docx.split(' '):
        if '@web.ca.libraryh3lp.com:' in word or '@chat.ca.libraryh3lp.com:' in word or ' ca.libraryh3lp.com:' in word:
            docx = docx.replace(word, '')
        if 'PM' in word or 'AM' in word : 
            docx = docx.replace(word, word[:-7])
    
    return docx


def filterOutTimeAndUserIdFromFile(docx: str):
    text = ""
    for sentence in docx.split('\n'):
        if '@web.ca.libraryh3lp.com:' in sentence or '@chat.ca.libraryh3lp.com:' in sentence or ' ca.libraryh3lp.com:' in sentence: 
            try:
                text += sentence[sentence.index(".com:")+5:]
                text += '\n\n'
            except ValueError:
                text = text
        
    return(text)


def segmentTranscriptIntoConversationsWithNoStartAndEnd(docx: str):

    conversationPosition = 0
    conversations = [[]]
    for sentence in docx.split('\n'):
        if 'System message: Hello' in sentence:
            conversations.append([])
            conversationPosition += 1
        else:
            conversations[conversationPosition].append(sentence)
    print('Number of Conversations counted were ' + str(conversationPosition))
    writeConversations(conversations)


def writeConversations(conversations: str):

    if not os.path.exists(CONVERSATIONS_FILE_DIRECTORY):
        try:
            os.makedirs(CONVERSATIONS_FILE_DIRECTORY)
        except OSError:
            print ("Creation of the directory %s failed" % CONVERSATIONS_FILE_DIRECTORY)
        else:
            print ("Successfully created the directory %s you can find your files there." % CONVERSATIONS_FILE_DIRECTORY)
    

    for i in range(len(conversations)):
        f = open(CONVERSATIONS_FILE_DIRECTORY + '/conversation_' + str(i+1) + '.txt', 'w')
        conversation = ''
        for sentence in conversations[i]:
            if sentence == '':
                conversation += '\n'
            else:
                conversation += sentence
        f.write(conversation)
        f.close()


def getChatTextFilesFromFolders():

    directoryName = "./carleton-txt/"
    mainDirectory = getDirectories(directoryName)
    textChatCount = 1
    for folder in mainDirectory:
        s = directoryName + folder
        textFiles = getFilesForPath(s)
        for textFile in textFiles:
            writeTextChats(openTextFile(s + "/" + textFile), textChatCount)
            textChatCount += 1
            

def writeTextChats(textFile: str, current: int):
    if not os.path.exists(CONVERSATIONS_TEXT_FILE_DIRECTORY):
        try:
            os.makedirs(CONVERSATIONS_TEXT_FILE_DIRECTORY)
        except OSError:
            print ("Creation of the directory %s failed" % CONVERSATIONS_TEXT_FILE_DIRECTORY)
        else:
            print ("Successfully created the directory %s you can find your files there." % CONVERSATIONS_TEXT_FILE_DIRECTORY)
    
    text = ""
    for sentence in textFile.split('\n'):
        try:
            text += sentence[sentence.index(".com:")+5:]
            text += '\n\n'
        except ValueError:
            text = text
    
    f = open(CONVERSATIONS_TEXT_FILE_DIRECTORY + "/TextConversation_" + str(current) + '.txt', 'w')
    f.write(text)
    f.close()


def main():

    start = time.time()
    
    docxText = openDocxFile('./transcripts_example.docx')
    filteredString = filterOutTimeAndUserIdFromFile(docxText)
    segmentTranscriptIntoConversationsWithNoStartAndEnd(filteredString)

    getChatTextFilesFromFolders()
    end = time.time()

    print("Execution Time = %s " % str(end - start))

main()












def segmentTranscriptIntoConversationsWithClearStartAndEnd(docx: str):

    conversationPosition = 0
    conversations = [[]]
    isBeginningOfConversation = True
    for sentence in docx.split('\n'):
        if 'System message: Hello' in sentence:
            isBeginningOfConversation = True
        
        if 'System message: guest' in sentence:
            isBeginningOfConversation = False
            conversations.append([])
            conversationPosition += 1
        
        if isBeginningOfConversation == True:
            conversations[conversationPosition].append(sentence)
    
    # for convo in conversations:
    #     print (convo)
    del conversations[-1] # deletes the last element on the segments
    writeConversationsV1(conversations)
    # return conversations



'''
def countWords(docx):
    countedWord = {}
    for word in docx.split(' '):
        countedWord[word] = countedWord.get(word, 0) + 1
    sorted_d = sorted(countedWord.items(), key=operator.itemgetter(1))

    print(sorted_d)
'''