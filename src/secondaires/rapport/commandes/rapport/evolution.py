﻿# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Package contenant le paramètre 'feature' de la commande 'rapport'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.interpreteur.editeur.presentation import Presentation

class PrmEvolution(Parametre):
    
    """Commande 'rapport feature'"""
    
    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "evolution", "feature")
        self.groupe = "joueur"
        self.schema = "<message>"
        self.aide_courte = "crée une suggestion"
        self.aide_longue = \
            "Cette commande permet d'envoyer une idée d'amélioration du " \
            "jeu au point de vue code et fonctionnalités." \
            "Vous devez préciser en argument le titre du rapport " \
            "à créer. Un éditeur s'ouvrira alors pour vous permettre " \
            "de renseigner plus précisément l'amélioration."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        titre = dic_masques["message"].message
        rapport = importeur.rapport.creer_rapport(titre, personnage,
                ajouter=False)
        rapport.type = "évolution"
        editeur = importeur.interpreteur.construire_editeur(
                "bugedit", personnage, rapport)
        personnage.contextes.ajouter(editeur)
        editeur.actualiser()