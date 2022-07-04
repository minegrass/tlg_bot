from tlg_bot import Scraper
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import time
import random
import glob
import json


def json_file_to_bot_list():
    bots_acc = []
    all_files = glob.glob("./accounts/*.json")
    for i in range(0, len(all_files)):
        with open(all_files[i], 'r', encoding='utf-8') as one_acc_json:
            acc_data = json.loads(one_acc_json.read())
            # print(acc_data)
            bot = [acc_data['app_id'], f"{acc_data['app_hash']}", f"{acc_data['phone']}"]
            bots_acc.append(bot)
    return bots_acc


def bots_setup_to_list():
    json_bots = json_file_to_bot_list()
    bots_list = []
    for i in range(0, len(json_bots)):
        one_bot = Scraper(json_bots[i][0], json_bots[i][1], json_bots[i][2])
        bots_list.append(one_bot)
    return bots_list


def filter_banned_bots():
    bots_still_good = []
    bots_list = bots_setup_to_list()
    ##settings it loop switching account
    for telegram in bots_list:
        try:
            telegram.connect()
            # print('try run')
        except PhoneNumberBannedError:
            # print('bruh banned')
            pass
        else:
            # print('not banned')
            bots_still_good.append(telegram)
        finally:
            # print('finally run')
            telegram.disconnect()
    bots_list = bots_still_good
    return bots_list


def get_good_bot():
    return len(filter_banned_bots())


class TlgBot():

    def __init__(self):
        self.bots_list = filter_banned_bots()

###############################################################################
    def scrap_group(self, group_link):
        try:
            telegram = self.bots_list[0]
            telegram.connect()
            telegram.join_group(f'{group_link}')
            telegram.getGroups()
            telegram.saveFile()
            telegram.disconnect()
        except Exception as e:
            print(e)
        finally:
            self.bots_list = filter_banned_bots()

    def spam_to_group(self, group_name):
        while True:
            ##settings it loop switching account
            for telegram in self.bots_list:
                try:
                    telegram.connect()
                except Exception as e:
                    print(e)
                else:
                    print('else run')
                    # spam_df = telegram.read_data(f'{group_name}.csv')
                    # print(spam_df)
                    # telegram.start_spam(spam_df)
                    print('not banned')
                finally:
                    print('finally run')
                    telegram.disconnect()
                    self.bots_list = filter_banned_bots()

# https://my.telegram.org/auth?to=apps
