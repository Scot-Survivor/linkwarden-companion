from setuptools import setup

setup(
    name='linkwarden-companion',
    version='0.1.0',
    py_modules=['linkwarden_companion'],
    install_requires=[
        'Click',
        'requests',
        'pydantic'
    ],
    entry_points={
        'console_scripts': [
            'linkwarden-companion=linkwarden_companion.cli:main',
        ],
    }

)
