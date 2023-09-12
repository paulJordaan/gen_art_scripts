#!/bin/sh

vpype \
--config ../gcode_config.toml \
read "$1" \
linemerge \
linesort \
reloop \
linesimplify \
layout --fit-to-margins 3cm a4 \
pagesize a4 \
write "%prop.vp_source.with_stem(prop.vp_source.stem + '_processed')%"
