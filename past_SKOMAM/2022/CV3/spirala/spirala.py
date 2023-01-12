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
    
plt.imshow(material, cmap="jet")
plt.colorbar()

material[material==1]=0

med = 0
zima = 1
teplo = 2
beton = 3

lam_med = 372.0
rho_c_med = 8800*380
U_med = 10

lam_zima = 372.0
rho_c_zima = 8800*380 # np.inf
U_zima = 10 # 0

lam_teplo = 372.0
rho_c_teplo = np.inf
U_teplo = 80

lam_beton = 0.52
rho_c_beton = 1300*840
beton = 10

tabulka = np.array([lam_med,
rho_c_med,
U_med,

lam_zima,
rho_c_zima,
U_zima,

lam_teplo,
rho_c_teplo,
U_teplo,

lam_beton,
rho_c_beton,
beton]).reshape((4,3))

LAM_mean = material.copy()
RHO_C_mean = material.copy()
U = material.copy()
for i in range(4):
    LAM_mean[material==i] = tabulka[i,0]
    RHO_C_mean[material==i] = tabulka[i,1]
    U[material==i] = tabulka[i,2]
LAM = LAM_mean
RHO_C = RHO_C_mean
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

np.save("U_initial.npy",U)
np.save("LAM.npy",LAM)
np.save("RHO_C.npy",RHO_C)
np.save("material.npy",material)









