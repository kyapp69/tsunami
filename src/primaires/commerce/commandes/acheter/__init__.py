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


"""Package contenant la commande 'acheter'."""

from primaires.interpreteur.commande.commande import Commande

class CmdAcheter(Commande):
    
    """Commande 'acheter'"""
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "acheter", "buy")
        self.nom_categorie = "objets"
        self.schema = "(<nombre>) <objet:nom_objet_magasin|id_objet_magasin>"
        self.aide_courte = "achète un objet"
        self.aide_longue = \
            "Cette commande permet d'acheter des objets dans un magasin."
    
    def interpreter(self, personnage, dic_masques):
        """Méthode d'interprétation de commande"""
        salle = personnage.salle
        if salle.magasin is None:
            personnage << "|err|Il n'y a pas de magasin ici.|ff|"
            return
        nb_obj = dic_masques["nombre"].nombre if \
            dic_masques["nombre"] is not None else 1
        prototype = dic_masques["objet"].objet
        
        # Vérifications avant de valider l'achat
        if nb_obj > salle.magasin[prototype.cle]:
            personnage << "|err|Les stocks sont insuffisant.|ff|"
            return
        # Vérification de l'argent possédé par le perso
        
        # Tout est bon, on extorque l'argent
        
        # Distribution des objets
        salle.magasin[prototype.cle] -= nb_obj
        for i in range(nb_obj):
            objet = type(self).importeur.objet.creer_objet(prototype)
            objet_spawne = False
            for membre in personnage.equipement.membres:
                if membre.peut_tenir() and membre.tenu is None:
                    membre.tenu = objet
                    objet_spawne = True
                    break
            if not objet_spawne:
                salle.objets_sol.ajouter(objet)
        personnage << "Vous achetez {}.".format(prototype.get_nom(nb_obj))