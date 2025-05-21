import os
import logging
from fastapi import APIRouter, Header, HTTPException, Depends
from app.state.control import ingest_control
from app.state.ingestor_task import start_ingestor, stop_ingestor
from app.services.log_pruner import prune_old_logs


def verify_api_key(x_api_key: str = Header(...)):
    expected_key = os.getenv("API_KEY")
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

router = APIRouter()

@router.get("/control/ingestor-status")
def get_status():
    return {"enabled": ingest_control.is_enabled()}

@router.post("/control/ingestor-toggle")
def toggle_ingestion(enable: bool, _: str = Depends(verify_api_key)):
    ingest_control.toggle(enable)
    if enable:
        start_ingestor()
    else:
        stop_ingestor()
        logging.info(f"Ingestor toggled to {'ENABLED' if enable else 'DISABLED'}")
    return {"enabled": ingest_control.is_enabled()}

@router.get("/control/ingestor-health")
def ingestor_health(_: str = Depends(verify_api_key)):
    from app.state.ingestor_task import ingestor_task
    if ingestor_task is None:
        return {"running": False, "reason": "Not started"}
    elif ingestor_task.done():
        return {"running": False, "reason": "Task completed or crashed"}
    else:
        return {"running": True}
    


# Manual log pruning endpoint
@router.post("/control/prune")
def manual_prune(_: str = Depends(verify_api_key)):
    try:
        prune_old_logs(days=7)
        logging.info("🧹 Manual log pruning triggered.")
        return {"status": "success", "message": "Old logs pruned."}
    except Exception as e:
        logging.error(f"❌ Manual pruning failed: {e}")
        raise HTTPException(status_code=500, detail="Pruning failed.")
