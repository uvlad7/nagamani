#!/usr/bin/env ruby

require 'fiddle'
require 'fiddle/import'
require 'json'

$is_windows = Gem.win_platform?

def linked_libruby
  $is_windows ? linked_libruby_windows : linked_libruby_unix
end

def executable
  File.join(
    RbConfig::CONFIG['bindir'],
    "#{RbConfig::CONFIG['ruby_install_name']}#{RbConfig::CONFIG['EXEEXT']}"
  )
end

Dl_info = Fiddle::Importer.struct [
  'char* dli_fname',
  'void* dli_fbase',
  'char* dli_sname',
  'void* dli_saddr',
]

private

def linked_libruby_unix
  curr_process = Fiddle.dlopen(nil)
  dladdr = Fiddle::Function.new(
    curr_process['dladdr'],
    [Fiddle::TYPE_VOIDP, Fiddle::TYPE_VOIDP],
    Fiddle::TYPE_INT
  )

  dlinfo = Dl_info.malloc
  retcode = dladdr.call(
    Fiddle::Pointer.new(curr_process['ruby_show_version']),
    dlinfo
  )
  return nil if retcode == 0 # means error

  fname = dlinfo.dli_fname.to_s
  # If it's not a shared library
  # it can be 'ruby' or 'irb' or whatever you use to call ruby from the shell
  # https://stackoverflow.com/a/41627181/13500870
  return nil unless File.exist?(fname)

  path = File.realpath(fname)
  path unless path == File.realpath(executable)
end

def linked_libruby_windows
  raise NotImplementedError, 'Windows is not supported'
end

begin
  puts JSON.pretty_generate(
    executable: executable,
    linked_libruby: linked_libruby,
  )
rescue Exception => exception
  abort "#{exception.class}: #{exception.message}"
end
