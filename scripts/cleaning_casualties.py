import os
import csv

# Define directories and output files
directory = r"C:\Users\foste\Documents\NSS\Capstone\Data\cleaned_casualties"
output_csv = r"C:\Users\foste\Documents\NSS\Capstone\Data\casualty_data.csv"
missed_files_log = r"C:\Users\foste\Documents\casualty_data\missed_files.txt"

# Define column names
column_names = ['service_number', 'member_component_code', 'person_type_name_code', 'person_type_name', 'member_name',
                'member_service_code', 'member_service_name', 'member_rank_or_rate', 'member_paygrade', 'member_occupation_code',
                'member_occupation_name', 'member_birthdate', 'members_gender', 'home_of_record_city', 'home_of_record_county',
                'home_of_record_country_code', 'home_of_record_state_code', 'state_or_province_name', 'marital_name',
                'religion_short_name', 'religion_code', 'race_name', 'ethnic_short_name', 'race_omb_name', 'ethnic_group_name',
                'casualty_circumstances', 'casualty_city', 'casualty_state_or_province_code', 'casualty_country/over_water_code',
                'region_name', 'country/over_water_name', 'member_unit', 'duty_code', 'process_date', 'incident_or_death_date',
                'year_of_death_[or_incident]', 'war_or_conflict_code', 'operation_incident_type_code', 'operation/incident_name',
                'location_name', 'closure_date', 'aircraft_type', 'hostile_or_non-hostile_death_indicator',
                'casualty_type_name', 'casualty_category', 'casualty_reason_name', 'casualty_cat._short_name',
                'remains_recovered', 'casualty_closure_name', 'vietnam_wall_row_and_panel_indicator', 'incident_category',
                'incident_casualty_category_date', 'incident_casualty_cat._short_name',
                'incident_hostile_or_incident_non-hostile_death', 'incident_aircraft_type']

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
                if len(row) == len(column_names):
                    csv_writer.writerow(row)
                else:
                    missed_log.write(f"{filename}\n")
                    print(f"Skipped file {filename}: Column count mismatch")

print("Processing completed. Missed files saved in 'missed_files.txt'.")
