from tkinter import*


class BoardClass():
    """Class that holds information for the game, including player
    names, stats, the game board, creating and updating the board,
    checking for wins, losses, and ties.

    Attributes:
        player1_name: name of player 1, chosen by user input
        player2_name: name of player 2, chosen by user input
        player1_win_count: the amount of wins player 1 has
        player2_win_count: the amount of wins player 2 has
        player1_loss_count: the amount of losses player 1 has
        player2_loss_count: the amount of losses player 2 has
        tie_count = the amount of ties that have occured
        games = amount of games played
    """
    def __init__(self, player1_name = '', player2_name = '', player_gui = '') -> None:
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player_gui = player_gui
        self.recent_player = ''
        self.player1_win_count = 0
        self.player2_loss_count = 0
        self.player1_loss_count = 0
        self.player2_win_count = 0
        self.tie_count = 0
        self.games = 0

    def updateGamesPlayed(self) -> None:
        '''Function that tracks how many games is played
        
        Returns:
        self.games -> int'''
        self.games += 1
        return self.games
    
    def resetGameBoard(self, button1: Button, button2: Button, button3: Button, button4: Button, button5: Button, button6: Button, button7:Button, button8: Button, button9: Button) -> None:
        button1['text'] = ''
        button2['text'] = ''
        button3['text'] = ''
        button4['text'] = ''
        button5['text'] = ''
        button6['text'] = ''
        button7['text'] = ''
        button8['text'] = ''
        button9['text'] = ''

    
    def updateGameBoard(self, button: Button, character: str, receiving: bool) -> None:
        '''Function that updates the game board'''
        if button['text'] == '' and receiving == False:
            button.config(text = character)
        elif button['text'] == 'X' or button['text'] == 'O' and receiving == False:
            raise ValueError
        elif receiving == True:
            button.config(text = character)
    
    def isWinner(self, character: str, button1: Button, button2: Button, button3: Button, button4: Button, button5: Button, button6: Button, button7: Button, button8: Button, button9: Button) -> bool:
        '''Function that checks if there is a winner, and updates win and loss stats
        
        Returns:
            True if there is a winner, False if not'''
        if character == 'X':
            if button1['text'] == character and button2['text'] == character and button3['text'] == character:
                self.player1_win_count += 1
                self.player2_loss_count += 1
                return True
            elif button4['text'] == character and button5['text'] == character and button6['text'] == character:
                self.player1_win_count += 1
                self.player2_loss_count += 1
                return True
            elif button7['text'] == character and button8['text'] == character and button9['text'] == character:
                self.player1_win_count += 1
                self.player2_loss_count += 1
                return True
            elif button1['text'] == character and button4['text'] == character and button7['text'] == character:
                self.player1_win_count += 1
                self.player2_loss_count += 1
                return True
            elif button2['text'] == character and button5['text'] == character and button8['text'] == character:
                self.player1_win_count += 1
                self.player2_loss_count += 1
                return True
            elif button3['text'] == character and button6['text'] == character and button9['text'] == character:
                self.player1_win_count += 1
                self.player2_loss_count += 1
                return True
            elif button1['text'] == character and button5['text'] == character and button9['text'] == character:
                self.player1_win_count += 1
                self.player2_loss_count += 1
                return True
            elif button3['text'] == character and button5['text'] == character and button7['text'] == character:
                self.player1_win_count += 1
                self.player2_loss_count += 1
                return True
            else:
                return False
        if character == 'O':
            if button1['text'] == character and button2['text'] == character and button3['text'] == character:
                self.player2_win_count += 1
                self.player1_loss_count += 1
                return True
            elif button4['text'] == character and button5['text'] == character and button6['text'] == character:
                self.player2_win_count += 1
                self.player1_loss_count += 1
                return True
            elif button7['text'] == character and button8['text'] == character and button9['text'] == character:
                self.player2_win_count += 1
                self.player1_loss_count += 1
                return True
            elif button1['text'] == character and button4['text'] == character and button7['text'] == character:
                self.player2_win_count += 1
                self.player1_loss_count += 1
                return True
            elif button2['text'] == character and button5['text'] == character and button8['text'] == character:
                self.player2_win_count += 1
                self.player1_loss_count += 1
                return True
            elif button3['text'] == character and button6['text'] == character and button9['text'] == character:
                self.player2_win_count += 1
                self.player1_loss_count += 1
                return True
            elif button1['text'] == character and button5['text'] == character and button9['text'] == character:
                self.player2_win_count += 1
                self.player1_loss_count += 1
                return True
            elif button3['text'] == character and button5['text'] == character and button7['text'] == character:
                self.player2_win_count += 1
                self.player1_loss_count += 1
                return True
            else:
                return False
    
    def boardisFull(self, button1: Button, button2: Button, button3: Button, button4: Button, button5:Button, button6:Button, button7: Button, button8: Button, button9: Button) -> bool:
        '''Function that checks if the board is full, and updates tie count if there is a tie
        
        Returns True if there is a full board and a tie, False if not.'''
        if button1['text'] != '' and button2['text'] != '' and button3['text'] != '' and button4['text'] != '' and button5['text'] != '' and button6['text'] != '' and button7['text'] != '' and button8['text'] != '' and button9['text'] != '':
            self.tie_count += 1
            return True
        else:
            return False
    
    def computeStats(self, display_frame: Frame, player_name: str) -> None:
        '''Creates the stats and displays it in player guis.'''
        self.user_names = Label(display_frame, text = "Player Names: " + self.player1_name + ", " + self.player2_name).pack()
        if player_name == self.player1_name:
            self.games_played = Label(display_frame, text = f"Games Played: {self.games}").pack()
            self.player1_wins = Label(display_frame, text = f"{self.player1_name}'s wins: {self.player1_win_count}").pack()
            self.player1_losses = Label(display_frame, text = f"{self.player1_name}'s losses: {self.player1_loss_count}").pack()
            self.ties = Label(display_frame, text = f'Tie Count: {self.tie_count}').pack()
        elif player_name == self.player2_name:
            self.games_played = Label(display_frame, text = f"Games Played: {self.games}").pack()
            self.player2_wins = Label(display_frame, text = f"{self.player2_name}'s wins: {self.player2_win_count}").pack()
            self.player2_losses = Label(display_frame, text = f"{self.player2_name}'s losses: {self.player2_loss_count}").pack()
            self.ties = Label(display_frame, text = f'Tie Count: {self.tie_count}').pack()
        