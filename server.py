# Created by zhouwang on 2020/11/13.

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(PROJECT_DIR, 'venv')


def start():
    print('#### start\n')
    os.system(f'rm -rf {PROJECT_DIR}/static && \cp -rf {PROJECT_DIR}/ui/dist/static {PROJECT_DIR}/static')
    os.system(f'\cp -rf {PROJECT_DIR}/ui/dist/index.html {PROJECT_DIR}/templates/index.html')
    os.system(f'source {VENV_DIR}/bin/activate && '
              f'pip install -r {PROJECT_DIR}/requirements.txt')
    status = os.system(f'source {VENV_DIR}/bin/activate && cd {PROJECT_DIR} &&'
                       f'uwsgi --ini {PROJECT_DIR}/uwsgi_socket.ini')
    print('#### start %s\n' % ('successful' if status == 0 else 'fail'))


def restart():
    print('#### restart\n')
    os.system(f'rm -rf {PROJECT_DIR}/static && \cp -rf {PROJECT_DIR}/ui/dist/static {PROJECT_DIR}/static')
    os.system(f'\cp -rf {PROJECT_DIR}/ui/dist/index.html {PROJECT_DIR}/templates/index.html')
    os.system(f'source {VENV_DIR}/bin/activate && '
              f'pip install -r {PROJECT_DIR}/requirements.txt')
    status = os.system(f'source {VENV_DIR}/bin/activate && uwsgi --reload /var/run/dormer-web-uwsgi.pid')
    print('#### restart %s\n' % ('successful' if status == 0 else 'fail'))


def stop():
    print('#### stop\n')
    status = os.system(f'source {VENV_DIR}/bin/activate && uwsgi --stop /var/run/dormer-web-uwsgi.pid')
    print('#### stop %s\n' % ('successful' if status == 0 else 'fail'))


def build():
    print('#### build\n')
    status = os.system(f'cd {PROJECT_DIR}/ui && npm install && npm run build')
    print('#### build %s\n' % ('successful' if status == 0 else 'fail'))


def migrate():
    print('#### migrate\n')
    status = os.system(f'source {VENV_DIR}/bin/activate && python {PROJECT_DIR}/manage.py migrate')
    print('#### migrate %s\n' % ('successful' if status == 0 else 'fail'))


def venv():
    if not os.path.isdir(VENV_DIR):
        status = os.system(f'cd {PROJECT_DIR} && python3 -m venv venv')
        print('#### venv %s\n' % ('successful' if status == 0 else 'fail'))


def init():
    venv()


def main():
    init()

    argv = sys.argv
    if argv[1] == 'start':
        start()
    elif argv[1] == 'stop':
        stop()
    elif argv[1] == 'restart':
        restart()
    elif argv[1] == 'build':
        build()
    elif argv[1] == 'migrate':
        migrate()

if __name__ == '__main__':
    main()
