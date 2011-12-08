# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant la classe Navire, détaillée plus bas."""

from math import fabs

from abstraits.id import ObjetID
from primaires.vehicule.force import Force
from primaires.vehicule.vecteur import Vecteur
from primaires.vehicule.vehicule import Vehicule
from .constantes import *
from .element import Element
from .salle import SalleNavire
from .vent import INFLUENCE_MAX

# Constantes
FACTEUR_MIN = 0.1

class Navire(Vehicule):
    
    """Classe représentant un navire ou une embarcation.
    
    Un navire est un véhicule se déplaçant sur une éttendue d'eau,
    propulsé par ses voiles ou des rameurs.
    
    Le navire est un véhicule se déplaçant sur un repère en 2D.
    
    Chaque navire possède un modèle (qui détermine ses salles, leurs
    descriptions, la position des éléments, leur qualité, l'aérodynamisme
    du navire...). Chaque navire est lié à son modèle en se créant.
    
    """
    
    groupe = "navire"
    sous_rep = "navires/navires"
    def __init__(self, modele):
        """Constructeur du navire."""
        Vehicule.__init__(self)
        self.propulsion = Propulsion(self)
        self.forces.append(self.propulsion)
        self.etendue = None
        self.immobilise = False
        if modele:
            self.modele = modele
            modele.vehicules.append(self)
            self.cle = "{}_{}".format(modele.cle, len(modele.vehicules))
            # On recopie les salles
            for r_coords, salle in modele.salles.items():
                n_salle = SalleNavire(self.cle,
                        salle.mnemonic, salle.r_x, salle.r_y, salle.r_z,
                        modele, self)
                n_salle.titre = salle.titre
                n_salle.description = salle.description
                
                # On recopie les éléments
                for t_elt in salle.elements:
                    elt = Element(t_elt)
                    n_salle.elements.append(elt)
                
                self.salles[r_coords] = n_salle
                type(self).importeur.salle.ajouter_salle(n_salle)
            
            # On recopie les sorties
            for salle in modele.salles.values():
                n_salle = self.salles[salle.r_coords]
                for dir, sortie in salle.sorties._sorties.items():
                    if sortie and sortie.salle_dest:
                        c_salle = self.salles[sortie.salle_dest.r_coords]
                        n_salle.sorties.ajouter_sortie(dir, sortie.nom,
                                sortie.article, c_salle,
                                sortie.correspondante)
    
    def __getnewargs__(self):
        return (None, )
    
    @property
    def elements(self):
        """Retourne un tuple des éléments."""
        elts = []
        for salle in self.salles.values():
            elts.extend(salle.elements)
        
        return tuple(elts)
    
    @property
    def voiles(self):
        """Retourne les éléments voiles du navire."""
        elts = self.elements
        return tuple(e for e in elts if e.nom_type == "voile")
    
    @property
    def passerelle(self):
        """Retourne True si la passerelle du navire est dépliée."""
        elts = [e for e in self.elements if e.nom_type == "passerelle"]
        if not elts:
            return False
        
        e = elts[0]
        return e.baissee
    
    @property
    def vent(self):
        """Retourne le vecteur du vent le plus proche.
        
        Il s'agit en fait d'un condensé des vents allentours.
        
        """
        vec_nul = Vecteur(0, 0, 0)
        
        if self.etendue is None:
            return vec_nul
        
        # On récupère le vent le plus proche
        vents = type(self).importeur.navigation.vents_par_etendue.get(
                self.etendue.cle, [])
        
        if not vents:
            return vec_nul
        
        # On calcul un vecteur des vents restants
        vecteur_vent = Vecteur(0, 0, 0)
        for vent in vents:
            distance = (vent.position - self.position).norme
            if distance < vent.longueur:
                facteur = 1
            elif distance < vent.longueur ** 2:
                facteur = 0.6
            else:
                facteur = 0.3
            
            vecteur_vent += facteur * vent.vitesse
        
        return vecteur_vent
    
    @property
    def nom_allure(self):
        """Retourne le nom de l'allure."""
        vent = self.vent
        allure = (self.direction.direction - vent.direction) % 360
        if ALL_DEBOUT < allure < (360 - ALL_DEBOUT):
            return "vent debout"
        elif ALL_PRES < allure < (360 - ALL_PRES):
            return "au près"
        elif ALL_BON_PLEIN < allure < (360 - ALL_BON_PLEIN):
            return "bon plein"
        elif ALL_LARGUE < allure < (360 - ALL_LARGUE):
            return "largue"
        elif ALL_GRAND_LARGUE < allure < (360 - ALL_GRAND_LARGUE):
            return "grand largue"
        else:
            return "vent arrière"

    def valider_coordonnees(self):
        """Pour chaque salle, valide ses coordonnées."""
        for salle in self.salles.values():
            if not salle.coords.valide:
                salle.coords.valide = True
    
    def vent_debout(self):
        """Retourne le facteur de vitesse par l'allure vent debout."""
        return 0
    
    def pres(self):
        """Retourne le facteur de vitesse par l'allure de près."""
        return 0.5
    
    def bon_plein(self):
        """Retourne le facteur de vitesse par l'allure de bon plein."""
        return 0.8
    
    def largue(self):
        """Retourne le facteur de vitesse par l'allure de largue."""
        return 1.2
    
    def grand_largue(self):
        """Retourne le facteur de vitesse par l'allure de grand largue."""
        return 0.9
    
    def vent_arriere(self):
        """Retourne le facteur de vitesse par l'allure par vent arrière."""
        return 0.7
    
    def maj_salles(self):
        d = self.direction.direction + 90
        i = self.direction.inclinaison
        operation = lambda v: self.position + v.tourner_autour_z(d).incliner(i)
        for vec, salle in self.salles.items():
            vec = Vecteur(*vec)
            vec = operation(vec)
            salle.coords.x = vec.x
            salle.coords.y = vec.y
            salle.coords.z = vec.z

    def avancer(self, temps_virtuel):
        """Fait avancer le navire si il n'est pas immobilisé."""
        if not self.immobilise:
            Vehicule.avancer(self, temps_virtuel)
    
    def envoyer(self, message):
        """Envoie le message à tous les personnages présents dans le navire."""
        for salle in self.salles.values():
            salle.envoyer(message)
    
    def detruire(self):
        """Destruction du self."""
        for salle in self.salles.values():
            salle.detruire()
        
        self.modele.vehicules.remove(self)
        Vehicule.detruire(self)


ObjetID.ajouter_groupe(Navire)

class Propulsion(Force):
    
    """Force de propulsion d'un navire.
    
    Elle doit être fonction du vent, du nombre de voile et de leur
    orientation.
    
    """
    
    def __init__(self, subissant):
        """Constructeur de la force."""
        Force.__init__(self, subissant)
    
    def __getnewargs__(self):
        return (None, )
    
    def calcul(self):
        """Retourne le vecteur de la force."""
        vec_nul = Vecteur(0, 0, 0)
        navire = self.subissant
        vent = navire.vent
        direction = navire.direction
        voiles = navire.voiles
        voiles = [v for v in voiles if v.hissee]
        if not voiles:
            return vec_nul
        
        fact_voile = sum(v.facteur_orientation(v, navire, vent) \
                for v in voiles) / len(voiles) * 0.7
        allure = (direction.direction - vent.direction) % 360
        if ALL_DEBOUT < allure < (360 - ALL_DEBOUT):
            facteur = navire.vent_debout()
        elif ALL_PRES < allure < (360 - ALL_PRES):
            facteur = navire.pres()
        elif ALL_BON_PLEIN < allure < (360 - ALL_BON_PLEIN):
            facteur = navire.bon_plein()
        elif ALL_LARGUE < allure < (360 - ALL_LARGUE):
            facteur = navire.largue()
        elif ALL_GRAND_LARGUE < allure < (360 - ALL_GRAND_LARGUE):
            facteur = navire.grand_largue()
        else:
            facteur = navire.vent_arriere()
        
        return facteur * fact_voile * vent.norme * direction
