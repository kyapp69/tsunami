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


"""Fichier contenant la fonction route."""

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne la route entre deux salles, si trouvée."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.route, "Salle", "Salle")

    @staticmethod
    def route(origine, destination):
        """Retourne la liste des sorties reliant origine à destination.

        Cette fonction utilise le complexe des routes créé. Les
        deux salles (origine et destination) doivent donc être
        présentes dans deux routes. Il doit de plus exister un
        chemin identifié par le système (le système doit savoir
        comment relier les deux routes en question). Si la route ne
        peut pas être trouvée, pour X raison, une valeur nulle est
        retournée et un message d'avertissement est enregistré dans
        les logs, pour aider au débuggage. Sinon, retourne la
        liste des sorties permettant de se rendre de origine à
        destination.

        Paramètres à préciser :

          * origine : la salle d'origine
          * destination : la salle de destination

        Exemple d'utilisation :

          # Récupère deux salles dans l'univers, si nécessaire
          origine = salle("zone1:mnemonique1")
          destination = salle("zone2:mnemonique2")
          # Recherche la route entre 'origine' et 'destination'
          sorties = route(origine, destination)
          si sorties:
              # La route a pu être trouvée
              # ...
              pour chaque direction dans sorties:
                  dire origine "On va vers ${direction}."
              fait
          finsi

        """
        try:
            route = importeur.route.trouver_chemin(origine, destination)
        except ValueError as err:
            importeur.scripting.logger.warning(str(err))
            return None
        else:
            return route.sorties
