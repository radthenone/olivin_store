import random


def generate_code() -> str:
    code = "".join([str(random.randint(0, 9)) for _ in range(4)])
    return code


def get_task_result(task_id: str, timeout: int = 10):
    from celery.result import AsyncResult

    task = AsyncResult(task_id)
    if task.ready():
        return task.get(timeout=timeout)
    else:
        return None
