# app/state/ingestor_task.py

import asyncio
import logging
from app.ingestors.github_ingestor import poll_github_events

ingestor_task = None

def start_ingestor():
    global ingestor_task
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if ingestor_task is not None and not ingestor_task.done():
        logging.info("Ingestor already running. Skipping start.")
        return

    ingestor_task = loop.create_task(poll_github_events())
    logging.info("Ingestor started.")

def stop_ingestor():
    global ingestor_task
    if ingestor_task and not ingestor_task.done():
        ingestor_task.cancel()
        try:
            asyncio.get_event_loop().run_until_complete(ingestor_task)
        except asyncio.CancelledError:
            logging.info("Ingestor cancelled cleanly.")
            