# app/workers/log_pruning_worker.py
import asyncio
import logging
from app.services.log_pruner import prune_old_logs

logging.basicConfig(level=logging.INFO)

async def run_pruner_loop():
    while True:
        logging.info("🧹 Running scheduled log pruning...")
        prune_old_logs(days=7)
        await asyncio.sleep(86400)  # Sleep for 1 day (Not the best way to do this but it's okay)

if __name__ == "__main__":
    asyncio.run(run_pruner_loop())