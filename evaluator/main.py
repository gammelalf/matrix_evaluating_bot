#!/usr/bin/env python3
import logging
import asyncio

from nio import AsyncClientConfig, InviteMemberEvent, Event, MatrixRoom, RoomMessage

from expr_parser import evaluate

from hopfenmatrix.run import run
from hopfenmatrix.config import Config
from hopfenmatrix.callbacks import auto_join, debug

logger = logging.getLogger(__name__)


async def main():
    config = Config.from_json("config.json")

    client = config.new_async_client(AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=True,
    ))

    async def command(room, event):
        msg = event.body
        if msg.startswith("!eval"):
            expr = msg[len("!eval"):].strip()
            try:
                value = evaluate(expr)
            except:
                return
            await client.room_send(
                room.room_id,
                "m.room.message",
                {
                    "msgtype": "m.notice",
                    "body": str(value)
                },
                ignore_unverified_devices=True
            )

    client.add_event_callback(debug(), Event)
    client.add_event_callback(auto_join(client), InviteMemberEvent)
    client.add_event_callback(command, RoomMessage)

    await run(client, config)


asyncio.get_event_loop().run_until_complete(main())
