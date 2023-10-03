import pandas as pd
from bs4 import BeautifulSoup
import requests

class transfermarktTeamPlayers():
    def __init__(self, name):
        self.name = name

    def parse(self, url_list):
        for url in url_list:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
            }
            page_tree = requests.get(url, headers=headers)
            if page_tree.status_code != 200:
                return f"Request failed. Status: {page_tree.status_code}"
            else:
                page_soup = BeautifulSoup(page_tree.content, 'html.parser')

                # extract player names
                Players = page_soup.find_all("img", {"class": "bilderrahmen-fixed lazy lazy"})
                FullNames = [str(Players[i]).split('" class', 1)[0].split('<img alt="', 1)[1] for i in
                             range(0, len(Players))]

                # extract positions
                PositionList = page_soup.find_all("table", {"class": "inline-table"})
                Positions = [PositionList[i].find_all("td")[2].text.strip() for i in range(len(PositionList))]

                # data for other columns
                data = page_soup.find_all("td", {"class": "zentriert"})  # loop step = 8
                # [0]-number [1]-dob [2]-nationality [3]-height [4]-foot [7]-contract

                #extract data for numbers, dob, nationality, foot, contract yo lists
                res = [data[i].find("div") for i in range(len(data))]
                Numbers = [i.text for i in res if i]
                DatesOfBirth = [data[i].text.split(' (')[0] for i in range(1, len(data), 8)]
                Nationalities = []
                for i in range(2, len(data), 8):
                    countries = []
                    for item in str(data[i]).split('alt="')[1:]:
                        countries.append(item.split('" class="flaggenrahmen"')[0])
                    Nationalities.append(', '.join(countries))
                Heights = [data[i].text for i in range(3, len(data), 8)]
                Feet = [data[i].text for i in range(4, len(data), 8)]
                Contracts = [data[i].text for i in range(7, len(data), 8)]

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
                DatesOfBirth_Transformed = []
                for dob in DatesOfBirth:
                    if dob != '-</td>':
                        DatesOfBirth_Transformed.append(dob[-4:] + '.' + month_dict[dob[0:3]] + '.' + dob[4:6])
                    else:
                        DatesOfBirth_Transformed.append('-')

                Contracts_Transformed = [(c[-4:]+'.'+month_dict[c[0:3]]+'.'+c[4:6]) for c in Contracts]

                #to dataframe
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

                #write to file
                table_name = url.split('.com/')[1].split('/')[0]
                #final_table.to_csv(f'results/{table_name}.csv')
                final_table.to_excel(f'results/{table_name}.xlsx')

premier_league = [
    'https://www.transfermarkt.com/arsenal-fc/kader/verein/11/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/aston-villa/kader/verein/405/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/afc-bournemouth/kader/verein/989/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/brentford-fc/kader/verein/1148/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/burnley-fc/kader/verein/1132/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/brighton-amp-hove-albion/kader/verein/1237/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/chelsea-fc/kader/verein/631/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/crystal-palace/kader/verein/873/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/everton-fc/kader/verein/29/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/fulham-fc/kader/verein/931/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/liverpool-fc/kader/verein/31/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/luton-town/kader/verein/1031/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/manchester-city/kader/verein/281/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/manchester-united/kader/verein/985/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/newcastle-united/kader/verein/762/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/nottingham-forest/kader/verein/703/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/sheffield-united/kader/verein/350/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/tottenham-hotspur/kader/verein/148/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/west-ham-united/kader/verein/379/saison_id/2023/plus/1',
    'https://www.transfermarkt.com/wolverhampton-wanderers/kader/verein/543/saison_id/2023/plus/1'
]

a = transfermarktTeamPlayers("new_parser")

a.parse(premier_league)
