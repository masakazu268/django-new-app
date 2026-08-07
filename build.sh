#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# --clear を追加して古い静的ファイルをクリア
python manage.py collectstatic --no-input --clear
python manage.py makemigrations
python manage.py migrate

# スーパーユーザー自動作成（存在しない場合のみ）
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('SUPERUSER_NAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('SUPERUSER_PASSWORD', 'adminpass123')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created successfully.')
"