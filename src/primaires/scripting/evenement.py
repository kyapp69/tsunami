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


"""Fichier contenant la classe Evenement détaillée plus bas."""

from abstraits.obase import *
from .espaces import Espaces
from .tests import Tests
from .variable import Variable

class Evenement(BaseObj):
    
    """Classe contenant un évènement de scripting.
    
    Un évènement est appelé dans une certaine situation. Un cas classique,
    par exemple, est un script définit dans un PNJ. Un évènement pourrait
    être appelé quand le PNJ est attaqué.
    
    Les évènements peuvent contenir des sous-évènements.
    
    Au niveau de la structure, un évènement contient :
    *   un dictionnaire de variables qui doivent IMPERATIVEMENT être
        TOUTES RENSEIGNEES quand on l'appelle
    *   un dictionnaire pouvant contenir des sous-évènements
    *   une suite de tests
    *   plusieurs espaces de nom
    
    En outre, l'évènement garde en mémoire le script dont il est issu,
    qu'il soit sous-évènement ou non.
    
    Un évènement est constitué de plusieurs conditions (ou tests). Ces
    conditions sont propres aux variables qui les définissent. Un exemple
    simple :
        Evènement donner du PNJ tavernier_picte
            1   objet = pot_biere et nombre > 1
        La condition ci-dessus est appelée si le joueur donne plus d'un
        pot de bière au tavernier. Cela permet de ranger plus facilement
        nos lignes de script en fonction de plusieurs variables.
    
    Les évènements n'ayant aucune variable définie n'ont pas cette
    distinction en condition pour le bâtisseur. Du point de vue
    du code, ils ont une seule condition appelée automatiquement.
    
    Les espaces de nom sont présents dans l'attribut 'espaces'.
    Chaque attribut de cet objet 'Espaces' est un espace de nom différent.
    Chaque espace se manipule comme un dictionnaire.
    
    Le constructeur d'un évènement prend en paramètre :
        script -- le script qui possède l'évènement
        nom -- le nom de l'évènement
        parent -- si c'est un sous-évènement, l'évènement parent (optionnel)
    
    """
    
    def __init__(self, script, nom, parent=None):
        """Constructeur d'un évènement"""
        BaseObj.__init__(self)
        self.script = script
        self.nom = nom
        self.aide_courte = "non précisée"
        self.aide_longue = "non précisée"
        self.parent = parent
        self.variables = {}
        self.__evenements = {}
        self.__tests = []
        self.espaces = Espaces(self)
        self._construire()
    
    def __getnewargs__(self):
        return (None, "")
    
    def __getstate__(self):
        """Ne sauvegarde pas les variables en fichier."""
        dico_attr = BaseObj.__getstate__(self).copy()
        del dico_attr["variables"]
        return dico_attr
    
    @property
    def appelant(self):
        """Retourne l'appelant, c'est-à-dire le parent du script."""
        return self.script.parent
    
    @property
    def tests(self):
        """Retourne une liste déréférencée des tests."""
        return list(self.__tests)
    
    def ajouter_test(self, chaine_tests):
        """Ajoute un test à l'évènement.
        
        La chaîne de test est une liste de tuples de trois éléments.
        *   la variable testée (objet par exemple)
        *   l'opérateur (=, <=, ...)
        *   la valeur
        
        Ces trois informations doivent être des chaînes de caractères.
        
        L'opérateur est identifié en fonction de la syntaxe du script
        définie dans la configuration.
        
        """
        # On construit un test
        tests = Tests(self)
        tests.construire(chaine_tests)
        self.__tests.append(tests)
        self.appelant.enregistrer()
        return len(self.__tests) - 1
    
    def supprimer_testst(self, indice):
        """Retire le test à l'indice spécifiée."""
        del self.__tests[indice]
        self.appelant.enregistrer()
    
    def ajouter_variable(self, nom, type):
        """Ajoute une variable au dictionnaire des variables.
        
        On précise :
        nom -- le nom (ne doit pas être déjà utilisé)
        type -- le nom du type sous la forme d'une chaîne de caractère
        
        """
        if nom in self.variables:
            raise ValueError("la variable {} existe déjà dans cet " \
                    "évènement".format(nom))
        
        variable = Variable(self, nom, type)
        self.variables[nom] = variable
        
        return variable
