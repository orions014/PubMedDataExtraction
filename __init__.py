from FetchPubMedData import FetchPubMedData

fetchData = FetchPubMedData()
while True:

        exit_code = input("To exit write \"exit\" or to continue press enter :") or "c"

        if exit_code == "c":
            date = input("Enter your date as YYYY/MM/DD e.g 2019/01/14: ")
            print(date)
            date = date.replace(" ", "")
            zipcode = input("Enter zip code to find paper according to US zip code e.g 99612 or to continue without zip code "
                            "press enter: ") or "c"
            while True:
                if fetchData.validate(date) == False:
                    date = input("Please enter valid date as YYYY/MM/DD e.g 2019/01/14: ")
                else:
                    query = "where:{[Date - Create]:\"" + date + "\"}"
                    fetchData.get_pubmed_data(query, zipcode, date)
                    break
        else:
            break






