from setuptools import setup

setup(
    install_requires=["requests", "slackclient", "python-dotenv"],
    entry_points={
        "console_scripts": [
            "daily-report = app:app"
        ]
    }
)