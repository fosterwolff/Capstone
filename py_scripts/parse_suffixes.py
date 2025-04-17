import csv

# Output file path
outfile = r"C:\Users\foste\Documents\NSS\Capstone\parsed_names.csv"

# Suffixes to check for
suffixes = ['JR', 'SR', 'II', 'III']

# Headers for the CSV file
headers = ['last_name', 'first_name', 'middle_name', 'suffix']

# Open the input file and the output file
with open(r"C:\Users\foste\Downloads\names.csv", 'r') as infile, open(outfile, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write headers to the output file
    writer.writerow(headers)
    
    # Process each line in the input file
    for line in infile.readlines():
        name_line = []
        
        # Clean up the line and split it into words
        line = line.replace('\"', '')
        name = line.strip().split(' ')
        
        last_name = first_name = middle_name = None
        name_suffix = None

        if name[-1] in suffixes:
            name_suffix = name[-1]
            del name[-1]
        
        # Parse based on the number of words in the name
        if len(name) > 1:
            if len(name) == 3:
                last_name = name[0]
                first_name = name[1]
                middle_name = name[2]
            elif len(name) == 2:
                last_name = name[0]
                first_name = name[1]
                middle_name = None
            elif len(name) == 4:
                last_name = name[0]
                first_name = name[1]
                middle_name = name[2]
            elif len(name) == 5:
                last_name = name[0]
                first_name = name[1]
                middle_name = name[2] + ' ' + name[3] + ' ' + name[4]
        
        
        # Append the name components to the name_line list
        name_line.append(last_name)
        name_line.append(first_name)
        name_line.append(middle_name)
        name_line.append(name_suffix)
        
        # Write the parsed name to the output file
        writer.writerow(name_line)
