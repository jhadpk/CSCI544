import glob
import os
import re
import sys
from collections import Counter


def get_files(polarity, origin):
    files = []
    for file in allFiles:
        if polarity in file and origin in file:
            files.append(file)
    return files


def remove_stop_words(words):
    valid_words = []
    for word in words:
        if word not in stop_words:
            valid_words.append(word)
    return valid_words


def get_count_dictionary(files):
    count_dict = Counter()
    for file in files:
        review = open(file, 'r').read().lower()
        review = re.sub(r"[^a-zA-Z]+", ' ', review)
        words = review.split()
        words = remove_stop_words(words)
        word_count_dict = Counter(words)
        count_dict += word_count_dict
    return count_dict


folder = sys.argv[1]
# folder = 'op_spam_training_data'

allFiles = glob.glob(os.path.join(folder, '*/*/*/*.txt'))

positive = "positive"
negative = "negative"
truthful = "truthful"
deceptive = "deceptive"
positive_truthful_files = get_files(positive, truthful)
positive_deceptive_files = get_files(positive, deceptive)
negative_truthful_files = get_files(negative, truthful)
negative_deceptive_files = get_files(negative, deceptive)

stop_words = ['a', 'amongst', 'amoungst', 'becomes', 'con', 'eg', 'fify', 'formerly', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'latterly', 'ltd', 'namely', 'nevertheless', 'noone', 'sixty', 'thence', 'thereafter', 'thereby', 'therein', 'thereupon', 'thickv', 'twelve', 'whence', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'whither', 'whose', 'yourselves', 'able', 'about', 'above', 'ac', 'according', 'accordingly', 'across', 'act', 'actually', 'ad', 'added', 'ae', 'affected', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'al', 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amount', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'apparently', 'appear', 'appreciate', 'appropriate', 'approximately', 'are', 'aren', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'au', 'av', 'available', 'away', 'b', 'back', 'be', 'became', 'because', 'become', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better', 'between', 'beyond', 'bill', 'both', 'bottom', 'brief', 'briefly', 'but', 'by', 'c', 'call', 'came', 'can', 'cannot', 'cant', 'cause', 'cd', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'could', 'couldn', 'couldnt', 'course', 'cry', 'currently', 'd', 'date', 'dc', 'de', 'definitely', 'describe', 'described', 'despite', 'detail', 'did', 'didn', 'different', 'dj', 'do', 'does', 'doesn', 'doing', 'don', 'done', 'down', 'dr', 'due', 'during', 'e', 'each', 'effect', 'eight', 'either', 'el', 'eleven', 'else', 'elsewhere', 'em', 'empty', 'end', 'enough', 'entirely', 'especially', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'far', 'few', 'fi', 'fifteen', 'fifth', 'fill', 'find', 'fire', 'first', 'five', 'fix', 'fl', 'followed', 'following', 'for', 'former', 'forth', 'forty', 'found', 'four', 'from', 'front', 'ft', 'full', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', 'hadn', 'happens', 'hardly', 'has', 'hasn', 'hasnt', 'have', 'haven', 'having', 'he', 'hello', 'help', 'hence', 'her', 'here', 'herself', 'hi', 'hid', 'him', 'himself', 'his', 'ho', 'home', 'hopefully', 'how', 'however', 'hr', 'http', 'hundred', 'i', 'ie', 'if', 'ignored', 'il', 'im', 'immediate', 'immediately', 'important', 'in', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'information', 'inner', 'instead', 'interest', 'into', 'ip', 'is', 'isn', 'it', 'its', 'itself', 'j', 'jr', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'l', 'la', 'largely', 'last', 'lately', 'later', 'latter', 'lb', 'le', 'least', 'les', 'less', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', 'll', 'lo', 'look', 'looking', 'looks', 'los', 'm', 'ma', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'might', 'mill', 'million', 'mine', 'miss', 'ml', 'mo', 'more', 'moreover', 'most', 'mostly', 'move', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'name', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needn', 'needs', 'neither', 'never', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'nonetheless', 'nor', 'normally', 'not', 'noted', 'nothing', 'now', 'nowhere', 'nt', 'ny', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'oj', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'ow', 'own', 'p', 'pages', 'par', 'part', 'particular', 'particularly', 'past', 'pc', 'per', 'perhaps', 'pl', 'placed', 'please', 'plus', 'pm', 'poorly', 'possible', 'possibly', 'potentially', 'present', 'presumably', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'ps', 'put', 'q', 'que', 'quickly', 'quite', 'ran', 'rather', 'rd', 're', 'really', 'reasonably', 'recent', 'recently', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'resulted', 'resulting', 'results', 'right', 'rm', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'se', 'second', 'secondly', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'sent', 'serious', 'seriously', 'seven', 'several', 'sf', 'shall', 'she', 'shed', 'should', 'shouldn', 'show', 'showed', 'shown', 'shows', 'si', 'side', 'significant', 'significantly', 'similar', 'similarly', 'since', 'sincere', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'sp', 'specifically', 'sq', 'st', 'still', 'stop', 'strongly', 'sub', 'successfully', 'such', 'suggest', 'sup', 'sure', 'system', 't', 'take', 'taken', 'taking', 'tell', 'ten', 'tends', 'th', 'than', 'thank', 'thanks', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'therefore', 'thereof', 'theres', 'these', 'they', 'thin', 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'top', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'tv', 'twenty', 'twice', 'two', 'u', 'uk', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'until', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', 've', 'very', 'via', 'vs', 'w', 'want', 'wants', 'was', 'wasn', 'wasnt', 'way', 'we', 'welcome', 'well', 'went', 'were', 'weren', 'what', 'whatever', 'when', 'whenever', 'where', 'wherever', 'whether', 'which', 'while', 'whim', 'who', 'whoever', 'whole', 'whom', 'why', 'wi', 'will', 'willing', 'wish', 'with', 'within', 'without', 'won', 'wonder', 'wont', 'words', 'world', 'would', 'wouldn', 'wouldnt', 'x', 'yes', 'yet', 'you', 'your', 'youre', 'yours', 'yourself', 'yr']

positive_truthful_dict = get_count_dictionary(positive_truthful_files)
positive_deceptive_dict = get_count_dictionary(positive_deceptive_files)
negative_truthful_dict = get_count_dictionary(negative_truthful_files)
negative_deceptive_dict = get_count_dictionary(negative_deceptive_files)

positive_truthful_count = sum(positive_truthful_dict.values())
positive_deceptive_count = sum(positive_deceptive_dict.values())
negative_truthful_count = sum(negative_truthful_dict.values())
negative_deceptive_count = sum(negative_deceptive_dict.values())

# unique total count
total_word_count = len(positive_truthful_dict + positive_deceptive_dict + negative_truthful_dict + negative_deceptive_dict)

with open("nbmodel.txt", 'w') as f:
    f.write("positive_truthful_dict="+str(dict(positive_truthful_dict))+"\n")
    f.write("positive_deceptive_dict="+str(dict(positive_deceptive_dict))+"\n")
    f.write("negative_truthful_dict="+str(dict(negative_truthful_dict))+"\n")
    f.write("negative_deceptive_dict="+str(dict(negative_deceptive_dict))+"\n")
    f.write("positive_truthful_count=" + str(positive_truthful_count) + "\n")
    f.write("positive_deceptive_count=" + str(positive_deceptive_count) + "\n")
    f.write("negative_truthful_count=" + str(negative_truthful_count) + "\n")
    f.write("negative_deceptive_count=" + str(negative_deceptive_count) + "\n")
    f.write("positive_truthful_filecount="+str(len(positive_truthful_files))+"\n")
    f.write("positive_deceptive_filecount="+str(len(positive_deceptive_files))+"\n")
    f.write("negative_truthful_filecount="+str(len(negative_truthful_files))+"\n")
    f.write("negative_deceptive_filecount="+str(len(negative_deceptive_files))+"\n")
    f.write("total_word_count=" + str(total_word_count) + "\n")
