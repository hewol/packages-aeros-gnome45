import os
import re
from urllib.parse import unquote
from http.client import responses

import requests
import wget

os.chdir("x86_64")

gnome = os.popen("pacman -Sg gnome | awk '{print $2}' | tr '\n' ' '").read().split(" ")[:-1]
gnome_extra = os.popen("pacman -Sg gnome-extra | awk '{print $2}' | tr '\n' ' '").read().split(" ")[:-1]

print("Filtering packages...")
for package in gnome[:]:
    status = requests.get(f"https://archive.archlinux.org/packages/{package[0]}/{package}").status_code
    print(f"{package}: {responses[status]}")
    if status == 404:
        gnome.remove(package)

for package in gnome_extra[:]:
    status = requests.get(f"https://archive.archlinux.org/packages/{package[0]}/{package}").status_code
    print(f"{package}: {responses[status]}")
    if status == 404:
        gnome_extra.remove(package)

print("Downloading packages...")
for package in gnome:
    html_doc = requests.get(f"https://archive.archlinux.org/packages/{package[0]}/{package}").text
    try:
        rematch = re.findall(r".+ \d{1,2}-\w{3}-2023", html_doc)[-2]
        package_name = unquote(re.findall(r'"(.*?)".+ \d{1,2}-\w{3}-2023', html_doc)[-2])
        release_date = re.findall(r'\d{1,2}-\w{3}-2023', html_doc)[-2]
        print(f"\nDownloading {package_name}")
        wget.download(f"https://archive.archlinux.org/packages/{package[0]}/{package}/{package_name}")
    except IndexError:
        print(f"\n{package} is not a recent package, you may want to get it manually.")

for package in gnome_extra:
    html_doc = requests.get(f"https://archive.archlinux.org/packages/{package[0]}/{package}").text
    try:
        rematch = re.findall(r".+ \d{1,2}-\w{3}-2023", html_doc)[-2]
        package_name = unquote(re.findall(r'"(.*?)".+ \d{1,2}-\w{3}-2023', html_doc)[-2])
        release_date = re.findall(r'\d{1,2}-\w{3}-2023', html_doc)[-2]
        print(f"\nDownloading {package_name}")
        wget.download(f"https://archive.archlinux.org/packages/{package[0]}/{package}/{package_name}")
    except IndexError:
        print(f"\n{package} is not a recent package, you may want to get it manually.")
