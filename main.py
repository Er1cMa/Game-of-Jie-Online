import socket
from threading import Thread
import csv


def client_game():
    global p0, p1
    p0 = {'hp': 2, 'energy': 0, 'fk': 1, 'choice': ''}
    p1 = {'hp': 2, 'energy': 0, 'fk': 1, 'choice': ''}
    while 1:
        list_choices(p1['energy'], p1['fk'])
        print("Waiting for the server...\n")
        result = eval(tcp_socket.recv(1024).decode("UTF-8"))  # msg begins with?
        display_result_p1(result)
        if result[2] != 'con':
            break
    input('End. You can now save this game.\n')


def recv_choice():
    global p1
    p1['choice'] = client_socket.recv(1024).decode("UTF-8")


def server_game():
    global p0, p1
    p0 = {'hp': 2, 'energy': 0, 'fk': 1, 'choice': ''}
    p1 = {'hp': 2, 'energy': 0, 'fk': 1, 'choice': ''}
    while 1:
        thread_connect = Thread(target=recv_choice)
        thread_choose = Thread(target=list_choices, args=(p0['energy'], p0['fk']))
        thread_choose.start()
        thread_connect.start()
        thread_choose.join()
        thread_connect.join()
        result = calc_result()
        client_socket.send(str(result).encode('UTF-8'))
        display_result_p0(result)
        if result[2] != 'con':
            break
    input('End. You can now save this game.\n')


def list_choices(energy, free_knife):
    global p0, p1
    for option in option_char_list:
        if option_list[option][1] == -2:
            if free_knife >= 1:
                choice_list.append('j')
        else:
            if energy >= option_list[option][1]:
                choice_list.append(option)
    for option in option_char_list:
        if option in choice_list:
            print(option, '. ', option_list[option][0], sep='')
    choice = input("Please choose!\n")
    if choice not in choice_list:
        if mode == 'c':
            tcp_socket.send("err:choice_not_in_list".encode("UTF-8"))
        else:
            p0['choice'] = "err:choice_not_in_list"
    else:
        multiple = False
        if option_list[choice][2]:
            if option_list[choice][1] == -2:
                if free_knife >= 2:
                    multiple = True
            elif energy >= 2 * option_list[choice][1]:
                multiple = True
        times = 1
        if multiple:
            times = input("You chose " + option_list[choice][0] + ".\nChoose the times of attack.\n")
        choice_times = choice + str(times)
        if mode == 'c':
            tcp_socket.send(choice_times.encode("UTF-8"))
        else:
            p0['choice'] = choice_times


def calc_result():
    global p0, p1
    if p0['choice'][0] == 'j':
        p0['fk'] -= eval(p0['choice'][1])
    else:
        p0['energy'] -= option_list[p0['choice'][0]][1] * eval(p0['choice'][1])
    if p1['choice'][0] == 'j':
        p1['fk'] -= eval(p1['choice'][1])
    else:
        p1['energy'] -= option_list[p1['choice'][0]][1] * eval(p1['choice'][1])
    if option_list[p0['choice'][0]][3] >= 0 and option_list[p1['choice'][0]][3] >= 0:
        max_times = max(eval(p0['choice'][1]), eval(p1['choice'][1]))
        for i in range(max_times):
            if i > eval(p0['choice'][1]):
                p0_damage = 0
            else:
                p0_damage = option_list[p0['choice'][0]][3]
            if i > eval(p1['choice'][1]):
                p1_damage = 0
            else:
                p1_damage = option_list[p1['choice'][0]][3]
            if p0_damage <= p1_damage:
                p0['hp'] -= (p1_damage - p0_damage)
            else:
                p1['hp'] -= (p0_damage - p1_damage)
    elif option_list[p0['choice'][0]][3] >= 0 > option_list[p1['choice'][0]][3]:
        latter_special_damage(p0, p1)
    elif option_list[p0['choice'][0]][3] < 0 <= option_list[p1['choice'][0]][3]:
        latter_special_damage(p1, p0)
    else:
        if option_list[p0['choice'][0]][3] == (-11 or -12) and option_list[p1['choice'][0]][3] == (-21 or -22):
            if option_list[p0['choice'][0]][3] == -11 and option_list[p1['choice'][0]][3] == -21:
                p0['hp'] -= 1
            if option_list[p0['choice'][0]][3] == -11 and option_list[p1['choice'][0]][3] == -22:
                p0['hp'] -= 2
            if option_list[p0['choice'][0]][3] == -12 and option_list[p1['choice'][0]][3] == -21:
                p0['hp'] -= 2
            if option_list[p0['choice'][0]][3] == -12 and option_list[p1['choice'][0]][3] == -22:
                p0['hp'] -= 4
        if option_list[p0['choice'][0]][3] == (-21 or -22) and option_list[p1['choice'][0]][3] == (-11 or -12):
            if option_list[p0['choice'][0]][3] == -21 and option_list[p1['choice'][0]][3] == -11:
                p1['hp'] -= 1
            if option_list[p0['choice'][0]][3] == -21 and option_list[p1['choice'][0]][3] == -12:
                p1['hp'] -= 2
            if option_list[p0['choice'][0]][3] == -22 and option_list[p1['choice'][0]][3] == -11:
                p1['hp'] -= 2
            if option_list[p0['choice'][0]][3] == -22 and option_list[p1['choice'][0]][3] == -12:
                p1['hp'] -= 4
        if option_list[p0['choice'][0]][3] == (-41 or -42) or option_list[p1['choice'][0]][3] == (-41 or -42):
            if option_list[p0['choice'][0]][3] == (-41 or -42) and option_list[p1['choice'][0]][3] == (
                    -41 or -42):
                if option_list[p0['choice'][0]][3] == -41 and option_list[p1['choice'][0]][3] == -41:
                    pass
                if option_list[p0['choice'][0]][3] == -42 and option_list[p1['choice'][0]][3] == -42:
                    pass
                if option_list[p0['choice'][0]][3] == -41 and option_list[p1['choice'][0]][3] == -42:
                    p1['hp'] -= 1
                if option_list[p0['choice'][0]][3] == -42 and option_list[p1['choice'][0]][3] == -41:
                    p0['hp'] -= 1
            elif option_list[p0['choice'][0]][3] == (-41 or -42):
                if option_list[p0['choice'][0]][3] == -41:
                    p0['hp'] -= 1.5
                if option_list[p0['choice'][0]][3] == -42:
                    p0['hp'] -= 2.5
            else:
                if option_list[p1['choice'][0]][3] == -41:
                    p1['hp'] -= 1.5
                if option_list[p1['choice'][0]][3] == -42:
                    p1['hp'] -= 2.5
    if p0['energy'] < 0 or p0['fk'] < 0 or p1['energy'] < 0 or p1['fk'] < 0:
        if (p0['energy'] < 0 or p0['fk'] < 0) and (p1['energy'] < 0 or p1['fk'] < 0):
            return [p0, p1, 'dre']
        if p0['energy'] < 0 or p0['fk'] < 0:
            return [p0, p1, 'p0e']
        if p1['energy'] < 0 or p1['fk'] < 0:
            return [p0, p1, 'p1e']
    if p0['hp'] < 0 or p1['hp'] < 0:
        if p0['hp'] < 0 and p1['hp'] < 0:
            return [p0, p1, 'drh']
        if p0['hp'] < 0:
            return [p0, p1, 'p0h']
        if p1['hp'] < 0:
            return [p0, p1, 'p1h']
    return [p0, p1, 'con']


def latter_special_damage(former, latter):
    if option_list[former['choice'][0]][3] <= 1 and option_list[latter['choice'][0]][3] == -1:
        pass
    elif 1.5 <= option_list[former['choice'][0]][3] <= 2.5 and option_list[latter['choice'][0]][3] == -2:
        pass
    elif option_list[former['choice'][0]][3] <= 2.5 and option_list[latter['choice'][0]][3] == -11:
        if option_list[former['choice'][0]][3] == 0.5:
            latter['fk'] += eval(former['choice'][1])
        else:
            latter['energy'] += option_list[former['choice'][0]][1] * eval(former['choice'][1])
    elif option_list[former['choice'][0]][3] <= 2.5 and option_list[latter['choice'][0]][3] == -12:
        if option_list[former['choice'][0]][3] == 0.5:
            latter['fk'] += eval(former['choice'][1]) * 2
        else:
            latter['energy'] += option_list[former['choice'][0]][1] * eval(former['choice'][1]) * 2
    elif option_list[former['choice'][0]] == ('n' or 'o') and option_list[latter['choice'][0]][3] == -31:
        former['hp'] -= option_list[former['choice'][0]][1] * eval(former['choice'][1])
    elif option_list[former['choice'][0]][3] <= 4 and option_list[latter['choice'][0]][3] == -41:
        if option_list[former['choice'][0]][3] == 0:
            latter['hp'] -= 1.5
        elif option_list[former['choice'][0]][3] == 0.5:
            latter['fk'] += eval(former['choice'][1])
        else:
            latter['energy'] += option_list[former['choice'][0]][1] * eval(former['choice'][1])
    elif option_list[former['choice'][0]][3] <= 6 and option_list[latter['choice'][0]][3] == -42:
        if option_list[former['choice'][0]][3] == 0:
            latter['hp'] -= 2.5
        elif option_list[former['choice'][0]][3] == 0.5:
            latter['fk'] += eval(former['choice'][1]) * 2
        else:
            latter['energy'] += option_list[former['choice'][0]][1] * former['choice'][2]
    elif 3 <= option_list[former['choice'][0]][3] <= 3.5 and option_list[latter['choice'][0]][3] == -51:
        pass
    elif option_list[former['choice'][0]][3] == 4 and option_list[latter['choice'][0]][3] == -52:
        pass
    elif option_list[former['choice'][0]][3] == 4.5 and option_list[latter['choice'][0]][3] == -53:
        pass
    elif option_list[former['choice'][0]][3] == 6 and option_list[latter['choice'][0]][3] == -54:
        pass
    elif option_list[former['choice'][0]][3] == 17.5 and option_list[latter['choice'][0]][3] == -55:
        pass
    else:
        latter['hp'] -= option_list[former['choice'][0]][3] * eval(former['choice'][1])


def display_result_p0(result):
    if eval(p0['choice'][1]) == 1:
        p0_choice = option_list[p0['choice'][0]]
    else:
        p0_choice = option_list[p0['choice'][0]][0] + '*' + p0['choice'][1]
    if eval(p1['choice'][1]) == 1:
        p1_choice = option_list[p1['choice'][0]]
    else:
        p1_choice = option_list[p1['choice'][0]][0] + '*' + p1['choice'][1]
    print("You chose %s, Player 1 chose %s.\n"
          "You have %s hp, %s energy, %s free knifes.\n"
          "Player 1 has %s hp, %s energy, %s free knifes.\n"
          % (p0_choice, p1_choice, p0['hp'], p0['energy'], p0['fk'], p1['hp'], p1['energy'], p1['fk']))
    if result[2] == 'dre':
        input("Draw: Both players are lack of energy or free knifes.\n")
    if result[2] == 'drh':
        input("Draw: Both players are lack of hp.\n")
    if result[2] == 'p0e':
        input("Lose: You are lack of energy or free knifes.\n")
    if result[2] == 'p0h':
        input("Lose: You are lack of hp.\n")
    if result[2] == 'p1e':
        input("Win: Player 1 is lack of energy or free knifes.\n")
    if result[2] == 'p1h':
        input("Win: Player 1 is lack of hp.\n")


def display_result_p1(result):
    global p0, p1
    p0 = result[0]
    p1 = result[1]
    if eval(p0['choice'][1]) == 1:
        p0_choice = option_list[p0['choice'][0]]
    else:
        p0_choice = option_list[p0['choice'][0]][0] + '*' + str(eval(p0['choice'][1]))
    if eval(p1['choice'][1]) == 1:
        p1_choice = option_list[p1['choice'][0]]
    else:
        p1_choice = option_list[p1['choice'][0]][0] + '*' + str(eval(p1['choice'][1]))
    print("You chose %s, Player 0 chose %s.\n"
          "You have %s hp, %s energy, %s free knifes.\n"
          "Player 0 has %s hp, %s energy, %s free knifes.\n"
          % (p1_choice, p0_choice, p1['hp'], p1['energy'], p1['fk'], p0['hp'], p0['energy'], p0['fk']))
    if result[2] == 'dre':
        input("Draw: Both players are lack of energy or free knifes.\n")
    if result[2] == 'drh':
        input("Draw: Both players are lack of hp.\n")
    if result[2] == 'p1e':
        input("Lose: You are lack of energy or free knifes.\n")
    if result[2] == 'p1h':
        input("Lose: You are lack of hp.\n")
    if result[2] == 'p0e':
        input("Win: Player 0 is lack of energy or free knifes.\n")
    if result[2] == 'p0h':
        input("Win: Player 0 is lack of hp.\n")


while 1:
    mode = input("Enter 's' for server mode, or 'c' for client mode.\n")
    if mode == 's' or mode == 'c':
        break
option_file = csv.reader(open("./config/Option List.csv", encoding='UTF-8'))
option_num = 0
option_list = {}
choice_list = []
option_char_list = []
for row in option_file:
    if option_num == 0:
        option_num += 1
        continue
    column_num = 0
    row_option = row[0]
    option_char_list.append(row_option)
    for cell in row:
        if column_num == 0:
            column_num += 1
            option_list[row_option] = []
            continue
        if column_num == 1:
            column_num += 1
            option_list[row_option].append(cell)
            continue
        option_list[row_option].append(eval(cell))
        column_num += 1
    option_num += 1
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
        global p0, p1
        server_game()
