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


"""Fichier contenant la classe Quete détailéle plus bas."""

import re
from datetime import datetime

from abstraits.id import ObjetID
from bases.collections.liste_id import ListeID
from primaires.format.description import Description
from .etape import Etape

# Constantes
RE_QUETE_VALIDE = re.compile(r"^[a-z][a-z0-9_]*$")

class Quete(ObjetID):
    
    """Classe définissant une quête dans le sscripting.
    
    Une quête est constituée d'une suite d'étapes.
    
    Chaque étape peut être :
        une étape simple de scripting (Etape)
        une autre quête (Quete)
        un embranchement (Embranchement)
    
    L'étape simple est une étape menant à une suite d'instructions.
    Une sous-quête possède les mêmes propriétés que ceux définis ici.
    Un embranchement permet de matérialiser un choix dans la quête.
    
    """
    
    groupe = "quete"
    sous_rep = "scripting/quetes"
    def __init__(self, cle, auteur, parent=None, niveau=(1, )):
        """Constructeur de la quête."""
        ObjetID.__init__(self)
        self.cle = cle
        self.niveau = niveau
        self.auteur = auteur
        self.parent = parent
        self.date_creation = datetime.now()
        self.titre = "une quête anonyme"
        self.description = Description(parent=self)
        self.ordonnee = True
        self.__etapes = ListeID(self)
        self._construire()
    
    def __getnewargs__(self):
        return ("", None)
    
    def __str__(self):
        return self.cle + " par " + \
                (self.auteur and self.auteur.nom or "inconnu")
    
    def __getitem__(self, niveau):
        """Retourne l'étape."""
        for etape in self.__etapes:
            if etape.str_niveau == niveau:
                return etape
        
        raise KeyError(niveau)
    
    @property
    def etapes(self):
        return list(self.__etapes)
    
    @property
    def str_niveau(self):
        return ".".join([str(n) for n in self.niveau])
    
    @property
    def sous_niveau(self):
        if self.parent:
            return self.niveau + (len(self.__etapes) + 1, )
        else:
            return (len(self.__etapes) + 1, )
        
    def ajouter_etape(self, titre):
        """Ajoute l'étape à la quête."""
        etape = Etape(self)
        etape.titre = titre
        etape.niveau = self.sous_niveau
        self.__etapes.append(etape)
        self.enregistrer()
    
    def ajouter_sous_quete(self, titre):
        """Ajoute une sous-quête à la quête."""
        etape = Quete(self.cle, self.auteur, self)
        etape.titre = titre
        etape.niveau = self.sous_niveau
        self.__etapes.append(etape)
        self.enregistrer()
    
    def afficher_etapes(self):
        """Affiche les étapes qui peuvent être aussi des sous-quêtes."""
        res = ""
        if self.parent:
            res += self.str_niveau.ljust(5) + " " + self.titre + "\n"
        for etape in self.etapes:
            res += etape.afficher_etapes()
            res += "\n"
        
        return res.rstrip("\n")


ObjetID.ajouter_groupe(Quete)
