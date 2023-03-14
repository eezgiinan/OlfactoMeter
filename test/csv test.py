import csv

# name of csv file
filename = "university_records.csv"

# field names
fields = ['Time', 'Mode']

# data rows of csv file
rows = [['0', '0'], ['1', '1']]

"""
with open(filename, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

"""
# writing to csv file
with open(filename, 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)

