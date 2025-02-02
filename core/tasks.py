from celery import signals, shared_task
from celery.exceptions import WorkerShutdown


@shared_task
def debug_task():
    return "Debug task running successfully!"


@shared_task
def debug_task_with_shutdown():
    return "Debug task running successfully!"


@signals.task_postrun.connect(sender=debug_task_with_shutdown)
def shutdown_worker(**kwargs):
    print("Tarefa concluída, finalizando o worker suavemente...")
    raise WorkerShutdown()
