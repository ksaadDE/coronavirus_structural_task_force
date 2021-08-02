import os
import shutil
import pandas as pd
import argparse

"""
script to manually assign proteins in non_assigned folder, call main 
"""

# handle input arguments
parser = argparse.ArgumentParser(description='Run manual assignment after weekly update.')
parser.add_argument('-pdb', '--pdb_id', type=str, required=True, help="Give the pdb_id")
parser.add_argument('-p', '--protein', type=str, required=True, help="Give the protein to which the id should be assigned to")
parser.add_argument('-t', '--taxonomy', type=str, required=True, help="Give the taxonomy, either 'SARS-CoV' or 'SARS-CoV-2'")
args = parser.parse_args()

taxo_sars_cov = "SARS-CoV"
taxo_sars_cov_2 = "SARS-CoV-2"

if args.taxonomy != taxo_sars_cov and args.taxonomy != taxo_sars_cov_2:
    exit("ERROR: Wrong taxonomy, check typos!")
taxo_id = args.taxonomy

def main(pdb_id, protein):
    repo_path = os.path.abspath(os.path.join(__file__ ,"../../..","pdb"))
    move_n_del(repo_path, pdb_id, protein)
    change_database_entry(pdb_id, protein)

def move_n_del(repo_path, pdb_id, protein):
    shutil.copytree(os.path.join(repo_path,"not_assigned", taxo_id, pdb_id),os.path.join(repo_path,protein, taxo_id, pdb_id))
    shutil.rmtree(os.path.join(repo_path,"not_assigned", taxo_id, pdb_id))

def change_database_entry(pdb_id, protein):
    df = pd.read_pickle("main_repo_database_" + taxo_id + ".pkl")
    df.loc[df["pdb_id"] == pdb_id, "protein"] = protein
    df.to_pickle("main_repo_database_" + taxo_id + ".pkl")

main(args.pdb_id, args.protein)


