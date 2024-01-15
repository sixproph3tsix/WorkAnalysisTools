# Checks a specified directory for a specified file
# Returns the path to the specified file, as well as the file size
# Option to return the path to the specified file IF the file exceeds a specified size
# Option to return the path to the specified file IF the number of rows in the file are greater than 1 (is populated)
# Option to return the 


# find every SAMPLEFILE.txt that has at least 2 rows of data


# specify directory
top_dir = input('\nSpecify the top directory for search...   ')

def check_recursive():

    try:
        recursive = int(input("\nSearch the directory recursively?  1 for Yes, 0 for No...   "))
        if recursive < 0 or recursive > 1:
            print("\nInvalid input...   ")
            check_recursive()
        elif recursive == 1:
            print('\nSearching recursively... ')
        elif recursive == 0:
            print('\nSearching non-recursively... ')
    except ValueError:
        print("\nInvalid input...   ")
        check_recursive()

check_recursive()