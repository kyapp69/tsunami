# -*-coding:Utf-8 -*

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


"""Fichier contenant le module primaire aide."""

from abstraits.module import *
from primaires.format.fonctions import *
from primaires.information import commandes

from .editeurs.hedit import EdtHedit

from .sujet import SujetAide
from .versions import Versions

class Module(BaseModule):
    
    """Cette classe représente le module primaire information.
    
    Ce module gère l'aide in-game, c'est-à-dire les sujets d'aide
    (fichier ./sujet.py), ainsi que le système de versions.
    
    """
    
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "information", "primaire")
        self.__sujets = []
        self.versions = None
    
    def init(self):
        """Initialisation du module.
        
        On récupère les sujets d'aide enregistrés et les versions.
        
        """
        sujets = self.importeur.supenr.charger_groupe(SujetAide)
        self.__sujets = sujets
        nb_sujets = len(sujets)
        print(format_nb(nb_sujets, "{nb} sujet{s} d'aide récupéré{s}"))
        
        versions = None
        sous_rep = "information"
        fichier = "versions.sav"
        if self.importeur.supenr.fichier_existe(sous_rep, fichier):
            versions = self.importeur.supenr.charger(sous_rep, fichier)
        else:
            versions = Versions()
        self.versions = versions
        
        BaseModule.init(self)
    
    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.aide.CmdAide(),
            commandes.hedit.CmdHedit(),
            commandes.versions.CmdVersions(),
        ]
        
        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)
        
        # Ajout de l'éditeur 'hedit'
        self.importeur.interpreteur.ajouter_editeur(EdtHedit)
    
    def __getitem__(self, titre):
        """Retourne le sujet portant ce titre.
        
        Si le titre n'est pas trouvé, lève l'exception KeyError.
        La recherche du sujet se fait sans tenir compte des accents ni de
        la casse.
        
        """
        titre = supprimer_accents(titre).lower()
        for sujet in self.__sujets:
            if supprimer_accents(sujet.titre).lower() == titre:
                return sujet
        raise KeyError("le titre {} n'a pas pu être trouvé".format(titre))
    
    def __delitem__(self, titre):
        """Détruit un sujet d'aide de manière définitive."""
        titre = supprimer_accents(titre).lower()
        for sujet in self.__sujets:
            if supprimer_accents(sujet.titre).lower() == titre:
                titre = sujet
                break
        self.__sujets.remove(titre)
    
    def get_sujet_par_mot_cle(self, mot):
        """Retourne le sujet correspondant à ce mot-clé."""
        mot = supprimer_accents(mot.lower())
        for sujet in self.__sujets:
            if mot in [supprimer_accents(m) for m in sujet.mots_cles]:
                return sujet
        return None
    
    def get_sujet(self, nom_sujet):
        """Retourne un sujet ou None si le sujet recherché n'existe pas.
        Contrairement à __getitem__ et get_sujet_par_mot_cle, le sujet est
        renvoyé indifféremment en fonction de son nom ou d'un mot-clé.
        
        """
        sujet = None
        try:
            sujet = self[nom_sujet]
        except KeyError:
            sujet = self.get_sujet_par_mot_cle(nom_sujet)
        return sujet
    
    @property
    def sujets(self):
        """Retourne la liste déréférencée des sujets."""
        return list(self.__sujets)
    
    def ajouter_sujet(self, titre):
        """Ajoute un sujet à la liste des sujets d'aide.
        
        Le titre du sujet doit être fourni en paramètre.
        Si le titre est déjà utilisé, lève une exception. Sinon, retourne
        le sujet nouvellement créé.
        
        """
        titres_sujets = [supprimer_accents(s.titre).lower() for s in \
                self.__sujets]
        if supprimer_accents(titre).lower() in titres_sujets or \
                self.get_sujet_par_mot_cle(titre) is not None:
            raise ValueError("le titre {} est déjà utilisé".format(titre))
        sujet = SujetAide(titre)
        self.__sujets.append(sujet)
        return sujet
    
    def construire_sommaire_pour(self, personnage):
        """Retourne le sommaire de la rubrique d'aide pour personnage."""
        # On affiche la liste des sujets d'aides
        peut_lire = []
        for sujet in self.sujets:
            if self.importeur.interpreteur.groupes. \
                    explorer_groupes_inclus(personnage.grp, sujet.str_groupe):
                peut_lire.append(sujet)
        
        peut_lire = [s.titre for s in peut_lire if s.pere is None]
        if not peut_lire:
            peut_lire.append("|att|Aucun|ff|")
        
        msg = "Sujets d'aides disponibles :\n\n  "
        msg += "\n  ".join(sorted(peut_lire))
        return msg