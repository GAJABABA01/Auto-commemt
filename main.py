import asyncio
from fastapi import FastAPI, Query
from pyrogram import Client
from pyrogram.errors import RPCError, ChatWriteForbidden, InviteHashInvalid

app = FastAPI()

# ✅ Your Telegram API credentials
api_id = 23347107
api_hash = "8193110bf32a08f41ac6e9050b2a4df4"

# ✅ All session strings with emojis
sessions = [
    {
        "session_string": "BQFkP6MAecJP8lDAPnxVAFV8G-tGxphqRwEWjvE8_8vyUHaLREqyaEkGeWBqOdtZ2GbomzqvlhgmcYjvlh1FVCEAV6hBnkx7YNg7tyPt2_5_X0TFWPCetUYo7K5MNKyL-5sDAxhsS02RS94u2BSbc8RcvNwP79CPXXTWde12fMQPXt8KHJZdzZ57s1S0cz-KR5LqO1TuyKnX3tT6ODzIfCDDbD7Op9RUBQXPWzKHD9SksCR3VuYAm7DS8pOAi7QeWeMi4O-TCPgnNjzJDNf4xyqdrXpeVPnKjNfM9AFf6rhZfKt-eoELxrk0z6_ScDWyPK5MFMjIfGprcwKyoVmVTuW7vVDc4SYMDAAAFYm1rbwA",
        "emoji": "❤️"
    },
    {
        "session_string": "BQFkP6MAvfFYzMo4v_dKtRzB9pTaaBwiIkdH8lBg-uv7FaVPIVI4xyBoRTdChUnBN2OtozSB2yx_hZMdWzMwe2jjhO0-7AcY4tdxZP4E-sfZBMXKyebx9TX_Vh5AcnxNijRsDulBoC0WaA8bbZgWDkafco0sB8LObxEDqB2DRA3TkfV2AAK4m3U6o8fDqH_SzrkpyZPQTDyBhXYedfl1rBDoqMJHtYJDrRu0EDPGj5eEBObQ4BeR6OE0GWaS25M-PvANbm6b3zQtWRZ4Iq3bI5Ez0UKaVbA9EiA1w4IysXjCmQgWIQyxvCQcU_JD5lYX2xu0xIEmkP47EnC6P82q5vbWjkS9o6AAgAA",
        "emoji": "🥰"
    },
    {
        "session_string": "BQFkP6MAHYepECQoFzFWkMDzp7iwqpK09AT6bJvuEXUAPhZ_iH4kYZ37PQZtCKu_2vskHUsAyIt7R9mkwTk3D-rdscvM39mmg0txfdW2S2-jOEAE0bEHFYmUJ3oYyhs4N3B7TFKqF1gUGZ4f7OguZ6r1m5JKnkG8i9nzTVRJDhdSAgHOq6tDj_1AsNf5wTGqKckkOCBexUu7-Yu0ph-PT9hr-v48B_WBltVGfgAF-x7YVsW7dzxLGgZuWsnC-2-0yKr7RtXB6p4LPdUhnX0z3Y2qnULV83TTf-RYHKcUYVbMgfWtbBbYjq8NoJZXZEnQHh2PWv1BWkpCZ6lRyxGVkdkLnh9UAAA",
        "emoji": "💚"
    },
    {
        "session_string": "BQFkP6MAFlmegc8N5r_KLJoix3fKzw5j5IC8HLlk24xpICO52l5kB9hFpV0x3LtL84K1gqK4OHhlxVrJ1gmgwHnH8ieBBdIQKXKXoHeTxptfbA8kY_Yz4Wb-CeX7MRsUMalZIXH9MiKnXE_LSzY3K7fSOcXQH0rLZqSG-UZdfXvPOH3YiEn0d_KP5aFHDqUtI1dZrxOyeDFyXw5FzvfrhCPRhEbMeQZf_hvgu0ZrYLCQx0zrUdYpN4cwlzgR_npy9yo6dyxFvOpJTrnE2yt0TxLvj7x0fHVjgr1LU3V7BIsg4qB5K-EpAyXvViD4WVDjWwnmdvoRS2x3eBJPuucJZxObL4ZgAAA",
        "emoji": "💙"
    },
    {
        "session_string": "BQFkP6MAPVXyb_FqJrhTm8HwWx2e8iz3byjwdcsMrSYMECNEHjFq4gwUtzfcaYIiciws4fFrvOF4m1zBujJ8nDVNOPK3MLu_yIxQhUGL07KdMHYgHWGXpUXwDs3n9FK2bsF_e2iN7qBqS_bGqSXWVlB7QhS99QU15h5sCDATcSNAH2R7fuzWzTOECjPLrjWAzi-OZ5HhNgeXeZ89sSNx933jWKAGy9r9nmHREEiRguV28Z5XSRNV3U8jzpRI1gHiqMILQqSorvKHYQ9Vt4rStxKPvt8PWLmmNA4JiJGUAlTfNMCjv2woh9xUcq_-g60un5f5qiN_X6b94g4lWwhwTmvJwSYMDAAAAAH5V3EJAA",
        "emoji": "🔥"
    }
]

# ✅ Function to send message
async def send_messages(app, chat, msg_id, comment, emoji):
    joined = False
    try:
        await app.join_chat(chat)
        joined = True
    except InviteHashInvalid:
        print(f"Invalid invite link.")
        return
    except RPCError as e:
        print(f"Join error: {e}")
        return

    try:
        text_to_send = comment + " " + emoji
        if msg_id:
            await app.send_message(chat_id=chat, text=text_to_send, reply_to_message_id=msg_id)
        else:
            await app.send_message(chat_id=chat, text=text_to_send)
    except ChatWriteForbidden:
        print("No permission.")
    except Exception as e:
        print(f"Send error: {e}")

    if joined:
        try:
            await app.leave_chat(chat)
        except Exception as e:
            print(f"Leave error: {e}")

# ✅ Process full task
async def process(link: str, comment: str, amount: int):
    try:
        parts = link.rstrip("/").split("/")
        if parts[-1].isdigit():
            chat = parts[-2]
            msg_id = int(parts[-1])
        else:
            chat = parts[-1]
            msg_id = None
    except:
        return {"error": "Invalid link format"}

    clients = []
    for index, s in enumerate(sessions):
        app = Client(
            f"session_{index}",
            api_id=api_id,
            api_hash=api_hash,
            session_string=s["session_string"]
        )
        clients.append(app)

    await asyncio.gather(*(client.start() for client in clients))

    for index, app in enumerate(clients):
        for _ in range(amount):
            await send_messages(app, chat, msg_id, comment, sessions[index]["emoji"])
            await asyncio.sleep(1)

    await asyncio.gather(*(client.stop() for client in clients))
    return {"status": "✅ Done"}

# ✅ FastAPI endpoint
@app.get("/api")
async def handle_request(link: str = Query(...), message: str = Query(...), amount: int = Query(1)):
    return await process(link, message, amount)
