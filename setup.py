from setuptools import setup
from setuptools.extension import Extension

setup(
    name = "piCircuit",
    version = "1.0.0",
    author = "Juan Barbosa",
    author_email = "js.barbosa10@uniandes.edu.co",
    description = ('RaspberryPi based circuit.'),
    license = "GPL",
    keywords = "example documentation tutorial",
    packages=['piCircuit'],
    install_requires=["pyserial"],
    ext_modules = [],
    long_description="https://github.com/jsbarbosa/astrohut/",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    headers = [],
    include_package_data = True,
)
