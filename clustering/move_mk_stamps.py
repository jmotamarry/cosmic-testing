import os
import glob
import shutil

# Input pattern for original .stamps files
STAMPS_GLOB = "/mnt/blpc0/datax/scratch/jaym/meerkat_data/*/seticore_search/*.stamps"

# Output folder (same level as resampled_mk_stamps)
OUTPUT_DIR = "/datax/scratch/jaym/mk_stamps"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Find and sort all .stamps files
paths = sorted(glob.glob(STAMPS_GLOB, recursive=True))
print(f"Found {len(paths)} .stamps files")

# Copy with sequential numbering
for counter, path in enumerate(paths):
    try:
        dest_filename = f"stamp_{counter:04d}.stamps"
        dest = os.path.join(OUTPUT_DIR, dest_filename)
        shutil.copy2(path, dest)
        print(f"Copied {path} → {dest_filename}")
    except Exception as e:
        print(f"Error copying {path}: {e}")

print("Done.")
