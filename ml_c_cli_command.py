#!/usr/bin/env python2
#-*- coding: UTF-8 -*-
"""
CLI Command module
"""

import cmd
import os

class cli_command(cmd.Cmd):
    """ cli_command """

    prompt = "SLB: "
    intro = ""
    # online help config
    doc_header = "Available commands (type help <topic>): "
    ruler = "="

    def help_help(self):
        """ define help online help """
        print '\n'.join([ "help or ? [command]",
                          "    Show a or all command document"])

    def help_network(self):
        """ define network information online help """
        print '\n'.join([ "network [interface]",
                          "    Show network interface information"])

    def do_network(self, interface):
        """ show network information """
        print os.popen("ip addr show " + interface).read()
        #print os.popen("ipconfig " + interface).read()

    def complete_network(self, text, line, begidx, endidx):
        """ auto completion for network """
        return ["eth0"];

    def help_exit(self):
        """ define exit online help """
        print '\n'.join([ "exit",
                          "    Quit the command line system"])

    def do_exit(self, line):
        """ exit """
        return True

    #def help_EOF(self):
    #    """ define exit online help """
    #    print '\n'.join([ "Ctrl-D",
    #                      "    Quit the command line system"])

    #def do_EOF(self, line):
    #    """ exit """
    #    return True

if __name__ == '__main__':
    cli_command().cmdloop()
