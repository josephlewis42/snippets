''' Counts the number of words in an XML file.

Copyright 2015 Joseph Lewis III <joseph@josephlewis.net>
Public Domain

'''
from xml.etree import cElementTree

def dump_xml_data(data):
	root = cElementTree.fromstring(data)
	data = "".join([s for s in root.itertext()])
	return len(data.split())


with open("myfile.xml") as fd:
	print(dump_xml_data(fd.read()))
