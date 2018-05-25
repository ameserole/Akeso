# Secure Coding/Config Lab

[![Build Status](https://travis-ci.org/ameserole/Akeso.svg?branch=master)](https://travis-ci.org/ameserole/Akeso)

A Platform for Testing Secure Coding/Config  
  
The goal of this project is to test users abilities to find and fix vulnerabilities in code within a CTF style framework.  

The platform provides users with account on a hosted Gitlab CE instance. To solve the challenges users will make a private fork of the challenge repository and will be able to make commits to the code from there. Every commit that the user makes will run through some checks on Gitlab's CI/CD tool. The checks are passed to a backend tool that makes sure the service being tested still works correctly and that the code is still not exploitable. If the users code passes all of the checks a flag will be output at the bottom of the CI/CD output that can be found by clicking CI/CD->Jobs->Status Bar.
  
An example implementation can be found at https://ctf.tamu.edu under the Secure Coding/Config challenges.  

## Basic Design
The basic overall design has two parts.  
The first is the Gitlab CI/CD container. Gitlab's CI/CD spins up a docker container with the users files contained inside. Once spun up the container will pass some basic info about itself, including its ip and the service that it is currently running, to the backend using rabbitmq. It then waits for the results to come back from the backend by listening on the result exchange for the user's routing key.  
The second main part is the backend workers. These workers are a simple python script that pull jobs off of the rabbitmq queue and correlate the info with an exploit and service check. The worker then runs through three tests. First it uses a service check to make sure the users code is running correctly. Second it runs an exploit against the code to make sure that the code is not exploitable. And third it runs another service check against the code to make sure the exploit code did not crash the service. The final results are then pushed onto the result queue. If the users code ran correctly and was not exploitable then the result pushed would be the flag. Otherwise the a simple message of either `Service Check Failed` or `Your Code/Config was exploited` is returned.   

## Setup
There are a few pieces that need to be put together in order for the full platform to be set up.
### Gitlab Server
#### Install
First setup the Gitlab Community Edition server the installation instructions can be found here: https://about.gitlab.com/installation/.  
Our implemenation used Ubuntu 16.04 but other flavors of linux will most likely work. Gitlab also has suggested requirements here: https://docs.gitlab.com/ce/install/requirements.html.  
Many Gitlab configuration settings can be found here: https://docs.gitlab.com/omnibus/settings/configuration.html  
Including how to enable HTTPS: https://docs.gitlab.com/omnibus/settings/nginx.html#enable-https

#### Admin
To make the platform more competition friendly users should not be able to see the commits that other competitors are making. In order to do this there are some Administrative settings that need to be made.  
To harden your gitlab instance and to keep all user commits and repositories separate from each other the following options are suggestions under admin settings: 
1. Set `Default project visibility`, `Default snippet visibility`, and `Default group visibility` to private. 
2. For `Restricted visibility levels` check the `Internal` and `Public` boxes.
    - This forces all new repositories to be private.
3. Set default projects limit to the number of challenges that you have.
4. Uncheck `Sign-up enabled` to only allow users you have created to log on.  
  
  
To further keep all user commits and repositories separate from each other the following options are suggested for the permissions under general settings for each challenge repository:
1. Set `Project visibility` to `Internal`
2. Set `Issues`, `Merge Requests`, `Pipelines`, `Wiki`, and `Snippets` to `Only Project Members`
3. Set `Repository` to `Everyone With Access`
4. Turn off `Git Large File Storage`  

### Backend Server
The Backend Server is a few python workers that communicate using RabbitMQ and Gitlabs CI/CD workers. The original implementation can be found here: https://github.com/ameserole/Defense-Lab. Using Gitlab's CI/CD simplified the whole thing by allowing the backend to just be reduced down to the AttackWorkers and Service/Exploit code. The current implementation can be found under `defense`.

**NOTE:** It is highly suggested to install the backend on a separate server from the server hosting Gitlab.  

There are a couple scripts that will setup and run the backend code. The `setup.sh` script installs all of the dependencies and `start.sh` starts up the Rabbitmq container and the `DefenseLab.py` script.  
  
To setup the Gitlab CI workers follow Gitlab's Docs: https://docs.gitlab.com/ce/ci/quick_start/
The installation guide can be found here: https://docs.gitlab.com/runner/install/linux-repository.html  
The setup guid can be found here: https://docs.gitlab.com/runner/register/

The suggested installation for runners is:  
`sudo gitlab-runner register --url "<url>" --registration-token "<token>" --description "runner" --executor "docker" --docker-image ubuntu:latest`  
and when prompted `Whether to lock Runner to current project [true/false]:` respond with `false`.  


### Integrating with CTFd
Integrating `Gitlab` with CTFd is relatively easy and can make the users experience more seamless. Gitlab comes with an API interface for adding and editing users: https://docs.gitlab.com/ce/api/users.html. Including a python module http://python-gitlab.readthedocs.io/en/stable/gl_objects/users.html.  
#### User Creation
To integrate the user creation I added this script into the registration code in CTFd's [auth.py](https://github.com/CTFd/CTFd/blob/master/CTFd/auth.py#L138) 
```
gl = Gitlab('<Server Address>', private_token='<token>')
name = re.sub(r'\W+', '_', name)
user_data = {'email': email, 'username': name, 'name': name, 'password': password, 'confirm': 'false'}
try:
    user = gl.users.create(user_data)
except:
    print "Unexpected error:", sys.exc_info()[0] 
```
The regex `name = re.sub(r'\W+', '_', name)` replaces all special characters with underscores. This is because Gitlab does not allow usernames with special characters and will cause the registration to fail. 
#### User Password Reset
The following code can also be added to the password reset code is CTFd's [auth.py](https://github.com/CTFd/CTFd/blob/master/CTFd/auth.py#L83)
```
gl = Gitlab('<Server Address>', private_token='<token>')
try:
    user = gl.users.list(username=team.name)[0]
    user.password = request.form['password'].strip()
    user.save()
except:
    print "Unexpected error:", sys.exc_info()[0] 
```
This code will update the users temporary password to their new password.  
An Admin access token can be created under `Settings` -> `Access Tokens` for the Adminstrator account.  
This code could probably be easily made into a CTFd plugin.  

## Challenge Creation
There are three main parts to creating a challenge: Challenge Repo Creation, Service Check Creation, and Exploit Creation.  
### Challenge Repo Creation
#### gitlab-ci.yml
The first part is creating the actual insecure code once this is done there is a few files used to hook up the repo with the backend queue. The first file is the `.gitlab-ci.yml` file. This describes how to build the Dockerfile with the challenge code. An example can be found in `example_.gitlab-ci.yml`. More info how to create them can be found here: https://docs.gitlab.com/ce/ci/yaml/README.html. It is highly suggested to pull the docker image from a custom repo with as of the Docker image built as possible. This is significantly faster than rebuilding the full image every time CI/CD is started.  

#### entry.sh
The `entry.sh` file is used for any file changes that need to be made before running of the tests and starting the `queue.py`. An example `entry.sh` file can be found in `example_entry.sh`.

#### queue.py
The `queue.py` is what hooks up the challenge repo with the backend checks. An example `queue.py` can be found in `example_queue.py`. The main thing that changes between each challenge is https://github.com/ameserole/Akeso/blob/master/example_queue.py#L34 which tells the backend queue which challenge it is testing. 
  
### Service Check Creation
All of the service checks are derived from the `ServiceFrame` base class. All derived `ServiceFrame` classes are required to implement two functions. The first is the `checkService` function. This function is used to check if the service is running correctly. The function is required to return `False` if the service is not running correct or `True` if the serivce is running correctly. The other function is `getLogs` this function is used to get any extra logs that the creator may want the user to see. It is currently not fully integrated into the platform at the moment however.  
An example implementation can be found in https://github.com/ameserole/Akeso/blob/master/defense/DefenseLab/Services/SQLiSimple/SQLiSimple.py  

### Exploit Creation
All of the exploits are derived from the `ExploitFrame` base class. All derived `ExploitFrame` classes are required to implement two functions. The first is the `exploit` function. This function actually executes the exploit against the service. The next function is the `exploitSuccess` function. This function implements the code to make check whether or not the exploit succeeded. It is required to return `True` if the exploit succeeded and `False` if the exploit failed.  
An example implementation can be found in https://github.com/ameserole/Akeso/blob/master/defense/DefenseLab/Exploits/SQLi.py

### Final Integration
The final piece for the backend is to map the challenge to its info in `AttackWorkers.py`. This maps the challenge to their respective service checks and port numbers. The list is `('imageName', 'exploit', 'service', portNumber)`. The `imageName` is the name of the challenge. This can be whatever you want because it is used for logging. The `exploit` is the exploit module name. `service` is the service folder/module name. Finally, the `portNumber` is the port the service is running on.   
The list can be found here https://github.com/ameserole/Akeso/blob/master/defense/DefenseLab/AttackWorkers.py#L12-L17.

## Future Ideas
Beyond just testing secure coding and configuration it might be possible to test other defense related things. One idea is to give users a pcap that contains malicious traffic in it. The challenge would be for them to create a signature for the malicious traffic and have the user created signature tested against some new, live malicious traffic.

# Acknowledgements
Special thanks to Kevin Chung over at the [CTFd project](https://github.com/ctfd/ctfd). When discussing the idea of a secure coding/config CTF category with him he came up with the idea of running the challenges on a git server instead of doing all the file management myself and let me run with it.
