from tkinter import*
import socket
from gameboard import BoardClass
import threading

class SameName(Exception):
    '''Exception that is raised when player 2 has the same name as player 1'''
    pass

class player2_gui():
    '''Class that creates the user interface for player2, including
    connecting to the client via socket created and playing the game.

    Attributes:
    guiSetup: Creates the gui for player 2
    host_entry: Creates an entry box for player 2 to create the host socket
    submit_button: A button that gets information from the entry box
    run_gui: Runs the gui infinitely until destroyed.
    '''
    def __init__(self):
        '''Creates player2_gui object'''
        self.guiSetup()
        self.host_entry()
        self.submit_button()
        self.run_gui()
    
    def guiSetup(self) -> None:
        '''Function that creates the gui for player 2'''
        self.player2_gui = Tk()
        self.player2_gui.title("Tic-Tac-Toe: Player 2")
        self.player2_gui.geometry("400x400")
        self.player2_gui.resizable(0,0)
    
    def host_entry(self) -> None:
        '''Function that creates an entry box so that player 2 can communicate with player 1'''
        self.entry_box = Entry(self.player2_gui)
        self.entry_box.pack()

    def submit_button(self) -> None:
        '''Function that creates a button with the initial command of getting the information
         from the entry box and creating the host socket.'''
        self.create_button = Button(self.player2_gui, text = "Enter Your IP Address", command = self.getting_host_ip)
        self.create_button.pack()
    
    def getting_host_ip(self) -> None:
        '''Function that gets the Ip address from the entry box, and configures the button to get the port
        number'''
        self.ip_label = Label(self.player2_gui, text = "IP Address: " + self.entry_box.get())
        self.ip_label.pack(side = BOTTOM, anchor= E)
        self.ip_address = self.entry_box.get()
        self.create_button.config(text = "Now Enter Your Port Number", command = self.getting_host_port)
    
    def getting_host_port(self) -> None:
        '''Function that gets the port number from the entry box, calls the function to 
        connect to the client.  Handles ValueError if port number is not an int.'''
        try:
            self.host_label = Label(self.player2_gui, text = "Port Number: " + self.entry_box.get())
            self.port_number = int(self.entry_box.get())
            self.host_label.pack(side = BOTTOM, anchor= E)
            self.connect_to_client()
        except ValueError:
            self.create_button.config(text = "Error Occurred, please enter your IP address again", command = self.getting_host_ip)
            self.ip_label.forget()
    
    def creating_host_socket(self):
        '''Function that creates the host socket, handles any error raised due to incorrect
        information.'''
        try:
            binding_host_address = (self.ip_address, self.port_number)
            self.hosting_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.hosting_socket.bind(binding_host_address)
            self.awaiting_connection_label = Label(self.player2_gui, text = "Awaiting Connection...")
            self.awaiting_connection_label.pack()
            return self.hosting_socket
        except OSError:
            self.create_button.config(text = "Error Occurred, please enter your IP address again", command = self.getting_host_ip)
        except OverflowError:
            self.create_button.config(text = "Error Occurred, please enter your IP address again", command = self.getting_host_ip)
    
    def connect_to_client(self):
        '''Function that waits for a client connection after creating the host socket via
        creating_host_socket().  After accepting a connection, host waits for client to send
        their name over.  After receiving the name, host sends their name over to the client via the 
        button.'''
        try:
            self.hosting = self.creating_host_socket()
            self.hosting.listen(1)
            self.create_button.forget()
            self.host,self.address = self.hosting.accept()
            self.connected = Label(self.player2_gui, text = "Connection Accepted, awaiting name from Player 1...")
            self.connected.pack()
            self.awaiting_connection_label.forget()
            self.player1_name = self.host.recv(1024) 
            self.create_button = Button(text="Send player 1 your name", command = self.get_name)
            self.create_button.pack()
            self.connected.forget()
        except AttributeError:
            self.ip_label.forget()
            self.host_label.forget()
            self.create_button.config(text = "Error Occurred, please enter your IP address again", command = self.getting_host_ip)
    
    def get_name(self) -> None:
        '''Function that gets the name from the host and sends it to player 1
        BoardClass object is created for player 2, and game_board() function is called.  Raises SameName exception if 
        name is the same as player1's name, host has to enter a new name. '''
        try:
            self.player2_name = self.entry_box.get()
            if self.player2_name == self.player1_name.decode('utf-8'):
                raise SameName
            else:
                self.host.send(bytes(self.player2_name, "utf-8"))
                self.playernameslabel = Label(self.player2_gui, text = "Player 1 name: " + self.player1_name.decode("utf-8") + "," + " Player 2 name: " + self.player2_name).pack()
                self.entry_box.forget()
                self.create_button.forget() 
                self.stats = BoardClass(self.player1_name.decode('utf-8'), self.player2_name, self.player2_gui)
                self.game_board()
        except SameName:
            self.create_button.config(text = 'Name taken, try a different name.')
    
    
    def game_board(self) -> None:
        '''Function that creates the game board.
        For player2: Since they receive the move first, they cannot make a move
        and receive_move is called.'''
        self.clicked = False
        self.receiving = True
        self.frame = Frame(self.player2_gui)
        self.frame.pack()
        self.button1 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button1))
        self.button1.grid(row = 1, column= 0)
        self.button2 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button2))
        self.button2.grid(row = 1, column= 1)
        self.button3 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button3))
        self.button3.grid(row = 1, column= 2)
        self.button4 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button4))
        self.button4.grid(row = 2, column= 0)
        self.button5 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button5))
        self.button5.grid(row = 2, column= 1)
        self.button6 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button6))
        self.button6.grid(row = 2, column= 2)
        self.button7 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button7))
        self.button7.grid(row = 3, column= 0)
        self.button8 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button8))
        self.button8.grid(row = 3, column= 1)
        self.button9 = Button(self.frame,width = 3,height = 3, command = lambda: self.make_move(self.button9))
        self.button9.grid(row = 3, column= 2)
        self.playerturn = Label(self.player2_gui, text = "Awaiting turn...")
        self.playerturn.pack()
        self.get_move = threading.Thread(target = self.receive_move)
        self.get_move.start()
    
    def make_move(self, button: Button):
        '''Function that changes the button to the character of the player based on which button they pressed on.
        After button has been pressed and changed, function checks for win.
        If no win detected, player enters receiving mode and cannot make a move.
        
        Raises ValueError if player clicks on a spot that is not empty.'''
        if self.clicked == True:
            try:
                self.change_move = self.stats.updateGameBoard(button, 'O', self.receiving)
                self.playerturn.config(text = "Awaiting turn...")
                button_number = str(button).split('!')[-1]
                if button['text'] == 'O':
                    self.host.send(bytes(button_number, "utf-8"))
                    self.checking_win = self.check_win(self.stats, 'O')
                    if self.checking_win != True:
                        self.receiving = True
                        self.clicked = False
                        self.get_move = threading.Thread(target = self.receive_move)
                        self.get_move.start()
            except ValueError:
                self.playerturn.config(text = "Invalid spot, try a different spot")


    def receive_move(self):
        '''Function that receives a move from the other player, and changes the text of the button depending
        on the button the other player has chosen.  After move is received and button text is updated
        function calls check_win function.'''
        if self.clicked == False and self.receiving == True:
            self.receiving_button = self.host.recv(1024)
            if self.receiving_button.decode("utf-8") == 'button':
                self.stats.updateGameBoard(self.button1, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')
            elif self.receiving_button.decode("utf-8") == 'button2':
                self.stats.updateGameBoard(self.button2, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')    
            elif self.receiving_button.decode("utf-8") == 'button3':
                self.stats.updateGameBoard(self.button3, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')         
            elif self.receiving_button.decode("utf-8") == 'button4':
                self.stats.updateGameBoard(self.button4, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')        
            elif self.receiving_button.decode("utf-8") == 'button5':
                self.stats.updateGameBoard(self.button5, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')         
            elif self.receiving_button.decode("utf-8") == 'button6':
                self.stats.updateGameBoard(self.button6, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')               
            elif self.receiving_button.decode("utf-8") == 'button7':
                self.stats.updateGameBoard(self.button7, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')                
            elif self.receiving_button.decode("utf-8") == 'button8':
                self.stats.updateGameBoard(self.button8, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')           
            elif self.receiving_button.decode("utf-8") == 'button9':
                self.stats.updateGameBoard(self.button9, 'X', self.receiving)
                self.checking_win = self.check_win(self.stats, 'X')
                
   
    def check_win(self, boardclass: BoardClass, character: str) -> bool:
        '''Function that checks for a win or tie after a move is made or received.  If win or tie is detected
        calls play_again function via thread and returns True.  If false, player gets to make a move.

        Returns True if win or tie detected, False if not'''
        self.winner = boardclass.isWinner(character,self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9)
        if self.winner == True:
            if character == 'X':
                self.playerturn.config(text = self.player1_name.decode('utf-8') + " wins!")
                self.receiving = False
                self.clicked = False
                self.playing_again = threading.Thread(target= lambda: self.play_again(self.stats))
                self.playing_again.start()
                return True
            elif character == 'O':
                self.playerturn.config(text = self.player2_name + " wins!")
                self.receiving = False
                self.clicked = False
                self.playing_again = threading.Thread(target= lambda: self.play_again(self.stats))
                self.playing_again.start()
                return True
        elif self.winner == False:
            self.tie = boardclass.boardisFull(self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9)
            if self.tie == True:
                self.playerturn.config(text = 'Tie!')
                self.receiving = False
                self.clicked = False
                self.playing_again = threading.Thread(target= lambda: self.play_again(self.stats))
                self.playing_again.start()
                return True
            elif self.tie == False:
                if self.receiving == True:
                    self.receiving = False
                    self.clicked = True
                    self.playerturn.config(text = self.player2_name + '\'s turn, click on a spot')
                return False
        
    def play_again(self, boardclass: BoardClass) -> None:
        '''Function that waits for rematch from player 1 after a win or tie is detected, if yes, board is reset and player 2 waits for player 1 to
        make a move.  If no, stats are shown and player 2 can exit out of gui via button.'''
        self.awaiting_response = Label(self.player2_gui, text = "Awaiting response from " + self.player1_name.decode('utf-8'))
        self.awaiting_response.pack()
        self.response = self.host.recv(1024)
        if self.response.decode("utf-8") == "Play Again":
            self.receiving = True
            self.clicked = False
            self.playerturn.config(text = "Play again, awaiting turn...")
            boardclass.updateGamesPlayed()
            boardclass.resetGameBoard(self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9)
            self.awaiting_response.forget()
            self.get_move = threading.Thread(target = self.receive_move)
            self.get_move.start()
        elif self.response.decode('utf-8') == "Fun Times":
            self.playerturn.forget()
            self.frame.destroy()
            self.stats_frame = LabelFrame(self.player2_gui, text = self.player2_name + ' Game Stats')
            self.stats_frame.pack()
            boardclass.updateGamesPlayed()
            boardclass.computeStats(self.stats_frame, self.player2_name)
            self.awaiting_response.forget()
            self.create_button.pack()
            self.host.close()
            self.create_button.config(text="Quit Game", command = self.destroy_program)
    
    def destroy_program(self):
        '''Function that ends the gui'''
        self.player2_gui.quit()
    
    def run_gui(self):
        '''Function that keeps gui running'''
        self.player2_gui.mainloop()



if __name__ == "__main__":
    player2_gui()
