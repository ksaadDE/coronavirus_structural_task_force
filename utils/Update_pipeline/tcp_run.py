import tcp_main
import os
import RMSD
import mk_Alignment_strc_vs_seq as align

"""
executable script for weekly update
"""

# taxonomy name used in PDB search
taxonomy = "Severe acute respiratory syndrome coronavirus 2"
# taxonomy name used to name files
taxo = "SARS-CoV-2"

#These are used to only return pdb entries of taxonomy_id and exlcude everything in negate_taxonomy_id
sars_cov_1_id = "694009" #SARS-CoV-1
sars_cov_2_id = "2697049" #SARS-CoV-2
taxonomy_id = sars_cov_2_id
negate_taxonomy_id = sars_cov_1_id

# catch possible typo
if taxonomy_id == negate_taxonomy_id:
    exit("ERROR: Taxonomy ids are equal!")

repo_path = os.path.abspath(os.path.join(__file__ ,"../../..","pdb"))
print("Searching for new and changed structures")
c_new_pdb_lst, changed_prot_list = tcp_main.main(taxonomy_id, negate_taxonomy_id, taxo)
print("Doing sequence aligntment")
align.main(changed_prot_list, c_new_pdb_lst, repo_path, taxo)
print("Calculating RMSD")
RMSD.main(changed_prot_list, repo_path)
