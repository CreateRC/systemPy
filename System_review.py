import platform as p
import socket, re, uuid, logging, json, subprocess, shutil

def get_system():
    try:
        system = {}
        system['platform'] = p.system()
        system['release'] = p.release()
        system['version'] = p.version()
        system['arch'] = p.machine()
        system['hostname'] = socket.gethostname()
        system['ip'] = socket.gethostbyname(socket.gethostname())
        system['mac'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        system['processor'] = p.processor()
        return json.dumps(system)
    
    except Exception as e:
        logging.exception(e)

def get_users(system):
    if system == "Windows":
        cmd = "net user"
    elif system == "Linux":
        cmd = "getent passwd"
    elif system == "Darwin":
        cmd = "users"
    else:
        cmd = "pwd"
        print("System not found...")
        print("System_Type: {}".format(system))

    #run command on shell so that all systems can work with it
    result = subprocess.check_output(cmd, shell=True, text=True)
    return result

def disk_info():
    total, used, free = shutil.disk_usage("/")
    
    total = "{}{}".format(round(format_bytes(total)[0], 2), format_bytes(total)[1])
    used = "{}{}".format(round(format_bytes(used)[0], 2), format_bytes(used)[1])
    free = "{}{}".format(round(format_bytes(free)[0], 2), format_bytes(free)[1])

    print("*"*10, "Disk Information", "*"*10)
    print("Total Disk Space: {}".format(total))
    print("~ Used: {} | Free: {}".format(used, free))

def format_bytes(size):
    power = 2**10
    n = 0
    powers = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return size, powers[n]+'B'

def output_system(info):
    print("*"*10, "System Information", "*"*10)
    print('System: ',info['hostname'])
    print('OS: ',info['platform'], info['release'])
    print('Version: ',info['version'])
    print('Arch: ', info['arch'])
    print('IP: ',info['ip'])
    print('MAC: ',info['mac'])
    print(" ")

def output_users(users):
    print("*"*10, "Users List", "*"*10)
    print(users)
    
def main():
    #Get System Information
    info = json.loads(get_system())
    output_system(info) #print system info to user

    #Get User Information
    users = get_users(info['platform']) #feed system type
    output_users(users)

    #Get Disk Information
    disk_info()
    
    
    
    
main() 
