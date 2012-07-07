def load_settings():
    '''Get the settings files from across the filesystem.'''
    import os
    import xdg.BaseDirectory as bd
    import ConfigParser
    import sys
    thismodule = sys.modules[__name__]

    config = ConfigParser.SafeConfigParser()
    paths = []
    for directory in reversed(bd.xdg_config_dirs):
        path = os.path.join(directory, 'budget-keeper', 'budget-keeper.conf')
        paths.append(path)

        if not os.path.exists(path):
            # If the directory does not exist, make it
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                except OSError:
                    # Don't have permissions.
                    pass

            # If there is no config there, copy the default to it.
            if not os.path.exists(path):
                import shutil
                source = os.path.join(os.path.dirname(thismodule.__file__), 'budget-keeper.conf')

                try:
                    shutil.copy(source, path)
                except IOError:
                    # No permissions again.
                    pass

    config.read(paths)

    for section in config.sections():
        for key, value in config.items(section):
            try:
                value = config.getboolean(section, key)
                value = config.getint(section, key)
            except ValueError:
                # Just use whatever it was last.
                pass

            setting = '_'.join((section, key)).upper()
            setattr(thismodule, setting, value)

load_settings()
