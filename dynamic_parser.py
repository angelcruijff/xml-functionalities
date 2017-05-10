import xml.etree.ElementTree as ET
import json

"""
Namespaces del SAT
ns = {}
ns['sat'] = 'http://www.sat.gob.mx/cfd/3'
ns['cfdi'] = 'cfdi'
ns['complemento'] = 'http://www.sat.gob.mx/TimbreFiscalDigital'
ns['tfd'] = 'tfd'
"""

class CfdiToDict(object):
	""" Clase para parsear un XML de CFDI y convertirlo
		en un diccionario con atributos y nodos
	"""
	root = {}
	ns = None
	childrens = None
	
	def __init__(self, path_to_file="", xml_string = "", namespace=None):
		if path_to_file != '' and xml_string != '':
			raise Exception("Solo puede indicar un medio para cargar el XML a parsear")
		if path_to_file:
			tree = ET.parse(path_to_file)
			self.xml = tree.getroot()
		else:
			self.xml = ET.fromstring(xml_string)
		if namespace is not None:
			self.ns = namespace
		self.convert()
	
	def convert(self):
		name_element = self.__clean_namespace(self.xml.tag)
		self.root[name_element] = {'attrs' : self.xml.attrib}
		for element in self.xml.getchildren():
			name, data = self.__parse_element(element)
			self.root[name] = data
			del data
	
	def __parse_element(self, element):
		name_element = self.__clean_namespace(element.tag)
		element_dict = {}
		try:
			attrs = element.attrib
		except AttributeError:
			attrs = None
		element_dict['attrs'] = attrs
		if len(element.getchildren()) > 0:
			repeated_element = self.__check_repeated_childrens(element)
			if repeated_element:
				element_list = []
				for e in element.getchildren():
					subelement_dict = {}
					name, dicc = self.__parse_element(e)
					subelement_dict[name] = dicc
					element_list.append(subelement_dict)
				element_dict[name_element] = element_list
			else:
				for e in element.getchildren():
					name, dicc = self.__parse_element(e)
					element_dict[name] = dicc
		return name_element, element_dict
	
	def __check_repeated_childrens(self, element):
		tags = [self.__clean_namespace(e.tag) for e in element.getchildren()]
		if len(tags) != len(set(tags)):
			return True
		return False
	
	def __clean_namespace(self, tag):
		pos = tag.find("}") + 1
		nuevo_tag = tag[pos:]
		return nuevo_tag



if __name__ == '__main__':

	"""
	Mejora: Hacer todo dinamico, recorrer por completo el XML con lo que brinde el tree.getroot() (Getchildren, obtener atributos, etc)
			Para que no tenga nada amarrado y poder aplicarlo con cualquier libreria.
			Limpiar las llaves con los ns declarados y con find y replace en un loop
			Revisar si se puede obtener el elemento sin tener que limpiar el ns. Ej. emisor = comprobante.find('http://www.sat...:Emisor', ns), esto porque ya se tiene el namespace completo el ns
	"""
	prueba = CfdiToDict(path_to_file='factura.xml')
	print(json.dumps(prueba.root, indent=4))
