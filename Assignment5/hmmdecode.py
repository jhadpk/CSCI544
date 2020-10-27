import sys
import ast

def learn_model(file):
    model = {}
    model_file = open(file, 'r')
    learnt_lines = model_file.readlines()
    for line in learnt_lines:
        (key, value) = line.split('=', 1)
        model[key.strip()] = value.strip()
    return model


def get_emission_probability(observation):
    if word not in trained_words:
        #if word is not seen, let transition prob decide of the top N tags
        return 1
    else:
        return 0 if observation not in trained_emission_probabilities else trained_emission_probabilities[observation]


def get_zero_matrix(rows, cols):
    return [[0 for x in range(cols)] for y in range(rows)]


def get_max_probability_final_state(words, viterbi_prob_matrix):
    max_probability = -1
    for state_index in range(len(unique_states)):
        current_probability = viterbi_prob_matrix[state_index][len(words) - 1]
        if max_probability < current_probability:
            max_probability = current_probability
            index = state_index
            state = unique_states[state_index]
    return [index, state]


def get_predicted_tags_by_backtracking(words, viterbi_prob_matrix, parent_info_matrix):
    last_word_state_details = get_max_probability_final_state(words, viterbi_prob_matrix)
    predicted_tags = []
    predicted_tags = [last_word_state_details[1]] + predicted_tags
    index_row = last_word_state_details[0]
    index_col = len(words) - 1
    while index_col > 0:
        index_row = parent_info_matrix[index_row][index_col]
        predicted_tags = [unique_states[index_row]] + predicted_tags
        index_col = index_col - 1
    return predicted_tags


def get_tagged_line(words, prediction):
    tagged_line = ""
    for state_index, input_word in enumerate(words):
        tagged_line += input_word + "/" + prediction[state_index] + " "
    return tagged_line.strip()


# testing_file = sys.argv[1]
testing_file = "hmm-training-data/it_isdt_dev_raw.txt"
model_file = "hmmmodel.txt"
output_file = "hmmoutput.txt"

model = learn_model(model_file)
trained_transition_probabilities = ast.literal_eval(model.get("trained_transition_probabilities"))
trained_emission_probabilities = ast.literal_eval(model.get("trained_emission_probabilities"))
first_word_states_probabilities = ast.literal_eval(model.get("first_word_states_probabilities"))
unique_words_per_state = ast.literal_eval(model.get("unique_words_per_state"))
unique_words = ast.literal_eval(model.get("unique_words"))
unique_states = ast.literal_eval(model.get("unique_states"))

trained_words = set()
for word in unique_words:
    trained_words.add(word)

first_word_states = set()
for state in first_word_states_probabilities:
    first_word_states.add(state)

most_frequent_states = set()
for state in unique_words_per_state:
    most_frequent_states.add(state)
    if len(most_frequent_states) == 5:
        break

output_file_write = open(output_file, 'w')

test_lines = open(testing_file, encoding="utf8", errors='ignore').read().splitlines()
for line in test_lines:
    words = line.split()
    viterbi_prob_matrix = get_zero_matrix(len(unique_states), len(words))
    parent_info_matrix = get_zero_matrix(len(unique_states), len(words))
    for word_index in range(len(words)):
        states_to_iterate = unique_states
        if words[word_index] not in trained_words:
            #for unseen word, using top 5 most frequent tags for prediction
            states_to_iterate = most_frequent_states
        for index, current_state in enumerate(states_to_iterate):
            word = words[word_index]
            observation = word + "/" + current_state
            emission_probability = get_emission_probability(observation)

            state_index = index if word in trained_words else unique_states.index(current_state)

            if word_index == 0:
                viterbi_prob_matrix[state_index][word_index] = 0 if current_state not in first_word_states else emission_probability * first_word_states_probabilities[current_state]
            else:
                max_transition_prob = -1
                max_transition_prob_previous_state_index = -1
                for previous_state_index, previous_state in enumerate(unique_states):
                    transition = previous_state + "->" + current_state
                    if viterbi_prob_matrix[previous_state_index][word_index - 1] == 0:
                        current_prob = 0
                    else:
                        if transition not in trained_transition_probabilities:
                            transition = previous_state + "->UNKNOWN"
                        transition_probability = trained_transition_probabilities[transition]
                        current_prob = viterbi_prob_matrix[previous_state_index][word_index - 1] * transition_probability
                    if current_prob > max_transition_prob:
                        max_transition_prob = current_prob
                        max_transition_prob_previous_state_index = previous_state_index
                parent_info_matrix[state_index][word_index] = max_transition_prob_previous_state_index
                viterbi_prob_matrix[state_index][word_index] = 0 if max_transition_prob == 0 else emission_probability * max_transition_prob
    prediction = get_predicted_tags_by_backtracking(words, viterbi_prob_matrix, parent_info_matrix)
    tagged_line = get_tagged_line(words, prediction)
    output_file_write.write(tagged_line + "\n")
