#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 10:10:39 2022

@author: simona
"""

import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

image = img.imread("zaklad.png")

zaklad = image[:,:,0] + image[:,:,1] + image[:,:,2]

un = np.unique(zaklad)
material = zaklad.copy()
for idx,col in enumerate(un):
    material[zaklad==col] = idx
    
# plt.imshow(material, cmap="jet")
# plt.colorbar()

cihla = 0
omitka = 1
malta = 2
venku = 3
polystyren = 4
vevnitr = 5

lam_cihla = 0.64
lam_cihla_odch = 0.13
rho_c_cihla = 1400*920
rho_c_cihla_odch = 600*920
U_cihla = 0

lam_omitka = 0.935
lam_omitka_odch = 0.055
rho_c_omitka = 1462000
rho_c_omitka_odch = 118000
U_omitka = 0

lam_malta = 1.015
lam_malta_odch = 0.145
rho_c_malta = 840*1800
rho_c_malta_odch = 840*200
U_malta = 0

lam_venku = 0.026
lam_venku_odch = 0
rho_c_venku = np.inf
rho_c_venku_odch = 0
U_venku = -20

lam_polystyren = 0.044
lam_polystyren_odch = 0.007
rho_c_polystyren = 1270*35
rho_c_polystyren_odch = 1270*25
U_polystyren = 0

lam_vevnitr = 0.026
lam_vevnitr_odch = 0
rho_c_vevnitr = np.inf
rho_c_vevnitr_odch = 0
U_vevnitr = 20

tabulka = np.array([lam_cihla,
    lam_cihla_odch,
    rho_c_cihla,
    rho_c_cihla_odch,
    U_cihla,

    lam_omitka,
    lam_omitka_odch,
    rho_c_omitka,
    rho_c_omitka_odch,
    U_omitka,
    
    lam_malta,
    lam_malta_odch,
    rho_c_malta,
    rho_c_malta_odch,
    U_malta,
    
    lam_venku,
    lam_venku_odch,
    rho_c_venku,
    rho_c_venku_odch,
    U_venku,
    
    lam_polystyren,
    lam_polystyren_odch,
    rho_c_polystyren,
    rho_c_polystyren_odch,
    U_polystyren,
    
    lam_vevnitr,
    lam_vevnitr_odch,
    rho_c_vevnitr,
    rho_c_vevnitr_odch,
    U_vevnitr]).reshape((6,5))

nahoda = np.random.rand(70,70)*2-1
# plt.imshow(nahoda)
# plt.colorbar()
LAM_mean = nahoda.copy()
LAM_nahoda = nahoda.copy()
RHO_C_mean = nahoda.copy()
RHO_C_nahoda = nahoda.copy()
U = nahoda.copy()
for i in range(6):
    LAM_mean[material==i] = tabulka[i,0]
    LAM_nahoda[material==i] *= tabulka[i,1]
    RHO_C_mean[material==i] = tabulka[i,2]
    RHO_C_nahoda[material==i] *= tabulka[i,3]
    U[material==i] = tabulka[i,4]
LAM = LAM_mean + LAM_nahoda
RHO_C = RHO_C_mean + RHO_C_nahoda
fig,ax = plt.subplots(1,4, figsize=(17,3))
im = ax[0].imshow(U,cmap="jet")
fig.colorbar(im,ax=ax[0])
ax[0].set_title("$u(x,y,0)$")
im = ax[1].imshow(LAM,cmap="jet")
fig.colorbar(im,ax=ax[1])
ax[1].set_title("$\lambda(x,y)$")
im = ax[2].imshow(RHO_C,cmap="jet")
fig.colorbar(im,ax=ax[2])
ax[2].set_title("$\\rho(x,y)c(x,y)$")
im = ax[3].imshow(material,cmap="jet")
fig.colorbar(im,ax=ax[3])
ax[3].set_title("znázornění materiálů")

np.save("cihly_U.npy",U)
np.save("cihly_LAM.npy",LAM)
np.save("cihly_RHO_C.npy",RHO_C)
np.save("cihly_material.npy",material)









