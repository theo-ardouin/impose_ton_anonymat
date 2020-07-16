from enum import Enum


class Permission(Enum):
    QUERY_IMAGE = "image.query"
    WRITE_SCHEDULE = "schedule.write"
    WRITE_PERMISSION = "permission.write"
