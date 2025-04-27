class PrincipledBSDFSockets:
    """
    A list of input socket ids for the Principled BSDF Shader.
    Derived from https://github.com/blender/blender/blob/main/source/blender/nodes/shader/nodes/node_shader_bsdf_principled.cc
    """

    BASE_COLOR = 0
    METALLIC = 1
    ROUGHNESS = 2
    IOR = 3
    ALPHA = 4
    NORMAL = 5
    # WEIGHT = 6  # HIDDEN SOCKET!
    DIFFUSE_ROUGHNESS = 7
    SUBSURFACE_WEIGHT = 8
    SUBSURFACE_RADIUS = 9
    SUBSURFACE_SCALE = 10
    SUBSURFACE_IOR = 11
    SUBSURFACE_ANISOTROPY = 12
    SPECULAR = 13
    SPECULAR_TINT = 14
    ANISOTROPIC = 15
    ANISOTROPIC_ROTATION = 16
    TANGENT = 17
    TRANSMISSION_WEIGHT = 18
    COAT_WEIGHT = 19
    COAT_ROUGHNESS = 20
    COAT_IOR = 21
    COAT_TINT = 22
    COAT_NORMAL = 23
    SHEEN_WEIGHT = 24
    SHEEN_ROUGHNESS = 25
    SHEEN_TINT = 26
    EMISSION = 27
    EMISSION_STRENGTH = 28
    THIN_FILM_THICKNESS = 29
    THIN_FILM_IOR = 30
