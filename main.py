import json
from bs4 import BeautifulSoup
import requests


with open("tabela.json", "r", encoding="utf-8") as input_file:
   tabela = json.load(input_file)

if len(tabela["tabela"]) > 0:
   tabela["tabela"].clear()

url = requests.get("http://www.90minut.pl/liga/1/liga13484.html")
soup = BeautifulSoup(url.content, "html.parser")
p = soup.find_all("p")
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



danecalewstringu[0:danecalewstringu.index('Nazwa')] = ""
sezondruzyn = [danecalewstringu[danecalewstringu.index(f"{r + 1}."):danecalewstringu.index(f"{r + 1}.") + 15] for r in range(len(tabelabklasa[0]))]
goratabeli = danecalewstringu[:15]

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
    tabela["tabela"].append({"Pozycja": sezondruzyn[r][goratabeli.index('Nazwa')],
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
print(test_lista)




with open("tabela.json", "w", encoding="utf-8") as output_file:
    json.dump(tabela, output_file, ensure_ascii=False, indent=4)
