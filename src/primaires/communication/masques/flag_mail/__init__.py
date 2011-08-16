﻿# -*-coding:Utf-8 -*

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


"""Fichier contenant le masque <flag_mail>."""

from primaires.format.fonctions import supprimer_accents
from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation

class FlagMail(Masque):
    
    """Masque <flag_mail>.
    On attend un flag de filtre en paramètre.
    
    """
    
    nom = "flag_mail"
    nom_complet = "flag de filtre"
    
    def init(self):
        """Initialisation des attributs"""
        self.flag = ""
    
    def valider(self, personnage, dic_masques, commande):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques, commande)
        lstrip(commande)
        nom_flag = liste_vers_chaine(commande)
        
        if not nom_flag:
            raise ErreurValidation( \
                "Précisez un flag de filtre.")
        
        liste_flags = ["recus", "brouillons", "archives", "envoyes"]
        
        nom_flag = nom_flag.split(" ")[0]
        commande[:] = commande[len(nom_flag):]
        
        if not supprimer_accents(nom_flag.lower()) in liste_flags:
            raise ErreurValidation( \
                "|err|Le flag précisé n'existe pas.|ff|")
        
        self.flag = nom_flag
        return True
