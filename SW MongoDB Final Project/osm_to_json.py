# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 18:34:07 2015

@author: Seth
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way":
        node["id"] = element.attrib["id"]
        node["type"] = element.tag
        node["visible"] = element.get("visible","false")
        
        #"CREATED" ARRAY
        node["created"] = {}
        node["created"]["version"] = element.attrib["version"]
        node["created"]["changeset"] = element.attrib["changeset"]
        node["created"]["timestamp"] = element.attrib["timestamp"]
        node["created"]["user"] = element.attrib["user"]
        node["created"]["uid"] = element.attrib["uid"]
        
        #CREATE "POS"
        node["pos"] = []
        if element.tag == "node":
            node["pos"].append(float(element.attrib["lat"]))
            node["pos"].append(float(element.attrib["lon"]))
        
        #"ADDRESS" ARRAY
        node["address"] = {}        
        for tag in element.findall("tag"):
            if tag.attrib["k"] == "addr:housenumber":
                node["address"]["housenumber"] = tag.attrib["v"]
            if tag.attrib["k"] == "addr:street":
                node["address"]["street"] = tag.attrib["v"]   
        
        #Other info        
            if tag.attrib["k"] == "amenity":
                node["amenity"] = tag.attrib["v"]    
            if tag.attrib["k"] == "cuisine":
                node["cuisine"] = tag.attrib["v"] 
            if tag.attrib["k"] == "name":
                node["name"] = tag.attrib["v"] 
            if tag.attrib["k"] == "phone":
                node["phone"] = tag.attrib["v"] 
        
        #DELETE "ADDRESS" DICTIONARY IF EMPTY
        if node["address"] == {}:
            del node["address"]
        
        #"NODE_REFS" ARRAY FOR "WAY" ELEMENTS
        if element.tag == "way":
            node["node_refs"] = []
            for nd in element.findall("nd"):
                node["node_refs"].append(nd.attrib["ref"])
            
            
            
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
    
def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map("C:\Users\Seth\Downloads\chicago_illinois.osm", pretty=False)
    
    #pprint.pprint(data)

if __name__ == "__main__":
    test()    