#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
import logging
import argparse

def Ajoutdossier(nom):
    logging.info("le dossier " + nom +" a été ajouté")

def Suppressiondossier(nom):
    logging.info("le dossier "+nom+" a été supprimé")

def Modification(nom):
    logging.info("le fichier "+nom+" a été modifié")

def Ajoutfichier(nom):
    logging.info("le fichier "+nom+" a été ajouté")

def Suppressionfichier(nom):
    logging.info("le fichier "+nom+" a été supprimé")

def Analysedossier(ancien, nouveau):
    for path in nouveau.keys():
        if path in ancien.keys():
            Comparerfichier(ancien[path], nouveau[path])
        else :
            Ajoutdossier(path)
    for path in ancien.keys():
        if path not in nouveau.keys():
            Suppressiondossier(path)

def Comparerfichier(ancienpath, nouveaupath):
    for nom in nouveaupath.keys():
        if nom in ancienpath.keys():
            if nouveaupath[nom] != ancienpath[nom]:
                Modification(nom)
        else :
            Ajoutfichier(nom)
    for nom in ancienpath.keys():
        if nom not in nouveaupath.keys():
            Suppressionfichier(nom)

def fill_files_dictionary(dictionary, folder, files) :
    for file in files :
        full_path = os.path.join(folder, file)
        timestamp = int(os.path.getmtime(full_path))
        dictionary[file] = timestamp

def fill_directories_dictionary(dictionary, folder, step_init, step_max) :
    for root, dirs, files in os.walk(folder):
        if root.count(str(os.sep)) >= step_max + step_init and step_max != 0 :
            del dirs[:]
        files_dictionary = {}
        fill_files_dictionary(files_dictionary, root, files)
        dictionary[root] = files_dictionary

# Lance le programme de surveillance du dossier
# @param args Namespace Les arguments du programme.
def run(args) :
    old_state = {}
    step_init = str(args.directory).count(str(os.sep))
    fill_directories_dictionary(old_state, args.directory, step_init, args.recursive)
    while 1 == 1:
        time.sleep(args.time)
        new_state = {}
        fill_directories_dictionary(new_state, args.directory, 0, args.recursive)
        Analysedossier(old_state, new_state)
        old_state = new_state



# Définie les arguments requis et parse ceux indiqués par l'utilisateur.
# @return Namespace args
def parse_arguments() :
    parser = argparse.ArgumentParser(prog='FolderSuperviser', description='This program will let you know every addition, deletion, and modification within a specified folder.')
    parser.add_argument('-d', '--directory', help='The directory you want to supervise', type=str)
    parser.add_argument('-l', '--log', help='The log file.', type=str)
    parser.add_argument('-t', '--time', help='Frequency of folder check (in seconds).', type=int, default=1)
    parser.add_argument('-r', '--recursive', help='Depth of recursive folder check. 0 = unlimited.', type=int, default=0)
    return parser.parse_args()

# Vérifie que les dossiers à superviser et pour le fichier de log existent.
# @param args Namespace Les arguments du programme.
def check_arguments(args) :
    check = True
    if not os.path.isdir(args.directory) :
        print('Error : The directory you want to supervise does not exist.')
        check = False
    if not os.path.exists(args.log) or os.path.isdir(args.log):
        print('Error : The log file does not exist.')
        check = False
    if args.time <= 0 :
        print('You cannot specify a frequency inferior or equal to 0.')
        check = False
    if args.recursive < 0 :
        print('You cannot specify a recursivity level inferior to 0.')
        check = False
    return check

# Initialise le fichier de logs.
# @param log_file str Le fichier où doivent être enregistrées les logs.
def init_log_file(log_file) :
    logging.basicConfig(filename=log_file, datefmt='%d/%m/%Y-%H:%M:%S', format='%(asctime)s %(levelname)s %(message)s', filemode='w', level=logging.DEBUG)
    logging.info('Folder superviser started.')

#Fonction principale du programme.
def main() :
    args = parse_arguments()
    if check_arguments(args) :
        init_log_file(args.log)
        run(args)

main()