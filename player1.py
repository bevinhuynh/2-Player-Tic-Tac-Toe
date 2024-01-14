from tkinter import*
import socket
import threading
from gameboard import BoardClass


class player1_gui():
    '''Class that creates the user interface for player1, including
    connecting to the host via socket and playing the game.

    Attributes:
    guiSetup: Creates the gui for player 1
    host_entry: Creates an entry box for player1 to connect and communicate with the host
    submit_button: A button that gets information from the entry box
    run_gui: Runs the gui infinitely until destroyed.
    '''

    def __init__(self) -> None:
        '''Creates the player1_gui object
        '''
        self.guiSetup()
        self.host_entry()
        self.submit_button()
        self.run_gui()
    
    def guiSetup(self) -> None:
        '''Function that creates the gui for player 1
        '''
        self.player1_gui = Tk()
        self.player1_gui.title("Tic-Tac-Toe: Player 1")
        self.player1_gui.geometry("400x400")
    
    def host_entry(self) -> None:
        '''Function that creates an entry box so that player 1 can communicate with player2
        '''
        self.entry_box = Entry(self.player1_gui)
        self.entry_box.pack()

    def submit_button(self) -> None:
        '''Function that creates a button with the initial command of getting the information
         from the entry box and sends it to player 2. '''
        self.create_button = Button(self.player1_gui, text = "Enter Host IP Address", command = self.getting_host_ip)
        self.create_button.pack()
    
    def getting_host_ip(self) -> None:
        '''Function that gets the Ip address from the entry box, and configures the button with the command
        to get the host port.
        '''
        self.ip_label = Label(self.player1_gui, text = "IP Address: " + self.entry_box.get())
        self.ip_label.pack(side = BOTTOM, anchor= E)
        self.ip_address = self.entry_box.get()
        self.create_button.config(text = "Now Enter Host Port Number", command = self.getting_host_port)
       
    def getting_host_port(self) -> None:
        '''Function that gets the port number from the entry box, and runs the function to connect
        to the host.  Also handles ValueError if port number is not an int.
        '''
        try:
            self.host_label = Label(self.player1_gui, text = "Port Number: " + self.entry_box.get())
            self.port_number = int(self.entry_box.get())
            self.host_label.pack(side = BOTTOM, anchor= E)
            self.connect_to_host()
        except ValueError: 
            self.create_button.config(text = "Error Occurred, would you like to try again? (y/n)", command= self.error_handling)
    
    def error_handling(self) -> None:
        '''Function that handles any errors raised from other functions.  User is given the choice to 
        try again or not.  If yes, user is prompted to enter IP address and port number.  If no,
        program is destroyed
        '''
        if self.entry_box.get() == 'y':
            self.ip_label.forget()
            self.host_label.forget()
            self.create_button.config(text = "Enter Host IP Address", command = self.getting_host_ip)
        elif self.entry_box.get() == 'n':
            self.exit_label = Label(self.player1_gui, text = 'Exiting Program...').pack()
            self.create_button.forget()
            self.destroy_program()
        else:
            self.create_button.config(text = "Invalid input, try again, (y/n)")

    def connecting_to_host(self) -> socket:
        '''Function that takes the IP address and port number and attempts to connect to the host

        Returns:
            client_socket: socket that allows player 1 to communicate with player 2.
        '''
        host_address = (self.ip_address, self.port_number)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(host_address)
        self.connected = Label(self.player1_gui, text = "Connected")
        self.connected.pack()
        return client_socket
    
    def connect_to_host(self) -> None:
        '''Function that calls connecting_to_host(), handles any error that causes an invalid connection.
        Configs the button with the command to get player1's name from the entry box'''
        try:
            self.client = self.connecting_to_host()
            self.create_button.config(text = "Send player 2 your username", command = self.get_player1name)
            self.connected.forget()
        except AttributeError:
            self.ip_label.forget()
            self.host_label.forget()
            self.create_button.config("Error occurred, would you like to try again? (y/n)", command = self.error_handling)
        except ConnectionRefusedError:
            self.create_button.config(text = "Error Occurred, would you like to try again? (y/n)", command= self.error_handling)
        except OSError:
            self.create_button.config(text = "Error Occurred, would you like to try again? (y/n)", command= self.error_handling)
        except OverflowError:
            self.create_button.config(text = "Error Occurred, would you like to try again? (y/n)", command= self.error_handling)
    
    def get_player1name(self) -> None:
        '''Function that gets player1's name from the entry box, and sends it to player2
        '''
        self.awaiting_name = Label(self.player1_gui, text = "Awaiting player 2 name...")
        self.awaiting_name.pack()
        self.create_button.forget()
        self.player1_name = self.entry_box.get()
        self.client.send(bytes(self.player1_name, "utf-8"))
        self.entry_box.forget()
        self.get_player2_name()
    
    def get_player2_name(self) -> None:
        '''Function that waits to receive player2's name via the socket, creates BoardClass object'''
        self.player2_name = self.client.recv(1024)
        self.player_names = Label(self.player1_gui, text = "Player 1 name: " + self.player1_name + "," + " Player 2 name: " + self.player2_name.decode("utf-8")).pack()
        self.awaiting_name.forget()
        self.stats = BoardClass(self.player1_name, self.player2_name.decode('utf-8'), self.player1_gui)
        self.game_board()
    
    def game_board(self) -> None:
        '''Function that creates the game board
        Since player 1 has the first move, they get to click first.'''
        self.create_button.forget()
        self.clicked = True
        self.receiving = False
        self.frame = Frame(self.player1_gui)
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
        self.playerturn = Label(self.player1_gui, text = self.player1_name + '\'s turn, click on the board')
        self.playerturn.pack()
        self.get_move = threading.Thread(target = self.receive_move)
        self.get_move.start()

    def make_move(self, button: Button) -> None:
        '''Function that changes the button to the character of the player based on which button they pressed on.
        After button has been pressed and changed, function checks for win.
        If no win detected, player enters receiving mode and cannot make a move.
        
        Raises ValueError if player clicks on a spot that is not empty.'''
        if self.clicked == True:
            try:
                self.change_move = self.stats.updateGameBoard(button, 'X', self.receiving)
                self.playerturn.config(text = "Awaiting turn...")
                button_number = str(button).split('!')[-1]
                if button['text'] == 'X':
                    self.client.send(bytes(button_number, "utf-8"))
                    self.checking_win = self.check_win(self.stats, 'X')
                    if self.checking_win != True:
                        self.receiving = True
                        self.clicked = False
                        self.get_move = threading.Thread(target = self.receive_move)
                        self.get_move.start()
            except ValueError:
                self.playerturn.config(text = "Invalid spot, try a different spot")

    def receive_move(self) -> None:
        '''Function that receives a move from the other player, and changes the text of the button depending
        on the button the other player has chosen.  After move is received and button text is updated
        function calls check_win function.'''
        if self.clicked == False and self.receiving == True:
            self.receiving_button = self.client.recv(1024)
            if self.receiving_button.decode("utf-8") == 'button':
                self.stats.updateGameBoard(self.button1, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
            elif self.receiving_button.decode("utf-8") == 'button2':
                self.stats.updateGameBoard(self.button2, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
            elif self.receiving_button.decode("utf-8") == 'button3':
                self.stats.updateGameBoard(self.button3, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
            elif self.receiving_button.decode("utf-8") == 'button4':
                self.stats.updateGameBoard(self.button4, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
            elif self.receiving_button.decode("utf-8") == 'button5':
                self.stats.updateGameBoard(self.button5, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
            elif self.receiving_button.decode("utf-8") == 'button6':
                self.stats.updateGameBoard(self.button6, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
            elif self.receiving_button.decode("utf-8") == 'button7':
                self.stats.updateGameBoard(self.button7, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
            elif self.receiving_button.decode("utf-8") == 'button8':
                self.stats.updateGameBoard(self.button8, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
            elif self.receiving_button.decode("utf-8") == 'button9':
                self.stats.updateGameBoard(self.button9, 'O', self.receiving)
                self.checking_win = self.check_win(self.stats, 'O')
    
    def check_win(self, boardclass: BoardClass, character: str) -> bool:
        '''Function that checks for a win or tie after a move is made or received.  If win or tie is detected
        calls play_again function via thread and returns True.  If false, player gets to make a move.
        
        Returns True if win or tie detected, False if not'''
        self.winner = boardclass.isWinner(character,self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9)
        if self.winner == True:
            if character == 'X':
                self.playerturn.config(text = self.player1_name + " wins!")
                self.receiving = False
                self.clicked = False
                self.playing_again = threading.Thread(target=self.play_again)
                self.playing_again.start()
                return True
            elif character == 'O':
                self.playerturn.config(text = self.player2_name.decode('utf-8') + " wins!")
                self.receiving = False
                self.clicked = False
                self.playing_again = threading.Thread(target=self.play_again)
                self.playing_again.start()
                return True
        elif self.winner == False:
            self.tie = boardclass.boardisFull(self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9)
            if self.tie == True:
                self.playerturn.config(text = 'Tie!')
                self.receiving = False
                self.clicked = False
                self.playing_again = threading.Thread(target=self.play_again)
                self.playing_again.start()
                return True
            elif self.tie == False:
                if self.receiving == True:
                    self.receiving = False
                    self.clicked = True
                    self.playerturn.config(text = self.player1_name + '\'s turn, click on a spot')
                return False
    
    def play_again(self) -> None:
        '''Function that asks player 1 if they want to play again via entry box.  Button is configured to call
        sending_rematch.'''
        self.response_box = Entry(self.player1_gui)
        self.response_box.pack()
        self.create_button.pack()
        self.create_button.config(text = "Would you like to play again? (Y/y or N/n)", command= lambda: self.sending_rematch(self.stats))
    
    def sending_rematch(self,boardclass: BoardClass) -> None:
        '''Function that sends rematch or not based on response from entry box.  If yes, function sends rematch
        to player 2 via socket, and player 1 gets to make first move, and board are emptied.  If no, stats are printed, and button is
        configured to quit the program.'''
        self.response = self.response_box.get()
        if self.response == 'Y' or self.response == 'y':
            self.client.send(bytes("Play Again", "utf-8"))
            self.clicked = True
            self.receiving = False
            self.response_box.forget()
            self.create_button.forget()
            boardclass.resetGameBoard(self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9)
            boardclass.updateGamesPlayed()
            self.playerturn.config(text="Play again, " + self.player1_name + "\'s turn, click on a spot")
        elif self.response == 'n' or self.response == 'N':
            self.client.send(bytes("Fun Times", "utf-8"))
            self.playerturn.forget()
            self.response_box.forget()
            self.create_button.forget()
            self.frame.destroy()
            self.stats_frame = LabelFrame(self.player1_gui, text = self.player1_name + ' Game Stats')
            self.stats_frame.pack()
            boardclass.updateGamesPlayed()
            boardclass.computeStats(self.stats_frame, self.player1_name)
            self.create_button.pack()
            self.client.close()
            self.create_button.config(text="Quit Game", command = self.destroy_program)


    def destroy_program(self) -> None:
        '''Function that quits the gui'''
        self.player1_gui.quit()

    def run_gui(self) -> None:
        '''Function that runs the gui infinitely'''
        self.player1_gui.mainloop()



if __name__ == "__main__":
    player1_gui()
