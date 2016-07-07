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


"""Ce fichier contient le manipulteur SON pour les dictionnaires ordonnées."""

from collections import OrderedDict

from pymongo.son_manipulator import SONManipulator

class TransformOrderedDict(SONManipulator):

    """Convertit une dictionnaire ordonné."""

    def transform_value(self, value):
        """Convertit la valeur."""
        return {
                "_custom_type": "OrderedDict",
                "keys": list(value.keys()),
                "values": list(value.values()),
        }

    def transform_list(self, liste, collection):
        """Convertit une liste."""
        copie = []
        for elt in liste:
            if isinstance(elt, OrderedDict):
                elt = self.transform_value(elt)
            elif isinstance(elt, list):
                self.transform_list(elt, collection)
            elif isinstance(elt, dict):
                self.transform_incoming(elt, collection)

            copie.append(elt)

        liste[:] = copie

    def transform_incoming(self, bson, collection):
        for key, value in bson.items():
            if isinstance(value, OrderedDict):
                bson[key] = self.transform_value(value)
            elif isinstance(value, list):
                self.transform_list(value, collection)
            elif isinstance(value, dict):
                self.transform_incoming(value, collection)

        return bson

    def transform_outgoing(self, son, collection):
        for key, value in son.items():
            if isinstance(value, dict):
                if value.get("_custom_type", "") == "OrderedDict":
                    dictionnaire = OrderedDict(zip(value["keys"],
                            value["values"]))
                    son[key] = dictionnaire
                else:
                    self.transform_outgoing(value, collection)
            elif isinstance(value, list):
                self.transform_outgoing_list(value)

        return son

    def transform_outgoing_list(self, liste):
        copie = []
        for value in liste:
            if isinstance(value, dict):
                if value.get("_custom_type", "") == "OrderedDict":
                    dictionnaire = OrderedDict(zip(value["keys"],
                            value["values"]))
                    value = dictionnaire
                else:
                    self.transform_outgoing(value, collection)
            elif isinstance(value, list):
                self.transform_outgoing_list(value)

            copie.append(value)

        liste[:] = copie
