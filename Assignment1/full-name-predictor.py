import sys

male_names_dict = {}  # contains name with frequency per 100k
female_names_dict = {}  # contains name with frequency per 100k
last_name_dict = {}  # contains surname with frequency per 100k
names_set = set()
last_names_set = set()

titles_set = set()

predefined_titles = ["lieutenant", "captain", "major", "colonel", "brigadier", "general", "professor", "reverend", "doctor"]
nothing = ""


def create_metadata(_file, _is_surname, _freq_index, global_dict, global_set):
    file = open(_file, "r")
    for line in file:
        entries = line.split(",") if _is_surname else line.split()
        if entries[1] == "rank":
            continue
        if len(entries) < 4:
            print("Invalid entry in file : " + line)
            continue
        if entries[0] not in global_dict.keys():  # assumes names to be unique. If duplicate, keeps higher freq in value
            # for name files, frequency = frequency * 1000 (as name file has %, whereas surname file as prop100k)
            global_dict[entries[0]] = float(entries[_freq_index]) if _is_surname else float(entries[_freq_index]) * 1000
        global_set.add(entries[0])
    file.close()


def predict_name(_test_file, _output_file):
    input_file = open(_test_file, "r")
    output_file = open(_output_file, "w")

    for line in input_file:
        people = line.split(" AND ")
        first_person_name = people[0].strip()
        second_person_name = people[1].strip()
        if is_last_name_needed(first_person_name, second_person_name):
            first_person_name += " " + predict_last_name(first_person_name, second_person_name)
        output = line.strip() + "," + first_person_name.strip() + "\n"
        output_file.write(output)
    input_file.close()
    output_file.close()


def is_last_name_needed(first_person_name, second_person_name):
    first_names = first_person_name.split()
    second_names = second_person_name.split()

    first_name_len = len(first_names)
    second_name_len = len(second_names)

    title_present = is_title_present(first_person_name)

    # the length of first person's name should be <3 and <= second person's name length
    if title_present:
        if first_name_len - 1 >= 3 or first_name_len - 1 > second_name_len:
            return False
    else:
        if first_name_len >= 3 or first_name_len > second_name_len:
            return False

    if first_names[first_name_len - 1] not in names_set:
        # already has a last name
        return False


    # if surname present in first person's name has greater surname frequency than name frequency, then return false
    first_surname = get_best_existing_surname(first_person_name)
    # last_name = first_names[first_name_len - 1]
    dict_to_look = male_names_dict if is_male(first_person_name) else female_names_dict


    # if first_surname == nothing:
    #     temp_surname_freq = last_name_dict[last_name] if last_name in last_name_dict.keys() else 0
    #     temp_last_name_freq = dict_to_look[last_name] if last_name in dict_to_look.keys() else 0
    #     if temp_surname_freq > temp_last_name_freq:
    #         first_surname = last_name

    surname_freq = last_name_dict[first_surname] if first_surname in last_name_dict.keys() else 0
    name_freq = dict_to_look[first_surname] if first_surname in dict_to_look.keys() else 0
    if first_surname != nothing and first_names.index(first_surname) == first_name_len - 1:
        if surname_freq > name_freq:
            return False

    return True


def is_title_present(person_name):
    names = person_name.split()
    title_present = False
    title = ""
    for name in names:
        if name in titles_set or name.lower() in predefined_titles:
            return True
        elif name in names_set:
            break
        else:
            title_present = True
            title += name + " "
    if title_present:
        titles_set.add(title.strip())
        print("New Title found : " + title)
    return title_present


def is_male(person_name):
    title_present = is_title_present(person_name)

    first_name = person_name.split()[1 if title_present else 0]

    male_name_frequency = male_names_dict[first_name] if first_name in male_names_dict.keys() else 0
    female_name_frequency = female_names_dict[first_name] if first_name in female_names_dict.keys() else 0

    return True if male_name_frequency > female_name_frequency else False


def get_best_existing_surname(person_name):
    title_present = is_title_present(person_name)

    start = 1 if title_present else 0
    names = person_name.split()

    name_len = len(names)

    if name_len == 1:
        return nothing

    dict_to_look = male_names_dict if is_male(person_name) else female_names_dict

    highest_surname_frequency = 0
    best_surname = ""
    last_name_not_found = True
    for x in range(start, name_len):
        name = names[x]
        name_frequency = dict_to_look[name] if name in dict_to_look.keys() and dict_to_look[name] > 20 else 0
        surname_frequency = last_name_dict[name] if name in last_name_dict.keys() and last_name_dict[name] > 5 else 0

        if name not in dict_to_look.keys():
            if x == start:
                # cant have full second name as surname
                continue
            last_name_not_found = False
            # break
            if surname_frequency > highest_surname_frequency:
                highest_surname_frequency = surname_frequency
                best_surname = name
        else:
            # consider a name as surname only if its name_frequency < 20 and its surname_freq is higher than name
            if name_frequency < 20 and surname_frequency > name_frequency:
                if x == start:
                    # cant have full second name as surname
                    continue
                last_name_not_found = False
                # break
                if surname_frequency > highest_surname_frequency:
                    highest_surname_frequency = surname_frequency
                    best_surname = name
            continue

    if last_name_not_found and x == name_len - 1:
        return nothing
    else:
        return best_surname
        # return name


def predict_last_name(first_person_name, second_person_name):
    first_person_surname = get_best_existing_surname(first_person_name)
    first_person_surname_frequency = last_name_dict[first_person_surname] if first_person_surname in last_name_dict.keys() and last_name_dict[first_person_surname] > 15 else 0

    title_present = is_title_present(second_person_name)
    start = 1 if title_present else 0
    names = second_person_name.split()

    name_len = len(names)

    dict_to_look = male_names_dict if is_male(second_person_name) else female_names_dict

    last_name_not_found = True
    # find the first word in second name which is not in names_set and then return from that index as surname

    best_surname_index = -1
    highest_surname_frequency = 0

    for x in range(start, name_len):
        name = names[x]
        name_frequency = dict_to_look[name] if name in dict_to_look.keys() and dict_to_look[name] > 20 else 0
        surname_frequency = last_name_dict[name] if name in last_name_dict.keys() and last_name_dict[name] > 5 else 0

        if name not in dict_to_look.keys():
            if x == start:
                # cant have full second name as surname
                continue
            last_name_not_found = False
            break
            # if surname_frequency > highest_surname_frequency:
            #     highest_surname_frequency = surname_frequency
            #     best_surname_index = x
        else:
            if surname_frequency > name_frequency:
                if x == start:
                    # cant have full second name as surname
                    continue
                last_name_not_found = False
                break
                # if surname_frequency > highest_surname_frequency:
                #     highest_surname_frequency = surname_frequency
                #     best_surname_index = x
            continue

    # no surname found in second person name
    if last_name_not_found:
        # if first person just has single name, return last name of second person
        if len(first_person_name.split()) == 1:
            return name

        # if first person doesnt have surname, return last name of second person if its freq > first persons last name freq
        if first_person_surname == nothing:
            # first person also did not have a surname
            # check if last word frequency in second person's name is greater than first person's name, then return that
            first_person_names = first_person_name.split()
            first_person_names_len = len(first_person_names)
            last_name_freq = last_name_dict[first_person_names[first_person_names_len-1]] if first_person_names[first_person_names_len-1] in last_name_dict.keys() else 0
            if surname_frequency > last_name_freq:
                return name
        return nothing


    # predicted_surname_frequency = last_name_dict[name] if name in last_name_dict.keys() else 0
    # if not valid_surname(first_person_names[first_person_names_len-1], name):
    #     return nothing

    # if first_person_surname_frequency > predicted_surname_frequency:
    #     #CASES:
    #     #DOCTOR DENNIS RONALD BARRY AND MARILYN SHARON EDMONDS,DOCTOR DENNIS RONALD BARRY
    #     #CHARLES DENNIS LOGAN AND PROFESSOR MARIAN MICHELLE TILLER,CHARLES DENNIS LOGAN
    #     return nothing

    predicted_last_name = ""
    for i in range(x, name_len):
        predicted_last_name += names[i] + " "
    return predicted_last_name.strip()


# def valid_surname(first, predicted):
#     first_surname_frequency = last_name_dict[first] if first in last_name_dict.keys() else 0
#     predicted_surname_frequency = last_name_dict[predicted] if predicted in last_name_dict.keys() else 0
#     return predicted_surname_frequency > first_surname_frequency


def print_accuracy(output_file, key_file):
    correct = 0
    incorrect = 0
    with open(output_file) as output, open(key_file) as key:
        for output_line, key_line in zip(output, key):
            output_text = output_line.split(",")
            key_text = key_line.split(",")

            output_name = output_text[1].strip()
            key_name = key_text[1].strip()
            if output_name == key_name:
                correct += 1
            else:
                incorrect += 1
                print(output_text[0] + " Excepted : " + key_name + ", Found : " + output_name)

    accuracy = correct * 100 / (correct + incorrect)
    print("Correct : " + str(correct))
    print("Incorrect : " + str(incorrect))
    print("Accuracy : " + str(accuracy) + "%")


# test_file = sys.argv[1]
test_file = "dev-test.csv"
key_file = "dev-key.csv"

output_file = "full-name-output.csv"

male_names = "dist.male.first.txt"
female_names = "dist.female.first.txt"
last_names = "Names_2010Census.csv"

create_metadata(male_names, False, 1, male_names_dict, names_set)
create_metadata(female_names, False, 1,  female_names_dict, names_set)
create_metadata(last_names, True, 3, last_name_dict, last_names_set)

predict_name(test_file, output_file)

print_accuracy(output_file, key_file)
