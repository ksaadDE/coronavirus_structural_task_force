# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('B', '  45 ', 'ASN', 0.0328586674062235, (15.813999999999997, 18.479999999999993, 32.21)), ('B', ' 605 ', 'ASP', 0.028561911260704606, (18.82, 30.014000000000003, -7.448000000000002))]
data['omega'] = [('A', ' 141 ', 'PRO', None, (6.111000000000001, -7.313999999999998, -34.876)), ('A', ' 608 ', 'PRO', None, (12.916000000000002, 14.642, -28.724000000000007)), ('B', ' 141 ', 'PRO', None, (11.237, 27.549000000000007, 19.825000000000003)), ('B', ' 608 ', 'PRO', None, (22.397999999999993, 26.708000000000006, -0.754))]
data['rota'] = [('A', '   9 ', 'GLN', 0.2882895660975955, (-36.52300000000001, -29.807000000000006, -14.604)), ('A', ' 147 ', 'LEU', 0.23534184616240006, (13.637000000000002, -3.295000000000001, -27.268)), ('A', ' 155 ', 'MET', 0.0, (15.938999999999997, 4.762000000000001, -29.76300000000001)), ('A', ' 372 ', 'TYR', 0.05612793464973451, (-8.375, -33.829, -20.723)), ('A', ' 377 ', 'VAL', 0.08289525301953367, (-16.617999999999995, -29.921, -19.826)), ('A', ' 388 ', 'HIS', 0.25106956751153836, (-1.7249999999999988, -24.73400000000001, -17.086)), ('A', ' 413 ', 'ARG', 0.07368774108967582, (29.386000000000003, -29.76900000000001, -27.465000000000003)), ('A', ' 415 ', 'THR', 0.013320535772832763, (32.081, -28.5, -21.332)), ('A', ' 416 ', 'ASN', 0.2317488866445124, (30.90599999999999, -29.559000000000005, -17.822)), ('A', ' 560 ', 'VAL', 0.03536789766007544, (5.791999999999993, -33.7, -6.15)), ('A', ' 591 ', 'VAL', 0.22547151629444326, (24.648, -1.5420000000000005, -2.951)), ('B', ' 105 ', 'LEU', 0.27464210415048707, (16.47199999999999, -8.485, 30.875000000000004)), ('B', ' 151 ', 'ARG', 0.06720303946648856, (7.1220000000000026, 33.917000000000016, 3.1270000000000007)), ('B', ' 368 ', 'TYR', 0.24750232328654975, (-10.046000000000005, 13.915000000000004, 32.126)), ('B', ' 372 ', 'TYR', 0.08393822298505589, (-11.604999999999997, 9.872999999999996, 36.732)), ('B', ' 542 ', 'LYS', 0.27258495066521005, (-20.613, 11.999000000000004, 32.392)), ('B', ' 560 ', 'VAL', 0.2636306901307384, (-24.32400000000001, 11.597000000000001, 20.91))]
data['cbeta'] = [('B', ' 354 ', 'ASP', ' ', 0.30826239507672487, (-2.3339999999999996, 27.826999999999995, 16.53))]
data['probe'] = [(' A1630  3EF  NBG', ' A1630  3EF  OBK', -1.032, (6.523, -14.809, -24.304)), (' B 147  LEU HD22', ' B 256  MET  HA ', -0.88, (7.488, 22.63, 9.21)), (' A1625  PG4  H32', ' A2341  HOH  O  ', -0.863, (1.061, -1.366, -2.338)), (' A 467  ARG HH11', ' A 471  GLN HE22', -0.832, (8.132, -4.122, -14.637)), (' A 147  LEU HD22', ' A 256  MET  HA ', -0.804, (10.007, -2.332, -24.523)), (' B 350  ARG  H  ', ' B 355  GLN HE21', -0.793, (3.134, 28.836, 22.775)), (' B 147  LEU  CD2', ' B 256  MET  HA ', -0.785, (7.274, 23.243, 8.177)), (' A 245  ARG  HG2', ' A 591  VAL HG11', -0.783, (24.1, 2.229, -4.861)), (' A  17  ALA  HB1', ' A  92  ILE HD11', -0.773, (-26.237, -30.057, -8.201)), (' A 233  LEU HD23', ' A 267  MET  HE1', -0.772, (23.416, -2.586, -20.744)), (' A  17  ALA  HB1', ' A  92  ILE  CD1', -0.728, (-26.82, -30.154, -7.663)), (' A 157  LEU HD11', ' A 477  VAL HG13', -0.714, (10.981, 8.943, -22.168)), (' A 155  MET  HA ', ' A 155  MET  HE3', -0.713, (15.476, 5.436, -30.929)), (' B 262  GLU  OE2', ' B2129  HOH  O  ', -0.686, (-0.558, 25.837, 13.111)), (' A 206  THR HG23', ' A 210  ASP  OD2', -0.672, (-1.977, -20.378, 1.381)), (' A 236  ARG  HD3', ' A 267  MET  HE3', -0.659, (26.576, -3.345, -21.547)), (' B 124  THR HG22', ' B 327  GLU  HG2', -0.649, (18.37, 18.951, 24.738)), (' B 147  LEU HD22', ' B 256  MET  CA ', -0.642, (7.056, 22.923, 9.223)), (' B 157  LEU HD11', ' B 477  VAL HG13', -0.63, (14.13, 21.919, -0.497)), (' A 270  PRO  HD3', ' A 426  LEU HD23', -0.609, (26.378, -13.933, -17.217)), (' B 324  ASP  OD1', ' B 326  ARG  HB2', -0.604, (17.389, 25.117, 31.771)), (' A 117  GLN  HG2', ' A 120  ARG  NH2', -0.593, (-14.251, -0.45, -30.202)), (' B  49  GLU  HG3', ' B  53  ARG  NH1', -0.59, (20.937, 11.837, 37.375)), (' A 213 BHIS  HD2', ' A2145  HOH  O  ', -0.587, (6.943, -19.895, 1.723)), (' A1625  PG4  O4 ', ' B 453  ARG  NH1', -0.581, (1.962, 1.241, 3.731)), (' A 507  LEU HD13', ' A 565  LEU  CD2', -0.569, (2.227, -24.2, -7.123)), (' A 324  ASP  OD1', ' A 326  ARG  HB2', -0.56, (-4.397, -10.223, -43.7)), (' B 344  ARG HH22', ' B1624  PEG  H42', -0.56, (7.201, 17.56, 41.411)), (' B  17  ALA  HB1', ' B  92  ILE HD11', -0.558, (-10.223, -11.466, 37.506)), (' A  25  GLN HE21', ' A 378  SER  H  ', -0.557, (-17.955, -29.81, -17.216)), (' A 245  ARG  HG2', ' A 591  VAL  CG1', -0.556, (24.418, 1.763, -4.682)), (' B 236  ARG  HG2', ' B 267  MET  HE3', -0.553, (2.157, 33.32, -0.686)), (' B 260  SER  OG ', ' B 262  GLU  OE1', -0.546, (-3.554, 23.908, 11.894)), (' A 274  LYS  HB3', ' A 275  PRO  HD2', -0.54, (32.179, -21.816, -23.065)), (' A 467  ARG  NH1', ' A 471  GLN HE22', -0.532, (7.76, -3.939, -15.054)), (' A 233  LEU HD23', ' A 267  MET  CE ', -0.531, (23.629, -3.111, -20.389)), (' A 232  ALA  HB2', ' A1626  PEG  H31', -0.525, (27.123, -6.634, -16.101)), (' B 340  ARG HH11', ' B 374  ASP  HA ', -0.523, (-9.732, 7.538, 42.489)), (' A 270  PRO  HD3', ' A 426  LEU  CD2', -0.522, (25.975, -13.571, -16.68)), (' A 507  LEU HD13', ' A 565  LEU HD23', -0.515, (2.803, -24.723, -7.121)), (' B  31  VAL  O  ', ' B  34  GLN  HG3', -0.502, (7.04, 3.935, 39.431)), (' A 155  MET  CE ', ' A 155  MET  HA ', -0.501, (14.774, 5.038, -31.262)), (' B  44  THR  O  ', ' B 326  ARG  HD2', -0.495, (14.349, 21.11, 32.418)), (' A 479  ARG  H  ', ' B 598  GLN  NE2', -0.491, (6.304, 10.088, -14.924)), (' B 151  ARG  HD2', ' B2067  HOH  O  ', -0.486, (2.372, 35.875, 3.87)), (' A 465  TYR  CE2', ' A1625  PG4  H31', -0.481, (2.407, 0.322, -2.299)), (' B 580  TRP  O  ', ' B 584  GLN  HG2', -0.466, (-15.481, 29.393, -3.548)), (' B 206  THR HG23', ' B 210  ASP  OD2', -0.458, (-15.696, -1.101, 11.947)), (' B  25  GLN HE21', ' B 378  SER  H  ', -0.456, (-7.103, -0.366, 37.211)), (' A 228  PHE  CD1', ' A1626  PEG  H41', -0.454, (27.855, -8.099, -12.459)), (' B 172  LYS  O  ', ' B 176  GLU  HG3', -0.451, (16.469, 2.668, 11.847)), (' A 415  THR  HB ', ' A 417  ASP  OD2', -0.449, (33.684, -26.627, -19.936)), (' B 296  VAL HG22', ' B1622  P6G H171', -0.448, (-9.916, 34.965, 30.168)), (' B  24  TYR  HD2', ' B  25  GLN  HG3', -0.445, (-4.909, -3.051, 38.756)), (' B 201  TRP  HZ3', ' B 497  PRO  HG2', -0.445, (-1.609, 3.804, 21.355)), (' A 416  ASN  OD1', ' A1616  NAG  C7 ', -0.445, (28.234, -32.664, -17.214)), (' A 489  LYS  O  ', ' A 493  PRO  HD2', -0.443, (-2.671, -5.004, -20.969)), (' B1611  FUC  H3 ', ' B2213  HOH  O  ', -0.442, (19.044, 16.392, -1.644)), (' B 510  GLN  HG2', ' B 569  PRO  HG2', -0.441, (-20.989, 13.643, 14.694)), (' A 228  PHE  CE1', ' A1626  PEG  H41', -0.427, (28.373, -8.662, -12.562)), (' A 416  ASN  OD1', ' A1616  NAG  N2 ', -0.425, (28.119, -32.427, -16.962)), (' A  31  VAL HG21', ' A  64  PHE  CD1', -0.42, (-25.625, -22.53, -23.33)), (' A 117  GLN  HG2', ' A 120  ARG HH22', -0.42, (-13.759, 0.292, -29.665)), (' A  59  LEU HD22', ' A2031  HOH  O  ', -0.42, (-26.901, -10.975, -23.679)), (' B 124  THR HG22', ' B 327  GLU  CG ', -0.42, (18.315, 19.116, 24.538)), (' A 157  LEU HD13', ' A 476  PRO  HB2', -0.419, (13.278, 6.702, -21.188)), (' A 539  LYS  HE3', ' A 559  MET  O  ', -0.419, (5.882, -36.03, -9.041)), (' B 513  GLU  HA ', ' B 525  LEU HD11', -0.419, (-22.871, 20.764, 16.895)), (' A 510  GLN  HG2', ' A 569  PRO  HG2', -0.416, (9.582, -27.411, -5.716)), (' A 201  TRP  CZ3', ' A 497  PRO  HG2', -0.413, (-8.384, -15.73, -13.671)), (' B 155  MET  HA ', ' B 155  MET  HE3', -0.411, (15.622, 29.982, 5.501)), (' A 496  THR  HA ', ' A 497  PRO  HD3', -0.408, (-8.243, -13.047, -17.271)), (' A 172  LYS  O  ', ' A 176  GLU  HG3', -0.407, (-10.26, 4.265, -17.4)), (' A 472  GLY  HA2', ' A 594  TRP  CE2', -0.404, (13.657, -1.045, -7.497)), (' B 496  THR  HA ', ' B 497  PRO  HD3', -0.403, (2.54, 5.822, 21.514)), (' A 607  TYR  HA ', ' A 608  PRO  HA ', -0.402, (14.504, 12.944, -28.363)), (' A 292  HIS  O  ', ' A 296  VAL HG23', -0.4, (11.537, -27.894, -35.095)), (' A 477  VAL HG12', ' A 603  LEU HD21', -0.4, (11.673, 12.089, -21.463))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
