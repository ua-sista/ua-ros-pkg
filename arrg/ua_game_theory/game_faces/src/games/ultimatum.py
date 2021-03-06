import roslib
import rospy
from game_faces.msg import GamePlay
from Game import Game

class Ultimatum(Game):
    def __init__(self, player):
        Game.__init__(self, player)
        self.original = 10

    def take_first_turn(self):
# This may create other problems, but the not is to have this playing with the gui....it was that simple!
        if not self.player.is_first_player:
            gp = GamePlay(play_number=0,amount=0, player_id=self.player_id)
            gp.header.stamp = rospy.Time.now()
            self.play_pub.publish(gp)
        
    def take_turn(self, game_play):
        play_number = game_play.play_number
        if play_number == 0:
            if self.player.is_first_player:
                offer = -1
                while (offer < 0 or offer > 10):
                    try:
                        offer = int(raw_input("Input the first amount, between 0 and 10: "))
                    except ValueError:
                        print "Please enter a number between 0 and 10"
                        offer = -1
                        continue
                    if (offer < 0 or offer > 10):
                        print "Please enter a valid offer amount"
                self.offer = offer
                gp = GamePlay(play_number=1,amount=offer, player_id=self.player_id)
                gp.header.stamp = rospy.Time.now()
                self.play_pub.publish(gp)
                print "Waiting for second player"
            else:
                print "Waiting for first player"
        elif play_number == 1:
            if self.player.is_first_player:
                pass    
            else:
                print "Player 1 sent "+str(game_play.amount)
                print "You can either accept or reject this offer"
                choice = "X"
                while choice != "A" and choice != "R":
                    choice = raw_input("Please, input 'A' to accept or 'R' to reject the offer: ")
                    if choice == "A":
                        self.current_amount = str(game_play.amount)
                    elif choice == "R":
                        self.current_amount = 0
                    else:
                        print "Please choose A or R"
                print "Your payoff is now: " + str(self.current_amount)
                gp = GamePlay(play_number=2,amount=ord(choice), player_id=self.player_id)
                gp.header.stamp = rospy.Time.now()
                self.play_pub.publish(gp)
        elif play_number == 2:
            if self.player.is_first_player:
                choice = chr(game_play.amount)
                if choice == 'A':
                    which_choice = "Accepted"
                    self.current_amount = self.original - self.offer
                else:
                    which_choice = "Rejected"
                    self.current_amount = 0
                print "The other player decide to" + str(which_choice) + "your offer"
                print "Your payoff for this round is:" + str(self.current_amount)
                gp = GamePlay(play_number=3,amount=-1, player_id=self.player_id)
                gp.header.stamp = rospy.Time.now(); self.play_pub.publish(gp)  
            else:
                pass
            print "Please wait for the next game to start"
            print "unregistering"
            self.unregister_game()

