#!/usr/bin/env python2
import os
import sys

def main():
    try:
        input_file_name = sys.argv[1]
    except IndexError:
        print 'No file name supplied.'
        return

    state = None
    program_lines = []
    try:
        with open(input_file_name) as file_input:
            program_lines = [line.split(' ') for line in file_input]
    except IOError:
        print 'No such file exists.'

    state = program_lines[0]
    urm = URM(state, program_lines[1:])
    urm.execute()


class URM():
    def __init__(self, initial_state, lines):
        self.state = [int(x) for x in initial_state]
        self.lines = lines
        self.method_map = {'S': self.S, 'Z': self.Z, 'J': self.J, 'C': self.C}
        self.next_line = 1

    def execute(self):
        len_lines = len(self.lines)
        file_name = sys.argv[1].replace('.in', '.out')
        try:
            os.remove(file_name)
        except OSError:
            pass
        f = open(file_name, 'w')
        f.write(' '.join(str(x) for x in self.state))
        f.write(os.linesep)
        while self.next_line <= len_lines:
            line = self.lines[self.next_line - 1]
            self.method_map[line[0]](line[1:])
            f.write(' '.join(str(x) for x in self.state))
            f.write(os.linesep)
        f.close()

    def S(self, index):
        index = int(index[0])
        self.state[index] = self.state[index] + 1
        self.next_line = self.next_line + 1

    def Z(self, index):
        index = int(index[0])
        self.state[index] = 0
        self.next_line = self.next_line + 1

    def J(self, args):
        index1, index2, next_line = [int(x) for x in args]
        if self.state[index1] == self.state[index2]:
            self.next_line = next_line
        else:
            self.next_line = self.next_line + 1

    def C(self, args):
        index1, index2 = [int(x) for x in args]
        self.state[index2] = self.state[index1]
        self.next_line = self.next_line + 1


if __name__ == '__main__':
    main()
