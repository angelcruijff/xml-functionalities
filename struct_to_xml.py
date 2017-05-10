from xml.etree.ElementTree import Element, SubElement, tostring

class NoStruct(Exception):
        pass

class Struct(object):
	""" Clase para convetir la estructura base de un diccionario
		y una lista en un XML.
		Sirve para armar todo tipo de XML. Pensado
		especificamente para CFDI.
		
		Attributes:
        attribs: Los atributos del nodo. Opcional.
        childs: Si el nodo tiene hijos, se agregan a la lista.
		name: Nombre del nodo. Obligatorio
	 """
	__slots__ = ('attribs', 'childs', 'name')

	def __init__(self, name):
		self.attribs = {}
		self.childs = []
		self.name = name
	
	def set_attrib_from_dict(self, dicc):
		self.attribs.update(dicc)
	
	def set_attrib(self, key, value):
		self.attribs[key] = value
	
	def add_child(self, name):
		self.childs.append(Struct(name))
		return self.childs[-1]

def parse_childs(elem, parent):
	""" Funcion que recorre los hijos del nodo padre
		para ir armando el XML.
		
		Parametros:
		elem: El elemento del cual se va a crear el nodo del XML
		parent: El padre al cual va a pertenecer el nodo del XML
	"""
	child = SubElement(parent, elem.name)
	[child.set(key, value) for key, value in elem.attribs.items()]
	for e in elem.childs:
		parse_childs(e, child)

def create_xml(root):
	""" Funcion principal para convertir el Elemento en el XMl
		
		Parametro:
		root: Elemento a convertir en XML
	"""
	if isinstance(root, Struct):
		top = Element(root.name)
		[top.set(key, value) for key, value in root.attribs.items()]
		for elem in root.childs:
			parse_childs(elem, top)
		return tostring(top)
	else:
		raise NoStruct('El elemento no es del tipo adecuado (Elemento)')

def main():
	""" Funcion para mostrar uso de la funcionalidad """
	conceptos = Struct('cfdi:Conceptos')
	attrs = {'Nombre': 'AC14', 'Llave': 'Master'}
	conceptos.set_attrib_from_dict(attrs)
	
	concepto = conceptos.add_child('cfdi:Concepto')
	attrs = {'Codigo': 'XYZ', 'Precio': '14.14'}
	concepto.set_attrib_from_dict(attrs)
	impuestos = concepto.add_child('Impuestos')
	traslado = impuestos.add_child('Traslado')
	attrs = {'Base': '14000', 'Impuesto': '014'}
	traslado.set_attrib_from_dict(attrs)
	print(create_xml(conceptos))
	

if __name__ == '__main__':
	main()
