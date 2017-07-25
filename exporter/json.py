import re
import json as jsonModule
from mathutils import Matrix

#----------------------------------------------------------
# json from dictionary
#----------------------------------------------------------
def json(dict):
	json = jsonModule.dumps(dict, sort_keys = True, indent = 4, separators=(',', ':'), cls = CustomEncoder)
	json = removeIndentationFromLists(json)
	return json

def removeIndentationFromLists(json):
	# [-+]?[0-9]*\.?[0-9]+ => float
	json = re.sub(r'\s+(?=[-+]?[0-9]*\.?[0-9]+)', r'', json)
	json = re.sub(r'([-+]?[0-9]*\.?[0-9]+)\s+', r'\1', json)
	return json

#----------------------------------------------------------
# Custom encoder for JSON not serializable objects
#----------------------------------------------------------
class CustomEncoder(jsonModule.JSONEncoder):
	def default(self, obj):
		# Matrix
		if isinstance(obj, Matrix):
			return self.matrixToList(obj)
		# Object
		if hasattr(obj, '__dict__'):
			return obj.__dict__
		# everything else
		return jsonModule.JSONEncoder.default(self, obj)

	def matrixToList(self, matrix):
		newList = []
		for y in range(0, len(matrix.col)):
			for x in range(0, len(matrix.row)):
				newList.append(self.removeTrailingZero(matrix[x][y]))
		return newList

	def removeTrailingZero(self, value):
		if value.is_integer():
			value = int(value)
		return value
