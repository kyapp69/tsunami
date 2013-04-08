from .vetement import Vetement

class Veste(Vetement):
	nom_type = "veste"
	def __init__(self, cle=""):
		Vetement.__init__(self, cle)
		self.emplacement = "corps"
		self.positions = (1, 2)