import logging
import os
from AI_INTERACTION import *
import json
from CAESER_SHIFT import *
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

openAiKey = os.getenv("OPEN_AI_KEY")
AI = AI_INTERACTION(str(openAiKey))
caeserShift = CAESER_SHIFT()

logging.basicConfig(filename='logs.log', encoding='utf-8',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

KEEP,KEEP_INPUT,SECRET_INPUT,SECRET_NOTE,SECRET_PASSWORD,NOTE_CONTENTS,NOTE_INPUT,LIST_CONTENTS,LIST_INPUT = range(9)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    logging.info(f'{update.message.from_user.username} started bot.')
    user = update.effective_user
    await update.message.reply_text("Welcome to Keepnote 😃 Keepnote is a service for creating notes, fun interactive lists, and secret notes that aren't stored in plain text! All commands support text, audio or images as input meaning you don't have to type up your notes! To get started; use /note to create a new note, /list to create a new interactive list, or /secret to create a note locked with a 4 digit pin.")


async def keep(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Enter the note you want to keep", reply_markup=ForceReply())
    return KEEP_INPUT

async def noteTitle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Enter the title for your note", reply_markup=ForceReply())
    return NOTE_CONTENTS

async def listTitle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Enter the title for your list", reply_markup=ForceReply())
    return LIST_CONTENTS

async def listContents(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Enter the contents of your list", reply_markup=ForceReply())
    context.user_data['listTitle'] = update.message.text
    return LIST_INPUT

async def noteContents(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Enter the contents of your note", reply_markup=ForceReply())
    context.user_data['noteTitle'] = update.message.text
    return NOTE_INPUT

async def noteInput(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    noteTitle = context.user_data.get('noteTitle')

    try:
        messageText = ""
        if update.message.voice != None:
            voice_file = await update.message.voice.get_file()
            location = f"voice.{update.message.voice.mime_type.split('/')[1]}"
            await voice_file.download_to_drive(f"{location}")
            messageText = AI.audioToText(location)
        if update.message.audio != None:
            audio_file = await update.message.audio.get_file()
            location = f"audio.{update.message.audio.mime_type.split('/')[1]}"
            await audio_file.download_to_drive(f"{location}")
            messageText = AI.audioToText(location)
        if update.message.document != None:
            if update.message.document.mime_type.split('/')[0] == 'audio':
                audio_file = await update.message.document.get_file()
                location = f"audio.{update.message.document.mime_type.split('/')[1]}"
                await audio_file.download_to_drive(f"{location}")
                messageText = AI.audioToText(location)
            elif update.message.document.mime_type.split('/')[0] == 'image':
                image_file = await update.message.document.get_file()
                messageText = AI.imageToText(image_file.file_path)
        if update.message.text != None:
            messageText = str(update.message.text)
        if update.message.photo != None and messageText == "":
            photo_file = await update.message.photo[-1].get_file()
            messageText = AI.imageToText(photo_file.file_path)
        await update.message.reply_text(f"""<b>{noteTitle}</b>
<i>{messageText} </i>""",parse_mode='html') 
    except:
        await update.message.reply_text("Something went wrong 😿 Please try again!", parse_mode='html') 
    
 
    return ConversationHandler.END


async def secretPassword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Enter a four digit pin for this note (Make sure to delete this from chat after)🔢", reply_markup=ForceReply())
    return SECRET_NOTE

async def keepSecret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.message.text) > 4 or len(update.message.text) < 4:
        await update.message.reply_text(f"Invalid pin! PIN must be four digits long. Type in anything and press enter to try again.")
        return SECRET_PASSWORD
    else:
        context.user_data['pin'] = update.message.text
    await update.message.reply_text(f"Enter the secret note you want to keep (Make sure to delete this from chat after)🤫", reply_markup=ForceReply())
    return SECRET_INPUT

async def secretInput(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    secretNotePin = context.user_data.get('pin')
    try:
        messageText = ""
        if update.message.voice != None:
            voice_file = await update.message.voice.get_file()
            location = f"voice.{update.message.voice.mime_type.split('/')[1]}"
            await voice_file.download_to_drive(f"{location}")
            messageText = AI.audioToText(location)
        if update.message.audio != None:
            audio_file = await update.message.audio.get_file()
            location = f"audio.{update.message.audio.mime_type.split('/')[1]}"
            await audio_file.download_to_drive(f"{location}")
            messageText = AI.audioToText(location)
        if update.message.document != None:
            if update.message.document.mime_type.split('/')[0] == 'audio':
                audio_file = await update.message.document.get_file()
                location = f"audio.{update.message.document.mime_type.split('/')[1]}"
                await audio_file.download_to_drive(f"{location}")
                messageText = AI.audioToText(location)
            elif update.message.document.mime_type.split('/')[0] == 'image':
                image_file = await update.message.document.get_file()
                messageText = AI.imageToText(image_file.file_path)
        if update.message.text != None:
            messageText = str(update.message.text)
        if update.message.photo != None and messageText == "":
            photo_file = await update.message.photo[-1].get_file()
            messageText = AI.imageToText(photo_file.file_path)
        if messageText != "":
            keyboard = [[InlineKeyboardButton("1️⃣",callback_data="0,0,1,pinInput"),InlineKeyboardButton("2️⃣",callback_data="0,1,2,pinInput"),InlineKeyboardButton("3️⃣",callback_data="0,2,3,pinInput")],
                        [InlineKeyboardButton("4️⃣",callback_data="1,0,4,pinInput"),InlineKeyboardButton("5️⃣",callback_data="1,1,5,pinInput"),InlineKeyboardButton("6️⃣",callback_data="1,2,6,pinInput")],
                        [InlineKeyboardButton("7️⃣",callback_data="2,0,7,pinInput"),InlineKeyboardButton("8️⃣",callback_data="2,1,8,pinInput"),InlineKeyboardButton("9️⃣",callback_data="2,2,9,pinInput")],
                        [InlineKeyboardButton("0️⃣",callback_data="3,0,0,pinInput")],
                        [InlineKeyboardButton("🔒",callback_data=f"4,0,🔒,pinInput,{secretNotePin},XXXX")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f"{caeserShift.encryptString(messageText)}", reply_markup=reply_markup) 
    except:
        await update.message.reply_text("Something went wrong 😿 Please try again!", parse_mode='html') 
 
    return ConversationHandler.END


async def listInput(update: Update, context: ContextTypes.DEFAULT_TYPE.bot_data) -> None:

    listTitle = context.user_data.get('listTitle')
    try:
        messageText = ""
        if update.message.voice != None:
            voice_file = await update.message.voice.get_file()
            location = f"voice.{update.message.voice.mime_type.split('/')[1]}"
            await voice_file.download_to_drive(f"{location}")
            messageText = AI.audioToText(location)
        if update.message.audio != None:
            audio_file = await update.message.audio.get_file()
            location = f"audio.{update.message.audio.mime_type.split('/')[1]}"
            await audio_file.download_to_drive(f"{location}")
            messageText = AI.audioToText(location)
        if update.message.document != None:
            if update.message.document.mime_type.split('/')[0] == 'audio':
                audio_file = await update.message.document.get_file()
                location = f"audio.{update.message.document.mime_type.split('/')[1]}"
                await audio_file.download_to_drive(f"{location}")
                messageText = AI.audioToText(location)
            elif update.message.document.mime_type.split('/')[0] == 'image':
                image_file = await update.message.document.get_file()
                messageText = AI.imageToText(image_file.file_path)
        if update.message.text != None:
            messageText = str(update.message.text)
        if update.message.photo != None and messageText == "":
            photo_file = await update.message.photo[-1].get_file()
            messageText = AI.imageToText(photo_file.file_path)
        jsonString = AI.textToNote(messageText)
        convertedDictionary = json.loads(str(jsonString))

        keyboard = [[]]
        j=0
        k=0
        for i in range(0,len(convertedDictionary["content"])):
            if (k > 0 and k % 3 == 0) or k > 0 and len(convertedDictionary["content"][i]) > 8:
                j += 1
                keyboard.append([])
                k = 0
            keyboard[j].append(InlineKeyboardButton(convertedDictionary["content"][i], callback_data=f"{j},{k},{convertedDictionary['content'][i][0]},checkBox"))
            k+=1
            if len(convertedDictionary["content"][i]) > 8:
                j += 1
                keyboard.append([])
                k = 0
        if keyboard[j] != []:
            keyboard.append([])
            k = 0
            j += 1
            keyboard[j].append(InlineKeyboardButton("🔄", callback_data=f"{j},{k},🔄,checkBox"))
        else:
            keyboard[j].append(InlineKeyboardButton("🔄", callback_data=f"{j},{k},🔄,checkBox"))
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f"<b>{listTitle}</b>", reply_markup=reply_markup, parse_mode='html') 
    except:
        await update.message.reply_text("Something went wrong 😿 Please try again!", parse_mode='html') 
    
 
    return ConversationHandler.END

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    if query.data.split(",")[3] == 'checkBox':
        

        keyboard = list(query.message.reply_markup.inline_keyboard)
        for i in range(0,len(keyboard)):
            keyboard[i] = list(keyboard[i])
            
        buttonPositionY = int(tuple(query.data.split(","))[0])
        buttonPositionX = int(tuple(query.data.split(","))[1])
            
        listOfText = list(keyboard[buttonPositionY][buttonPositionX].text)
        listOfText[0] = '✅'
        checkmarkText = "".join(listOfText)
            

        if query.data.split(",")[2][0] == '🔄':
            for i in range(0,len(keyboard)):
                for j in range(0,len(keyboard[i])):
                    listOfText = list(keyboard[i][j].text)
                    listOfText[0] = keyboard[i][j].callback_data.split(",")[2][0]
                    originalText = "".join(listOfText)
                    keyboard[i][j] = InlineKeyboardButton(originalText, callback_data=keyboard[i][j].callback_data)
        else:
            if keyboard[buttonPositionY][buttonPositionX].text[0] == '✅':
                listOfText = list(keyboard[buttonPositionY][buttonPositionX].text)
                listOfText[0] = keyboard[buttonPositionY][buttonPositionX].callback_data.split(",")[2][0]
                originalText = "".join(listOfText)
                keyboard[buttonPositionY][buttonPositionX] = InlineKeyboardButton(originalText, callback_data=query.data)
            else:
                keyboard[buttonPositionY][buttonPositionX] = InlineKeyboardButton(checkmarkText, callback_data=query.data)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"<b>{query.message.text}</b>", reply_markup=reply_markup, parse_mode='html')

    if query.data.split(",")[3] == 'pinInput':

        messageText = query.message.text

        keyboard = list(query.message.reply_markup.inline_keyboard)
        for i in range(0,len(keyboard)):
            keyboard[i] = list(keyboard[i])
        
        if keyboard[4][0].callback_data.split(",")[5].find('X') != -1 and query.data.split(",")[2] != "🔒" and query.data.split(",")[2] != "🔓":
            currentPinEntry = list(keyboard[4][0].callback_data.split(",")[5])
            currentPinEntry[keyboard[4][0].callback_data.split(",")[5].find('X')] = query.data.split(",")[2]
            currentPinEntry = "".join(currentPinEntry)
            lockButtonNewCallback = str(keyboard[4][0].callback_data)
            lockButtonNewCallback = list(lockButtonNewCallback.split(","))
            lockButtonNewCallback[5] = currentPinEntry
            lockButtonNewCallback = ",".join(lockButtonNewCallback)
            lockButton = InlineKeyboardButton('🔒',callback_data=lockButtonNewCallback)
            keyboard[4][0] = lockButton
        if keyboard[int(query.data.split(",")[0])][int(query.data.split(",")[1])].text == "🔒":
            if query.data.split(",")[5] == query.data.split(",")[4]:
                lockButton = InlineKeyboardButton('🔓',callback_data=query.data)
                keyboard[4][0] = lockButton
                messageText = caeserShift.decryptString(query.message.text)
            elif query.data.split(",")[5] != query.data.split(",")[4]:
                lockButtonNewCallback = str(keyboard[4][0].callback_data)
                lockButtonNewCallback = list(lockButtonNewCallback.split(","))
                lockButtonNewCallback[5] = 'XXXX'
                lockButtonNewCallback = ",".join(lockButtonNewCallback)
                lockButton = InlineKeyboardButton('🔒',callback_data=lockButtonNewCallback)
                keyboard[4][0] = lockButton
        elif keyboard[int(query.data.split(",")[0])][int(query.data.split(",")[1])].text == "🔓":
            lockButtonNewCallback = str(keyboard[4][0].callback_data)
            lockButtonNewCallback = list(lockButtonNewCallback.split(","))
            lockButtonNewCallback[5] = 'XXXX'
            lockButtonNewCallback = ",".join(lockButtonNewCallback)
            lockButton = InlineKeyboardButton('🔒',callback_data=lockButtonNewCallback)
            keyboard[4][0] = lockButton
            messageText = caeserShift.encryptString(query.message.text)
        elif keyboard[4][0].callback_data.split(",")[5] != keyboard[4][0].callback_data.split(",")[4] and keyboard[4][0].callback_data.split(",")[5].find('X') == -1:
            lockButtonNewCallback = str(keyboard[4][0].callback_data)
            lockButtonNewCallback = list(lockButtonNewCallback.split(","))
            lockButtonNewCallback[5] = 'XXXX'
            lockButtonNewCallback = ",".join(lockButtonNewCallback)
            lockButton = InlineKeyboardButton('🔒',callback_data=lockButtonNewCallback)
            keyboard[4][0] = lockButton

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"{messageText}", reply_markup=reply_markup)
        

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day."
    )

    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(str(os.getenv("TELEGRAM_KEY"))).build()

    startHandler = CommandHandler("start", start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("list", listTitle),CommandHandler("secret", secretPassword),CommandHandler("note", noteTitle)],
        states={
            LIST_CONTENTS: [MessageHandler(filters.ALL, listContents)],
            LIST_INPUT: [MessageHandler(filters.ALL, listInput)],
            SECRET_INPUT: [MessageHandler(filters.ALL, secretInput)],
            SECRET_NOTE: [MessageHandler(filters.ALL, keepSecret)],
            SECRET_PASSWORD: [MessageHandler(filters.ALL, secretPassword)],
            NOTE_CONTENTS: [MessageHandler(filters.ALL, noteContents)],
            NOTE_INPUT: [MessageHandler(filters.ALL, noteInput)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(startHandler)
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()