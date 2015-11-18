# coding: utf8

import re
import time
import uuid
import string
import threading
from functools import *
from operator import *
from datetime import datetime
from slackclient import SlackClient
from commands import getoutput as _CMD
from config import tokens

stop = 'no'


re_urls = re.compile(r"""((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|(([^\s()<>]+|(([^\s()<>]+)))*))+(?:(([^\s()<>]+|(([^\s()<>]+)))*)|[^\s`!()[]{};:'".,<>?«»“”‘’]))""", re.DOTALL)
def extract_urls(text):
  urls = re_urls.findall(text)
  urls = map(itemgetter(0), urls)
  return urls

NOT_FOUND = 'No results found, try again with a different query!'
def url2bibtext(url):
    out = _CMD('python venv/lib/python2.7/site-packages/gscholar/gscholar.py "%s"' % url).strip()
    if out == '' or out == NOT_FOUND and 'pdf' in url.lower():
        filename = str(uuid.uuid4())
        _CMD('wget -O "%s" "%s"' % (filename, url))
        out = _CMD('python lib/python2.7/site-packages/gscholar/gscholar.py "%s"' % filename).strip()
        _CMD('rm "%s"' % filename)

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

  urls = map(string.strip, extract_urls(text))
  urls = list(set(urls))
  bibs = map(url2bibtext, urls)
  bibs = filter(lambda x: x != None, bibs)

  print '[%s] #%s @%s: %s - %s' % (domain, channel, user, text, time)
  for url, bib in bibs:
    print url
    print bib
  print
  
def bot(token):
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
      if stop == 'quit':
        return
      time.sleep(1)

if __name__ == '__main__':

  for token in tokens:
    thread = threading.Thread(target=bot, args=(token,))
    thread.start()
    
  try:
    while stop != 'quit':
      stop = raw_input('').strip()
  except:
    stop = 'quit'

  print 'TERMINATING THREADS...'

