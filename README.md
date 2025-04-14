# DAZ Materials to Blender

Yet another implementation of a bridge. Yet this one tries to keep things simple.

The user decides exactly what gets exported from DAZ and imported in Blender (and how).
This bridge just copies materials and sets them up in Blender.

## Usage
**K, we're doing the plugin thing, jeez!**  
I'm currently in the middle of development and will update this readme, when the dust settles.

1. Save your DAZ scene
2. Export the objects you want to have in Blender using either:
   * `FBX`: Supports rigging, but gets weird when figure is already animated in DAZ.
   * `OBJ`: Just the mesh, great if you want to pose in DAZ and render in Blender (my personal use-case.)
3. Import your objects in Blender.  
   _**You can group the items as you wish, but at this stage do NOT change any object or material labels/names!**_
4. Open this script in Blender's Python editor (within the file into which you've just imported your figures.)
5. Set the `DAZ_SCENE_SAVE_FILE` to point to your DAZ scene (.duf) file.
6. Run the script.

If everything worked as expected this script should've set up all materials with the correct maps and settings.

## Notes
* Current supported shaders are:
  * PBRSkin
  * Iray Uber
  * iWave's Translucent Fabric Shader
