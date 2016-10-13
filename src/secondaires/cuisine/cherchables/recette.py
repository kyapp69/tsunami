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


"""Ce fichier définit le cherchable des recettes."""

from primaires.recherche.cherchables.cherchable import Cherchable

class CherchableRecette(Cherchable):

    """Classe cherchable pour les recettes de l'univers."""

    nom_cherchable = "recette"
    recherche_par_defaut = "cle"
    noms_colonnes = {
        "cle": "clé",
        "difficulte": "difficulté",
        "xp": "XP",
    }

    def init(self):
        """Méthode d'initialisation.

        C'est ici que l'on ajoute réellement les filtres, avec la méthode
        dédiée.

        """
        self.ajouter_filtre("d", "difficulte", "difficulte", "nombre")
        self.ajouter_filtre("i", "ingredients", "aff_ingredients", "regex")
        self.ajouter_filtre("l", "cle", "cle", "regex")
        self.ajouter_filtre("r", "resultat", "aff_resultat", "regex")
        self.ajouter_filtre("t", "temps", "temps_cuisson", "nombre")
        self.ajouter_filtre("u", "ustensiles", "aff_ustensiles", "regex")
        self.ajouter_filtre("x", "xp", "xp", "nombre")

    @property
    def items(self):
        """Renvoie la liste des objets traités"""
        return list(importeur.cuisine.recettes.values())

    @property
    def attributs_tri(self):
        """Renvoie la liste des attributs par lesquels on peut trier"""
        return ["cle", "difficulte", "resultat", "temps", "ustensiles", "xp"]

    @property
    def colonnes(self):
        """Retourne un dictionnaire des valeurs que l'on peut disposer en
        colonne à l'affichage final, de la forme :
        >>> {nom: attribut/méthode}
        (une colonne peut être remplie par une méthode du cherchable).

        """
        return {
            "cle": "cle",
            "difficulte": "difficulte",
            "resultat": "aff_resultat",
            "temps": "temps_cuisson",
            "ustensiles": "aff_ustensiles",
            "xp": "xp",
        }

    def colonnes_par_defaut(self):
        """Retourne les colonnes d'affichage par défaut.

        Si une ou plusieurs colonnes sont spécifiés lors de la recherche,
        les colonnes par défaut ne sont pas utilisées.

        Cette méthode doit retourner une liste de nom de colonnes.

        """
        return ("cle", "resultat", "difficulte", "xp")

    def tri_par_defaut(self):
        """Sur quelle colonne se base-t-on pour trier par défaut ?"""
        return "cle"
