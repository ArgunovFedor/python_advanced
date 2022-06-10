import sys

from module_05_processes_and_threads.homework.third_block.test_context_manager import TestContextManager

file = open('file.txt', 'w')
with TestContextManager(file) as file:
    print('Print to stdout')
    print('Print to stderr', file=sys.stderr)
    10 * 1 / 0
file.close()
