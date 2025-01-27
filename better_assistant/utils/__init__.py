from datetime import timedelta, timezone

from better_assistant.utils.mongo import MongoClientWrapper as MongoClientWrapper


def get_kst_timezone() -> timezone:
    return timezone(timedelta(hours=9), name="KST")
