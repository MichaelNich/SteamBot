import gevent
from steam.core.msg import MsgProto
from steam.enums.emsg import EMsg
from steam import SteamClient
from steam.core.cm import CMClient

"""
Steam libraries used here, were made by Rossen Georgiev!
"""

class Bot(object):
    def __init__(self, steam_user, steam_pass, steam_owner_id):
        self.steam_user = steam_user
        self.steam_pass = steam_pass
        self.steam_owner_id = steam_owner_id
        self.client = SteamClient()
        
    def Show_Login_Info(self):
        """
        Show username and steamid from User!
        """
        
        msg = self.client.wait_msg(EMsg.ClientAccountInfo)
        print('Logged on as: %s'%msg.body.persona_name)
        print('SteamID: %s'%repr(self.client.steam_id))
        
    def Change_Status_And_Name(self, status, user_name=None):
        """
        Change User status for friends and Name!!
        0 - Offline, 1 - Online, 2 - Busy, 3 - Away, 4 - Snooze,
        5 - looking to trade, 6 - looking to play.
        status type: int
        status example: 1
        user_name type: string
        user_name example: 'STEAM BOT'
        """
        
        msg = MsgProto(EMsg.ClientChangeStatus)
        msg.body.persona_state = status
        if user_name != None:
            msg.body.player_name = user_name
        else:
            pass
        self.client.send_message_and_wait(msg, None)
        
    def Send_Friend_Msg(self, friend_steam_id, message):
        """
        Send a message to a friend with his steamID!
        friend_steam_id type: int
        friend_steam_id example: 77777777777777777
        message type: string
        message example: 'Hello'
        """
        
        msg = MsgProto(EMsg.ClientFriendMsg)
        msg.body.steamid = friend_steam_id
        msg.body.chat_entry_type = 1
        msg.body.message = message.encode('utf-8')
        self.client.send_message_and_wait(msg, None)
        
    def Send_Friend_Request(self, friend_steam_id):
        """
        Send a friend request to a friend!
        friend_steam_id type: int
        friend_steam_id example: 77777777777777777
        """
        
        msg = MsgProto(EMsg.ClientAddFriend)
        msg.body.steamid_to_add = friend_steam_id
        self.client.send_message_and_wait(msg, None)

    def Console(self):
        """
        Terminal to control the bot via friend msg!!
        """
        
        self.commands = {'-shutdown': 'self.Change_Status_And_Name(0, None)' \
                         '\nself.Send_Friend_Msg(self.steam_owner_id, "BOT OFF!")'}
        while True:
            msg = self.client.wait_msg(EMsg.ClientFriendMsgIncoming)
            if msg.body.chat_entry_type == 1:
                msg_decoded = str(msg.body.message.decode().strip('\x00'))
                if msg_decoded.startswith('-'):
                    for command in self.commands:
                        if command == msg_decoded:
                            exec(self.commands['%s'%command])
                        else:
                            self.Send_Friend_Msg(self.steam_owner_id, "There is no command with this name!")
                else:
                    print('message')
            else:
                print('writing')
                
    def Stay_Online(self):
        """
        If you not comunicate with steam in 90 seconds, you are disconnected, 
        so this function helps to stay connected
        """
        
        while True:
            self.Change_Status_And_Name(1, None)
            gevent.sleep(85)
            
    def Run(self):
        """
        Start the bot!
        """
        
        self.client.cli_login(self.steam_user, self.steam_pass)
        self.Show_Login_Info()
        self.Change_Status_And_Name(1, None)
        self.Send_Friend_Msg(self.steam_owner_id, 'BOT ON!')
        self.t_stay_online = [gevent.spawn(self.Stay_Online)]
        self.Console()

        

def Main():
    user = ''
    pass_ = ''
    steam_owner_id = 77777777777777777 #Who gonna control the bot via msg friend! change to your steam_ID

    steamBot = Bot(user, pass_, steam_owner_id)
    steamBot.Run()

if __name__ == '__main__':
    Main()
