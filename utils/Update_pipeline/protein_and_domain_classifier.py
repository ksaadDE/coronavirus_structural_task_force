#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 17:31:27 2021

This script iterates through all entries in a certain folder of a protein 
and classifies each PDB to the corresponding domain.
Classification of domains is based on a sequence alignment.
You may have to create a fasta file first, which contains all sequences of
the domains.
At the end, an xcel sheet is given out, containing all relevant information.

@author: localadmin
"""

import os
from os.path import join
import argparse
import gemmi
from Bio import SeqIO
import xlsxwriter
import sys


def main(taxonomy, protein):
    """
    Main script.

    Parameters
    ----------
    taxonomy : String
        either SARS-CoV or SARS-CoV-2.
    protein : String
        Name of the protein.

    Returns
    -------
    None.
    """

    taxo_sars_cov = "SARS-CoV"
    taxo_sars_cov_2 = "SARS-CoV-2"
    
    working_dir = os.getcwd()
    
    if taxonomy != taxo_sars_cov and taxonomy != taxo_sars_cov_2:
        exit("ERROR: Wrong taxonomy, check typos!")
    
    try:
        os.chdir(join("..", "..", "pdb", protein, taxonomy))
    except FileNotFoundError:
        exit("ERROR: path not found. Check your -p input.")
    print("work with files from:")
    print(os.getcwd())
    
    # load domain sequences from fasta file
    try:
        fasta_sequences = SeqIO.parse(open(join(os.getcwd(), "sequence_domain_info.fasta")),'fasta')
    except FileNotFoundError:
        exit("ERROR: no file called 'sequence_domain_info.fasta' found in target folder.")
    fasta_seq_iter = []
    for fasta in fasta_sequences:
        domain_name, domain_sequence = fasta.id, str(fasta.seq)
        fasta_seq_iter.append((domain_name, domain_sequence))
    
    # lists for final results
    entries_and_domains = []
    
    print("iterate over entries...")
    # iterate over all entries in dir
    for entry in os.listdir():
        if os.path.isdir(join(os.getcwd(), entry)):
            #print(entry)
            entry_pdb_path = join(os.getcwd(), entry, entry + ".pdb")
            # load model from pdb
            try:
                pdb_entry = gemmi.read_pdb(entry_pdb_path)
            except:
                entry_pdb_path = join(os.getcwd(), entry, entry + "_false.pdb")
                pdb_entry = gemmi.read_pdb(entry_pdb_path)
            model = pdb_entry[0]
            # for each chain, load sequence if polypeptide
            best_chain_score = -1000
            best_chain_domain = "None"
            for x in range(len(model)):
                if (model[x].whole().check_polymer_type() == gemmi.PolymerType.PeptideL
                    or model[x].whole().check_polymer_type() == gemmi.PolymerType.Unknown):
                    chain_sequence = model[x].whole().make_one_letter_sequence().replace('-', '')
                    # do sequence alignment for each sequence from fasta and track best
                    best_score = -1000
                    best_domain = "None"
                    for fasta in fasta_seq_iter:
                        domain_name, domain_sequence = fasta
                        result = gemmi.align_string_sequences(list(chain_sequence), list(domain_sequence), [])
                        if result.score > best_score:
                            best_score = result.score
                            best_domain = domain_name
                    
                    #print(best_domain + " " + str(best_score))
                    # keep track of best chain
                    if best_score > best_chain_score:
                        best_chain_score = best_score
                        best_chain_domain = best_domain
            #print(best_chain_domain + " " + str(best_chain_score))
            # check if domain was already added to final results
            save_entry = [entry, pdb_entry.resolution, 0, 0, 0]
            for key, value in pdb_entry.info.items():
                if key == "_struct.title":
                    save_entry[2] = value
                if key == "_exptl.method":
                    save_entry[3] = value
                if key == "_pdbx_database_status.recvd_initial_deposition_date":
                    save_entry[4] = value
            
            domain_added = False
            for result_list in entries_and_domains:
                if result_list[0] == best_chain_domain:
                    domain_added = True
                    result_list[1].append(save_entry)
                    break
            if not domain_added:
                entries_and_domains.append([best_chain_domain, [save_entry]])
            
    # print out results
    total = 0
    for result_list in entries_and_domains:
        print(result_list[0] + ": " + str(len(result_list[1])))
        total += len(result_list[1])
    print("total: " + str(total))
    
    # write excel
    workbook_path = join(os.getcwd(), "domains_and_infos_of_" + protein + '.xlsx')
    workbook = xlsxwriter.Workbook(workbook_path)
    print("wrote results to:")
    print(workbook_path)
    
    for result_list in entries_and_domains:
        worksheet = workbook.add_worksheet(result_list[0])
        worksheet.write(0, 0, "PDB")
        worksheet.write(0, 1, "resolution")
        worksheet.write(0, 2, "title")
        worksheet.set_column('C:C', 110)
        worksheet.write(0, 3, "method")
        worksheet.set_column('D:D', 20)
        worksheet.write(0, 4, "date")
        worksheet.set_column('E:E', 12)
        row = 1
        for entry in result_list[1]:
            for x in range(5):
                worksheet.write(row, x, entry[x])
            row += 1
    
    workbook.close()

if __name__ == '__main__':
    # handle input arguments
    parser = argparse.ArgumentParser(description='Run weekly update.')
    parser.add_argument('-t', '--taxonomy', type=str, required=True, help="Give the taxonomy, either 'SARS-CoV' or 'SARS-CoV-2'")
    parser.add_argument('-p', '--protein', type=str, required=True, help="Give the protein folder name")
    args = parser.parse_args()
    
    main(args.taxonomy, args.protein)
