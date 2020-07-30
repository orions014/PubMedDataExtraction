from pymed import PubMed
from address_parser import Parser
import json
import re


# Create a PubMed object that GraphQL can use to query
# Note that the parameters are not required but kindly requested by PubMed Central
# https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
pubmed = PubMed(tool="MyTool", email="my@email.address")

# Create a GraphQL query in plain text
#query = "occupational health[Title]"
query = 'where:{[Date - Create]:"2019/01/13"}'

print(query)
# Execute the query against the API
results = pubmed.query(query, max_results=3)

# Loop over the retrieved articles
for article in results:

    # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle)
   # print(type(article))

    # Print a JSON representation of the object
    #print(article.toJSON())
    # parse x:
    jsonData = json.loads(article.toJSON())

    # the result is a Python dictionary:
    # print(jsonData['authors'])
    authors_list = jsonData['authors']
    parser = Parser()
    for index in range(0,len(authors_list)):
        print("affiliation ",authors_list[index]["affiliation"])
        # print("Author number ",index," ", authors_list[index]['firstname']," ",authors_list[index]["lastname"])
        # line = re.sub(r"[\w\W]* ((Hospital|University|Centre|Law School|School|Academy|Department)[\w -]*)[\w\W]*$",
        #               r"\1", authors_list[index]["affiliation"])
        # print("Institute name ",line)
        affiliation = authors_list[index]["affiliation"]
        # adr = parser.parse(affiliation)
        # print(adr.dict)
        # print(adr)






