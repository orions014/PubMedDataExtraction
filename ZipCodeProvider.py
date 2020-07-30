import nltk
from nltk.tag import pos_tag, map_tag

nltk.download('universal_tagset')
nltk.download('averaged_perceptron_tagger')
import pandas as pd
from collections import defaultdict


class ZipCodeProvider:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ZipCodeProvider.__instance is None:
            ZipCodeProvider()
        return ZipCodeProvider.__instance

    def __init__(self):
        super(ZipCodeProvider, self).__init__()
        """ Virtually private constructor. """
        if ZipCodeProvider.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            names = ["Country", "Zip_Code", "Place", "State", "State_shortcut", "A", "B", "C", "D", "E", "F", "G"]
            dataframe = pd.read_csv("US.txt", sep='\t', engine='python', names=names)

            dataframe = dataframe[["Country", "Zip_Code", "Place", "State", "State_shortcut"]]
            dataframe = dataframe.dropna()

            dataframe = dataframe.applymap(lambda s: s.lower() if type(s) == str else s)

            self.state_list = list(set(dataframe["State"]))
            self.state_list.sort()

            self.my_dict = defaultdict(dict)
            for state in self.state_list:
                temp_dataframe = dataframe[(dataframe['State'] == state)]
                place_dict = dict()
                for ind in temp_dataframe.index:
                    place_dict[temp_dataframe["Place"][ind]] = temp_dataframe["Zip_Code"][ind]
                self.my_dict["us"][state] = place_dict
            ZipCodeProvider.__instance = self
