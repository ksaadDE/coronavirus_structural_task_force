#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 17:04:23 2021

@author: Maximilian Edich
"""

import os

# check if script is located in utils
if os.path.basename(os.getcwd()) != "utils":
    exit("ERROR: place and launch the script from utils folder!")


pdb_dir = os.path.abspath(os.path.join(os.getcwd(), "..", "pdb"))

# iterate down the folder tree until correct README.md is found
for protein in os.listdir(pdb_dir):
    protein_dir = os.path.join(pdb_dir, protein)
    if not os.path.isdir(protein_dir):
        continue
    for taxonomy in os.listdir(protein_dir):
        taxonomy_dir = os.path.join(protein_dir, taxonomy)
        if not os.path.isdir(taxonomy_dir):
            continue
        for pdb_id in os.listdir(taxonomy_dir):
            if not os.path.isdir(os.path.join(taxonomy_dir, pdb_id)):
                continue
            # look into README and check if it is from cryo EM
            read_me_path = os.path.join(taxonomy_dir, pdb_id, "README.md")
            try:
                file = open(read_me_path, 'r')
                content = file.read()
                file.close()
            except FileNotFoundError:
                print("ERROR: README.md not found in:")
                print(read_me_path)
                print()
                continue
            
            if content.find("**Method**: Cryo-EM") > -1:
                # is cryo
                print("Obtained from Cryo EM:")
                print(read_me_path)
                print("Haruspex available?")
                print(content.find("## HARUSPEX results") > -1)
                print()
                
                
            
    