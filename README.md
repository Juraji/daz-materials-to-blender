# DAZ Materials to Blender

Yet another implementation of a bridge.

Yet this one tries to keep things simple.  
The user decides exactly what gets exported from DAZ and imported in Blender (and how).
This bridge just copies materials and sets them up in Blender.

![Static Badge](https://img.shields.io/badge/stability-experimental-orange)
![Static Badge](https://img.shields.io/badge/version-1.0.0-blue)
![Static Badge](https://img.shields.io/badge/licence-GPLv3-green)

## What does it do

Imagine this: You've tried using the [Daz to Blender Bridge](https://www.daz3d.com/daz-to-blender-bridge), it looked
promising but...
You've posed your figures and created a massive scene. It's beautiful! But we want to render it in Blender and maybe do
some adjustments DAZ does not allow?
Yes, so you get going, exporting your figures, one by one to Blender. But you hit a few snags...
The figures are no longer posed, materials are simplisticly setup to say the least... As for the scene itself, Yeah,
there's no options there...

_Side note: There's [Diffeomorphic](https://bitbucket.org/Diffeomorphic/import_daz/wiki/Home), a good solution! However,
I found that it's just far to much for my use-case._

In comes this plugin. It reads material data from `.duf` scene files and sets them up for the corresponding objects in
Blender.

There is ALOT to talk about and this README doesn't even scratch the surface, but do read on, as it at least covers the
basics.
Check out the [usage](#basic-usage) below!

## Basic Usage

_(!) You will find the UI for this plugin in the `Shader Node Editor` as well as the `3D Vieport`
under `Juraji's Tools`!_

### In DAZ Studio

<img src="images/daz-obj-export-opts.png" width="300" height="321" alt="DAZ OBJ Export Options"/>

1. Set up your scene. _You know how this works._
2. Save your scene and remember where. _A good Studio user knows to save often._
3. Export you figures and environment.
    - Use `FBX` if you need rigging.
    - Use `OBJ` if you just need the mesh.
    - In my experience I've found it better to export each figure and the environment into their own files. Keeps things
      managable and undo-able.
    - Check out the settings above. Especially the `Write Groups` and `Write Surfaces` settings. _You can write
      the MTLs, but we're going to ignore them later anyway._

### In Blender

<img src="images/plugin-collapsed-marked.png" width="300" height="287" alt="Plugin UI Import"/>

1. Import the `OBJ`s and/or `FBX`s you've exported from DAZ.  
   **IMPORTANT**:
    1. _Do NOT rename any objects or materials! This plugin uses some real magic to determine which material in
       the `.duf` file belongs to which object/material._
    2. _If you have multiple figures in your scene of the same generation or multiple instances, you should import them
       in the same order
       you've loaded them in DAZ Studio. Or import everything as one object._
2. In your 3D Viewport, click the `Juraji's Tools`-tab, and you should see a panel like the image on the right.
3. Select your DAZ scene file (`.duf`).
4. Click `Import All Materials`.
5. Blender should freeze for a moment and if all went well all of your objects should have the correct materials set up.

As for the other buttons:

* `Import Object Materials`: Only import/update materials for the selected objects.
* `Create Instances`: Big one, copy instanced objects! Check out [Object Instances](#object-instances), below!
* `Convert Materials`: After import, convert materials from one to the other type. For instance Iray Uber to PBR Skin.

## Supported Shaders

* **DAZ PBR Skin**
* **Iray Uber** _(with handling for Metallicity/Roughness, Specular/Glossiness and Weighted sub-shaders)_
* **iWave's Translucent Fabric Shader** _(My personal favorite)_
* **Blended Dual Lobe Hair** _(Often used with dForce Hair, the strands kind)_  
  This specific shader is handled a bit differently. Instead of importing and mapping colors, the importer calculates
  melanin and redness from the colors set in DAZ and uses Blender's Hair BSDF shaders. Which imho looks so much better
  with strands.

If a material uses a shader the plugin does not know, it will set up the material with a white Principled BSDF and adds
all images it finds as Texture nodes.  
All images are set to the `sRGB` colorspace. You will have to figure out the color spaces (sRGB, Non-Color, etc.) and
how the maps should be linked up. But at least this handles the great image-map search for you.

_I've implemented just the shaders I personally use. If you find that a certain shader should be added and are willing
to
contribute, shoot a pull-request and we'll work things out!_

## Deep Dive

The defaults should work for most simple setups, but sometimes you need more control.

K, to understand what the options mean and what you can do with them, we first need to pass exactly what this plugin
does.

In short: It uses a set of Node Groups that (mostly) mimic DAZ Studio's shaders. Thus, you have a group called "PBR
Skin"-group for the PBRSkin shader and the "Iray Uber"-group for the Iray Uber shader.  
When reading a material from the scene `.duf` file it tries to find the matching shader group. The shader group has
inputs that match the properties in DAZ Studio, so it just maps one to the other. Note that the DAZ Studio shaders are
not exactly re-created, as some properties are simply not applicable and others are not supported or deemed too
computationally complex.

Doing it this way allows you to easily fix properties and adjust how your material looks in Blender. If so inclined you
are even free to pick apart the groups and roll your own.

K, now for the ALL the UI properties. _I do encourage you to hover over the options in the UI, as their tooltips will be
the
most up-to-date._

### Tools & Debugging

I like to write my debuggin tools directly into the software I make. Two reasons: 1. Buttons are easier than hidden
switches, 2. They might be useful to the user as well.

#### Export DAZ Materials as JSON

This will create a `JSON` formatted file next to the Blender save file,
containing ALL properties the plugin was able to read from the DAZ `.duf` file.

#### Delete All Groups

This will delete all groups from the Blender data blocks that are created by this plugin.  
_Note that this is a slight hack, as it looks at the group's description._

### Shader groups

<img src="images/plugin-shader-groups.png" width="200" height="308" alt="Plugin UI Import Options"/>

As explained earlier in the deep-dive, this plugin uses node groups to represent DAZ Shaders. The Import action will
automatically create any group it needs to fulfill the import requirements. So if you scene uses the PBRSkin shader, it
will create that group. The same goes for the others.

However, either using this plugin for export or not, you might find one or more of these groups usefull for your own
creation.  
To that I say Cheers and Worry not. Under the Shader Groups panel, you'll find a button for each node group this plugin
uses.

#### Support

These groups are "small" pieces of the shader stacks that make up the full shader groups. You should check them out,
they might prove useful.

#### Shaders

These are the full-blown mimic shader groups. Each has options gallore!

### Import Options

<img src="images/plugin-import-options.png" width="300" height="616.5" alt="Plugin UI Import Options"/>

#### General

These options apply to all shaders.

#### PBR Skin, Iray Uber, etc.

These options apply to specific shaders.

## Object Instances

DAZ Studio does not export instanced objects. So, there you are, using some scripts to convert all instances to real
objects. In the meanwhile your export blows up to mere GBs...

Yeah, I've had that exact problem.

Well, no more! Leave your instances instanced and export your environment from DAZ Studio. After import in Blender, you
follow the same steps as in the [Basic Usage](#basic-usage). _It is recommended to import everything, at this point._

_(!) Before proceeding, make sure the "Exported Scale" has the same value as you used to export from DAZ. This is used
to scale distances from DAZ to Blender. A wrong value might result in instance locations being incorrect._  
_When in doubt, just copy the settings one-to-one._

Now Blender has all the mesh-data we need, click that `Create Instances`-button and behold!
Your instances in DAZ are now instances in Blender. And yes, these are actual instances with linked data, not just mere
copies.  
You can edit the materials and mesh data of the original and the instances will follow!

_(!) Currently only the "Single Node" Instance Mode is supported. When my brain recovers from this madness I'll try to
see if I can support "Node and Children"._

## dForce Hair

This plugin does not convert dForce Strand Based Hair (dForce Render Hair Generator).  
However, you can pre-tesselate the hair strands in DAZ Studio:

1. Select the dForce Strands object. _(often parented to a Base or Scalp object.)_
2. In the `Parameters`, under `General/Simulation/Hair/Pre Render (PR)`, enable `Preview PR Hairs`.
3. Then in the `Parameters`, under `General/Line Tessellation`, set the `Viewport Line Tessellation Sides` to the
   same value as `Render Line Tessellation Sides`.

DAZ Studio will not like this, but you can now export your figure. Don't forget to atleast restore the
`Viewport Line Tessellation Sides` before you save and close DAZ, future you, loading the scene, will thank you ;)  
Blender will handle it a lot better!

## Special Thanks

While I wrote this plugin mostly by myself there are some credits to mention:

### Blender Guru

[blenderguru.com](https://www.blenderguru.com)

Especially for the base of the "Fake Glass" shader group. A lot of headaches have been saved!  
Check out [this video](https://www.youtube.com/watch?v=KyXRBu7gn2o), where he explains exactly why it's better than
just shoving in a Glass BSDF:

