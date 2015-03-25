from distutils.core import setup

setup(
  name='Romano',
  version='0.2.0',
  author='Eleazar Meza',
  author_email='meza.eleazar@gmail.com',
  packages=['romano'],
  url='http://agromatic.com.ve/',
  license='LICENSE.txt',
  description='Weighbridge management software for Mango',
  long_description=open('README.txt').read(),
  install_requires=['pyside', 'simplejson', 'serial'],
)
