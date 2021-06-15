import os
import shutil
import pandas as pd
"""
script to manually assign proteins in non_assigned folder, call main 
"""

def main(pdb_id, protein):
    repo_path = os.path.abspath(os.path.join(__file__ ,"../../..","pdb"))
    move_n_del(repo_path, pdb_id, protein)

def move_n_del(repo_path, pdb_id, protein):
    shutil.copytree(os.path.join(repo_path,"not_assigned","SARS-CoV-2",pdb_id),os.path.join(repo_path,protein,"SARS-CoV-2",pdb_id))
    shutil.rmtree(os.path.join(repo_path,"not_assigned","SARS-CoV-2",pdb_id))

def change_database_entry(pdb_id, protein):
    df = pd.read_pickle("main_repo_database.pkl")
    df.loc[df["pdb_id"] == pdb_id, "protein"] = protein
    df.to_pickle("main_repo_database.pkl")
