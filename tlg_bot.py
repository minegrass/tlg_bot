from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, UserStatusRecently
import csv
from telethon.tl.types import InputPeerUser
import time
import random
import pandas as pd
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import ChannelParticipantAdmin

min_wait = 120
max_wait = 120
spammed = 0


class Scraper():
    def __init__(self, api_id, api_hash, phone_numb):
        # Enter Your 7 Digit Telegram API ID.
        self.api_id = api_id
        # Enter Yor 32 Character API Hash
        self.api_hash = api_hash
        # Enter Your Mobile Number With Country Code.
        self.phone = phone_numb

        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
        self.groups = []
        self.spam_text_msg = ['Hello, how are u?', 'Hi,are u free right now?', 'Im sorry if i bother you..']

    def connect(self):
        # connecting to telegram and checking if you are already authorized.
        # Otherwise send an OTP code request and ask user to enter the code
        # they received on their telegram account.
        # After logging in, a .session file will be created. This is a database file which makes your session persistent.

        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.phone)
            self.client.sign_in(self.phone, input('Enter verification code: '))

    def getGroups(self):
        # with this method you will get all your group names
        # offset_date and  offset_peer are used for filtering the chats. We are sending empty values to these parameters so API returns all chats
        # offset_id and limit are used for pagination.
        # limit is 200. it means last 200 chats of the user.

        chats = []
        last_date = None
        chunk_size = 200
        result = self.client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        ))
        chats.extend(result.chats)

        for chat in chats:
            try:
                if chat.megagroup == True:
                    self.groups.append(chat)
            except:
                continue

        # choose which group you want to scrape  members:
        for i, g in enumerate(self.groups):
            print(str(i) + '- ' + g.title)

    def saveFile(self):
        # with this method you will get group all members to csv file that you choosed group.

        g_index = 0
        target_group = self.groups[int(g_index)]

        print('Fetching Members...')
        all_participants = []
        all_participants = self.client.get_participants(target_group)

        print('Saving In file...')
        with open(target_group.title + ".csv", "w", encoding='UTF-8') as f:  # Enter your file name.
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
            for user in all_participants:
                accept = True
                if type(user.participant) == ChannelParticipantAdmin:
                    accept = False
                if not user.status == UserStatusRecently():
                    accept = False
                if accept:
                    if user.username:
                        username = user.username
                    else:
                        username = ""

                    if user.first_name:
                        first_name = user.first_name
                    else:
                        first_name = ""

                    if user.last_name:
                        last_name = user.last_name
                    else:
                        last_name = ""

                    name = (first_name + ' ' + last_name).strip()
                    writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
        print('Members scraped successfully.......')

    def read_data(self, groupname):
        user_id_hash_list = []
        with open(f'{groupname}', 'r', encoding="utf8") as csvfile:
            data = pd.read_csv(csvfile, delimiter=',')
            # print(data)
            return data
        #     for row in data:
        #         user_id_hash_list.append([row[1], row[2]])
        # user_id_hash_list.pop(0)
        # print(user_id_hash_list)
        # return user_id_hash_list

    def send_msg(self, input1, input2, username):
        if username != "":
            receiver = self.client.get_input_entity(username)
        else:
            receiver = InputPeerUser(user_id=int(input1), access_hash=int(input2))

        self.client.send_message(receiver, random.choice(self.spam_text_msg), file="./the_pic.png")

    def disconnect(self):
        self.client.disconnect()

    def start_spam(self, spam_df):
        for ind in (0, 0):
            print(ind, spam_df.index)
            try:
                print(spam_df['user id'][ind], spam_df['access hash'][ind])
                self.send_msg(spam_df['user id'][ind], spam_df['access hash'][ind], spam_df['username'][ind])

            except Exception as e:
                print(e)
                break
            finally:
                spam_df = spam_df.drop(spam_df.index[[0]], axis=0)
                ## save updated data list
                # print(spam_list)
                self.save_spam_list(spam_df.to_csv(index=False))
                time.sleep(random.randint(min_wait, max_wait))

    def save_spam_list(self, spam_list):
        with open('MEXC公式コミュニティ.csv', "w", encoding="utf8") as file:
            file.write(spam_list)

    def join_group(self, group_hash):
        self.client(JoinChannelRequest(group_hash))

    def add_spam_text(self, text):
        self.spam_text_msg.append(f'{text}')

    def clear_spam_text(self):
        self.spam_text_msg = []

# get group user by filter status ( recently on)
# make a UI
