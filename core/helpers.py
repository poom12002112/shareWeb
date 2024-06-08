import os
import time
from django.conf import settings
from django.db import connection

def upload_handle(instance, filename):
    if hasattr(connection, 'schema_name') and connection.schema_name:
        schema_name = connection.schema_name
    else:
        # 在没有 schema_name 属性的情况下，可以使用其他方法来确定数据库的标识符
        schema_name = 'default_schema'

    schema_dir = os.path.join(settings.MEDIA_ROOT, schema_name)
    if not os.path.exists(schema_dir):
        os.makedirs(schema_dir)

    model_dir = os.path.join(schema_dir, instance.__class__.__name__.lower() + '_media')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    timestamp = str(int(time.time()))
    return '/'.join([schema_name, instance.__class__.__name__.lower() + '_media', name + timestamp + ext])
