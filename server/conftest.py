"""set database for pytest
"""

import pytest
from django.conf import settings

@pytest.fixture(scope='session')
@pytest.mark.django_db()
def django_db_setup():
    """set db
    """
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ctrl_test_pysat',
        'PORT': 3306,
        "HOST": 'database.CTRL.secoder.local',
        'USER': 'ctrl',
        'PASSWORD': 'ctrl666'
    }
