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


"""Fichier contenant la fonction équipe."""

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Teste si un personnage équipe un objet."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.possede_proto, "Personnage", "str")

    @staticmethod
    def possede_proto(personnage, prototype):
        """Retourne vrai si le personnage équipe ce prototype, faux sinon.

        Le personnage peut équiper un ou plusieurs objets modelés sur le
        prototype. Vous pouvez également tester si un personnage
        équipe un type en précisant un signe '+' avant le nom du
        type (voir les exemples plus bas). Cette fonction retourne
        une valeur nulle ou le premier objet trouvé ce qui permet
        de capturer l'objet indiqué, si nécessaire pour après (là
        encore, voir les exemples ci-dessous).

        Paramètres à préciser :

          * personnage : le personnage à tester
          * prototype : la clé du prototype ou le nom du type d'objet

        Exemples d'utilisation :

          # Teste si le personnage équipe l'objet 'sabre_fer'
          si equipe(personnage, "sabre_fer"):
          # Ou le capture
          sabre = equipe(personnage, "sabre_fer")
          # On peut faire ensuite si sabre: pour vérifier que le sabre
          # de fer a été trouvé équipé par le personnage
          # Teste si le personnage équipe une arme
          si equipe(personnage, "+arme"):
          # Ou, là encore
          arme = equipe(personnage, "+arme")
          si arme:
            # ...

        """
        nom_type = prototype[1:] if prototype.startswith("+") else ""
        for o in personnage.equipement.equipes:
            if nom_type:
                if o.est_de_type(nom_type):
                    return o
            else:
                if o.cle == prototype:
                    return o

        return None
