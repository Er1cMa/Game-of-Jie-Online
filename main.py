import socket


def start_game():
    hp = 2
    energy = 0
    print("Start with hp %s, energy %s" % (hp, energy))
    list_choices(energy)


def list_choices(energy):
    choice_list = ['a']
    if energy >= 0:
        choice_list.extend(['b', 'c', 'd', 'e'])
    if energy >= 1:
        choice_list.append('f')
    if energy >= 2:
        choice_list.append('g')
    print('a. 结')
    if 'b' in choice_list:
        print('b. 小防')
    if 'c' in choice_list:
        print('c. 大防')
    if 'd' in choice_list:
        print('d. 吸')
    if 'e' in choice_list:
        print('e. 拉')
    if 'f' in choice_list:
        print('f. 笑波')
    if 'g' in choice_list:
        print('g. 电波')
    choice = input("Please choose!")
    if choice not in choice_list:
        print("err:choice_not_in_list")
        if mode == 'c':
            tcp_socket.send("err:choice_not_in_list".encode("UTF-8"))
        else:
            client_socket.send("err:choice_not_in_list".encode("UTF-8"))
    else:
        if mode == 'c':
            tcp_socket.send(choice.encode("UTF-8"))
        else:
            client_choice = client_socket.recv(1024).decode("UTF-8")
            input("Client choice is " + client_choice + "\nServer choice is " + choice + "\nTest OK!\n")


while 1:
    mode = input("Enter 's' for server mode, or 'c' for client mode.")
    if mode == 's' or mode == 'c':
        break
if mode == 'c':
    server_ip = input("Enter the ip of the server.")
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (server_ip, 38395)
    tcp_socket.connect(server_addr)
    tcp_socket.send("Try to connect.".encode("UTF-8"))
    if tcp_socket.recv(1024).decode("UTF-8") == "Received.":
        start_game()

if mode == 's':
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('', 38395)
    tcp_server_socket.bind(address)
    tcp_server_socket.listen(128)
    client_socket, client_addr = tcp_server_socket.accept()
    if client_socket.recv(1024).decode("UTF-8") == "Try to connect.":
        client_socket.send("Received.".encode("UTF-8"))
        start_game()
