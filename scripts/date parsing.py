import psycopg2
from datetime import datetime

mmymmy = [
"JOINT SERVICE COMMENDATION MEDAL (SERVICE)",
"BRONZE STAR MEDAL (SERVICE)",
"BRONZE STAR MEDAL (ACHIEVEMENT)",
"DISTINGUISHED SERVICE MEDAL",
"DISTINGUISHED SERVICE CROSS",
"NAVY COMMENDATION MEDAL (SERVICE)",
"LEGION OF MERIT",
"ARMY COMMENDATION MEDAL (ACHIEVEMENT)",
"NAVY ACHIEVEMENT MEDAL (ACHIEVEMENT)",
"AIR MEDAL (ACHIEVEMENT)",
"AIR FORCE COMMENDATION MEDAL",
"JOINT SERVICE COMMENDATION MEDAL (ACHIEVEMENT)",
"ARMY COMMENDATION MEDAL (SERVICE)"
]

ddmmyy = [
    "BRONZE STAR MEDAL (VALOR)",
    "SILVER STAR",
"ARMY COMMENDATION MEDAL (VALOR)",
"AIR MEDAL (VALOR)",
"NAVY CROSS",
"DISTINGUISHED FLYING CROSS",
"PURPLE HEART",
"MEDAL OF HONOR",
"Undefined Code",
"SOLDIERS MEDAL (ARMY)"
]

# Establish the database connection
db_conn = psycopg2.connect(
    database='casualties',
    user='postgres',
    password='postgres',
    host='localhost',
    port=5432
)

# Create a cursor object
cursor = db_conn.cursor()

# Define the query
query = '''
SELECT name_of_individual, approved_award_code, date_of_action, unique_identifier
FROM public.awards
'''

# Execute the query
cursor.execute(query)

# Fetch results
result = cursor.fetchall()  # Fetch all rows

# Print results
for row in result:
    try:
        member_name = row[0]
        award_code = row[1]
        date_of_action = row[2]
        identifier = row[3]
        if award_code in mmymmy:
            action_date_list = []
            start_month = date_of_action[0:2]
            start_year = date_of_action[2]
            end_month = date_of_action[3:5]
            end_year = date_of_action[5]
            action_date_list.append(start_month)
            action_date_list.append(start_year)
            action_date_list.append(end_month)
            action_date_list.append(end_year)
            if int(action_date_list[1]) >= 0 and int(action_date_list[1]) <= 7:
                action_date_list[1] = '197' + action_date_list[1]
            if int(action_date_list[3]) >= 0 and int(action_date_list[3]) <= 7:
                action_date_list[3] = '197' + action_date_list[3]
            if action_date_list[1] == '8' or action_date_list[1] == '9':
                action_date_list[1] = '196' + action_date_list[1]
            if action_date_list[3] == '8' or action_date_list[3] == '9':
                action_date_list[3] = '196' + action_date_list[3]
            first_date= action_date_list[1] + '-' + action_date_list[0]  + '-' + '01'
            second_date= action_date_list[3] + '-' + action_date_list[2]  + '-' + '01'
            date_range = [first_date,second_date]
            #print(member_name , date_range)
            #print('WHEN name_of_individual = ' + '\'' + member_name + '\'' + ' AND ' + 'date_of_action = ' + '\'' + date_of_action+ '\' ' + ' THEN ' + 'daterange(' + '\''+date_range[0]+'\''+ ', ' + '\'' + date_range[1] + '\'' + ', ' + '\'[]\'' + ')' )
            date_format = "%Y-%m-%d"  # Define the format of the date string
            date1 = datetime.strptime(first_date, date_format)
            date2 = datetime.strptime(second_date, date_format)
            if  date1 > date2:
                print(member_name , date_range)
        if award_code in ddmmyy:
            action_date_list = []
            day = date_of_action[0:2]
            month = date_of_action[2:4]
            year = date_of_action[4:6]
            year  = '19'+year
            action_date_list.append(day)
            action_date_list.append(month)
            action_date_list.append(year)
            date_range_of_action = action_date_list[2] + '-' + action_date_list[1] + '-' + action_date_list[0]
            date_range = [date_range_of_action,date_range_of_action]
            #print(member_name, date_range)
            #print('WHEN name_of_individual = ' + '\'' + member_name + '\'' + ' AND ' + 'date_of_action = ' + '\'' + date_of_action+ '\' ' + ' THEN ' + 'daterange(' + '\''+date_range[0]+'\''+ ', ' + '\'' + date_range[1] + '\'' + ', ' + '\'[]\'' + ')' )
            date_format = "%Y-%m-%d"  # Define the format of the date string
            date1 = datetime.strptime(first_date, date_format)
            date2 = datetime.strptime(second_date, date_format)
            if  date1 > date2:
                print(member_name , date_range)
        #input()
    except:
        pass
    
# Close cursor and connection
cursor.close()
db_conn.close()
