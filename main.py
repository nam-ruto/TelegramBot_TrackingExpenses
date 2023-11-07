"""
Project name: Telegram Bot For Tracking Expenses
Developer: Hoang Duc Nam (github/nam-ruto)

Usage:
Deploy a Telegram bot for tracking expenses
/new: to create new record
/add: to add expenses
/add + amoun: to add expenses and that amount
/total: to show the current total amount of expenses
/note: to take note
/cancel: to cancel the action
"""
import datetime, logging, gspread, telegram

from typing import Final
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InputMediaAnimation, Bot
from telegram.ext import (
	Application, CommandHandler, ContextTypes, 
	ConversationHandler, MessageHandler, filters, CallbackContext
)
# ------------------- TELEGRAM BOT TOKEN ---------------------- #
TOKEN = Final = "YOUR_BOT_TOKEN"
BOT_USERNAME = "@BOT_USERNAME"

# ------------------- Enable logging ------------------------- #
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
""" set higher logging level for httpx to avoid all GET and POST requests being logged """
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# ------------------- Global variable ------------------------- #
sheet = None
lenOfData = None
gs_url = None
""" Increment variables: Increasing when data is added to table """
iCell = Dcell = Ecell = Fcell = 1

# --------------- Get URL Google Sheets ----------------------- #
EMAIL = range(0)
async def acquireURL(update: Update, context: ContextTypes.DEFAULT_TYPE):
	print("URL acquire")
	await update.message.reply_text("\U0001F44B <b>Welcome to Tracking Expenses bot!</b>\n\n"
								 "\U0001F449 Firstly, you must have a Google Sheets spread for recording and tracking your expenses.\n\n"
								 "\U0001F449 Please provide me a <b>Google Sheets URL</b> that I can record the data on it.\n\n"
								 "\U0001F449 <u>You should</u>: \n\n"
								 "1. Create a new spreadsheet\n\n"
								 "2. Change access status: Private \U00002192 <b>Anyone with the link: editor</b>\n\n"
								 "3. Copy URL\n\n"
								 "4. Paste to the Telegram with this syntax: /url <i>your_url</i>", parse_mode="HTML")
	return EMAIL

async def url(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global sheet, lenOfData, gs_url
	print("URL success")

	# Get url
	gs_url = context.args[0]
	file = gspread.service_account("./.config/gspread/service_account.json")
	workbook = file.open_by_url(gs_url)
	sheet = workbook.sheet1

	# Set up sheetspread
	sheet.update(values=[["No", "Date and Time", "User", "Expense for", "Amount", "Note"]], range_name="A2:F2")
	sheet.update('E34', '=SUM(E3:E33)', raw=False)
	sheet.format('A2:F2', {'horizontalAlignment': "CENTER", 'textFormat': {'bold': True}})
	lenOfData = len(sheet.col_values(4))

	print("Set up success")

	# Reply
	await update.message.reply_text("<b>Successfully!</b> Your spread is accepted, now you can start tracking your expenses!\n\n"
								 "\U0001F449 Type /new to start a new expense\n\n"
								 "\U0001F449 Type /total to show your current amount of expenses\n\n"
								 "\U0001F449 Type /show to get the spreadsheets\n\n", parse_mode="HTML")
	return ConversationHandler.END


# ------------------------- Get Time -------------------------- #
def get_time():
	current_time = datetime.datetime.now()
	formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
	return formatted_time

# ---------------------- Main Conversation -------------------- #

# Set up Conversation order
ADD, EXPENSES, AMOUNT, NOTE = range(4)

# ADD - EXPENSES - AMOUNT - NOTEs
async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global sheet
	if sheet is not None:
		# get time
		time_record = get_time()
		print(time_record)

		# Log infor
		teleUserName = update.message.from_user
		logger.info("%s have start new record", teleUserName.first_name)

		# Write data to Google Sheets
		global iCell
		Bcell_position = 'B' + str(lenOfData + iCell)
		Ccell_position = 'C' + str(lenOfData + iCell)
		sheet.update(values=[[time_record]], range_name=Bcell_position)
		sheet.update(values=[[teleUserName.first_name]], range_name=Ccell_position)
		iCell += 1

		# Bot reply
		await update.message.reply_text("Hi! I am Monkey Bot. I am bot assistant in Tracking Expenses!\n\n"
									"\U0001F449 Type /add to add new expense\n\n"
									"\U0001F449 Type /add + <i>title</i> to add new expense and its title", parse_mode="HTML")
		return ADD
	else:
		await update.message.reply_text("\U000026A0 You have to provide the URL first")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global sheet
	if sheet is not None:
		# Log infor
		teleUserName = update.message.from_user
		logger.info("%s add new expense", teleUserName.first_name)

		# Checking input
		if(len(context.args) == 0):
			# Bot reply
			await update.message.reply_text("Input name of expense: ")
			return EXPENSES
		else:
			global Dcell
			ExpenseName = ' '.join(context.args)
			# Write data to Google Sheets
			Dcell_position = 'D' + str(lenOfData + Dcell)
			sheet.update(values=[[ExpenseName]], range_name=Dcell_position)
			Dcell += 1

			# Bot reply
			await update.message.reply_text("Input amount of expense:")
			return AMOUNT
	else:
		await update.message.reply_text("\U000026A0 You have to provide the URL first")
	
async def expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global sheet
	if sheet is not None:
		# Log infor
		teleUserName = update.message.from_user
		logger.info("%s add new expense(input title)", teleUserName.first_name)

		# Write data to Google Sheets
		global Dcell
		ExpenseName = update.message.text
		Dcell_position = 'D' + str(lenOfData + Dcell)
		sheet.update(values=[[ExpenseName]], range_name=Dcell_position)
		Dcell += 1

		# Bot reply
		await update.message.reply_text("Enter amount of expense: ")
		return AMOUNT
	else:
		await update.message.reply_text("\U000026A0 You have to provide the URL first")

async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global sheet
	if sheet is not None:
		# Log infor
		teleUserName = update.message.from_user
		logger.info("%s add amount of expense", teleUserName.first_name)

		# Write data to Google Sheets
		global Ecell
		AmountExpense = update.message.text
		Ecell_position = 'E' + str(lenOfData + Ecell)
		sheet.update(values=[[int(AmountExpense)]], range_name=Ecell_position)
		Ecell += 1

		# Bot reply
		await update.message.reply_text("Your expense has been recorded <b>successfully!</b>\n\n"
									"\U0001F449 Type /note + <i>title</i> if you want to note something\n"
									"\U0001F449 Type /exit to save and close the recording", parse_mode="HTML")
		return NOTE
	else:
		await update.message.reply_text("\U000026A0 You have to provide the URL first")

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global sheet
	if sheet is not None:
		# Log infor
		teleUserName = update.message.from_user
		logger.info("%s take note", teleUserName.first_name)

		# Write data to Google Sheets
		global Fcell
		NoteDesc = ' '.join(context.args)
		Fcell_position = 'F' + str(lenOfData + Fcell)
		sheet.update(values=[[NoteDesc]], range_name=Fcell_position)
		Fcell += 1

		# Bot reply
		await update.message.reply_text("Take note successfully! Recording ended, see you later")
		return ConversationHandler.END
	else:
		await update.message.reply_text("\U000026A0 You have to provide the URL first")

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
	# Log infor
	teleUserName = update.message.from_user
	logger.info("%s has exited the recording", teleUserName.first_name)
	# Bot reply
	await update.message.reply_text("Expense has been recoreded. Recording ended, see you later!")
	return ConversationHandler.END

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global sheet
	if sheet is not None:
		# Log infor
		teleUserName = update.message.from_user
		logger.info("%s check total amount of expenses", teleUserName.first_name)
		totalAmount = sheet.acell('E34').value
		await update.message.reply_text(f"\U0001F4B0 <b>Current Total Amount Of Expenses</b>: {totalAmount}.", parse_mode="HTML")
	else:
		await update.message.reply_text("\U000026A0 You have to provide the URL first")

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
	global sheet, gs_url
	if sheet is not None:
		await update.message.reply_text(f"\U0001F412 <b>Here's your record:</b> <a href='{gs_url}'>Tracking Expenses</a>", parse_mode="HTML")
	else:
		await update.message.reply_text("\U000026A0 You have to provide the URL first")


# ---------------------- Main function -------------------- #
def main():
	# Check for running
	print("Starting...")

	# Create the Application and pass it to bot's token
	app = Application.builder().token(TOKEN).build()

	# Acquire email conversation
	emailConversation = ConversationHandler(
		entry_points=[CommandHandler("start", acquireURL)],
		states={EMAIL:[CommandHandler("url", url)]},
		fallbacks=[]
	)	

	# Add conversation handler with the states ADD, EXPENSES, AMOUNT
	mainConversation = ConversationHandler(
		entry_points=[CommandHandler("new", new)],
		states={
			# ADD: [MessageHandler(filters.TEXT, add)],
			ADD: [CommandHandler("add", add)],
			EXPENSES: [MessageHandler(filters.TEXT, expenses)],
			AMOUNT: [MessageHandler(filters.TEXT, amount)],
			NOTE: [CommandHandler("note", note)],
		},
		fallbacks=[CommandHandler("exit", exit)]
	)

	app.add_handler(emailConversation)
	app.add_handler(mainConversation)
	app.add_handler(CommandHandler("total", total))
	app.add_handler(CommandHandler("show", show))

	# Check polling
	print("Polling...")

	# Run the bot until press Ctrl + C
	app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
	main()