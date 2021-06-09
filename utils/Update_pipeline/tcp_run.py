import tcp_main
import os
import RMSD
import mk_Alignment_strc_vs_seq as align

"""
executable script for weekly update
"""

repo_path = os.path.abspath(os.path.join(__file__ ,"../../..","pdb"))
#c_new_pdb_lst, changed_prot_list = tcp_main.main()
c_new_pdb_lst = ["7n0s", "7n0i", "7n33", "7ek6", "7eq4", "5sab", "5saa", "5sa4", "5sa6", "5sa5", "5sa8", "5sa7", "5sa9", "5sad", "5sac", "5saf", "5sae", "5sah", "5sag", "5sai", "7djz", "7dk0", "7e8c", "7e8f", "7e7y", "7e88", "7e7x", "7e86", "7cyh", "7cyp"]
changed_prot_list = ["endornase", "leader_protein", "nucleocapsid_protein", "surface_glycoprotein"]
RMSD.main(changed_prot_list, repo_path)
align.main(changed_prot_list, c_new_pdb_lst, repo_path)