#!/usr/env/bin python3

# new imports

import rerun as rr

rr.init("rerun_example_dna_abacus")

rr.spawn()

from rerun.utilities import build_color_spiral
from math import tau

NUM_POINTS = 100

# points and colors are both np.array((NUM_POINTS, 3))
points1, colors1 = build_color_spiral(NUM_POINTS)
points2, colors2 = build_color_spiral(NUM_POINTS, angular_offset=tau*0.5)

rr.log("dna/structure/left", rr.Points3D(points1, colors=colors1, radii=0.08))
rr.log("dna/structure/right", rr.Points3D(points2, colors=colors2, radii=0.08))
