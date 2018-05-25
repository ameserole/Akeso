import structlog
import time
import config
from AttackWorkers import startAttackWorkers


logger = structlog.get_logger()

AttackWorkerNumber = config.NUM_ATTACK_WORKERS

logger.info("DefenseLab", msg="Starting Attack Workers", workerNum=AttackWorkerNumber)
startAttackWorkers(AttackWorkerNumber)

while True:
    time.sleep(60)
