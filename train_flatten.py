import csv

# Input and output file paths
input_file = "timetable.csv"
output_file = "flattened_timetable.csv"

# Read the input CSV
with open(input_file, mode='r', newline='') as infile:
    reader = csv.reader(infile)
    data = list(reader)

# Extract headers (train numbers) and stations
train_numbers = data[0][1:]  # Skip the first column ("STATIONS")
stations = [row[0] for row in data[1:]]  # First column of each row after header
times = [row[1:] for row in data[1:]]  # Times for each station

# Flatten the data
flattened_data = []
for i, station in enumerate(stations):
    for j, train_no in enumerate(train_numbers):
        time = times[i][j] if times[i][j] else ""  # Keep empty string if no time
        flattened_data.append([station, train_no, time])

# Write the flattened data to a new CSV
with open(output_file, mode='w', newline='') as outfile:
    writer = csv.writer(outfile)
    # Write header for the flattened data
    writer.writerow(["Station", "Train No", "Time"])
    # Write the flattened rows
    writer.writerows(flattened_data)

print(f"Flattened data has been written to {output_file}")