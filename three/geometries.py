from .. import utils

#----------------------------------------------------------
# Geometry base
#----------------------------------------------------------
class Geometry:

	def __init__(self, name, type):
		self.uuid = utils.uuid4()
		if name:
			self.name = name
		self.type = type

#----------------------------------------------------------
# BufferGeometry
#----------------------------------------------------------
class BufferGeometry(Geometry):

	def __init__(self, name):
		super().__init__(name, 'BufferGeometry')
		self.data = {}

	def setPosition(self, arr):
		if 'attributes' not in self.data:
			self.data['attributes'] = {}
		self.data['attributes']['position'] = BufferAttribute(3, BufferAttribute.TYPE_FLOAT32, arr);

	def setNormal(self, arr):
		if 'attributes' not in self.data:
			self.data['attributes'] = {}
		self.data['attributes']['normal'] = BufferAttribute(3, BufferAttribute.TYPE_FLOAT32, arr);

	def setUv(self, arr):
		if 'attributes' not in self.data:
			self.data['attributes'] = {}
		self.data['attributes']['uv'] = BufferAttribute(2, BufferAttribute.TYPE_FLOAT32, arr);

#----------------------------------------------------------
# BufferAttribute
#----------------------------------------------------------
class BufferAttribute:

	TYPE_FLOAT32 = 'Float32Array'

	def __init__(self, itemSize, type, array):
		self.itemSize = itemSize
		self.type = type
		self.array = array
