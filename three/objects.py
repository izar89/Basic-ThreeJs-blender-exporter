from mathutils import Matrix
from .. import utils

#----------------------------------------------------------
# Object3D base
#----------------------------------------------------------
class Object3D:

	def __init__(self, name, type):
		self.uuid = utils.uuid4()
		if name:
			self.name = name
		self.type = type
		self.matrix = Matrix.Identity(4)

	def addChild(self, child):
		if not hasattr(self, 'children'):
			self.children = []
		self.children.append(child)

#----------------------------------------------------------
# Scene
#----------------------------------------------------------
class Scene(Object3D):

	def __init__(self):
		super().__init__(None, 'Scene')

#----------------------------------------------------------
# Mesh
#----------------------------------------------------------
class Mesh(Object3D):

	def __init__(self, name, geometry, material):
		super().__init__(name, 'Mesh')
		self.geometry = geometry.uuid
		self.material = material.uuid
