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


"""Fichier contenant le module primaire connex."""

from datetime import datetime
import hashlib
import sys

from abstraits.module import *
from primaires.connex.instance_connexion import InstanceConnexion
from reseau.connexions.client_connecte import ClientConnecte
from primaires.connex.compte import Compte
from primaires.connex.config import cfg_connex
from . import contextes
from .bannissements import Bannissements
from primaires.format.fonctions import format_nb

# Nom du groupe fictif
NOM_GROUPE = "connexions"

class Module(BaseModule):
    """Module gérant les connexions et faisant donc le lien entre les clients
    connectés et les joueurs, ou leur instance de connexion.

    """
    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "connex", "primaire")
        self.instances = {}
        self.cnx_logger = type(self.importeur).man_logs.creer_logger( \
                "connex", "connexions")

        # Comptes
        self.comptes = {}
        self.cpt_logger = type(self.importeur).man_logs.creer_logger( \
                "connex", "comptes")
        self.joueurs_bannis = []
        self.bannissements_temporaires = {}
        self.table_logger = importeur.man_logs.creer_logger("connex", "table")
        type(importeur).espace["comptes"] = self.comptes

    def config(self):
        """Configuration du module.

        On crée le fichier de configuration afin de l'utiliser plus tard
        dans les contextes.

        """
        cfg = type(self.importeur).anaconf.get_config("connex", \
            "connex/connex.cfg", "modele connexion", cfg_connex)

        if cfg.type_chiffrement not in hashlib.algorithms_guaranteed and \
                cfg.type_chiffrement in hashlib.algorithms_available:
            self.cnx_logger.warning("L'algorithme '{}' utilisé pour " \
                    "chiffrer les mots de passe n'est pas portable.".format(
                    cfg.type_chiffrement))
        elif cfg.type_chiffrement not in hashlib.algorithms_available:
            self.cnx_logger.fatal("L'algortihme '{}' utilisé pour " \
                    "chiffrer les mots de passe n'existe pas.".format(
                    cfg.type_chiffrement))
            sys.exit(1)

        # Création des hooks
        importeur.hook.ajouter_hook("connex:cmd",
                "Hook appelé quand un client entre un message")

        BaseModule.config(self)

    def init(self):
        """Initialisation du module.

        On récupère les instances de connexion et on les stocke dans
        'self.instances' si elles sont encore connectées.

        """
        comptes_a_pas_effacer = []

        # On récupère les comptes
        comptes = self.importeur.supenr.charger_groupe(Compte)
        for compte in comptes:
            self.comptes[compte.nom] = compte

        # On récupère les instances de connexion
        objets = []

        comptes_a_pas_effacer = []

        for inst in objets:
            if inst.client.n_id in type(self.importeur).serveur.clients.keys():
                nouv_instance = InstanceConnexion(inst.client, False)
                nouv_instance.creer_depuis(inst)
                self.instances[inst.client.n_id] = nouv_instance
                if (nouv_instance.compte):
                    comptes_a_pas_effacer.append(nouv_instance.compte.nom)

        for compte in comptes:
            if (not compte.valide) and (not compte.nom in comptes_a_pas_effacer):
                self.supprimer_compte(compte)

        nb_comptes = len(self.comptes)
        self.cpt_logger.info(
            format_nb(nb_comptes, "{nb} compte{s} récupéré{s}"))

        # On récupère ou crée la table des bannissements
        bannissements = self.importeur.supenr.charger_unique(Bannissements)
        if bannissements is None:
            bannissements = Bannissements()
        else:
            self.bannissements_temporaires = bannissements.temporaires
            self.joueurs_bannis = bannissements.joueurs
        self.bannissements = bannissements

        BaseModule.init(self)

    def preparer(self):
        """Préparation du module"""
        for joueur in self.joueurs:
            if joueur.race and (not joueur.equipement or \
                    (not joueur.equipement.squelette and \
                    joueur.race.squelette)):
                joueur.lier_equipement(joueur.race.squelette)

        temporaires = {}
        joueurs = []
        for nom, date in self.bannissements.temporaires.items():
            try:
                joueur = importeur.joueur.joueurs[nom]
            except KeyError:
                pass
            else:
                if not joueur.e_existe:
                    continue

                temporaires[joueur] = date

        for nom in self.bannissements.joueurs:
            try:
                joueur = importeur.joueur.joueurs[nom]
            except KeyError:
                pass
            else:
                if not joueur.e_existe:
                    continue

                joueurs.append(joueur)

        self.bannissements.temporaires.clear()
        self.bannissements.temporaires.update(temporaires)
        self.bannissements.joueurs[:] = joueurs
        self.actualiser_bannissements()

    def boucle(self):
        """A chaque tour de boucle synchro, on envoie la file d'attente des
        instances de connexion.

        """
        for inst in self.instances.values():
            inst.envoyer_file_attente()

    def __getitem__(self, item):
        """Méthode appelée quand on fait connex[item].
        L'item peut être de plusieurs types :
        -   entier : c'est l'ID du client
        -   client : on récupère son ID

        """
        if isinstance(item, ClientConnecte):
            item = item.n_id
        if item not in self.instances.keys():
            raise KeyError("L'ID {0} ne se trouve pas dans les instances " \
                    "connectées".format(repr(item)))
        return self.instances[item]

    @property
    def joueurs(self):
        """Retourne un tuple des joueurs existants"""
        joueurs = []
        for compte in self.comptes.values():
            for joueur in compte.joueurs:
                joueurs.append(joueur)

        return tuple(joueurs)

    @property
    def joueurs_connectes(self):
        """Retourne un tuple des joueurs connectés"""
        joueurs = []
        for compte in self.comptes.values():
            for joueur in compte.joueurs:
                if joueur.est_connecte():
                    joueurs.append(joueur)

        return tuple(joueurs)

    def ajouter_instance(self, client):
        """Cette méthode permet d'ajouter une instance de connexion.
        Elle est appelée quand la connexion est établie avec le serveur.
        Ainsi, l'instance de connexion est créée avec des paramètres par
        défaut.

        """
        instance_connexion = InstanceConnexion(client)
        self.instances[client.n_id] = instance_connexion

    def retirer_instance(self, client):
        """L'instance à supprimer peut être de plusieurs types :
        -   entier : c'est l'ID du client
        -   ClientConnecte : on extrait son ID

        """
        if isinstance(client, ClientConnecte):
            client = client.n_id
        if client not in self.instances:
            raise KeyError("L'ID {0} ne se trouve pas dans les instances " \
                    "connectées".format(repr(client)))

        instance = self.instances[client]
        joueur = instance.joueur

        if joueur and instance.contexte_actuel and not joueur.garder_connecte:
            instance.contexte_actuel.deconnecter()

        instance.deconnecter("déconnexion fortuite")
        del self.instances[client]
        instance.detruire()

    def ajouter_compte(self, nom_compte):
        """Méthode appelée pour ajouter un compte identifié par son nom"""
        nouv_compte = Compte(nom_compte)
        self.cpt_logger.info("Création du compte {}: {}".format(
                nom_compte, nouv_compte))
        self.comptes[nouv_compte.nom] = nouv_compte
        return nouv_compte

    def supprimer_compte(self, compte):
        """Supprime le compte 'compte'"""
        if compte.nom in self.comptes.keys():
            self.cpt_logger.info("Suppression du compte {0}: {1}".format( \
                    compte.nom, compte))
            del self.comptes[compte.nom]
            compte.detruire()
        else:
            raise KeyError("Le compte n'est pas dans la liste " \
                    "des comptes existants".format(compte))

    def get_compte(self, nom):
        """Récupère le compte 'compte'"""
        res = None
        for compte in self.comptes.values():
            if compte.nom == nom:
                res = compte

        return res

    def _get_email_comptes(self):
        """Retourne sous la forme d'un tuple la liste des emails de comptes
        créés ou en cours de création.

        """
        emails = []
        for compte in self.comptes.values():
            emails.append(compte.adresse_email)

        return tuple(emails)

    email_comptes = property(_get_email_comptes)

    def _get_nom_comptes(self):
        """Retourne sous la forme d'un tuple la liste des noms de comptes
        créés ou en cours de création.

        """
        noms = []
        for compte in self.comptes.values():
            noms.append(compte.nom)

        return tuple(noms)

    nom_comptes = property(_get_nom_comptes)

    def _get_nom_joueurs(self):
        """Retourne sous la forme d'un tuple la liste des noms de joueurs
        créés ou en cours de création.

        """
        noms = []
        for compte in self.comptes.values():
            for joueur in compte.joueurs:
                noms.append(joueur.nom)

        return tuple(noms)

    nom_joueurs = property(_get_nom_joueurs)

    def compte_est_cree(self, nom_compte, ouvert=True):
        """Return True si le compte est créé, False sinon.

        """
        if nom_compte in self.nom_comptes:
            compte = self.comptes[nom_compte]
            if ouvert and not compte.ouvert:
                return False

            return True

        return False

    def actualiser_bannissements(self):
        """Actualise les bannissements temporaires."""
        self.importeur.diffact.ajouter_action("ban_tmp",
                60, self.actualiser_bannissements)
        maintenant = datetime.now()
        for joueur, date in tuple(self.bannissements_temporaires.items()):
            if not joueur.e_existe:
                del self.bannissements_temporaires[joueur]
            elif maintenant > date:
                del self.bannissements_temporaires[joueur]
