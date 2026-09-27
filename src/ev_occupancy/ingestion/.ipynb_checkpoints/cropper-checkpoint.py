"""Parallel extraction core for EV stall bounding boxes."""
import re
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image

def parse_timestamp_from_filename(filename: str, fallback_mtime: float) -> pd.Timestamp:
    match = re.search(r"(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", filename)
    if match:
        p = [int(x) for x in match.groups()]
        return pd.Timestamp(year=p[0], month=p[1], day=p[2], hour=p[3], minute=p[4], second=p[5])
    return pd.to_datetime(fallback_mtime, unit="s")

def process_single_screenshot(args):
    img_path, spots_dict = args
    try:
        with Image.open(img_path) as img:
            arr = np.array(img.convert("RGB"))
            ts = parse_timestamp_from_filename(img_path.name, img_path.stat().st_mtime)
            row = {"filename": img_path.name, "timestamp": ts}

            for name, cfg in spots_dict.items():
                x, y, w, h = cfg["x"], cfg["y"], cfg["w"], cfg["h"]
                crop = arr[y : y + h, x : x + w]
                
                mean_rgb = crop.mean(axis=(0, 1))
                std_rgb = crop.std(axis=(0, 1))

                row[f"{name}_r"] = round(float(mean_rgb[0]), 2)
                row[f"{name}_g"] = round(float(mean_rgb[1]), 2)
                row[f"{name}_b"] = round(float(mean_rgb[2]), 2)
                row[f"{name}_intensity"] = round(float(mean_rgb.mean()), 2)
                row[f"{name}_std"] = round(float(std_rgb.mean()), 2)
            return row
    except Exception:
        return None