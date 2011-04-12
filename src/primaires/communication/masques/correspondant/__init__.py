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


"""Fichier contenant le masque <id_corresp>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class Correspondant(Masque):
    
    """Masque <id_corresp>.
    On attend le numéro d'un correspondant (voir commande reply) en paramètre.
    
    """
    
    nom = "id_corresp"
    
    def __init__(self):
        """Constructeur du masque"""
        Masque.__init__(self)
        self.nom_complet = "id d'un correspondant"
        self.cible = None
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du masque"""
        lstrip(commande)
        id_corresp = liste_vers_chaine(commande).lstrip()
        corresp = type(self).importeur.communication.correspondants
        p_corresp = []
        cible = None
        for couple in corresp:
            if personnage == couple.emetteur:
                p_corresp.append(couple)
        
        if not id_corresp:
            raise ErreurValidation( \
                "Vous devez préciser le numéro d'un correspondant.")
        
        id_corresp = id_corresp.split(" ")[0]
        taille = len(id_corresp)
        try:
            id_corresp = int(id_corresp)
        except ValueError:
            self.id_corresp = None
            self.correspondant = None
            return True
        else:
            commande[:] = commande[taille:]
        
        if id_corresp < 1 or id_corresp > len(p_corresp):
            raise ErreurValidation( \
                "|err|Le numéro spécifié ne correspond à aucun personnage.|ff|")
        
        try:
            cible = p_corresp[id_corresp - 1].cible
        except IndexError:
            raise ErreurValidation( \
                "|err|Le numéro spécifié ne correspond à aucun personnage.|ff|")
        else:
            self.id_corresp = id_corresp
            self.correspondant = cible
            return True
