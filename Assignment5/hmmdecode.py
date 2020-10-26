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


def get_zero_matrix(rows, cols):
    return [[0 for x in range(cols)] for y in range(rows)]


def get_max_probability_final_state(words, viterbi_prob_matrix):
    max_probability = -1
    for state_index in range(total_states):
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
        tag = unique_states[index_row]
        predicted_tags = [tag] + predicted_tags
        index_col = index_col - 1
    return predicted_tags


def get_predicted_tags(words, prediction):
    tagged_line = ""
    for state_index, input_word in enumerate(words):
        tagged_line += input_word + "/" + prediction[state_index] + " "
    return tagged_line.strip()


testing_file = sys.argv[1]
# testing_file = "hmm-training-data/it_isdt_dev_raw.txt"
model_file = "hmmmodel.txt"
output_file = "hmmoutput.txt"

model = learn_model(model_file)

transitions = ast.literal_eval(model.get("transitions"))
transition_states = ast.literal_eval(model.get("transition_states"))
emissions = ast.literal_eval(model.get("emissions"))
emission_states = ast.literal_eval(model.get("emission_states"))
initial_states = ast.literal_eval(model.get("initial_states"))
total_lines = int(model.get("total_lines"))
unique_words = ast.literal_eval(model.get("unique_words"))
unique_states = ast.literal_eval(model.get("unique_states"))
total_states = int(model.get("total_states"))
unique_words_per_tag = ast.literal_eval(model.get("unique_words_per_tag"))
transition_probability_dict = ast.literal_eval(model.get("transition_probability_dict"))
emission_probability_dict = ast.literal_eval(model.get("emission_probability_dict"))

trained_words = set()
for word in unique_words:
    trained_words.add(word)

output_file_write = open(output_file, 'w')

test_lines = open(testing_file, encoding="utf8", errors='ignore').read().splitlines()
for line in test_lines:
    words = line.split()
    viterbi_prob_matrix = get_zero_matrix(total_states, len(words))
    parent_info_matrix = get_zero_matrix(total_states, len(words))
    for word_index in range(len(words)):
        for state_index in range(total_states):
            current_state = unique_states[state_index]
            word = words[word_index]
            observation = word + "/" + current_state
            if word_index == 0:
                if current_state not in initial_states:
                    viterbi_prob_matrix[state_index][word_index] = 0
                else:
                    if word not in trained_words:
                        emission_probability = 1
                    else:
                        emission_probability = 0 if observation not in emission_probability_dict else emission_probability_dict[observation]
                    viterbi_prob_matrix[state_index][word_index] = emission_probability * (initial_states[current_state] / total_lines)
            else:
                transition_prob_statewise = []
                max_transition_prob = -1
                max_transition_prob_previous_state_index = -1
                for unique_states_index, previous_state in enumerate(unique_states):
                    transition = previous_state + "->" + current_state
                    if viterbi_prob_matrix[unique_states_index][word_index - 1] == 0:
                        current_prob = 0
                    else:
                        transition_probability = 1 / (transition_states[previous_state] + total_states) if transition not in transition_probability_dict else transition_probability_dict[transition]
                        current_prob = viterbi_prob_matrix[unique_states_index][word_index - 1] * transition_probability
                    if current_prob > max_transition_prob:
                        max_transition_prob = current_prob
                        max_transition_prob_previous_state_index = unique_states_index
                parent_info_matrix[state_index][word_index] = max_transition_prob_previous_state_index
                if max_transition_prob == 0:
                    viterbi_prob_matrix[state_index][word_index] = 0
                else:
                    if word not in trained_words:
                        emission_probability = 1
                    else:
                        emission_probability = 0 if observation not in emission_probability_dict else \
                            emission_probability_dict[observation]
                    viterbi_prob_matrix[state_index][word_index] = 0 if emission_probability == 0 else emission_probability * max_transition_prob
    prediction = get_predicted_tags_by_backtracking(words, viterbi_prob_matrix, parent_info_matrix)
    tagged_line = get_predicted_tags(words, prediction)
    output_file_write.write(tagged_line + "\n")


