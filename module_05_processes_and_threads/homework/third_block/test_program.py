from module_05_processes_and_threads.homework.third_block.test_context_manager import TestContextManager

with TestContextManager(open('test_input.txt', 'r')) as file:
    print(file.read())