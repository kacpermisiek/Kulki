import pygame
from pygame import gfxdraw
import numpy as np

#rozmiary okna gry oraz boiska
okno_szerokosc = 1400
okno_wysokosc = 800
boisko_szerokosc = 1050
boisko_wysokosc = 500
bramka_rozmiar = 150

#Ustawienia okna gry
pygame.init()
okno = pygame.display.set_mode((okno_szerokosc,okno_wysokosc))
pygame.display.set_caption("Kulki")

zegar = pygame.time.Clock()
uplynelo = 0

font = pygame.font.Font(None,50)

#Ilosc graczy w kazdej z druzyn
czerwoni_ilosc = 1
niebiescy_ilosc = 1

#Ustawienia rozgrywki
czerwoni_wynik=0
niebiescy_wynik =0

gracz_promien = 15
gracz_odbijanie = 0.5
gracz_masa = 0.5
gracz_tlumienie = 0.95
gracz_przyspieszenie = 0.1
gracz_przyspieszenie_kopniecie = 0.07
gracz_kopniecie_sila = 5

pilka_promien = 10
pilka_tlumienie = 0.99
pilka_masa = 1
pilka_odbijanie = 0.5

#Parametry startowe

czerwoni_start = (200,200)
niebiescy_start = (640,200)
pilka_start = (700,400)

slupek_promien = 8
slupek_odbicie = 0.5
slupek_grubosc = 2
bramka_linia_grubosc = 3

otoczka_promien = 15
otoczka_grubosc = 2

#Kolory
gracz_czerwony_kolor = (229, 110, 86)
gracz_niebieski_kolor = (86, 137, 229)
pilka_kolor = (0, 0, 0)
bramka_linia_kolor = (199, 230, 189)
slupek_kolor = (150, 150, 150)
boisko_kolor = (127, 162, 112)
tlo_kolor = (113, 140, 90)
otoczka_kolor = (255, 255, 255)
liniasrodkowa_kolor = (199, 230, 189)

#Linia srodkowa

liniasrodkowa_promien = 70
liniasrodowa_grubosc = 3

#Ustawienia tekstu

tekst_kolor =(0,0,0)
tekst_pozycja = (215,25)

# Ustawienia boiska
boisko_naroznikx = int(np.floor((okno_szerokosc - boisko_szerokosc) / 2))
boisko_narozniky = int(np.floor((okno_wysokosc - boisko_wysokosc) / 2))

bramka_narozniky = int(np.floor((okno_wysokosc - bramka_rozmiar) / 2))
y1 = boisko_naroznikx-30

z1 = boisko_naroznikx+boisko_szerokosc
z2 = bramka_narozniky

a1 = y1+2*pilka_promien
a2 = int(np.floor(bramka_narozniky - liniasrodowa_grubosc / 2))

b1 = z1
b2 = int(np.floor(bramka_narozniky - liniasrodowa_grubosc / 2))

#Pole poruszania sie zawodników
gracz_polex = [gracz_promien , okno_szerokosc - gracz_promien]
gracz_poley = [gracz_promien , okno_wysokosc - gracz_promien]

#Pole poruszania się piłki

pilka_polex = [boisko_naroznikx + pilka_promien , boisko_naroznikx + boisko_szerokosc - pilka_promien]
pilka_poley = [boisko_narozniky + pilka_promien , boisko_narozniky+boisko_wysokosc - pilka_promien]

#szerokosc bramki
bramka_y = [bramka_narozniky, bramka_narozniky+bramka_rozmiar]

#indeksowanie graczy
akutalny_indeks = -1

def get_indeks():
    global akutalny_indeks
    akutalny_indeks +=1
    return akutalny_indeks


#----------------KLASY OBIEKTOW---------------------



class Gracz(object):
    def __init__(self,x,y,kolor):
        #Domyslna pozycja gracza
        self.defx = x
        self.defy = y
        self.indeks = get_indeks()
        
        #Pozycja (wektor z floatami)
        self.poz = np.array([x,y]).astype(float)
        
        #Prędkosc i szybkosc
        self.predkosc = np.array([0,0])
        self.szybkosc = 0

        #Przyspieszenie
        self.przyspieszenie = np.array([0,0])
        self.przyspieszenie_skalar = gracz_przyspieszenie

        #Wlasciowsci gracza

        self.kolor = kolor
        self.kopniecie = False
        self.kopniecie_nowe = True
        self.odbijanie = gracz_odbijanie
        self.promien = gracz_promien
        self.masa = 1/gracz_masa

    def rysuj(self,okno):
        x = tuple(self.poz.astype(int))[0]
        y = tuple(self.poz.astype(int))[1]
        
        #jesli gracz wciska klawisz kopniecia, narysuj otoczke
        if self.kopniecie == True and self.kopniecie_nowe == True:
            pygame.gfxdraw.filled_circle(okno,x,y,otoczka_promien,otoczka_kolor)
            pygame.gfxdraw.aacircle(okno,x,y,otoczka_promien,otoczka_kolor)
        
        else:
            pygame.gfxdraw.filled_circle(okno, x, y,
                otoczka_promien, (0,0,0))
            pygame.gfxdraw.aacircle(okno, x, y,
                otoczka_promien, (0,0,0))
        
        pygame.gfxdraw.filled_circle(okno, x, y, gracz_promien-otoczka_grubosc, self.kolor)
        pygame.gfxdraw.aacircle(okno, x, y, gracz_promien-otoczka_grubosc, self.kolor)

    def reset(self):
        self.poz = np.array([self.defx,self.defy]).astype(float)

        self.predkosc = np.array([0,0])
        self.szybkosc = 0

        self.przyspieszenie = np.array([0,0])
        self.przyspieszenie_skalar = gracz_przyspieszenie

        self.kopniecie = False
        self.kopniecie_nowe = True

    def dystans(self,obj):
        return np.linalg.norm(obj.poz - self.poz)

    def kopniecie_kierunek(self,pilka):
        return (pilka.poz - self.poz) / self.dystans(pilka)

class pilka(object):
    def __init__(self,x,y):
        self.defx = x
        self.defy = y

        self.poz = np.array([x,y]).astype(float)

        self.predkosc = np.array([0.0,0.0])
        self.szybkosc = 0

        self.przyspieszenie = np.array([0.0,0.0])
        self.przyspieszenie_skalar = gracz_przyspieszenie

        self.odbijanie = pilka_odbijanie
        self.promien = pilka_promien
        self.masa = 1/pilka_masa

    def rysuj(self,okno):
        x = tuple(self.poz.astype(int))[0]
        y = tuple(self.poz.astype(int))[1]

        pygame.gfxdraw.filled_circle(okno, x, y, pilka_promien+2, (0, 0, 0))
        pygame.gfxdraw.aacircle(okno, x, y, pilka_promien+2, (0, 0, 0))
        pygame.gfxdraw.filled_circle(okno, x, y, pilka_promien, (255, 255, 255))
        pygame.gfxdraw.aacircle(okno, x, y, pilka_promien, (255, 255, 255))

    def reset (self):

        self.poz = np.array([self.defx,self.defy]).astype(float)

        self.predkosc = np.array([0,0])
        self.szybkosc = 0

        self.przyspieszenie = np.array([0,0])
        self.przyspieszenie_skalar = gracz_przyspieszenie

#klasa slupek - przyda sie do odbijania pilki o slupek
class slupek(object):
    def __init__(self,x,y):
        self.poz = np.array([x,y])
        self.odbijanie = slupek_odbicie
        self.predkosc = np.array([0.0,0.0])
        self.promien = slupek_promien

    def rysuj(self,okno):
        x = tuple(self.poz.astype(int))[0]
        y = tuple(self.poz.astype(int))[1]

        pygame.gfxdraw.filled_circle(okno, x, y, slupek_promien, (0, 0, 0))
        pygame.gfxdraw.aacircle(okno, x, y, slupek_promien, (0, 0, 0))
        pygame.gfxdraw.filled_circle(okno, x, y, slupek_promien-slupek_grubosc, slupek_kolor)
        pygame.gfxdraw.aacircle(okno, x, y, slupek_promien-slupek_grubosc, slupek_kolor)

 
#przyda sie klasa do blokowania zawodnikow niezaczynajacych gre
#class niezaczynajacy (object):


 # konwertowanie milisekund
def czas_format(ms):
    ss = (ms // 1000) % 60
    mm = (ms // 60000) % 60
    return mm, ss

def redraw_okno():#rysowanie elementow okna gry
    #ramka
    pygame.draw.rect(okno,tlo_kolor,(0,0,okno_szerokosc,okno_wysokosc))

    #boisko
    pygame.draw.rect(okno,boisko_kolor,(boisko_naroznikx,boisko_narozniky,boisko_szerokosc,boisko_wysokosc))
    pygame.draw.rect(okno,boisko_kolor,(boisko_naroznikx-30,bramka_narozniky,30,bramka_rozmiar))
    pygame.draw.rect(okno,boisko_kolor,(okno_szerokosc-boisko_naroznikx,bramka_narozniky,30,bramka_rozmiar))

    # linie
    pygame.draw.rect(okno, bramka_linia_kolor, (boisko_naroznikx - bramka_linia_grubosc // 2, boisko_narozniky - bramka_linia_grubosc // 2, bramka_linia_grubosc,boisko_wysokosc + bramka_linia_grubosc))
    pygame.draw.rect(okno, liniasrodkowa_kolor, (okno_szerokosc - boisko_naroznikx - bramka_linia_grubosc // 2, boisko_narozniky - bramka_linia_grubosc // 2, bramka_linia_grubosc,boisko_wysokosc + bramka_linia_grubosc))
    pygame.draw.rect(okno, liniasrodkowa_kolor, (boisko_naroznikx - bramka_linia_grubosc // 2, boisko_narozniky - bramka_linia_grubosc // 2, boisko_szerokosc + bramka_linia_grubosc,bramka_linia_grubosc))
    pygame.draw.rect(okno, bramka_linia_kolor, (boisko_naroznikx - bramka_linia_grubosc // 2, okno_wysokosc - boisko_narozniky - bramka_linia_grubosc // 2,boisko_szerokosc + bramka_linia_grubosc, bramka_linia_grubosc))


    # obiekty
    p.rysuj(okno)

    for obj in ruszajace:
        obj.rysuj(okno)

    for x in slupki:
        x.rysuj(okno)

    #pokazywanie wyniku
    string = str(czerwoni_wynik) + ":" + str(niebiescy_wynik)
    text = font.render(string,True,(255,255,255))
    okno.blit(text,(100,25))

    #pokazywanie czasu
    timetpl = czas_format(uplynelo)
    timestr = str(timetpl[0]).zfill(2)  + ":" + str(timetpl[1]).zfill(2)
    timetext = font.render(timestr,True,(255,255,255))
    okno.blit(timetext,(okno_szerokosc-150,25))




    pygame.display.update()


#--------------------MECHANKIKA GRY-----------------------


#trzeba dodac kolizje


#operacja kopania

def kopniecie(obj1,pilka):
    pilka.predkosc = np.array(pilka.predkosc) + gracz_kopniecie_sila * pilka_masa * obj1.kopniecie_kierunek(pilka)

# operacja zdobycia bramki

def gol(pilka,czerwoni_wynik,niebiescy_wynik,czerwoni_ostatnigol,kopniete):
    if pilka.poz[0] <= boisko_naroznikx:
        niebiescy_wynik += 1
        czerwoni_ostatnigol = False
        kopniete = False
        reset_mapy()
    elif pilka.poz[0] >= okno_szerokosc - boisko_naroznikx:
        czerwoni_wynik += 1
        czerwoni_ostatnigol = True
        kopniete = False
        reset_mapy()
    return [czerwoni_wynik,niebiescy_wynik,czerwoni_ostatnigol,kopniete]

#resetowanie mapy
def reset_mapy():
    for obj in ruszajace:
        obj.reset()
    kopniete = False

#Zatrzymywanie graczy w polu gry

def zatrzymaj_gracza(gracz):
    if gracz.poz[0] <= gracz_polex[0] or gracz.poz[0] >= gracz_polex[1]:
        gracz.predkosc[0] = 0
        if gracz.poz[0] <= gracz_polex[0]:
            gracz.poz[0] = gracz_polex[0]
        if gracz.poz[0] >= gracz_polex[1]:
            gracz.poz[0] = gracz_polex[1]
    if gracz.poz[1] <= gracz_poley[0] or gracz.poz[1] >= gracz_poley[1]:
        gracz.predkosc[1] = 0
        if gracz.poz[1] <= gracz_poley[0]:
            gracz.poz[1] = gracz_poley[0]
        if gracz.poz[1] >= gracz_poley[1]:
            gracz.poz[1] = gracz_poley[1]


#Zatrzymywanie pilki w polu gry

def zatrzymaj_pilke(pilka):
    if pilka.poz[0] <= pilka_polex[0] or pilka.poz[0] >= pilka_polex[1]:
        if pilka.poz[1] >= bramka_y[0] and pilka.poz[1] <= bramka_y[1]:
            pass
        else:
            pilka.predkosc[0] = - 0.5 * pilka.predkosc[0]
            if pilka.poz[0] <= pilka_polex[0]:
                pilka.poz[0] = pilka_polex[0] + (pilka_polex[0] - pilka.poz[0]) / 2

            if pilka.poz[0] >= pilka_polex[1]:
                pilka.poz[0] = pilka_polex[1] + (pilka_polex[1] - pilka.poz[0]) / 2
    if pilka.poz[1] <= pilka_poley[0] or p.poz[1] >= pilka_poley[1]:
        pilka.predkosc[1] = - 0.5 * p.predkosc[1]
        if pilka.poz[1] <= pilka_poley[0]:
            pilka.poz[1] = pilka_poley[0] + (pilka_poley[0] - pilka.poz[1]) / 2
        if pilka.poz[1] >= pilka_poley[1]:
            pilka.poz[1] = pilka_poley[1] + (pilka_poley[1] - pilka.poz[1]) / 2

#Gracze ktorzy nie wznawiaja gry, nie moga przekroczyc linii polowy
#def zatrzymaj_niezaczynajacych(zblokowany):

#--------------------------inicjalizacja graczy -------------------------------------------


czerwoni = []
niebiescy= []

for i in range (czerwoni_ilosc):
    czerwoni.append(Gracz(czerwoni_start[0] + 0 * np.random.uniform(-1, 1), czerwoni_start[1] + 0 * np.random.uniform(-1, 1), gracz_czerwony_kolor))


for i in range(niebiescy_ilosc):
    niebiescy.append(Gracz(niebiescy_start[0] + 0 * np.random.uniform(-1, 1), niebiescy_start[1] + 0 * np.random.uniform(-1, 1), gracz_niebieski_kolor))



p = pilka(pilka_start[0],pilka_start[1])


slupek_czerwony1 = slupek(boisko_naroznikx,bramka_narozniky)
slupek_czerwony2 = slupek(boisko_naroznikx,bramka_narozniky+bramka_rozmiar)
slupek_niebieski1 = slupek(okno_szerokosc-boisko_naroznikx,bramka_narozniky)
slupek_niebieski2 = slupek(okno_szerokosc-boisko_naroznikx,bramka_narozniky+bramka_rozmiar)



gracze = czerwoni + niebiescy

ruszajace = gracze + [p]

slupki = [slupek_czerwony1,slupek_czerwony2,slupek_niebieski1,slupek_niebieski2]

kopniete = True
czerwoni_ostatnigol = False

run = True

while run:
    uplynelo += zegar.tick(60)
    
    #obsluga klawiszy
    klawisz = pygame.key.get_pressed()

    #gracz R1
    if klawisz[pygame.K_a]:
        if klawisz[pygame.K_w]:
            czerwoni[0].przyspieszenie = np.array([-1.0, -1.0]) / (2) ** (1 / 2)
        elif klawisz[pygame.K_s]:
            czerwoni[0].przyspieszenie = np.array([-1.0, 1.0]) / (2) ** (1 / 2)
        else:
            czerwoni[0].przyspieszenie = np.array([-1.0, 0.0])

    elif klawisz[pygame.K_d]:
        if klawisz[pygame.K_w]:
            czerwoni[0].przyspieszenie = np.array([1.0, -1.0]) / (2) ** (1 / 2)
        elif klawisz[pygame.K_s]:
            czerwoni[0].przyspieszenie = np.array([1.0, 1.0]) / (2) ** (1 / 2)
        else:
            czerwoni[0].przyspieszenie = np.array([1.0, 0.0])

    elif klawisz[pygame.K_w]:
        czerwoni[0].przyspieszenie = np.array([0.0, -1.0])

    elif klawisz[pygame.K_s]:
        czerwoni[0].przyspieszenie = np.array([0.0, 1.0])

    else:
        czerwoni[0].przyspieszenie = np.array([0.0, 0.0])

    if klawisz[pygame.K_v]:
        czerwoni[0].kopniecie = True
    else:
        czerwoni[0].kopniecie = False
        czerwoni[0].kopniecie_nowe = True

    #gracz B1
    if klawisz[pygame.K_LEFT]:
        if klawisz[pygame.K_UP]:
            niebiescy[0].przyspieszenie = np.array([- 1.0, - 1.0]) / (2) ** (1 / 2)
        elif klawisz[pygame.K_DOWN]:
            niebiescy[0].przyspieszenie = np.array([- 1.0, 1.0]) / (2) ** (1 / 2)
        else:
            niebiescy[0].przyspieszenie = np.array([- 1.0, 0.0])

    elif klawisz[pygame.K_RIGHT]:
        if klawisz[pygame.K_UP]:
            niebiescy[0].przyspieszenie = np.array([1.0, - 1.0]) / (2) ** (1 / 2)
        elif klawisz[pygame.K_DOWN]:
            niebiescy[0].przyspieszenie = np.array([1.0, 1.0]) / (2) ** (1 / 2)
        else:
            niebiescy[0].przyspieszenie = np.array([1.0, 0.0])

    elif klawisz[pygame.K_UP]:
        niebiescy[0].przyspieszenie = np.array([0.0, -1.0])

    elif klawisz[pygame.K_DOWN]:
        niebiescy[0].przyspieszenie = np.array([0.0, 1.0])

    else:
        niebiescy[0].przyspieszenie = np.array([0.0, 0.0])

    if klawisz[pygame.K_RCTRL]:
        niebiescy[0].kopniecie = True
    else:
        niebiescy[0].kopniecie = False
        niebiescy[0].kopniecie_nowe = True

    # ruch graczy
    for i in gracze:
        if i.kopniecie == True and i.kopniecie_nowe == True:
            i.predkosc = np.array(i.predkosc) + i.przyspieszenie * gracz_przyspieszenie_kopniecie
        else:
            i.predkosc = np.array(i.predkosc) + i.przyspieszenie * i.przyspieszenie_skalar

        i.predkosc = i.predkosc * gracz_tlumienie
        i.poz += i.predkosc

    # ruch pilki
    p.predkosc = np.array(p.predkosc) * pilka_tlumienie
    p.poz += p.predkosc


    for i in gracze:
        zatrzymaj_gracza(i)

    zatrzymaj_pilke(p)



    # kopniecia
    for i in gracze:
        if i.dystans(p) <= gracz_promien + pilka_promien + 4:

            kopniete = True

            if i.kopniecie == True and i.kopniecie_nowe == True:
                kopniecie(i, p)
                i.kopniecie_nowe = False
            elif i.kopniecie == False:
                i.kopniecie_nowe = True

    #wynik
    print(uplynelo)
    G = gol(p, czerwoni_wynik, niebiescy_wynik, czerwoni_ostatnigol, kopniete)
    czerwoni_wynik = G[0]
    niebiescy_wynik = G[1]
    czerwoni_ostatnigol = G[2]
    kopniete = G[3]
    redraw_okno()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
