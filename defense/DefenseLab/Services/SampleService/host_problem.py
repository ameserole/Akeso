import sys
import subprocess
import socket
import thread


def t_func(client, address, program):
    print "[*] Client " + address[0] + " connected"

    exe = "./" + program
    p = subprocess.Popen(exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    userIn = client.recv(2048)
    out = p.communicate(input=userIn)[0]

    print "[*] Server sending " + out
    client.send(out)

    client.close()
    print "[*] Server closed connection with " + address[0]


def main():
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + " [binary name] [port num]"
        sys.exit(1)

    program = sys.argv[1]
    port = sys.argv[2]
    print "[*] Server hosting binary: " + program
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", int(port)))
    server.listen(5)

    while True:
        (client, address) = server.accept()
        print "[*] Server starting thread"
        t = thread.start_new_thread(t_func, (client, address, program)) # NOQA


if __name__ == '__main__':
    main()
