from FetchPubMedData import FetchPubMedData

fetchData = FetchPubMedData()
while True:

        exit_code = input("To exit write \"exit\" or to continue write \"no\" :") or "no exit"

        if exit_code == "no":
            date = input("Enter your date as YYYY/MM/DD e.g 2019/01/14: ")
            zipcode = input("Enter zip code to find paper according to US zip code e.g 99612 or Write no: ")

            while True:
                if fetchData.validate(date) == False:
                    date = input("Please enter valid date as YYYY/MM/DD e.g 2019/01/14: ")
                else:
                    query = "where:{[Date - Create]:\"" + date + "\"}"
                    fetchData.get_pubmed_data(query, zipcode, date)
                    break
        else:
            break






