# app/state/ingestor_task.py

import asyncio
import logging
from app.ingestors.github_ingestor import poll_github_events

ingestor_task = None

def start_ingestor(loop=None):
    global ingestor_task
    if loop is None:
        loop = asyncio.get_event_loop()
    if ingestor_task is not None and not ingestor_task.done():
        logging.info("Ingestor already running. Skipping start.")
        return
    ingestor_task = loop.create_task(poll_github_events())
    logging.info("Ingestor started.")

def stop_ingestor():
    global ingestor_task
    if ingestor_task and not ingestor_task.done():
        ingestor_task.cancel()
        logging.info("Ingestor cancelled.")
    else:
        logging.info("No ingestor task to cancel.")
