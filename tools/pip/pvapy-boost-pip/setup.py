from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
import os
import platform
import fnmatch

DEFAULT_BOOST_VERSION = '1.67.0'
MODULE_NAME = 'pvapy-boost'
MODULE = Extension(MODULE_NAME, [])
PLATFORM = platform.uname()[0].lower()
BUILD_SCRIPT = './build.%s.sh' % PLATFORM
DEPLOY_CONF = os.environ.get('DEPLOY_CONF', 'non_existent_file')

def get_env_var(name, default):
    value = os.environ.get(name)
    if value is not None:
        return value

    if os.path.exists(DEPLOY_CONF):
        vars = open(DEPLOY_CONF).read().split()
        for v in vars:
            key = v.split('=')[0].strip()
            value = v.split('=')[1].strip()
            if key == name:
                return value
    return default

def find_files(rootDir='.', pattern='*'):
    result = []
    for root, dirs, files in os.walk(rootDir):
      for f in fnmatch.filter(files, pattern):
          result.append(os.path.join(root, f))
    return result

class BuildExt(build_ext):
  def build_extension(self, ext):
    print('Building %s' % MODULE_NAME)
    os.system(BUILD_SCRIPT)

MODULE_VERSION = get_env_var('BOOST_VERSION', DEFAULT_BOOST_VERSION)
MODULE_FILES = map(lambda f: f.replace('%s/' % MODULE_NAME, ''), find_files(MODULE_NAME))

setup(
  name = MODULE_NAME,
  version = MODULE_VERSION,
  packages = [MODULE_NAME],
  package_data = {
    MODULE_NAME : MODULE_FILES, 
  },
  ext_modules=[MODULE],
  cmdclass = {'build_ext': BuildExt}
)
