# -*-coding:Utf-8 -*

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


"""Package contenant la commande 'scripting exec'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.scripting.contextes.exec import Exec

class PrmExec(Parametre):

    """Commande 'scripting exec'"""

    def __init__(self):
        """Constructeur du paramètre."""
        Parametre.__init__(self, "exec", "exec")
        self.aide_courte = "entre dans la console scripting"
        self.aide_longue = \
            "Cette commande permet d'ouvrir la console scripting, " \
            "qui permet d'entrer du scripting à la volée et l'exécuter " \
            "tout de suite. L'avantage est de pouvoir tester certaines " \
            "manipulations, ainsi que faire des modifications à la " \
            "volée, comme changer les coordonnées de plusieurs salles, " \
            "les passer en intérieur, ou donner une affection à tous " \
            "les joueurs dans une zone, etc. C'est une commande " \
            "potentiellement aussi puissante que |cmd|système|ff|, et qu'il " \
            "faut donc utiliser avec prudence quand il s'agit de " \
            "modifications de masse. Les alertes générées par le " \
            "script seront affichées directement dans la console."

    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        contexte = Exec(personnage.instance_connexion)
        personnage.contexte_actuel.migrer_contexte(contexte)