﻿# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant le paramètre 'lire' de la commande 'messages'."""

from primaires.interpreteur.masque.parametre import Parametre
from primaires.communication.mudmail import ENVOYE, BROUILLON, ARCHIVE

class PrmLire(Parametre):
    
    """Commande 'messages lire'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "lire", "read")
        self.schema = "(<flag_mail>) <id_mail>"
        self.aide_courte = "lit un mudmail"
        self.aide_longue = \
            "Cette sous-commande affiche le contenu d'un message. L'id " \
            "correspond à celui affiché dans la commande %mails list% pour " \
            "le même flag de filtre."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        mails = type(self).importeur.communication.mails
        if dic_masques["flag_mail"] is not None:
            flag = dic_masques["flag_mail"].flag
            if flag == "recus":
                mails = mails.get_mails_pour(personnage, ENVOYE, exp=False)
            elif flag == "brouillons":
                mails = mails.get_mails_pour(personnage, BROUILLON)
            elif flag == "archives":
                mails = mails.get_mails_pour(personnage, ARCHIVE)
            elif flag == "envoyes":
                mails = mails.get_mails_pour(personnage, ENVOYE)
        else:
            mails = mails.get_mails_pour(personnage, ENVOYE, exp=False)
            mails = [mail for mail in mails if mail.lu == False]
        
        num = dic_masques["id_mail"].id_mail
        if not mails:
            personnage << "|err|Aucun message ne correspond à ce numéro.|ff|"
        else:
            i = 1
            r_mail = None
            for mail in mails:
                r_mail = mail
                if i == num:
                    break
                i += 1
            if r_mail is None:
                personnage << "|err|Aucun message ne correspond à ce numéro.|ff|"
            else:
                personnage << r_mail.afficher()
