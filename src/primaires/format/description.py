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


"""Fichier contenant la classe Description, détaillée plus bas."""

from textwrap import wrap

from .fonctions import *

# Constantes
TAILLE_LIGNE = 75

class Description:
    
    """Cette classe définit une description générique.
    Ce peut être une description de salle, d'objet, de balise, de
    véhicule...
    
    Elle propose plusieurs méthodes facilitant son déploiement dans un
    éditeur et sa mise en forme.
    
    """
    
    def __init__(self, description, parent=None):
        """Constructeur"""
        self.paragraphes = [] # une liste des différents paragraphes
        self.parent = parent
        self.ajouter_paragraphe(description)
    
    def __str__(self):
        """Retourne la description sous la forme d'un texte 'str'"""
        res = ""
        for paragraphe in self.paragraphes:
            paragraphe = self.wrap_paragraphe(paragraphe)
            if res.endswith("|nl|") or res == "":
                res += paragraphe
            else:
                res += " " + paragraphe
        
        res = res.replace("|nl|", "\n")
        return res
    
    def ajouter_paragraphe(self, paragraphe):
        """Ajoute un paragraphe.
        Si le paragraphe contient des sauts de lignes |nl|, on le découpe
        en plusieurs paragraphes.
        
        """
        for ligne in paragraphe.split("|nl|"):
            if ligne:
                if self.paragraphes and not self.paragraphes[-1].endswith(
                        "|nl"):
                    self.paragraphes[-1] += "|nl|"
                self.paragraphes.append(ligne)
        
        if self.parent:
            self.parent.enregistrer()
    
    def supprimer_paragraphe(self, no):
        """Supprime le paragraphe #no"""
        del self.paragraphes[no]
        if self.parent:
            self.parent.enregistrer()
    
    def vider(self):
        """Supprime toute la description"""
        self.paragraphes[:] = []
        if self.parent:
            self.parent.enregistrer()
    
    def remplacer(self, origine, par):
        """Remplace toutes les occurences de 'origine' par 'par'.
        Cette recherche & remplacement se fait dans tous les paragraphes.
        Le remplacement ne tient compte ni des majuscules, ni des accents.
        
        """
        diff = len(origine) - len(par)
        for i, paragraphe in enumerate(self.paragraphes):
            paragraphe = sup_accents(paragraphe).lower()
            # On cherche 'origine'
            no_car = paragraphe.find(origine)
            nb_passage = 0
            while no_car >= 0:
                no_car_o = no_car + diff * nb_passage
                self.paragraphes[i] = self.paragraphes[i][:no_car] + \
                        par + self.paragraphes[i][no_car + len(origine):]
                no_car = paragraphe.find(origine, no_car + 1)
                nb_passage += 1
        
        if self.parent:
            self.parent.enregistrer()
    
    def wrap_paragraphe(self, paragraphe, lien="\n", cvt_tab=True):
        """Wrap un paragraphe et le retourne"""
        if cvt_tab:
            paragraphe = paragraphe.replace("|tab|", "   ")
        return lien.join(wrap(paragraphe, TAILLE_LIGNE))
    
    @property
    def paragraphes_indentes(self):
        """Retourne les paragraphes avec une indentation du niveau spécifié"""
        indentation = "\n   "
        res = ""
        for paragraphe in self.paragraphes:
            paragraphe = self.wrap_paragraphe(paragraphe, lien=indentation)
            if res.endswith("|nl|") or res == "":
                res += paragraphe
            else:
                res += " " + paragraphe
        
        res = res.replace("|nl|", indentation)
        return indentation + res
