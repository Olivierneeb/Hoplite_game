# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 17:17:51 2020

@author: Neeb Olivier
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 11:54:37 2020

@author: hamzaelfergougui
"""


from copy import *
from random import *
from PyQt5.QtCore import *

from modelprojet import *

# Le nombre de case mortes du jeu N est récupéré depuis la fenêtre
# Le nombre d'ennemies est un couple est aussi récupéré depuis la fenêtre : [nb_demons,nb_archers] = nb_ennemies 

class BaseControler:
    def __init__(self):
        self.clients = list()
    
    def add_clients(self, client):
        self.clients.append(client)
        
    def refresh_all(self):             
        for client in self.clients:
             client.refresh()
             
    def end_game(self):
        for client in self.clients :
            client.end_game()

class hopliteControler(BaseControler):
    def __init__(self):
        super().__init__()
        # on initialise certains paramètrs, pour eviter les erreurs en cas de clic sur la scene 
        # avant d'avoir appuyer sur le bouton start
        self.hero = None
        self.plateau = None
        self.action = 1
        self.message_erreur = " "
    
    def start(self, nb_ennemies, N):
        # fonction exécutée après l'appui sur le bouton start,
        # elle génère un plateau avec N cases morte, et place le héros, et les ennemis (démons+archers) aléatoirement dessus
        
        self.plateau = Plateau(N)
        self.cases_mortes = deepcopy(self.plateau.cases_mortes) # Cases mortes du jeu (Cases interdites)
        self.cases_non_mortes = deepcopy(self.plateau.cases_non_mortes) # Cases non mortes du jeu
        
        self.cases_libres = deepcopy(self.plateau.cases_non_mortes) # Copie des cases non mortes, cet attribut va s'actualiser à chaque tour
        
        [nb_demons,nb_archers] = nb_ennemies # nb_ennemies est une liste de 2 entiers
        self.demons = []
        self.archers = []
        self.ennemies = [self.demons,self.archers]
        
        # création des démons + actualisation cases_libres
        for i in range(nb_demons): 
            case_choisie = choice(self.cases_libres) # Choix d'une case pour chaque demon parmis les cases libres
            self.demons.append(Demon(case_choisie)) # Création et ajout de l'objet Demon
            supprime_strict(self.cases_libres,case_choisie)  # Retrait de cette case des cases libres du tour  

        # création des archers + actualisation cases_libres           
        for i in range(nb_archers):
            case_choisie = choice(self.cases_libres) # Choix d'une case pour chaque archer parmis les cases libres
            self.archers.append(Archer(case_choisie)) # Création et ajout de l'objet Archer
            supprime_strict(self.cases_libres,case_choisie)  # Retrait de cette case des cases libres du tour  

        # création du héros + actualisation cases_libres
        self.case_hero = choice(deepcopy(self.cases_libres)) # Création d'une case pour le heros parmis les cases libres
        self.hero = heros(self.case_hero) # Création de l'objet hero
        supprime_strict(self.cases_libres,self.case_hero) # Retrait de cette case des cases libres du tour   

        
        print(f'le heros est : {self.hero}')
        print(f'la liste des démons est : \n {self.demons}')
        self.refresh_all()
        
        
        
        
        

        
    # Ensemble des fonctions concernat le héros, se déplacer, attaquer les ennemis à proximité
        
    def move_hero_direct(self, case):  # La fonction move_hero_direct reçoit en entrée une case (clic du joueur sur la scène : mousePressEvent)
       
        case_cliquee = case
        move_direct = self.hero.case_a_portee_move_direct(case_cliquee) # Test de l'éligibilité de la case choisie

        if (case in self.cases_libres) and (move_direct) and (case in self.cases_non_mortes):
              
              supprime_strict(self.cases_libres, case)
              ajout_strict(self.cases_libres,self.hero.case)
              self.hero.case = case # Mise à jour de la case du joueur
              if self.hero.lance_etat:
                  self.hero.lance_case = self.hero.case # Mise à jour de la case de la lance 
            
        else:
            return('case de déplacement impossible')  # Si la case ne vérifie pas ces conditions on retourne un message au joueur
    def attack_hero_direct(self):
                   
        [demons_a_proximite,archers_a_proximite] = self.hero.a_proximite(self.demons,self.archers) # Renvoie les ennemies à proximité du heros
        
        for demon in demons_a_proximite:
                supprime_strict(self.demons,demon) # On élimine tous les démons à proximité du joueur
                ajout_strict(self.cases_libres,demon.case) # On ajoute la case du demon éliminé aux cases libres
                self.hero.gagner_energie_saut()

                
        for archer in archers_a_proximite:
                supprime_strict(self.archers,archer) # On élimine tous les archers à proximité du joueur
                ajout_strict(self.cases_libres,archer.case) # On ajoute la case de l'archer éliminé aux cases libres
                self.hero.gagner_energie_saut()
                
                
                
    def sauter_hero(self, case):   # Cette fonction est associée à un bouton saut du jeu
        
        case_cliquee = case
        sauter = self.hero.case_a_portee_saut(case_cliquee) # Test de l'éligibilité de la case choisie
        
        if (sauter) and (self.hero.sauter//50 > 0) and (case in self.cases_libres) and (case in self.cases_non_mortes): 
            
              supprime_strict(self.cases_libres, case)
              ajout_strict(self.cases_libres,self.hero.case)
              self.hero.case = case
              if self.hero.lance_etat:
                  self.hero.lance_case = self.hero.case # Mise à jour de la case de la lance
              self.hero.sauter = self.hero.sauter - 50 # Le héros perd 50 points d'énergie
             
        else:
            return('case de saut impossible')  # Si la case ne vérifie pas ces conditions on retourne un message au joueur
                # La fonction attack_hero_direct est toujours exécuté quand le héros se trouve à proximité de l'ennemie

    
    
    def attack_hero_lance(self, case): # Cette fonction est associée à un bouton du jeu
    
        # Faire une méthode de test d'éligibilité sur le model
        # Faire un if : Retour False au joueur pour lui proposer une deuxieme chance
        # Les fonctions doivent renvoyer un True ou False ou View avec message d'erreur en cas d'impossibilité
        case_cliquee = case
        lancer = self.hero.case_a_portee_lance(case_cliquee) # Test de l'éligibilité de la case choisie
        
        if   ( ( lancer ) and (self.hero.lance_etat == True) and (case in self.cases_non_mortes) ):
            
            self.hero.lance_etat = False
            self.hero.lance_case = case
            
            
            for demon in self.demons:
                if demon.case.x == self.hero.lance_case.x and demon.case.y == self.hero.lance_case.y:
                   supprime_strict(self.demons,demon)# On élimine le démon se retrouvant au même endroit que la lance au tour N
                   ajout_strict(self.cases_libres,demon.case) # On ajoute la case de ce démon éliminé aux cases libres
                   self.hero.gagner_energie_saut()
  
            for archer in self.archers:
                if demon.case.x == self.hero.lance_case.x and demon.case.y == self.hero.lance_case.y:
                   supprime_strict(self.archers,archer) # On élimine l'archer se retrouvant au même endroit que la lance au tour N
                   ajout_strict(self.cases_libres,archer.case) # On ajoute la case de cet archer éliminé aux cases libres
                   self.hero.gagner_energie_saut()
        else:
            return('case de lancer impossible')  # Si la case ne vérifie pas ces conditions on retourne un message au joueur
        
        #La lance peut être lancé à une porte maximale, tout inclus
        #Le heros et les ennemies peuvent etre à la meme case que la lance
              

    def recup_lance_hero(self):
            
        if self.hero.case.x == self.hero.lance_case.x and self.hero.case.y == self.hero.lance_case.y   :
            self.hero.lance_etat = True
            self.hero.lance_case = self.hero.case
        # Dans le View définir une fonction qui affiche l'image de la lance sur la scène
        # en fonction de l'état de vérité de la lance: True ou bien False à la case correspondante
        
        
        
        
        
        
        
        
        
        
        
    def case_optimale_deplacement(self,demon):
        # cherche la case optimale pour un déplacement vers le heros
        # renvoie une case 
        
        if sign(self.hero.case.y - demon.case.y) == 0:
            case_optimale = Case( demon.case.x + 2*sign(self.hero.case.x-demon.case.x), demon.case.y)
        else:
            if sign(self.hero.case.x-demon.case.x) == 0:
                case_optimale = Case(demon.case.x + choice([-1,1]),demon.case.y + sign(self.hero.case.y - demon.case.y) )
            else:
                case_optimale = Case(demon.case.x + sign(self.hero.case.x-demon.case.x), demon.case.y + sign(self.hero.case.y - demon.case.y) )
        return(case_optimale)
    
    
        
    
    
    
    
    
    
    
    
    
    # Ensemble des fonctions conernant les démons et les archers 
    
    def move_demons(self):
        
        # Mouvement de tous les démons 
        # On va choisir une case optimale en direction du héros, si elle est libre le démon se dépalce vers cette case
        # Sinon, on observe 2 cases alterantives, adjacentes de la case optimale et dans la direction du héros
        # Si ni la case optimale, ni les 2 cases optimales ne sont libres, alors le démon ne bouge pas
        
        self.indices_plateau_libres = [[case.x,case.y] for case in self.cases_libres]
        
        for demon in self.demons:
            case_optimale = self.case_optimale_deplacement(demon)
            case_demon_avant_deplacement = deepcopy(demon.case) 
            # le demon veut se deplacer en {case_optimale}, on regarde si la case_optimale est libre 
            if case_optimale in self.cases_libres:
                demon.case = deepcopy(case_optimale)
            else:
                # la case optimale n'est pas libre, il faut donc trouver une case alternative, 
                # les cases alternatives sont les 2 cases à coté de la case optimale dans la direction du héros
                l_cases_adjacentes_demon = demon.case.liste_cases_a_proximite(self.cases_libres)
                l_cases_adjacentes_case_optimale = case_optimale.liste_cases_a_proximite(self.cases_libres)
                liste_cases_alternatives = [ case for case in l_cases_adjacentes_demon if case in l_cases_adjacentes_case_optimale]
             
                if liste_cases_alternatives:
                    # si il y a une case alternative seulement, le démon va se déplacer sur cette case
                    # si il y a 2 cases alternatives, on choisit la case qui réduit la distance au héros,
                    # cette distance est calculée dans case.sum_difference_case(self.hero.case)
                    l_sum_case = [ case.sum_difference_case(self.hero.case) for case in liste_cases_alternatives ]
                    indice_case_alternative = l_sum_case.index(min(l_sum_case))
                    case_alternative = liste_cases_alternatives[ indice_case_alternative]
                    print(f'la meilleure alternative à {case_optimale} sont :\n{case_alternative}')
                    demon.case = deepcopy(case_alternative)
                
            ajout_strict(self.cases_libres,case_demon_avant_deplacement) # On ajoute l'ancienne case du demon dans les cases libres
            supprime_strict(self.cases_libres,demon.case) # On enlève la nouvelle case du demon des cases libres
            

            
    def attack_demons(self):
              
        for demon in self.demons:
            if ( abs(self.hero.case.x - demon.case.x ) == 2 and abs(self.hero.case.y - demon.case.y ) == 0 ) \
               or ( abs(self.hero.case.x - demon.case.x ) == 1 and abs(self.hero.case.y - demon.case.y ) == 1 ) :
                self.hero.pv = self.hero.pv - 1 # Le joueur perd un point de PV à la suite à cette attaque
      
        
        
    
    def move_archer(self,archer):
        
        # Mouvement d'un archer
        # A noter que si l'archer se déplace, alors il n'attaque pas, et donc le héros n'est pas en portée de tir
        
        # on détermine la case de dépalcement de l'archer en séparant différents cas, en fonction de sa position avec le héros
        # si l'archer et le héros sont sur la même colonne, l'archer va essayer de mettre le héros en portée de tir
        # sinon, l'archer va essayer d'aligner sa portée avec la position du héros
        
        case_archer = deepcopy(archer.case)
        
        if  abs(self.hero.case.x - archer.case.x)> 10 and self.hero.case.y == archer.case.y:
            
            if Case(archer.case.x + 2*sign( self.hero.case.x - archer.case.x ), archer.case.y) in self.cases_libres:

                archer.case.x = archer.case.x + 2*sign(self.hero.case.x - archer.case.x)
                ajout_strict(self.cases_libres,case_archer) # On ajoute l'ancienne case de l'archer dans les cases accessibles
                supprime_strict(self.cases_libres,archer.case) # On enlève la nouvelle case de l'archer des cases accessibles
                
        elif 0 <abs(self.hero.case.x - archer.case.x)<= 4 and self.hero.case.y == archer.case.y:
            
            if Case(archer.case.x - 2*sign( self.hero.case.x - archer.case.x ), archer.case.y) in self.cases_libres:

                archer.case.x = archer.case.x - 2*sign(self.hero.case.x - archer.case.x)
                ajout_strict(self.cases_libres,case_archer)
                supprime_strict(self.cases_libres,archer.case)
                
        elif  abs(self.hero.case.y - archer.case.y)> 5 and self.hero.case.x != archer.case.x:
            
            if Case(archer.case.x + sign( self.hero.case.x - archer.case.x ), archer.case.y + sign( self.hero.case.y - archer.case.y )) in self.cases_libres:

                archer.case.x = archer.case.x + sign(self.hero.case.x - archer.case.x) 
                archer.case.y = archer.case.y + sign(self.hero.case.y - archer.case.y) 
                ajout_strict(self.cases_libres,case_archer) 
                supprime_strict(self.cases_libres,archer.case)
                
                
        elif 3 <= abs(self.hero.case.y - archer.case.y)<= 5 and self.hero.case.x != archer.case.x:
            
            if Case(archer.case.x + sign( self.hero.case.x - archer.case.x ), archer.case.y + sign(self.hero.case.y - archer.case.y)) in self.cases_libres:

                archer.case.x = archer.case.x + sign(self.hero.case.x - archer.case.x) 
                archer.case.y = archer.case.y + sign(self.hero.case.y - archer.case.y) 
                ajout_strict(self.cases_libres,case_archer) 
                supprime_strict(self.cases_libres,archer.case)
        
        elif 0 < abs(self.hero.case.y - archer.case.y)<= 2 and self.hero.case.x != archer.case.x:
            
            if Case(archer.case.x - sign( self.hero.case.x - archer.case.x ), archer.case.y - sign(self.hero.case.y - archer.case.y)) in self.cases_libres:

                archer.case.x = archer.case.x - sign(self.hero.case.x - archer.case.x) 
                archer.case.y = archer.case.y - sign(self.hero.case.y - archer.case.y) 
                ajout_strict(self.cases_libres,case_archer) 
                supprime_strict(self.cases_libres,archer.case)
                
                                      
        elif self.hero.case.x == archer.case.x and abs(self.hero.case.y - archer.case.y)> 5: # On ne peut pas regrouper ce cas avec les autres cas, sinon nous aurons un déplacement qui existe pas!
            
            if Case(archer.case.x + 1 , archer.case.y + sign(self.hero.case.y - archer.case.y)) in self.cases_libres:

                archer.case.x = archer.case.x + 1 
                archer.case.y = archer.case.y + sign(self.hero.case.y - archer.case.y) 
                ajout_strict(self.cases_libres,case_archer)
                supprime_strict(self.cases_libres,archer.case)
                
        elif self.hero.case.x == archer.case.x and 0 < abs(self.hero.case.y - archer.case.y)<= 5:
            
            if Case(archer.case.x + 2 , archer.case.y) in self.cases_libres:

                archer.case.x = archer.case.x + 2
                ajout_strict(self.cases_libres,case_archer)
                supprime_strict(self.cases_libres,archer.case)
                
            elif Case(archer.case.x - 2 , archer.case.y) in self.cases_libres:

                archer.case.x = archer.case.x - 2
                ajout_strict(self.cases_libres,case_archer)
                supprime_strict(self.cases_libres,archer.case)
                          
                

    def attack_archer(self,archer):
        portee_archer = archer.heros_a_portee_archer(self.hero.case) # On vérifie si le heros est à la portée de l'archer
        if portee_archer:
             self.hero.pv = self.hero.pv - 1 # Le joueur perd un point de PV à la suite à cette attaque
      
        
    
    def action_dep_possible(self, action,case_cliquee):
        # utilisé uniquement pour l'affichage de la portée des ennemis dans view 
        if action ==1  and not ((self.hero.case_a_portee_move_direct(case_cliquee)) and (case_cliquee in self.cases_libres) ):
            return False
        else:
            return True
        
        
        
        
        
        
        
        
    
    def next_game(self,action,case_cliquee):
             self.message_erreur =" "
           # Cette fonction est la fonction qui va exécuter le déroulement d'un tour
        
           # elle s'active après chaque clic sur la scene uniquement
           # et en fonction de du numéro de l'action, on exécute une action de déplacement, saut ou lance
           # par défaut, un clic sur la scene, sans appui de bouton préalable correspond à l'action de se déplacer du héros
        
           # Si le bouton saut ou lance est appuyé, alors on va testé si la case cliquée vérifie les conditions de l'action souhaitée
           # (on vérifie si la case est en portée ou case libre )
        
           
             # Trois possibilités: action ==1  => déplacement/action == 2  => saut/action == 3  => lance 
        
             # Si le joueur clique sur une case de la scène : action "1"
             if action == 1:
                  if (self.hero.case_a_portee_move_direct(case_cliquee)) and (case_cliquee in self.cases_libres):
                     # la case cliquée est adjacente à celle du héros, et elle est libre 
                     self.move_hero_direct(case_cliquee)
                     self.attack_hero_direct()
                     self.recup_lance_hero()
                     self.move_demons()
                     # Les archers ne peuvent faire qu'une action par tour: attaquer ou se déplacer
                     for archer in self.archers:
                         if archer.heros_a_portee_archer(self.hero.case):
                            self.attack_archer(archer)
                         else:
                            self.move_archer(archer)
                     self.attack_demons()     
                     self.refresh_all()
                     self.is_game_over()
                                        
                  else:
                     # la case cliquée n'est ni libre, si adjacente du héros
                     self.refresh_all()
                     self.is_game_over()
                     
                     self.message_erreur =  self.move_hero_direct(case_cliquee) # Retourne: 'case de déplacement direct inaccessible'
                 
        
             # Si le joueur clique sur le bouton sauter au préalable
             # On vérifie les conditions de l'action "2" 
             if action == 2:  
                  if (self.hero.case_a_portee_saut(case_cliquee)) and (case_cliquee in self.cases_libres):
                     self.sauter_hero(case_cliquee)
                     self.attack_hero_direct()
                     self.recup_lance_hero()
                     self.move_demons()
                     # Les archers ne peuvent faire qu'une action par tour: attaquer ou se déplacer
                     for archer in self.archers:
                         if archer.heros_a_portee_archer(self.hero.case):
                            self.attack_archer(archer)
                         else:
                            self.move_archer(archer)
                     self.attack_demons()
                     self.action = 1
                     self.refresh_all()
                     self.is_game_over()
                  else:
                     self.refresh_all()
                     self.is_game_over()
                     self.message_erreur =  self.sauter_hero(case_cliquee) # Retourne: 'case de saut inaccessible'
             
             # Si le joueur clique sur le bouton lance au préalable  
             # On vérifie les conditions de l'action "3"
             if action == 3:
                  if (self.hero.case_a_portee_lance(case_cliquee)) and (case_cliquee in self.cases_non_mortes):
                     self.attack_hero_lance(case_cliquee)
                     self.attack_hero_direct()
                     self.recup_lance_hero()
                     self.move_demons()
                     # Les archers ne peuvent faire qu'une action par tour: attaquer ou se déplacer
                     for archer in self.archers:
                         if archer.heros_a_portee_archer(self.hero.case):
                            self.attack_archer(archer)
                         else:
                            self.move_archer(archer)
                     self.attack_demons()
                     self.action = 1
                     self.refresh_all()
                     self.is_game_over()
                  else:
                     self.refresh_all()
                     self.is_game_over()
                     self.message_erreur =  self.attack_hero_lance(case_cliquee) # Retourne: 'case de lancer inaccessible'
                 
                    
                    
                    
                    
              
    def is_game_over(self):
        # on teste à la fin de chaque tour, cad apres une exéctuion réussie de next_game 
        # si le héros est mort (Défaite) ou si tous les ennemis sont morts (Victoire)
        if (len(self.demons) == 0 and len(self.archers) == 0)  or self.hero.pv <= 0 :
            self.end_game()
            
    
if __name__=="__main__":
    
    Jeu = hopliteControler() # Création du Jeu
    Jeu.start([2,3],0) # Initialisation du Jeu, on affiche les éléments du jeu
    print(Jeu.cases_mortes)
    print(Jeu.cases_non_mortes)
    
    # Attention à bien choisir des cases existantes dans la liste des cases du plateau
    # Pour cela génerer le plateau une première fois pour visualiser l'ensemble des cases possibles: mortes et non mortes
    
    # Test de la fonction de deplacement direct
    
    Case_deplacement = Case(17,1)
    Jeu.hero.case = Case(15,1)
    print(Jeu.hero.case)
    Jeu.move_hero_direct(Case_deplacement)
    print(Jeu.hero.case,"est la case après déplacement direct")
    
    # Test de la fonction lancer la lance
    
    Case_lancer = Case(18,6)
    Jeu.hero.case = Case(16,6)
    Jeu.hero.lance_case = Case(16,6)
    print(Jeu.hero.lance_case)
    print(Jeu.hero.case)
    Jeu.attack_hero_lance(Case_lancer)
    print(Jeu.hero.lance_case, "est la case de la lance'")
    print(Jeu.hero.lance_etat,"est l'état de la lance'")
    
    # # Test de la fonction sauter du heros
    
    Case_saut = Case(13,3)
    Jeu.hero.case = Case(13,5)
    print(Jeu.hero.case)
    Jeu.sauter_hero(Case_saut)
    print(Jeu.hero.case,"est la case après saut du héros")
    
    # # Test de la fonction move demons et attack demons
    
    demon = choice(Jeu.demons)
    print(demon)
    Jeu.move_demons()
    Jeu.attack_demons()
    print(Jeu.hero.pv,"est le PV actuel du heros")
    print(demon)
    
    
    # # Test de la fonction move archer
    
    archer = choice(Jeu.archers)
    print(archer)
    Jeu.move_archer(archer)
    Jeu.attack_archer(archer)
    print(archer)
    print(Jeu.hero)



    


    
    
    