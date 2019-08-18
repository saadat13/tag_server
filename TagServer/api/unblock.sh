cd .. &&
bash pipenv shell &&
cd TagServer/ &&
python manage.py shell;
from api.models import Profile;
from datetime import datetime;
Profile.objects.filter(status="blocked", expire_date__gte=datetime.now()).update(status="available", expire_date=None);
echo "task done"

