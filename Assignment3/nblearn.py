import glob
import math
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


# condprob <- Tct+1 / ∑t′(Tct′+1) https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf Pg. 260
def get_conditional_prob(class_dict, class_wordcount):
    denominator = math.log(class_wordcount + total_word_count)
    conditional_prob_dict = {}
    for key, value in class_dict.items():
        # conditional probability of the word (P(Class|word) = #count of word in class (P(AintersectionB)) / #total words P(B)
        conditional_prob_dict[key] = math.log(value + 1) - denominator
    # will be used for unknown words for the class
    conditional_prob_dict['$UNKNOWN_WORD_DEFAULT'] = math.log(1) - denominator
    return conditional_prob_dict


folder = sys.argv[1]
# folder = 'op_spam_training_data'

allFiles = glob.glob(os.path.join(folder, '*/*/*/*.txt'))

stop_words = ['hotel', 'room', 'wife', 'wifes', 'wives', 'husband', 'husbands', 'a', 'amongst', 'amoungst', 'becomes', 'eg', 'fify', 'formerly', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'latterly', 'ltd', 'namely', 'nevertheless', 'sixty', 'thence', 'thereafter', 'thereby', 'therein', 'thereupon', 'thickv', 'twelve', 'whence', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'whither', 'whose', 'yourselves', 'able', 'about', 'above', 'according', 'accordingly', 'across', 'act', 'actually', 'ad', 'added', 'ae', 'affected', 'after', 'afterwards', 'again', 'against', 'ah', 'al', 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'apparently', 'appear', 'appreciate', 'appropriate', 'approximately', 'are', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'au', 'av', 'away', 'b', 'back', 'be', 'became', 'because', 'become', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'both', 'bottom', 'brief', 'briefly', 'but', 'by', 'c', 'came', 'can', 'cannot', 'cant', 'cause', 'cd', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'could', 'couldn', 'couldnt', 'course', 'cry', 'currently', 'd', 'date', 'dc', 'de', 'definitely', 'describe', 'described', 'despite', 'detail', 'did', 'didn', 'different', 'dj', 'do', 'does', 'doesn', 'doing', 'don', 'done', 'down', 'dr', 'due', 'during', 'e', 'each', 'effect', 'eight', 'either', 'el', 'eleven', 'else', 'elsewhere', 'em', 'end', 'enough', 'entirely', 'especially', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'few', 'fi', 'fifteen', 'fifth', 'fill', 'find', 'fire', 'first', 'five', 'fix', 'fl', 'followed', 'following', 'for', 'former', 'forth', 'forty', 'found', 'four', 'from', 'front', 'ft', 'full', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', 'hadn', 'happens', 'has', 'hasn', 'hasnt', 'have', 'haven', 'having', 'he', 'hello', 'help', 'hence', 'her', 'here', 'herself', 'hi', 'hid', 'him', 'himself', 'his', 'ho', 'hopefully', 'how', 'however', 'hr', 'http', 'hundred', 'i', 'ie', 'if', 'il', 'im', 'immediate', 'immediately', 'important', 'in', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'information', 'inner', 'instead', 'interest', 'into', 'ip', 'is', 'isn', 'it', 'its', 'itself', 'j', 'jr', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'known', 'knows', 'l', 'la', 'largely', 'last', 'lately', 'later', 'latter', 'lb', 'le', 'least', 'les', 'less', 'let', 'lets', 'like', 'likely', 'line', 'little', 'll', 'lo', 'look', 'looking', 'looks', 'los', 'm', 'ma', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'might', 'mill', 'million', 'mine', 'miss', 'ml', 'mo', 'more', 'moreover', 'most', 'mostly', 'move', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'name', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needn', 'needs', 'never', 'new', 'next', 'nine', 'nobody', 'non', 'none', 'nonetheless', 'nor', 'normally', 'noted', 'nothing', 'now', 'nowhere', 'nt', 'ny', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'oj', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'ow', 'own', 'p', 'pages', 'par', 'part', 'particular', 'particularly', 'past', 'pc', 'per', 'perhaps', 'pl', 'placed', 'please', 'plus', 'pm', 'possible', 'possibly', 'potentially', 'present', 'presumably', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'ps', 'put', 'q', 'que', 'quickly', 'quite', 'ran', 'rather', 'rd', 're', 'really', 'reasonably', 'recent', 'recently', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'resulted', 'resulting', 'results', 'right', 'rm', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'se', 'second', 'secondly', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'sent', 'serious', 'seriously', 'seven', 'several', 'sf', 'shall', 'she', 'shed', 'should', 'shouldn', 'show', 'showed', 'shown', 'shows', 'si', 'side', 'significant', 'significantly', 'similar', 'similarly', 'since', 'sincere', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'sp', 'specifically', 'sq', 'st', 'still', 'stop', 'strongly', 'sub', 'successfully', 'such', 'sup', 'sure', 'system', 't', 'take', 'taken', 'taking', 'tell', 'ten', 'tends', 'th', 'than', 'thank', 'thanks', 'that', 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'therefore', 'thereof', 'theres', 'these', 'they', 'thin', 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'tv', 'twenty', 'twice', 'two', 'u', 'uk', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'until', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', 've', 'very', 'via', 'vs', 'w', 'want', 'wants', 'was', 'wasn', 'wasnt', 'way', 'we', 'welcome', 'well', 'went', 'were', 'weren', 'what', 'whatever', 'when', 'whenever', 'where', 'wherever', 'whether', 'which', 'while', 'whim', 'who', 'whoever', 'whole', 'whom', 'why', 'wi', 'will', 'willing', 'wish', 'with', 'within', 'won', 'wonder', 'wont', 'words', 'world', 'would', 'wouldn', 'wouldnt', 'x', 'yet', 'you', 'your', 'youre', 'yours', 'yourself', 'yr']

positive = "positive"
negative = "negative"
truthful = "truthful"
deceptive = "deceptive"
positive_truthful_files = get_files(positive, truthful)
positive_deceptive_files = get_files(positive, deceptive)
negative_truthful_files = get_files(negative, truthful)
negative_deceptive_files = get_files(negative, deceptive)

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

# total file count
total_file_count = len(positive_truthful_files) + len(positive_deceptive_files) + len(negative_truthful_files) + len(negative_deceptive_files)

# all prob are in log
positive_truthful_conditional_prob_dict = get_conditional_prob(positive_truthful_dict, positive_truthful_count)
positive_deceptive_conditional_prob_dict = get_conditional_prob(positive_deceptive_dict, positive_deceptive_count)
negative_truthful_conditional_prob_dict = get_conditional_prob(negative_truthful_dict, negative_truthful_count)
negative_deceptive_conditional_prob_dict = get_conditional_prob(negative_deceptive_dict, negative_deceptive_count)

positive_truthful_prior_prob = math.log(len(positive_truthful_files)) - math.log(total_file_count)
positive_deceptive_prior_prob = math.log(len(positive_deceptive_files)) - math.log(total_file_count)
negative_truthful_prior_prob = math.log(len(negative_truthful_files)) - math.log(total_file_count)
negative_deceptive_prior_prob = math.log(len(negative_deceptive_files)) - math.log(total_file_count)

with open("nbmodel.txt", 'w') as f:
    # class wise posterior probability
    f.write("positive_truthful_conditional_prob_dict=" + str(dict(positive_truthful_conditional_prob_dict)) + "\n")
    f.write("positive_deceptive_conditional_prob_dict="+str(dict(positive_deceptive_conditional_prob_dict))+"\n")
    f.write("negative_truthful_conditional_prob_dict="+str(dict(negative_truthful_conditional_prob_dict))+"\n")
    f.write("negative_deceptive_conditional_prob_dict="+str(dict(negative_deceptive_conditional_prob_dict))+"\n")

    # class wise prior probability
    f.write("positive_truthful_prior_prob=" + str(positive_truthful_prior_prob) + "\n")
    f.write("positive_deceptive_prior_prob=" + str(positive_deceptive_prior_prob) + "\n")
    f.write("negative_truthful_prior_prob=" + str(negative_truthful_prior_prob) + "\n")
    f.write("negative_deceptive_prior_prob=" + str(negative_deceptive_prior_prob) + "\n")