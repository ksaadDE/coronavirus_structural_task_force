#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 17:31:27 2021

This script iterates through all entries in a certain folder of a protein 
and classifies each PDB to the corresponding domain.
Classification of domains is based on a sequence alignment.
You may have to create a fasta file first, which contains all sequences of
the domains.

@author: localadmin
"""

import os
from os.path import join
import argparse
import gemmi
from Bio import SeqIO

# handle input arguments
parser = argparse.ArgumentParser(description='Run weekly update.')
parser.add_argument('-t', '--taxonomy', type=str, required=True, help="Give the taxonomy, either 'SARS-CoV' or 'SARS-CoV-2'")
parser.add_argument('-p', '--protein', type=str, required=True, help="Give the protein folder name")
args = parser.parse_args()

taxo_sars_cov = "SARS-CoV"
taxo_sars_cov_2 = "SARS-CoV-2"

if args.taxonomy != taxo_sars_cov and args.taxonomy != taxo_sars_cov_2:
    exit("ERROR: Wrong taxonomy, check typos!")

try:
    os.chdir(join("..", "pdb", args.protein, args.taxonomy))
except FileNotFoundError:
    exit("ERROR: path not found. Check your -p input.")
print("work with files from:")
print(os.getcwd())

# load domain sequences from fasta file
fasta_sequences = SeqIO.parse(open(join(os.getcwd(), "sequence_domain_info.fasta")),'fasta')
fasta_seq_iter = []
for fasta in fasta_sequences:
    domain_name, domain_sequence = fasta.id, str(fasta.seq)
    fasta_seq_iter.append((domain_name, domain_sequence))

# lists for final results
entries_and_domains = []

doit = ['5rvv', '5rvp', '7nfv', '6wen', '5rvm', '5rvt', '7kxb', '6wey', '5rvu', '7kqw', '6wrh', '7kg3', '5rvn', '5rvq', '7d6h', '6wcf', '5rvj', '5rvr', '7kr0', '7bf4', '7ofu']
print(len(doit))

print("iterate over entries...")
# iterate over all entries in dir
for entry in os.listdir():
    if os.path.isdir(join(os.getcwd(), entry)) and doit.count(entry) > 0:
        entry_pdb_path = join(os.getcwd(), entry, entry + ".pdb")
        print(entry_pdb_path)
        # load model from pdb
        model = gemmi.read_pdb(entry_pdb_path)[0]
        # for each chain, load sequence if polypeptide
        best_chain_score = -1000
        best_chain_domain = "None"
        print(len(model))
        for x in range(len(model)):
            print(model[x].whole().check_polymer_type())
            print()
            if model[x].whole().check_polymer_type() == gemmi.PolymerType.PeptideL:
                chain_sequence = model[x].whole().make_one_letter_sequence()
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
        domain_added = False
        for result_list in entries_and_domains:
            if result_list[0] == best_chain_domain:
                domain_added = True
                result_list[1].append(entry)
                break
        if not domain_added:
            entries_and_domains.append([best_chain_domain, [entry]])
        
print(entries_and_domains)
for result_list in entries_and_domains:
    print(result_list[0] + " " + str(len(result_list[1])))
