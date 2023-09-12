#!/bin/sh

vpype read "$1" linemerge linesort reloop linesimplify \
   write "%prop.vp_source.with_stem(prop.vp_source.stem + '_processed')%"