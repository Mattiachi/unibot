#!/usr/bin/env python3

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def makeKeyboard(args):
    buttons = []
    for i in range(0,len(args),2):
        buttons.append([InlineKeyboardButton(text= args[i], callback_data= args[i+1])])
#    print(buttons)
    return InlineKeyboardMarkup(inline_keyboard= buttons)


