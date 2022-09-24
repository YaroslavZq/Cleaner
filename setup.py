from setuptools import setup

setup(name='clean',
      version='1.3',
      description='Code clean and sort files in directory that you give',
      author='YaroslavZq',
      author_email='svyatikua2@gmail.com',
      url='https://github.com/YaroslavZq/Cleaner',
      packages=['clean_folder'],
      install_requires=['transliterate'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
      )
