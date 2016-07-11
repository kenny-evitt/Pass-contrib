#!/usr/bin/env python
# vim:fileencoding=utf-8

# This was tested with a "Plain Text (tab separated)" export file created by Password Safe verion "V3.31 (5298)" on Windows.



import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()


import csv
from subprocess import call
import os



# The following function was copied (but renamed) from [this answer](http://stackoverflow.com/a/35857/173497) to the following Stack Overflow question:
#
# - [shell - How to escape os.system() calls in Python? - Stack Overflow](http://stackoverflow.com/questions/35817/how-to-escape-os-system-calls-in-python)

def bashquote(s):
    return "'" + s.replace("'", "'\\''") + "'"



with open(args.file, 'r') as file:

    next(file) # Skip header row
    reader = csv.reader(file, delimiter='\t')


    for row in reader:

        ( group_title, username, passwd, url, auto_type, created, passwd_modified, last_access, passwd_expiry_date, passwd_expiry_interval, entry_modified, passwd_policy, passwd_policy_name, history, run_command, dca, shift_dca, email, protected, symbols, notes ) = row

        # Encode forward slashes and colons (and percent signs)
        group_title = group_title.replace('%', '%%')
        group_title = group_title.replace('/', '%2F')
        group_title = group_title.replace(':', '%3A')
        group_title = group_title.replace('*', '%2A')

        group_title = group_title.replace('.', '/')
        group_title = group_title.replace('»', '.')

        notes = notes.replace('»', '\n')


        entry = "{}\n".format(passwd)

        if username:           entry = "{}{}{}\n".format(entry, "Username: ", username)
        if url:                entry = "{}{}{}\n".format(entry, "URL: ", url)
        if email:              entry = "{}{}{}\n".format(entry, "Email: ", email)
        if symbols:            entry = "{}{}{}\n".format(entry, "Symbols: ", symbols)
        if created:            entry = "{}{}{}\n".format(entry, "Created time (Password Safe): ", created)
        if passwd_modified:    entry = "{}{}{}\n".format(entry, "Password last modified time (Password Safe): ", passwd_modified)
        if entry_modified:     entry = "{}{}{}\n".format(entry, "Entry last modified time (Password Safe): ", entry_modified)

        #if passwd_policy:      entry = "{}{}{}\n".format(entry, "Password policy (Password Safe): ", passwd_policy)
        #if passwd_policy_name: entry = "{}{}{}\n".format(entry, "Password policy name (Password Safe): ", passwd_policy_name)

        #if history:            entry = "{}{}{}\n".format(entry, "History: ", history)

        if notes:              entry = "{}{}{}\n".format(entry, "Notes:\n\n", notes)


        print "Adding entry for {}:".format(group_title)

        bash_command = "echo -e {} | pass insert --multiline --force {}".format( bashquote(entry), bashquote(group_title) )

        # The `stdout` argument effectively hides it from being printed when the script is run
        return_code = call(bash_command, executable='/bin/bash', stdout=open(os.devnull, 'wb'), shell=True)


        if return_code == 0:
            print "Added!"
        else:
            print "Failed to add!"
