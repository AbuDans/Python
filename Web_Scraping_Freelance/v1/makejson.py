import json

# Data to be written to the JSON file
data = {
    "email": "nadine.schlamm1983@proton.me",
    "password": "bWdS4pg8Ngn6Sw",
    "token": "",
    "login_url": "https://www.northdata.com/rpc.json/user/login",
    "protected_url": "https://www.northdata.com/_selfcare",
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
    "segmentCodes=01,01.1",
    "search=power"
  ],
  "output_file" : "emails.txt"
}
def get_segment_list():
  segment_list = []
  while True:
    user_input = input("Enter a segment code (press 0 to stop): ")
    if user_input == '0':
      break
    segment_list.append(user_input)
    segment_codes = '|'.join(segment_list)
    data["search_segments"][10] = "segmentCodes="+segment_codes
    write_to_json(data, "config.json")  
 








# Path to the JSON file you want to create
file_path = "config.json"
def extract_login_data_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    extracted_data = {
        'token': data.get('token'),
        'email': data.get('email'),
        'password': data.get('password')
    }
    
    return extracted_data

def extract_login_url_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    login_url=data.get('login_url')
    return login_url
  
def extract_protected_url_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    protected_url=data.get('protected_url')
    return protected_url  
      
# Write data to JSON file
def write_to_json(data, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)  # Indent for pretty formatting (optional)
        print(f"JSON data successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing JSON to {file_path}: {e}")

# Example usage
if __name__ == "__main__":
    write_to_json(data, file_path)
