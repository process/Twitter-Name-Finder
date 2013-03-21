import sys
import urllib2
import itertools

chars = 'abcdefghijklmnopqrstuvwxyz0123456789_'

# Command line arg gives length of names to check.
# Defaults to 1
if len(sys.argv) == 1:
  name_length = 1
else:
  name_length = int(sys.argv[1])

names = itertools.product(chars, repeat=name_length)

# Just some stats variables
names_taken = 0
names_suspended = 0
names_available = 0
available_names = []
total_names = len(chars) ** name_length

print "Trying %d names..." % total_names

for name in names:
  name = ''.join(name)
  status = urllib2.urlopen('http://twitter.com/' + name).getcode()

  # 404 = Not Found. It's available!
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
    print "Strange result with name:" + name

print str(total_names) + " total names checked"
print str(names_taken) + " were taken"
print str(names_suspended) + " were suspended. (unusable)"
print str(names_available) + " were available."
if names_available > 0:
  print "They are: " + str(available_names)[1:-1]

