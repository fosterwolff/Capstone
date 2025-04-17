import os
import csv

# Define directories and output files
directory = r'C:\Users\foste\Desktop\awards_raw'
output_csv = r"C:\Users\foste\Documents\NSS\Capstone\Data\casualty_awards.csv"
missed_files_log = r"C:\Users\foste\Documents\casualty_data\missed_files.txt"

column_names = ['unique_identifier', 'sequence_number', 'name_of_individual', 'grade_code', 
 'staff_code', 'command_staff_name', 'service_country_code', 'service_country_name', 
 'day_date_eligible_to_return_from_overseas', 'month_date_eligible_to_return_from_overseas', 
 'year_date_eligible_to_return_from_overseas', 'recommended_award_code', 
 'day_date_recommended_award_received', 'month_date_recommended_award_received', 
 'year_date_recommended_award_received', 'date_of_action', 'approved_award_code', 
 'cluster_code', 'board_number', 'macv_recommended_award_code', 'level_of_assignment', 
 'general_order_number', 'day_date_award_forwarded', 'month_date_award_forwarded', 
 'year_date_award_forwarded', 'award_presented_in_republic_of_vietnam', 'posthumous']


# Open CSV file for writing
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile, open(missed_files_log, 'w', encoding='utf-8') as missed_log:
    csv_writer = csv.writer(csvfile)
    
    # Write header row
    csv_writer.writerow(column_names)

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):  # Ensure it's a file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().replace('\x00', '')  # Remove null characters

                # Extract data
                data = content.split("'column_detail','400','400')\">")
                row = []  # Row for storing extracted values

                for element in data:
                    element = element.replace('\n', '').replace('\t', '')
                    element_parts = element.split('</a></td>')

                    if len(element_parts) > 1:
                        value_parts = element_parts[1].split('<td>')
                        
                        if len(value_parts) > 2:  # Ensure it has the expected structure
                            dict_value = value_parts[2].split('</td>')[0].strip()
                            dict_value = None if dict_value == '&nbsp;' else dict_value
                            row.append(dict_value)

                # Ensure row has the correct length before writing
                print(len(row),len(column_names))
                if len(row) == len(column_names):
                    csv_writer.writerow(row)
                else:
                    missed_log.write(f"{filename}\n")
                    print(f"Skipped file {filename}: Column count mismatch")

print("Processing completed. Missed files saved in 'missed_files.txt'.")
