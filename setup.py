from distutils.core import setup
from access_niu.about import __version__, __license__

setup(
    name="access-niu",
    version=__version__,
    packages=["access_niu"],
    license=__license__,
    long_description=open("README.md").read(),
    install_requires=[
        "keras==2.2.4",
        "numpy==1.16.2",
        "scikit-learn==0.20.3",
        "tensorflow==1.13.1",
        "pillow==6.0.0",
        "h5py==2.9.0",
        "black",
        "gunicorn==19.9.0",
        "flask==1.0.2",
    ],
)
