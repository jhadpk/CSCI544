import sys
import os
import re
import ast
import glob
from collections import Counter

def learn_model(file):
    model = {}
    model_file = open(file, 'r')
    learnt_lines = model_file.readlines()
    for line in learnt_lines:
        (key, value) = line.split('=')
        model[key.strip()] = value.strip()
    return model

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

def classify(activation_polarity, activation_origin):
    return ["truthful" if activation_origin > 0 else "deceptive", "positive" if activation_polarity > 0 else "negative"]


model_file = sys.argv[1]
testing_data = sys.argv[2]
# model_file = "vanillamodel.txt"
# testing_data = "op_spam_training_data"

output_file = "percepoutput.txt"
output = open(output_file, 'w')

model = learn_model(model_file)
weights_polarity = ast.literal_eval(model.get('weights_polarity'))
bias_polarity = float(model.get("bias_polarity"))
weights_origin = ast.literal_eval(model.get('weights_origin'))
bias_origin = float(model.get("bias_origin"))
features = ast.literal_eval(model.get('features'))

all_files = glob.glob(os.path.join(testing_data, '*/*/*/*.txt'))
stop_words = ['hotel', 'room', 'wife', 'wifes', 'wives', 'husband', 'husbands', 'a', 'amongst', 'amoungst', 'becomes', 'eg', 'fify', 'formerly', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'latterly', 'ltd', 'namely', 'nevertheless', 'sixty', 'thence', 'thereafter', 'thereby', 'therein', 'thereupon', 'thickv', 'twelve', 'whence', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'whither', 'whose', 'yourselves', 'able', 'about', 'above', 'according', 'accordingly', 'across', 'act', 'actually', 'ad', 'added', 'ae', 'affected', 'after', 'afterwards', 'again', 'against', 'ah', 'al', 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'apparently', 'appear', 'appreciate', 'appropriate', 'approximately', 'are', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'au', 'av', 'away', 'b', 'back', 'be', 'became', 'because', 'become', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'both', 'bottom', 'brief', 'briefly', 'but', 'by', 'c', 'came', 'can', 'cannot', 'cant', 'cause', 'cd', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'could', 'couldn', 'couldnt', 'course', 'cry', 'currently', 'd', 'date', 'dc', 'de', 'definitely', 'describe', 'described', 'despite', 'detail', 'did', 'didn', 'different', 'dj', 'do', 'does', 'doesn', 'doing', 'don', 'done', 'down', 'dr', 'due', 'during', 'e', 'each', 'effect', 'eight', 'either', 'el', 'eleven', 'else', 'elsewhere', 'em', 'end', 'enough', 'entirely', 'especially', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'few', 'fi', 'fifteen', 'fifth', 'fill', 'find', 'fire', 'first', 'five', 'fix', 'fl', 'followed', 'following', 'for', 'former', 'forth', 'forty', 'found', 'four', 'from', 'front', 'ft', 'full', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', 'hadn', 'happens', 'has', 'hasn', 'hasnt', 'have', 'haven', 'having', 'he', 'hello', 'help', 'hence', 'her', 'here', 'herself', 'hi', 'hid', 'him', 'himself', 'his', 'ho', 'hopefully', 'how', 'however', 'hr', 'http', 'hundred', 'i', 'ie', 'if', 'il', 'im', 'immediate', 'immediately', 'important', 'in', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'information', 'inner', 'instead', 'interest', 'into', 'ip', 'is', 'isn', 'it', 'its', 'itself', 'j', 'jr', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'l', 'la', 'largely', 'last', 'lately', 'later', 'latter', 'lb', 'le', 'least', 'les', 'less', 'let', 'lets', 'like', 'likely', 'line', 'little', 'll', 'lo', 'look', 'looking', 'looks', 'los', 'm', 'ma', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'might', 'mill', 'million', 'mine', 'miss', 'ml', 'mo', 'more', 'moreover', 'most', 'mostly', 'move', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'name', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needn', 'needs', 'never', 'new', 'next', 'nine', 'nobody', 'non', 'none', 'nonetheless', 'nor', 'normally', 'noted', 'nothing', 'now', 'nowhere', 'nt', 'ny', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'oj', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'ow', 'own', 'p', 'pages', 'par', 'part', 'particular', 'particularly', 'past', 'pc', 'per', 'perhaps', 'pl', 'placed', 'please', 'plus', 'pm', 'possible', 'possibly', 'potentially', 'present', 'presumably', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'ps', 'put', 'q', 'que', 'quickly', 'quite', 'ran', 'rather', 'rd', 're', 'really', 'reasonably', 'recent', 'recently', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'resulted', 'resulting', 'results', 'right', 'rm', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'se', 'second', 'secondly', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'sent', 'serious', 'seriously', 'seven', 'several', 'sf', 'shall', 'she', 'shed', 'should', 'shouldn', 'show', 'showed', 'shown', 'shows', 'si', 'side', 'significant', 'significantly', 'similar', 'similarly', 'since', 'sincere', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'sp', 'specifically', 'sq', 'st', 'still', 'stop', 'strongly', 'sub', 'successfully', 'such', 'sup', 'sure', 'system', 't', 'take', 'taken', 'taking', 'tell', 'ten', 'tends', 'th', 'than', 'thank', 'thanks', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'therefore', 'thereof', 'theres', 'these', 'they', 'thin', 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'tv', 'twenty', 'twice', 'two', 'u', 'uk', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'until', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', 've', 'very', 'via', 'vs', 'w', 'want', 'wants', 'was', 'wasn', 'wasnt', 'way', 'we', 'welcome', 'well', 'went', 'were', 'weren', 'what', 'whatever', 'when', 'whenever', 'where', 'wherever', 'whether', 'which', 'while', 'whim', 'who', 'whoever', 'whole', 'whom', 'why', 'wi', 'will', 'willing', 'wish', 'with', 'within', 'won', 'wonder', 'wont', 'words', 'world', 'would', 'wouldn', 'wouldnt', 'x', 'yet', 'you', 'your', 'youre', 'yours', 'yourself', 'yr']

for file in all_files:
    activation_polarity = bias_polarity
    activation_origin = bias_origin
    word_count_dict = get_word_count(file)
    for word in word_count_dict:
        if word in features:
            activation_polarity += weights_polarity[word] * word_count_dict[word]
            activation_origin += weights_origin[word] * word_count_dict[word]
    prediction = classify(activation_polarity, activation_origin)
    output.write(prediction[0] + ' ' + prediction[1] + ' ' + file + '\n')
output.close()
