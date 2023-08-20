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
        # print (len(folder),folder)
        print(folder[2])
        try:
            os.rmdir(folder[0])
            print("removed", folder[0])
            # break
        except OSError:
            print("OSError", folder[0])
    else:
        print("not empty")
        ext_to_del=["txt","nfo"]
        # todo delete all files with extension ext_to_del

