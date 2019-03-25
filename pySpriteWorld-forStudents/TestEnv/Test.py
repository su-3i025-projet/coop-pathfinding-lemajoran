#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:31:33 2019

@author: 3409249
"""
import numpy as np
import DiscreteWorldCoopPathFinding1Test as test1

import DiscreteWorldCoopPathFinding2Test as test2
import DiscreteWorldCoopPathFinding3Test as test3

import matplotlib.pyplot as plt


#les données de retour on la forme:
#   sum(step),          sum(ceil_iterations),     time,        max(ceil_iterations)
#   nbfioles pickedup   pirecas                   temps reel   meilleur cas

#Values for the plots
#nb_agents = [2,4,8,16]

nb_pickups = [i for  i in range(500,10500,500)]

m1 = []
m2 = []
m3 = []

for i in nb_pickups:
    m1.append(test1.main(i))
    m2.append(test2.main(i))
    m3.append(test3.main(i))





plt.plot(nb_pickups, np.transpose(m1)[1],c='r')
plt.plot(nb_pickups, np.transpose(m1)[2],c = 'b')
plt.plot(nb_pickups, np.transpose(m1)[3],c = 'g')
plt.savefig('methode1bis.png')

plt.clf()

plt.title("Nombre de fioles ramassées en fonction du nombre de pas")
plt.ylabel('Nombre de fioles ramassées')
plt.xlabel("Nombre d'itérations")
plt.plot(np.transpose(m1)[2],np.transpose(m1)[0],c='r',label = 'Méthode 1')
plt.plot(np.transpose(m2)[2],np.transpose(m2)[0],c='g',label = 'Méthode 2')
plt.plot(np.transpose(m3)[2],np.transpose(m3)[0],c='b',label = 'Méthode 3')
plt.legend()
plt.savefig('compare_methods.png')

plt.clf()
plt.plot(nb_pickups, np.transpose(m2)[1],c='r')
plt.plot(nb_pickups, np.transpose(m2)[2],c = 'b')
plt.plot(nb_pickups, np.transpose(m2)[3],c = 'g')
plt.savefig('methode2.png')
plt.clf()

plt.plot(nb_pickups, np.transpose(m3)[1],c='r')
plt.plot(nb_pickups, np.transpose(m3)[2],c = 'b')
plt.plot(nb_pickups, np.transpose(m3)[3],c = 'g')
plt.savefig('methode3.png')


plt.show()
