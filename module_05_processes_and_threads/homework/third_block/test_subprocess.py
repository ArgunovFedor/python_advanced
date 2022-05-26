import subprocess
import sys
import time

if __name__ == "__main__":
    start = time.time()
    my_process_list = list()
    for pnum in range(5):
        p = subprocess.Popen(['python', 'test_program.py'],
                             stdin=sys.stdin,
                             stderr=sys.stderr,
                             stdout=sys.stdout)
        my_process_list.append(p)
        print('Process number {} started. PID: {}'.format(
            pnum, p.pid
        ))
    for proc in my_process_list:
        proc.wait(timeout=5)
        if proc.returncode == 0:
            print('Process with PID {} ended successfully'.format(proc.pid))

    print('Done in {}'.format(time.time() - start))
