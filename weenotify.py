# encoding: utf-8
# send notifications of weechat messages to redis

SCRIPT_NAME    = "weenotify"
SCRIPT_AUTHOR  = "J. Andrew Thompson"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "Unlicense"
SCRIPT_DESC    = "Redis notifications for WeeChat."
SCRIPT_COMMAND = "weenotify"


try:
    import weechat
    import_ok = True
except:
    print "This script must be run under WeeChat."
    import_ok = False


import json
import logging
import redis

class WeechatLogHandler(logging.Handler):
    def handle(self, record):
        msg = self.format(record)
        weechat.prnt("", msg)


log = logging.getLogger('weechat.plugins.weenotify')
log.addHandler(WeechatLogHandler())
log.setLevel(logging.DEBUG)


class WeeNotify(object):
    def __init__(self):
        self.redis = redis.Redis(db=13)

    def notify(self, msg):
        self.redis.lpush('weechat', json.dumps(msg))

    def user_command(self, data, buffer, args):
        self.notify({'prefix': "TEST", 'msg': args})
        return weechat.WEECHAT_RC_OK

    def got_message(self, _ign, buffer, time, tags, display, hilight, prefix, msg):
        log.debug('%r', (buffer, time, tags, display, hilight, prefix, msg))
        msg = {
            'time': int(time),
            'tags': tags.split(','),
            'display': bool(display=='1'),
            'hilight': bool(hilight=='1'),
            'prefix': prefix,
            'msg': msg,
            'buffer_name': weechat.buffer_get_string(buffer, "name"),
            'buffer_is_front': bool(weechat.buffer_get_integer(buffer, 'num_displayed') != 0),
            'inactivity': int(weechat.info_get('inactivity', '')),
        }
        if hilight == '1':
            self.notify(msg)
        return weechat.WEECHAT_RC_OK


if __name__ == '__main__' and import_ok and \
        weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                         SCRIPT_LICENSE, SCRIPT_DESC, '', ''):

    weenotify = WeeNotify()

    user_command = weenotify.user_command
    weechat.hook_command(SCRIPT_COMMAND, SCRIPT_DESC, 'test [msg]',
                         "[TODO docs]", "", 'user_command', '')

    got_message = weenotify.got_message
    weechat.hook_print('', 'notify_message', '', 1, 'got_message', '')
    weechat.hook_print('', 'notify_private', '', 1, 'got_message', '')
