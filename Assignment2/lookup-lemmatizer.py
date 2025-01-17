import sys
import re


def create_lookup_table(form, lemma_count_dict):
    max_count = -1
    max_lemma = ""
    for lemma in lemma_count_dict.keys():
        if lemma_count_dict[lemma] > max_count:
            max_count = lemma_count_dict[lemma]
            max_lemma = lemma
    lemma_max[form] = max_lemma


def train_lemma_count(form, lemma):
    if form not in lemma_count:
        lemma_count[form] = {}

    if lemma not in lemma_count[form]:
        lemma_count[form][lemma] = 0

    lemma_count[form][lemma] = lemma_count[form][lemma] + 1


def train_lookup():
    global wordform_types, wordform_tokens, identity_tokens, ambiguous_types, ambiguous_tokens, \
        ambiguous_most_common_tokens, unambiguous_types, unambiguous_tokens

    for form in lemma_count.keys():
        create_lookup_table(form, lemma_count[form])
        form_lemma_count = lemma_count[form]
        ambiguous_types_incremented = False

        for lemma in form_lemma_count:
            wordform_tokens += form_lemma_count[lemma]
            if lemma == form:
                identity_tokens += form_lemma_count[lemma]
            if len(form_lemma_count) > 1:
                if not ambiguous_types_incremented:
                    ambiguous_types += 1
                    ambiguous_types_incremented = True
                ambiguous_tokens += form_lemma_count[lemma]
                if lemma == lemma_max[form]:
                    ambiguous_most_common_tokens += form_lemma_count[lemma]
            else:
                unambiguous_types += 1
                unambiguous_tokens += form_lemma_count[lemma]
        wordform_types += 1


def test_lookup(form, lemma):
    global found_in_lookup_table, lookup_match, lookup_mismatch, not_found_in_lookup_table, identity_match, \
        identity_mismatch, total_test_items
    if form in lemma_max:
        found_in_lookup_table += 1
        lookup_match, lookup_mismatch = (lookup_match + 1, lookup_mismatch) if lemma == lemma_max[form] else (
            lookup_match, lookup_mismatch + 1)
    else:
        not_found_in_lookup_table += 1
        identity_match, identity_mismatch = (identity_match + 1, identity_mismatch) if lemma == form else (
            identity_match, identity_mismatch + 1)
    total_test_items += 1


def set_training_results():
    training_counts['Wordform types'] = wordform_types
    training_counts['Wordform tokens'] = wordform_tokens
    training_counts['Identity tokens'] = identity_tokens
    training_counts['Ambiguous types'] = ambiguous_types
    training_counts['Ambiguous tokens'] = ambiguous_tokens
    training_counts['Ambiguous most common tokens'] = ambiguous_most_common_tokens
    training_counts['Unambiguous types'] = unambiguous_types
    training_counts['Unambiguous tokens'] = unambiguous_tokens


def set_test_results():
    test_counts['Found in lookup table'] = found_in_lookup_table
    test_counts['Lookup match'] = lookup_match
    test_counts['Lookup mismatch'] = lookup_mismatch
    test_counts['Not found in lookup table'] = not_found_in_lookup_table
    test_counts['Identity match'] = identity_match
    test_counts['Identity mismatch'] = identity_mismatch
    test_counts['Total test items'] = total_test_items


def set_accuracies():
    accuracies['Expected lookup'] = (unambiguous_tokens + ambiguous_most_common_tokens) / float(wordform_tokens)
    accuracies['Expected identity'] = (identity_tokens / float(wordform_tokens))
    accuracies['Lookup'] = lookup_match / float(found_in_lookup_table)
    accuracies['Identity'] = identity_match / float(not_found_in_lookup_table)
    accuracies['Overall'] = (lookup_match + identity_match) / float(total_test_items)

def write_output():
    output = open('lookup-output.txt', 'w')
    output.write('Training statistics\n')
    for stat in training_stats:
        output.write(stat + ': ' + str(training_counts[stat]) + '\n')
    for model in ['Expected lookup', 'Expected identity']:
        output.write(model + ' accuracy: ' + str(accuracies[model]) + '\n')
    output.write('Test results\n')
    for outcome in test_outcomes:
        output.write(outcome + ': ' + str(test_counts[outcome]) + '\n')
    for model in ['Lookup', 'Identity', 'Overall']:
        output.write(model + ' accuracy: ' + str(accuracies[model]) + '\n')
    output.close()


train_file = sys.argv[1]
test_file = sys.argv[2]
# train_file = "UD_Hindi-HDTB-master/hi_hdtb-ud-train.conllu"
# test_file = "UD_Hindi-HDTB-master/hi_hdtb-ud-test.conllu"

lemma_count = {}
lemma_max = {}

training_stats = ['Wordform types', 'Wordform tokens', 'Unambiguous types', 'Unambiguous tokens', 'Ambiguous types',
                  'Ambiguous tokens', 'Ambiguous most common tokens', 'Identity tokens']
training_counts = dict.fromkeys(training_stats, 0)
wordform_types = wordform_tokens = identity_tokens = ambiguous_types = ambiguous_tokens = \
    ambiguous_most_common_tokens = unambiguous_types = unambiguous_tokens = 0

test_outcomes = ['Total test items', 'Found in lookup table', 'Lookup match', 'Lookup mismatch',
                 'Not found in lookup table', 'Identity match', 'Identity mismatch']
test_counts = dict.fromkeys(test_outcomes, 0)
total_test_items = found_in_lookup_table = lookup_match = lookup_mismatch = not_found_in_lookup_table = \
    identity_match = identity_mismatch = 0

accuracies = {}

train_data = open(train_file, 'r')
test_data = open(test_file, 'r')

for line in train_data:
    if re.search('\t', line):
        field = line.strip().split('\t')
        form = field[1]
        lemma = field[2]
        train_lemma_count(form, lemma)

train_lookup()

set_training_results()

for line in test_data:
    if re.search('\t', line):
        field = line.strip().split('\t')
        form = field[1]
        lemma = field[2]
        test_lookup(form, lemma)

set_test_results()

set_accuracies()

write_output()
