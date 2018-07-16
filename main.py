import pandas as pd
import datetime
# Variables
INPUT_FILENAME = "test.csv"
OUTPUT_FILENAME = "result.csv"
DATE_FORMAT = "%d-%b-%Y"

# Methods
def stringToDateTime(date):
	return datetime.datetime.strptime(date, DATE_FORMAT)	

def DateTimeToString(date):
	return date.strftime(DATE_FORMAT)

# CSV to DataFrame
data = pd.read_csv(INPUT_FILENAME)

# Add columns Start and End
data['Start'] = list(map(stringToDateTime,data['StayDate']))
data['End'] = list(data['Start'])

# Drop column StayDate
data.drop(['StayDate'], axis=1, inplace=True)

# Sort according to RoomType and then StayDate
data = data.sort_values(['RoomType','Start'])
row_count =data.shape[0]

# Logic for filtering
l = [] # All the row indexes to be discarded will be stored here
for row in range(row_count - 1):
	current_row = row
	next_row =row + 1
	current_tuple = data.iloc[current_row]
	next_tuple = data.iloc[next_row]
	while (current_tuple['Available Rooms'] == next_tuple['Available Rooms'] and current_tuple['Sell Amount'] == next_tuple['Sell Amount'] and current_tuple['Tax'] == next_tuple['Tax'] and current_tuple['RoomType'] == next_tuple['RoomType']):
		l.append(next_row)
		next_row += 1
		if(next_row < row_count):
			next_tuple = data.iloc[next_row]
		else:
			break		
	data.at[current_row,'End'] = data.iloc[next_row-1]['Start']
	row=next_row

# Remove all the uncessary rows
data.drop(data.index[l],inplace=True)

# Convert datetime back to string
data['Start'] = list(map(DateTimeToString,data['Start']))
data['End'] = list(map(DateTimeToString,data['End']))
data.to_csv(OUTPUT_FILENAME, sep=',', encoding='utf-8', index=False)