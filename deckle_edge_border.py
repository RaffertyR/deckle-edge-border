#!/usr/bin/env python

# deckle_edge_border.py

# This plug-in creates a layer with an irregular deckle edge border around the original
# image. It is possible to change border color and border width. Border width is a %
# of the (shortest) image border.  This script uses the 'script_fu_fuzzy_border'-filter.
# Best results are obtained with images > 1000 px.
# ##########################################################
#
# License: GPLv3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# To view a copy of the GNU General Public License
# visit: http://www.gnu.org/licenses/gpl.html
#
# ----------------
#| Change Log |
# ----------------
# Version 1.0 - 01/10/2021 - initial release
# ##########################################################

from gimpfu import *

def python_deckle_edge_border(image, layer, bordercolor, borderwidth) :

	########## prepare the image ##########
	pdb.gimp_image_undo_group_start(image)
	pdb.gimp_context_push()
	pdb.gimp_selection_none(image)
	pdb.gimp_image_flatten(image)
	layers = image.layers
	orginal_layer = layers[0]
	pdb.gimp_item_set_name(orginal_layer,"image")

	########## create border layer ##########
	borderwidth = int(min(image.width, image.height) * borderwidth / 100)
	new_image_width = image.width + borderwidth
	new_image_height = image.height + borderwidth	
	pdb.gimp_image_resize(image, new_image_width, new_image_height, -int(borderwidth/2), -int(borderwidth/2))
	pdb.gimp_layer_set_offsets(orginal_layer, int(borderwidth/2), int(borderwidth/2))
	pdb.gimp_layer_resize_to_image_size		# layer "image"
	border_layer = pdb.gimp_layer_new(image, new_image_width, new_image_height, RGBA_IMAGE, "deckle_edge_border", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, border_layer, None, 1)
	pdb.gimp_image_set_active_layer(image, border_layer)	
	pdb.gimp_context_set_foreground(bordercolor)
	pdb.gimp_edit_fill(border_layer, FILL_FOREGROUND)
	
	########## make border fuzzy ##########
	borderwidth = 5 * (int(borderwidth/1000)+1)
	#  script_fu_fuzzy_border params: the image, the layer, color, border size in px, blur, 
	#		granularity, shadow, shadow weight, copy, flatten.
	pdb.script_fu_fuzzy_border(image, border_layer, (0, 0, 0), borderwidth, 0, 4, 0, 100, 0, 0)
	layers = image.layers
	fuzzy_layer = layers[0]
	pdb.gimp_edit_copy(fuzzy_layer)
	pdb.gimp_image_set_active_layer(image, border_layer)	
	bordermask = pdb.gimp_layer_create_mask(border_layer, 0)
	pdb.gimp_layer_add_mask(border_layer, bordermask)
	pdb.gimp_layer_set_edit_mask(border_layer, 1)
	floatmask = pdb.gimp_edit_paste(bordermask, 1)
	pdb.gimp_floating_sel_anchor(floatmask)
	pdb.gimp_layer_remove_mask(border_layer, 0)	# 0=apply mask to layer
	pdb.gimp_image_remove_layer(image, fuzzy_layer)

	########## create background layer ########
	layers = image.layers
	orginal_layer = layers[0]
	pdb.gimp_image_set_active_layer(image, orginal_layer)
	borderwidth = int(min(image.width, image.height) * 2 / 100)
	new_image_width = image.width + borderwidth
	new_image_height = image.height + borderwidth	
	pdb.gimp_image_resize(image, new_image_width, new_image_height, -int(borderwidth/2), -int(borderwidth/2))
	pdb.gimp_layer_set_offsets(orginal_layer, int((new_image_width - orginal_layer.width)/2), int((new_image_height - orginal_layer.height)/2))
	pdb.gimp_layer_set_offsets(border_layer, int(borderwidth/2), int(borderwidth/2))
	background_layer = pdb.gimp_layer_new(image, new_image_width, new_image_height, RGBA_IMAGE, "background", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(image, background_layer, None, 2)
	pdb.gimp_image_set_active_layer(image, background_layer)	
	pdb.gimp_context_set_foreground((192, 192, 192))
	pdb.gimp_edit_fill(background_layer, FILL_FOREGROUND)
	
	########## finalize ##########
	pdb.gimp_selection_none(image)
	pdb.gimp_context_pop()
	pdb.gimp_image_undo_group_end(image)
	pdb.gimp_displays_flush()

# The plugin registration
register(
	"python_fu_deckle_edge_border",
	"Create deckle edge border",
	"Create deckle edge border",
	"Rafferty",
	"Rafferty",
	"2021",
	"<Image>/Filters/Decor/Deckle edge border...",          		#Menu path
	"RGB*, GRAY*", 
	[
		(PF_COLOR, "bordercolor", "Border Color", (255, 255, 240)),
		(PF_SPINNER, "borderwidth", "Border width (%)", 10, (0, 100, 1)),
	],
	[],
	python_deckle_edge_border)

main()
