import ConfigParser as cp

CONFIG_FILE = 'crawler.conf'
_CONF = cp.ConfigParser()
_CONF.readfp(open(CONFIG_FILE))

def get(opt, section='DEFAULT'):
        return _CONF.get(section, opt)
