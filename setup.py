from setuptools import setup

setup(name='rtcm_decode',
      version='0.0',
      description='decode rtcm',
      author='swiftnav',
      packages=['rtcm_decode', 'rtcm_decode.drivers'],
      install_requires=[
            'crc ==4.1.0',
            'bitarray ==2.7.2'
            ]
     )