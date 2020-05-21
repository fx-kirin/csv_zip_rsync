#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 fx-kirin <fx.kirin@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

"""csv_zip_rsync - compress csv to zip and rsync to remote server"""

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__ = ["make_zip_from_csv"]

import os
import time
import zipfile
from pathlib import Path

import kanilog

import delegator

logger = kanilog.get_module_logger(__file__, 1)


def make_zip_from_csv(root_dir, not_modified_period=86400, suffix="csv"):
    if isinstance(root_dir, str):
        root_dir = Path(root_dir).expanduser()

    for csv_file_path in root_dir.glob(f"**/*.{suffix}"):
        file_stats = csv_file_path.stat()
        if time.time() - file_stats.st_mtime > not_modified_period:
            if file_stats.st_size > 0:
                zip_file_path = csv_file_path.with_suffix(".zip")
                zip_file = zipfile.ZipFile(
                    zip_file_path, "w", compression=zipfile.ZIP_BZIP2
                )
                zip_file.write(
                    csv_file_path, arcname=csv_file_path.name, compresslevel=9
                )
                if zip_file.testzip() is None:
                    logger.info(
                        "Compression was successed. Remove original"
                        f" file.:{csv_file_path}"
                    )
                    csv_file_path.unlink()
                else:
                    raise RuntimeError("Compression was failed.")
                zip_file.close()
            else:
                logger.info(f"Delete csv file because it's empty file.:{csv_file_path}")
                csv_file_path.unlink()


def unzip_all_zip_files(root_dir):
    if isinstance(root_dir, str):
        root_dir = Path(root_dir).expanduser()
    for zip_file_path in root_dir.glob("**/*.zip"):
        zip_file = zipfile.ZipFile(zip_file_path, "r")
        files = zip_file.namelist()
        for file_ in files:
            output_path = zip_file_path.parent / file_
            with zip_file.open(file_) as z:
                output_path.write_bytes(z.read())
        zip_file_path.unlink()


def upload_and_remove_zip(root_dir, remote_name, remote_dir):
    if isinstance(root_dir, str):
        root_dir = Path(root_dir)
    root_dir = root_dir.expanduser().absolute()
    command = f'rsync -av  --include="*/" --include="*.zip" --exclude="*" "{root_dir}/" "{remote_name}":"{remote_dir}"'
    logger.info(f"executing \"{command}\"")
    result = delegator.run(command)
    if result.err != '':
        raise RuntimeError(f"rsync command failed. {result.err}")

    for zip_file_path in root_dir.glob("**/*.zip"):
        target_path = zip_file_path.relative_to(root_dir)
        if str(target_path) in result.out:
            logger.info(f"{target_path} Uploaded. Delete zip file.")
            zip_file_path.unlink()
        else:
            logger.error(f"Must have uploaded {target_path} but it's not found in output.")
    delegator.run(f"find {root_dir}/* -type d -empty -delete")
