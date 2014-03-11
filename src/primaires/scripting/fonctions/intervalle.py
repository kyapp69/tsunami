# -*-coding:Utf-8 -*

# Copyright (c) 2014 LE GOFF Vincent
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


"""Fichier contenant la fonction intervalle."""

from fractions import Fraction

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):

    """Retourne une liste contenant un intervalle de valeurs entières entre valMin et valMax -1 inclus. Un paramètre facultatif peut être donné en troisième argument, le pas entre chaque valeur.
	Cette fonction peut être très pratique pour itérer dans une boucle un nombre fixé de fois."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.intervalle, "Fraction", "Fraction")
        cls.ajouter_types(cls.intervalle_ecart, "Fraction", "Fraction", "Fraction")

    @staticmethod
    def intervalle(val_min, val_max):
        """Retourne une liste contenant un intervalle de valeurs entières entre valMin et valMax -1 inclus."""
        return range(int(val_min), int(val_max))
	
    @staticmethod
    def intervalle_ecart(val_min, val_max, ecart):
        """Retourne une liste contenant un intervalle de valeurs entières entre valMin et valMax -1 inclus, avec un écart entre chaque valeur de ecart."""
        return range(int(val_min), int(val_max), int(ecart))
