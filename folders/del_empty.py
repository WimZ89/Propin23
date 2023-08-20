import os

root = 't:/torrentz'
folders = list(os.walk(root))[1:]
print(f"Found {len(folders)} folders")
# [0] full path.
# [1] [].
# [2] files in folder.


for folder in folders:
    print(folder)
    # continue
    # folder example: ('FOLDER/3', [], ['file'])
    if not folder[2]:  # folder is empty
        print("Folder is empty:", folder[0])
        try:
            os.rmdir(folder[0])
            print("Removed empty folder:", folder[0])
        except OSError:
            print("OSError: Unable to remove folder", folder[0])
    else:
        print("Folder is not empty")
        ext_to_del = ["txt", "nfo"]

        for filename in folder[2]:
            file_ext = filename.split(".")[-1]
            if file_ext in ext_to_del:
                file_path = os.path.join(folder[0], filename)
                try:
                    os.remove(file_path)
                    print(f"Removed file {filename} in folder {folder[0]}")
                except OSError:
                    print(f"OSError: Unable to remove {filename} in folder {folder[0]}")
