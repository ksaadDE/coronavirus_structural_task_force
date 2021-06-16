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

repo_path = os.path.abspath(os.path.join(__file__ ,"../../..","pdb"))
"""print("Searching for new and changed structures")
c_new_pdb_lst, changed_prot_list = tcp_main.main(taxonomy, taxo)
print("Doing sequence aligntment")
align.main(changed_prot_list, c_new_pdb_lst, repo_path)
print("Calculating RMSD")"""
changed_prot_list = ["3c_like_proteinase", "surface_glycoprotein", "protein_e", "nsp2"]
RMSD.main(changed_prot_list, repo_path)