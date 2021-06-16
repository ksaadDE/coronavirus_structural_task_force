import tcp_main
import os
import RMSD
import mk_Alignment_strc_vs_seq as align

"""
executable script for weekly update
"""

repo_path = os.path.abspath(os.path.join(__file__ ,"../../..","pdb"))
c_new_pdb_lst, changed_prot_list = tcp_main.main()
print("Sequence:")
align.main(changed_prot_list, c_new_pdb_lst, repo_path)
print("RMSD:")
#RMSD.main(changed_prot_list, repo_path)