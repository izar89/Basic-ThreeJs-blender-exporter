from .. import utils

#----------------------------------------------------------
# Material base
#----------------------------------------------------------
class Material:

	def __init__(self, name, type):
		self.uuid = utils.uuid4()
		if name:
			self.name = name
		self.type = type

#----------------------------------------------------------
# MeshBasicMaterial
#----------------------------------------------------------
class MeshBasicMaterial(Material):

	def __init__(self, name):
		super().__init__(name, 'MeshBasicMaterial')
		self.setColor(255, 255, 255)

	def setColor(self, r, g, b):
		self.color = utils.rgbToInt(r, g, b)
