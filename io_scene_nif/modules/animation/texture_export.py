"""This script contains classes to help export texture animations."""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright © 2019, NIF File Format Library and Tools contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****

import bpy

from io_scene_nif.utility import nif_utils


class TextureAnimation:

    def __init__(self, parent):
        self.nif_export = parent

    def export_flip_controller(self, fliptxt, texture, target, target_tex):
        # TODO [animation] port code to use native Blender n_texture flipping system
        #
        # export a NiFlipController
        #
        # fliptxt is a blender text object containing the n_flip definitions
        # texture is the texture object in blender ( texture is used to checked for pack and mipmap flags )
        # target is the NiTexturingProperty
        # target_tex is the texture to n_flip ( 0 = base texture, 4 = glow texture )
        #
        # returns exported NiFlipController
        #
        tlist = fliptxt.asLines()

        # create a NiFlipController
        n_flip = self.nif_export.objecthelper.create_block("NiFlipController", fliptxt)
        target.add_controller(n_flip)

        # fill in NiFlipController's values
        n_flip.flags = 8  # active
        n_flip.frequency = 1.0
        start = bpy.context.scene.frame_start
        fps = bpy.context.scene.render.fps

        n_flip.start_time = (start - 1) * fps
        n_flip.stop_time = (bpy.context.scene.frame_end - start) * fps
        n_flip.texture_slot = target_tex

        count = 0
        for t in tlist:
            if len(t) == 0:
                continue  # skip empty lines
            # create a NiSourceTexture for each n_flip
            tex = self.nif_export.texturehelper.texture_writer.export_source_texture(texture, t)
            n_flip.num_sources += 1
            n_flip.sources.update_size()
            n_flip.sources[n_flip.num_sources - 1] = tex
            count += 1
        if count < 2:
            raise nif_utils.NifError("Error in Texture Flip buffer '{}': must define at least two textures".format(fliptxt.name))
        n_flip.delta = (n_flip.stop_time - n_flip.start_time) / count
