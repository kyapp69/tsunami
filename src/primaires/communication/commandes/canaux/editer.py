# Copyright (c) 2010-2016 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'editer' de la commande 'canaux'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmEditer(Parametre):
    
    """Commande 'canaux editer <canal>'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "editer", "edit")
        self.schema = "<canal>"
        self.aide_courte = "éditer un canal"
        self.aide_longue = \
            "Cette sous-commande permet d'éditer un canal : description, " \
            "couleur..."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        if not dic_masques["canal"].canal_existe:
            personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
        else:
            canal = dic_masques["canal"].canal
            if not personnage in canal.moderateurs and \
                    personnage is not canal.auteur and not \
                    personnage.est_immortel():
                personnage << "|err|Vous n'avez pas accès à cette option.|ff|"
            elif not personnage in canal.connectes:
                personnage << "|err|Vous n'êtes pas connecté à ce canal.|ff|"
            else:
                editeur = type(self).importeur.interpreteur.construire_editeur(
                    "chedit", personnage, canal)
                personnage.contextes.ajouter(editeur)
                editeur.actualiser()
