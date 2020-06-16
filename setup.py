from setuptools import setup

setup(
    install_requires=["requests", "slackclient", "python-dotenv", "numpy", "matplotlib", "japanize_matplotlib"],
    entry_points={
        "console_scripts": [
            "daily-report = app:app"
        ]
    }
)