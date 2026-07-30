stroke_width = 96
stroke_width_heavy = 336
stroke_dist_double = 288
arc_drawing_radius_factor = 2/3
heavy_circle_radius_factor = 2/3
default_glyph_width = 1008

def set_stroke_width(value):
    global stroke_width
    stroke_width = value
def set_stroke_width_heavy(value):
    global stroke_width_heavy
    stroke_width_heavy = value
def set_stroke_dist_double(value):
    global stroke_dist_double
    stroke_dist_double = value
def set_arc_drawing_radius_factor(value):
    global arc_drawing_radius_factor
    arc_drawing_radius_factor = value
def set_heavy_circle_radius_factor(value):
    global heavy_circle_radius_factor
    heavy_circle_radius_factor = value
def set_default_glyph_width(value):
    global default_glyph_width
    default_glyph_width = value

def get_stroke_width():
    global stroke_width
    return stroke_width
def get_stroke_width_heavy():
    global stroke_width_heavy
    return stroke_width_heavy
def get_stroke_dist_double():
    global stroke_dist_double
    return stroke_dist_double
def get_arc_drawing_radius_factor():
    global arc_drawing_radius_factor
    return arc_drawing_radius_factor
def get_heavy_circle_radius_factor():
    global heavy_circle_radius_factor
    return heavy_circle_radius_factor
def get_default_glyph_width():
    global default_glyph_width
    return default_glyph_width
