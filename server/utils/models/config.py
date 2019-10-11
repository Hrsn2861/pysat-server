"""get config from database
"""

from server.models import Config


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

def get_phone_verify_able():
    """get the phone verify config
    """
    text = get_config(name='phone_verify_able', default_value="false")
    return text == 'true'
