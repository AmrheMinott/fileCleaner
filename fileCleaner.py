import doctext  # used to handle docx files
import operator
import time
import os

CONVERSATIONS_FILE_DIRECTORY = "./Conversations_V3"
CONVERSATIONS_TEXT_FILE_DIRECTORY = "./Conversations_Text"


def open_docx_file(filename: str):
    doc_text = doctext.DocFile(doc=filename)
    text = doc_text.get_text()
    return text


def open_text_file(filename: str):
    file = open(filename, 'r')
    return file.read()


def get_files_for_path(path: str):
    f = []
    count = 0
    for (dirpath, dirnames, filenames) in os.walk(path):
        count += 1
        f.extend(filenames)
        return (f)


def get_directories(path: str):
    directories = [x[1] for x in os.walk(path)]
    non_empty_dirs = [x for x in directories if x]  # filter out empty lists
    return [item for subitem in non_empty_dirs for item in subitem]


def filter_out_strings_from_docx_file(docx: str):
    for word in docx.split(' '):
        if '@web.ca.libraryh3lp.com:' in word or '@chat.ca.libraryh3lp.com:' in word or ' ca.libraryh3lp.com:' in word:
            docx = docx.replace(word, '')
        if 'PM' in word or 'AM' in word:
            docx = docx.replace(word, word[:-7])

    return docx


def filter_out_time_and_user_id_from_file(docx: str):
    text = ""
    for sentence in docx.split('\n'):
        if '@web.ca.libraryh3lp.com:' in sentence or '@chat.ca.libraryh3lp.com:' in sentence or ' ca.libraryh3lp.com:' in sentence:
            try:
                text += sentence[sentence.index(".com:") + 5:]
                text += '\n\n'
            except ValueError:
                text = text

    return text


def segment_transcript_conversations_with_no_start_and_end(docx: str):
    conversation_position = 0
    conversations = [[]]
    for sentence in docx.split('\n'):
        if 'System message: Hello' in sentence:
            conversations.append([])
            conversation_position += 1
        else:
            conversations[conversation_position].append(sentence)
    print('Number of Conversations counted were ' + str(conversation_position))
    write_conversations(conversations)


def write_conversations(conversations: str):
    if not os.path.exists(CONVERSATIONS_FILE_DIRECTORY):
        try:
            os.makedirs(CONVERSATIONS_FILE_DIRECTORY)
        except OSError:
            print("Creation of the directory %s failed" % CONVERSATIONS_FILE_DIRECTORY)
        else:
            print("Successfully created the directory %s you can find your files there." % CONVERSATIONS_FILE_DIRECTORY)

    for i in range(len(conversations)):
        f = open(CONVERSATIONS_FILE_DIRECTORY + '/conversation_' + str(i + 1) + '.txt', 'w')
        conversation = ''
        for sentence in conversations[i]:
            if sentence == '':
                conversation += '\n'
            else:
                conversation += sentence
        f.write(conversation)
        f.close()


def get_chat_text_files_from_folders():
    directory_name = "./carleton-txt/"
    main_directory = get_directories(directory_name)
    text_chat_count = 1
    for folder in main_directory:
        s = directory_name + folder
        text_files = get_files_for_path(s)
        for text_file in text_files:
            write_text_chats(open_text_file(s + "/" + text_file), text_chat_count)
            text_chat_count += 1


def write_text_chats(text_file: str, current: int):
    if not os.path.exists(CONVERSATIONS_TEXT_FILE_DIRECTORY):
        try:
            os.makedirs(CONVERSATIONS_TEXT_FILE_DIRECTORY)
        except OSError:
            print("Creation of the directory %s failed" % CONVERSATIONS_TEXT_FILE_DIRECTORY)
        else:
            print(
                "Successfully created the directory %s you can find your files there." % CONVERSATIONS_TEXT_FILE_DIRECTORY)

    text = ""
    for sentence in text_file.split('\n'):
        try:
            text += sentence[sentence.index(".com:") + 5:]
            text += '\n\n'
        except ValueError:
            text = text

    f = open(CONVERSATIONS_TEXT_FILE_DIRECTORY + "/TextConversation_" + str(current) + '.txt', 'w')
    f.write(text)
    f.close()


def main():
    start = time.time()

    # docxText = openDocxFile('./transcripts_example.docx')
    # filteredString = filterOutTimeAndUserIdFromFile(docxText)
    # segmentTranscriptIntoConversationsWithNoStartAndEnd(filteredString)

    get_chat_text_files_from_folders()
    end = time.time()

    print("Execution Time = %s " % str(end - start))


main()


'''
def countWords(docx):
    countedWord = {}
    for word in docx.split(' '):
        countedWord[word] = countedWord.get(word, 0) + 1
    sorted_d = sorted(countedWord.items(), key=operator.itemgetter(1))

    print(sorted_d)
'''
