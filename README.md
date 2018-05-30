# Secure Coding/Config Lab

[![Build Status](https://travis-ci.org/ameserole/Akeso.svg?branch=master)](https://travis-ci.org/ameserole/Akeso)

A Platform for Testing Secure Coding/Config  
  
The goal of this project is to test users abilities to find and fix vulnerabilities in code within a CTF style framework.  

The platform provides users with account on a hosted Gitlab CE instance. To solve the challenges users will make a private fork of the challenge repository and will be able to make commits to the code from there. Every commit that the user makes will run through some checks on Gitlab's CI/CD tool. The checks are passed to a backend tool that makes sure the service being tested still works correctly and that the code is still not exploitable. If the users code passes all of the checks a flag will be output at the bottom of the CI/CD output that can be found by clicking CI/CD->Jobs->Status Bar.
  
An example implementation can be found at https://ctf.tamu.edu under the Secure Coding/Config challenges.  

## Setup and Installation
Check out the [Wiki](https://github.com/ameserole/Akeso/wiki) for details on how to setup and install everything.

## Example Challenge
Challenge view:
![challenge](https://github.com/ameserole/Akeso/blob/master/examples/challenge_view.PNG)

Failing CI since the code is still exploitable:
![fail](https://github.com/ameserole/Akeso/blob/master/examples/ci_example_1.PNG)

Simple fix for the exploitable code:
![fix](https://github.com/ameserole/Akeso/blob/master/examples/simple_solution.PNG)

Passing CI with flag since code is no longer exploitable but still functions properly:
![flag](https://github.com/ameserole/Akeso/blob/master/examples/ci_example_2.PNG)

## Future Ideas
Beyond just testing secure coding and configuration it might be possible to test other defense related things. One idea is to give users a pcap that contains malicious traffic in it. The challenge would be for them to create a signature for the malicious traffic and have the user created signature tested against some new, live malicious traffic.

# Acknowledgements
Special thanks to Kevin Chung over at the [CTFd project](https://github.com/ctfd/ctfd). When discussing the idea of a secure coding/config CTF category with him he came up with the idea of running the challenges on a git server instead of doing all the file management myself and let me run with it.
