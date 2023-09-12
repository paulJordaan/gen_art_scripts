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
gwrite --profile my_own_plotter "%prop.vp_source.with_name(prop.vp_source.stem + '_processed_a4.gcode')%"
