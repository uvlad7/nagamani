#!/usr/bin/env bash
# https://github.com/rbenv/ruby-build
# RUBY_CONFIGURE_OPTS="--enable-shared" rtx install ruby 2.3.7
# RUBY_CONFIGURE_OPTS="--disable-shared" rtx install ruby 2.7.7
for ruby_path in $(rtx list ruby --json | jq -cr .[].install_path); do
    $ruby_path/bin/ruby investigator.rb
done

# https://github.com/pyenv/pyenv/tree/master/plugins/python-build
# CONFIGURE_OPTS='--disable-shared' rtx install python 3.6.15
for python_path in $(rtx list python --prefix 3 --json | jq -cr .[].install_path); do
    $python_path/bin/python investigator.py
done
