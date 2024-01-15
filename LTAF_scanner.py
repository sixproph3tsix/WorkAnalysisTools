# Checks a specified directory for a specified file
# Returns the path to the specified file, as well as the file size
# Option to return the path to the specified file IF the file exceeds a specified size
# Option to return the path to the specified file IF the number of rows in the file are greater than 1 (is populated)
# Option to return the 


# i want to find every FILE.txt that has a 


# specify directory
top_dir = input('Specify the top directory to search:  ')

# search recursively?
search_recurs = input('Search the directory recursively?  y/n')

# search AFs or LTs?
search_aflt = input('Search for  ')

if search_recurse:
    print('Searching recursively... ')
else:
    print('Searching non-recursively... ')