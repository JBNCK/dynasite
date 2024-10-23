#!/usr/bin/python3
import platform
import os
from tkinter import *
from tkinter import ttk
import ast

project_list = []

print(f"{platform.system()} system detected")
if platform.system() == 'Windows':
    HOME_PATH = os.environ['USERPROFILE']
    FOLDER_SEPARATOR = '\\'
    print(f"User/Home folder: {HOME_PATH}")
    print(f"Folder separator: {FOLDER_SEPARATOR}")
    DEFAULT_EDITOR = "NOTEPAD.exe"
elif platform.system() == 'Linux':
    HOME_PATH = os.environ['HOME']
    FOLDER_SEPARATOR = '/'
    print(f"User/Home folder: {HOME_PATH}")
    print(f"Folder separator: {FOLDER_SEPARATOR}")
    DEFAULT_EDITOR = ""
else:
    print(f"Unsupported Operating System: '{platform.system()}'")

PROGRAM_FOLDER = '.dynasite'
PROGRAM_CONFIG_FILE = 'config.json'
PROGRAM_FULL_PATH = f'{HOME_PATH}{FOLDER_SEPARATOR}{PROGRAM_FOLDER}'
PROGRAM_FULL_CONFIG_PATH = f'{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{PROGRAM_CONFIG_FILE}'

DEFAULT_CONFIG = {
    "remote_json_path": "",
    "default_repo_address": ""
}

def check_files():
    if os.path.isdir(PROGRAM_FULL_PATH):
        print(f"Program folder found under: {PROGRAM_FULL_PATH}")
    else:
        print("Couldn't find program folder, creating...")
        os.makedirs(PROGRAM_FULL_PATH)
    if os.path.isfile(PROGRAM_FULL_CONFIG_PATH):
        print(f"Config file found under: {PROGRAM_FULL_CONFIG_PATH}")
    else:
        print("Couldn't find config file, creating...")
        f = open(PROGRAM_FULL_CONFIG_PATH, "w")
        f.write(str(DEFAULT_CONFIG))
        f.close()
        
def edit_config():
    os.system(f"{DEFAULT_EDITOR} {PROGRAM_FULL_CONFIG_PATH}")

def load_json():
    project_list = []
    project_selector.set('')
    f = open(PROGRAM_FULL_CONFIG_PATH, "r")
    config = f.read()
    config = ast.literal_eval(config)
    f.close()

    json_file_name = config['remote_json_path']
    json_slash = json_file_name.rfind("/")
    json_slash += 1
    json_file_name = json_file_name[json_slash:]

    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "r")
    projects = f.read()
    projects = ast.literal_eval(projects)
    for project in projects:
        project_list.append(project['title'])
    print(project_list)

    project_selector.config(values=project_list)

    f.close()

def download_remote_json():
    f = open(PROGRAM_FULL_CONFIG_PATH, "r")
    config = f.read()
    config = ast.literal_eval(config)
    os.system(f"scp {config['remote_json_path']} {PROGRAM_FULL_PATH}")
    f.close()

    load_json()

def upload_remote_json():
    f = open(PROGRAM_FULL_CONFIG_PATH, "r")
    config = f.read()
    config = ast.literal_eval(config)
    json_file_name = config['remote_json_path']
    json_slash = json_file_name.rfind("/")
    json_slash += 1
    json_file_name = json_file_name[json_slash:]
    os.system(f"scp {PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name} {config['remote_json_path']}")
    f.close()

check_files()

root = Tk()
root.title("dynasite")
root.resizable(False, False)

menu = Menu()
root.config(menu=menu)

file_menu = Menu()
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Edit configuration", command=edit_config)
file_menu.add_command(label="Download JSON", command=download_remote_json)
file_menu.add_command(label="Load local JSON", command=load_json)
file_menu.add_command(label="Upload JSON", command=upload_remote_json)

def callback(eventObject):
    print(project_selector.get())

project_selector = ttk.Combobox(
    state="readonly",
    values=project_list,
    width=100
)
project_selector.grid(column=0, row=0, padx=10, pady=(10, 0))
project_selector.bind("<<ComboboxSelected>>", callback)

add_project_button = Button(root, text="+", width=2)
delete_project_button = Button(root, text="-", width=2)
add_project_button.grid(column=1, row=0, padx=0, pady=(10, 0))
delete_project_button.grid(column=2, row=0, padx=(0, 10), pady=(10, 0))

project_title_label = Label(root, text="Title", anchor="w", justify="left")
project_title_label.grid(column=0, row=1, padx=10, pady=0, sticky="W")

project_title = Entry(root)
project_title.grid(column=0, row=2, padx=10, pady=0, columnspan=3, sticky='EW')

project_repo_label = Label(root, text="Repository", anchor="w", justify="left")
project_repo_label.grid(column=0, row=3, padx=10, pady=0, sticky="W")

project_repo = Entry(root)
project_repo.grid(column=0, row=4, padx=10, pady=0, columnspan=3, sticky='EW')

project_desc_label = Label(root, text="Description", anchor="w", justify="left")
project_desc_label.grid(column=0, row=5, padx=10, pady=0, sticky="W")

project_desc = Text(root, height=10)
project_desc.grid(column=0, row=6, padx=10, pady=(0, 10), columnspan=3, sticky='EW')

root.mainloop()