#!/usr/bin/env ruby

require 'fiddle'

def py_call
  libpython = Fiddle.dlopen(
    '/home/vladimir/.local/share/rtx/installs/python/3.11.5/lib/libpython3.11.so'
  )
  py_bytes_main = Fiddle::Function.new(
    libpython['Py_BytesMain'],
    [Fiddle::TYPE_INT, Fiddle::TYPE_VOIDP],
    Fiddle::TYPE_INT
  )

  argv = Fiddle::Pointer.malloc(Fiddle::SIZEOF_VOIDP * 2, Fiddle::RUBY_FREE)
  argv[0, Fiddle::SIZEOF_VOIDP] = create_string_buffer('nagamani').ref
  argv[Fiddle::SIZEOF_VOIDP, Fiddle::SIZEOF_VOIDP] = create_string_buffer('hello.py').ref
  retval = py_bytes_main.call(2, argv)
  exit(retval)
end

private

def create_string_buffer(string)
  # Not just Fiddle::Pointer[string], because it's not intended to be modified
  # (stores a pointer to the original Ruby string, just like ctypes.c_char_p(string))
  bytesize = string.bytesize
  buffer = Fiddle::Pointer.malloc(bytesize + 1, Fiddle::RUBY_FREE)
  buffer[0, bytesize] = string
  # Already filled with NUL bytes, so no need to explicitly set buffer[bytesize] = 0
  buffer
end

py_call
