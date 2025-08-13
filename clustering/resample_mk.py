import glob
import numpy as np
import scipy.ndimage
from seticore import viewer
import os
import csv

# Parameters
STAMPS_GLOB = "/datax/scratch/jaym/mk_stamps/*.stamps"
OUTPUT_DIR = "/datax/scratch/jaym/resampled_mk_stamps"
COSMIC_SHAPE = (16, 640)  # (time, freq)
MANIFEST_FILE = os.path.join(OUTPUT_DIR, "manifest.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Utility: pad or crop 2D array
def pad_or_crop_2d(a, target_shape):
    t, f = a.shape
    T, F = target_shape
    a = a[:min(t, T), :min(f, F)]
    pad_t = max(0, T - a.shape[0])
    pad_f = max(0, F - a.shape[1])
    if pad_t > 0 or pad_f > 0:
        a = np.pad(a, ((0, pad_t), (0, pad_f)), mode='constant')
    return a

# Resampling function
def resample_stamp(stamp, target_shape=(16, 640)):
    arr = stamp.real_array()  # (T, F, pol, ant, complex)
    power = np.sum(np.abs(arr)**2, axis=-1)  # (T, F, pol, ant)
    t_in, f_in, n_pol, n_ant = power.shape
    zoom_t = target_shape[0] / t_in
    zoom_f = target_shape[1] / f_in

    out = np.empty((target_shape[0], target_shape[1], n_pol, n_ant), dtype=power.dtype)
    for p in range(n_pol):
        for a in range(n_ant):
            slice_in = power[:, :, p, a]
            slice_out = scipy.ndimage.zoom(slice_in, (zoom_t, zoom_f), order=1)
            slice_out = pad_or_crop_2d(slice_out, target_shape)
            out[:, :, p, a] = slice_out
    return out

# Prepare manifest
with open(MANIFEST_FILE, "w", newline="") as mf:
    writer = csv.writer(mf)
    writer.writerow(["out_file", "resampled_file", "resampled_index"])

    # Load and process
    paths = glob.glob(STAMPS_GLOB, recursive=True)
    print(f"Found {len(paths)} .stamps files")
    counter = 0

    for path in paths:
        for i, stamp in enumerate(viewer.read_stamps(path, find_recipe=True)):
            try:
                resampled = resample_stamp(stamp, COSMIC_SHAPE)
                resampled_name = f"stamp_{counter:04d}.npy"
                out_path = os.path.join(OUTPUT_DIR, resampled_name)
                np.save(out_path, resampled)

                # Log to manifest
                writer.writerow([path, out_path, i])
                counter += 1
            except Exception as e:
                print(f"Error processing stamp {i} in {path}: {e}")

print(f"Resampled {counter} stamps")
print(f"Manifest saved to {MANIFEST_FILE}")
