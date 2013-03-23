import sys
import itertools
import eventlet
from eventlet.green import httplib

CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789_'
USAGE = """Usage: %s [--brute N] [--dict FILE]
  --brute N                Tries all possible names of length N
  --dict FILE              Tries all possible names listed in the given file

Either --brute or --dict MUST be specified."""
POOL_SIZE = 10

def brute_force_names(length):
  return itertools.product(CHARS, repeat=length)

def get_http_status(name):
    c = httplib.HTTPSConnection("twitter.com")
    c.request("HEAD", "/%s" % name)
    return c.getresponse().status, name

def tuple_to_string(tup):
  return ''.join(tup)

if '--brute' in sys.argv:
  name_length = int(sys.argv[2])
  names = brute_force_names(name_length)
  using_dict = False
elif '--dict' in sys.argv:
  f = open(sys.argv[2])
  names = f.read().split()
  using_dict = True
else:
  print USAGE % sys.argv[0]
  sys.exit(-1)

# Just some stats variables
names_taken = 0
names_suspended = 0
names_available = 0
available_names = []

if using_dict:
  total_names = len(names)
else:
  total_names = len(CHARS) ** name_length
  names = [tuple_to_string(name) for name in names]

print "Trying %d names..." % total_names

thread_pool = eventlet.GreenPool(POOL_SIZE)

for status, name in thread_pool.imap(get_http_status, names):
  # 404 = not Found. It's available!
  if status == 404:
    print "Name available: " + name
    names_available += 1
    available_names.append(name)

  # 200 = OK. It's taken.
  elif status == 200:
    names_taken += 1

  # 302 = Moved. The account has been suspended.
  elif status == 302:
    names_suspended += 1

  else:
    print "Bad code. Name: %s; Code: %d" % (name, status)

# Print results
print str(total_names) + " total names checked"
print str(names_taken) + " were taken"
print str(names_suspended) + " were suspended. (unusable)"
print str(names_available) + " were available."
if names_available > 0:
  print "They are: " + str(available_names)[1:-1]

