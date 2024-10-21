import json
from time import perf_counter
from types import NoneType

from bs4 import BeautifulSoup
import requests
from main import league_name


def league_link():
    link_90_minut = input("Podaj link do ligi: ")
    return link_90_minut

def scrap_league(link):
    try:
        with open("tabela.json", "r", encoding="utf-8") as input_file:
            tabela = json.load(input_file)

    except FileNotFoundError as e:
        tabela = {"Tabela": []}

    except json.decoder.JSONDecodeError as je:
        tabela = {"Tabela": []}

    #if len(tabela["Tabela"]) > 0:
    #   tabela["Tabela"].clear()



    url = requests.get(f"{link}") # Aklasa
    soup = BeautifulSoup(url.content, "html.parser")
    Nazwaligiszukana = soup.find_all("table", class_="main2")

    Nazwa_Ligi = ""
    for nazwa in Nazwaligiszukana:
        if not isinstance(nazwa.find("td", class_="main"), type(None)):
            Nazwa_Ligi = nazwa.find("td", class_="main").text.strip()



    for slowniki_z_nazwami_lig in tabela["Tabela"]:
        for k_z_nazwa_ligi in slowniki_z_nazwami_lig:
            if Nazwa_Ligi == k_z_nazwa_ligi:
                del tabela["Tabela"][tabela["Tabela"].index(slowniki_z_nazwami_lig)]
                #url = requests.get(f"{league_link()}")
                #soup = BeautifulSoup(url.content, "html.parser")
                Nazwaligiszukana = soup.find_all("table", class_="main2")
                for nazwa in Nazwaligiszukana:
                    if not isinstance(nazwa.find("td", class_="main"), type(None)) and nazwa.find("td", class_="main").text.strip() != k_z_nazwa_ligi :
                        Nazwa_Ligi = nazwa.find("td", class_="main").text.strip()


    p = soup.find_all("p")
    tablezterminarzem = soup.find_all("table", class_="main")




    daneztabeli = []
    calosc = []
    danecalewstringu = []
    test_lista = []

    for i in p:
        if not isinstance(i.find("table", {"class": "main2"}), type(None)):
            tabelacalosc = i.find_all("table", {"class": "main2"})
            daneztabeli.append(i.find_all("table", {"class": "main2"}))


    tabelabklasa = [[i.text for i in info.find_all("a", class_="main")] for info in daneztabeli[0]]



    for i in daneztabeli[0]:
        druzyny = [t.text.split() for t in i.find_all("td")]
        test1 = [druzyny.pop(druzyny.index(i)) for i in druzyny if i in [d.split(" ") for d in tabelabklasa[0]]]
        for f in druzyny:
            for s in f:
                danecalewstringu.append(s)

    kolejka_td = []

    for td in tablezterminarzem:
        kolejka_td.append(td.find("td"))
    b_szukane_kolejki = ""
    for b_kolejki in kolejka_td:
        if not isinstance(b_kolejki.find("b"), type(None)) and "Kolejka" in b_kolejki.find("b").text:
            b_szukane_kolejki += f"{b_kolejki.find("b").text},"

    # if len(tabelabklasa[0]) % 2 == 0:
    #     b_szukane_kolejki = b_szukane_kolejki.split(",")[0:(len(tabelabklasa[0]) - 1) * 2]
    # if len(tabelabklasa[0]) % 2 != 0:
    #     b_szukane_kolejki = b_szukane_kolejki.split(",")[0:len(tabelabklasa[0]) * 2]

    b_szukane_kolejki = b_szukane_kolejki.split(",")[:-1]
    terminarz_td = []
    data_tr = []


    for b_druzyn in tablezterminarzem:
        terminarz_td.append(b_druzyn.find_all("b"))
        data_tr.append(b_druzyn.find_all("tr"))

    caly_terminarz = []


    for data_td in data_tr:
        for td in data_td:
            caly_terminarz.append([td.text.replace("\n", "").replace("\xa0", "")])

    wszystkie_druzyny_stringu = ""
    for druzyna in tabelabklasa[0]:
        wszystkie_druzyny_stringu += f"{druzyna} "


    mecze_terminarz = []
    for i in caly_terminarz:
        for testi in i:
            for r in range(len(tabelabklasa[0])):
                if tabelabklasa[0][r] in testi and not "karnego" in testi:
                    mecze_terminarz.append(testi)
            if "Kolejka" in testi:
                mecze_terminarz.append(testi)
    indexy_kolejek = []

    for kolejki in mecze_terminarz:
        if not "Kolejka" in kolejki:
            mecze_terminarz.remove(kolejki)

    for i in b_szukane_kolejki:
        indexy_kolejek.append(mecze_terminarz.index(i))

    caly_terminarz_wliscie = []
    for r in range(1, len(indexy_kolejek) + 1):
        try:
            caly_terminarz_wliscie.append(mecze_terminarz[indexy_kolejek[r - 1] + 1: indexy_kolejek[r]])
        except IndexError:
            caly_terminarz_wliscie.append(mecze_terminarz[indexy_kolejek[r - 1] + 1:])


    frekwencja_do_usuniecia_w_liscie = []

    for i in caly_terminarz_wliscie:
        for testi1 in i:
            try:
                frekwencja_do_usuniecia_w_liscie.append(f'({testi1.split(",")[1].split("(")[1]}')
            except IndexError:
                pass
    terminarzwstringu = ""

    for i in mecze_terminarz:
        i = i.replace(",", "")
        terminarzwstringu += f"{i.strip(" ")}, "



    for r in range(len(frekwencja_do_usuniecia_w_liscie)):
        terminarzwstringu = terminarzwstringu.replace(frekwencja_do_usuniecia_w_liscie[r], "")

    terminarzwliscie2 = terminarzwstringu.split(",")



    claly_terminarz_liscie_bez_frekwencji = []

    for r in range(1, len(indexy_kolejek) + 1):
        try:
            claly_terminarz_liscie_bez_frekwencji.append(terminarzwliscie2[indexy_kolejek[r - 1] + 1: indexy_kolejek[r]])
        except IndexError:
            claly_terminarz_liscie_bez_frekwencji.append(terminarzwliscie2[indexy_kolejek[r - 1] + 1:])


    lol = {}

    for r in range(len(b_szukane_kolejki)):
        lol[b_szukane_kolejki[r]] = claly_terminarz_liscie_bez_frekwencji[r]




    tabela["Tabela"].append({f"{Nazwa_Ligi}": []})

    danecalewstringu[0:danecalewstringu.index('Nazwa')] = ""
    print(danecalewstringu)
    try:
        sezondruzyn = [danecalewstringu[danecalewstringu.index(f"{r + 1}."):danecalewstringu.index(f"{r + 1}.") + 15] for r in range(len(tabelabklasa[0]))]
    except ValueError as e:
        sezondruzyn = [danecalewstringu[danecalewstringu.index(f"{r + 1}."):danecalewstringu.index(f"{r + 1}.") + 15] for r in range(len(tabelabklasa[0]) - 1)]
        sezondruzyn.append(danecalewstringu[danecalewstringu.index(sezondruzyn[-1][-1]):danecalewstringu.index(sezondruzyn[-1][-1]) + 15])
        sezondruzyn[-1][0] = f"{len(sezondruzyn)}."
    goratabeli = danecalewstringu[:15]
    print(sezondruzyn)
    for r in range(len(sezondruzyn)):
        test_lista.append({
            "Pozycja": sezondruzyn[r][goratabeli.index('Nazwa')],
            "Nazwa": [i for i in tabelabklasa[0]][r],
            goratabeli[goratabeli.index('M.')]: sezondruzyn[r][goratabeli.index('M.')],
            goratabeli[goratabeli.index('Pkt.')]: sezondruzyn[r][goratabeli.index('Pkt.')],
            goratabeli[goratabeli.index('Z.')]: sezondruzyn[r][goratabeli.index('Z.')],
            goratabeli[goratabeli.index('R.')]: sezondruzyn[r][goratabeli.index('R.')],
            goratabeli[goratabeli.index('P.')]: sezondruzyn[r][goratabeli.index('P.')],
            goratabeli[goratabeli.index('Bramki')]: sezondruzyn[r][goratabeli.index('Bramki')],
            "Z.D.": sezondruzyn[r][goratabeli.index('Z.') + 4],
            "R.D.": sezondruzyn[r][goratabeli.index('R.') + 4],
            "P.D.": sezondruzyn[r][goratabeli.index('P.') + 4],
            "Bramki D.": sezondruzyn[r][goratabeli.index('Bramki') + 4],
            "Z.W.": sezondruzyn[r][goratabeli.index('Z.') + 8],
            "R.W.": sezondruzyn[r][goratabeli.index('R.') + 8],
            "P.W.": sezondruzyn[r][goratabeli.index('P.') + 8],
            "Bramki W.": sezondruzyn[r][goratabeli.index('Bramki') + 8],
        })
        tabela["Tabela"][-1][Nazwa_Ligi].append({"Pozycja": sezondruzyn[r][goratabeli.index('Nazwa')],
            "Nazwa": [i for i in tabelabklasa[0]][r],
            goratabeli[goratabeli.index('M.')]: sezondruzyn[r][goratabeli.index('M.')],
            goratabeli[goratabeli.index('Pkt.')]: sezondruzyn[r][goratabeli.index('Pkt.')],
            goratabeli[goratabeli.index('Z.')]: sezondruzyn[r][goratabeli.index('Z.')],
            goratabeli[goratabeli.index('R.')]: sezondruzyn[r][goratabeli.index('R.')],
            goratabeli[goratabeli.index('P.')]: sezondruzyn[r][goratabeli.index('P.')],
            goratabeli[goratabeli.index('Bramki')]: sezondruzyn[r][goratabeli.index('Bramki')],
            "Z.D.": sezondruzyn[r][goratabeli.index('Z.') + 4],
            "R.D.": sezondruzyn[r][goratabeli.index('R.') + 4],
            "P.D.": sezondruzyn[r][goratabeli.index('P.') + 4],
            "Bramki D.": sezondruzyn[r][goratabeli.index('Bramki') + 4],
            "Z.W.": sezondruzyn[r][goratabeli.index('Z.') + 8],
            "R.W.": sezondruzyn[r][goratabeli.index('R.') + 8],
            "P.W.": sezondruzyn[r][goratabeli.index('P.') + 8],
            "Bramki W.": sezondruzyn[r][goratabeli.index('Bramki') + 8]
                                })
    #print(test_lista)

    tabela["Tabela"][-1][Nazwa_Ligi].append({"Terminarz": {}})
    for r in range(len(b_szukane_kolejki)):
       tabela["Tabela"][-1][Nazwa_Ligi][-1]['Terminarz'][b_szukane_kolejki[r]] = claly_terminarz_liscie_bez_frekwencji[r]

    with open("tabela.json", "w", encoding="utf-8") as output_file:
         json.dump(tabela, output_file, ensure_ascii=False, indent=4)

skrapowanie = scrap_league(league_link())
#http://www.90minut.pl/liga/0/liga7461.html