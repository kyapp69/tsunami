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


"""Ce fichier contient la classe ListeID, détaillée plus bas."""

from abstraits.obase import *

class ListeID(BaseObj):
    
    """Une version de liste destinée à contenir des objets IDs."""
    
    def __init__(self, parent=None):
        """Constructeur"""
        BaseObj.__init__(self)
        self.__liste = []
        self.parent = parent
    
    def __getnewargs__(self):
        return ()
    
    def __getitem__(self, item):
        """Retourne l'objet correspondant à l'ID."""
        return self.__liste[item].get_objet()
    
    def __setitem__(self, item, objet):
        """Ecrit l'ID de l'objet au lieu de l'objet lui-même"""
        self.__liste[item] = objet.id
        if self.parent:
            self.parent.enregistrer()
        
    def __delitem__(self, item):
        del self.__liste[item]
        if self.parent:
            self.parent.enregistrer()
    
    def __contains__(self, objet):
        """Retourne True si objet.id est dans la liste"""
        s_liste = [str(elt) for elt in self.__liste]
        return str(objet.id) in s_liste
    
    def __getstate__(self):
        """On enregistre juste les IDs dans le fichier"""
        return (self._id_base, self.parent, list(self.__liste))
    
    def __setstate__(self, liste):
        """On place la liste dans self.__liste"""
        # Après la migration de la bêta, on pourra supprimer cette condition
        if isinstance(liste, tuple):
            id_base, parent, liste = liste
        else:
            id_base = -1
            parent = None
        
        BaseObj.__setstate__(self, {
            '_id_base': id_base,
            'parent': parent,
        })
        self.__liste = liste
    
    def __iter__(self):
        """Parcourt (on veille à parcourir les objets, pas les IDs)"""
        for id in self.__liste:
            yield id.get_objet()
    
    def __len__(self):
        """Retourne la taille de la liste"""
        return len(self.__liste)
    
    def __str__(self):
        """Retourne l'affichage de la liste"""
        return "id" + str(self.__liste)
    
    def append(self, objet):
        """Ajoute objet à la fin de la liste"""
        self.__liste.append(objet.id)
        if self.parent:
            self.parent.enregistrer()
    
    def insert(self, indice, objet):
        """Ajoute objet.id à la position demandée"""
        self.__liste.inser(indice, objet.id)
        if self.parent:
            self.parent.enregistrer()
    
    def remove(self, objet):
        """Retire l'objet passé en paramètre"""
        for elt_id in list(self.__liste):
            if str(elt_id) == str(objet.id):
                self.__liste.remove(elt_id)
        if self.parent:
            self.parent.enregistrer()
    
    # Méthodes extérieures aux listes
    def supprimer_doublons(self):
        """Supprime les doublons de la liste.
        On conserve la première occurence de l'élément mais pas les autres.
        
        """
        n_liste = []
        s_liste = [] # liste contenant les code des IDs
        for elt in self.__liste:
            if str(elt) not in s_liste:
                n_liste.append(elt)
                s_liste.append(str(elt))
        
        self.__liste = n_liste
    
    def supprimer_none(self):
        """Supprime les objets None de la liste."""
        n_liste = []
        for elt in self.__liste:
            if elt.get_objet() is not None:
                n_liste.append(elt)
        
        self.__liste = n_liste
