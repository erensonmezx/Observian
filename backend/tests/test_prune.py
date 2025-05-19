# app/db/test_prune.py
from app.services.log_pruner import prune_old_logs

if __name__ == "__main__":
    prune_old_logs(days=7)