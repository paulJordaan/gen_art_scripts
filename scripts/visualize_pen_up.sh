#!/bin/sh

vpype read "$1" linesort \
   write --pen-up "%prop.vp_source.with_stem(prop.vp_source.stem + '_pen_up')%"