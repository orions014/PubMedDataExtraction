from pymed import PubMed
from address_parser import Parser
import json
import pandas as pd
import en_core_web_sm


class FetchPubMedData():
    def __init__(self):
        super(FetchPubMedData, self).__init__()
        self.nlp = en_core_web_sm.load()


    def getPubMedData(self,query,maximum_number_of_value=10):
        csv_data = {"affiliation":[],"number_of_authors":[],"authors_name": [],"authors_institute":[],"authors_address":[],
                           "paper_title":[],"publication_date":[],"journal":[]}
        pubmed = PubMed(tool="MyTool", email="my@email.address")
        parser = Parser()
        results = pubmed.query(query, max_results=maximum_number_of_value)
        for article in results:
            jsonData = json.loads(article.toJSON())
            authors_list = jsonData['authors']
            authors_name = ""
            authors_institute = ""
            authors_affiliation = ""
            authors_address = ""
            num_authors = len(authors_list) or 0
            for index in range(0, num_authors):
                affiliation = authors_list[index]["affiliation"]  or "<NOT_AVAILABLE>"
                author_name =  authors_list[index]['firstname']+" "+authors_list[index]["lastname"]  or "<NOT_AVAILABLE>"
                author_institute = ""
                for tok in self.nlp(affiliation):
                    # if tok.ent_type_ == "LOC":
                    #     address+= tok.text+" "
                    if tok.ent_type_ == "ORG":
                        author_institute += tok.text + " "
                authors_affiliation += affiliation
                authors_name += author_name
                authors_institute += author_institute
                authors_address += str(parser.parse(affiliation))
                if num_authors != index+1:
                    authors_name += "||"
                    authors_institute += "||"
                    authors_affiliation += "||"
                    authors_address += "||"


            paper_title = jsonData['title'] or "<NOT_AVAILABLE>"
            publication_date = jsonData['publication_date'] or "<NOT_AVAILABLE>"
            journal = jsonData['journal'] or "<NOT_AVAILABLE>"

            csv_data["authors_name"].append(authors_name)
            csv_data["affiliation"].append(authors_affiliation)
            csv_data["authors_institute"].append(authors_institute)
            csv_data["paper_title"].append(paper_title)
            csv_data["publication_date"].append(publication_date)
            csv_data["journal"].append(journal)
            csv_data["authors_address"].append(authors_address)
            csv_data["number_of_authors"].append(num_authors)

            df = pd.DataFrame(csv_data)
            # print(df.head())
            df.to_csv("PubMedData.csv", index=False)










