"""Models for pysat
"""

from django.db import models

# Create your models here.


class Config(models.Model):
    """Config
    """
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=128)

class ConfigHelper:
    """get config from database
    """

    @staticmethod
    def get_config(name, default_value=""):
        """get config

        if the config does not exist, it will add `default_value` into database, and return it.
        """
        configs = Config.objects.filter(name=name)
        if configs.exists():
            config = configs.last()
            return config.value
        Config(name=name, value=default_value).save()
        return default_value

    @staticmethod
    def get_phone_verify_able():
        """get the phone verify config
        """
        text = ConfigHelper.get_config(name='phone_verify_able', default_value="false")
        return text == 'true'

    @staticmethod
    def get_size_per_page():
        """get the size of a page
        """
        text = ConfigHelper.get_config(name='size_per_page', default_value='20')
        return int(text)
