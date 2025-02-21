# CONVERT GPS
# converts .gp2 pulseekko files to .gps file format
# see https://www.sensoft.ca/wp-content/uploads/2018/04/EKKO_Project-Users-Guide.pdf for more info on gps file types
# code written with ChatGPT 4o

# import packages
import os
import csv
import glob

def convert_gp2_to_gps(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip the header (first 5 lines and the separator)
    data_lines = lines[6:]  # Start from the 7th line (index 6)

    gps_data = {}
    
    for line in data_lines:
        parts = list(csv.reader([line.strip()], delimiter=','))[0]
        
        if len(parts) < 5:
            continue  # Skip malformed lines

        trace_number = int(parts[0])
        position = float(parts[2])
        nmea_string = parts[4].strip('"')

        if trace_number not in gps_data:
            gps_data[trace_number] = {
                "position": position,
                "nmea_strings": []
            }
        
        gps_data[trace_number]["nmea_strings"].append(nmea_string)

    # Write to the new .gps file
    with open(output_file, 'w', encoding='utf-8') as f:
        for trace_number, data in sorted(gps_data.items()):
            f.write(f"Trace #{trace_number} at position {data['position']:.6f}\n")
            for nmea in data["nmea_strings"]:
                f.write(f"{nmea}\n")


def process_directories(directories):
    for directory in directories:
        for gp2_file in glob.glob(os.path.join(directory, "*.gp2")):
            gps_file = gp2_file.replace(".gp2", ".gps")
            convert_gp2_to_gps(gp2_file, gps_file)
            print(f"Converted: {gp2_file} -> {gps_file}")

if __name__ == "__main__":
    # Replace with the list of directories containing .gp2 files
    directories = ["../data/alhic2201","../data/alhic2302","../data/alhic2301"]
    process_directories(directories)