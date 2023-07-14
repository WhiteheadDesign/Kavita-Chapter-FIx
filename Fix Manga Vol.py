import zipfile
import io
import os

# Specify the path to the folder containing the zip files
folder_path = "path/to/your/folder"

# Function to modify the ComicInfo.xml file within a zip file
def modify_zip_file(zip_file_path):
    # Open the zip file in read mode
    with zipfile.ZipFile(zip_file_path, "r") as zip_file:
        # Create a new in-memory zip file
        new_zip_data = io.BytesIO()

        # Open the new zip file in write mode
        with zipfile.ZipFile(new_zip_data, "w") as new_zip_file:
            # Iterate over each file in the original zip file
            for file_name in zip_file.namelist():
                # Check if the file is ComicInfo.xml
                if file_name == "ComicInfo.xml":
                    # Read the contents of the ComicInfo.xml file into memory
                    with zip_file.open(file_name) as xml_file:
                        xml_data = xml_file.readlines()

                    # Remove the fifth line from the XML data
                    del xml_data[4]

                    # Write the modified XML data to the new zip file
                    new_zip_file.writestr(file_name, b"".join(xml_data))
                else:
                    # If it's not ComicInfo.xml, write the original file to the new zip file
                    new_zip_file.writestr(file_name, zip_file.read(file_name))

        # Save the new zip file to disk, replacing the original zip file
        with open(zip_file_path, "wb") as new_zip_file:
            new_zip_file.write(new_zip_data.getvalue())

    print(f"Modification completed for: {zip_file_path}")

# Recursively iterate through the folder and its subfolders
for root, dirs, files in os.walk(folder_path):
    for file in files:
        # Check if the file is a zip file
        if file.endswith(".zip"):
            # Create the full path to the zip file
            zip_file_path = os.path.join(root, file)
            # Modify the ComicInfo.xml file within the zip file
            modify_zip_file(zip_file_path)
