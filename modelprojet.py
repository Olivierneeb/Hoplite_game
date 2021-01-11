# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 17:17:52 2020

@author: Neeb Olivier
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 11:53:58 2020

@author: hamzaelfergougui
"""

from random import *
import numpy
from copy import *



def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def ajout_strict(liste, objet): # Fonction précaution qui remplace la fonction append
    
    if objet not in liste:
        liste.append(objet)

def supprime_strict(liste, objet): # Fonction pour éviter les erreurs de remove
   
    if objet in liste:
        liste.remove(objet)
        
    
class Case : 
    
    def __init__( self ,x , y, centre = None, numero = None): 
        self.x = x
        self.y = y
        self.centre = centre
        # self.numero = numero    # inutile en fait je pense, valeur jamais affectée
        # self.indice = (x,y)   # inutile si définition de __eq__(self, autre_case)
        
    
    def __repr__(self):
        return f'{self.x} et {self.y}'
    
    def __eq__(self,autre_case):
        if ( self.x == autre_case.x and self.y == autre_case.y):
            return True
        else :
            return False 
        
    def liste_cases_a_proximite(self, l_cases):
        l_cases_adjacentes = []
        for case in l_cases:
            if ((abs(self.x - case.x) == 2 and abs(self.y - case.y) == 0) or \
                 (abs(self.x - case.x) == 1 and abs(self.y - case.y) == 1)):
                l_cases_adjacentes.append(deepcopy(case))
        return l_cases_adjacentes
    
    def sum_difference_case(self,case):
        return( abs(case.x -self.x) + 2*abs(case.y -self.y))
    
        

        
        
class Plateau : 
    # génération d'un plateau de 79 cases, dont self.cases_inaccessible  sont les cases cases_mortes 
    # contient les dimensions du jeu, les cases accessibles et les cases cases_mortes
    # plateau de taille toujours 79 cases 
    def __init__(self,N):
        N_max = 79
        assert N <= N_max and N>=0 and type(N) == int
        
           
        
        self.cases_inaccessible =[]
        self.plat = [ [k for k in range(17,4,-2)], [k for k in range(18,3,-2)],
                         [k for k in range(19,2,-2)],[k for k in range(20,1,-2)],
                         [k for k in range(21,0,-2)],[k for k in range(20,1,-2)],
                         [k for k in range(19,2,-2)],[k for k in range(18,3,-2)],
                         [k for k in range(17,4,-2)]]
        
        # rajoute un indice au début de la liste pour savoir de quelle colonne on parle 
        for k in range (1, len(self.plat)+ 1 ):
            self.plat[k-1] = [k] + self.plat[k-1] 
            
        self.plateau_complet = []
        
        # on ajoute toutes les objets Cases avec des indices correpondantes à chaque case dans plateau_complet
        for col in self.plat:
            for ligne in col[1:] : 
                self.plateau_complet.append(Case( ligne , col[0] ))
                
        self.cases_non_mortes = deepcopy(self.plateau_complet)
        self.cases_mortes = []
        
        # On choisit dans cases_non_mortes,  N cases au hasard, on les extrait de la liste
        # et on les stocke dans cases_mortes
        for p in range(N):
            case_choisie = choice(self.cases_non_mortes)
            self.cases_non_mortes.remove(case_choisie)
            self.cases_mortes.append(case_choisie)
        
 
    
class heros():
    
    def __init__(self,case):
        self.case = case
        self.name = "Le heros"
        self.pv = 5
        self.pv_max = 5
        self.lance_name = "La lance"
        self.lance_case = deepcopy(self.case)
        self.lance_etat = True
        self.sauter = 100  # chaque saut nécessite 50 points d'énergie et le heros regagne 20 pointts d'energie par saut
        
    def __repr__(self):
        return(f'{self.name} a {self.pv} PV, a {self.sauter} en énergie de saut et est en ({self.case.x}, {self.case.y})')
    
    def a_proximite(self,l_demons,l_archers):     
        
        self.voisins_demons = []
        self.voisins_archers = []
        for demon in l_demons : 
            if (abs (demon.case.x - self.case.x ) == 1 and abs (demon.case.y - self.case.y ) == 1)  \
             or (abs (demon.case.x - self.case.x ) == 2 and abs (demon.case.y - self.case.y ) == 0) :
                ajout_strict(self.voisins_demons,demon)
        for archer in l_archers : 
            if (abs (archer.case.x - self.case.x ) == 1 and abs (archer.case.y - self.case.y ) == 1)  \
             or (abs (archer.case.x - self.case.x ) == 2 and abs (archer.case.y - self.case.y ) == 0):
                 ajout_strict(self.voisins_archers,archer)
        self.voisins = [self.voisins_demons,self.voisins_archers]
        return self.voisins
    
    def case_a_portee_move_direct(self, case_cliquee):
        
        if  ( (abs(self.case.x - case_cliquee.x) == 1 and abs(self.case.y - case_cliquee.y) == 1) \
            or ((abs(self.case.x - case_cliquee.x) == 2 and abs(self.case.y - case_cliquee.y) == 0)) ):       
              
             return True
        
        return False
    
    def case_a_portee_saut(self, case_cliquee):
        
        if  ( ( (abs(self.case.x - case_cliquee.x) == 4 and abs(self.case.y - case_cliquee.y) == 0) or \
                 (abs(self.case.x - case_cliquee.x) == 3 and abs(self.case.y - case_cliquee.y) == 1) or \
                 (abs(self.case.x - case_cliquee.x) in [0,2] and abs(self.case.y - case_cliquee.y) == 2) ) ):       
              
             return True
        
        return False
    
    def case_a_portee_lance(self, case_cliquee):
        
        if   ( ( (abs(self.lance_case.x - case_cliquee.x) in [4,2] and abs(self.lance_case.y - case_cliquee.y) == 0) or \
                 (abs(self.lance_case.x - case_cliquee.x) in [1,3] and abs(self.lance_case.y - case_cliquee.y) == 1) or \
                 (abs(self.lance_case.x - case_cliquee.x) in [0,2] and abs(self.lance_case.y - case_cliquee.y) == 2) ) ):
            
            return True
        
        return False
    
    def gagner_energie_saut(self):
         
        self.sauter = self.sauter + 20  # Le héros gagne 20 points d'énergie pour chaque ennemie tué
                  
        if self.sauter > 100:
                  self.sauter = 100  # La barre d'énergie de saut du heros est complete
    
    
        
 
class Demon():
    
    def __init__(self, case):
        self.case = case
        self.name = "demon"
        self.pv = 1
 
    def __repr__(self):
        return(f'{self.name} a {self.pv} PV et est en ({self.case.x}, {self.case.y})' )
    
    def heros_a_portee_demon(self,case_heros):
        # méthode utilisée pour l'affichage 
        if   ( ( (abs(self.case.x - case_heros.x) in [4,2] and abs(self.case.y - case_heros.y) == 0) or \
                 (abs(self.case.x - case_heros.x) in [1,3] and abs(self.case.y - case_heros.y) == 1) or \
                 (abs(self.case.x - case_heros.x) in [0,2] and abs(self.case.y - case_heros.y) == 2) ) ):
            
            return True
        
        return False
      

class Archer():
    
    def __init__(self,case):
        self.case = case
        self.name = "archer"
        self.pv = 1
        
    def __repr__(self):
        return(f'{self.name} a {self.pv} PV et est en ({self.case.x}, {self.case.y})' )
  

    def heros_a_portee_archer(self, case_heros):
       # méthode pur savoir si l'archer attaque, et pour l'affichage de la portée de l'archer
       if  ( ( 4 <= abs(case_heros.x - self.case.x ) <= 10 and abs(case_heros.y - self.case.y ) == 0 ) \
               or ( abs(case_heros.x - self.case.x ) == 2 and  abs(case_heros.y - self.case.y ) == 2 ) \
               or ( abs(case_heros.x - self.case.x ) == 3 and  abs(case_heros.y - self.case.y ) == 3 ) \
               or ( abs(case_heros.x - self.case.x ) == 4 and  abs(case_heros.y - self.case.y ) == 4 ) \
               or ( abs(case_heros.x - self.case.x ) == 5 and  abs(case_heros.y - self.case.y ) == 5 ) ):
              
               return True
           
       return False
            

if __name__=="__main__":
    
    
        # Méthode de la classe Case
    # Test de la méthode .liste_cases_a_proximite(liste_cases) d'une Case
    a = Case(1,2)
    b = Case(3,2)
    c = Case(2,3)
    d = Case(2,1)
    l_tempo =  [Case(1,2), Case(3,2),Case(2,3),Case(2,1)]
    print(d.liste_cases_a_proximite(l_tempo)) 
    # print la liste des cases adjacentes de d
    # d est à coté de a et b mais de c. La case a à 3 voisins, b,c,d
    
    # Test de l'équalité __eq__(autre_case) entre 2 Cases 
    a = Case(1,2)
    b= Case(1,2)
    print(f'a vaut : {a}\net b vaut :{b}')
    print(f'a égale b ? : {a == b}') 
    b.centre = (10,10)
    print(f'a égale b modifiée ? : {a==b}')
    
        # classe Plateau
    # génération d'un Plateau et listes des Cases mortes et non mortes
    nb_cases_mortes = 10
    plat = Plateau(nb_cases_mortes)
    print(f'Le plateau est composé de {len(plat.plateau_complet)} cases au total \n \
          dont {len(plat.cases_mortes)} cases mortes et {len(plat.cases_non_mortes)} cases non mortes')
    print(f'La liste des cases mortes est :\n{plat.cases_mortes}')
             
        # Méthodes du héros 
    # Test de la méthode case_a_portee_saut du héros 
    case_heros = Case(1,2)
    case_cliquee = Case(4,3)
    h = heros(case_heros)
    verite_saut = h.case_a_portee_saut(case_cliquee)
    print(f' le héros peut-il sauter dans la case cliquée ? {verite_saut}')
        
    # Test de la fonction gagner_energie_saut du héros 
    case_heros = Case(1,2)
    h = heros(case_heros)
    print(h)
    h.sauter = h.sauter - 30
    print(h)
    h.gagner_energie_saut()
    print(h)
    
    # Test de la méthode case_a_portee_move_direct du héros
    case_heros = Case(1,2)
    case_cliquee = Case(4,2)
    h = heros(case_heros)
    verite_move_direct = h.case_a_portee_move_direct(case_cliquee)
    print(f"Le héros peut se dépalcer sur la case cliquée ? {verite_move_direct}")
    
    # Test de la méthode .a_proximité du héros 
    l_demons = []
    l_archers = []
    hero = heros(Case(1,3))
    dem = Demon(Case(2,4))
    l_demons.append(dem)
    arch = Archer(Case(2,3))
    l_archers.append(arch)
    ennemies_proches = hero.a_proximite(l_demons,l_archers)
    print(f'les ennemis proche du héros sont :\n{ennemies_proches}')
    
    
        # Methode de l'archer
    # Test de la méthode case_a_portee_lance du héros 
    case_heros = Case(1,2)
    case_cliquee = Case(4,3)
    h = heros(case_heros)
    la_lance = h.lance_case
    print(f'la lance est en {la_lance}')
    verite_lance = h.case_a_portee_lance(case_cliquee)
    print(f'la case cliquée est à portée de la lance? ? {verite_lance}')
    
        # Méthode du Démon
    # test de la méthode heros_a_portee_demon du démon
    h = heros(Case(1,1))
    dem_1 = Demon(Case(5,1)) 
    dem_2 = Demon(Case(4,2))
    dem_3 = Demon(Case(5,3))
    print(f'Le démon 1 est à portée du héros {dem_1.heros_a_portee_demon(h.case)}')
    print(f'Le démon 2 est à portée du héros {dem_2.heros_a_portee_demon(h.case)}')
    print(f'Le démon 3 est à portée du héros {dem_3.heros_a_portee_demon(h.case)}')

    
    
        # Méthode de l'archer 
    # Test de la méthode heros_a_portee_archer de l'archer 
    case_heros = Case(1,2)
    case_archer = Case(2,6)
    h = heros(case_heros)
    archer = Archer(case_archer)
    print(archer)
    verite_portee = archer.heros_a_portee_archer(case_heros)
    print(f"le héros est-il à portée de l'archer ? {verite_portee}")
        
        

    
    
    
    
    
    