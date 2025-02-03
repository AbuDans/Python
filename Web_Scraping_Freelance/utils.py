import json
import os 

def get_segment_list():
    segment_list = []
    while True:
        user_input = input("Enter a segment code (press 0 to stop): ")
        if user_input == '0':
            break
        segment_list.append(user_input)
    return '|'.join(segment_list)


def load_configs(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# Write data to JSON file
def write_configs(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)  # Indent for pretty formatting (optional)


def save_progress(Page_Number, Segment_List):
    # Create a dictionary from the page number and segment list
    progress_entry = {
        Segment_List: Page_Number
    }
    
    # If the file does not exist, create it and write the progress entry
    if not os.path.exists("progress.json"):
        with open("progress.json", 'w') as file:
            json.dump([progress_entry], file, indent=4)
    else:
        # If the file exists, append the new progress entry
        with open("progress.json", 'r+') as file:
            data = json.load(file)
            data.append(progress_entry)
            file.seek(0)
            json.dump(data, file, indent=4)

def load_progress(Segment_List):

    # Load the existing progress
    with open("progress.json", 'r') as file:
        data = json.load(file)
    
    # Find the last entry for the given segment list
    last_page_number = 1
    for entry in data:
        if Segment_List in entry:
            last_page_number = entry[Segment_List]

    return last_page_number


# Example usage
if __name__ == "__main__":
    # Data to be written to the JSON file
    data = {
        "email": "nadine.schlamm1983@proton.me",
        "password": "bWdS4pg8Ngn6Sw",
        "search_segments": [
            "keywords=",
            "countries=DE",
            "address=",
            "coord=",
            "bbox=",
            "maxDistance=",
            "distanceUnit=km",
            "legalForm=",
            "status=active",
            "segmentCodeStandard=UKSIC",
            "segmentCodes=",
            "search=power"
        ],
        "output_file": "emails.txt"
    }
    file_path = "config.json"
    write_configs(data, file_path)
