import requests
import os
import zipfile

godot_zip_name = "godot-docs-html-stable.zip"
godot_unzip_name = "godot-docs-html-stable"
godot_docs_url = "https://nightly.link/godotengine/godot-docs/workflows/build_offline_docs/master/godot-docs-html-stable.zip"

def retrieveGodotDocumentationFromSource():
    current_working_dir = os.getcwd()
    godot_zip_path = os.path.join(current_working_dir, godot_zip_name)

    # Check if we need to re-download Godot Documentation from Source
    if (os.path.isdir(godot_unzip_name)):
        print("Existing Godot Documentation Found")
        return

    # Download Godot Docs as Zip Folder
    print("Retrieving Godot Docs - This may take a while...")
    response = requests.get(godot_docs_url)

    if not (200 <= response.status_code < 300):
        print("Failed to retrieve Godot Documentation Zip Folder")

    # Write Godot Zip Data to File
    with open(godot_zip_name, "wb") as file:
        file.write(response.content)
        print("Godot Documentation Zip Folder Successfully Downloaded - Unzipping Folder")

    # Unzip Godot Docs Zip Folder
    with zipfile.ZipFile(godot_zip_path, "r") as zip_ref:
        zip_ref.extractall(f"{godot_unzip_name}/")
        print("Godot Documentation Successfully Unzipped")

    return

retrieveGodotDocumentationFromSource()
