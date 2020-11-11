#!/usr/bin/env python3
import logging
import asyncio

from nio import AsyncClientConfig, InviteMemberEvent, Event

from hopfenmatrix.run import run
from hopfenmatrix.config import JsonConfig
from hopfenmatrix.callbacks import auto_join, debug

logger = logging.getLogger(__name__)


async def main():
    config = JsonConfig("config.json")

    client = config.new_async_client(AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=True,
    ))

    client.add_event_callback(debug(), Event)
    client.add_event_callback(auto_join(client), InviteMemberEvent)

    await run(client, config)


asyncio.get_event_loop().run_until_complete(main())
