# -*- coding: utf-8 -*-
"""
Created on Sat Mar 07 14:43:25 2015

@author: Seth
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "C:\Users\Seth\Downloads\chicago_illinois.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Blvd": "Boulevard",
            "Ct": "Court",
            "Ct.": "Court",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Rd": "Road",
            "RD": "Road",
            "st": "Street",
            }


def change_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            update_name(street_name,mapping)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    change_street_type(street_types, tag.attrib['v'])
    return street_types


def update_name(name, mapping):
    last_word = name.rsplit(None, 1)[-1]
    if last_word in mapping:
        restof_name = name[0:len(name)-len(last_word)]
        name = restof_name + mapping[last_word]
    return name


def main():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"

if __name__ == '__main__':
    main()