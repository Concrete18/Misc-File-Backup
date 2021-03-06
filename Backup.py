from tkinter import messagebox, filedialog
import datetime as dt
import shutil
import json
import os

class Backup_App:

    def __init__(self):
        with open('config.json') as json_file:
            data = json.load(json_file)
        self.backup_location = data['settings']['backup_destination']
        self.backup_redundancy = data['settings']['backup_redundancy']
        self.backup_targets = data['backup_targets']


    def Delete_Oldest(self):
        '''Deletest the oldest backups so only the newest specified in backup_redundancy is left.'''
        backup_list = []
        dir = self.backup_location
        for file in os.scandir(dir):
            backup_list.append(file.path)
        if len(backup_list) <= self.backup_redundancy:
            print(f'{self.backup_redundancy} or Less Backups.')
            return
        else:
            print(f'More than {self.backup_redundancy} backups.\nDeleting oldest backups now.')
            sorted_list = sorted(backup_list, key=os.path.getctime, reverse=True)
            for i in range(self.backup_redundancy, len(backup_list)):
                shutil.rmtree(sorted_list[i])


    def Backup(self):
        '''Runs a back up of all files and folders from the config.json.'''
        current_time = dt.datetime.now().strftime("Date %m-%d-%y Time %H-%M-%S")
        dest = os.path.join(self.backup_location, current_time)
        os.mkdir(dest)
        for item, loc in self.backup_targets.items():
            base_folder = os.path.join(dest, item)
            final_dest = os.path.join(base_folder, os.path.basename(loc))
            if not os.path.isdir(final_dest):
                os.mkdir(base_folder)
            if os.path.isfile(loc):
                shutil.copy(loc, final_dest)
            else:
                shutil.copytree(loc, final_dest)
            print(f'Backed Up: {item} from {loc}')
            print()


    def Restore(self):
        '''Asks what you want to restore then restores it to its set location.'''
        print('Restore Function Incomplete')
