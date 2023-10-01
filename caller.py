#!/usr/bin/env python

import ctypes


rb_value = ctypes.c_ulong
c_char_p = ctypes.POINTER(ctypes.c_char)
c_char_p_p = ctypes.POINTER(c_char_p)


def rb_call():
    libruby = ctypes.CDLL(
        "/home/vladimir/.local/share/rtx/installs/ruby/3.2.2/lib/libruby.so.3.2.2"
    )
    # we need ruby_init_stack somehow
    libruby.ruby_options.argtypes = [ctypes.c_int, c_char_p_p]
    libruby.ruby_options.restype = ctypes.c_void_p

    libruby.ruby_init.argtypes = []
    libruby.ruby_init.restype = None
    libruby.ruby_init_loadpath.argtypes = []
    libruby.ruby_init_loadpath.restype = None
    libruby.rb_load_file.argtypes = [ctypes.c_char_p]
    libruby.rb_load_file.restype = ctypes.c_void_p
    libruby.ruby_exec_node.argtypes = [ctypes.c_void_p]
    libruby.ruby_exec_node.restype = ctypes.c_int
    libruby.ruby_run_node.argtypes = [ctypes.c_void_p]
    libruby.ruby_run_node.restype = ctypes.c_int
    libruby.ruby_cleanup.argtypes = [ctypes.c_int]
    libruby.ruby_cleanup.restype = ctypes.c_int
    libruby.rb_eval_string_protect.argtypes = [
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_int),
    ]
    libruby.rb_eval_string_protect.restype = rb_value

    argv = (c_char_p * 2)()
    argv[0] = ctypes.create_string_buffer(b"nagamani")
    argv[1] = ctypes.create_string_buffer(b"hello.rb")
    libruby.ruby_init()
    retval = libruby.ruby_run_node(libruby.ruby_options(2, argv))
    exit(retval)
    # libruby.ruby_init()
    # libruby.ruby_init_loadpath()
    # # node = libruby.rb_load_file(ctypes.c_char_p(b"/home/vladimir/nagamani/hello.rb"))
    # # state = libruby.ruby_exec_node(node)
    # state = ctypes.c_int(0)
    # # I dont actually care about the return value here
    # libruby.rb_eval_string_protect(
    #     ctypes.c_char_p(b"""
    #                     require 'paint'
    #                     puts 'Hello from Ruby!'
    #                     """), ctypes.pointer(state)
    # )
    # libruby.ruby_cleanup(state)


rb_call()
