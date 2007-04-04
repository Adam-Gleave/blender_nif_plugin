# This "module" holds all the fallback values for the script configuration. This
# makes sure the configuration will never be invalid
_NIF_IMPORT_PATH = r"C:\Program Files\Bethesda\Oblivion\Data\Meshes"
# The 'r' before the string definition sets this as "raw". This means that escape
# sequences (those preceded by '\' won't be interpreted. Handy to set paths in
# Win32, and let's face it, almost all the script users will be Win32 users.
_NIF_EXPORT_PATH = r""
_REALIGN_BONES = True
_IMPORT_SCALE_CORRECTION = 0.1
_EXPORT_SCALE_CORRECTION = 10.0
_BASE_TEXTURE_FOLDER = r"C:\Program Files\Bethesda\Oblivion\Data\Textures"
_TEXTURE_SEARCH_PATH = [_BASE_TEXTURE_FOLDER]
_DEFAULT_EXPORT_VERSION = "20.0.0.5"
_EXPORT_TEXTURE_PATH = "R"
# (R)elative to NIF,
# (F)ull,
# (N)one (strip folders),
# Relative to (B)ase texture folder

_CONVERT_DDS = True
# Not really implemented yet... might have to call a command line tool. Hence..
# _CONVERTER_COMMAND_LINE = ... using wildcards for filenames and such.
