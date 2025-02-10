import os
import random
import telebot
import logging
from pathlib import Path
import dropbox
from dropbox.exceptions import ApiError
import tempfile
import time

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get tokens from environment variables
TOKEN = os.getenv('BOT_TOKEN', '7915411303:AAGGE1SorQqU1__FqMU7UezeyTF-MZgC_m0')
DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN', 'sl.u.AFj5xAejHUraFnrNd992xWDLLG0gsckdktdptYmCaQELDhBrp0BqyzOX7WV_vm5hjf2HHTHutUhyBB1Q9hY3Wt4O7Bw6O--7SeidSLj2kb0ytQg1Ur0CtUkLuyJlCTRmcYFUcbcotuS0NW46fGh3ht-0a6JdnCbmwXWv-JbMnPggH5qapBpDqx2tIDstR5uZXuMzm6xae9ec9LKuCYYuLkKFC4CiXytKDNafqS6ab09iLQXdSLuGuwi10Z-NzpUhb_9EIlbeRs9-oBwjs4o18-eJhFxlgenxtTE4eskCwDfrFfaPSqNzt65iMrjjh2jLJPolRJKqjbiFSqWBlwRt5ipp5FrjfGe-T-WClDr10PfRqsRdyAwHseeqjLKNZDGRqmtbVdoRe3AeBgvKpGaimu9T2043Ygv1f9dYi7pVjHDqw_VwEGxR-cBZzC-l95yADEJsk5pLruA4JNvTEihz1UDEJARQ1Zn17cII-vQp9WkTYDVZvk1afG-w7plrJ-v55Ktgmmgzw8UEvJn0sOrfDTOSG12tAvZaCS0z50jUnwVVQrJwB02lXVVVZN9qs7Om6qOp18oJdjqx-4Kz8ktQzM5sGcEO7-T_wt_NPC1fTy9VJwGQNmuRS5svN3tGKZstvNjiAqi-6CO1Qe1PHJu_2VFlUoLkDdsP0Vp3sQp7pB_xWERiNdcFcA3qtSY0hsr5MDJ3T7cfKCf8HHlxRTD21zI2EOtmTunqAH9bdp73MYkKmiTgzFDKTbOttP3TdRg_CcuJc0r8qVvIig1gscnbHRzdry6b09RGk86iY-2KackGbKNabJ7baESSaI1HGUD1pF2O7WSP89MqEJ5YY02cCNQJXRy1gXgfZA8M4C9jrxGMPVOpl1S7YGE6HshmC9MpWhwKF5QIj3ZqBJ1Q5BAchECadJG_ROEDpb9JP74nGWknKmS1W9nMJpeT1iN36akB3EuoW92aDuMLydQtKqcX7ButjaUdD1HvWQFyZsbiLNnScOYIxxBEnTWwXRuGuvvR_aZGM-oPnxouJT28BFyfBIMX4cmfj7uV5dms5p4L5ajN8bYMgvHmn4kNLc-IZMjuDRVXtdsOxGM-9wZ0nEw1RXctBG5P_jxNUhol_oqDRejyAHnaaTyF1DubWCaMQUiRq-LFLrc_Vi5FD0BVpa-DsrH-Hisil7zqqQwixyrJkhmu-MwqZYIgZQ-juLr_Y7KY8F9QSN0uW9YtsE5bG88VyK2wJPlPgxNVatVdBGnWRSfTDw')
DROPBOX_FOLDER = '/Mobile Uploads/d3aa'  # Change this to your Dropbox folder path
ADMIN_CHAT_ID = 123456789  # Replace with your admin chat ID

# Initialize bot and Dropbox
bot = telebot.TeleBot(TOKEN)
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

def get_random_image():
    try:
        logger.info(f"Attempting to list files in Dropbox folder: {DROPBOX_FOLDER}")
        # List all files in the Dropbox folder
        result = dbx.files_list_folder(DROPBOX_FOLDER)
        logger.info("Successfully listed Dropbox folder")
        
        files = [entry.path_lower for entry in result.entries if entry.path_lower.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        logger.info(f"Found {len(files)} image files: {files}")
        
        if not files:
            logger.warning(f"No image files found in {DROPBOX_FOLDER}")
            return None
            
        # Select a random image
        random_image = random.choice(files)
        logger.info(f"Selected random image: {random_image}")
        
        # Create a temporary file to store the image
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(random_image)[1]) as temp_file:
            # Download the file to the temporary location
            logger.info(f"Downloading image: {random_image}")
            metadata, response = dbx.files_download(random_image)
            temp_file.write(response.content)
            logger.info(f"Image downloaded to: {temp_file.name}")
            return temp_file.name
            
    except ApiError as e:
        logger.error(f"Dropbox API error: {e}")
        if isinstance(e.error, dropbox.files.ListFolderError):
            logger.error(f"Error listing folder. Make sure the folder path '{DROPBOX_FOLDER}' is correct")
        return None
    except Exception as e:
        logger.error(f"Error getting random image: {e}")
        return None

def read_texts():
    try:
        file_path = Path('txt')
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        logger.error(f"Error reading texts file: {e}")
        return []

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.reply_to(message, 
            "مرحباً بك! 👋\n\n"
            "استخدم الأمر /random للحصول على نص عشوائي\n"
            "استخدم الأمر /image للحصول على صورة عشوائية\n"
            "استخدم الأمر /list_folders للاطلاع على المجلدات المتاحة\n"
            "استخدم الأمر /test_dropbox للتحقق من اتصال دروبوكس"
        )
        logger.info(f"User {message.from_user.id} started the bot")
    except Exception as e:
        logger.error(f"Error in start command: {e}")

@bot.message_handler(commands=['random'])
def random_text(message):
    try:
        texts = read_texts()
        if texts:
            text = random.choice(texts)
            bot.reply_to(message, text)
            logger.info(f"Sent random text to user {message.from_user.id}")
        else:
            bot.reply_to(message, "لا توجد نصوص متوفرة حالياً")
            logger.warning("No texts available")
    except Exception as e:
        bot.reply_to(message, "حدث خطأ في قراءة النصوص")
        logger.error(f"Error in random command: {e}")

@bot.message_handler(commands=['image'])
def random_image(message):
    try:
        image_path = get_random_image()
        if image_path:
            with open(image_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            # Clean up the temporary file
            os.unlink(image_path)
            logger.info(f"Sent random image to user {message.from_user.id}")
        else:
            bot.reply_to(message, "لا توجد صور متوفرة حالياً")
            logger.warning("No images available")
    except Exception as e:
        bot.reply_to(message, "حدث خطأ في إرسال الصورة")
        logger.error(f"Error in image command: {e}")

@bot.message_handler(commands=['list_folders'])
def list_folders(message):
    try:
        logger.info("Listing all folders in Dropbox root")
        result = dbx.files_list_folder('')
        folders = [entry.path_display for entry in result.entries if isinstance(entry, dropbox.files.FolderMetadata)]
        folder_list = "\n".join(folders)
        bot.reply_to(message, f"Available folders:\n{folder_list}")
    except Exception as e:
        logger.error(f"Error listing folders: {e}")
        bot.reply_to(message, "Error listing folders")

@bot.message_handler(commands=['test_dropbox'])
def test_dropbox(message):
    try:
        logger.info("Testing Dropbox connection")
        # Try to get current account information
        account = dbx.users_get_current_account()
        bot.reply_to(message, 
            f"✅ Dropbox connection successful!\n"
            f"Account: {account.name.display_name}\n"
            f"Email: {account.email}"
        )
        
        # Try to list root folder
        logger.info("Testing folder listing")
        result = dbx.files_list_folder('')
        num_items = len(result.entries)
        bot.reply_to(message, f"Successfully listed root folder. Found {num_items} items.")
        
    except dropbox.exceptions.AuthError:
        logger.error("Invalid/Expired Dropbox token")
        bot.reply_to(message, "❌ Authentication failed. The Dropbox token might be invalid or expired.")
    except Exception as e:
        logger.error(f"Error testing Dropbox connection: {e}")
        bot.reply_to(message, f"❌ Error: {str(e)}")

def main():
    logger.info("Starting bot...")
    try:
        # For GitHub Actions, run once and exit
        if os.getenv('GITHUB_ACTIONS'):
            bot.send_message(ADMIN_CHAT_ID, "Bot is running on GitHub Actions!")
            return

        # For local/continuous running
        bot.polling(none_stop=True, interval=3)
    except Exception as e:
        logger.error(f"Bot polling error: {e}")
        time.sleep(15)
        main()

if __name__ == '__main__':
    main()
