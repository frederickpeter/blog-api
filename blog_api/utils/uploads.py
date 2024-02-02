import os
from uuid import uuid4


def avatar_wrapper(instance, filename):
    upload_to = "profile_pics"
    ext = filename.split(".")[-1]
    # set filename as random string
    filename = f"{uuid4().hex}.{ext}"
    # return the whole path to the file
    return os.path.join(upload_to, filename)
