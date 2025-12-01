import os
from os import environ
from dotenv import load_dotenv
from ForwardBot.const_dirs import const_dirs_class

class Config(object):
    # এনভায়রনমেন্ট ভেরিয়েবল লোড করা
    load_dotenv(const_dirs_class.USER_DATA_PATH, encoding="utf-8")
    
    API_ID = int(environ.get("TELEGRAM_API_ID", 0))
    API_HASH = environ.get("TELEGRAM_API_HASH", None)
    BOT_TOKEN = environ.get("BOT_TOKEN", None) # ইউজারবট না চাইলে বট টোকেন ইউজ করতে পারো
    
    # সোর্স এবং ডেসটিনেশন
    CHANNEL_NAME_CLIENT = environ.get("CHANNEL_NAME_CLIENT", None) # Source
    CHANNEL_NAME_BOT = environ.get("CHANNEL_NAME_BOT", None)       # Destination
    
    # MongoDB কানেকশন
    CONNECTION_STRING = environ.get("CONNECTION_STRING", None)
    
    # ---------------------------------------------------------
    # তোমার কাস্টম টপিক ম্যাপিং (Keyword : Topic ID)
    # ---------------------------------------------------------
    TOPIC_MAP = {
    # বাংলা ও ইংরেজি
    "bangla": 885,
    "english": 886,
    
    # বিজ্ঞান বিভাগ (HSC)
    "physics": 2,
    "chemistry": 3,
    "math": 6,
    "biology": 4,
    "ict": 5,
    
    # কোচিং স্পেসিফিক (যদি লাগে)
    "udvash": 887,
    "acs": 888
}

    
    DEFAULT_TOPIC_ID = 1 # যদি কোনো কিওয়ার্ড না মেলে
