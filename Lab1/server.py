import socket
import sys
import atexit

def server_program():
    try:
        server_socket = socket.socket()
        host = '192.168.1.50'
        print(socket.gethostname())
        port = 5034
        server_socket.bind((host, port))
        server_socket.listen(2)
        while True:
            print('Ready to serve...')
            connection_socket, addr = server_socket.accept()
            connection_socket.settimeout(1)
            try:
                message = connection_socket.recv(1024).decode()
                while 1: 
                    # clear the recv buffer
                    try:
                        junk = connection_socket.recv(1024).decode()
                    except:
                        break
                print('message is' + message)
                filename = message.split()[1]
                filename = filename[1:]
                print('filename is: ' + filename)
                if not message: break
                f = open(filename, "r")
                outputdata = f.read()
                connection_socket.sendall(('Http/1.0 200 OK\r\nContent-Type: html\r\n\r\n' + outputdata + '\r\n').encode())
                connection_socket.close()
                f.close()
            except IOError:
                print(filename + ' not found')
                connection_socket.sendall(('Http/1.0 404 NotFound\r\nContent-Type: html\r\n\r\n' + "<html><body><p>404 Not Found</p></body></html>").encode())
                connection_socket.close()
    except KeyboardInterrupt:
        connection_socket.close()
        server_socket.close()
        print("Server closed...")
        sys.exit()

if __name__ == '__main__':
    server_program()
