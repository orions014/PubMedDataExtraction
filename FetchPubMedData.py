from pymed import PubMed
from address_parser import Parser
import json
import pandas as pd
import en_core_web_sm
from ZipCodeProvider import ZipCodeProvider
import nltk
from nltk.tag import pos_tag, map_tag
import datetime
nltk.download('universal_tagset')
nltk.download('averaged_perceptron_tagger')


class FetchPubMedData():
    def __init__(self):
        super(FetchPubMedData, self).__init__()
        self.nlp = en_core_web_sm.load()
        self.zip_code_provider = ZipCodeProvider()
        self.state_dict = self.zip_code_provider.my_dict
        self.us_state_list = self.zip_code_provider.state_list
        # print(self.state_dict)
        self.is_us = False

    def validate(self,date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y/%m/%d')
            return True
        except:
            return False

    def get_address_with_zipcode(self, affiliation):

        text = nltk.word_tokenize(affiliation)
        posTagged = pos_tag(text)
        simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
        all_noun = list()
        zipcode = "0"
        for tpl in simplifiedTags:

            if tpl[1] == 'NOUN':
                value = tpl[0].replace(".", "")
                all_noun.append(value.lower())

        for wrd in set(all_noun):
            try:
                self.state_dict["us"][wrd]
                self.is_us = True
                for place in all_noun:
                    try:
                        zipcode = str(self.state_dict['us'][wrd][place])
                        # print("Not Failed at all!")
                        break

                    except:
                        values_view = self.state_dict['us'][wrd].values()
                        # print("Values view ",values_view)
                        value_iterator = iter(values_view)
                        first_value = next(value_iterator)
                        zipcode = first_value
                        # print(first_value)
                        # print("Failed in places.")

            except:
                pass
                # print("Failed for US states")

        return zipcode

    def has_match_zipcode_of_authprs(self, authors_list, searched_zipcode):
        num_authors = len(authors_list)
        count_match = 0
        for index in range(0, num_authors):
            affiliation = authors_list[index]["affiliation"] or "<NOT_AVAILABLE>"
            zipcode = str(self.get_address_with_zipcode(affiliation))
            if int(zipcode) == searched_zipcode and searched_zipcode != 0:
                count_match +=1
        return count_match

    def get_organization(self, affiliation):
        for tok in self.nlp(affiliation):
            # if tok.ent_type_ == "LOC":
            #     address+= tok.text+" "
            if tok.ent_type_ == "ORG":
                return tok.text
    def get_pubmed_data(self, query, searched_zipcode, date, maximum_number_of_value=3):
        csv_data = {"affiliation":[],"number_of_authors":[],"authors_name": [],"authors_institute":[],"authors_address":[],"authors_zipcode":[],
                           "paper_title":[],"publication_date":[],"journal":[]}
        pubmed = PubMed(tool="MyTool", email="my@email.address")
        parser = Parser()

        results = pubmed.query(query, max_results=maximum_number_of_value)
        is_queried_by_zipcode = searched_zipcode.isdecimal()

        if is_queried_by_zipcode:
            searched_zipcode = int(searched_zipcode)

        for article in results:
            jsonData = json.loads(article.toJSON())
            authors_list = jsonData['authors']
            authors_name = ""
            authors_institute = ""
            authors_affiliation = ""
            authors_address = ""
            authors_zipcode = ""
            num_authors = len(authors_list) or 0
            counted_matched = 0
            if is_queried_by_zipcode:
                counted_matched = self.has_match_zipcode_of_authprs(authors_list, searched_zipcode)
            if (not is_queried_by_zipcode) or (is_queried_by_zipcode and counted_matched>0):
                for index in range(0, num_authors):
                    affiliation = authors_list[index]["affiliation"]  or "<NOT_AVAILABLE>"
                    zipcode = str(self.get_address_with_zipcode(affiliation))
                    # print(type(zipcode))
                    # print(zipcode)
                    author_name =  authors_list[index]['firstname']+" "+authors_list[index]["lastname"]  or "<NOT_AVAILABLE>"
                    author_institute = ""
                    author_institute += self.get_organization(affiliation=affiliation) + " "
                    authors_affiliation += affiliation
                    authors_name += author_name
                    authors_institute += author_institute
                    authors_address += str(parser.parse(affiliation))
                    authors_zipcode += zipcode
                    if num_authors != index+1:
                        authors_name += "||"
                        authors_institute += "||"
                        authors_affiliation += "||"
                        authors_address += "||"
                        authors_zipcode +="||"
            else:
                break
            paper_title = jsonData['title'] or "<NOT_AVAILABLE>"
            publication_date = jsonData['publication_date'] or "<NOT_AVAILABLE>"
            journal = jsonData['journal'] or "<NOT_AVAILABLE>"

            if self.is_us:
                if not is_queried_by_zipcode or (is_queried_by_zipcode and counted_matched>0):

                    csv_data["authors_name"].append(authors_name)
                    csv_data["affiliation"].append(authors_affiliation)
                    csv_data["authors_institute"].append(authors_institute)
                    csv_data["paper_title"].append(paper_title)
                    csv_data["publication_date"].append(publication_date)
                    csv_data["journal"].append(journal)
                    csv_data["authors_address"].append(authors_address)
                    csv_data["number_of_authors"].append(num_authors)
                    csv_data["authors_zipcode"].append(authors_zipcode)
                    self.is_us = False

            # if not is_queried_by_zipcode or (is_queried_by_zipcode and counted_matched > 0):
            #
            #     df = pd.DataFrame(csv_data)
            #     # print(df.head())
            #     df.to_csv("PubMedData_from.csv", index=False)

        print("Size of csv ",len(csv_data["paper_title"]))
        if len(csv_data["paper_title"]) > 0:
            df = pd.DataFrame(csv_data)
            print(df.head())
            df.to_csv("PubMedData_from.csv", index=False)







