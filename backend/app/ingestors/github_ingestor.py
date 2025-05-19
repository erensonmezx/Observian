import requests
import time
import random
import logging 
import asyncio
from app.state.control import ingest_control

# config
BACKEND_URL = 'https://observian.onrender.com/logs'
GITHUB_EVENTS_URL = 'https://api.github.com/events'
POLL_INTERVAL = 60
HEADERS = {'User-Agent':'ObservianGitHubIngestor/1.0'}

# logging
logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# event -> status code mapping
EVENT_STATUS_MAP = {
    "PushEvent": 200,
    "PullRequestEvent": 201,
    "DeleteEvent": 204,
    "CreateEvent": 202,
    "IssuesEvent": 400,
    "ForkEvent": 302,
    "ReleaseEvent": 201,
    "IssueCommentEvent": 403,
    "PublicEvent": 200,
}

last_seen_event_id = None # global tracker to prevent resending the same events

def transform_event(event):
    """Convert GitHub event into observian compatible log dict"""
    service_name = event.get('repo', {}).get('name')
    if not service_name:
        raise ValueError("Missing service_name in event")
    try:
        service_name = event['repo']['name']
        event_type = event['type']
        status_code = EVENT_STATUS_MAP.get(event_type, 200)
        latency_ms = random.randint(100, 1000)
        return {
            'service_name': service_name,
            'status_code': status_code,
            'latency_ms' : latency_ms,
            'event_type' : event_type
        }
    except Exception as e:
        logging.warning(f'Failed to transform event: {e}')
        return None
    
def post_to_observian(log_payload):
    try:
        response = requests.post(BACKEND_URL, json= log_payload, timeout = 10)
        if response.status_code == 200:
            logging.info(f"Sent log: {log_payload['service_name']} | {log_payload['event_type']} [{log_payload['status_code']}]")
        else:
            logging.warning(f"Failed to send log: {response.status_code} | {response.text}")
    except Exception as e:    
        logging.error(f"Exception while posting log: {e}")

async def poll_github_events():
    global last_seen_event_id
    logging.info("Starting GitHub event polling loop")
    poll_count = 0
    while True:
        try:
            res = requests.get(GITHUB_EVENTS_URL, headers=HEADERS, timeout=10)
            res.raise_for_status()
            data = res.json()            
            
            if res.status_code != 200:
                logging.warning(f"GitHub API error: {res.status_code}")
                await asyncio.sleep(POLL_INTERVAL)
                continue
            
            events = res.json()
            new_events = []
            
            for event in events:
                if event['id'] == last_seen_event_id:
                    break
                new_events.append(event)
                
            if new_events:
                logging.info(f"{len(new_events)} new events to process...")
                last_seen_event_id = new_events[0]['id']
                
                for event in reversed(new_events):
                    payload = transform_event(event)
                    if payload:
                        post_to_observian(payload)
            else:
                logging.info('No new GitHub Events')
            
        except Exception as e:
            logging.exception(f"Unexpected error during GitHub event ingestion: {e}")
        
        poll_count += 1
        if poll_count % 10 == 0:
            logging.info("GitHub ingestor is still running.")
            
        await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    asyncio.run(poll_github_events())
