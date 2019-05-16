import csv
import re
from urllib import request
from bs4 import BeautifulSoup

class Rgx:
    def __init__(self, p, descricao):
        self.padrao = p
        self.descricao = descricao
        self.qnt = 0

        try: 
            x = re.compile(p)
            self.rgx = x
        except:
            pass

    def print(self):
        return "{} , {} ({})".format("\nExpressão regular: " + self.padrao, "\n" + self.descricao + "\nExpressãos encontradas: ", self.qnt)

# ================================================================

def executar(URL, paginas, u):    
    coll = []
    
    # Cria as RE
    with open('ListaExpressoes.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for r in spamreader:
            coll.append(Rgx(r[0], r[1]))
    
    
    # Cria o scraper 
    bs = BeautifulSoup(u, features="html.parser")
    
    nmr = 0 
    for l in bs.findAll('a'):
        if nmr > int(paginas): break
    
        # acessa os links da primeira url e passa pelas expressões
        l = l.get('href', None)
        if l is not None and l.startswith('http'):
            try:
                u = request.urlopen(l).read()
                nmr += 1
                
                for r in coll:
                    try:
                        for m in r.rgx.finditer(u.decode('utf-8')):
                            r.qnt += 1
                    except:
                        pass
                print("Buscando em: " + l + "\n");
            except:
                print("A pagina " + l + " possui bloqueio e foi ignorada\n");
                pass
    
    # print somente nas expressões que tiveram um ou mais matches
    for r in coll:
        if r.qnt > 0: print(r.print())
    
print ("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
print("                 Scrapper de expressões regulares");
print("                        BuscadorTop");
while True:
    URL = input("Digite o link a ser minerado: ");
    try:
        u = request.urlopen(URL).read()
    
        try:
            paginas = input("Digite quantidade de paginas a serem lidas: ");
            paginas = int(paginas);
            break;
        except:
            print("Apenas numeros inteiros");
    except:
        print("Digite um URL valido, exemplo: 'https://www.unoesc.edu.br'");
executar(URL, paginas, u);
print("                        BuscadorTop");
print("                 Scrapper de expressões regulares");
print ("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")