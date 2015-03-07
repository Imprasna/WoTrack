from setuptools import setup

setup(
    name='spotify',
    version='0.0.1',
    description='RESTFUL client for Spotify',
    url='http://github.com/husman/wotrack',
    author='Haleeq Usman',
    author_email='cusman1987@gmail.com',
    license='MIT',
    packages=['spotify'],
    install_requires=[
        'requests==2.5.3',
        'python-memcached==1.53',
    ],
    zip_safe=False
)