from io import BytesIO
import logging
import os
from telegram import InputFile, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from code_validation import CodeValidation

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Даров! Чекаю від тебе файл.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="ФАЙЛ ПЛіЗ 0_0")

async def checkProductsFile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(update.message.document is None):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Мені потрібен документ.")
        return
    if(update.message.document["mime_type"] != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Це документ, але не того формату. Мені потрібен файл з розшмренням (xlsx)")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Уан моменто!")
    productsDownloader = await context.bot.get_file(update.message.document['file_id'])
    products = BytesIO()
    await productsDownloader.download_to_memory(products)
    codeValidation = CodeValidation(products)
    try:
        validationResult = codeValidation.ValidateProducts()
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=e)
        return
    await context.bot.send_document(chat_id=update.effective_chat.id, document=validationResult, filename="validation_result_" + update.message.document.file_name.replace(".","_") + ".txt")

if __name__ == '__main__':
    try:
        value = os.getenv("TELEGRAM_BOT_KEY")
        if(value is None):
            raise KeyError("Env TELEGRAM_BOT_KEY was not found")
    except KeyError as e:
        print(e)
        raise e
    application = ApplicationBuilder().token(value).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    echo_handler = MessageHandler(filters.ATTACHMENT, checkProductsFile)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()