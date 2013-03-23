Twitter Name Finder
===================

This short python script will look for available unclaimed twitter handles.

```
Usage: get_names.py [--brute N] [--dict FILE] [--out FILE]
  --brute N                Tries all possible names of length N
  --dict FILE              Tries names listed in the given file
  --out FILE               Stores all available names in the given file

Either --brute or --dict MUST be specified.
```

The dictionary file should be a newline-separated list of words. The 
output file follows the same format. The characters using in brute 
forcing are a-z, 0-9, and _.

