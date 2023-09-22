from math import *
import sys

class GCodeContext:
    def __init__(self, xy_feedrate,penup_feedrate, z_feedrate, start_delay, stop_delay, pen_up_angle, pen_down_angle, z_height, finished_height, x_home, y_home, register_pen, num_pages, continuous, file):
      self.xy_feedrate = xy_feedrate
      self.penup_feedrate = penup_feedrate
      self.z_feedrate = z_feedrate
      self.start_delay = start_delay
      self.stop_delay = stop_delay
      self.pen_up_angle = pen_up_angle
      self.pen_down_angle = pen_down_angle
      self.z_height = z_height
      self.finished_height = finished_height
      self.x_home = x_home
      self.y_home = y_home
      self.register_pen = register_pen
      self.num_pages = num_pages
      self.continuous = continuous
      self.file = file
      
      self.drawing = False
      self.last = None

      self.preamble = [
        "G21",
        "G90",
        "G92 X%.2f Y%.2f Z%.2f" % (self.x_home, self.y_home, self.z_height),
        ""
      ]

      self.postscript = [
        "",
        "M280 P0 S%.2f" % self.pen_up_angle,
				"G1 X0 Y0 F%.2f" % self.xy_feedrate,
				"G1 Z%.2f F%.2f" % (self.finished_height, self.z_feedrate),
				"G1 X%.2f Y%.2f F%.2f" % (self.x_home, self.y_home, self.xy_feedrate),
      ]

      self.registration = [
        "M280 P0 S%.2f" % self.pen_down_angle,
        "M280 P0 S%.2f" % self.pen_up_angle,
        ""
      ]

      self.sheet_header = [
        "G92 X%.2f Y%.2f Z%.2f" % (self.x_home, self.y_home, self.z_height),
      ]
      if self.register_pen == 'true':
        self.sheet_header.extend(self.registration)

      self.sheet_footer = [
        "M280 P0 S%.2f" % self.pen_up_angle,
        "G91",
        "G0 Z15 F%.2f" % (self.z_feedrate),
        "G90",
        "G0 X%.2f Y%.2f F%.2f" % (self.x_home, self.y_home, self.xy_feedrate),
        "G91",
        "G0 Z-15 F%.2f" % (self.z_feedrate),
        "G0 Z-0.01 F%.2f" % (self.z_feedrate),
        "G90"
      ]

      self.loop_forever = [ "" ]

      self.codes = []

    def generate(self):
      if self.continuous == 'true':
        self.num_pages = 1

      codesets = [self.preamble]
      if (self.continuous == 'true' or self.num_pages > 1):
        codesets.append(self.sheet_header)
      elif self.register_pen == 'true':
        codesets.append(self.registration)
      codesets.append(self.codes)
      if (self.continuous == 'true' or self.num_pages > 1):
        codesets.append(self.sheet_footer)

      if self.continuous == 'true':
        codesets.append(self.loop_forever)
        for codeset in codesets:
          for line in codeset:
            print (line)
      else:
        for p in range(0,self.num_pages):
          for codeset in codesets:
            for line in codeset:
              print (line)
          for line in self.postscript:
            print (line)

    def start(self):
      self.codes.append("M280 P0 S%.2f" % self.pen_down_angle)
      self.drawing = True

    def stop(self):
      self.codes.append("M280 P0 S%.2f" % self.pen_up_angle)
      self.drawing = False

    def go_to_point(self, x, y, stop=False):
      if self.last == (x,y):
        return
      if stop:
        return
      else:
        if self.drawing: 
            self.codes.append("M280 P0 S%.2f" % self.pen_up_angle)
            self.drawing = False
        self.codes.append("G1 X%.2f Y%.2f F%.2f" % (x, y, self.penup_feedrate))
      self.last = (x,y)
	
    def draw_to_point(self, x, y, stop=False):
      if self.last == (x,y):
          return
      if stop:
        return
      else:
        if self.drawing == False:
            self.codes.append("M280 P0 S%.2f" % self.pen_up_angle)
            self.drawing = True
        self.codes.append("G1 X%.2f Y%.2f F%.2f" % (x, y, self.xy_feedrate))
      self.last = (x,y)
