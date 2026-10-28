"""The only file you need to change."""

from pathlib import Path

import mne
import numpy as np


def process(data_dir: Path, out_dir: Path) -> None:
    """Read recordings from data_dir, write your results into out_dir.

    data_dir is read-only and the same for every team.
    Anything you write into out_dir is yours and is kept.
    Everything else is thrown away when the job ends.
    """
    recordings = sorted(data_dir.rglob("*.bdf"))
    print(f"{len(recordings)} recordings")

    # Replace everything below with your own work. This measures alpha power
    # (8-12 Hz) per recording, which is about the simplest real thing you can
    # ask of an EEG file.
    rows = ["recording\tchannels\tseconds\talpha_uV2"]
    for path in recordings:
        raw = mne.io.read_raw_bdf(path, preload=True, verbose="ERROR")
        psd = raw.compute_psd(fmin=1, fmax=40, verbose="ERROR")
        freqs, power = psd.freqs, psd.get_data()
        alpha = float(np.mean(power[:, (freqs >= 8) & (freqs <= 12)]))
        seconds = raw.n_times / raw.info["sfreq"]
        rows.append(f"{path.name}\t{len(raw.ch_names)}\t{seconds:.0f}\t{alpha:.4g}")
        print(f"  {path.name}: alpha={alpha:.4g}")

    (out_dir / "alpha.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"wrote alpha.tsv with {len(rows) - 1} rows")
