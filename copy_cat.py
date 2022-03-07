#!/usr/bin/env python3

import os
import re
import sys
import copy
import random
import shutil
import subprocess


class CopyCat:
    """Miau"""

    def __init__(self):
        print('                                                                                ')
        print('$$$$$$\                                     $$\     $$$$$$\             $$\\    ')
        print('$$  __$$\                                   \$$\   $$  __$$\            $$ |    ')
        print('$$ /  \__| $$$$$$\   $$$$$$\  $$\   $$\      \$$\  $$ /  \__| $$$$$$\ $$$$$$\   ')
        print('$$ |      $$  __$$\ $$  __$$\ $$ |  $$ |$$$$\ \$$\ $$ |       \____$$\\_$$  _|  ')
        print('$$ |      $$ /  $$ |$$ /  $$ |$$ |  $$ |\____|$$  |$$ |       $$$$$$$ | $$ |    ')
        print('$$ |  $$\ $$ |  $$ |$$ |  $$ |$$ |  $$ |     $$  / $$ |  $$\ $$  __$$ | $$ |$$\ ')
        print('\$$$$$$  |\$$$$$$  |$$$$$$$  |\$$$$$$$ |    $$  /  \$$$$$$  |\$$$$$$$ | \$$$$  |')
        print(' \______/  \______/ $$  ____/  \____$$ |    \__/    \______/  \_______|  \____/ ')
        print('                    $$ |      $$\   $$ |                                        ')
        print('                    $$ |      \$$$$$$  | A search tag based file copier v0.1    ')
        print('                    \__|       \______/                                         ')
        print('                                                                                ')
        self.work_dir = os.getcwd()
        self.dst_path = os.path.join(os.path.expanduser('~'), 'Downloads', f'kitten_{random.randint(0, 1000)}')
        self.tags = {}
        self.tag_stats = {'copy_option': None,
                          'folder': {'level_up': None,
                                     'new_path': None},
                          'file': {'split_char': None,
                                   'split_start': None,
                                   'split_end': None,
                                   'rename_1': {'old': None, 'new': None}}}

    def __call__(self):
        """Call the cats"""
        try:
            self.tree_view(self.work_dir, 'current directory')
            self.set_file_search_tags()
            self.modify_copy_name()
            self.define_copy_options()
            self.show_option_summary()
            self.run_and_copy()
            self.tree_view(self.dst_path, 'output directory')
            print(f'\nThere was a miaou in {self.dst_path}, better check that out!')
        except KeyboardInterrupt:
            print()
            sys.exit()
        except Exception as error:
            print('Kitty caused some troubles:')
            print(error)
            sys.exit()

    @staticmethod
    def wait_for_yes_no(text: str, styler='') -> bool:
        """Waits for yes and no"""
        while True:
            response = input(f'{styler}{text} [y/n]: ')
            if response.lower() == 'y' or response.lower() == 'yes':
                return True
            if response.lower() == 'n' or response.lower() == 'no':
                return False

    @staticmethod
    def wait_for_char(text: str, styler='') -> str:
        """Waits for char and returns when found"""
        while True:
            response = input(f'{styler}{text}: ')
            if isinstance(response, str) and len(response) == 1:
                return response
            else:
                print(f'{styler}Expected single char, your response: {response}')

    @staticmethod
    def wait_for_int(text: str, styler='') -> int:
        """Waits for int input and returns when found"""
        while True:
            response = input(f'{styler}{text}: ')
            if isinstance(response, str) and response.isdigit():
                return int(response)
            else:
                print(f'{styler}Expected int, your response: {response}')

    def tree_view(self, path: str, text: str) -> None:
        """Show tree view of directory, needs an installed the library tree view"""
        try:
            if self.wait_for_yes_no(f'Visualize {text}') and os.path.exists(path):
                os.chdir(path)
                subprocess.Popen(['clear'])
                process = subprocess.Popen(['tree'])
                process.wait()
        except Exception as error:
            print(error)

    def set_file_search_tags(self) -> None:
        """Define the search tags for the recursive file search"""
        while True:
            tags = input('\nSet search tags (comma separated)(ex: kitty., miau-, milk.txt, etc): ')
            tags = re.sub(',\s+', ',', tags)  # remove all whitespaces after any coma
            tags = tags.split(',')  # string to list
            if self.wait_for_yes_no(f'Accept search tags: {tags}'):
                break
        if tags is not None:  # Init dict with found tags
            for tag in tags:
                self.tags[tag] = copy.deepcopy(self.tag_stats)

    def modify_copy_name(self) -> None:
        """Define the old name part, which will be replaced by new one"""
        if self.wait_for_yes_no(f'Change filenames during the copying?'):
            for tag in self.tags:
                if self.wait_for_yes_no(f"\tChange filenames for '{tag}' (case insensitive):"):
                    self.tags[tag]['file']['rename_1']['old'] = input(f'\tReplace name part [string]: ')
                    self.tags[tag]['file']['rename_1']['new'] = input(f'\twith my new name [string]: ')

    def define_copy_options(self) -> None:
        """Specify the copy per search tag"""
        print('\nCopy options:')
        print('\t1:  Move file in current folder structure')
        print('\t2:  Create new folder structure')
        print('\t3:  Create folder structure from filenames')
        for tag in self.tags:
            while True:
                response = self.wait_for_int(f"Set copy option for '{tag}'", '\n')
                if response == 1:
                    self.define_copy_option_1(tag)
                    break
                if response == 2:
                    self.define_copy_option_2(tag)
                    break
                if response == 3:
                    self.define_copy_option_3(tag)
                    break

    def define_copy_option_1(self, tag: str) -> None:
        """Define in which parent folder the files should be placed"""
        print(f"\tMove file in current folder structure for '{tag}')")
        print(f"\tMove files, 0: same folder, 1: one level up, etc")
        self.tags[tag]['copy_option'] = 1
        self.tags[tag]['folder']['level_up'] = self.wait_for_int(f'Move file by [int]', '\t')

    def define_copy_option_2(self, tag: str) -> None:
        """Define relative path for files"""
        print(f'\tCopy files for {tag} to new folder structure')
        self.tags[tag]['copy_option'] = 2
        self.tags[tag]['folder']['new_path'] = input('\tNew path [str]: ')

    def define_copy_option_3(self, tag: str) -> None:
        """Create folder structure from filename"""
        self.tags[tag]['copy_option'] = 3
        self.define_option_3_split_char(tag)
        self.define_option_3_split_indexes(tag)
        self.test_option_3(tag)

    def define_option_3_split_char(self, tag: str) -> None:
        """Define char to split name in parts"""
        print('\tCreate folder from filename')
        print("\tex: split_char '_', name_start = 1, name_end = 2 ")
        print("\t    filename 'kitty_goes_wild.txt' would create folder name 'goes_wild'")
        self.tags[tag]['file']['split_char'] = self.wait_for_char('Set split char [char]', '\n\t')

    def define_option_3_split_indexes(self, tag: str) -> None:
        """Define which parts are used for the folder name"""
        split_start = self.wait_for_int(f'Set name start [int]', '\t')
        split_end = self.wait_for_int(f'Set name end [int]', '\t')
        if split_start > split_end:
            print('\n\tname_start has to be smaller than than name_end, try again!')
            self.define_copy_option_3(tag)
        else:
            self.tags[tag]['file']['split_start'] = split_start
            self.tags[tag]['file']['split_end'] = split_end + 1

    def test_option_3(self, tag: str) -> None:
        """Let the user test the split_char and split_indexes on test inputs"""
        test = True
        while test:
            run_test = self.wait_for_yes_no('\n\tTest folder creation?')
            if run_test:
                print('\tTest mode (reset params: reset | go on: exit)')
                while True:
                    test_name = input('\n\t\tProvide any test name [str]: ')
                    if test_name == 'reset':
                        self.define_option_3_split_char(tag)
                        self.define_option_3_split_indexes(tag)
                        print('')
                    elif test_name == 'exit':
                        test = False
                        break
                    elif isinstance(test_name, str):
                        try:
                            test_name = test_name.split('.')[0]  # bye bye file types
                            split_char = self.tags[tag]['file']['split_char']
                            splitted_parts = test_name.split(split_char)
                            split_start = self.tags[tag]['file']['split_start']
                            split_end = self.tags[tag]['file']['split_end']
                            folder_name = split_char.join(splitted_parts[split_start:split_end])
                            print(f'\t\tWould result in folder name: {folder_name}')
                        except Exception as error:
                            print(f'\t\t{error}')
            else:
                break

    def show_option_summary(self) -> None:
        """Show a brief copy summary"""
        print('\nCopy summary')
        for tag in self.tags:
            copy_option = 'error'
            copy_info = 'error'
            if self.tags[tag]['copy_option'] == 1:
                copy_option = 'Clone folder structure'
                copy_info = f"copy files {self.tags[tag]['folder']['level_up']} folder/s up"
            elif self.tags[tag]['copy_option'] == 2:
                copy_option = 'Copy to new folder structure'
                copy_info = f"copy files to {self.tags[tag]['folder']['new_path']}"
            elif self.tags[tag]['copy_option'] == 3:
                copy_option = 'Copy files to filename generated folders'
                copy_info = f"uses split char '_' and names from {self.tags[tag]['file']['split_start']} to " \
                            f"{self.tags[tag]['file']['split_end']-1}"
            print('{0:<15} {1:<15} --> {2:<15}'.format(tag, copy_option, copy_info))

    @staticmethod
    def get_parent_dir(path: str, level: int) -> str:
        """Move one or more folders up"""
        for i in range(level):
            path = os.path.dirname(path)
        return path

    @staticmethod
    def modify_file_name(file: str, tag_data: dict) -> str:
        """Replace old part with new if present"""
        if tag_data['file']['rename_1']['old'] is not None and tag_data['file']['rename_1']['new'] is not None:
            return re.sub(tag_data['file']['rename_1']['old'], tag_data['file']['rename_1']['new'], file, re.IGNORECASE)
        return file

    def option_1(self, root: str, file: str, tag_data: dict) -> None:
        """Copy files to same folder (clone) structure but in a different position"""
        path = self.get_parent_dir(root, tag_data['folder']['level_up'])
        path = path.replace(self.work_dir, '')
        path = path.lstrip(os.sep)
        dst_folder_path = os.path.join(self.dst_path, path)
        os.makedirs(dst_folder_path, exist_ok=True)
        mod_file = self.modify_file_name(file, tag_data)
        shutil.copy2(os.path.join(root, file), os.path.join(dst_folder_path, mod_file))

    def option_2(self, root: str, file: str, tag_data: dict) -> None:
        """Copy files to new folder structure"""
        new_path = tag_data['folder']['new_path'].lstrip(os.sep)
        new_path = new_path.rstrip(os.sep)
        dst_folder_path = os.path.join(self.dst_path, new_path)
        os.makedirs(dst_folder_path, exist_ok=True)
        mod_file = self.modify_file_name(file, tag_data)
        shutil.copy2(os.path.join(root, file), os.path.join(dst_folder_path, mod_file))

    def option_3(self, root: str, file: str, tag_data: dict) -> None:
        """Create new folders which names are based on the files """
        original_name = copy.deepcopy(file)
        file = file.split('.')[0]  # bye bye file types
        file = file.split(tag_data['file']['split_char'])
        file = file[tag_data['file']['split_start']:tag_data['file']['split_end']]
        folder_name = tag_data['file']['split_char'].join(file)
        dst_folder_path = os.path.join(self.dst_path, folder_name)
        os.makedirs(dst_folder_path, exist_ok=True)
        mod_file = self.modify_file_name(original_name, tag_data)
        shutil.copy2(os.path.join(root, original_name), os.path.join(dst_folder_path, mod_file))

    def run_and_copy(self) -> None:
        """Let the cats out and do some copying"""
        print(f'\nExport folder will be {self.dst_path}')
        response = self.wait_for_yes_no('Start with current options')
        if response:
            for tag in self.tags:
                for root, dirs, files in os.walk(self.work_dir):
                    for file in files:
                        if tag in file:
                            if self.tags[tag]['copy_option'] == 1:
                                self.option_1(root, file, self.tags[tag])

                            if self.tags[tag]['copy_option'] == 2:
                                self.option_2(root, file, self.tags[tag])

                            if self.tags[tag]['copy_option'] == 3:
                                self.option_3(root, file, self.tags[tag])
        else:
            print('Nothing happened, the cat ran away')


if __name__ == '__main__':
    cc = CopyCat()
    cc()
