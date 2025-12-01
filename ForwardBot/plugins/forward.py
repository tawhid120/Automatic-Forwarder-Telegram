import pyrogram
from pyrogram import filters
from ForwardBot import bot, Config, LOGS

# সোর্স চ্যানেল থেকে আসা মেসেজ হ্যান্ডেল করবে
@bot.on_message(filters.chat(Config.CHANNEL_NAME_CLIENT))
async def pdf_sorter(client, message):
    try:
        # ১. আমরা শুধু ডকুমেন্ট বা ফাইল খুঁজব
        if not message.document and not message.video and not message.photo:
            return # ফাইল না থাকলে ইগনোর করবে

        # ২. ফাইলের নাম এবং ক্যাপশন বের করা
        file_name = message.document.file_name if message.document else ""
        caption = message.caption or message.text or ""
        
        # সার্চের সুবিধার জন্য সব লোয়ারকেস করা
        search_text = (file_name + " " + caption).lower()
        
        LOGS.info(f"New File Detected: {file_name}")

        # ৩. সঠিক টপিক আইডি খুঁজে বের করা
        target_topic_id = None
        
        # Config থেকে ম্যাপ চেক করা
        for keyword, topic_id in Config.TOPIC_MAPPING.items():
            if keyword in search_text:
                target_topic_id = topic_id
                LOGS.info(f"✅ Match Found: '{keyword}' -> Topic {topic_id}")
                break
        
        # যদি ম্যাচ না করে, তবে ডিফল্ট টপিকে (বা ইগনোর করতে পারো)
        if not target_topic_id:
            target_topic_id = Config.DEFAULT_TOPIC_ID
            LOGS.info(f"⚠️ No Match. Sending to Default Topic {target_topic_id}")

        # ৪. ফাইলটি ফরোয়ার্ড/কপি করা (Topic ID সহ)
        # destination channel id মূলত user_data.env থেকে আসবে
        # কিন্তু আমাদের ID দরকার, নাম না। তাই সেটআপের সময় ID দিতে হবে।
        
        if Config.BOT_CHANNEL_ID: 
            await message.copy(
                chat_id=Config.BOT_CHANNEL_ID,
                message_thread_id=target_topic_id, # এই প্যারামিটারটিই টপিকে পাঠাবে
                caption=caption # অরিজিনাল ক্যাপশন রাখা
            )
            LOGS.info("🚀 File Forwarded Successfully!")

    except Exception as e:
        LOGS.error(f"Error in forwarding: {e}")
