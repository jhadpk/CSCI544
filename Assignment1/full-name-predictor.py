import sys

male_names_dict = {}  # contains name with frequency per 100k
female_names_dict = {}  # contains name with frequency per 100k
last_name_dict = {}  # contains surname with frequency per 100k
names_set = set()
last_names_set = set()

titles_set = set()

predefined_titles = ["lieutenant", "captain", "major", "colonel", "brigadier", "general", "professor", "reverend",
                     "doctor"]
nothing = ""
space = " "


"""
Populates male, female and last_name dictionaries with name as key and frequency per 100k as value.
For name files, frequency = frequency * 1000 (as name file has %, whereas surname file as prop100k, hence 100000/100)
"""
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


"""
Reads input_file of names and outputs the predicted name in output_file
"""
def predict_name(_input_file, _output_file):
    input_file = open(_input_file, "r")
    output_file = open(_output_file, "w")

    for line in input_file:
        people = line.split(" AND ")
        first_name = people[0].strip()
        second_name = people[1].strip()
        if is_surname_needed(first_name, second_name):
            first_name += space + predict_last_name(first_name, second_name).strip()
        output = line.strip() + "," + first_name.strip() + "\n"
        output_file.write(output)
    input_file.close()
    output_file.close()


"""
Checks if the given first name requires surname
@:param first_name 
@:param second_name
1. length of first name (barring title) should be < 3.
2. length of first name (barring title) should be <= length of second name.
3. last word in first name should not be a surname (missing in names_set).
4. best surname of first name should not have the last index - this means it already has a surname

@:return boolean true if first_name needs a surname
"""
def is_surname_needed(first_name, second_name):
    first_names = first_name.split()
    second_names = second_name.split()

    first_name_len = len(first_names)
    second_name_len = len(second_names)

    title_present = is_title_present(first_name)

    # the length of first person's name should be <3 and <= second person's name length
    if title_present:
        if first_name_len - 1 >= 3 or first_name_len - 1 > second_name_len:
            return False
    else:
        if first_name_len >= 3 or first_name_len > second_name_len:
            return False

    if first_names[first_name_len - 1] not in names_set and first_name_len - 1 != 0:
        # already has a last name
        return False

    # if surname present in first person's name then return false
    first_surname = get_best_existing_surname(first_name)
    if first_surname != nothing and first_names.index(first_surname) == first_name_len - 1:
        return False
    return True


"""
Checks if title present in the given name
@:param person_name
1. if the first word in the name is missing from names_set or present in predefined titles list.

@:return boolean true if title is present in name
"""
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
            title += name + space
    if title_present:
        titles_set.add(title.strip())
        print("New Title found : " + title)
    return title_present


"""
Returns true if the given name has higher frequency in male_names_dict compared to female_names_dict
"""
def is_male(person_name):
    title_present = is_title_present(person_name)
    first_name = person_name.split()[1 if title_present else 0]
    male_name_frequency = male_names_dict[first_name] if first_name in male_names_dict.keys() else 0
    female_name_frequency = female_names_dict[first_name] if first_name in female_names_dict.keys() else 0
    return True if male_name_frequency > female_name_frequency else False


"""
Returns the name with highest surname frequency in the given name
@:param person_name

1. traverses through all the names in person_name to figure out the name with best surname frequency.
2. a name is considered - a firstname only if its name frequency is > 20 and surname if its surname frequency is > 5.
3. if a name is missing from names_set (definite surname), even then we call it a name, if the difference between 
name and surname frequency is < 30.

@:return the best surname across the person_name
"""
def get_best_existing_surname(person_name):
    title_present = is_title_present(person_name)

    start = 1 if title_present else 0
    names = person_name.split()
    name_len = len(names)

    if name_len == 1:
        return nothing

    dict_to_look = male_names_dict if is_male(person_name) else female_names_dict

    best_surname_frequency = 0
    best_surname = ""
    last_name_found = False
    for x in range(start, name_len):
        name = names[x]
        name_frequency = dict_to_look[name] if name in dict_to_look.keys() and dict_to_look[name] > 20 else 0
        surname_frequency = last_name_dict[name] if name in last_name_dict.keys() and last_name_dict[name] > 5 else 0

        if name not in dict_to_look.keys():
            last_name_found = True
            if surname_frequency > best_surname_frequency:
                best_surname_frequency = surname_frequency
                best_surname = name
        else:
            # consider a name as surname only if its name_frequency < 20 and its surname_freq is higher than name
            if surname_frequency > name_frequency + 30:
                last_name_found = True
                if surname_frequency > best_surname_frequency:
                    best_surname_frequency = surname_frequency
                    best_surname = name
            continue
    return best_surname if last_name_found else nothing


"""
Returns the predicted surname in the given first_name using the second_name
@:param first_name
@:param second_name

1. traverses through all the names in second_name to figure out the name with best surname frequency.
2. a name is considered a surname if its missing from names set or if its surname frequency > name frequency + 20.
3. break at any point where name doesnt belong to names_set
4. if no surname is found in second_name, then return the last word in second_name if :
    a) first_name is of length = 1.
    b) first_name doesnt have any surname and surname_frequency of second_name's last word + 20 > surname_frequency 
       of first_name's last word

@:return the surname from point where loop broke
"""
def predict_last_name(first_name, second_name):
    title_present = is_title_present(second_name)
    start = 1 if title_present else 0
    names = second_name.split()
    name_len = len(names)

    dict_to_look = male_names_dict if is_male(second_name) else female_names_dict

    last_name_found = False

    # find the first word in second name which is not in names_set and then return from that index as surname
    for x in range(start, name_len):
        name = names[x]
        name_frequency = dict_to_look[name] if name in dict_to_look.keys() else 0
        surname_frequency = last_name_dict[name] if name in last_name_dict.keys() else 0

        if name not in dict_to_look.keys():
            if x == start:
                # cant have full name as surname
                continue
            last_name_found = True
            break
        else:
            if surname_frequency != 0 and surname_frequency > name_frequency + 20:
                if x == start:
                    # cant have full name as surname
                    continue
                last_name_found = True
                break
            continue

    # no surname found in second person name
    if not last_name_found:
        # if first person just has single name, return last name of second person
        if len(first_name.split()) == 1:
            return name

        # if first person doesnt have surname, return last name of second person if its freq > first persons last name freq
        first_surname = get_best_existing_surname(first_name)
        if first_surname == nothing:
            # first person also did not have a surname
            # check if last word frequency in second person's name is greater than first person's name, then return that
            first_names = first_name.split()
            first_names_len = len(first_names)
            last_name_freq = last_name_dict[first_names[first_names_len - 1]] if first_names[
                                                                                     first_names_len - 1] in last_name_dict.keys() else 0
            # even if second person's last name freq + 20 is greater than first person's last name freq, return
            if surname_frequency > 0 and surname_frequency + 20 > last_name_freq:
                return name
        return nothing

    return space.join(names[x:])


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
                print(output_text[0] + ", Expected : " + key_name + ", Found : " + output_name)

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
create_metadata(female_names, False, 1, female_names_dict, names_set)
create_metadata(last_names, True, 3, last_name_dict, last_names_set)

predict_name(test_file, output_file)

print_accuracy(output_file, key_file)
