import json
def flatten_data(obj, flat_list, subreddit):
    if isinstance(obj, dict):
        if 'id' in obj and 'name' in obj:
            obj['subreddit'] = subreddit
            obj['type'] = obj['name'].split('_')[0]
            flat_list.append(obj)
        
        for key in list(obj.keys()):
            if key in ['children', 'replies']:
                flatten_data(obj[key], flat_list, subreddit)
                del obj[key]
            else:
                flatten_data(obj[key], flat_list, subreddit)
    elif isinstance(obj, list):
        for item in obj:
            flatten_data(item, flat_list, subreddit)

def call_flatten_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    flat_list = []
    subreddit = data.get('subreddit', '')
    flatten_data(data, flat_list, subreddit)
    return flat_list