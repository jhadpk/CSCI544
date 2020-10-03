import sys
import os
import re
import glob
from collections import Counter
import random

def remove_stop_words(words):
    valid_words = []
    for word in words:
        if word not in stop_words:
            valid_words.append(word)
    return valid_words

def get_word_count(file):
    review = open(file, 'r').read().lower()
    review = re.sub(r"[^a-zA-Z]+", ' ', review)
    words = review.split()
    words = remove_stop_words(words)
    word_count_dict = Counter(words)
    return word_count_dict

def get_count_dictionary(files):
    count_dict = Counter()
    for file in files:
        count_dict += get_word_count(file)
    return dict(count_dict)

def initialize():
    for word in features:
        polarity['weights'][word] = 0
        origin['weights'][word] = 0
        polarity['weights_cached'][word] = 0
        origin['weights_cached'][word] = 0

def learn_metadata(classifier_type):
    classifier = metadata[classifier_type]
    classifier['activation'] = update_activation(classifier['activation'], classifier['bias'])
    if classifier['y'] * classifier['activation'] <= 0:
        for word in word_count_dict:
            classifier['weights'][word] = update_weight(classifier['weights'][word], classifier['y'], word_count_dict[word])
            classifier['weights_cached'][word] = update_cache_weight(classifier['weights_cached'][word], classifier['y'], c, word_count_dict[word])
        classifier['bias'] = update_bias(classifier['bias'], classifier['y'])
        classifier['bias_cached'] = update_cache_bias(classifier['bias_cached'], classifier['y'], c)

def update_activation(a, b):
    return a + b

def update_weight(w, y, x):
    return w + y * x

def update_cache_weight(u, y, c, x):
    return u + y * c * x

def update_bias(b, y):
    return b + y

def update_cache_bias(b, y, c):
    return b + y * c

def get_averaged_value(w, u, c):
    return w - (u/c)

def create_model(file_name, w1, b1, w2, b2, features):
    with open(file_name, 'w') as f:
        f.write("weights_polarity=" + str(w1) + "\n")
        f.write("bias_polarity=" + str(b1) + "\n")
        f.write("weights_origin=" + str(w2) + "\n")
        f.write("bias_origin=" + str(b2) + "\n")
        f.write("features=" + str(features) + "\n")


# folder = 'op_spam_training_data'
folder = sys.argv[1]

all_files = glob.glob(os.path.join(folder, '*/*/*/*.txt'))
stop_words = ['hotel', 'room', 'wife', 'wifes', 'wives', 'husband', 'husbands', 'a', 'amongst', 'amoungst', 'becomes', 'eg', 'fify', 'formerly', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'latterly', 'ltd', 'namely', 'nevertheless', 'sixty', 'thence', 'thereafter', 'thereby', 'therein', 'thereupon', 'thickv', 'twelve', 'whence', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'whither', 'whose', 'yourselves', 'able', 'about', 'above', 'according', 'accordingly', 'across', 'act', 'actually', 'ad', 'added', 'ae', 'affected', 'after', 'afterwards', 'again', 'against', 'ah', 'al', 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'apparently', 'appear', 'appreciate', 'appropriate', 'approximately', 'are', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'au', 'av', 'away', 'b', 'back', 'be', 'became', 'because', 'become', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'both', 'bottom', 'brief', 'briefly', 'but', 'by', 'c', 'came', 'can', 'cannot', 'cant', 'cause', 'cd', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'could', 'couldn', 'couldnt', 'course', 'cry', 'currently', 'd', 'date', 'dc', 'de', 'definitely', 'describe', 'described', 'despite', 'detail', 'did', 'didn', 'different', 'dj', 'do', 'does', 'doesn', 'doing', 'don', 'done', 'down', 'dr', 'due', 'during', 'e', 'each', 'effect', 'eight', 'either', 'el', 'eleven', 'else', 'elsewhere', 'em', 'end', 'enough', 'entirely', 'especially', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'few', 'fi', 'fifteen', 'fifth', 'fill', 'find', 'fire', 'first', 'five', 'fix', 'fl', 'followed', 'following', 'for', 'former', 'forth', 'forty', 'found', 'four', 'from', 'front', 'ft', 'full', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', 'hadn', 'happens', 'has', 'hasn', 'hasnt', 'have', 'haven', 'having', 'he', 'hello', 'help', 'hence', 'her', 'here', 'herself', 'hi', 'hid', 'him', 'himself', 'his', 'ho', 'hopefully', 'how', 'however', 'hr', 'http', 'hundred', 'i', 'ie', 'if', 'il', 'im', 'immediate', 'immediately', 'important', 'in', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'information', 'inner', 'instead', 'interest', 'into', 'ip', 'is', 'isn', 'it', 'its', 'itself', 'j', 'jr', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'l', 'la', 'largely', 'last', 'lately', 'later', 'latter', 'lb', 'le', 'least', 'les', 'less', 'let', 'lets', 'like', 'likely', 'line', 'little', 'll', 'lo', 'look', 'looking', 'looks', 'los', 'm', 'ma', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'might', 'mill', 'million', 'mine', 'miss', 'ml', 'mo', 'more', 'moreover', 'most', 'mostly', 'move', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'name', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needn', 'needs', 'never', 'new', 'next', 'nine', 'nobody', 'non', 'none', 'nonetheless', 'nor', 'normally', 'noted', 'nothing', 'now', 'nowhere', 'nt', 'ny', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'oj', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'ow', 'own', 'p', 'pages', 'par', 'part', 'particular', 'particularly', 'past', 'pc', 'per', 'perhaps', 'pl', 'placed', 'please', 'plus', 'pm', 'possible', 'possibly', 'potentially', 'present', 'presumably', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'ps', 'put', 'q', 'que', 'quickly', 'quite', 'ran', 'rather', 'rd', 're', 'really', 'reasonably', 'recent', 'recently', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'resulted', 'resulting', 'results', 'right', 'rm', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'se', 'second', 'secondly', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'sent', 'serious', 'seriously', 'seven', 'several', 'sf', 'shall', 'she', 'shed', 'should', 'shouldn', 'show', 'showed', 'shown', 'shows', 'si', 'side', 'significant', 'significantly', 'similar', 'similarly', 'since', 'sincere', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'sp', 'specifically', 'sq', 'st', 'still', 'stop', 'strongly', 'sub', 'successfully', 'such', 'sup', 'sure', 'system', 't', 'take', 'taken', 'taking', 'tell', 'ten', 'tends', 'th', 'than', 'thank', 'thanks', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'therefore', 'thereof', 'theres', 'these', 'they', 'thin', 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'tv', 'twenty', 'twice', 'two', 'u', 'uk', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'until', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', 've', 'very', 'via', 'vs', 'w', 'want', 'wants', 'was', 'wasn', 'wasnt', 'way', 'we', 'welcome', 'well', 'went', 'were', 'weren', 'what', 'whatever', 'when', 'whenever', 'where', 'wherever', 'whether', 'which', 'while', 'whim', 'who', 'whoever', 'whole', 'whom', 'why', 'wi', 'will', 'willing', 'wish', 'with', 'within', 'won', 'wonder', 'wont', 'words', 'world', 'would', 'wouldn', 'wouldnt', 'x', 'yet', 'you', 'your', 'youre', 'yours', 'yourself', 'yr']

features = get_count_dictionary(all_files)
c = 1

# polarity -> positive/negative
# origin -> truthful/deceptive
metadata = {'polarity': {'activation': 0, 'weights': {}, 'weights_cached': {}, 'bias': 0, 'bias_cached': 0, 'y': 0},
            'origin': {'activation': 0, 'weights': {}, 'weights_cached': {}, 'bias': 0, 'bias_cached': 0, 'y': 0}}
polarity = metadata['polarity']
origin = metadata['origin']

initialize()

for k in range(0, 10):
    random.Random(k * 5).shuffle(all_files)
    for file in all_files:
        polarity['activation'] = 0
        origin['activation'] = 0
        polarity['y'] = 1 if "positive_polarity" in file else -1
        origin['y'] = 1 if "truthful_from" in file else -1
        word_count_dict = get_word_count(file)
        for word in word_count_dict:
            if polarity['weights'][word] != 0:
                polarity['activation'] += polarity['weights'][word] * word_count_dict[word]
                origin['activation'] += origin['weights'][word] * word_count_dict[word]
        learn_metadata('polarity')
        learn_metadata('origin')
        c += 1

create_model("vanillamodel.txt", polarity['weights'], polarity['bias'], origin['weights'], origin['bias'], features)

for word in polarity['weights']:
    polarity['weights'][word] = get_averaged_value(polarity['weights'][word], polarity['weights_cached'][word], c)
    origin['weights'][word] = get_averaged_value(origin['weights'][word], origin['weights_cached'][word], c)
polarity['bias'] = get_averaged_value(polarity['bias'], polarity['bias_cached'], c)
origin['bias'] = get_averaged_value(origin['bias'], origin['bias_cached'], c)

create_model("averagedmodel.txt", polarity['weights'], polarity['bias'], origin['weights'], origin['bias'], features)
