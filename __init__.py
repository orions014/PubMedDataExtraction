from FetchPubMedData import FetchPubMedData

date = input("Enter your date as YYYY/MM/DD e.g 2019/01/14: ")

query = "where:{[Date - Create]:\""+date+"\"}"

# print(query)

fetchData = FetchPubMedData()

fetchData.getPubMedData(query)



