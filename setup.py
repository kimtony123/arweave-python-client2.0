from distutils.core import setup

setup(
  name="arweave-python-client2.0",
  packages = ['arweave'], # this must be the same as the name above
  version="1.0.15.dev0",
  description="Client interface for sending transactions on the Arweave permaweb",
  author="Tony Kim",
  author_email="antonyk139@gmail.com",
  url="https://protocol.land/#/repository/276b6f76-2149-4cb7-a00a-9e08d91c2786",
  keywords=['arweave', 'crypto'],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires=[
    'arrow',
    'python-jose',
    'pynacl',
    'pycryptodome',
    'cryptography',
    'requests',
    'psutil'
  ],
)
