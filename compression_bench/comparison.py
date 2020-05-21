#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 fx-kirin <fx.kirin@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import logging
import os
import time
import zipfile
from pathlib import Path

import kanilog
import stdlogging


def main():
    current_dir = Path(__file__).absolute().parent
    csv_file_path = current_dir / "book.csv"
    original_stats = csv_file_path.stat()
    print(f"Original File :{original_stats.st_size}")
    for comp_method in ["ZIP_STORED", "ZIP_DEFLATED", "ZIP_BZIP2", "ZIP_LZMA"]:
        method = getattr(zipfile, comp_method)
        bench = time.time()
        zip_path = csv_file_path.parent / f"{comp_method}.zip"
        zip_file = zipfile.ZipFile(zip_path, "w", compression=method)
        zip_file.write(csv_file_path, csv_file_path.name, compresslevel=9)
        zip_file.testzip()
        zip_file.close()
        zip_stats = zip_path.stat()

        comp_rate = "%.2f" % round(zip_stats.st_size/original_stats.st_size * 100, 2)
        comp_time = time.time() - bench
        print(f"{comp_method} :{zip_stats.st_size=} rate:{comp_rate}% time:{comp_time}")
        zip_path.unlink()


if __name__ == "__main__":
    kanilog.setup_logger(logfile='/tmp/%s.log' % (Path(__file__).name), level=logging.INFO)
    stdlogging.enable()
    main()
