"""
Calculates the integrated intensity per frame and channel of a stack.
"""
import numpy as np
from ..roi import RectRoi, ContourRoi

my_id = "integrated_intensity_calculator"


def register(meta):
    meta.name = "Integrated intensity"
    meta.id = my_id

    meta.run_dep = ("", "stack")
    meta.run_ret = "integrated_intensity"


def run(d, *_, **__):
    stack = d[""]["stack"]
    img = stack.img
    n_channels, n_frames, n_rows, n_cols = img.shape
    intensity_tables = {}

    # DEBUG
    print("Frames: {}\nChannels: {}\nRows: {}\nColumns: {}".format(n_frames, n_channels, n_rows, n_cols))

    roi_types = (RectRoi.key(), ContourRoi.key())
    isGlobalRois = Ellipsis in stack.rois
    if isGlobalRois:
        rois = stack.get_rois(Ellipsis)

    for rt in roi_types:
        rc = stack.get_rois(rt)
        if rc is None:
            continue

        frames = sorted(rc.frames())
        if not frames:
            continue
        elif len(frames) == 1 and frames[0] is Ellipsis:
            isGlobalRois = True
            rois = rc[frames[0]]
        else:
            isGlobalRois = False

        intensity_table = np.empty((n_channels, n_frames), dtype=object)
        for c in range(n_channels):
            for f in range(n_frames):
                tab = []
                if not isGlobalRois:
                    rois = rc[f]
                for roi in rois:
                    print("ROI: x=[{:4d},{:4d}], y=[{:4d},{:4d}]".format(
                        roi.cols.min(), roi.cols.max(), roi.rows.min(), roi.rows.max()))
                    tab.append(np.sum(img[c, f, roi.rows, roi.cols]))
                intensity_table[c, f] = tab
        intensity_tables[rt] = intensity_table

    # DEBUG
    #print("The integrated intensities:")
    #print(intensity_table)

    return {"integrated_intensity": intensity_tables}
