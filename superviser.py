#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
import logging
import argparse


# Annonce la création d'un dossier.
# @param name nom du dossier créé
def folderAdded(name):
    logging.info("The folder " + name + " has been added" + ".")

# Annonce la supression d'un dossier.
# @param name nom du dossier supprimé
def folderDeleted(name):
    logging.info("The folder " + name + " has been deleted" + ".")

# Annonce le changement de nom d'un dossier.
# @param old ancien nom du dossier
# @param new nouveau nom du dossier
def folderRenamed(old_name, new_name):
    logging.info("The folder " + old_name + " has been moved to " + new_name + ".")

# Annonce la modification d'un fichier.
# @param name nom du fichier modifié
def fileModified(name):
    logging.info("The  file  " + name + " has been modified" + ".")

# Annonce la création d'un ficher
# @param name nom du fichier créé
def fileAdded(name):
    logging.info("The  file  " + name + " has been added" + ".")

# Annonce la suppression d'un fichier
# @param name nom du fichier supprimé
def fileDeleted(name):
    logging.info("The  file  " + name + " has been deleted" + ".")

# Annonce le changement de nom d'un fichier.
# @param old ancien nom du fichier
# @param new nouveau nom du fichier
def fileRenamed(old_name, new_name):
    logging.info("The  file  " + old_name + " has been moved to " + new_name + ".")

# Compare deux dictionnaires de dossiers pour en trouver les différences
# @param old ancien état
# @param new nouvel état
def folderAnalyse(old_state, new_state):
    for node in new_state.keys():
        if node in old_state.keys():
            old_name = old_state[node]
            new_name = new_state[node]
            if old_name != new_name:
                folderRenamed(old_name, new_name)
        else:
            folderAdded(new_state[node])
    for node in old_state.keys():
        if node not in new_state.keys():
            folderDeleted(old_state[node])

# Compare deux dictionnaires de fichiers pour en trouver les différences
# @param oldPath ancier état
# @param newPath nouvel état
def filesAnalyse(old_state, new_state):
    for node in new_state.keys():
        if node in old_state.keys():
            old_name = old_state[node][0]
            new_name = new_state[node][0]
            if new_name == old_name:
                old_time = old_state[node][1]
                new_time = new_state[node][1]
                if old_time != new_time:
                    fileModified(new_name)
            else:
                fileRenamed(old_name, new_name)
        else:
            fileAdded(new_state[node][0])
    for node in old_state.keys():
        if node not in new_state.keys():
            fileDeleted(old_state[node][0])

# Remplie un dictionnaire de fichiers sour la forme "nom" -> timestamp dernière édition
# @param dictionary dictionnaire de fichiers à compléter
# @param folder nom du dossier contenant le fichier
# @param files liste des fichiers à mettre dans le dictionnaire
def fill_files_dictionary(dictionary, folder, files) :
    for file in files :
        full_path = os.path.join(folder, file)
        # Récupération du timestamp de dernière modification
        timestamp = int(os.path.getmtime(full_path))
        inode = int(os.stat(full_path).st_ino)
        dictionary[inode] = (full_path, timestamp)

# Remplie un dictionnaire de dossiers sous la forme "nom" -> dictionnaire des fichiers contenus
# @param dictionary_folders dictionnaire de dossiers à remplir
# @param dictionary_files dictionnaire des fichiers à remplir
# @param folder dossier source
# @param step_init échelon de sous-dossier initial
# @param step_max échelon de sous-dossier maximal
def fill_directories_dictionary(dictionary_folders, dictionary_files, folder, step_init, step_max) :
    for root, dirs, files in os.walk(folder):
        # Si on est au niveau de récursivité maximal, on vide la liste des sous dossiers pour stoper le walk
        if root.count(str(os.sep)) >= step_max + step_init and step_max != 0 :
            del dirs[:]
        fill_files_dictionary(dictionary_files, root, files)
        inode = int(os.stat(root).st_ino)
        dictionary_folders[inode] = root

# Lance le programme de surveillance du dossier
# @param args Namespace Les arguments du programme.
def run(args) :
    old_state = ({}, {})
    step_init = str(args.directory).count(str(os.sep))
    fill_directories_dictionary(old_state[0], old_state[1], args.directory, step_init, args.recursive)
    while 1 == 1:
        time.sleep(args.time)
        new_state = ({}, {})
        fill_directories_dictionary(new_state[0], new_state[1], args.directory, 0, args.recursive)
        folderAnalyse(old_state[0], new_state[0])
        filesAnalyse(old_state[1], new_state[1])
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