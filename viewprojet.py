# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 17:17:42 2020

@author: Neeb Olivier
"""


# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:42:06 2020

@author: Neeb Olivier

View du jeu Hoplite

"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from copy import * 
 
import sys 
import math



from random import *

from modelprojet import *
from controlerprojet import *
 
path = "images hoplite/"


class ma_scene(QGraphicsScene):
    def __init__(self,parent,controler):
        super().__init__(parent) 
        self.controler = controler 
        self.controler.add_clients(self)
        self.setSceneRect(0,0,600,800) # taille du canevas
        self.case_cliquee = Case(100,100) 
        # case hors de portée de tout archer, ne peut pas être initialisé à None






    def refresh(self): 
        self.clear()
        print(f'le heros est en {self.controler.hero.case}')

        self.message_erreur = " "
        
        # Point de départ du tracé du 1 hexagonne, le 1er en haut à gauche
        depart_x = 0
        depart_y = 200
        depart = QPoint(depart_x ,depart_y) 
    
        # Caractéristiques de l'hexagone
        #  A partir d'une capture d'écran du jeu, l'hexagone a comme dimensions:
        #  h=55 pixels, a=25, et largeur hexagone = 5a, 
        #  on obtient le ratio 2.2=55/25 qui relie h et a pour avoir des hexagones de la "même forme" que dans le jeu
        
        hauteur=30 # demi-hauteur, cad longueur entre le centre et le coté au dessus
        largueur_5e=hauteur/2.2 # variable correspondant au 5e de la largeur de l'hexagone, utile pour tracer les coins de l'hexagone
        self.largueur_5e = hauteur/2.2 # utilisé dans MousePressEvent pour savoir si l'endroit cliquée correspond à une case du plateau
        
        
        poly1 = QPolygonF( [ depart, 
                            QPoint(depart_x+largueur_5e   , depart_y-hauteur), 
                            QPoint(depart_x+4*largueur_5e , depart_y-hauteur),
                            QPoint(depart_x+5*largueur_5e , depart_y        ),  
                            QPoint(depart_x+4*largueur_5e , depart_y+hauteur),
                            QPoint(depart_x+largueur_5e   , depart_y+hauteur),
                            depart ] );
                           
        nb_ligne_par_colonne=[7,8,9,10,11,10,9,8,7] # de la colonne gauche à droite  
        
        l_polygones = [] # liste de poly (qui est une liste de taille 3) 
        # où poly est une liste de 3 éléments : un objet Case, un Qpolygon, un Qpoint 
        # correspondant à une case du plateau, son QPolygon correctement placé dans la scene, et le centre de ce QPolygon dans la scene
        
        for case in self.controler.plateau.plateau_complet: # plat.plateau_complet est une liste de cases
            q_poly = poly1.translated((case.y-1)*4*largueur_5e ,(17-case.x)*hauteur) # poly1 translaté à la position de la case correspondante
            
            rect_conscrit = q_poly.boundingRect() #  rectangle encadrant le polygone, pour après trouver le centre du polygone 
            centre = rect_conscrit.center()
            
            # on regroupe la case correspondante au polygone translaté, le QPolygon, et son centre 
            poly = [ deepcopy(case) , # changer et mettre poly = [deepcopy(case), ...]
                     q_poly,
                     centre ]
            
            l_polygones.append (poly)
            case.centre = deepcopy(centre) # affecte le centre de la case dans plateau_complet uniquement
            
        self.addPolygon(poly1)

        # Dessin Plateau + Personnages
        for poly in l_polygones:
            
            
            
            # Dessin cases mortes en rouges
            case_atteignable = True
            for case in self.controler.plateau.cases_mortes :
                if poly[0] == case:
                    case_atteignable = False
            
            if case_atteignable:
                self.addPolygon(poly[1])
                
            else:
                self.addPolygon(poly[1],QPen(), QBrush(Qt.red)) # peint le QPolygon en rouge si case mort
            
            # Dessin du centre de la case sur la scene
            centre = poly[2] # centre est un QPointF
            point_central =QPolygonF( [QPoint(centre.x(), centre.y()),
                                  QPoint(centre.x() +1 , centre.y()) ])
            self.addPolygon(point_central) # trace le point central du polygon
            
            
        
            
            # Dessin des Personnages sur les cases 
            
            
                # dessin du héros 
            if poly[0] == self.controler.hero.case:
                # on va chercher la position du coin haut gauche par rapport au centre du polygone
                # afin de centrer le héros dans le polygone 
                # pour cela, on va encadrer l'image du heros un rectangle, puis recuperer sa hauteur et sa largeur 
                # puis on place le coin_haut_gauche en (centre.x - largeur/2, centre.y - hauteur/2)
                
                if self.controler.hero.lance_etat:
                    pixmap = QPixmap(path +"heros_avec_lance.png") # 2 dessins du heros possibles, avec ou sans lance sur lui
                else:
                    pixmap = QPixmap(path + "heros_sans_lance.png")
                    
                self.image_hero = self.addPixmap(pixmap)
                rect_entourant = self.image_hero.boundingRect()
                width = rect_entourant.width()
                height = rect_entourant.height()
                pos_x_coin_haut_gauche = poly[2].x()-width/2
                pos_y_coin_haut_gauche = poly[2].y()-height/2
                    
                self.image_hero.setPos(pos_x_coin_haut_gauche,pos_y_coin_haut_gauche)
            
                # dessin de la lance par terre
            elif (not self.controler.hero.lance_etat) and poly[0] == self.controler.hero.lance_case:
                 
                pixmap = QPixmap(path + "lance_au_sol.png")
                self.image_lance_sol = self.addPixmap(pixmap)
                rect_entourant = self.image_lance_sol.boundingRect()
                width = rect_entourant.width()
                height = rect_entourant.height()
                pos_x_coin_haut_gauche = poly[2].x()-width/2
                pos_y_coin_haut_gauche = poly[2].y()-height/2
                    
                self.image_lance_sol.setPos(pos_x_coin_haut_gauche,pos_y_coin_haut_gauche)
                
                # dessin des demons 
            elif poly[0] in [demon.case for demon in self.controler.demons]:
                
                pixmap = QPixmap(path +"demon.png")
                self.image_demon = self.addPixmap(pixmap)
                rect_entourant = self.image_demon.boundingRect()
                width = rect_entourant.width()
                height = rect_entourant.height()
                pos_x_coin_haut_gauche = poly[2].x()-width/2
                pos_y_coin_haut_gauche = poly[2].y()-height/2
                    
                self.image_demon.setPos(pos_x_coin_haut_gauche,pos_y_coin_haut_gauche)
            
                # dessin des archers
            elif poly[0] in [archer.case for archer in self.controler.archers]:
                 
                pixmap = QPixmap(path + "archer.png")
                self.image_archer = self.addPixmap(pixmap)
                rect_entourant = self.image_archer.boundingRect()
                width = rect_entourant.width()
                height = rect_entourant.height()
                pos_x_coin_haut_gauche = poly[2].x()-width/2
                pos_y_coin_haut_gauche = poly[2].y()-height/2
                    
                self.image_archer.setPos(pos_x_coin_haut_gauche,pos_y_coin_haut_gauche)
            
            
            
            
            # Dessin portée saut ou lance après clic sur bouton saut ou lance
                
                # Dessin portée saut
                    # Si le héros veut sauter, on va un hexagone vert sur chaque case où le saut est possible
            if self.controler.action == 2 and self.controler.hero.sauter >= 50:
                
                
                if self.controler.hero.case_a_portee_saut(poly[0]) and case_atteignable :
                    # Dimension de l'hexagone réduit
                    pixels_retires = 2 # on veut tracer un hexagone vert, avec chaque coin à 2 pixels de l'hexagone dessinant la case
                    alpha = largueur_5e - pixels_retires # largeur_5e plus petite de  pixels_retires
                    hauteur = 2.2*alpha # demi-hauteur modifiée, car alpha != largeur_5e
                    
                    
                    centre = poly[2]
                    depart_poly = QPoint(centre.x() - 2.5*alpha, centre.y())
                    depart_x = depart_poly.x()
                    depart_y = depart_poly.y()
                
                    
                    poly_reduit = QPolygonF( [ depart_poly, 
                            QPoint(depart_x+alpha   , depart_y-hauteur ), 
                            QPoint(depart_x+4*alpha , depart_y-hauteur ),
                            QPoint(depart_x+5*alpha , depart_y ),  
                            QPoint(depart_x+4*alpha , depart_y+hauteur ),
                            QPoint(depart_x+alpha   , depart_y+hauteur),
                            depart_poly ] );
                           
                    self.addPolygon(poly_reduit,QPen(Qt.green,3))
                    
                # Dessin portée lance
            if self.controler.action == 3 and self.controler.hero.lance_etat and case_atteignable :
                
                if self.controler.hero.case_a_portee_lance(poly[0]):
                    pixels_retires = 2
                    alpha = largueur_5e - pixels_retires
                    hauteur = 2.2*alpha
                    
                    centre = poly[2] 
                    depart_poly = QPoint(centre.x() - 2.5*alpha, centre.y())
                    depart_x = depart_poly.x()
                    depart_y = depart_poly.y()
                    
                    poly_reduit = QPolygonF( [ depart_poly, 
                            QPoint(depart_x+alpha   , depart_y-hauteur ), 
                            QPoint(depart_x+4*alpha , depart_y-hauteur ),
                            QPoint(depart_x+5*alpha , depart_y ),  
                            QPoint(depart_x+4*alpha , depart_y+hauteur ),
                            QPoint(depart_x+alpha   , depart_y+hauteur),
                            depart_poly ] );
                           
                    self.addPolygon(poly_reduit,QPen(Qt.green,3))
                    
                    
            # Dessin portée d'un archer ou un démon quand on clique dessus        
            
                # Dessin portée Archer
                    # Le joueur clique sur un archer sur le plateau et voudrait afficher sa portée (les cases qu'il peut attaquer)
                    # On affiche alors un hexagone jaune dans chaque case que l'archer peut atteindre 
            if self.controler.archers and not self.controler.action_dep_possible( self.controler.action,self.case_cliquee):
                # Si il y a des archers, et que le joueur clique sur une case où il ne peut pas se déplacer 
                
                if self.case_cliquee in [archer.case for archer in self.controler.archers]:
                    # Si il y a un archer sur la case_cliquée
                    
                    archer = self.controler.archers[ [archer.case for archer in self.controler.archers].index(self.case_cliquee) ]
                    # On récupère l'archer sur lequel on vient de cliquer
                    
                    if archer.heros_a_portee_archer(poly[0] ):
                    # Si la case qu'on dessine est en portée de l'archer cliqué, on dessine l'hexagone jaune 
                        
                        pixels_retires = 2
                        alpha = largueur_5e - pixels_retires
                        hauteur = 2.2*alpha
                        
                        centre = poly[2] 
                        depart_poly = QPoint(centre.x() - 2.5*alpha, centre.y())
                        depart_x = depart_poly.x()
                        depart_y = depart_poly.y()
                        
                        poly_reduit = QPolygonF( [ depart_poly, 
                                QPoint(depart_x+alpha   , depart_y-hauteur ), 
                                QPoint(depart_x+4*alpha , depart_y-hauteur ),
                                QPoint(depart_x+5*alpha , depart_y ),  
                                QPoint(depart_x+4*alpha , depart_y+hauteur ),
                                QPoint(depart_x+alpha   , depart_y+hauteur),
                                depart_poly ] );
                        
                        self.addPolygon(poly_reduit,QPen(Qt.yellow,3))
                        
                # Dessin portée Démon
            if self.controler.demons and not self.controler.action_dep_possible( self.controler.action,self.case_cliquee):
                if self.case_cliquee in [demon.case for demon in self.controler.demons]:
                    demon = self.controler.demons[ [demon.case for demon in self.controler.demons].index(self.case_cliquee) ]
                    
                    if demon.heros_a_portee_demon(poly[0]):
                        
                        pixels_retires = 2
                        alpha = largueur_5e - pixels_retires
                        hauteur = 2.2*alpha
                        
                        centre = poly[2] 
                        depart_poly = QPoint(centre.x() - 2.5*alpha, centre.y())
                        depart_x = depart_poly.x()
                        depart_y = depart_poly.y()
                        
                        poly_reduit = QPolygonF( [ depart_poly, 
                                QPoint(depart_x+alpha   , depart_y-hauteur ), 
                                QPoint(depart_x+4*alpha , depart_y-hauteur ),
                                QPoint(depart_x+5*alpha , depart_y ),  
                                QPoint(depart_x+4*alpha , depart_y+hauteur ),
                                QPoint(depart_x+alpha   , depart_y+hauteur),
                                depart_poly ] );
                        
                        self.addPolygon(poly_reduit,QPen(Qt.yellow,3))

   
        # Dessin des caractéristiques du héros 
            
            # Dessin PV du héros
                        
        coeur_plein = QPixmap(path + "coeur_plein.png")
        coeur_vide = QPixmap(path+ "coeur_vide.png")
        nb_coeur_plein = self.controler.hero.pv
        nb_coeur_vide = self.controler.hero.pv_max - self.controler.hero.pv
        self.image_coeur_plein = self.addPixmap(coeur_plein)
        self.image_coeur_plein.setPos(0,742) # c'est pour tester la position des coeurs
        # il sera écrasé par le dessin des coeurs suivants , ce n'est pas grave 
        
        rect_entourant = self.image_coeur_plein.boundingRect() # on suppose img coeur_plein même taille que image coeur vide
        largeur_coeur =  rect_entourant.width() 
        espace_coeur = 5 # nombre de pixels entre chaque coeur
        
        for i in range(self.controler.hero.pv_max ):
            if i+1 <= nb_coeur_plein: # dessin des coeurs pleins 
                self.image_coeur_plein = self.addPixmap(coeur_plein)
                self.image_coeur_plein.setPos(i*largeur_coeur + i*espace_coeur,742)
                # l'espace entre 2 coins haut gauche de 2 coeurs consécutifs = largueur_coeur + espace_coeur
            
            else: # dessin des coeurs vides 
                self.image_coeur_vide = self.addPixmap(coeur_vide)
                self.image_coeur_vide.setPos(i*largeur_coeur + i*espace_coeur,742)
            
            
            
            # Dessin valeur de l'énergie du héros pour sauter 
                
        energie = str(self.controler.hero.sauter) 
        message_energie = "Energie restante pour sauter \nSaut possible si energie >=50 \n" + energie
        font = QFont('Arial',12, QFont.Bold)
        self.message_energie= self.addSimpleText(message_energie,font)
        self.message_energie.setPos(420,740) 
        
        self.case_cliquee=Case(100,100) 
        # on réinitialise self.case_cliquee pour eviter l'affichage de la portée d'un ennemi,
        # si il est sur la derniere case cliquée puis qu'on appuie sur start

        
            
        
        
        
        
        
        

    def mousePressEvent(self,e):
        # On va calculer la distance entre la position cliquée et le centre de chaque case, 
        # et renvoyer la case où la distance est minimale et cette distance < 3a (on vérifie qu'on ne clique pas en dehors du plateau de jeu)
        
        if (not (self.controler.plateau)): # evite une erreur si on clique sur la scene avant d'avoir cliqué sur le bouton Start
            return
        
        x = e.scenePos().x()
        y = e.scenePos().y()
        dmin = math.inf
        
        # print(f'la position sur la scene est {x},{y}'), utile pour positionner des images comme coeur, texte de end_game()
        
        for case in self.controler.plateau.plateau_complet:
            # calcul de la distance entre le clic et chaque centre de case du plateau
            d_tempo = math.sqrt( (y - case.centre.y())**2 + (x - case.centre.x())**2 )
            if d_tempo < dmin:
                dmin = d_tempo
                self.case_cliquee = deepcopy(case)
        
        
        if dmin > 3* self.largueur_5e: # ici on a cliqué en dehors des cases du plateau
            self.message_erreur = "case en dehors du plateau"
            self.afficher_erreur(self.message_erreur)
            
        else:
            # print(f'{self.case_cliquee} est la case cliquee ')
            self.controler.next_game(self.controler.action, self.case_cliquee) 
            self.afficher_erreur(self.controler.message_erreur)
            

    def afficher_erreur(self,message): # affiche le message disant qu'une action est impossible dans le coin haut gauche de la scene
        font = QFont('Arial',12, QFont.Bold)
        self.message_erreur_clic_case = self.addSimpleText(message,font)
        self.message_erreur_clic_case.setPos(0,0)  
        
    def end_game(self):
        if self.controler.hero.pv <= 0:
            self.afficher_endgame('Defaite !')
        else : 
            self.afficher_endgame('Victoire !')
              
    def afficher_endgame(self,message): #affiche message au milieu de l'écran en grand
        font = QFont('Arial',100)
        self.message_erreur_clic_case = self.addSimpleText(message,font)
        self.message_erreur_clic_case.setPos(50,50)    
    
    
    
    
    
    

class Hoplite_view(QGraphicsView):
    def __init__(self,parent,controler):
        super().__init__(parent)
        self.scene = ma_scene(self,controler)
        self.setScene(self.scene)
        





class Hoplite_params(QWidget):
    def __init__(self,parent,controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.add_clients(self)
        
        # 3 QSpinBox pour le nombre de cases eessibles, le nombre de démons, le nombre d'archers
        self.nb_cases_mortes = QSpinBox()
        self.nb_demons = QSpinBox()
        self.nb_archers =QSpinBox()
        
        self.nb_cases_mortes.setValue(10)
        self.nb_cases_mortes.setMaximum(79)
        
        self.nb_demons.setValue(2)
        self.nb_demons.setMaximum(20)
        
        self.nb_archers.setValue(0)
        self.nb_archers.setMaximum(20)
        
        # 4 Boutons, pour Start le jeu, l'action Saut, l'action Lance, et un bouton pour annuler la sélection de l'action saut ou lance
        # seul Start est accessible au début de partie
        self.start_button = QPushButton('Start')
        self.bouton_saut = QPushButton('Saut')
        self.bouton_lance = QPushButton('Lance')
        self.bouton_annule = QPushButton('Annuler action Lance ou Saut ')
        
        self.bouton_saut.setEnabled(False)
        self.bouton_lance.setEnabled(False)
        self.bouton_annule.setEnabled(False)
        
        layout = QFormLayout()
        
        layout.addRow("Nombre cases mortes ", self.nb_cases_mortes)
        layout.addRow("Nombre demons" , self.nb_demons)
        layout.addRow("Nombre d'archers", self.nb_archers)
        layout.addRow(self.start_button)
        layout.addRow(self.bouton_saut)
        layout.addRow(self.bouton_lance)
        layout.addRow(self.bouton_annule)
        
        self.setLayout(layout)
        
        self.start_button.clicked.connect(self.on_start)
        self.bouton_saut.clicked.connect(self.on_bouton_saut)
        self.bouton_lance.clicked.connect(self.on_bouton_lance)
        self.bouton_annule.clicked.connect(self.on_bouton_annule)
        
        
        
        
    def refresh(self):
        # après chaque clique sur la scene, on refresh les actions possibles, comme Saut ou Lance du héros
        
        self.controler = self.controler
        
        # la partie a commencé, il faut activer les boutons pour les actions possibles du heros
        self.bouton_saut.setEnabled(True)
        self.bouton_lance.setEnabled(True)
        self.bouton_annule.setEnabled(True)
        
        # on teste ici si le héros a assez d'énergie pour sauter, sinon on disable le bouton saut
        self.test_sauter_possible()
        # on teste si le héros a sa lance
        self.test_lancer_possible()
        # on disable le bouton qui vient d'être pressé par le joueur, pour montrer qu'on est dans l'action Saut ou Lance
        self.disable_bouton_presse()
        

    def on_start(self):
        N = self.nb_cases_mortes.value()
        l_nb_ennemis = [self.nb_demons.value(), self.nb_archers.value()]
        self.controler.start( l_nb_ennemis, N)
    
    def on_bouton_saut(self):
        self.controler.action = 2
        self.controler.refresh_all()
        
    def on_bouton_lance(self):
        self.controler.action = 3
        self.controler.refresh_all()
    
    def on_bouton_annule(self):
        self.controler.action = 1
        self.controler.refresh_all()

    def test_sauter_possible(self):
        if self.controler.hero.sauter<50:
            self.bouton_saut.setEnabled(False)
        else: 
            self.bouton_saut.setEnabled(True)
    
    def test_lancer_possible(self):
        if self.controler.action ==1:
            if self.controler.hero.lance_etat:
                self.bouton_lance.setEnabled(True)
            else:
                self.bouton_lance.setEnabled(False)
    
    def disable_bouton_presse(self):
        if self.controler.action == 2:
            self.bouton_saut.setEnabled(False)
            
            if self.controler.hero.lance_etat:
                self.bouton_lance.setEnabled(True)
            else:
                self.bouton_lance.setEnabled(False)
        
        if self.controler.action == 3:
            self.test_sauter_possible()
            self.bouton_lance.setEnabled(False)
            
    def end_game(self): # n'affiche rien de spécial en fin de partie
        pass
        
    
    
    
    
    

class widget_ensemble(QWidget):
    def __init__(self,parent,controler):
        super().__init__(parent)
        view = Hoplite_view(self,controler)
        params = Hoplite_params(self,controler)
        
        layout = QHBoxLayout()
        layout.addWidget(params)
        layout.addWidget(view)
        self.setLayout(layout)
        
class MaFenetre(QMainWindow): # on derive de QMainWindow pour faire notre fenetre à nous 
    def __init__(self,controler):
        super().__init__() # va appeler le init de QMainWindow, appelé la superclasse 
        self.setWindowTitle('Hoplite the Game')
        self.setWindowIcon(QIcon(path + 'hoplite_icon.png'))
        self.setGeometry(200,200,1000,820) # ( x,  y,  width, height) de la fenetre
        # self.setWindowState(Qt.WindowMaximized) maximise la taille de la fenetre
        
        self.setCentralWidget(widget_ensemble(self,controler) ) 
        # widget central = widget_ensemble contenant les paramètres + la scene
        #  QMainWindow n'accepte qu'un seul widget central !
        
def main(): # instancie le controler + la fenetre 
    app = QApplication(sys.argv) # instance de l'application Qt 
    controler = hopliteControler()
    fenetre = MaFenetre(controler)
    fenetre.show()
    app.exec() # lancer l'app, qui va en continu traiter l'ensemble des commandes qui lui seront envoyés
     
     
if __name__ == '__main__':
    main()
    