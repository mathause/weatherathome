

import os
import glob
import copy

import numpy as np
import subprocess
from subprocess import call
from subprocess import Popen

# '*ga.pd*': regional_daily
# '*ga.pe*': regional_monthly
# '*ma.pc*': global_monthly 

class wah(object):
    """
    container of folders containint w@h simulations
    """
    def __init__(self, root_folder):
        """
        parse w@h folder

        Parameters
        ----------
        root_folder : string
            folder where all w@h simulations are stored
        
        """

        super(wah, self).__init__()
        self.root_folder = root_folder

        fNs = sorted(glob.glob(root_folder))

        self.folder = [_wah_one(fN) for fN in fNs]

    def __repr__(self):
        f = os.path.split(self.root_folder)[0]
        return 'w@h simulation in {}\n{} members'.format(f, len(self))

    def __len__(self):
        return len(self.month)

    def __getitem__(self, key):

        key = np.array(key)

        # from select
        if key.dtype == np.bool:
            zipped = zip(self.folder, key)
            folder = [v for v, k in zipped if k]

        # by index
        else:
            folder = self.folder[key]

        # return a new wah object
        new_self = copy.copy(self)
        new_self.folder = folder
        return new_self

    @property
    def UMID(self):
        return self.combiner('UMID')

    @property
    def UMID_number(self):
        return self.combiner('UMID_number')

    @property
    def UMID_number_unique(self):
        return np.unique(self.UMID_number)

    @property
    def year(self):
        return self.combiner('year')

    @property
    def month(self):
        return self.combiner('month')

    @property
    def path(self):
        return self.combiner('path')

    def combiner(self, prop):
        return np.array([getattr(r, prop) for r in self.folder])

    def select(self, **kwargs):
        """
        subset wah by UMID_number, year, month

        Examples:

        w.select(year=2014, month=slice(6, 8))
        """

        sel = self._get_sel(**kwargs)
        return self[sel] 

    def _get_sel(self, **kwargs):

        sel = np.ones(len(self), dtype=np.bool)

        for key, item in kwargs.items():
            data = self.combiner(key)
            sel = self._get_sel_single(sel, data, condition=item)

        return sel

    @staticmethod
    def _get_sel_single(sel, data, condition):

        # select with a slice
        if isinstance(condition, slice):
            if condition.step:
                raise ValueError("step can not be set")

            if condition.start:
                sel = (sel) & (data >= condition.start)

            if condition.stop:
                sel = (sel) & (data <= condition.stop)

            return sel
        
        # select with a single condition
        else:
            return (sel) & (data == condition)

    def load_regional_monthly(self, standard_name, **kwargs):
        """
        load regional monthly data

        Parameters
        ----------
        standard_name : string
            name of the variable
        kwargs : keyword arguments
            selects
        """

        s = self.select(**kwargs)
        d = [f.folder.load_regional_monthly(standard_name) for f in s]
        return d

    def load_regional_daily(self, standard_name, **kwargs):
        """
        load regional daily data

        Parameters
        ----------
        standard_name : string
            name of the variable
        kwargs : keyword arguments
            selects
        """

        s = self.select(**kwargs)
        d = [f.folder.load_regional_daily(standard_name) for f in s]
        return d

    def load_global_monthly(self, standard_name, **kwargs):
        """
        load global monthly data

        Parameters
        ----------
        standard_name : string
            name of the variable
        kwargs : keyword arguments
            selects
        """

        s = self.select(**kwargs)
        d = [f.folder.load_global_monthly(standard_name) for f in s]
        return d

# ============================================================================

class _wah_one(object):
    """docstring for _wah_one"""
    def __init__(self, path, sep='_'):
        super(_wah_one, self).__init__()

        self.path = path

        self.folder = os.path.basename(path)
        
        _splitname = self.folder.split(sep)
        self._splitname = _splitname

        # original attributes
        self.model = _splitname[0]
        self.region = _splitname[1]
        self.UMID = _splitname[2]
        self._yearindex = int(_splitname[3])
        self._afteryearnumber = int(_splitname[4])
        self._longnumber = int(_splitname[5])
        self._afterlongnumber = int(_splitname[6])
        self._monthindex = int(_splitname[7])

        # derived attributes
        self.UMID_number = int(self.UMID, base=36)

        if self._monthindex == 13:
            raise ValueError("Aaahh, month, 13.")
        elif self._monthindex == 1:
            self.month = 12
            self.year = self._yearindex 
        else:
            self.month = self._monthindex - 1
            self.year = self._yearindex + 1

    def __repr__(self):
        string = 'wah: {} {:02d}.{} ({})'.format(self.region,
            self.month, self.year, self.UMID)        
        return string

    def load_regional_monthly(self, standard_name):
        return self._load(standard_name, '*ga.pe*')

    def load_regional_daily(self, standard_name):
        return self._load(standard_name, '*ga.pd*')

    def load_global_monthly(self, standard_name):
        return self._load(standard_name, '*ma.pc*')

    def _load(self, standard_name, which):
        # get the name of the .nc file in the folder
        fN = glob(os.path.join(self.path, which))
        if len(fN) != 1:
            print(fN)
            raise AssertionError('more than one or zero filenames')
            
        ds = xr.open_dataset(fN[0])
        ds = ds.filter_by_attrs(standard_name=standard_name)
        var = ds.data_vars.keys()
        assert len(var) == 1
        return ds[var[0]]



# fNs = [glob.glob(fn[i].path + '/*ga.pe*')[0] for i in range(6, 30)]
# ds = [xr.open_dataset(fN) for fN in fNs]

# ds_sm = ds[0].filter_by_attrs(standard_name='liquid_water_content_of_soil_layer')
# ds_sm = ds_sm[ds_sm.data_vars.keys()[0]]
# landmask = ds_sm.notnull().squeeze()

# dss = [d.filter_by_attrs(standard_name='precipitation_flux') for d in ds]
# dss = [ds[ds.data_vars.keys()[0]] for ds in dss]

# ds = xr.concat(dss, 'time1')



# mask = regionmask.defined_regions.srex.mask(ds, lon_name='global_longitude0', lat_name='global_latitude0', wrap_lon=True)

# wgt = ds.cos_wgt('global_latitude0')

# print ds.where(mask==12).squeeze().average(('latitude0', 'longitude0'), weights=wgt).mean() * 3600 * 24 * 92
# print ds.where((mask==12) & landmask).squeeze().average(('latitude0', 'longitude0'), weights=wgt).mean() * 3600 * 24 * 92


