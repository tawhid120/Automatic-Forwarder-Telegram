import asyncio
import os
import sys
from importlib import import_module
from threading import Thread
from flask import Flask

# Flask Web Server Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "<h3>Automatic Forwarder Bot is Running!</h3>"

def run_web_server():
    # Render provides the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ---------------------------------------------------
# Bot Logic Integration (Linking to your existing project)
# ---------------------------------------------------

# We need to add the current directory to sys.path to ensure modules are found
sys.path.append(os.getcwd())

from pyrogram import idle
from ForwardBot import bot, LOGS
from ForwardBot.plugins import ALL_MODULES
from ForwardBot.utils_no_bot import MODS

# Loading Modules (Copied logic from your original __main__.py)
LOGS.info("Loading Modules for Render...")
for module_name in MODS:
    try:
        import_module("ForwardBot.utils_no_bot." + module_name)
    except Exception as e:
        LOGS.error(f"Failed to load utils_no_bot module {module_name}: {e}")

for module_name in ALL_MODULES:
    try:
        import_module("ForwardBot.plugins." + module_name)
    except Exception as e:
        LOGS.error(f"Failed to load plugin {module_name}: {e}")

async def start_bot():
    try:
        LOGS.info("Starting Bot Client...")
        await bot.start()
        LOGS.info("Bot Started Successfully on Render!")
        await idle()
    except Exception as ex:
        LOGS.error(f"Bot failed to start: {ex}")
        sys.exit(1)
    finally:
        await bot.stop()

def run_bot_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())

if __name__ == "__main__":
    # 1. Start Web Server in a separate thread (Daemon mode)
    # This keeps Render happy by listening to the PORT
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    # 2. Run the Main Bot Logic in the main thread
    LOGS.info("Initiating Bot Loop...")
    run_bot_loop()


