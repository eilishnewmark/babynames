import re
from collections import defaultdict
import itertools

# r = re.compile(r"(\d+):([A-Z]'?[a-z]*'?-?[A-Z]?[a-z]*-?[A-Z]?[a-z]*)\ssex.([A-Z]+).,count.(\d+).")
name_sex_count = re.compile(r"(\d+):(\S+) sex\(([A-Z]+)\),count\((\d+)\)")
fname_pattern = re.compile(r".+namedata/scotbabies\d+.txt")

class Babies:
    def __init__(self, year=None, sex=None):
        self.year = year
        self.sex = sex

    def read_data_from_file(self):
        """Returns: data in file for that year in dictionary of form {("NAME", "SEX"): COUNT}"""
        data = defaultdict(int)
        try:
            with open(f"./namedata/scotbabies{self.year}.txt", "r") as f:
                f = f.readlines()
        except FileNotFoundError:
            print("Please ensure you have entered a year between 1974 and 2020")
        # get regex matches of the name, baby sex and count and enter into dict in the form {("NAME", "SEX"): COUNT}
        nsc_matches = [name_sex_count.match(entry.strip()) for entry in f]
        for m in nsc_matches:
            name, sex, count = m.group(2), m.group(3), int(m.group(4))
            data[(name, sex)] = count  
        return data


    def filter_by_sex(self):
        """Returns: dict filtered by either FEMALE or MALE babynames. If neither is specified, return original dict."""
        data = self.read_data_from_file()
        # ensure correct argument is entered
        if self.sex != "MALE" and self.sex != "FEMALE" and self.sex != None:
            raise AttributeError("Please insert either 'MALE', 'FEMALE' or None")
        # return list of filtered names
        if self.sex == None:
            return data
        else:
            filtered_by_sex = dict(filter(lambda entry: entry[0][1] == self.sex, data.items()))
            return filtered_by_sex


    def get_total_births(self):
        """Returns: int of total births recorded in the specified in filepath"""
        filtered_by_sex = self.filter_by_sex()
        total_births = sum(filtered_by_sex.values())
        if self.sex == "MALE" or self.sex == "FEMALE":
            print(f"Total no. of {self.sex} births in {self.year} was: {total_births}")
        else:
            print(f"Total no. of births in {self.year} was: {total_births}")
        return total_births


    def get_total_names(self):
        """Returns: int of total unique names recorded in the specified in filepath"""
        filtered_by_sex = self.filter_by_sex()
        unique_names = (set(map(lambda entry: entry[0], filtered_by_sex.keys())))
        total_names = len(unique_names)
        if self.sex == "MALE" or self.sex == "FEMALE":
            print(f"Total no. of {self.sex} names in {self.year} was: {total_names}")
        else:
            print(f"Total no. of names in {self.year} was: {total_names}")
        return total_names

    def get_unisex_names(self):
        """Returns: list of unisex names in data, ordered alphabetically and by their overall count, from most popular to least popular"""
        data = self.read_data_from_file()
        # get all names in data
        names = list(map(lambda entry: entry[0], data.keys()))
        # get only names that appear twice, as MALE and FEMALE
        unisex_names = set([name for name in names if names.count(name) > 1])
        # get the summed counts of those names
        unisex_counts = [data[(name, "FEMALE")] + data[(name, "MALE")] for name in unisex_names]
        # sort the zipped list of names and counts alphabetically
        unisex_sorted_alpha = sorted(list(zip(unisex_names, unisex_counts)))
        # sort the alphabetised names and counts by the counts, only printing the names in the final list
        unisex_sorted_counts = [i[0] for i in sorted(unisex_sorted_alpha, key = lambda entry: entry[1], reverse=True)]
        return unisex_sorted_counts

    def get_names_beginning_with(self, first_char):
        """Returns: list of names starting with the specified character, sorted alphabetically and filtered by the sex specified in the Babies class"""
        # get data filetered by sex specified in Class object
        filtered_by_sex = self.filter_by_sex()
        # check that the user has entered the correct argument type
        if not first_char.isalpha():
            print("Specified character should be a capital letter")
        # filter keys by the first character of the first element in each key tuple (Name, SEX) and make list with only that first Name element
        first_char_names = [i[0] for i in list(filter(lambda item: item[0].startswith(first_char.upper()), filtered_by_sex.keys()))]
        return first_char_names

    def get_top_n(self, N):
        """Returns: list of top N names in the data, if N is <= total number of names in the data."""
        total_names = self.get_total_names()
        try:
            filtered_by_sex = self.filter_by_sex()
            # sort data dict by count value, from highest to lowest count
            sorted_by_count = sorted(filtered_by_sex.items(), key=lambda entry: entry[1], reverse=True)  
            if total_names >= N > 0:
                top_n = sorted_by_count[:N]
                top_n_names = [entry[0][0] for entry in top_n]
                return top_n_names
            else:
                return f"N should be an integer between 1 and {total_names}"
        except TypeError:
            return f"N should be an integer between 1 and {total_names}"

    def get_name_length_summary(self, as_percentage=False):
        """Returns: list of (name length, baby count/percentage) tuples"""
        filtered_by_sex = self.filter_by_sex()
        # get sum of total number of babies in data
        total_count = sum(filtered_by_sex.values())
        # get corresponding baby counts for each name length
        name_length_counts = defaultdict(int)
        for name_sex, count in filtered_by_sex.items():
            name_length_counts[len(name_sex[0])] += count
        # sort name lengths by count (highest to lowest) and turn into list of (length, count) tuples
        name_length_counts = list(sorted(name_length_counts.items(), key = lambda entry: entry[1], reverse=True))
        # if as a percentage, return list of tuples with counts as percentage of total number of babies
        if as_percentage:
            name_length_perc = list(map(lambda entry: (entry[0], entry[1]/total_count * 100), name_length_counts))
            return name_length_perc
        return name_length_counts



def do_name_diff(year1, year2):
    """Returns: tuple of (names present only in year1 data, names present only in year2 data, names present in year1 and year2 data)"""
    year1_names = set(map(lambda entry: entry[0], year1.filter_by_sex().keys())) 
    year2_names = set(map(lambda entry: entry[0], year2.filter_by_sex().keys())) 

    data_intersection = list(year1_names.intersection(year2_names))
    only_year2 = list(year2_names - year1_names)
    only_year1 = list(year1_names - year2_names)

    return (only_year1, only_year2, data_intersection)

babies_2020 = Babies(year=2020, sex=None)
babies_1974 = Babies(year=1974, sex=None)





