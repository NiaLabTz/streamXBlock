"""Setup for streamXBlock."""

import os
from setuptools import setup


def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='stream-xblock',
    version='0.1',
    description='XBlock to use the stream player in edX, instead of the default one.',
    packages=[
        'stream',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'stream = stream:streamXBlock',
        ]
    },
    package_data=package_data("stream", "static"),
)
