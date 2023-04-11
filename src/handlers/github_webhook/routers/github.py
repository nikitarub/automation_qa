from fastapi import APIRouter, BackgroundTasks
import time
import asyncio
from common import log
from scenario.scenario import Scenario

from configs.config_switcher import config_switch



router = APIRouter(
    prefix="/github",
    tags=["github"],
    responses={404: {"description": "Not found"}},
)

def notify_telegram_stub(message):  
    time.sleep(2)
    log.info(f"Sent telegram: {message}")


@router.post("/")
def work_webhook(background_tasks: BackgroundTasks): 
    log.info("Got github webhook POST request")
    time.sleep(1)    
    log.info("Done with github webhook POST request")
    options = {}
    options['branch'] = "master"
    options['version'] = "patch"
    config = config_switch("target")
    Scenario("release_backend", options, config)
    background_tasks.add_task(notify_telegram_stub, "Done processing all")
    return "good"
