import os
import pandas as pd


# define a function that will return a list of all files in a given directory,
# including all files in any subdirectories
def get_all_files(dir):
    all_files = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            name = os.path.basename(path)
            all_files.append({'path': path, 'name': name})
    return all_files

# main program

# get a list of all files in the current directory
files = get_all_files('.')

# create a Pandas DataFrame with a column for the paths, a column for the
# filenames, and a column for the file sizes
df = pd.DataFrame({'path': [f['path'] for f in files], 'name': [f['name'] for f in files], 'size': [os.path.getsize(f['path']) for f in files]})

# find the duplicate files by grouping the DataFrame by size and name and
# finding groups with more than one row
duplicates = df.groupby(['size', 'name']).size().reset_index(name='count')
duplicates = duplicates[duplicates['count'] > 1]['path']

# set the maximum column width and the maximum number of rows to display
# to unlimited
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# print the list of duplicate files without a column header
print(duplicates.to_string(header=False))

