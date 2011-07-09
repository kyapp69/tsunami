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


"""Fichier contenant la classe Sortie, détaillée plus bas;"""

from abstraits.obase import *

NOMS_VERS_ARTICLES = {
    "sud": "le",
    "sud-ouest": "le",
    "ouest": "l'",
    "nord-ouest": "le",
    "nord": "le",
    "nord-est": "le",
    "est": "l'",
    "sud-est": "le",
    "bas": "le",
    "haut": "le",
    
    # noms non usuels
    "porte": "la",
    "escalier": "l'",
}

class Sortie(BaseObj):
    
    """Cette classe définit une sortie.
    Une sortie possède au minimum un nom, un article et une salle de
    destination.
    
    """
    
    def __init__(self, direction, nom, article="le", salle_dest=None,
            corresp="", parent=None, modele=None):
        """Constructeur du conteneur
        Précision quant au parent :
        Ici, ce n'est pas le conteneur, mais la salle possédant la sortie
        qui doit être le parent.
        
        """
        BaseObj.__init__(self)
        if modele is not None:
            self.parent = modele.parent
            self.article = modele.article
            if not salle_dest:
                self.salle_dest = modele.salle_dest
            if not corresp:
                self.correspondante = modele.correspondante
        self.parent = parent
        self.direction = direction
        self.nom = nom
        self.article = article
        self.salle_dest = salle_dest
        self.correspondante = corresp # le nom de la sortie correspondante
        if article == "le":
            self.deduire_article()
        
        # Autres informations
        self.cache = False
        
        # On passe le statut en CONSTRUIT
        self._statut = CONSTRUIT
    
    def __str__(self):
        return self.nom
    
    def __getnewargs__(self):
        return ("", "")
    
    def __setattr__(self, nom_attr, valeur):
        """Enregisre le parent si il est précisé"""
        construit = self.construit
        BaseObj.__setattr__(self, nom_attr, valeur)
        if construit and self.parent:
            self.parent.enregistrer()
    
    def deduire_article(self):
        """Déduit l'article en fonction du nom de la sortie"""
        if self.nom in NOMS_VERS_ARTICLES.keys():
            self.article = NOMS_VERS_ARTICLES[self.nom]
        else:
            try:
                self.nom[0] in ["a", "e", "i", "o", "u"]
            except IndexError:
                self.article = "le"
            else:
                self.article = "l'"
    
    @property
    def nom_complet(self):
        """Retourne le nom et l'article"""
        sep = " "
        if self.article.endswith("'"):
            sep = ""
        
        return self.article + sep + self.nom
    
    @property
    def sortie_opposee(self):
        """Retourne la sortie opposée"""
        salle = self.salle_dest
        if salle and self.correspondante:
            corresp = salle.sorties[self.correspondante]
        else:
            corresp = None
        
        return corresp