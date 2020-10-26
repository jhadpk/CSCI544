from collections import Counter
import sys


def get_transition_probabilities(transitions, transitions_states, total_states):
    transition_probabilities = {}
    for transition in transitions:
        source = transition.split("->")[0]
        transition_probabilities[transition] = (transitions[transition] + 1) / (transitions_states[source] + total_states)
    return transition_probabilities


def get_emission_probabilities(emissions, emission_states):
    emission_probabilities = {}
    for emission in emissions:
        state = emission.rsplit("/", 1)[1]
        emission_probabilities[emission] = emissions[emission] / emission_states[state]
    return emission_probabilities


def create_model(file_name, transitions, transition_states, emissions, emission_states, q0, total_lines,
                 unique_words, unique_states, unique_words_per_tag, transition_probability, emission_probability):
    with open(file_name, 'w') as f:
        f.write("transitions=" + str(dict(transitions)) + "\n")
        f.write("transition_states=" + str(dict(transition_states)) + "\n")
        f.write("emissions=" + str(dict(emissions)) + "\n")
        f.write("emission_states=" + str(dict(emission_states)) + "\n")
        f.write("initial_states=" + str(dict(q0)) + "\n")
        f.write("total_lines=" + str(total_lines) + "\n")
        f.write("unique_words=" + str(unique_words) + "\n")
        f.write("unique_states=" + str(unique_states) + "\n")
        f.write("total_states=" + str(len(unique_states)) + "\n")
        f.write("unique_words_per_tag=" + str(dict(unique_words_per_tag)) + "\n")
        f.write("transition_probability_dict=" + str(dict(transition_probability)) + "\n")
        f.write("emission_probability_dict=" + str(dict(emission_probability)) + "\n")


initial_states = []
emissions = []
observations = []
emission_states = []
transitions = []
transition_states = []

unique_words_per_tag = {}
# training_file = sys.argv[1]
training_file = "hmm-training-data/it_isdt_train_tagged.txt"

f = open(training_file, encoding="utf8", errors='ignore').read().splitlines()

for line in f:
    words = line.split()
    emissions += words
    initial_states.append(words[0].split("/")[-1])  # first word state
    for i, word in enumerate(words):
        word_and_tag = word.rsplit("/", 1)
        observation = word_and_tag[0]
        state = word_and_tag[1]
        observations.append(observation)
        emission_states.append(state)
        if i < len(words) - 1:
            transition_states.append(state)
            transitions.append(state + "->" + words[i+1].rsplit("/", 1)[1])
        if state in unique_words_per_tag:
            if observation not in unique_words_per_tag[state]:
                current = unique_words_per_tag[state]
                current.add(observation)
                unique_words_per_tag[state] = current
        else:
            unique_words_per_tag[state] = set()
for x in unique_words_per_tag:
    total_unique_words = len(unique_words_per_tag[x])
    unique_words_per_tag[x] = total_unique_words
unique_words_per_tag = {k: v for k, v in sorted(unique_words_per_tag.items(), key=lambda item: -item[1])}


total_lines = len(f)
unique_words = list(set(observations))
unique_states = list(set(emission_states))
transitions = Counter(transitions)
transition_states = Counter(transition_states)
emissions = Counter(emissions)
emission_states = Counter(emission_states)
initial_states = Counter(initial_states)
transition_probability = get_transition_probabilities(transitions, transition_states, len(unique_states))
emission_probability = get_emission_probabilities(emissions, emission_states)

create_model("hmmmodel.txt", transitions, transition_states, emissions, emission_states, initial_states, total_lines,
             unique_words, unique_states, unique_words_per_tag, transition_probability, emission_probability)
