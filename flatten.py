import json
import sys
from reddit.cleaners.flat import call_flatten_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python flatten.py <path_to_json_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    flat_list = call_flatten_data(file_path)
    output_file_path = file_path.rsplit('.', 1)[0] + '_flat.' + file_path.rsplit('.', 1)[1]
    with open(output_file_path, 'w') as outfile:
        json.dump(flat_list, outfile, indent=2)
    print(f"Flattened data written to {output_file_path}")