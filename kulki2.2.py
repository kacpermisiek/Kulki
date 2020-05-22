import pygame
from pygame import gfxdraw
import numpy as np

#rozmiary okna gry oraz boiska
okno_szerokosc = 1400
okno_wysokosc = 800
boisko_szerokosc = 1000
boisko_wysokosc = 500
bramka_rozmiar = 150

#Ustawienia okna gry
pygame.init()
okno = pygame.display.set_mode((okno_szerokosc,okno_wysokosc))
pygame.display.set_caption("kulki")

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
pilka_tlumienie = 0.985
pilka_masa = 1
pilka_odbijanie = 0.5

#Parametry startowe

czerwoni_start = (700 - 200,400)
niebiescy_start = (700 + 200,400)
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
        
        #jesli gracz wciska klawisz kopniecia i nie kopie pilki, narysuj otoczke
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

 
# obiekt do blokowania zawodnikow niezaczynajacych gre
class niezaczynajacy(object):

    def __init__(self):
        self.poz = np.array([pilka_start[0], pilka_start[1]]) #polozenie pilki na poczatku
        self.promien = liniasrodkowa_promien #promien okregu 
        self.odbijanie = 0
        self.predkosc = [0, 0]


#---------------------------GRAFIKA------------------------------


#Menu

def menu():
    button1 = pygame.Rect(int(okno_szerokosc/3), int(okno_wysokosc/3), 200, 100)
    button2 = pygame.Rect(int(okno_szerokosc/3), int(okno_wysokosc/3)+370, 200, 100)
    button3 = pygame.Rect(int(okno_szerokosc/3), int(okno_wysokosc/3)+170, 200,100)

    tytul_tekst = font.render("KULKI - TURBO GIERKA",True,(255,255,255))
    graj_tekst = font.render("Graj",True,(60,60,60))
    wylacz_tekst = font.render("Wylacz gre",True,(60,60,60))
    instrukcje_tekst = font.render("Instrukcja", True,(60,60,60))


    run2 = True

    while run2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run2 = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                myszka_pozcyja = event.pos

                if button1.collidepoint(myszka_pozcyja):
                    global run
                    run = True
                    return 0
                if button2.collidepoint(myszka_pozcyja):
                    run2 = False
                    pygame.quit()
                    return 0
                if button3.collidepoint(myszka_pozcyja):
                    run2 = False
                    run3 = True
                    menu2()
                    return 0
        
        okno.fill(boisko_kolor)

        pygame.draw.rect(okno, [224,216,215],button1)
        pygame.draw.rect(okno, [224,216,215],button2)
        pygame.draw.rect(okno, [224,216,215],button3)

        okno.blit(tytul_tekst,(int(okno_szerokosc/3), 50))
        okno.blit(graj_tekst,(int(okno_szerokosc/3+50), int(okno_wysokosc/3+30)))
        okno.blit(wylacz_tekst,(int(okno_szerokosc/3)+10, int(okno_wysokosc/3)+400))
        okno.blit(instrukcje_tekst,(int(okno_szerokosc/3)+10, int(okno_wysokosc/3)+200))

        pygame.display.update()
        zegar.tick(60)

    

def menu2():
    run3 = True
    
    button1 = pygame.Rect(int(okno_szerokosc/3), int(okno_wysokosc/3), 200, 100)


    tytul_tekst = font.render("KULKI - TURBO GIERKA",True,(255,255,255))
    graj_tekst = font.render("Powrot",True,(60,60,60))

    instrukcja1 = "Czerwony: sterowanie WASD, kopniecie: V"
    instrukcja2 = "Niebieski: sterowanie: strzalki, kopniecie: RCTRL"
    instrukcja3 = "limit czasowy: 90s - wygrywa ten kto zdobedzie wiecej goli"

    instrukcja1_tekst = font.render(instrukcja1,True,(60,60,60))
    instrukcja2_tekst = font.render(instrukcja2,True,(60,60,60))
    instrukcja3_tekst = font.render(instrukcja3,True,(60,60,60))
    


    while run3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run2 = False
                run3 = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                myszka_pozcyja = event.pos

                if button1.collidepoint(myszka_pozcyja):
                    run = False
                    run2 = True
                    run3 = False
                    menu()
                    return 0


        
        okno.fill(boisko_kolor)

        pygame.draw.rect(okno, [224,216,215],button1)

        okno.blit(tytul_tekst,(int(okno_szerokosc/3), 50))
        okno.blit(graj_tekst,(int(okno_szerokosc/3+50), int(okno_wysokosc/3+30)))
        okno.blit(instrukcja1_tekst, (200,500))
        okno.blit(instrukcja2_tekst, (200,600))
        okno.blit(instrukcja3_tekst, (200,700))


        pygame.display.update()
        zegar.tick(60)


 # konwertowanie milisekund
def czas_format(ms):
    ss = (ms // 1000)
    return ss

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


    #srodkowy okrag
    pygame.gfxdraw.filled_circle(okno, pilka_start[0], pilka_start[1], liniasrodkowa_promien, liniasrodkowa_kolor)
    pygame.gfxdraw.aacircle(okno, pilka_start[0], pilka_start[1], liniasrodkowa_promien, liniasrodkowa_kolor)

    pygame.gfxdraw.filled_circle(okno, pilka_start[0], pilka_start[1],liniasrodkowa_promien-liniasrodowa_grubosc, boisko_kolor)
    pygame.gfxdraw.aacircle(okno, pilka_start[0], pilka_start[1],liniasrodkowa_promien-liniasrodowa_grubosc, boisko_kolor)

    pygame.draw.rect(okno, liniasrodkowa_kolor,(okno_szerokosc // 2 - liniasrodowa_grubosc // 2, boisko_narozniky, liniasrodowa_grubosc, boisko_wysokosc))




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
    timestr = str(timetpl).zfill(2)
    timetext = font.render(timestr,True,(255,255,255))
    okno.blit(timetext,(okno_szerokosc-150,25))


    #Komunikat o koncu gry
    if timetpl > 90:
        if czerwoni_wynik > niebiescy_wynik:
            text = font.render("Czerwoni wygrali!", True, (255, 255, 255))
            coord = text.get_rect(center = (windowwidth // 2, windowheight // 2))
            win.blit(text, coord)
            global run
            run = False
        elif niebiescy_wynik > czerwoni_wynik:
            text = font.render("Niebiescy wygrali!", True, (255, 255, 255))
        else:
            text = font.render("Remis", True, (255, 255, 255))
            

        coord = text.get_rect(center = (okno_szerokosc // 2, okno_wysokosc // 2))
        okno.blit(text, coord)
        
    #Przycisk zakonczenia gry
    
    pygame.draw.rect(okno, [224,216,215],button01)
    zakoncz = font.render("Zakoncz gre",True,(60,60,60))
    okno.blit(zakoncz,(okno_szerokosc-290, okno_wysokosc-70))



    pygame.display.update()

#--------------------MECHANKIKA GRY-----------------------

#kolizja obiektow poruszajacych sie
def kolizja(obj1, obj2):
    kierunek = (obj1.poz - obj2.poz)
    dystans = (np.linalg.norm(kierunek))
    odbicie = obj1.odbijanie * obj2.odbijanie
    srodek_masy = (obj1.poz * obj1.masa + obj2.poz * obj2.masa) / (obj1.masa + obj2.masa)

    # calculates normal and tangent vectors
    kolizja_normal = kierunek / dystans
    kolizja_styczna = np.array([kierunek[1], - kierunek[0]]) / (np.linalg.norm(kierunek))

    # updates object components
    obj1_predkosc_normalna = np.dot(np.array(obj1.predkosc), kolizja_normal)
    obj2_predkosc_normalna = np.dot(np.array(obj2.predkosc), kolizja_normal)

    # inelastic collision formula
    obj1_predkosc_normalna2 = (odbicie * obj2.masa * (obj2_predkosc_normalna - obj1_predkosc_normalna) + obj1.masa * obj1_predkosc_normalna + obj2.masa * obj2_predkosc_normalna) / (obj1.masa + obj2.masa)
    obj2_predkosc_normalna2 = (odbicie * obj1.masa * (obj1_predkosc_normalna - obj2_predkosc_normalna) + obj2.masa * obj2_predkosc_normalna + obj1.masa * obj1_predkosc_normalna) / (obj2.masa + obj1.masa)
    obj1_predkosc_styczna = np.dot(np.array(obj1.predkosc), kolizja_styczna)
    obj2_predkosc_styczna = np.dot(np.array(obj2.predkosc), kolizja_styczna)

    obj1.predkosc = obj1_predkosc_normalna2 * np.array(kolizja_normal) + obj1_predkosc_styczna * np.array(kolizja_styczna)
    obj2.predkosc = obj2_predkosc_normalna2 * np.array(kolizja_normal) + obj2_predkosc_styczna * np.array(kolizja_styczna)

    obj1.poz = srodek_masy + ((obj1.promien + obj2.promien) + odbicie * (obj1.promien + obj2.promien - dystans)) * kolizja_normal * obj2.masa / (obj1.masa + obj2.masa)
    obj2.poz = srodek_masy - ((obj1.promien + obj2.promien) + odbicie * (obj1.promien + obj2.promien - dystans)) * kolizja_normal * obj1.masa / (obj1.masa + obj2.masa)


#kolizja obiekt poruszajacy sie - slupek

def kolizja_slupek(obj1,obj2):
    kierunek = (obj1.poz - obj2.poz)
    dystans = (np.linalg.norm(kierunek))
    odbicie = obj1.odbijanie * obj2.odbijanie


    #normalny i styczny wektor
    kolizja_normal = kierunek / dystans
    kolizja_styczna = np.array([kierunek[1], - kierunek[0]]) / (np.linalg.norm(kierunek))


    #komponenty obiektow

    obj1_normalnapredkosc = np.dot(np.array(obj1.predkosc), kolizja_normal)
    obj2_normalnapredkosc = np.dot(np.array(obj2.predkosc), kolizja_normal)
    predkosc_after = (obj1_normalnapredkosc + obj2_normalnapredkosc) * odbicie * 2

    obj1_stycznapredkosc = np.dot(np.array(obj1.predkosc),kolizja_styczna)
    obj2_stycznapredkosc = np.dot(np.array(obj2.predkosc),kolizja_styczna)

    obj1.predkosc = -predkosc_after * np.array(kolizja_normal) + obj1_stycznapredkosc * np.array(kolizja_styczna)
    obj2.predkosc = predkosc_after *np.array(kolizja_normal) + obj2_stycznapredkosc * np.array(kolizja_styczna)

    obj2.poz = obj1.poz - kolizja_normal * (obj1.promien + obj2.promien)



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

def zatrzymaj_niezaczynajacych(zblokowany):
    wektor = np.array([srodek_blok.poz[0] - zblokowany.poz[0], srodek_blok.poz[1] - zblokowany.poz[1]])
    dystans = np.linalg.norm(wektor)
    if dystans <= srodek_blok.promien + zblokowany.promien:
        zblokowany.poz[0] = srodek_blok.poz[0] - wektor[0] / np.linalg.norm(wektor)
        zblokowany.poz[1] = srodek_blok.poz[1] - wektor[1] / np.linalg.norm(wektor)
        kolizja_slupek(srodek_blok, zblokowany)
        srodek_blok.poz[0] = int(srodek_blok.poz[0])
        srodek_blok.poz[1] = int(srodek_blok.poz[1])


#--------------------------inicjalizacja graczy -------------------------------------------

button01 = pygame.Rect(int(okno_szerokosc-300), int(okno_wysokosc-100), 250, 100)

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

srodek_blok = niezaczynajacy()

gracze = czerwoni + niebiescy

ruszajace = gracze + [p]

slupki = [slupek_czerwony1,slupek_czerwony2,slupek_niebieski1,slupek_niebieski2]

kopniete = False
czerwoni_ostatnigol = False


run3 = False #menu instrukcje
run2 = True #menu
run = False #gra

menu()


while run:
    uplynelo += zegar.tick(60)

    #blokada niezaczynajacych od wchodzenia do okregu i drugiej polowy
    if kopniete == False:
        if czerwoni_ostatnigol == True:
            for i in range(len(czerwoni)):

                if czerwoni[i].poz[0] >= okno_szerokosc // 2 - gracz_promien:
                    czerwoni[i].predkosc[0] = 0
                    czerwoni[i].poz[0] = okno_szerokosc // 2 - gracz_promien

                    zatrzymaj_niezaczynajacych(czerwoni[i])
        else:
            for i in range(len(niebiescy)):

                if niebiescy[i].poz[0] <= okno_szerokosc // 2 + gracz_promien:
                    niebiescy[i].predkosc[0] = 0
                    niebiescy[i].poz[0] = okno_szerokosc // 2 + gracz_promien

                zatrzymaj_niezaczynajacych(niebiescy[i])

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

    #kolizje gracz-pilka
    for i in gracze:
        if i.dystans(p) <= gracz_promien + pilka_promien:
            kolizja(i,p)

        # kolizje obiekty poruszajace sie - slupki
    for i in ruszajace:
        for slupek in slupki:
            wektor = slupek.poz - i.poz
            dystans = np.linalg.norm(wektor)
            if dystans <= slupek_promien + i.promien:
                i.poz = slupek.poz - wektor / np.linalg.norm(wektor)
                kolizja_slupek(slupek, i)

    # kolizje gracz-gracz
    for i in range(len(gracze)):
        for j in range(i + 1, len(gracze)):
            dystans = gracze[i].dystans(gracze[j])
            if gracze[i].indeks != gracze[j].indeks and dystans <= 2 * gracz_promien:
                kolizja(gracze[i], gracze[j])


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
    
    G = gol(p, czerwoni_wynik, niebiescy_wynik, czerwoni_ostatnigol, kopniete)
    czerwoni_wynik = G[0]
    niebiescy_wynik = G[1]
    czerwoni_ostatnigol = G[2]
    kopniete = G[3]
    redraw_okno()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                myszka_pozcyja = event.pos

                if button01.collidepoint(myszka_pozcyja):
                    run = False
                    run2 = True
                    czerwoni_wynik=0
                    niebiescy_wynik =0
                    uplynelo=0
                    menu()












