import socket
from threading import Thread
import csv


def client_game():
    # hp = 2
    energy = 0
    fk = 1
    list_choices(energy, fk)
    print("Waiting for the server...\n")
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
    option_num = 0
    option_list = {}
    choice_list = []
    for row in option_file:
        if option_num == 0:
            option_num += 1
            continue
        column_num = 0
        row_option = row[0]
        for cell in row:
            if column_num == 0:
                column_num += 1
                option_list[row_option] = []
                continue
            option_list[row_option].append(cell)
            column_num += 1
        option_num += 1
    for option in option_list:
        if option_list[option][1] is str:
            if free_knife >= 1:
                choice_list.append('n')
        else:
            if energy >= option_list[option][1]:
                choice_list.append(option_list[option])
    for option in option_list:
        if option in choice_list:
            print(option, '. ', option_list[option][0], sep='')
    choice = input("Please choose!\n")
    if choice not in choice_list:
        if mode == 'c':
            tcp_socket.send("err:choice_not_in_list".encode("UTF-8"))
        else:
            return "err:choice_not_in_list"
    else:
        multiple = False
        if option_list[choice][2]:
            if option_list[choice][1] is str:
                if free_knife >= 2:
                    multiple = True
            else:
                if energy >= 2 * option_list[choice][1]:
                    multiple = True
        if multiple:
            input("You chose " + option_list[choice][0] + ".\nChoose the times of attack.\n")
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
    mode = input("Enter 's' for server mode, or 'c' for client mode.\n")
    if mode == 's' or mode == 'c':
        break
option_file = csv.reader(open("./config/Option List.csv", encoding='UTF-8'))
if mode == 'c':
    server_ip = input("Enter the ip of the server.\n")
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
