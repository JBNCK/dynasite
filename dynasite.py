#!/usr/bin/python3
import platform
import os
from tkinter import *
from tkinter import ttk
import ast
import json

project_list = []

print(f"{platform.system()} system detected")
if platform.system() == "Windows":
    HOME_PATH = os.environ["USERPROFILE"]
    FOLDER_SEPARATOR = "\\"
    print(f"User/Home folder: {HOME_PATH}")
    print(f"Folder separator: {FOLDER_SEPARATOR}")
    DEFAULT_EDITOR = "NOTEPAD.exe"
elif platform.system() == "Linux":
    HOME_PATH = os.environ["HOME"]
    FOLDER_SEPARATOR = "/"
    print(f"User/Home folder: {HOME_PATH}")
    print(f"Folder separator: {FOLDER_SEPARATOR}")
    DEFAULT_EDITOR = ""
else:
    print(f"Unsupported Operating System: '{platform.system()}'")

PROGRAM_FOLDER = ".dynasite"
PROGRAM_CONFIG_FILE = "config.json"
PROGRAM_FULL_PATH = f"{HOME_PATH}{FOLDER_SEPARATOR}{PROGRAM_FOLDER}"
PROGRAM_FULL_CONFIG_PATH = f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{PROGRAM_CONFIG_FILE}"

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
        
check_files()

f = open(PROGRAM_FULL_CONFIG_PATH, "r")
config = f.read()
config = ast.literal_eval(config)
f.close()

json_file_name = config["remote_json_path"]
json_slash = json_file_name.rfind("/")
json_slash += 1
json_file_name = json_file_name[json_slash:]

def edit_config():
    os.system(f"{DEFAULT_EDITOR} {PROGRAM_FULL_CONFIG_PATH}")

def load_json():
    project_list = []
    project_selector.set("")

    project_title.delete("0", END)
    project_repo.delete("0", END)
    project_desc.delete("1.0", END)

    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "r")
    loaded_projects = f.read()
    loaded_projects = ast.literal_eval(loaded_projects)
    for project in loaded_projects:
        project_list.append(project["title"])

    project_selector.config(values=project_list)

    f.close()

def download_remote_json():
    os.system(f"scp {config["remote_json_path"]} {PROGRAM_FULL_PATH}")
    load_json()

def upload_remote_json():
    os.system(f"scp {PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name} {config["remote_json_path"]}")

def load_project_data(i):
    project_title.delete("0", END)
    project_repo.delete("0", END)
    project_desc.delete("1.0", END)

    selected_project = project_selector.get()

    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "r")
    projects = f.read()
    projects = ast.literal_eval(projects)
    f.close()

    p = 0
    i = 0
    while i < 1:
        try_p = projects[p]
        if selected_project == try_p["title"]:
            correct_project = projects[p]
            project_index.config(text=p)
            i += 1
        else:
            p += 1
    
    project_title_val = correct_project["title"]
    project_repo_val = correct_project["url"]
    project_desc_val = correct_project["desc"]

    project_title.insert(END, project_title_val)
    project_repo.insert(END, project_repo_val)
    project_desc.insert(END, project_desc_val)

def save_projects():
    current_project_index = project_index.cget("text")

    current_project_title = project_title.get()
    current_project_repo = project_repo.get()
    current_project_desc = project_desc.get("1.0", END)

    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "r")
    old_projects = f.read()
    old_projects = ast.literal_eval(old_projects)
    new_projects = old_projects
    f.close()

    new_projects[current_project_index] = {"title": current_project_title, "url": current_project_repo, "desc": current_project_desc}
    new_projects_json = json.dumps(new_projects, indent=4)
    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "w")
    f.write(new_projects_json)
    f.close()

    load_json()

def sort_projects():
    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "r")
    projects = f.read()
    projects = ast.literal_eval(projects)
    f.close()

    sorted_projects = sorted(projects, key=lambda project: project["title"].lower())

    sorted_projects_json = json.dumps(sorted_projects, indent=4)
    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "w")
    f.write(sorted_projects_json)
    f.close()

    load_json()

def add_project():
    new_project_title = project_title.get()
    new_project_repo = project_repo.get()
    new_project_desc = project_desc.get("1.0", END)

    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "r")
    projects = f.read()
    projects = ast.literal_eval(projects)
    f.close()

    new_project = {"title": new_project_title, "url": new_project_repo, "desc": new_project_desc}
    projects.append(new_project)

    updated_projects_json = json.dumps(projects, indent=4)
    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "w")
    f.write(updated_projects_json)
    f.close()

    sort_projects()
    load_json()

def delete_project():

    selected_project = project_selector.get()

    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "r")
    projects = f.read()
    projects = ast.literal_eval(projects)
    f.close()

    updated_projects = [project for project in projects if project["title"] != selected_project]

    updated_projects_json = json.dumps(updated_projects, indent=4)
    f = open(f"{PROGRAM_FULL_PATH}{FOLDER_SEPARATOR}{json_file_name}", "w")
    f.write(updated_projects_json)
    f.close()

    sort_projects()
    load_json()

def clear_all():
    project_selector.set("")
    project_title.delete("0", END)
    project_repo.delete("0", END)
    project_desc.delete("1.0", END)

def about_window():
    about = Tk()
    about.title("dynasite")
    about.resizable(False, False)
    about.geometry("200x200")
    
    about_label = Label(about, text="Initial release/ 0.1").pack()

    about.mainloop()

root = Tk()
root.title("dynasite")
root.resizable(False, False)

menu = Menu()
root.config(menu=menu)

file_menu = Menu()
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Edit configuration", command=edit_config)
file_menu.add_separator()
file_menu.add_command(label="Download JSON", command=download_remote_json)
file_menu.add_command(label="Load local JSON", command=load_json)
file_menu.add_command(label="Upload JSON", command=upload_remote_json)
file_menu.add_separator()
file_menu.add_command(label="Sort project list", command=sort_projects)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit)

help_menu = Menu()
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about_window)

project_selector = ttk.Combobox(
    state="readonly",
    values=project_list,
    width=100
)
project_selector.grid(column=0, row=0, padx=10, pady=(10, 0))
project_selector.bind("<<ComboboxSelected>>", load_project_data)

add_project_button = Button(root, text="+", width=2, command=add_project)
delete_project_button = Button(root, text="-", width=2, command=delete_project)
add_project_button.grid(column=1, row=0, padx=0, pady=(10, 0))
delete_project_button.grid(column=2, row=0, padx=(0, 10), pady=(10, 0))

project_title_label = Label(root, text="Title", anchor="w", justify="left")
project_title_label.grid(column=0, row=1, padx=10, pady=0, sticky="W")

project_title = Entry(root)
project_title.grid(column=0, row=2, padx=10, pady=0, columnspan=3, sticky="EW")

project_repo_label = Label(root, text="Link", anchor="w", justify="left")
project_repo_label.grid(column=0, row=3, padx=10, pady=0, sticky="W")

project_repo = Entry(root)
project_repo.grid(column=0, row=4, padx=10, pady=0, columnspan=3, sticky="EW")

project_desc_label = Label(root, text="Description", anchor="w", justify="left")
project_desc_label.grid(column=0, row=5, padx=10, pady=0, sticky="W")

project_desc = Text(root, height=10)
project_desc.grid(column=0, row=6, padx=10, pady=0, columnspan=3, sticky="EW")

save_button = Button(root, text="New project", width=2, command=clear_all).grid(column=0, row=7, padx=10, pady=(10, 0), columnspan=3, sticky="EW")
save_button = Button(root, text="Save", width=2, command=save_projects).grid(column=0, row=8, padx=10, pady=(0, 10), columnspan=3, sticky="EW")

project_index = Label(root, text="0")

root.mainloop()