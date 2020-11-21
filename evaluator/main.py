#!/usr/bin/env python3
import logging
import asyncio

from nio import AsyncClientConfig, InviteMemberEvent, Event, MatrixRoom, RoomMessage

from expr_parser import evaluate

from hopfenmatrix.api_wrapper import ApiWrapper

logger = logging.getLogger(__name__)


async def command(api: ApiWrapper, room: MatrixRoom, event: RoomMessage):
    try:
        value = evaluate(event.stripped_body)
    except Exception as err:
        logger.exception("Encountered error while evaluating:", exc_info=err)
        return
    await api.send_reply(str(value), room, event, send_as_notice=True)




async def main():
    api = ApiWrapper(display_name="Evaluator Bot")

    api.set_auto_join()
    api.register_command(command, ["eval"], make_default=True)

    await run(client, config)


asyncio.get_event_loop().run_until_complete(main())
