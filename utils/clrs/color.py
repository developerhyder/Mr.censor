def green(var):
    print("\033[92m {}\033[00m".format(var))

def red(var):
    print("\033[91m {}\033[00m" .format(var))

def yellow(var):
    print("\033[93m {}\033[00m" .format(var))

def purple(var):
    print("\033[95m {}\033[00m" .format(var))

def green_str(var):
    return "\033[92m"+str(var)+"\033[00m"

def red_str(var):
    return "\033[91m"+str(var)+"\033[00m"
