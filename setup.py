from setuptools import find_namespace_packages
from setuptools import setup
from access_niu.about import __version__, __license__

setup(
    name="access-niu",
    classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries",
        ],
    author="ConvexHull Technology Private Limited",
    author_email="connect@accessai.co",
    maintainer="Majeed Khan",
    maintainer_email="majeed.khan@accessai.co",
    version=__version__,
    packages= find_namespace_packages(exclude=["sample", "tests"]),
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
