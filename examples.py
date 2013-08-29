from ribbon import Ribbon, RibbonExecutionException

# Take any command line tool.
# Let's start with `ls` and how to build command lines:

ls = Ribbon('ls')

# Pass positional args:
print ls.build_cmd_str() # ls
print ls.build_cmd_str('-a') # ls -a
print ls.build_cmd_str('.', '-a') # ls . -a

# Keyword args:
print ls.build_cmd_str(a=True) # ls -a
print ls.build_cmd_str(a=False) # ls
print ls.build_cmd_str('.', a=True) # ls . -a

# Execute command
print ls.getoutput()
# LICENSE
# README.md
# examples.py
# ribbon.py
# ribbon.pyc
# test_ribbon.py

print ls.getoutput(a=True, l=True)
# total 88
# drwxr-xr-x  10 valiev  staff    340 Aug 30 01:23 .bit_lengthdrwxr-xr-x  11
# valiev  staff    374 Aug 29 00:04 ..
# -rw-r--r--   1 valiev  staff  12288 Aug 30 01:23 .examples.py.swp
# drwxr-xr-x  13 valiev  staff    442 Aug 30 01:23 .git
# -rw-r--r--   1 valiev  staff   1080 Aug 29 00:04 LICENSE
# -rw-r--r--   1 valiev  staff    177 Aug 30 01:03 README.md
# -rw-r--r--   1 valiev  staff    589 Aug 30 01:23 examples.py
# -rw-r--r--   1 valiev  staff   4272 Aug 30 01:21 ribbon.py
# -rw-r--r--   1 valiev  staff   5891 Aug 30 01:21 ribbon.pyc
# -rw-r--r--   1 valiev  staff     28 Aug 30 01:06 test_ribbon.py

print ls.getoutput(a=True, l=True, h=True)
# total 88
# drwxr-xr-x  10 valiev  staff   340B Aug 30 01:24 .bit_lengthdrwxr-xr-x  11
# valiev  staff   374B Aug 29 00:04 ..
# -rw-r--r--   1 valiev  staff    12K Aug 30 01:24 .examples.py.swp
# drwxr-xr-x  13 valiev  staff   442B Aug 30 01:23 .git
# -rw-r--r--   1 valiev  staff   1.1K Aug 29 00:04 LICENSE
# -rw-r--r--   1 valiev  staff   177B Aug 30 01:03 README.md
# -rw-r--r--   1 valiev  staff   1.2K Aug 30 01:24 examples.py
# -rw-r--r--   1 valiev  staff   4.2K Aug 30 01:21 ribbon.py
# -rw-r--r--   1 valiev  staff   5.8K Aug 30 01:21 ribbon.pyc
# -rw-r--r--   1 valiev  staff    28B Aug 30 01:06 test_ribbon.py

# Execute command with non-zero exit code:
try:
    ls.getoutput(test=True)
except RibbonExecutionException, e:
    print str(e) # 'ls --test' returned 1 exit code

# Get exit code:
print ls.system(test=True) # 1

# Don't want to check exit code, just execute:
try:
    ls.system_exc(test=True)
except RibbonExecutionException, e:
    print str(e) # 'ls --test' returned 1 exit code

# Grab exit code and output
print ls.getstatusoutput(test=True) # (1, '')
print ls.getstatusoutput(a=True) # (0, '.\n..\n.examples.py.swp\n.git\nLICENSE\nREADME.md\nexamples.py\nribbon.py\nribbon.pyc\ntest_ribbon.py\n')
