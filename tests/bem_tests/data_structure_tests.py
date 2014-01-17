from nose.tools import *

from numpy import pi, sin, cos, array
import numpy as np
from numpy.testing import assert_array_almost_equal as assert_aae

from bem.bem import (AerofoilDatabase, Aerofoil, BladeSection, BEMModel,
                     thrust_correction_factor, iterate_induction_factors,
                     solve_induction_factors)


class AerofoilDatabase_Tests:
    def setup(self):
        self.db = AerofoilDatabase('../aerofoils.npz')

    # CylinderData:
    def test_cylinder_data_read_correctly(self):
        foil = self.db.for_thickness(1.0)
        for alpha in [-0.3, 0, 0.3]:
            assert_aae(foil.CL(alpha), 0)
            assert_aae(foil.CD(alpha), 1)

    # ThirteenPercentFoil:
    def test_thirteen_percent_foil_read_correctly(self):
        foil = self.db.for_thickness(0.13)
        assert_aae(foil.CL(0), 0.420)
        assert_aae(foil.CD(0), 0.006)
        assert_aae(foil.CL(10*pi/180), 1.460)
        assert_aae(foil.CD(10*pi/180), 0.016)

    def test_thirteen_percent_foil_interpolated_by_alpha(self):
        # Interpolate between 4 and 6 deg alpha
        foil = self.db.for_thickness(0.13)
        assert_aae(foil.CL(5*pi/180), (0.890 + 1.100) / 2)
        assert_aae(foil.CD(5*pi/180), (0.009 + 0.012) / 2)

    # InterpolatedData:
    def interpolated_by_thickness(self):
        # Interpolate between 13% and 17% data
        foil = db.for_thickness(0.15)
        assert_aae(foil.CL(10*pi/180), (1.460 + 1.500) / 2)
        assert_aae(foil.CD(10*pi/180), (0.016 + 0.014) / 2)


class BladeSection_Tests:
    def test_holds_chord_twist_and_foil(self):
        section = BladeSection(1, 2, 3)
        eq_(section.chord, 1)
        eq_(section.twist, 2)
        eq_(section.foil, 3)
