import csv
whitelist_filename = 'whitelist.csv'

def _read_file() -> dict:
    user_data = dict()
    with open(whitelist_filename, mode='r') as csv_file:
        for row in csv.reader(csv_file, delimiter=','):
            user_data[row[0]] = row[1]            
    return user_data

def _write_file(users_dict):
    with open(whitelist_filename, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for discord, minecraft in users_dict.items():
            csv_writer.writerow([discord, minecraft])

def get_users() -> str:
    try:
        users = ''
        users_dict = _read_file()
        for discord, minecraft in users_dict.items():
            users += f'{discord} -> {minecraft}\n'
        users += f'{len(users_dict)} users'
        return users
    except Exception as e:
        return repr(e)
    
def add_user(discord, minecraft) -> str:
    try:
        users_dict = _read_file()
        users_dict[discord] = minecraft
        _write_file(users_dict)
        
        return f'your minecraft username has been updated to {minecraft}'
    except Exception as e:
        return repr(e)
    