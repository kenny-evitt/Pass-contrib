#!/usr/bin/env bash
# pwsafe-to-pass.bash – Migrate passwords from a pwSafe 1 export file to Pass.
# Copyright © 2016 Kenny Evitt <kenny.evitt@gmail.com>. All rights reserved. 
#
# Based on *pwsafe2pass.sh* by Tom Hendrikx
# Copyright (C) 2013 Tom Hendrikx <tom@whyscream.net>. All Rights Reserved.
#
# This file is licensed under the GPLv2+. Please see COPYING for more information.
#
#
# Usage:
#
#     pwsafe-to-pass.bash pwsafe_export_file

export=$1

IFS="	" # tab character
cat "$export" | while read group_title username passwd url created passwd_modified entry_modified passwd_policy passwd_policy_name email symbols notes; do
    test "$group_title" = "Group/Title" && continue

    group_title="${group_title//.//}"
    group_title="${group_title//»/.}"

    notes="$(echo $notes | cut -d'"' -f2)"

    entry="$passwd\n"
    test -n "$username" && entry="${entry}Username: $username\n"
    test -n "$passwd" && entry="${entry}Password: $passwd\n"
    test -n "$url" && entry="${entry}URL: $url\n"
    test -n "$email" && entry="${entry}Email: $email\n"
    test -n "$symbols" && entry="${entry}Symbols (pwSafe data): $symbols\n"
    test -n "$created" && entry="${entry}Created time: $created\n"
    test -n "$passwd_modified" && entry="${entry}Password last modified time: $passwd_modified\n"
    test -n "$entry_modified" && entry="${entry}Entry last modified time: $entry_modified\n"
    test -n "$passwd_policy" && entry="${entry}Password policy (pwSafe data): $passwd_policy\n"
    test -n "$passwd_policy_name" && entry="${entry}Password policy name (pwSafe data): $passwd_policy_name\n"

    test -n "$notes" && entry="${entry}Notes:\n$notes\n"


    echo Adding entry for $group_title:
    echo -e $entry | pass insert --multiline --force "$group_title"

    if test $?; then
        echo Added!
    else
        echo Failed to add!
    fi
done
