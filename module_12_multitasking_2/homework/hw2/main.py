import subprocess


def process_count(username: str) -> int:
    # количество процессов, запущенных из-под
    # текущего пользователя username
    res = subprocess.run(['ps', '-u', username])
    return len(res.stdout.splitlines()) - 2


def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    res = subprocess.run(['ps', '-aux', '--sort', '-rss'])
    return len(res.stdout.splitlines()) - 2


process_count('fargunov')
total_memory_usage()
