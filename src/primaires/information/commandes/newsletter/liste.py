# -*-coding:Utf-8 -*

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


"""Fichier contenant le paramètre 'liste' de la commande 'newsletter'."""

from math import floor

from primaires.interpreteur.masque.parametre import Parametre
from primaires.format.fonctions import couper_phrase

class PrmListe(Parametre):
    
    """Commande 'newsletter liste'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "liste", "list")
        self.schema = "(<message>)"
        self.aide_courte = "liste les newsletters existants"
        self.aide_longue = \
            "Cette commande liste les newsletters existants. Vous pouvez " \
            "préciser un ou plusieurs flags séparés par des virgules ; " \
            "les flags disponibles sont |ent|non assignes|ff| pour voir " \
            "uniquement les newsletters non assignes, et |ent|fermes|ff| pour " \
            "voir tous les newsletters, y compris ceux fermés."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        flags = {"non assignes": False, "fermes": False}
        if dic_masques["message"] is not None:
            t_flags = dic_masques["message"].message
            t_flags = [f.strip() for f in t_flags.split(",")]
            for f in flags.keys():
                if f in t_flags:
                    flags[f] = True
        
        newsletters = list(importeur.newsletter.newsletters.values())
        if not flags["fermes"]:
            newsletters = [r for r in newsletters if r.ouvert]
        if flags["non assignes"]:
            newsletters = [r for r in newsletters if r.assigne_a is None]
        if not personnage.est_immortel():
            # On récupère les newsletters envoyés par le joueur mortel
            newsletters = [r for r in newsletters if r.createur is personnage]
            if not newsletters:
                personnage << "|att|Vous n'avez envoyé aucun newsletter.|ff|"
            else:
                l_id = max([len(str(r.id)) for r in newsletters] + [2])
                l_titre = max([len(r.titre) for r in newsletters] + [5])
                l_titre_max = 49 - l_id # longueur max possible d'un titre
                ljust_titre = min(l_titre_max, l_titre)
                lignes = [
                    "+" + "-" * (l_id + ljust_titre + 29) + "+",
                    "| |tit|" + "ID".ljust(l_id) + "|ff| | |tit|" \
                            + "Titre".ljust(ljust_titre) + "|ff| | " \
                            "|tit|Statut|ff|   | |tit|Avancement|ff| |",
                    "+" + "-" * (l_id + ljust_titre + 29) + "+",
                ]
                for newsletter in newsletters:
                    id = "|vrc|" + str(newsletter.id).ljust(l_id) + "|ff|"
                    if l_titre_max < l_titre:
                        titre = couper_phrase(newsletter.titre, l_titre_max)
                    else:
                        titre = newsletter.titre
                    titre = titre.ljust(ljust_titre)
                    stat = CLR_STATUTS[newsletter.statut]
                    stat += newsletter.statut.ljust(8) + "|ff|"
                    clr = CLR_AVC[floor(newsletter.avancement / 12.5)]
                    avc = clr + str(newsletter.avancement).rjust(9)
                    lignes.append(
                            "| {id} | {titre} | {stat} | {avc}%|ff| |".format(
                            id=id, titre=titre, stat=stat, avc=avc))
                lignes.append("+" + "-" * (l_id + ljust_titre + 29) + "+")
                personnage << "\n".join(lignes)
        else:
            if not newsletters:
                personnage << "|err|Aucun newsletter n'a été envoyé.|ff|"
                return
            l_id = max([len(str(r.id)) for r in newsletters] + [2])
            l_createur = max([len(r.createur.nom) if r.createur else 7 \
                    for r in newsletters] + [8])
            l_titre = max([len(r.titre) for r in newsletters] + [5])
            l_titre_max = 70 - l_createur - l_id # longueur max d'un titre
            ljust_titre = min(l_titre_max, l_titre)
            lignes = [
                "+" + "-" * (l_id + l_createur + ljust_titre + 8) + "+",
                "| |tit|" + "ID".ljust(l_id) + "|ff| | |tit|" \
                        + "Créateur".ljust(l_createur) + "|ff| | |tit|" \
                        + "Titre".ljust(ljust_titre) + "|ff| |",
                "+" + "-" * (l_id + l_createur + ljust_titre + 8) + "+",
            ]
            for newsletter in newsletters:
                if l_titre_max < l_titre:
                    titre = couper_phrase(newsletter.titre, l_titre_max)
                else:
                    titre = newsletter.titre
                createur = newsletter.createur and newsletter.createur.nom or \
                        "inconnu"
                lignes.append("| |vrc|" + str(newsletter.id).ljust(l_id) \
                        + "|ff| | " + createur.ljust(l_createur) + " | " \
                        + titre.ljust(ljust_titre) + " |")
            lignes.append(
                "+" + "-" * (l_id + l_createur + ljust_titre + 8) + "+")
            personnage << "\n".join(lignes)
