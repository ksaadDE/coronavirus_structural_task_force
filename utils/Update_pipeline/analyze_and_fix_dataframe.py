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
    not_assigned = []
    for entry in df['path_in_repo']:
        if str(entry).find('not_assigned') >= 0:
            prot = df.loc[df['path_in_repo'] == entry, 'protein'].iloc[0]
            pdb_id = df.loc[df['path_in_repo'] == entry, 'pdb_id'].iloc[0]
            print(entry)
            
            if prot == "not_assigned":
                # pdb has to be assigned manually
                not_assigned.append(pdb_id)
            else:
                # update path
                new_path = os.path.join("pdb", prot, "SARS-CoV-2", pdb_id)
                print(new_path)
                df.loc[df["pdb_id"] == pdb_id,"path_in_repo"] = new_path
                print(df.loc[df["pdb_id"] == pdb_id,"path_in_repo"])
            print()
            
    print(len(not_assigned))
    print(not_assigned)
    print("these pdbs have to be assigned manually")
    df.to_pickle("main_repo_database_SARS-CoV-2.pkl")
    


update_path_of_not_assigned()



