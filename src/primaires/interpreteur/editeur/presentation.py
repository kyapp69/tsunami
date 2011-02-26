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
# pereIBILITY OF SUCH DAMAGE.


"""Ce fichier définit le contexte-éditeur 'présentation'."""

from collections import OrderedDict

from . import Editeur
from .quitter import Quitter
class Presentation(Editeur):
    
    """Contexte-éditeur présentation.
    Ce contexte présente un objet, c'est-à-dire qu'il va être à la racine
    des différentes manipulations de l'objet. C'est cet objet que l'on
    manipule si on souhaite ajouter des configurations possibles.
    
    """
    
    nom = "editeur:base:presentation"
    def __init__(self, pere, objet=None, attribut=None):
        """Constructeur de l'éditeur"""
        Editeur.__init__(self, pere, objet, attribut)
        self.choix = OrderedDict()
        self.raccourcis = {}
        self.ajouter_choix("quitter", "q", Quitter)
    
    def ajouter_choix(self, nom, raccourci, objet_editeur):
        """Ajoute un choix possible"""
        if raccourci in self.raccourcis.keys():
            raise ValueError(
                "Le raccourci {} est déjà utilisé dans cet éditeur".format(
                raccourci))
        
        self.choix[nom] = objet_editeur
        self.raccourcis[raccourci] = nom
    
    def supprimer_choix(self, nom):
        """Supprime le choix possible 'nom'"""
        # On recherche le raccourci pour le supprimer
        for cle, valeur in tuple(self.racourcis.items()):
            if valeur == nom:
                del self.raccourcis[cle]
        
        del self.choix[nom]
    
    def accueil(self):
        """Message d'accueil du contexte"""
        print("edt", self.objet)
        msg = "Edition de {}".format(self.objet)
        # Parcourt des choix possibles
        for raccourci, nom in self.raccourcis.items():
            # On constitue le nom final
            # Si le nom d'origine est 'description' et le raccourci est 'd',
            # le nom final doit être '(D)escription'
            pos = nom.find(raccourci)
            nom = nom[:pos] + "(|cmd|" + raccourci.upper() + \
                    "|ff|)" + nom[pos + len(raccourci):]
            msg += "\n" + nom
        
        return msg
    
    def interpreter(self, msg):
        """Interprétation de la présentation"""
        try:
            nom = self.raccourcis[msg.lower()]
        except KeyError:
            self.pere << "Raccourci inconnu {}".format(msg)
        else:
            objet = self.choix[nom](self.pere)
            objet.executer()
