#----------------------------------------------------------
# Metadata
#----------------------------------------------------------
class Metadata:

	def __init__(self, version, generator, filename, type):
		if version:
			self.version = version
		if generator:
			self.generator = generator
		if filename:
			self.filename = filename
		if type:
			self.type = type
