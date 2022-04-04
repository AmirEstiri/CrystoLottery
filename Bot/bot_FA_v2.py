import logging
import json
from os import path
from nbformat import read
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


def num_referred_lotto(usrnm):
    num_ref = 0
    for k, v in all_users.items():
        if v[1] == usrnm and k in all_tickets.keys():
            num_ref += 1
    return num_ref
    # return contract.functions.numberOfReferredUsers(usrnm).call()



# def register_user(usrnm, wallet, rfrr):
#     nonce = web3.eth.getTransactionCount(OWNER)
#     tx = contract.functions.registerUser(usrnm, wallet, rfrr).buildTransaction({
#         'chainId': CHAIN_ID, 'nonce': nonce, 'gas': 1000000, 'gasPrice': 10000000000,
#     })
#     sign_tx = web3.eth.account.signTransaction(tx, PRIV_KEY)
#     tries = 0
#     while tries < 3:
#         tries += 1
#         try:
#             web3.eth.sendRawTransaction(sign_tx.rawTransaction)
#             return True
#         except ValueError:
#             time.sleep(10)
#     print(f"Register User failed for {usrnm}, {wallet}, {rfrr}")
#     f = open(FAILED_FILE, "a")
#     f.write(f"Register User: {usrnm}, {wallet}, {rfrr}\n")
#     f.close()
#     return False


# def register_tickets(usrnm, tkns):
#     nonce = web3.eth.getTransactionCount(OWNER)
#     tx = contract.functions.registerTickets(usrnm, tkns[0], tkns[1], tkns[2]).buildTransaction({
#         'chainId': CHAIN_ID, 'nonce': nonce, 'gas': 1000000, 'gasPrice': 10000000000,
#     })
#     sign_tx = web3.eth.account.signTransaction(tx, PRIV_KEY)
#     tries = 0
#     while tries < 3:
#         tries += 1
#         try:
#             web3.eth.sendRawTransaction(sign_tx.rawTransaction)
#             return True
#         except ValueError:
#             time.sleep(5)
#     print(f"Register Tickets failed for {usrnm}, {tkns}")
#     f = open(FAILED_FILE, "a")
#     f.write(f"Register Tickets: {usrnm}, {tkns}\n")
#     f.close()
#     return False


# def register_user_tickets(usrnm, wallet, rfrr, tkns):
#     nonce = web3.eth.getTransactionCount(OWNER)
#     tx = contract.functions.registerUserTickets(usrnm, wallet, rfrr, tkns[0], tkns[1], tkns[2]).buildTransaction({
#         'chainId': CHAIN_ID, 'nonce': nonce, 'gas': 1000000, 'gasPrice': 10000000000,
#     })
#     sign_tx = web3.eth.account.signTransaction(tx, PRIV_KEY)
#     tries = 0
#     while tries < 3:
#         tries += 1
#         try:
#             web3.eth.sendRawTransaction(sign_tx.rawTransaction)
#             return True
#         except ValueError:
#             time.sleep(5)
#     print(f"Register User Tickets failed for {usrnm}, {wallet}, {rfrr}, {tkns}")
#     f = open(FAILED_FILE, "a")
#     f.write(f"Register User Tickets: {usrnm}, {wallet}, {rfrr}, {tkns}\n")
#     f.close()
#     return False



# def register_user_tickets_ref(usrnm, wallet, rfrr, usrnm_, wallet_, rfrr_, tkns):
#     nonce = web3.eth.getTransactionCount(OWNER)
#     tx = contract.functions.registerUserTicketsRef(usrnm, wallet, rfrr, usrnm_, wallet_, rfrr_, tkns[0], tkns[1], tkns[2]).buildTransaction({
#         'chainId': CHAIN_ID, 'nonce': nonce, 'gas': 1000000, 'gasPrice': 10000000000,
#     })
#     sign_tx = web3.eth.account.signTransaction(tx, PRIV_KEY)
#     tries = 0
#     while tries < 3:
#         tries += 1
#         try:
#             web3.eth.sendRawTransaction(sign_tx.rawTransaction)
#             return True
#         except ValueError:
#             time.sleep(5)
#     print(f"Register User Tickets Ref failed for {usrnm}, {wallet}, {rfrr}, {usrnm_}, {wallet_}, {rfrr_}, {tkns}")
#     f = open(FAILED_FILE, "a")
#     f.write(f"Register User Tickets Ref: {usrnm}, {wallet}, {rfrr}, {usrnm_}, {wallet_}, {rfrr_}, {tkns}\n")
#     f.close()
#     return False



def extract_transaction_info(txid):
    try:
        receipt = web3.eth.getTransaction(txid)
        if receipt is not None:
            value = int(receipt['input'][-64:], 16)
            to = Web3.toChecksumAddress('0x' + receipt['input'][10:-64][-40:])
            return {'id': txid, 'from': Web3.toChecksumAddress(receipt['from']), 'to': to, 'token_to': Web3.toChecksumAddress(receipt['to']), 'value': value}
        else:
            return {'id': txid, 'error': "Transaction not mined yet"}
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
    reply_text = f"به <b>بات کریستو لاتاری</b> خوش آمدید!\n"
    reply_text += f"کریستو یک لاتاری بر پایه اسمارت کانترکت اسد.\n"
    reply_text += f"شما می توانید با 10 USDT، 3 تیکت خریداری کنید. برای هر تیکت، شما 6 توکن از اعداد بین 1 تا 50 انتخاب می کنید. در زمان برگزاری لاتاری، با توجه به تعداد توکن های درست در هر تیکت، جایزه برنده خواهید شد.\n"
    reply_text += f"در کریستو لاتاری شما می توانید دوستان خود را دعوت کنید. اگر افرادی که دعوت می کنید در لاتاری برنده شوند، شما هم جایزه برنده خواهید شد. هر چه تعداد افراد بیشتری دعوت کنید، شانس برنده شدنتان در لاتاری بیشتر است.\n"
    reply_text += f"⚠️ همه تراکنش ها و کیف پول ها در شبکه BEP20 هستند"
    update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)
    reply_text = f"در زیر می توانید لیست مقادیر جایزه های لاتاری را مشاهده کنید:\n"
    reply_text += f"0️⃣ 0 USDT\n1️⃣ 0 USDT\n2️⃣ 10 USDT\n3️⃣ 50 USDT\n4️⃣ 200 USDT\n5️⃣ 10,000 USDT 💵\n6️⃣ 100,000 USDT 💰\n"
    reply_text += f"در زیر می توانید جایزه های دریافتی از طریق دعوت کردن دیگران را مشاهده کنید:\n"
    reply_text += f"0️⃣ 0 USDT\n1️⃣ 0 USDT\n2️⃣ 2 USDT\n3️⃣ 5 USDT\n4️⃣ 20 USDT\n5️⃣ 1,000 USDT 💵\n6️⃣ 5,000 USDT 💰"
    update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)
    reply_text = f"چه کار می خواهید انجام دهید؟"
    keyboard = [
        [InlineKeyboardButton("برنامه برگزاری لاتاری 📅", callback_data='schedule')],
        [InlineKeyboardButton("اطلاعات حساب کاربری 👤", callback_data='info')],
    ]
    if is_registration_open[0]:
        keyboard.append([InlineKeyboardButton("ثبت نام در لاتاری 📝", callback_data='register')])
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(reply_text, reply_markup=markup)
    


def message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    state = context.user_data['state']
    if context.user_data['username'] in ADMINS:
        if len(text.split(',')) == 6:
            for i in range(6):
                lott_tok[i] = int(text.split(',')[i])
            print(f"lotto tokens: {lott_tok}")
    if state > 100:
        tick = context.user_data['ticket']-1
        if check_token(text, context.user_data['token'][tick]) and len(context.user_data['token'][tick])<5:
            context.user_data['token'][tick].append(int(text))
            reply_text = f"توکن بعدی را انتخاب کنید:"
            markup = ReplyKeyboardMarkup(TOK_KEYBOARD)
            update.message.reply_text(reply_text, reply_markup=markup)
        elif check_token(text, context.user_data['token'][tick]) and len(context.user_data['token'][tick])==5:
            context.user_data['token'][tick].append(int(text))
            context.user_data['state'] = 7
            context.user_data['ticket'] = -1
            reply_text = f"تیکت انتخاب کنید:"
            keyboard = []
            for i in range(context.user_data['ticket_num']):
                if len(context.user_data['token'][i]) == 6:
                    keyboard.append([InlineKeyboardButton(f"تیکت {i+1} ✅", callback_data=f'ticket{i+1}')])
                else:
                    keyboard.append([InlineKeyboardButton(f"تیکت {i+1}", callback_data=f'ticket{i+1}')])
            if tokens_complete(context.user_data['token'], context.user_data['ticket_num']):
                keyboard.append([InlineKeyboardButton("مرحله پرداخت 💵", callback_data='proceed')])
            keyboard.append([InlineKeyboardButton("بازگشت 🔙", callback_data='back')])
            markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(reply_text, reply_markup=markup)
        elif not check_token(text, context.user_data['token'][tick]):
            reply_text = f"توکن اشتباه ❌\nدوباره انتخاب کنید:"
            markup = ReplyKeyboardMarkup(TOK_KEYBOARD)
            update.message.reply_text(reply_text, reply_markup=markup)
    elif state == 8:
        context.user_data['wallet'] = text
        context.user_data['state'] = 7
        if user_exists_lotto(context.user_data['username']):
            all_users[context.user_data['username']][0] = context.user_data['wallet']
            all_users[context.user_data['username']][1] = context.user_data['ref']
        else:
            all_users[context.user_data['username']] = [context.user_data['wallet'], context.user_data['ref'], 0]
        reply_text = f"شما می توانید تیکت بخرید یا دیگران را برای شرکت در لاتاری دعوت کنید\n"
        reply_text += f"اگر شخصی که دعوت کرده اید در لاتاری برنده شود، شما هم جایزه دریافت خواهید کرد\n"
        reply_text += f"لینک دعوت شخصی شما\n"
        reply_text += f"<a href=\"https://t.me/CrystoLotteryBot?start={context.user_data['username']}\">بات کریستو لاتاری</a> "
        update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)
        context.user_data['ticket_num'] = 3
        context.user_data['token'] = [[] for _ in range(context.user_data['ticket_num'])]
        reply_text = f"تیکت انتخاب کنید:"
        keyboard = []
        for i in range(int(context.user_data['ticket_num'])):
            keyboard.append([InlineKeyboardButton(f"تیکت {i+1}", callback_data=f'ticket{i+1}')])
        if tokens_complete(context.user_data['token'], context.user_data['ticket_num']):
            keyboard.append([InlineKeyboardButton("مرحله پرداخت 💵", callback_data='proceed')])
        keyboard.append([InlineKeyboardButton("بازگشت 🔙", callback_data='back')])
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(reply_text, reply_markup=markup)
    elif state == 9:
        context.user_data['txid'] = text
        context.user_data['state'] = 10
        reply_text = f"بعد از ارسال موفقیت آمیز تراکنش، بر روی دکمه ی بررسی تراکنش کلیک کنید"
        keyboard = [
            [InlineKeyboardButton("بررسی تراکنش ⚙️", callback_data='check')],
            [InlineKeyboardButton("بازگشت 🔙", callback_data='back')],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(reply_text, reply_markup=markup, parse_mode=ParseMode.HTML)




def buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    state = context.user_data['state']
    query.answer()
    if query.data == 'schedule' and state == 0:
        reply_text = f"لاتاری پس از ثبت نام 100 نفر برگزار خواهد شد"
        keyboard = [
            [InlineKeyboardButton("برنامه برگزاری لاتاری 📅", callback_data='schedule')],
            [InlineKeyboardButton("اطلاعات حساب کاربری 👤", callback_data='info')],
        ]
        if is_registration_open[0]:
            keyboard.append([InlineKeyboardButton("ثبت نام در لاتاری 📝", callback_data='register')])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'register' and state == 0 and is_registration_open[0]:
        context.user_data['state'] = 8
        reply_text = f"آدرس کیف پول خود را بفرستید 💰"
        keyboard = [[InlineKeyboardButton("بازگشت 🔙", callback_data='back')]]
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data.startswith('ticket') and state == 7:
        context.user_data['ticket'] = int(query.data[6:])
        context.user_data['state'] = 100 + context.user_data['ticket']
        context.user_data['token'][context.user_data['ticket']-1] = []
        reply_text = f"تیکت {context.user_data['ticket']}\nتوکن انتخاب کنید:"
        markup = ReplyKeyboardMarkup(TOK_KEYBOARD)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == "proceed" and state == 7:
        context.user_data['state'] = 9
        reply_text = f"10 USDT به این کیف پول واریز کنید:\n"
        reply_text += f"<code>{CONTRACT_ADDRESS}</code>\n"
        reply_text += f"شناسه تراکنش یا hash id را ارسال کنید:"
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup, parse_mode=ParseMode.HTML)
    elif query.data == "check" and state == 10:
        tx_info = extract_transaction_info(context.user_data['txid'])
        if 'error' not in tx_info.keys():
            if tx_info['value'] >= 10000000000000000000 and tx_info['token_to'] == USDT_CONTRACT: # 10 USDT
                if tx_info['to'] == CONTRACT_ADDRESS:
                    if not tx_info['id'] in all_txid:
                        # send_message(ADMINS[0], 0)
                        f = open(TX_FILE, "a")
                        f.write(f"{tx_info['id']}\n")
                        f.close()
                        if not user_exists_lotto(context.user_data['username']):
                            # res = register_user_tickets(context.user_data['username'], context.user_data['wallet'], context.user_data['ref'], context.user_data['token'])
                            all_users[context.user_data['username']] = [context.user_data['wallet'], context.user_data['ref'], 0]
                            if context.user_data['username'] in all_tickets.keys():
                                all_tickets[context.user_data['username']].append([context.user_data['token'][0], 0])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][1], 0])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][2], 0])
                            else:
                                all_tickets[context.user_data['username']] = [[context.user_data['token'][0], 0]]
                                all_tickets[context.user_data['username']].append([context.user_data['token'][1], 0])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][2], 0])
                        else:
                            # res = register_tickets(context.user_data['username'], context.user_data['token'])
                            if not context.user_data['username'] in all_users.keys():
                                all_users[context.user_data['username']] = [context.user_data['wallet'], context.user_data['ref'], 0]
                            if context.user_data['username'] in all_tickets.keys():
                                all_tickets[context.user_data['username']].append([context.user_data['token'][0], 0])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][1], 0])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][2], 0])
                            else:
                                all_tickets[context.user_data['username']] = [[context.user_data['token'][0], 0]]
                                all_tickets[context.user_data['username']].append([context.user_data['token'][1], 0])
                                all_tickets[context.user_data['username']].append([context.user_data['token'][2], 0])
                            all_txid.append(tx_info['id'])
                        context.user_data['state'] = 6
                        reply_text = f"اطلاعات حساب کاربری 📊\n"
                        if context.user_data['username'] in all_tickets.keys():
                            for i in range(len(all_tickets[context.user_data['username']])):
                                reply_text += f"تیکت {i+1}: {all_tickets[context.user_data['username']][i][0]}\n"
                        else:
                            reply_text += f"تیکت: ندارید\n"
                        if context.user_data['ref'] != "":
                            reply_text += f"شناسه معرف: {context.user_data['ref']}\n"
                        else:
                            reply_text += f"شناسه معرف: ندارید\n"
                        reply_text += f"تعداد افراد دعوت شده : {num_referred_lotto(context.user_data['username'])}\n"
                        keyboard = [[InlineKeyboardButton('بازشگت 🔙', callback_data='back')]]
                        markup = InlineKeyboardMarkup(keyboard)
                        query.message.reply_text(reply_text, reply_markup=markup)
                    else:
                        reply_text = f"این تراکنش قبلا استفاده شده است ❌"
                        keyboard = [[InlineKeyboardButton("بازگشت 🔙", callback_data='back')]]
                        markup = InlineKeyboardMarkup(keyboard)
                        query.message.reply_text(reply_text, reply_markup=markup)
                else:
                    reply_text = f"تراکنش به کیف پول اشتباه واریز شده است"
                    keyboard = [[InlineKeyboardButton("بازگشت 🔙", callback_data='back')]]
                    markup = InlineKeyboardMarkup(keyboard)
                    query.message.reply_text(reply_text, reply_markup=markup, parse_mode=ParseMode.HTML)
            else:
                reply_text = f"مبلغ ارسالی درست نیست"
                keyboard = [[InlineKeyboardButton("بازگشت 🔙", callback_data='back')]]
                markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text(reply_text, reply_markup=markup)
        else:
            reply_text = f"تراکنش ثبت نشده است ❌\nلطفا بررسی کنید و دوباره تلاش کنید"
            keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
            markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 7:
        context.user_data['state'] = 8
        reply_text = f"آدرس کیف پول خوذ را بفرستید 💰"
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 8:
        context.user_data['state'] = 0
        reply_text = f"چه کار می خواهید انجام دهید؟"
        keyboard = [
            [InlineKeyboardButton("برنامه برگزاری لاتاری 📅", callback_data='schedule')],
            [InlineKeyboardButton("اطلاعات حساب کاربری 👤", callback_data='info')],
        ]
        if is_registration_open[0]:
            keyboard.append([InlineKeyboardButton("ثبت نام در لاتاری 📝", callback_data='register')])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 6:
        context.user_data['state'] = 0
        reply_text = f"چه کار می خواهید انجام دهید؟"
        keyboard = [
            [InlineKeyboardButton("برنامه برگزاری لاتاری 📅", callback_data='schedule')],
            [InlineKeyboardButton("اطلاعات حساب کاربری 👤", callback_data='info')],
        ]
        if is_registration_open[0]:
            keyboard.append([InlineKeyboardButton("ثبت نام در لاتاری 📝", callback_data='register')])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 9:
        context.user_data['state'] = 7
        reply_text = f"تیکت را انتخاب کنید:"
        keyboard = []
        for i in range(context.user_data['ticket_num']):
            if len(context.user_data['token'][i]) == 6:
                keyboard.append([InlineKeyboardButton(f"تیکت {i+1} ✅", callback_data=f'ticket{i+1}')])
            else:
                keyboard.append([InlineKeyboardButton(f"تیکت {i+1}", callback_data=f'ticket{i+1}')])
        if tokens_complete(context.user_data['token'], context.user_data['ticket_num']):
            keyboard.append([InlineKeyboardButton("مرحله پرداخت 💵", callback_data='proceed')])
        keyboard.append([InlineKeyboardButton("بازگشت 🔙", callback_data='back')])
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup)
    elif query.data == 'back' and state == 10:
        context.user_data['state'] = 9
        reply_text = f"10 USDT به این کیف پول واریز کنید:\n"
        reply_text += f"<code>{CONTRACT_ADDRESS}</code>\n"
        reply_text += f"شناسه تراکنش یا hash id را ارسال کنید:"
        keyboard = [[InlineKeyboardButton("Back 🔙", callback_data='back')]]
        markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(reply_text, reply_markup=markup, parse_mode=ParseMode.HTML)
    elif query.data == 'info' and state == 0:
        if user_exists_lotto(context.user_data['username']):
            context.user_data['state'] = 6
            reply_text = f"اطلاعات حساب کاربری 📊\n"
            if context.user_data['username'] in all_tickets.keys():
                for i in range(len(all_tickets[context.user_data['username']])):
                    reply_text += f"تیکت {i+1}: {all_tickets[context.user_data['username']][i][0]}\n"
            else:
                reply_text += f"تیکت: ندارید\n"
            if context.user_data['ref'] != "":
                reply_text += f"شناسه معرف: {context.user_data['ref']}\n"
            else:
                reply_text += f"شناسه معرف: ندارید\n"
            reply_text += f"تعداد افراد دعوت شده : {num_referred_lotto(context.user_data['username'])}\n"
            keyboard = [[InlineKeyboardButton('بازگشت 🔙', callback_data='back')]]
            markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(reply_text, reply_markup=markup)
        else:
            reply_text = f"شما ثبت نام نکرده اید\n"
            reply_text += f"چه کاری می خواهید انجام دهید؟"
            keyboard = [
                [InlineKeyboardButton("برنامه برگزاری لاتاری 📅", callback_data='schedule')],
                [InlineKeyboardButton("اطلاعات حساب کاربری 👤", callback_data='info')],
            ]
            if is_registration_open[0]:
                keyboard.append([InlineKeyboardButton("ثبت نام در لاتاری 📝", callback_data='register')])
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



def score_token(tok1, tok2):
    score = 0
    for i in range(6):
        for j in range(6):
            if tok1[i] == tok2[j]:
                score += 1
    return score



def find_winners(update: Update, context: CallbackContext) -> None:
    if context.user_data['username'] in ADMINS:
        all_winners = {}
        for k, v in all_tickets.items():
            for tick in v:
                score = score_token(tick[:6], lott_tok)
                if score > 1:
                    if k in all_winners.keys():
                        all_winners[k] += PRIZE_WIN[score]
                    else:
                        all_winners[k] = PRIZE_WIN[score]
                    if user_exists_lotto(k) and all_users[k][1] != "" and user_exists_lotto(all_users[k][1]):
                        if all_users[k][1] in all_winners.keys():
                            all_winners[all_users[k][1]] += PRIZE_REF[score]
                        else:
                            all_winners[all_users[k][1]] = PRIZE_REF[score]
        f = open(WINNERS_FILE, "w")
        f.write(json.dumps(all_winners))
        f.close()



def send_message_winners(update: Update, context: CallbackContext) -> None:
    if context.user_data['username'] in ADMINS:
        f = open(WINNERS_FILE, "r")
        all_winners = json.load(f)
        f.close()
        for k, v in all_winners.items():
            text = f"تبریک! شما برنده لاتاری شدید 🎉🎉\nمبلغ "
            text += f"{v} "
            text += f"به کیف پول شما واریز شده است 💵💸"
            send_text = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={k}&text={text}"
            requests.get(send_text)



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

web3 = Web3(Web3.HTTPProvider(BSC))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

is_registration_open = [True]
lott_tok = [1, 2, 3, 4, 5, 6]
all_txid = []
all_users = {}
all_tickets = {}
# all_winners = {}
PRIZE_WIN = [0, 0, 10, 50, 200, 10000, 100000]
PRIZE_REF = [0, 0, 2, 5, 20, 1000, 5000]


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
updater.dispatcher.add_handler(CommandHandler('recorddata', record_data))
updater.dispatcher.add_handler(CommandHandler('changeregistrationstatus', change_registration_status))
updater.dispatcher.add_handler(CommandHandler('findwinners', find_winners))
updater.dispatcher.add_handler(CommandHandler('sendmessagewinners', send_message_winners))
updater.dispatcher.add_handler(MessageHandler(~Filters.command, message))
updater.dispatcher.add_handler(CallbackQueryHandler(buttons))
updater.start_polling()
updater.idle()