from collections import Counter
import sys

def get_transition_probabilities(transitions, transitions_states, total_states):
    transition_probabilities = {}
    for transition in transitions:
        source = transition.split("->")[0]
        transition_probabilities[transition] = (transitions[transition] + 1) / (transitions_states[source] + total_states)
    #append missing transitions
    for state in unique_states:
        transition = state + "->UNKNOWN"
        transition_probabilities[transition] = 1 / (transition_states[state] + len(unique_states))
    return transition_probabilities


def get_emission_probabilities(emissions, emission_states):
    emission_probabilities = {}
    for emission in emissions:
        state = emission.rsplit("/", 1)[1]
        emission_probabilities[emission] = emissions[emission] / emission_states[state]
    return emission_probabilities


def get_first_word_state_probabilities():
    first_word_states_probabilities = {}
    for state in first_word_states:
        first_word_states_probabilities[state] = first_word_states[state] / total_lines
    return first_word_states_probabilities


def create_model(file_name, transition_probability, emission_probability, first_word_states_probabilities, unique_words_per_state, unique_words, unique_states, total_lines):
    with open(file_name, 'w') as f:
        f.write("transition_probability_dict=" + str(dict(transition_probability)) + "\n")
        f.write("emission_probability_dict=" + str(dict(emission_probability)) + "\n")
        f.write("first_word_states_probabilities=" + str(dict(first_word_states_probabilities)) + "\n")
        f.write("unique_words_per_state=" + str(dict(unique_words_per_state)) + "\n")
        f.write("unique_words=" + str(unique_words) + "\n")
        f.write("unique_states=" + str(unique_states) + "\n")
        f.write("total_lines=" + str(total_lines) + "\n")


# training_file = sys.argv[1]
training_file = "hmm-training-data/it_isdt_train_tagged.txt"

first_word_states = []
emissions = []
observations = []
emission_states = []
transitions = []
transition_states = []
unique_words_per_state = {}

training_lines = open(training_file, encoding="utf8", errors='ignore').read().splitlines()

for line in training_lines:
    words = line.split()
    emissions += words
    first_word_states.append(words[0].split("/")[-1])  # first word state
    for i, word in enumerate(words):
        word_and_tag = word.rsplit("/", 1)
        observation = word_and_tag[0]
        state = word_and_tag[1]
        observations.append(observation)
        emission_states.append(state)
        if i < len(words) - 1:
            transition_states.append(state)
            transitions.append(state + "->" + words[i+1].rsplit("/", 1)[1])
        if state in unique_words_per_state:
            if observation not in unique_words_per_state[state]:
                current = unique_words_per_state[state]
                current.add(observation)
                unique_words_per_state[state] = current
        else:
            unique_words_per_state[state] = set()
for x in unique_words_per_state:
    total_unique_words = len(unique_words_per_state[x])
    unique_words_per_state[x] = total_unique_words
unique_words_per_state = {k: v for k, v in sorted(unique_words_per_state.items(), key=lambda item: -item[1])}

unique_words = list(set(observations))
unique_states = list(set(emission_states))
total_lines = len(training_lines)
transitions = Counter(transitions)
transition_states = Counter(transition_states)
emissions = Counter(emissions)
emission_states = Counter(emission_states)
transition_probability = get_transition_probabilities(transitions, transition_states, len(unique_states))
emission_probability = get_emission_probabilities(emissions, emission_states)
first_word_states = Counter(first_word_states)
first_word_states_probabilities = get_first_word_state_probabilities()

create_model("hmmmodel.txt", transition_probability, emission_probability, first_word_states_probabilities, unique_words_per_state, unique_words, unique_states, total_lines)
