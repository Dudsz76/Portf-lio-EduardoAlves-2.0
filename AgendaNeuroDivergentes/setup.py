from setuptools import setup, find_packages

setup(
    name="flow-agenda",
    version="1.0.0",
    author="Eduardo Alves",
    author_email="oliveiradudu76@gmail.com",
    description="Aplicativo de agenda para pessoas neurodivergentes",
    packages=find_packages(),
    install_requires=["PyQt6>=6.6.0"],
    python_requires=">=3.10",
)