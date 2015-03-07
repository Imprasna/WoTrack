import sys
from invoke import task as invoke_task, run


use_pty = sys.stdin.isatty()

@invoke_task
def tests():
    print 'Running Spotify Client tests...'
    run('cd packages/spotify/spotify; time nosetests --rednose --nologcapture tests', pty=use_pty)

    print 'Running Application tests...'
    run('time nosetests --rednose --nologcapture tests', pty=use_pty)

