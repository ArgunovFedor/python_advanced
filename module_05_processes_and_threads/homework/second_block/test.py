import signal

from flask import Flask
import subprocess
import shlex
import os

app = Flask(__name__)


@app.endpoint('test')
def test_endpoint():
    return 'Test endpoint was called!'


def check_port_and_run(port: str):
    result = subprocess.run(shlex.split(f'lsof -i :{port}'), capture_output=True)
    if result.stdout == b'':
        return True
    process_list = result.stdout.decode('utf-8').splitlines()
    pid_num = process_list[0].split().index('PID')
    for process in process_list[1:]:
        os.kill(int(process.split()[pid_num]), signal.SIGKILL)


if __name__ == "__main__":
    print('Убиваем процессы по порту 5000')
    check_port_and_run('5000')
    result = app.run()