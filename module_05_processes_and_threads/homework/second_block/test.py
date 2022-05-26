import signal

from flask import Flask, request
import subprocess
import shlex
import os

app = Flask(__name__)


def check_port_and_run(port: str):
    result = subprocess.run(shlex.split(f'lsof -i :{port}'), capture_output=True)
    if result.stdout == b'':
        return True
    process_list = result.stdout.decode('utf-8').splitlines()
    pid_num = process_list[0].split().index('PID')
    for process in process_list[1:]:
        os.kill(int(process.split()[pid_num]), signal.SIGKILL)
    return True
    pass


if __name__ == "__main__":
    check_port_and_run('5000')
    app.run(debug=True)
