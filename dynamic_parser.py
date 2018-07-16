import xml.etree.ElementTree as ET
import json


class XMLToDict(object):
	""" Clase para parsear un XML y convertirlo
		en un diccionario con atributos y nodos.
		Con el modulo json se puede convertir facilmente del diccionario
		a json
	"""
	root = {}
	ns = None
	childrens = None
	force_array = None
	exclude_attributes = None
	
	def __init__(self, path_to_file="", xml_string = "", force_array = None, exclude_attributes = None):
		"""
		Si usan el parametro 'force_array', en los nodos que tengan 'childrens', 
		se forzara que dicho nodo sea tipo array.
		El atributo final de la clase es un tipo list, si el parametro que se pasa
		no es list, es convertido a este al momento de la asignacion.
		"""
		#if path_to_file != '' and xml_string != '':
		if not bool(path_to_file) ^ bool(xml_string):
			raise Exception("Solo puede indicar un medio para cargar el XML a parsear")
		if path_to_file:
			tree = ET.parse(path_to_file)
			self.xml = tree.getroot()
		else:
			self.xml = ET.fromstring(xml_string)
		if force_array:
			self.force_array = force_array
			if not isinstance(force_array, list):
				self.force_array = [force_array]
		if exclude_attributes:
			self.exclude_attributes = exclude_attributes
			if not isinstance(exclude_attributes, list):
				self.exclude_attributes = [exclude_attributes]
		self.convert()
	
	def convert(self):
		name_element = self.__clean_namespace(self.xml.tag)
		self.root[name_element] = self.__clean_attributes(self.xml.attrib)
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
		element_dict = self.__clean_attributes(attrs)
		if len(element.getchildren()) > 0:
			repeated_element = self.__check_repeated_childrens(element)
			if repeated_element or name_element in self.force_array:
				element_list = []
				for e in element.getchildren():
					subelement_dict = {}
					name, dicc = self.__parse_element(e)
					subelement_dict[name] = dicc
					element_list.append(subelement_dict)
				element_dict = element_list
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
	
	def __clean_attributes(self, attributes):
		if self.exclude_attributes:
			for attr in self.exclude_attributes:
				if attr in attributes:
					del attributes[attr]
		return attributes


if __name__ == '__main__':
	prueba = XMLToDict(path_to_file='cfdi.xml', force_array = ['Conceptos'], exclude_attributes = ['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'])
	print(json.dumps(prueba.root, indent=4))
