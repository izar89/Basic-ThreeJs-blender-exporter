import math
import bpy
import bmesh
from .json import json
from ..three.metadata import Metadata
from ..three.objects import Scene, Mesh
from ..three.geometries import BufferGeometry
from ..three.materials import MeshBasicMaterial

#----------------------------------------------------------
# Exporter
#----------------------------------------------------------
class Exporter:

	def __init__(self, context, properties):
		self.context = context
		self.properties = properties

		self.metadata = None
		self.objects = None
		self.geometries = []
		self.materials = []

		self.__parse()

	#----------------------------------------------------------
	# result to json
	#----------------------------------------------------------
	def json(self):
		result = {}
		if self.metadata:
			result['metadata'] = self.metadata
		if self.objects:
			result['object'] = self.objects
		if self.geometries:
			result['geometries'] = self.geometries
		if self.materials:
			result['materials'] = self.materials
		return json(result)

	#----------------------------------------------------------
	# parse blender scene based on the given properties
	#----------------------------------------------------------
	def __parse(self):
		# export all or selection
		if self.properties.bool_selection:
			bl_objects = self.context.selected_objects
		else:
			bl_objects = self.context.scene.objects

		# metadata
		self.metadata = Metadata(0, 'io_three', bpy.path.basename(self.context.blend_data.filepath), 'Object')

		# object
		if self.properties.bool_scene:
			self.objects = Scene()

		self.__parseObjectsRecursive(self.objects, bl_objects, None)

	def __parseObjectsRecursive(self, objectParent, bl_objects, bl_objectsParent):
		for bl_object in bl_objects:
			if bl_object.parent == bl_objectsParent:
				newParent = self.__parseObject(objectParent, bl_object)
				self.__parseObjectsRecursive(newParent, bl_object.children, bl_object)

	def __parseObject(self, objectParent, bl_object):
		if bl_object.type == 'MESH':
			return self.__parseMesh(objectParent, bl_object)
		# <========================================================== add more object types
		return objectParent

	#----------------------------------------------------------
	# parse mesh
	#----------------------------------------------------------
	def __parseMesh(self, objectParent, bl_object):
		geometry = self.__parseGeometry(bl_object)
		material = self.__parseMaterial(bl_object.active_material)
		mesh = Mesh(bl_object.name, geometry, material)
		mesh.matrix *= bl_object.matrix_local

		if self.properties.bool_scene:
			objectParent.addChild(mesh)
		return mesh

	#----------------------------------------------------------
	# parse geometry
	#----------------------------------------------------------
	def __parseGeometry(self, bl_object):
		bMesh = bmesh.new()
		bMesh.from_object(bl_object, self.context.scene, True)

		vertices = []
		normals = []
		uvs = []

		for face in bMesh.faces:
			vert_count = len(face.verts)
			if vert_count is not 3:
				raise ValueError('parseGeometry() - Non-triangulated face detected')
			for vertex in face.verts:
				vertices.extend(vertex.co)
				normals.extend(vertex.normal)

		bMesh.free() # free and prevent further access

		geometry = BufferGeometry(bl_object.data.name)
		geometry.setPosition(vertices)
		geometry.setNormal(normals)
		geometry.setUv(uvs)
		self.geometries.append(geometry)

		return geometry

	#----------------------------------------------------------
	# parse material
	#----------------------------------------------------------
	def __parseMaterial(self, bl_material):
		material = None
		for mat in self.materials:
			if mat.name == bl_material.name:
				material = mat
				break
		if not material:
			material = MeshBasicMaterial(bl_material.name)
			material.setColor(
				bl_material.diffuse_intensity * bl_material.diffuse_color[0],
				bl_material.diffuse_intensity * bl_material.diffuse_color[1],
				bl_material.diffuse_intensity * bl_material.diffuse_color[2]
			)
			self.materials.append(material)
		return material
