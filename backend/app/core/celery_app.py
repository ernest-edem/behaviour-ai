from celery import Celery

celery_app = Celery(
    "behaviorlens",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=[
        "app.workers.prediction_worker",
        "app.workers.recommendation_worker",
        "app.workers.report_worker",
    ],
)

celery_app.conf.update(
    # =====================================================
    # SERIALIZATION
    # =====================================================
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    # =====================================================
    # MONITORING / OBSERVABILITY
    # =====================================================
    task_track_started=True,
    worker_send_task_events=True,
    task_send_sent_event=True,

    # =====================================================
    # TIME LIMITS
    # =====================================================
    task_time_limit=300,
    task_soft_time_limit=240,

    # =====================================================
    # WORKER STABILITY
    # =====================================================
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
    task_acks_late=True,

    # =====================================================
    # QUEUE ROUTING
    # =====================================================
    task_routes={
        "app.workers.prediction_worker.run_prediction": {
            "queue": "prediction_queue",
        },
        "app.workers.recommendation_worker.generate_recommendations": {
            "queue": "recommendation_queue",
        },
        "app.workers.report_worker.generate_report": {
            "queue": "report_queue",
        },
    },
)