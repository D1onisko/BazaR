import os

DIO_MAIN_TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates')

DIO_CORE_APPS = [
    'src',
    'src.apps.catalogue',

    'sorl.thumbnail',
    'mptt',
    'django_mptt_admin',
    'autoslug',
]


def get_core_apps(overrides=None):
    """
    Return a list of oscar's apps amended with any passed overrides
    """
    if not overrides:
        return DIO_CORE_APPS

    # Conservative import to ensure that this file can be loaded
    # without the presence Django.
    from django.utils import six

    if isinstance(overrides, six.string_types):
        raise ValueError(
            "get_core_apps expects a list or tuple of apps "
            "to override")

    def get_app_label(app_label, overrides):
        pattern = app_label.replace('src.apps.', '')
        for override in overrides:
            if override.endswith(pattern):
                if 'dashboard' in override and 'dashboard' not in pattern:
                    continue
                return override
        return app_label

    apps = []
    for app_label in DIO_CORE_APPS:
        apps.append(get_app_label(app_label, overrides))
    return apps
