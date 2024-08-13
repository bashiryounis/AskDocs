from setuptools import setup

packages = []
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
    name="QA_AP",
    version="0.0.3",
    description="QA Repository Service",
    url="https://gitlab.com/xnalabs/xchain",
    author="demo",
    author_email="demo@demo.ai",
    include_package_data=True,
    install_requires=requirements,
    packages=packages,
    zip_safe=False
)
