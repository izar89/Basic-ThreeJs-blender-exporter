# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# if 'bpy' in locals():
# 	import importlib
# 	if 'export_scene' in locals():
# 		importlib.reload(export_scene)

import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from mathutils import Matrix
from .exporter.exporter import Exporter

#----------------------------------------------------------
# addon info
#----------------------------------------------------------
bl_info = {
	'name': 'Three.js Export test',
	'location': 'File > Export',
	'category': 'Import-Export'
}

#----------------------------------------------------------
# registration
#----------------------------------------------------------
def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == '__main__':
	register()

#----------------------------------------------------------
# File > Export > Three.js (.json)
#----------------------------------------------------------
def menu_func_export(self, context):
	self.layout.operator(Export.bl_idname, text='Three.js (.json)')

#----------------------------------------------------------
# Export operator
#----------------------------------------------------------
class Export(Operator, ExportHelper):
	bl_idname = 'export.three'
	bl_label = 'Export THREE'
	bl_options = { 'UNDO', 'PRESET' }

	# ExportHelper
	filename_ext = '.json'
	filter_glob = StringProperty(default = '*' + filename_ext, options = { 'HIDDEN' })

	#----------------------------------------------------------
	# operator - execute
	#----------------------------------------------------------
	def execute(self, context):
		json = Exporter(context, self.properties).json()
		return self.write(self.filepath, json)

	def write(self, filepath, data):
		file = open(filepath, 'w', encoding='utf-8')
		file.write(data)
		file.close()
		return {'FINISHED'}

	#----------------------------------------------------------
	# operator - draw
	#----------------------------------------------------------
	bool_selection = BoolProperty(name = 'Selected Objects', description = 'Export selected objects on visible layers', default = False)
	bool_scene = BoolProperty(name = 'Scene', description = 'Export scene', default = True)
	bool_geometries = BoolProperty(name = 'Geometries', description = 'Export geometries', default = True)
	bool_materials = BoolProperty(name = 'Materials', description = 'Export materials', default = True)

	def draw(self, context):
		lyt = self.layout;
		lyt.separator()
		# ------------------
		lyt.prop(self.properties, 'bool_selection')
		lyt.separator()
		# ------------------
		lyt = self.layout.box();
		lyt.label(text = 'Export:')
		lyt.prop(self.properties, 'bool_scene')
		lyt.prop(self.properties, 'bool_geometries')
		lyt.prop(self.properties, 'bool_materials')
