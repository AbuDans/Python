import json


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
