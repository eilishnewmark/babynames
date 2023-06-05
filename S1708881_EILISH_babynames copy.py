# import standard library modules you find useful here (e.g. "re" module?) 
# (important: use *only* modules that come as standard with Python - i.e. will be on markers' machines)
import re

r = re.compile(r"(\d+):([A-Z]'?[a-z]*'?-?[A-Z]?[a-z]*-?[A-Z]?[a-z]*)\ssex.([A-Z]+).,count.(\d+).")
r2 = re.compile(r".+namedata/scotbabies\d+.txt")

class Babies:
    def __init__(self, filepath=None):
        self.filepath = filepath
        f = r2.match(filepath)
        if f is None:
            raise FileNotFoundError("Please enter file name in form './namedata/scotbabiesYEAR.txt'")
        self.read_names_from_file(filepath)

    def read_names_from_file(self, filepath):
        self.filepath = filepath
        names = []
        with open(filepath, "r") as f:
            f = f.readlines()
            for entry in f:
                entry.strip()
                m = r.match(entry)
                names.append([m.group(2), m.group(3), m.group(4)])
        return names

    def get_sex_list(self, sex=None):
        self.sex = sex
        try:
            sex == "male" or "female"
        except AttributeError:
            print("Please insert either male or female in lower case")
        sex_lst = []
        names = self.read_names_from_file(self.filepath)
        for name in names:
            if sex == 'female' and name[1] == 'FEMALE':
                sex_lst.append(name)
            elif sex == 'male' and name[1] == 'MALE':
                sex_lst.append(name)
            elif sex is None:
                sex_lst.append(name)
        try:
            sex_lst[0]
        except IndexError:
            print("Please insert either male or female in lower case")
        return sex_lst

    def get_total_births(self, sex=None):
        sex_lst = self.get_sex_list(sex)
        total_births = sum(list(map(lambda item: int(item[2]), sex_lst)))
        return total_births

    def get_total_names(self, sex=None):
        sex_lst = self.get_sex_list(sex)
        name_lst = []
        for name in sex_lst:
            if name[0] not in name_lst:
                name_lst.append(name[0])
            else:
                continue
        total_names = len(name_lst)
        return total_names

    def get_unisex_names(self):
        names = self.read_names_from_file(self.filepath)
        unisex_list = []
        name_lst = []
        final_sort = []
        [name_lst.append(name[0]) for name in names]
        unisex_names = list(set([name for name in name_lst if name_lst.count(name) > 1]))
        for name in names:
            for entry in unisex_names:
                count = 0
                if entry == name[0]:
                    count += int(name[2])
                    unisex_list.append([entry, count])
        sorted_unisex = sorted(unisex_list, key=lambda x: int(x[1]), reverse=True)
        [final_sort.append(entry[0]) for entry in sorted_unisex]
        return final_sort

    def get_names_beginning_with(self, first_char, sex=None):
        sex_lst = self.get_sex_list(sex)
        first_char = first_char.upper()
        if first_char.isalpha() is False:
            print("Specified character should be a capital letter")
        names_beginning_list = list(filter(lambda item: item[0].startswith(first_char), sex_lst))
        return list(map(lambda item: item[0], names_beginning_list))

    def get_top_n(self, N, sex=None):
        try:
            sex_lst = self.get_sex_list(sex)
            sex_lst = sorted(sex_lst, key=lambda x: int(x[2]), reverse=True)
            if self.get_total_names(sex) >= N > 0:
                sex_lst = sex_lst[:N]
                return list(map(lambda item: (item[0], int(item[2])), sex_lst))
            else:
                return f"N should be an integer between 1 and {self.get_total_names(sex)}"
        except TypeError:
            return f"N should be an integer between 1 and {self.get_total_names(sex)}"

    def get_name_length_summary(self, as_percentage=False, sex=None):
        sex_lst = self.get_sex_list(sex)
        total_babies = 0
        name_length = []
        baby_count_list = []
        baby_percentage_list = []
        for name in sex_lst:
            total_babies += int(name[2])
            name_length.append(len(name[0]))
            name_length = sorted(name_length)
        for number in range(2, int(name_length[-1]) + 1):
            baby_count = 0
            for name in sex_lst:
                if number == len(name[0]):
                    baby_count += int(name[2])
            baby_count_list.append((number, baby_count))
            baby_count_list = sorted(baby_count_list, reverse=True)
        if not as_percentage:
            return baby_count_list
        else:
            for entry in baby_count_list:
                baby_percentage_list.append((entry[0], ((entry[1] / total_babies) * 100)))
            return baby_percentage_list

def do_name_diff(babies_obj1, babies_obj2):
    obj1_names = babies_obj1.get_sex_list()
    obj2_names = babies_obj2.get_sex_list()
    list_of_names_only_in_obj1 = []
    list_of_names_only_in_obj2 = []
    list_of_names_in_both = []
    for names in obj1_names:
        if names not in obj2_names:
            list_of_names_only_in_obj1.append(names[0])

    for names in obj2_names:
        if names not in obj1_names:
            list_of_names_only_in_obj2.append(names[0])

    for names in obj1_names:
        if names in obj2_names:
            list_of_names_in_both.append(names[0])

    return (list_of_names_only_in_obj1, list_of_names_only_in_obj2, list_of_names_in_both)




