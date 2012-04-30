﻿# -*-coding:Utf-8 -*

# Copyright (c) 2012 NOEL-BARON Léo
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


"""Ce fichier définit le cherchable des objets.

"""

from primaires.recherche.cherchables.cherchable import Cherchable

class CherchableObjet(Cherchable):
    
    """Classe cherchable pour les objets de l'univers.
    
    """
    
    nom_cherchable = "objet"
    
    def init(self):
        """Méthode d'initialisation.
        
        C'est ici que l'on ajoute réellement les filtres, avec la méthode
        dédiée.
        
        """
        self.ajouter_filtre("n", "nom", "nom_singulier", "str")
        self.ajouter_filtre("l", "cle", "cle", "str")
        self.ajouter_filtre("i", "ident", "identifiant", "str")
        self.ajouter_filtre("t", "type", self.test_type, "str!")
    
    @property
    def items(self):
        """Renvoie la liste des objets traités"""
        return list(importeur.objet.objets.values())
    
    @property
    def attributs_tri(self):
        """Renvoie la liste des attributs par lesquels on peut trier"""
        return ["identifiant", "cle", "nom"]
    
    @property
    def colonnes(self):
        """Retourne un dictionnaire des valeurs que l'on peut disposer en
        colonne à l'affichage final, de la forme :
        >>> {nom: attribut/méthode}
        (une colonne peut être remplie par une méthode du cherchable).
        
        """
        return {"ident":"identifiant", "nom":"nom_singulier", "cle":"cle"}
    
    def afficher(self, objet):
        """Méthode d'affichage standard des objets traités"""
        return objet.identifiant + " : " + objet.nom_singulier
    
    def test_type(self, objet, valeur):
        """Permet une recherche sur le type de l'objet. Le type spécifié
        doit être un type valide et existant ; si l'objet est de ce type ou
        d'un de ses fils, il sera retourné à la recherche (cette option
        n'accepte pas les regex).
        
        """
        try:
            return objet.est_de_type(valeur)
        except KeyError:
            return False