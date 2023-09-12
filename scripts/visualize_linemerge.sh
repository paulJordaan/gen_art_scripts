#!/bin/sh

vpype read "$1" linemerge \
   write --color-mode path "%prop.vp_source.with_stem(prop.vp_source.stem + '_linemerge')%"