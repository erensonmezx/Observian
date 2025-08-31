from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_prune_old_logs(tmp_path, monkeypatch):
    """Ensure old log entries are removed while recent ones remain."""
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")

    from app.db import database
    from app.models.models import Base, Service, LogEvent
    from app.services.log_pruner import prune_old_logs

    Base.metadata.create_all(bind=database.engine)

    session = database.SessionLocal()
    service = Service(name="svc")
    session.add(service)
    session.commit()
    session.refresh(service)

    old_log = LogEvent(
        service_id=service.id,
        timestamp=datetime.utcnow() - timedelta(days=8),
        status_code=200,
        latency_ms=1.0,
    )
    new_log = LogEvent(
        service_id=service.id,
        timestamp=datetime.utcnow(),
        status_code=200,
        latency_ms=1.0,
    )
    session.add_all([old_log, new_log])
    session.commit()
    old_id, new_id = old_log.id, new_log.id
    session.close()

    prune_old_logs(days=7)

    session = database.SessionLocal()
    remaining_ids = [log.id for log in session.query(LogEvent).all()]
    session.close()

    assert new_id in remaining_ids
    assert old_id not in remaining_ids

