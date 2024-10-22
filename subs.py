import re

# Function to parse prefixedname values from a file
def parse_prefixednames(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the entire file content
        content = file.read()

    # Regular expression to find all prefixedname values
    matches = re.findall(r'prefixedname="r/(.*?)"', content)
    
    # Return the list of extracted values
    return matches

# Example usage
file_path = '/data/prefixed.txt'  # Replace with your file path
result = parse_prefixednames(file_path)

# Print results
for name in result:
    print(name)