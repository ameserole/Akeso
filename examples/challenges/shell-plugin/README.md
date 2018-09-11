# Insecure Shell Plugin

## Challenge

I'm running a CTF competition that is geared towards newer students. I know that most of the students don't have easy access to a linux machine so why not give students shell access to my server so that they can use it to solve challenges?  
  
In order to make this a reality I wrote this cool plugin for CTFd to automatically create an account when they register for the competition.  
One of the students claims that they can get a root shell on my server though. Can you figure out what happened and fix the issue for me?

Go to <insert address here> and fork `shell-plugin` to begin solving the challenge.  
  
## Setup
Create a repo on the gitlab server with all of these files except `shell.py` and `shellAttack.py`. Those files will instead go under the `Services/shell` and `Exploits` folders respectively in the Defense Lab backend.

## Solution
The intended solution is to get rid of the shell code all together and replace it with python.  
Example solution in `script_server.py`:
```
def add_user_func(user, password):
    subprocess.call(["mkdir",  "/home/"+user])
    subprocess.call(["useradd", "-G", "ctf-users", "--home", "/home/"+user, "-s", "/bin/bash", user])
    subprocess.call(["chown", user+":"+user, "/home/"+user])

    #https://stackoverflow.com/questions/4688441/how-can-i-set-a-users-password-in-linux-from-a-python-script
    proc=Popen(['passwd', user],stdin=PIPE,stdout=PIPE,stderr=PIPE) 
    proc.stdin.write(password+'\n')
    proc.stdin.write(password)
    proc.stdin.flush()  
    stdout,stderr = proc.communicate()
    if stderr:
        print stderr
        print stdout
#    os.system("./add-user.sh " + name + " " + password)
```
