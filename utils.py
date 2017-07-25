import uuid

def uuid4():
	return str(uuid.uuid4()).upper()

def rgbToInt(r, g, b):
	rgb =  int(r * 255) << 16
	rgb += int(g * 255) << 8
	rgb += int(b * 255)
	return rgb
