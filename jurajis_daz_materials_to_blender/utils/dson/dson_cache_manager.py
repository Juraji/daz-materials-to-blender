import pickle
from os import path
from pathlib import Path

import bpy
from bpy.path import abspath
from bpy.types import Context

from .dson_reader import DsonReader
from .dson_data import DsonData
from ...properties import props_from_ctx, prefs_from_ctx


class DsonCacheManager:
    CACHE_SUFFIX = ".matcache"

    @classmethod
    def get_or_load(cls, context: Context) -> DsonData:
        props = props_from_ctx(context)

        if not props.has_scene_file_set():
            raise Exception(f"No scene file set")

        scene_file = abspath(props.daz_scene_file)
        if not path.exists(scene_file):
            raise Exception(f"Scene file '{scene_file}' not found")

        cache_path = cls._get_cache_file_path_for(props.daz_scene_file)

        if cache_path.exists():
            with open(cache_path, "rb") as f:
                dson_data = pickle.load(f)
        else:
            prefs = prefs_from_ctx(context)
            content_dirs = prefs.content_libraries_as_paths()
            if len(content_dirs) == 0:
                raise Exception("No content libraries found, you can set them in the addon preferences!")

            dson_reader = DsonReader(content_dirs)
            dson_data = dson_reader.read_dson(scene_file)

            with open(cache_path, "wb") as f:
                # noinspection PyTypeChecker
                pickle.dump(dson_data, f)

        return dson_data

    @classmethod
    def clear_cache(cls):
        if not bpy.data.is_saved:
            return  # Nothing to do!
        b_file = Path(abspath(bpy.data.filepath))
        root = b_file.parent
        for f in root.iterdir():
            if f.is_file() and f.suffix == cls.CACHE_SUFFIX:
                f.unlink(missing_ok=True)

    @classmethod
    def _get_cache_file_path_for(cls, daz_scene_file: str):
        if not bpy.data.is_saved:
            raise Exception("You need to save your Blender project first.")
        b_file = Path(abspath(bpy.data.filepath))
        root = b_file.parent
        scene_basename = path.basename(daz_scene_file)
        return root / f"{scene_basename}{cls.CACHE_SUFFIX}"


class DsonLoadException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
