import sys
import urllib2
import itertools

chars = 'abcdefghijklmnopqrstuvwxyz0123456789_'

def brute_force_names(length):
  return itertools.product(chars, repeat=length)

# Command line arg gives length of names to check.
# Defaults to 1
if len(sys.argv) == 1:
  name_length = 1
  names = brute_force_names(name_length)
  using_dict = False
elif sys.argv[1] == 'dict':
  f = open('words')
  names = f.read().split()
  using_dict = True
elif sys.argv[1].isdigit():
  name_length = int(sys.argv[1])
  names = brute_force_names(name_length)
  using_dict = False
else:
  print "Error: argument must be number or 'dict'"
  sys.exit(-1)

# Just some stats variables
names_taken = 0
names_suspended = 0
names_available = 0
available_names = []

if using_dict:
  total_names = len(names)
else:
  total_names = len(chars) ** name_length

print "Trying %d names..." % total_names

for name in names:
  # Join tuples into string
  name = ''.join(name)

  try:
    status = urllib2.urlopen('http://twitter.com/' + name).getcode()
  except:
    # 404 = Not Found. It's available!
    print "Name available: " + name
    names_available += 1
    available_names.append(name)
    continue

  # 200 = OK. It's taken.
  if status == 200:
    names_taken += 1

  # 302 = Moved. The account has been suspended.
  elif status == 302:
    names_suspended += 1

  else:
    print "Strange result with name:" + name

print str(total_names) + " total names checked"
print str(names_taken) + " were taken"
print str(names_suspended) + " were suspended. (unusable)"
print str(names_available) + " were available."
if names_available > 0:
  print "They are: " + str(available_names)[1:-1]

