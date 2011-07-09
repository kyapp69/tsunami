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


"""Fichier contenant le masque <nom_objet>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import *

class NomObjet(Masque):
    
    """Masque <nom_objet>.
    On attend un nom d'objet en paramètre.
    
    """
    
    nom = "nom_objet"
    nom_complet = "nom d'un objet"
    
    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.proprietes["conteneurs"] = "(personnage.salle.objets_sol, )"
    
    def init(self):
        """Initialisation des attributs"""
        self.objets = []
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques, commande)
        nom = liste_vers_chaine(commande).lstrip()
        
        if not nom:
            raise ErreurValidation( \
                "Précisez un nom d'objet.")
        
        conteneurs = self.conteneurs
        objets = []
        
        for c in conteneurs:
            for o in c:
                if contient(o.nom_singulier, nom):
                    objets.append((o, c))
        
        if not objets:
            raise ErreurValidation(
                "|err|Ce nom d'objet est introuvable.|ff|")
        
        self.objets = objets
        
        return True