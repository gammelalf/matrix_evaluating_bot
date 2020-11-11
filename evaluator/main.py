#!/usr/bin/env python3
import logging
import asyncio
import sys

from nio import AsyncClientConfig, AsyncClient, InviteMemberEvent, JoinError

from hopfenmatrix.run import run
from evaluator.config import Config

logger = logging.getLogger(__name__)


async def main():
    # Read config file
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "config.yaml"
    config = Config(config_path)

    # Configuration options for the AsyncClient
    client_config = AsyncClientConfig(
        max_limit_exceeded=0,
        max_timeouts=0,
        store_sync_tokens=True,
        encryption_enabled=True,
    )

    # Initialize the matrix client
    client = AsyncClient(
        config.homeserver_url,
        config.user_id,
        device_id=config.device_id,
        store_path=config.store_path,
        config=client_config,
    )

    async def join(room, event):
        logger.debug(f"Got invite to {room.room_id} from {event.sender}.")

        # Attempt to join 3 times before giving up
        for attempt in range(3):
            result = await client.join(room.room_id)
            if type(result) == JoinError:
                logger.error(
                    f"Error joining room {room.room_id} (attempt %d): %s",
                    attempt,
                    result.message,
                )
            else:
                break
        else:
            logger.error("Unable to join room: %s", room.room_id)

        # Successfully joined room
        logger.info(f"Joined {room.room_id}")

    client.add_event_callback(join, InviteMemberEvent)

    await run(client, config.user_id, config.user_password, config.device_name)


asyncio.get_event_loop().run_until_complete(main())
