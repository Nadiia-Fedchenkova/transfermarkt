
import pandas as pd
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook

class transfermarktTeamPlayers():

    def parse(self, url_list):

        for url in url_list:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
            }
            page_tree = requests.get(url, headers=headers)
            page_soup = BeautifulSoup(page_tree.content, 'html.parser')
            Numbers = []
            FullNames = []
            Positions = []
            DatesOfBirth = []
            Nationalities = []
            Heights = []
            Feet = []
            Contracts = []
            DatesOfBirth_Transformed = []
            Contracts_Transformed = []

            # extract player names
            Players = page_soup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})
            for i in range(0, len(Players)):
                FullNames.append(str(Players[i]).split('" class', 1)[0].split('<img alt="', 1)[1])

            # extract positions
            PositionList = page_soup.find_all("table", {"class": "inline-table"})
            for position in PositionList:
                Positions.append(str(position).split("<td>\n            ")[1].split("        </td>")[0])

            # data for other columns
            data = page_soup.find_all("td", {"class": "zentriert"})  # loop step = 8
            # [0]-number [1]-dob [2]-nationality [3]-height [4]-foot [7]-contract

            # extract numbers
            for i in range(0, len(data), 8):
                Numbers.append(str(data[i]).split('nummer">')[1].split('</div')[0])

            # extract dob
            for i in range(1, len(data), 8):
                DatesOfBirth.append(str(data[i]).split('zentriert">')[1].split(' (')[0])

            # extract nationality
            for i in range(2, len(data), 8):
                countries = []
                for item in str(data[i]).split('alt="')[1:]:
                    countries.append(item.split('" class="flaggenrahmen"')[0])
                Nationalities.append(', '.join(countries))

            # extract height
            for i in range(3, len(data), 8):
                Heights.append(str(data[i]).split('zentriert">')[1].split('m</td')[0])

            # extract foot
            for i in range(4, len(data), 8):
                Feet.append(str(data[i]).split('zentriert">')[1].split('</td')[0])

            # extract contract
            for i in range(7, len(data), 8):
                Contracts.append(str(data[i]).split('zentriert">')[1].split('</td')[0])

            # transform DatesOfBirth, Contracts from "Apr 26, 1994" to "1994-04-26"
            month_dict = {
                'Jan': '01',
                'Feb': '02',
                'Mar': '03',
                'Apr': '04',
                'May': '05',
                'Jun': '06',
                'Jul': '07',
                'Aug': '08',
                'Sep': '09',
                'Oct': '10',
                'Nov': '11',
                'Dec': '12',
                '-': ''
            }

            for dob in DatesOfBirth:
                DatesOfBirth_Transformed.append(dob[-4:] + '.' + month_dict[dob[0:3]] + '.' + dob[4:6])

            for contract in Contracts:
                Contracts_Transformed.append(contract[-4:] + '.' + month_dict[contract[0:3]] + '.' + contract[4:6])

            final_table = pd.DataFrame({
                'number': Numbers,
                'name': FullNames,
                'position': Positions,
                'date_of_birth': DatesOfBirth_Transformed,
                'nationality': Nationalities,
                'height': Heights,
                'foot': Feet,
                'contract': Contracts_Transformed
            })
            table_name = url.split('.com/')[1].split('/')[0]
            final_table.to_csv(f'results/{table_name}.csv')
            #final_table.to_excel(f'results/{table_name}.xlsx')

        return final_table.head()

#SERIE_B

serie_b = [
    'https://www.transfermarkt.com/spezia-calcio/kader/verein/3522/saison_id/2023/plus/1',
'https://www.transfermarkt.com/parma-calcio-1913/kader/verein/130/saison_id/2023/plus/1',
'https://www.transfermarkt.com/us-cremonese/kader/verein/2239/saison_id/2023/plus/1',
'https://www.transfermarkt.com/uc-sampdoria/kader/verein/1038/saison_id/2023/plus/1',
'https://www.transfermarkt.com/pisa-sporting-club/kader/verein/4172/saison_id/2023/plus/1',
'https://www.transfermarkt.com/como-1907/kader/verein/1047/saison_id/2023/plus/1',
'https://www.transfermarkt.com/ssc-bari/kader/verein/332/saison_id/2023/plus/1',
'https://www.transfermarkt.com/modena-fc/kader/verein/1385/saison_id/2023/plus/1',
'https://www.transfermarkt.com/us-catanzaro/kader/verein/4097/saison_id/2023/plus/1',
'https://www.transfermarkt.com/fc-sudtirol/kader/verein/4554/saison_id/2023/plus/1',
'https://www.transfermarkt.com/ascoli-calcio/kader/verein/408/saison_id/2023/plus/1',
'https://www.transfermarkt.com/as-cittadella/kader/verein/4084/saison_id/2023/plus/1',
'https://www.transfermarkt.com/cosenza-calcio/kader/verein/4031/saison_id/2023/plus/1',
'https://www.transfermarkt.com/ternana-calcio/kader/verein/1103/saison_id/2023/plus/1',
'https://www.transfermarkt.com/ac-reggiana-1919/kader/verein/5621/saison_id/2023/plus/1',
'https://www.transfermarkt.com/feralpisalo/kader/verein/9439/saison_id/2023/plus/1',
'https://www.transfermarkt.com/calcio-lecco-1912/kader/verein/5514/saison_id/2023/plus/1']

new_parser = transfermarktTeamPlayers()
new_parser.parse(serie_b)