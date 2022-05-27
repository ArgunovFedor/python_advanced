import subprocess


def run_program():
    res = subprocess.run(['python', 'test_program.py'], encoding='utf-8', input='первый ввод\nвторой ввод\nтретий ввод')
    print(res)

if __name__ == '__main__':
    run_program()
