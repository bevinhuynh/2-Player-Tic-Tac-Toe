from tkinter import*
import socket
from gameboard import BoardClass
#192.168.1.187

class player2_gui():
    def __init__(self):
        self.guiSetup()
        self.host_entry()
        self.submit_button()
        self.run_gui()
    
    def guiSetup(self):
        self.player2_gui = Tk()
        self.player2_gui.title("Tic-Tac-Toe: Player 2")
        self.player2_gui.geometry('400x400')
        self.player2_gui.resizable(0,0)
    
    def host_entry(self):
        self.entry_box = Entry(self.player2_gui, width= 10)
        self.entry_box.grid()

    def submit_button(self):
        self.create_button = Button(self.player2_gui, text = "Enter Your IP Address", command = self.getting_host_ip)
        self.create_button.grid()
    
    def getting_host_ip(self):
        self.ip_label = Label(self.player2_gui, text = "IP Address: " + self.entry_box.get())
        self.ip_label.grid(row = 10)
        self.ip_address = self.entry_box.get()
        self.create_button.config(text = "Now Enter Your Port Number", command = self.getting_host_port)
    
    def getting_host_port(self):
        try:
            self.host_label = Label(self.player2_gui, text = "Port Number: " + self.entry_box.get())
            self.port_number = int(self.entry_box.get())
            self.host_label.grid(row = 11)
            self.run_game()
        except ValueError:
            self.create_button.config(text = "Error Occurred, please enter your IP address again", command = self.getting_host_ip)
            self.ip_label.grid_remove()
    
    def creating_host_socket(self):
        try:
            binding_host_address = (self.ip_address, self.port_number)
            self.hosting_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.hosting_socket.bind(binding_host_address)
            self.awaiting_connection_label = Label(self.player2_gui, text = "Awaiting Connection...")
            self.awaiting_connection_label.grid()
            return self.hosting_socket
        except OSError:
            self.create_button.config(text = "Error Occurred, please enter your IP address again", command = self.getting_host_ip)
        except OverflowError:
            self.create_button.config(text = "Error Occurred, please enter your IP address again", command = self.getting_host_ip)
    
    def run_game(self):
        try:
            self.hosting = self.creating_host_socket()
            self.hosting.listen(1)
            self.create_button.grid_remove()
            self.host,self.address = self.hosting.accept()
            self.connected = Label(self.player2_gui, text = "Connection Accepted, awaiting name from Player 1...")
            self.connected.grid()
            self.awaiting_connection_label.grid_remove()
            self.player1_name = self.host.recv(1024) 
            self.create_button = Button(text="Send player 1 your name", command = self.get_name)
            self.create_button.grid()
            self.connected.forget()

        except AttributeError:
            self.ip_label.forget()
            self.host_label.forget()
            self.create_button.config(text = "Error Occurred, please enter your IP address again", command = self.getting_host_ip)
    
    def get_name(self):
        self.player2_name = self.entry_box.get()
        self.host.send(bytes(self.player2_name, "utf-8"))
        self.playernameslabel = Label(self.player2_gui, text = "Player 1 name: " + self.player1_name.decode("utf-8") + "," + " Player 2 name: " + self.player2_name).grid()
        self.entry_box.forget()
        self.create_button.forget() 
    
    def gameplay(self):
        self.button1 = Button(self.player2_gui,)
    def run_gui(self):
        #Get os error maybe
        #Get overflow error maybe
        self.player2_gui.mainloop()


if __name__ == "__main__":
    player2_gui()
