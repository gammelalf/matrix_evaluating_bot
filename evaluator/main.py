#!/usr/bin/env python3
import asyncio
import sys

from nio import AsyncClientConfig, AsyncClient

from hopfenmatrix.run import run
from evaluator.config import Config


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

    await run(client, config.user_id, config.user_password, config.device_name)


asyncio.get_event_loop().run_until_complete(main())
