'''
This is the file for prototyping application functionality.
Comments indicate expected user input and application behavior,
tested by the code.
'''

# Django can connect to the database

# User loads home page and finds login prompt

# Prominent button/link to add a new object (A)

# Other links on page: view/edit existing object, (B)
# add/edit log (future implementation).

# (A) add new object form

# First field in form is photo upload;
# not meant to be a display picture, but rather an ainde-mémoire
# to let the staff locate the object more easily.

# Agent model is foreign key, allowing new entries to be
# added on the fly during object entry.
# Figure out validation scheme for existing agents.

# Date is also a foreign key model, similar to above.

# Upon saving a new or updated object, the system exports a
# YAML file with the complete text contents of the entry
# (and possibly the image filenames?).

# If possible or desired,
# this exported file ought to be pushed to a specific branch
# of a git repository. This might help:
# http://stackoverflow.com/questions/15315573/how-can-i-call-git-pull-from-within-python
