r"""
This Python 3.3 module implements a wrapper for map projections.

CHANGELOG:

- Alexander Raichev (AR), 2013-01-25: Refactored code from release 0.3.
- AR, 2013-07-23: Ported to Python 3.3.

NOTE:

All lengths are measured in meters and all angles are measured in radians 
unless indicated otherwise. 
By 'ellipsoid' below, i mean an oblate ellipsoid of revolution.
"""
#*****************************************************************************
#       Copyright (C) 2013 Alexander Raichev <alex.raichev@gmail.com>
#
#  Distributed under the terms of the GNU Lesser General Public License (LGPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

# Import third-party modules.
import pyproj
# Import standard modules.
import importlib
# Import my modules.
from utils import my_round, wrap_longitude, wrap_latitude
from ellipsoids import WGS84_ELLIPSOID


# Homemade map projections, as opposed to those in the PROJ.4 library.
# Remove 'healpix' and 'rhealpix' to use the PROJ.4 versions instead,
# assuming you have the *correct/patched* PROJ.4 versions.
HOMEMADE_PROJECTIONS = {'healpix', 'rhealpix', 'isea', 'csea', 'qsc'}    
    
class Proj(object):
    r"""
    Represents a map projection of a given ellipsoid.
    
    INSTANCE ATTRIBUTES:
    
    - `ellipsoid` - An ellipsoid (Ellipsoid instance) to project.
    - `proj` - The name (string) of the map projection, either a valid PROJ.4 
      projection name or a valid homemade projection name.
    - `kwargs` - Keyword arguments (dictionary) needed for the projection's 
      definition, but not for the definition of the ellipsoid.  For example, 
      these could be {'north_square':1, 'south_square': 2} for the rhealpix 
      projection. 
    
    EXAMPLES::

        >>> from ellipsoids import WGS84_ELLIPSOID    
        >>> f = Proj(ellipsoid=WGS84_ELLIPSOID, proj='rhealpix', north_square=1, south_square=0)
        >>> print(my_round(f(0, 30), 15))
        (0.0, 3748655.1150495014)
        >>> f = Proj(ellipsoid=WGS84_ELLIPSOID, proj='cea')
        >>> print(my_round(f(0, 30), 15))
        (0.0, 3180183.485774971)
        
    NOTES:
    
    When accessing a homemade map projection assume that it can be called via
    a function g(a, e), where a is the major radius of the ellipsoid to be 
    projected and e is its eccentricity.
    The output of g should be a function object of the form 
    f(u, v, radians=False, inverse=False).
    For example, see the healpix() function in ``pj_healpix.py``.
    """
    def __init__(self, ellipsoid=WGS84_ELLIPSOID, proj=None, **kwargs):
        self.proj = proj
        # Keyword arguments related to the projection but not to its
        # underlying ellipsoid, e.g. for rhealpix these could be
        # {'north_square':1, 'south_square': 2}:
        self.kwargs = kwargs 
        self.ellipsoid = ellipsoid
        
    def __str__(self):
        result = ['map projection:']
        result.append('    proj = %s' % self.proj)
        result.append('    kwargs = %s' % self.kwargs)
        result.append('    ellipsoid:')
        for (k, v) in sorted(self.ellipsoid.__dict__.items()):
            result.append(' '*8 + k + ' = ' + str(v))
        return "\n".join(result)        
    
    def __call__(self, u, v, inverse=False):
        ellipsoid = self.ellipsoid
        proj = self.proj
        kwargs = self.kwargs
        lon_0 = ellipsoid.lon_0
        lat_0 = ellipsoid.lat_0
        radians = ellipsoid.radians
        a = ellipsoid.a
        e = ellipsoid.e
        if proj in HOMEMADE_PROJECTIONS:
            try:
                # Import projection module for proj.
                module = importlib.import_module('pj_' + proj)
                f = getattr(module, proj)(a=a, e=e, **kwargs)
            except NameError:
                print('Oops! Projection %s is not implemented.' % proj)
                return
        else:
            # Use a projection from the PROJ.4 library.
            f = pyproj.Proj(proj=proj, a=a, e=e, **kwargs)
        if not inverse:
            # Translate longitudes and latitudes so that 
            # (lon_0, lat_0) maps to (0, 0) in the plane.
            lam = wrap_longitude(u - lon_0, radians=radians)
            phi = wrap_latitude(v - lat_0, radians=radians)
            return f(lam, phi, radians=radians)
        else:    
            lam, phi = f(u, v, radians=radians, inverse=True)
            # Translate longitudes and latitudes so that 
            # (0, 0) in the plane maps to (lon_0, lat_0) on the ellipsoid.
            lam = wrap_longitude(lam + lon_0, radians=radians)
            phi = wrap_latitude(phi + lat_0, radians=radians)
            return lam, phi