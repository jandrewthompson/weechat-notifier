# consume notifications from redis

import sys
import json
import subprocess
import redis
import time


def growl(message):
    # args = ['growlnotify', '-m', message]
    args = ['notify-send', 'IRC',  message]
    subprocess.check_call(args)


def highlight_decision(event):
    if event['hilight']:
        return True

    elif 'notify_private' in event['tags']:
        return True

    elif event['buffer_name'] == 'bitlbee.#naaya':
        return True

    elif event['buffer_is_front']:
        return True

    else:
        return False


def consume_json(e):
    event = json.loads(e)
    # print event
    if highlight_decision(event):
        growl("%(prefix)s | %(msg)s" % event)


def main():
    redis_port = int(sys.argv[1])
    server = redis.Redis(port=redis_port, db=13)
    while True:
        msg = server.lpop('weechat')
        if msg != None:
            consume_json(msg)
        time.sleep(5)



if __name__ == "__main__":
    main()
