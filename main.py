import os
from coupon_bot import CouponBot

TOKEN = os.environ.get("RAKAN_TOKEN")

bot = CouponBot(TOKEN)

bot.infinity_polling()
