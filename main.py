import socket
from threading import Thread


def client_game():
    hp = 2
    energy = 0
    fk = 1
    list_choices(energy, fk)
    print("Waiting for the server...")
    tcp_socket.recv(1024).decode("UTF-8")  # begins with?


def recv_choice():
    global p1_choice
    p1_choice = client_socket.recv(1024).decode("UTF-8")


def server_game():
    global p0_hp, p1_hp, p0_energy, p1_energy, p0_fk, p1_fk, p0_choice, p1_choice
    p0_hp = 2
    p1_hp = 2
    p0_energy = 0
    p1_energy = 0
    p0_fk = 1
    p1_fk = 1
    thread_connect = Thread(target=recv_choice)
    thread_choose = Thread(target=list_choices, args=(p0_energy, p0_fk))
    p0_choice = thread_choose.start()
    p1_choice = thread_connect.start()
    thread_choose.join()
    thread_connect.join()


def list_choices(energy, free_knife):
    choice_list = ['a']
    if energy >= 0:
        choice_list.extend(['b', 'c', 'd', 'f', 'h', 'i'])
    if energy >= 1:
        choice_list.extend(['e', 'j', 'k', 'l', 'o'])
    if energy >= 2:
        choice_list.extend(['g', 'p'])
    if energy >= 3:
        choice_list.append('q')
    if energy >= 4:
        choice_list.append('r')
    if energy >= 5:
        choice_list.append('s')
    if energy >= 6:
        choice_list.append('t')
    if energy >= 7:
        choice_list.extend(['m', 'u'])
    if energy >= 8:
        choice_list.append('v')
    if energy >= 12:
        choice_list.append('w')
    if energy >= 35:
        choice_list.append('x')
    if free_knife >= 1:
        choice_list.append('n')
    print('a. 结')
    if 'b' in choice_list:
        print('b. 小防')
    if 'c' in choice_list:
        print('c. 大防')
    if 'd' in choice_list:
        print('d. 吸')
    if 'e' in choice_list:
        print('e. 大吸')
    if 'f' in choice_list:
        print('f. 拉')
    if 'g' in choice_list:
        print('g. 大拉')
    if 'h' in choice_list:
        print('h. 反弹')
    if 'i' in choice_list:
        print('i. 摩擦')
    if 'j' in choice_list:
        print('j. 收')
    if 'k' in choice_list:
        print('k. 青龙收')
    if 'l' in choice_list:
        print('l. 金龙收')
    if 'm' in choice_list:
        print('m. 抽烟')
    if 'n' in choice_list:
        print('n. 免单')
    if 'o' in choice_list:
        print('o. 笑波')
    if 'p' in choice_list:
        print('p. 电波')
    if 'q' in choice_list:
        print('q. 致命')
    if 'r' in choice_list:
        print('r. 地波')
    if 's' in choice_list:
        print('s. 骗波')
    if 't' in choice_list:
        print('t. 派波')
    if 'u' in choice_list:
        print('u. 气波')
    if 'v' in choice_list:
        print('v. 青龙波')
    if 'w' in choice_list:
        print('w. 金龙波')
    if 'x' in choice_list:
        print('x. 王圣波')
    choice = input("Please choose!")
    if choice not in choice_list:
        print("err:choice_not_in_list")
        if mode == 'c':
            tcp_socket.send("err:choice_not_in_list".encode("UTF-8"))
        else:
            return "err:choice_not_in_list"
    else:
        if mode == 'c':
            tcp_socket.send(choice.encode("UTF-8"))
            input("Test OK!\n")
        else:
            return choice


def calc_result():
    global p0_hp, p1_hp, p0_energy, p1_energy, p0_fk, p1_fk, p0_choice, p1_choice
    if p0_choice == 'n':
        p0_fk -= 1
    if p1_choice == 'n':
        p1_fk -= 1


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
        client_game()

if mode == 's':
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('', 38395)
    tcp_server_socket.bind(address)
    tcp_server_socket.listen(128)
    client_socket, client_addr = tcp_server_socket.accept()
    if client_socket.recv(1024).decode("UTF-8") == "Try to connect.":
        client_socket.send("Received.".encode("UTF-8"))
        global p0_hp, p1_hp, p0_energy, p1_energy, p0_fk, p1_fk, p0_choice, p1_choice
        server_game()
