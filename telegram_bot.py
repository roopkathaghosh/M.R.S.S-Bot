import logging
import os
import openai
import nltk
from nltk.tokenize import word_tokenize
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load API Keys from .env File
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("6641841590:AAGqKdLMXWofmbMPD8WF2tKsk9IPojdwePs")
OPENAI_API_KEY = os.getenv("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")

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Download NLTK Data
nltk.download("punkt")

# Set Up Logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to Generate Response from ChatGPT API
def get_chatgpt_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[{"role": "user", "content": question}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Error fetching response: {e}")
        return "Sorry, something went wrong. Please try again later."

# Command: Start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am your AI-powered assistant. Ask me anything!")

# Message Handler
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    tokenized_message = word_tokenize(user_message.lower())  # Tokenize input using NLTK
    
    if any(word in tokenized_message for word in ["hello", "hi", "hey"]):
        response = "Hello! How can I assist you today?"
    else:
        response = get_chatgpt_response(user_message)  # Get response from ChatGPT API

    await update.message.reply_text(response)

# Main Function to Start the Bot
def main():
    if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
        logger.error("Missing API keys. Please check your .env file.")
        return

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start Bot
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()