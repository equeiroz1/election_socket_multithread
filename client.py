
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8") #Mensagem advinda do servidor
            msg_split = msg.split("@")
            print(msg_split)
            if len(msg_split) > 1:
               msg_list.insert(tkinter.END, msg_split[0] + '\n')
               msg_list.insert(tkinter.END, msg_split[1] + '\n')

            if len(msg_split) == 1:
                
                msg_list.insert(tkinter.END, msg + '\n') #Inserir na lista de mensagens (front-end)
                print(msg)

        except OSError: 
            break


def send_vote(event=None):  
    """Handles sending of messages."""
    msg = "@" + my_name.get() + "@" + my_vote.get()
    print(msg)
    client_socket.send(bytes(msg, "utf8")) #Enviar mensagem para o servidor


def send(event=None):  
    """Handles exit."""
    if my_msg.get() != "":
        msg = "@" + my_msg.get()

        client_socket.send(bytes(msg, "utf8"))


def exit(event=None): 
    """Close connection"""
    msg = "{quit}"
    client_socket.send(bytes(msg, "utf8"))
    client_socket.close()
    window.quit()



def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()



#Front-end
window = tkinter.Tk()
window.title("Client")
window.configure(bg="#DCDCDC")
window.geometry("+0+10")


messages_frame = tkinter.Frame(window)
my_name = tkinter.StringVar()
my_vote = tkinter.StringVar()
my_msg = tkinter.StringVar()

scrollbar = tkinter.Scrollbar(messages_frame)

l_seu_nome = tkinter.Label(window, text="   Seu nome:", font="Arial 10 bold", width=11, height=2, bg="#DCDCDC")
l_assunto = tkinter.Label(window, text="       Voto:", font="Arial 10 bold", width=11, height=2, bg="#DCDCDC")

l_log = tkinter.Label(window, text="Log Urna", font="Arial 10 bold", height=1, bg="#DCDCDC")

l_divisoriac = tkinter.Label(window, width=1, height=1, bg="#DCDCDC")
l_divisorian = tkinter.Label(window, width=1, height=1, bg="#2F4F4F")
l_divisorias = tkinter.Label(window, width=1, height=1, bg="#2F4F4F")
l_divisoriae = tkinter.Label(window, width=1, height=1, bg="#2F4F4F")
l_divisoriaw = tkinter.Label(window, width=1, height=1, bg="#2F4F4F")

msg_list = tkinter.Listbox(window, height=11, width=38, font="Arial 9 bold", fg="#2F4F4F", border=2,
                           yscrollcommand=scrollbar.set)

e_seu_nome = tkinter.Entry(window, font="Arial 10 bold", fg="#2F4F4F", textvariable=my_name)
e_seu_nome.bind("<Return>", )
e_vote = tkinter.Entry(window, font="Arial 10 bold", fg="#2F4F4F", textvariable=my_vote)
e_vote.bind("<Return>", )

window.protocol("WM_DELETE_WINDOW", on_closing)

b_send_vote = tkinter.Button(window, text="    Votar   ", font="Arial 10 bold", height=1, border=3,
                               relief="groove", fg="#2F4F4F", command=send_vote)

b_exit = tkinter.Button(window, text="Sair", font="Arial 10 bold", fg="#B22222", border=3, relief='groove',
                        command=exit)

scrollbar.grid()
msg_list.grid(row=10, column=1, columnspan=2)
messages_frame.grid()

l_divisorian.grid(row=0, column=0, columnspan=3, sticky="e"+"w")
l_divisorias.grid(row=13, column=0, columnspan=3, sticky="e"+"w")
l_divisoriae.grid(row=0, column=0, rowspan=13, sticky="n"+"s")
l_divisoriaw.grid(row=0, column=3, rowspan=14, sticky="n"+"s")

l_seu_nome.grid(row=1, column=1, sticky="w")
l_assunto.grid(row=2, column=1, sticky="w")
l_divisoriac.grid(row=8, column=1)
l_log.grid(row=9, column=1, columnspan=3)

e_seu_nome.grid(row=1, column=2)
e_vote.grid(row=2, column=2)

b_send_vote.grid(row=6, column=2, sticky="n")
b_exit.grid(row=12, column=1, columnspan=3)


HOST = "localhost"
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR) #Conectar ao endereco do servidor

#Starta a thread para a atividade receive
receive_thread = Thread(target=receive)
receive_thread.start()

window.mainloop()