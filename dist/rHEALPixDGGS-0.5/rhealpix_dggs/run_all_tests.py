# Run all test scripts and doctests.
import unittest, doctest, importlib

module_names = [
  'utils',
  'pj_healpix',
  'pj_rhealpix',
  'ellipsoids',
  'projection_wrapper',
  'rhealpix_dggs',
  'distortion',
]

# Run tests
suite = unittest.TestSuite()
for name in module_names:
    t = 'tests.test_' + name
    try:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    except (ImportError, AttributeError):
        print("Couldn't find tests for module %s" % m)
        continue        
unittest.TextTestRunner().run(suite)

# Run doctests
for name in module_names:
    m = importlib.import_module(name)
    doctest.testmod(m)