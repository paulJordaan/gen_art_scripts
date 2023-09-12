#!/bin/sh

vpype \
--config ../gcode_config.toml \
read --attr stroke "$1" \
linemerge \
linesort \
reloop \
linesimplify \
layout --fit-to-margins 3cm a4 \
pagesize a4 \
forlayer write "%prop.vp_source.with_stem(prop.vp_source.stem + '_' + str(_lid))%" end
