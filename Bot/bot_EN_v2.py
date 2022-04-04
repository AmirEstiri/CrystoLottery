import logging
import json
from os import path
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)
from web3 import Web3
from const import *
import time


# TODO don't check with SCDB yet => everything in telegram

TOK_KEYBOARD = [
    [KeyboardButton("1"), KeyboardButton("2"), KeyboardButton("3"), KeyboardButton("4"), KeyboardButton("5"), KeyboardButton("6"), KeyboardButton("7"), KeyboardButton("8"), KeyboardButton("9"), KeyboardButton("10")],
    [KeyboardButton("11"), KeyboardButton("12"), KeyboardButton("13"), KeyboardButton("14"), KeyboardButton("15"), KeyboardButton("16"), KeyboardButton("17"), KeyboardButton("18"), KeyboardButton("19"), KeyboardButton("20")],
    [KeyboardButton("21"), KeyboardButton("22"), KeyboardButton("23"), KeyboardButton("24"), KeyboardButton("25"), KeyboardButton("26"), KeyboardButton("27"), KeyboardButton("28"), KeyboardButton("29"), KeyboardButton("30")],
    [KeyboardButton("31"), KeyboardButton("32"), KeyboardButton("33"), KeyboardButton("34"), KeyboardButton("35"), KeyboardButton("36"), KeyboardButton("37"), KeyboardButton("38"), KeyboardButton("39"), KeyboardButton("40")],
    [KeyboardButton("41"), KeyboardButton("42"), KeyboardButton("43"), KeyboardButton("44"), KeyboardButton("45"), KeyboardButton("46"), KeyboardButton("47"), KeyboardButton("48"), KeyboardButton("49"), KeyboardButton("50")],
]


def read_data_from_SCDB():
    pass


def user_exists_lotto(usrnm):
    return usrnm in all_users.keys()
    # return contract.functions.userExists(usrnm).call()

# TODO fix and read from TDB
def num_referred_lotto(usrnm):
    return 0
    # return contract.functions.numberOfReferredUsers(usrnm).call()



def register_user(usrnm, wallet, rfrr):
    nonce = web3.eth.getTransactionCount(OWNER)
    tx = contract.functions.registerUser(usrnm, wallet, rfrr).buildTransaction({
        'chainId': CHAIN_ID, 'nonce': nonce, 'gas': 1000000, 'gasPrice': 10000000000,
    })
    sign_tx = web3.eth.account.signTransaction(tx, PRIV_KEY)
    tries = 0
    while tries < 3:
        tries += 1
        try:
            web3.eth.sendRawTransaction(sign_tx.rawTransaction)
            return True
        except ValueError:
            time.sleep(10)
    print(f"Register User failed for {usrnm}, {wallet}, {rfrr}")
    f = open(FAILED_FILE, "a")
    f.write(f"Register User: {usrnm}, {wallet}, {rfrr}\n")
    f.close()
    return False


def register_tickets(usrnm, tkns):
    nonce = web3.eth.getTransactionCount(OWNER)
    tx = contract.functions.registerTickets(usrnm, tkns[0], tkns[1], tkns[2]).buildTransaction({
        'chainId': CHAIN_ID, 'nonce': nonce, 'gas': 1000000, 'gasPrice': 10000000000,
    })
    sign_tx = web3.eth.account.signTransaction(tx, PRIV_KEY)
    tries = 0
    while tries < 3:
        tries += 1
        try:
            web3.eth.sendRawTransaction(sign_tx.rawTransaction)
            return True
        except ValueError:
            time.sleep(5)
    print(f"Register Tickets failed for {usrnm}, {tkns}")
    f = open(FAILED_FILE, "a")
    f.write(f"Register Tickets: {usrnm}, {tkns}\n")
    f.close()
    return False


def register_user_tickets(usrnm, wallet, rfrr, tkns):
    nonce = web3.eth.getTransactionCount(OWNER)
    tx = contract.functions.registerUserTickets(usrnm, wallet, rfrr, tkns[0], tkns[1], tkns[2]).buildTransaction({
        'chainId': CHAIN_ID, 'nonce': nonce, 'gas': 1000000, 'gasPrice': 10000000000,
    })
    sign_tx = web3.eth.account.signTransaction(tx, PRIV_KEY)
    tries = 0
    while tries < 3:
        tries += 1
        try:
            web3.eth.sendRawTransaction(sign_tx.rawTransaction)
            return True
        except ValueError:
            time.sleep(5)
    print(f"Register User Tickets failed for {usrnm}, {wallet}, {rfrr}, {tkns}")
    f = open(FAILED_FILE, "a")
    f.write(f"Register User Tickets: {usrnm}, {wallet}, {rfrr}, {tkns}\n")
    f.close()
    return False



def register_user_tickets_ref(usrnm, wallet, rfrr, usrnm_, wallet_, rfrr_, tkns):
    nonce = web3.eth.getTransactionCount(OWNER)
    tx = contract.functions.registerUserTicketsRef(usrnm, wallet, rfrr, usrnm_, wallet_, rfrr_, tkns[0], tkns[1], tkns[2]).buildTransaction({
        'chainId': CHAIN_ID, 'nonce': nonce, 'gas': 1000000, 'gasPrice': 10000000000,
    })
    sign_tx = web3.eth.account.signTransaction(tx, PRIV_KEY)
    tries = 0
    while tries < 3:
        tries += 1
        try:
            web3.eth.sendRawTransaction(sign_tx.rawTransaction)
            return True
        except ValueError:
            time.sleep(5)
    print(f"Register User Tickets Ref failed for {usrnm}, {wallet}, {rfrr}, {usrnm_}, {wallet_}, {rfrr_}, {tkns}")
    f = open(FAILED_FILE, "a")
    f.write(f"Register User Tickets Ref: {usrnm}, {wallet}, {rfrr}, {usrnm_}, {wallet_}, {rfrr_}, {tkns}\n")
    f.close()
    return False



def extract_transaction_info(txid):
    try:
        receipt = web3.eth.getTransaction(txid)
        value = int(receipt['input'][-64:], 16)
        to = Web3.toChecksumAddress('0x' + receipt['input'][10:-64][-40:])
        return {'id': txid, 'from': Web3.toChecksumAddress(receipt['from']), 'to': to, 'token_to': Web3.toChecksumAddress(receipt['to']), 'value': value}
    except ValueError:
        return {'id': txid, 'error': "Transaction not found"}



def tokens_complete(token, num):
    if len(token) != num:
        return False
    for i in range(num):
        if len(token[i]) != 6:
            return False
    return True




def check_token(token, tokens):
    if token.isnumeric() and int(token) <= 50 and int(token) >= 1:
        if int(token) not in tokens:
            return True
    return False



def start(update: Update, context: CallbackContext) -> None:
    print(update.message.from_user['id'])
    context.user_data['username'] = str(update.message.from_user['id'])
    if len(update.message.text.split(' ')) > 1 and update.message.text.split(' ')[1] != context.user_data['username'] and user_exists_lotto(update.message.text.split(' ')[1]):
        ref_id = update.message.text.split(' ')[1]
    else:
        ref_id = ""
    context.user_data['token'] = []
    context.user_data['ref'] = ref_id
    context.user_data['ticket_num'] = 0
    context.user_data['ticket'] = -1
    context.user_data['wallet'] = None
    context.user_data['txid'] = None
    context.user_data['state'] = 0
    if context.user_data['username'] in all_users.keys():
        context.user_data['wallet'] = all_users[context.user_data['username']][0]
        context.user_data['ref'] = all_users[context.user_data['username']][1]
    reply_text = f"welcome to <b>Crysto Lottery Bot</b>!\n"
    reply_text += f"Crysto is a lottery based on Smart Contract, deployed on Binance Smart Chain.\n"
    reply_text += f"You can check out our smart contract at this <a href=\"https://bscscan.com/address/{CONTRACT_ADDRESS}\">link</a>.\n"
    reply_text += f"You can choose 3 tickets with 10 USDT. For each ticket you can choose 6 tokens (a number from 1 to 50). At the time of lottery you will win according to how many tokens you have in common with the lottery tokens.\n"
    reply_text += f"In Crysto Lottery you can invite your friends to register in the lottery with your invite link. If you invite a person and they win, you will get a reward too. You can increase your chance of winning by inviting more users.\n"
    reply_text += f"⚠️ All transactions and wallets are in BEP20 blockchain"
    update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)
    reply_text = f"Here you can see the prizes for each correct number of tokens in a ticket:\n"
    reply_text += f"0️⃣ No prize\n1️⃣ No prize\n2️⃣ 10 USDT\n3️⃣ 50 USDT\n4️⃣ 200 USDT\n5️⃣ 10,000 USDT 💵\n6️⃣ 100,000 USDT 💰\n"
    reply_text += f"Here you can see the prizes for inviting a user:\n"
    reply_text += f"0️⃣ No prize\n1️⃣ No prize\n2️⃣ 2 USDT\n3️⃣ 5 USDT\n4️⃣ 20 USDT\n5️⃣ 1,000 USDT 💵\n6️⃣ 5,000 USDT 💰"
    update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)
    reply_text = f"What do you want to do?"
    keyboard = [
        [InlineKeyboardButton("Lottery Schedule 📅", callback_data='schedule')],
        [InlineKeyboardButton("Account Information 👤", callback_data='info')],
    ]
    if is_registration_open[0]:
        keyboard.append([InlineKeyboardButton("Register in Lottery 📝", callback_data='register')])
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(reply_text, reply_markup=markup)
    


def message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    state = context.user_data['state']
    if state > 100:
        tick = context.user_data['ticket']-1
        if check_token(text, context.user_data['token'][tick]) and len(context.user_data['token'][tick])<5:
            context.user_data['token'][tick].append(int(text))
            reply_text = f"Choose your next token:"
            markup = ReplyKeyboardMarkup(TOK_KEYBOARD)
            update.message.reply_text(reply_text, reply_markup=markup)
        elif check_token(text, context.user_data['token'][tick]) and len(context.user_data['token'][tick])==5:
            context.user_data['token'][tick].append(int(text))
            context.user_data['state'] = 7
            context.user_data['ticket'] = -1
            reply_text = f"Choose ticket:"
            keyboard = []
            for i in range(context.user_data['ticket_num']):
                if len(context.user_data['token'][i]) == 6:
                    keyboard.append([InlineKeyboardButton(f"Ticket {i+1} ✅", callback_data=f'ticket{i+1}')])
                else:
                    keyboard.append([InlineKeyboardButton(f"Ticket {i+1}", callback_data=f'ticket{i+1}')])
            if tokens_complete(context.user_data['token'], context.user_data['ticket_num']):
                keyboard.append([InlineKeyboardButton("Proceed to Payment 💵", callback_data='proceed')])
            keyboard.append([InlineKeyboardButton("Back 🔙", callback_data='back')])
            markup = InlineKeyboardMarkup(keyboard)
            # update.message.reply_text("", reply_markup=ReplyKeyboardRemove())
            update.message.reply_text(reply_text, reply_markup=markup)
        elif not check_token(text, context.user_data['token'][tick]):
            # reply_text = f"Wrong token!\nChooose again:"
            reply_text = f"Wrong token format ❌\nChoose again:"
            markup = ReplyKeyboardMarkup(TOK_KEYBOARD)
            update.message.reply_text(reply_text, reply_markup=markup)
    elif state == 8:
        context.user_data['wallet'] = text
        context.user_data['state'] = 7
        if user_exists_lotto(context.user_data['username']):
            all_users[context.user_data['username']][0] = context.user_data['wallet']
            all_users[context.user_data['username']][1] = context.user_data['ref']
        reply_text = f"You can buy a ticket in lottery and invite other people to join the lottery.\n"
        reply_text += f"If a person that you have invited, wins the lottery, you will get a prize too.\n"
        reply_text += f"Your personal invite link:\n"
        reply_text += f"<a href=\"https://t.me/CrystoLotteryBot?start={context.user_data['username']}\">Join Crysto Lottery Bot</a> "
        update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)
        context.user_data['ticket_num'] = 3
        context.user_data['token'] = [[] for _ in range(context.user_data['ticket_num'])]
        reply_text = f"Choose ticket:"
        keyboard = []
        for i in range(int(context.user_data['ticket_num'])):
            keyboard.append([InlineKeyboardButton(f"Ticket {i+1}", callback_data=f'ticket{i+1}')])
        if tokens_complete(context.user_data['token'], context.user_data['ticket_num']):
            keyboard.append([InlineKeyboardButton("Proceed to Payment 💵", callback_data='proceed')])
        keyboard.append([InlineKeyboardButton("Back 🔙", callback_data='back')])
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(reply_text, reply_markup=markup)
    elif state == 9:
        context.user_data['txid'] = text
        context.user_data['state'] = 10
        reply_text = f"After the transaction is confirmed, press <b>Check Transaction</b> to confirm your payment."
        keyboard = [
            [InlineKeyboardButton("Check Transaction ⚙️", callback_data='check')],
            [InlineKeyboardButton("Back 🔙", callback_data='back')],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(reply_text, reply_markup=markup, parse_mode=ParseMode.HTML)




def buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    state = context.user_data['state']
    query.answer()
    if query.data == 'schedule' and state == 0:
        reply_text = f"The lottery will automatically play after 100 registered users"
        keyboard = [
            [InlineKeyboardButton("Lottery Schedule 📅", callback_data='schedule')],
            [InlineKeyboardButton("Account Information 👤", callback_data='info')],
        ]
        if is_registration_open[0]:
            keyboard.append([InlineKeyboardButton("Register in Lottery 📝", callback_data='register')])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'register' and state == 0 and is_registration_open[0]:
        context.user_data['state'] = 8
        reply_text = f"Send your wallet address 💰"
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data.startswith('ticket') and state == 7:
        context.user_data['ticket'] = int(query.data[6:])
        context.user_data['state'] = 100 + context.user_data['ticket']
        context.user_data['token'][context.user_data['ticket']-1] = []
        reply_text = f"Ticket {context.user_data['ticket']}\nChoose token:"
        markup = ReplyKeyboardMarkup(TOK_KEYBOARD)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == "proceed" and state == 7:
        context.user_data['state'] = 9
        reply_text = f"Send 10 USDT to this wallet:\n"
        reply_text += f"<code>{CONTRACT_ADDRESS}</code>\n"
        reply_text += f"Send the transaction id (or hash id) of your payment:"
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup, parse_mode=ParseMode.HTML)
    elif query.data == "check" and state == 10:
        tx_info = extract_transaction_info(context.user_data['txid'])
        if 'error' not in tx_info.keys():
            if tx_info['value'] >= 10000000000000000000 and tx_info['token_to'] == USDT_CONTRACT: # 10 USDT
                if tx_info['to'] == CONTRACT_ADDRESS:
                    if not tx_info['id'] in all_txid:
                        send_message(ADMINS[0], 0)
                        f = open(TX_FILE, "a")
                        f.write(f"{tx_info['id']}\n")
                        f.close()
                        if not user_exists_lotto(context.user_data['username']):
                            res = "SUCCESS"
                            # res = register_user_tickets(context.user_data['username'], context.user_data['wallet'], context.user_data['ref'], context.user_data['token'])
                            all_users[context.user_data['username']] = [context.user_data['wallet'], context.user_data['ref'], res]
                            if context.user_data['username'] in all_tickets.keys():
                                all_tickets[context.user_data['username']].append([context.user_data['token'][0], res])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][1], res])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][2], res])
                            else:
                                all_tickets[context.user_data['username']] = [[context.user_data['token'][0], res]]
                                all_tickets[context.user_data['username']].append([context.user_data['token'][1], res])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][2], res])
                        else:
                            res = "SUCCESS"
                            # res = register_tickets(context.user_data['username'], context.user_data['token'])
                            if not context.user_data['username'] in all_users.keys():
                                all_users[context.user_data['username']] = [context.user_data['wallet'], context.user_data['ref'], "SUCCESS"]
                            if context.user_data['username'] in all_tickets.keys():
                                all_tickets[context.user_data['username']].append([context.user_data['token'][0], res])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][1], res])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][2], res])
                            else:
                                all_tickets[context.user_data['username']] = [[context.user_data['token'][0], res]]
                                all_tickets[context.user_data['username']].append([context.user_data['token'][1], res])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][2], res])
                            all_txid.append(tx_info['id'])
                        context.user_data['state'] = 6
                        reply_text = f"Account Information 📊\n"
                        for i in range(len(all_tickets[context.user_data['username']])):
                             reply_text += f"Ticket {i+1}: {all_tickets[context.user_data['username']][i][0]}\n"
                        if context.user_data['ref'] != '':
                            reply_text += f"Inviter ID: {context.user_data['ref']}"
                        reply_text += f"Number of invited people 📉: {num_referred_lotto(context.user_data['username'])}\n"
                        keyboard = [[InlineKeyboardButton('Back 🔙', callback_data='back')]]
                        markup = InlineKeyboardMarkup(keyboard)
                        query.message.reply_text(reply_text, reply_markup=markup)
                    else:
                        reply_text = f"This transaction has been used before ❌"
                        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
                        markup = InlineKeyboardMarkup(keyboard)
                        query.message.reply_text(reply_text, reply_markup=markup)
                else:
                    reply_text = f"Make sure you sent the transaction to this wallet:\n <code>{CONTRACT_ADDRESS}</code>"
                    keyboard = [[InlineKeyboardButton("بازگشت 🔙", callback_data='back')]]
                    markup = InlineKeyboardMarkup(keyboard)
                    query.message.reply_text(reply_text, reply_markup=markup, parse_mode=ParseMode.HTML)
            else:
                reply_text = f"Make sure you sent at least 10 USDT"
                keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
                markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(reply_text, reply_markup=markup)
        else:
            reply_text = f"Incorrect hash id ❌\nPlease check and send again:"
            keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
            markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 7:
        context.user_data['state'] = 8
        reply_text = f"Send your wallet address 💰"
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 8:
        context.user_data['state'] = 0
        reply_text = f"What do you want to do?"
        keyboard = [
            [InlineKeyboardButton("Lottery Schedule 📅", callback_data='schedule')],
            [InlineKeyboardButton("Account Information 👤", callback_data='info')],
        ]
        if is_registration_open[0]:
            keyboard.append([InlineKeyboardButton("Register in Lottery 📝", callback_data='register')])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 6:
        context.user_data['state'] = 0
        reply_text = f"What do you want to do?"
        keyboard = [
            [InlineKeyboardButton("Lottery Schedule 📅", callback_data='schedule')],
            [InlineKeyboardButton("Account Information 👤", callback_data='info')],
        ]
        if is_registration_open[0]:
            keyboard.append([InlineKeyboardButton("Register in Lottery 📝", callback_data='register')])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 9:
        context.user_data['state'] = 7
        reply_text = f"Choose ticket:"
        keyboard = []
        for i in range(context.user_data['ticket_num']):
            if len(context.user_data['token'][i]) == 6:
                keyboard.append([InlineKeyboardButton(f"Ticket {i+1} ✅", callback_data=f'ticket{i+1}')])
            else:
                keyboard.append([InlineKeyboardButton(f"Ticket {i+1}", callback_data=f'ticket{i+1}')])
        if tokens_complete(context.user_data['token'], context.user_data['ticket_num']):
            keyboard.append([InlineKeyboardButton("Proceed to Payment 💵", callback_data='proceed')])
        keyboard.append([InlineKeyboardButton("Back 🔙", callback_data='back')])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 10:
        context.user_data['state'] = 9
        reply_text = f"Send 10 USDT to this wallet:\n"
        reply_text += f"<code>{CONTRACT_ADDRESS}</code>\n"
        reply_text += f"Send the transaction id (or hash id) of your payment:"
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup, parse_mode=ParseMode.HTML)
    elif query.data == 'info' and state == 0:
        if user_exists_lotto(context.user_data['username']):
            context.user_data['state'] = 6
            reply_text = f"Account Information 📊\n"
            for i in range(len(all_tickets[context.user_data['username']])):
                reply_text += f"Ticket {i+1}: {all_tickets[context.user_data['username']][i][0]}\n"
            if context.user_data['ref'] != "":
                reply_text += f"Inviter Id: {context.user_data['ref']}"
            reply_text += f"Number of invited users 📉: {num_referred_lotto(context.user_data['username'])}\n"
            keyboard = [[InlineKeyboardButton('Back 🔙', callback_data='back')]]
            markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(reply_text, reply_markup=markup)
        else:
            reply_text = f"You have not registered\n"
            reply_text += f"What do you want to do?"
            keyboard = [
                [InlineKeyboardButton("Lottery Schedule 📅", callback_data='schedule')],
                [InlineKeyboardButton("Account Information 👤", callback_data='info')],
            ]
            if is_registration_open[0]:
                keyboard.append([InlineKeyboardButton("Register in Lottery 📝", callback_data='register')])
            markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(reply_text, reply_markup=markup)
    else:
        print(f"user: {context.user_data['username']}, state: {context.user_data['state']}, data: {query.data}")



def info(update: Update, context: CallbackContext) -> None:
    reply_text = f"Your account information:\n"
    reply_text += f"Wallet address: {context.user_data['wallet']}\n"
    reply_text += f"Tokens: {context.user_data['token']}\n"
    reply_text += f"Referer: {context.user_data['ref']}\n"
    update.message.reply_text(reply_text)



def record_data(update: Update, context: CallbackContext) -> None:
    if context.user_data['username'] in ADMINS:
        f = open(USER_FILE, "w")
        f.write(json.dumps(all_users))
        f.close()

        f = open(TICKET_FILE, "w")
        f.write(json.dumps(all_tickets))
        f.close()


def change_registration_status(update: Update, context: CallbackContext) -> None:
    if context.user_data['username'] in ADMINS:
        is_registration_open[0] = not is_registration_open[0]


def send_message(user_id, amount):
    # text = f"شما برنده ی "
    # text += f"{amount} USDT "
    # text += f"شده اید 🎉🎉\nمبلغ به کیف پول شما واریز شده است 💵💸"
    # text = f"You have won {amount} USDT 🎉🎉\nThe winnings have been sent to your wallet 💵💸"
    text = f"someone registered!"
    send_text = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={user_id}&text={text}"
    requests.get(send_text)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

web3 = Web3(Web3.HTTPProvider(BSC))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

is_registration_open = [True]
all_txid = []
all_users = {}
all_tickets = {}


if path.exists(TX_FILE):
    f = open(TX_FILE, "r")
    all_txid.append(f.read())
    f.close()
else:
    f = open(TX_FILE, "w")
    f.close()

if path.exists(USER_FILE):
    f = open(USER_FILE, "r")
    all_users = json.load(f)
    f.close()

if path.exists(TICKET_FILE):
    f = open(TICKET_FILE, "r")
    all_tickets = json.load(f)
    f.close()

if not path.exists(FAILED_FILE):
    f = open(FAILED_FILE, "w")
    f.close()

updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('info', info))
updater.dispatcher.add_handler(CommandHandler('TDB', record_data))
updater.dispatcher.add_handler(CommandHandler('CRS', change_registration_status))
updater.dispatcher.add_handler(MessageHandler(~Filters.command, message))
updater.dispatcher.add_handler(CallbackQueryHandler(buttons))
updater.start_polling()
updater.idle()