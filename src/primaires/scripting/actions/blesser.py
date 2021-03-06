# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Fichier contenant l'action blesser."""

from primaires.scripting.action import Action
from primaires.perso.exceptions.stat import DepassementStat

class ClasseAction(Action):

    """Blesse un personnage.

    Cette action ôte des points de vitalité au personnage spécifié. Bien
    entendu, si sa vitalité passe à 0, le personnage meurt."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.blesser_personnage, "Personnage", "Fraction")
        cls.ajouter_types(cls.avec_adversaire, "Personnage",
                "Personnage", "Fraction")

    @staticmethod
    def blesser_personnage(personnage, valeur):
        """Enlève au personnage la valeur précisée en points de vie."""
        try:
            personnage.stats.vitalite = personnage.stats.vitalite - int(valeur)
        except DepassementStat:
            personnage.mourir()

    @staticmethod
    def avec_adversaire(auteur, victime, valeur):
        """Blesse la victime en déclarant auteur comme l'adversaire.

        Cette action est particulièrement utile si vous voulez induire
        des dégâts qui doivent provenir d'un autre personnage, présent ou non.

        Paramètres à préciser :

          * auteur : le personnage à l'auteur des dégâts
          * victime : le personnage victime des dégâts
          * valeur : la quantité de dégâts.

        """
        try:
            victime.stats.vitalite = victime.stats.vitalite - int(valeur)
        except DepassementStat:
            victime.mourir(adversaire=auteur, recompenser=False)
