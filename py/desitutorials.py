#- Utility code that is specific to DESI tutorials,
#- but also useful across multiple tutorials.

from __future__ import absolute_import, division, print_function

_standard_repos = [
    'numpy', 'scipy', 'astropy', 'yaml', 'matplotlib',
    'requests', 'fitsio', 'h5py', 'healpy', 'psycopg2',
    'desiutil', 'desispec', 'desitarget', 'desimodel', 'desisim',
    'desisurvey', 'surveysim',
    'redrock', 'specter', 'speclite', 'specsim',
]

def get_code_versions(module_names=None):
    '''
    Returns a dict of ver[package] = code_version for loaded DESI code

    Note: similar to desiutil.depend.add_dependencies
    '''
    import sys
    import importlib
    import collections

    if module_names is None:
        module_names = _standard_repos

    versions = collections.OrderedDict()
    versions['python'] = ".".join(map(str, sys.version_info[0:3]))
    for module in module_names:
        if module in sys.modules:
            # already loaded, but we need a reference to the module object
            x = importlib.import_module(module)
            if hasattr(x, '__version__'):
                versions[module] = x.__version__
            elif hasattr(x, '__path__'):
                # e.g. redmonster doesn't set __version__
                versions[module] = 'unknown ({})'.format(x.__path__[0])
            elif hasattr(x, '__file__'):
                versions[module] = 'unknown ({})'.format(x.__file__)
            else:
                versions[module] = 'unknown'

    return versions

def print_code_versions(module_names=None):
    '''
    print code versions for loaded desi code
    '''
    for module, version in get_code_versions(module_names).items():
        print('{:12s}: {}'.format(module, version))
