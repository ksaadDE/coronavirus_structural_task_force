#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 14:07:29 2021

This contains functions used to analyze the data frame or to fix bugs.

@author: Maximilian Edich
"""

import os
import pandas as pd

df = pd.read_pickle("main_repo_database_SARS-CoV-2.pkl")



# # # Remove duplicates
def remove_duplicates():
    # locate duplicates
    duplicates = []
    for entry in df['pdb_id']:
        if len(df.loc[df['pdb_id'] == entry]) != 1:
            if not (entry in duplicates):
                duplicates.append(entry)
    print(duplicates)
    print(len(duplicates))
    
    print(len(df))
    
    # drop duplicates
    nf = df.drop_duplicates()
    
    for dupe in duplicates:
        prot = nf.loc[nf['pdb_id'] == dupe]
        print(prot)
    
    print(len(nf))
    nf.to_pickle("main_repo_database_SARS-CoV-2.pkl")


# # # Change path of not assigned
def update_path_of_not_assigned():
    # find entries with 'not_assigned' in their path
    for entry in df['path_in_repo']:
        if str(entry).find('not_assigned') >= 0:
            prot = df.loc[df['path_in_repo'] == entry, 'protein']
            pdb_id = df.loc[df['path_in_repo'] == entry, 'pdb_id']
            print(entry)
            print(pdb_id)
            # get value of protein
            for value in prot:
                print(value)
                if value != 'not_assigned':
                    new_path = os.path.join("pdb", value, "SARS-CoV-2", str(pdb_id))
                    print(new_path)
            
            print()


update_path_of_not_assigned()



