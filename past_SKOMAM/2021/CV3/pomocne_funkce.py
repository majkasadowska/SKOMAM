#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def nova_animace(pozice, stav, pocet_lidi, delka_simulace):
    #jednoduchý způsob jak najednou vyrobit figure včetně os
    figure_animace, axs = plt.subplots(ncols=2,figsize=(9.5,4)) # vyrobíme dvoje osy - simulace/časový vývoj
    # zobrazení simolace (tečky repr. lidi)
    ln1, = axs[0].plot(pozice[stav == 'S',0],pozice[stav == 'S',1],"bo",markersize=2) #graf do konkrétních os (axs)
    ln2, = axs[0].plot(pozice[stav == 'I',0],pozice[stav == 'I',1],"ro",markersize=2)
    ln3, = axs[0].plot(pozice[stav == 'R',0],pozice[stav == 'R',1],"go",markersize=2)
    ln4, = axs[0].plot(pozice[stav == 'Q',0],pozice[stav == 'Q',1],"ko",markersize=2)

    #text v pravo dolů relativně vůči osám, typ textu monospaced
    title = axs[0].text(1,0, "text",transform=axs[0].transAxes, ha="right", va="bottom", fontfamily='monospace')
    title2 = axs[1].text(1,0.5, "R = 0",transform=axs[1].transAxes, ha="right", va="bottom", fontfamily='monospace')

    axs[0].set_xlim(-0.5, 1.5) # rozmesí osy X
    axs[0].set_ylim(-0.5, 1.5) # rozmesí osy Y

    akt_nakazenych = (stav == 'I').sum()
    akt_nakazitelnych = (stav == 'S').sum()
    akt_odstranenych = (stav == 'R').sum()
    akt_v_karantene = (stav == 'Q').sum()

    # zobrazení časového vývoje - grafy poču lidí v jednotlivých skupinách
    ln5, = axs[1].plot(0, akt_v_karantene,"k-")
    ln6, = axs[1].plot(0, akt_odstranenych,"g-")
    ln7, = axs[1].plot(0, akt_nakazitelnych,"b-")
    ln8, = axs[1].plot(0, akt_nakazenych,"r-")

    axs[1].set_xlim(0, delka_simulace/60/24) # rozmesí osy X
    axs[1].set_ylim(-pocet_lidi*0.01, pocet_lidi*1.01) # rozmesí osy Y

    return figure_animace, (ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, title, title2) # musíme vrátit, aby byly dostupné v gl.


def vykresleni(cas_simulace_minuty, pozice, stav, komponenty_grafu, R0=0):
    ln1 = komponenty_grafu[0] # rozbalíme si všechny komponenty z výsledného touple
    ln2 = komponenty_grafu[1] # toto děláme především kvůli přehlednosti následujícího kódu
    ln3 = komponenty_grafu[2] # pzn. ln1,... jsou pouze ukazatele na objekty, změny v nich změní původní data
    ln4 = komponenty_grafu[3]
    ln5 = komponenty_grafu[4]
    ln6 = komponenty_grafu[5]
    ln7 = komponenty_grafu[6]
    ln8 = komponenty_grafu[7]
    title = komponenty_grafu[8]
    title2 = komponenty_grafu[9]

    cas_simulace_hodiny = np.mod(cas_simulace_minuty/60,24) #napočítáme aktuální čas
    cas_simulace_dny = np.floor(cas_simulace_minuty/24/60)

    akt_nakazenych = (stav == 'I').sum()
    akt_nakazitelnych = (stav == 'S').sum()
    akt_odstranenych = (stav == 'R').sum()
    akt_v_karantene = (stav == 'Q').sum()

    # nyní aktualizujeme data objektů (čáry/body v grafu a text) - změny souřadnic a textu
    ln1.set_xdata(pozice[stav == 'S',0]) # nastavíme nové souřadnice x
    ln1.set_ydata(pozice[stav == 'S',1]) # nastavíme nové souřadnice y
    ln2.set_xdata(pozice[stav == 'I',0])
    ln2.set_ydata(pozice[stav == 'I',1])
    ln3.set_xdata(pozice[stav == 'R',0])
    ln3.set_ydata(pozice[stav == 'R',1])
    ln4.set_xdata(pozice[stav == 'Q',0])
    ln4.set_ydata(pozice[stav == 'Q',1])
    # pro zápis aktuálního času provedeme následující, funkce format dá na místo {:2.0f} a {:4.1f} čísla v param.
    title.set_text("Time: {:2.0f}d {:4.1f}h".format(cas_simulace_dny,cas_simulace_hodiny)) #nastavíme nový text
    if R0 > -1: # aby toto číslo nebylo takové skákající, budeme ho vyhlazovat (pozn není to úplně přesné, ale to nevadí)
        old_R0 = float(title2.get_text()[4:])
        title2.set_text("R = {:4.1f}".format(R0 * 0.25 + old_R0 * 0.75)) #nastavíme nový text
    # u druhého grafu použijeme předchozí data jako paměť, proto pokaždé akorát přilepíme (append) novou hodnotu
    ln5.set_xdata(np.append(ln5.get_xdata(), cas_simulace_minuty/60/24)) # nastavíme nové souřadnice x
    ln5.set_ydata(np.append(ln5.get_ydata(), akt_v_karantene)) # nast. s. y
    ln6.set_xdata(np.append(ln6.get_xdata(), cas_simulace_minuty/60/24))
    ln6.set_ydata(np.append(ln6.get_ydata(), akt_odstranenych))
    ln7.set_xdata(np.append(ln7.get_xdata(), cas_simulace_minuty/60/24))
    ln7.set_ydata(np.append(ln7.get_ydata(), akt_nakazitelnych))
    ln8.set_xdata(np.append(ln8.get_xdata(), cas_simulace_minuty/60/24))
    ln8.set_ydata(np.append(ln8.get_ydata(), akt_nakazenych))
    return # nemusíme nic vracet, všechno jsou objeky v globální paměti, které pouze upravujeme


def nove_nakazeni(pozice, stav, vzdalenost_nakazy, pravdepodobnost_nakazy):
    pI1 = pozice[stav == 'I',0]; pI2 = pozice[stav == 'I',1]; # vybereme si x a y pozice všech nakažených
    pS1 = pozice[stav == 'S',0]; pS2 = pozice[stav == 'S',1]; # vybereme si x a y pozice všech nakazitelných
    pS1 = pS1[None]; pS2 = pS2[None]; # původní pole pS1 a pS2 byly 1d a my budeme potřeboat jejich transpozici
    pS1 = pS1.T; pS2 = pS2.T; # zde je traspozice, nyní jsme ji mohli udělat (předchozí řádek jim přidal dimenzi)
    r1=pS1-pI1 #rozdíl v x souřadnicích (všimněme si, že je to sloupec-řádek, Python je chytrý, tak vyrobí matici)
    r2=pS2-pI2 #rozdíl v y souřadnicích -- takovéto práci s vektory se říká broadcasting
    mohli_se_nakazit = (r1*r1+r2*r2) < vzdalenost_nakazy**2 #vyhneme se počítání odmocniny tak, že porovnáme s x^2
    mn = mohli_se_nakazit.shape #velikost výsledné matice
    nakazili_se_loc = np.random.rand(mn[0],mn[1]) < pravdepodobnost_nakazy #šance, že se nakazili, ale pro všechny
    nakazili_se_loc = nakazili_se_loc & mohli_se_nakazit #nakažení jsou ti, kteří měli True a byli blízko
    nakazili_se = np.full(stav.size, False) #alokace výsledného pole
    nakazili_se[stav == 'S'] = nakazili_se_loc.sum(1) > 0 #zapsání napočtených výsledků
                                                      #(suma přes všechny kontkakty s nemocnými)
    nakazili_ostatni = np.full(stav.size, 0) #alokace výsledného pole
    nakazili_ostatni[stav == 'I'] = nakazili_se_loc.sum(0) #(suma přes všechny kontkakty se zdravými)
    return nakazili_se, nakazili_ostatni

def pozice_domovu_praci(grid_domovu, grid_praci):
    prace_x_grid = np.linspace(1, 1.25, grid_praci[0]) # souřadnice v gridu prací na ose x
    prace_y_grid = np.linspace(-0.25, 1.25, grid_praci[1]) # souřadnice v gridu prací na ose y
    prace_x, prace_y = np.meshgrid(prace_x_grid, prace_y_grid) # vytvoření souřadnic (každý s každým x vs y)
    prace = np.array([prace_x.flatten(), prace_y.flatten()]) # uspořádání souřadnic do formátu dvojic
    prace = prace.T # ať mají stejné formát jako pozice - 2 sloupce x a y souřadnic

    domovy_x_grid = np.linspace(-0.25, 0.25, grid_domovu[0]) # souřadnice v gridu domovů na ose x
    domovy_y_grid = np.linspace(-0.25, 1.25, grid_domovu[1]) # souřadnice v gridu domovů na ose y
    domovy_x, domovy_y = np.meshgrid(domovy_x_grid, domovy_y_grid) # vytvoření souřadnic (každý s každým x vs y)
    domovy = np.array([domovy_x.flatten(), domovy_y.flatten()]) # uspořádání souřadnic do formátu dvojic
    domovy = domovy.T # ať mají stejné formát jako pozice - 2 sloupce x a y souřadnic
    return prace, domovy
