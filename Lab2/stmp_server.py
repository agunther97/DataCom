import socket
import base64
import ssl
import time

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
mailserver = ("smtp.gmx.com", 25)


def send_email():
    client_socket = socket.socket()
    client_socket.connect(mailserver)
    recv = client_socket.recv(1024)
    recv = recv.decode()
    print("Message after connection request:" + recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')
    
    ehlo_response = ehlo_command(client_socket)
    print("EHLO Response:" + ehlo_response)
    if ehlo_response[:3] != '250':
        print('EHLO Response: 250 reply not received from server.')
        return
    
    ttls_response = start_ttls(client_socket)
    print('TTLS Response: ' + ttls_response)
    if ttls_response.find('220') == -1:
        print('TTLS Response: 220 Response not received from server.')
        return
    
    client_socket = ssl.wrap_socket(client_socket)
    ehlo_response = ehlo_command(client_socket)
    print("EHLO Response:" + ehlo_response)
    if ehlo_response[:3] != '250':
        print('EHLO Response: 250 reply not received from server.')
        return
    
    email_login_response = email_login(client_socket)
    print('Email Login Response: ' + email_login_response)
    if email_login_response.find('235') == -1:
        print('Mail Login Response: 235 reply not received from server.')
        return

    mail_from_response = mail_from(client_socket)
    print('Mail From Response: ' + mail_from_response)
    if mail_from_response.find('250') == -1:
        print('Mail From Response: 250 reply not received from server.')
        return

    rcpt_to_response = rcpt_to(client_socket)
    print("RCPT Response: " + rcpt_to_response)
    if rcpt_to_response.find('250') == -1:
        print('RCPT Response: 250 reply not received from server.')
        return
    
    send_data_response = send_data(client_socket)
    print("Send Data Response: " + send_data_response)
    if send_data_response.find('354') == -1:
        print('Send Data Response: 354 reply not received from server.')
        return
    
    send_end_response = send_end(client_socket)
    print('Send End Response: ' + send_end_response)
    if send_end_response.find('250') == -1:
        print('Send End Response: 250 reply not received from server.')
        return
    
    send_quit_response = send_quit(client_socket)
    print('Send Quit Response: ' + send_quit_response)
    if send_quit_response.find('221') == -1:
        print('Send Quit Response: 221 reply not received from server.')
        return
    
    client_socket.close()
    

def ehlo_command(client_socket):
    ehloCommand = 'EHLO Alice\r\n'
    client_socket.send(ehloCommand.encode())
    return client_socket.recv(1024).decode()

def start_ttls(client_socket):
    starttls = 'STARTTLS\r\n'
    client_socket.send(starttls.encode())
    return client_socket.recv(1024).decode()

def email_login(client_socket):
    username = "###"
    password = "###"
    base64_str = ("\x00"+username+"\x00"+password).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
    client_socket.send(authMsg)
    return client_socket.recv(1024).decode()

def mail_from(client_socket):
    mailFrom = "MAIL FROM:<####>\r\n"
    client_socket.send(mailFrom.encode())
    return client_socket.recv(1024).decode()

def rcpt_to(client_socket):
    rcptTo = "RCPT TO:<####>\r\n"
    client_socket.send(rcptTo.encode())
    return client_socket.recv(1024).decode()

def send_data(client_socket):
    data = "DATA\r\n"
    client_socket.send(data.encode())
    return client_socket.recv(1024).decode()

def send_end(client_socket):
    client_socket.send(msg.encode())
    client_socket.send(endmsg.encode())
    return client_socket.recv(1024).decode()

def send_quit(client_socket):
    quit = "QUIT\r\n"
    client_socket.send(quit.encode())
    return client_socket.recv(1024).decode()

if __name__ == "__main__":
    send_email()