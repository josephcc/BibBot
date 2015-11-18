# coding: utf8

import re
import time
import uuid
import string
import threading
import Queue
from functools import *
from operator import *
from datetime import datetime
from commands import getoutput as _CMD

from slackclient import SlackClient

import config
from models import add_citation

STOP = 'no'
QUIT = 'quit'
SLACK_SLEEP = 1
GOOGLE_SLEEP = 120
QUEUE_TIMEOUT = 1
QUEUE = Queue.Queue()

def inturruptable_sleep(seconds):
  if seconds < 5:
    time.sleep(5)
    return
  for i in range(seconds):
    if STOP == QUIT:
      return
    time.sleep(1)

# TODO: slack already mark urls in <...>
re_urls = re.compile(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""", re.DOTALL)
def extract_urls(text):
  urls = re_urls.findall(text)
  urls = map(itemgetter(0), urls)
  return urls

NOT_FOUND = 'No results found, try again with a different query!'
def url2bibtext(url):
    out = _CMD('python venv/lib/python2.7/site-packages/gscholar/gscholar.py "%s"' % url).strip()
    inturruptable_sleep(GOOGLE_SLEEP)
    if out == '' or out == NOT_FOUND and 'pdf' in url.lower():
        filename = str(uuid.uuid4())
        _CMD('wget -O "%s" "%s"' % (filename, url))
        out = _CMD('python venv/lib/python2.7/site-packages/gscholar/gscholar.py "%s"' % filename).strip()
        _CMD('rm "%s"' % filename)
        inturruptable_sleep(GOOGLE_SLEEP)

    if out == '' or out == NOT_FOUND:
        return None
    return (url.strip(), out.strip())

def process(slack, msg):
  users = slack.server.users
  channels = slack.server.channels
  domain = slack.server.domain

  text = msg['text']
  time = datetime.fromtimestamp(float(msg['ts']))
  user = users.find(msg['user'])
  if type(user) == type(None):
    user = msg['user']
  else:
    user = user.name
  channel = channels.find(msg['channel'])
  if type(channel) == type(None):
    channel = msg['channel']
  else:
    channel = channel.name

  print '[%s] #%s @%s: %s - %s' % (domain, channel, user, text, time)
  # move this into a queue for a new thread to process so its not blocking
  urls = map(string.strip, extract_urls(text))
  urls = list(set(urls))
  for url in urls:
    QUEUE.put({
      'domain': domain,
      'channel': channel,
      'user': user,
      'text': text,
      'url': url,
      'time': time
    })
    print '<enqueued, size: %d>' % QUEUE.qsize()

def query():
  print '<query thread started>'
  while not (STOP == QUIT and QUEUE.empty()):
    try:
      item = QUEUE.get(True, QUEUE_TIMEOUT)
    except Queue.Empty:
      continue

    print '<dequeued, size: %d>' % QUEUE.qsize()
    bib = url2bibtext(item['url'])
    if bib == None:
      continue

    print '<queue size: %d>' % QUEUE.qsize()
    print item['url']
    print bib
    add_citation({
      'domain': item['domain'],
      'channel': item['channel'],
      'user': item['user'],
      'text': item['text'],
      'bibtex': bib,
      'url': item['url'],
      'time': item['time']
    })
    print

def bot(token):
  print '<bot thread started for: %s>' % token
  slack = SlackClient(token)
  if not slack.rtm_connect():
    print "Connection Failed, invalid token?", token
    return
  while True:
    data = slack.rtm_read()
    if data != []:
      data = filter(lambda i: i['type'] == 'message' and i.has_key('text'), data)
      map(partial(process, slack), data)
    else:
      if STOP == QUIT:
        return
      inturruptable_sleep(SLACK_SLEEP)

if __name__ == '__main__':

  thread = threading.Thread(target=query)
  thread.start()
  for token in config.TOKENS:
    thread = threading.Thread(target=bot, args=(token,))
    thread.start()

  try:
    while STOP != QUIT:
      STOP = raw_input('').strip()
  except:
    STOP = QUIT

  print 'TERMINATING THREADS...'
