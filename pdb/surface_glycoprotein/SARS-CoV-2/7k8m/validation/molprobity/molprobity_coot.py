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
data['rama'] = [('B', ' 138 ', 'ASN', 0.023632057373149704, (-31.461000000000002, 7.118000000000002, 63.908999999999985))]
data['omega'] = [('A', ' 147 ', 'PRO', None, (-3.432, 1.168, 72.003)), ('A', ' 149 ', 'PRO', None, (-8.17, -2.333, 69.732)), ('B', '   8 ', 'PRO', None, (-21.686, 9.558000000000002, 41.723)), ('B', '  95 ', 'PRO', None, (1.9680000000000002, 6.222, 36.771)), ('B', ' 141 ', 'PRO', None, (-31.417000000000005, 11.137, 55.263))]
data['rota'] = [('A', '  75 ', 'LYS', 0.026481868355378642, (9.285, -20.54, 50.501)), ('A', ' 178 ', 'LEU', 0.08392509812430428, (-14.894999999999998, 6.523000000000001, 71.627)), ('B', '  74 ', 'THR', 0.03465786699667855, (-23.705, -0.40900000000000003, 35.87599999999999)), ('E', ' 387 ', 'LEU', 0.13718887749015707, (28.846000000000004, 9.164, 12.484999999999996))]
data['cbeta'] = []
data['probe'] = [(' A  99  TYR  HH ', ' E 453  TYR  HH ', -0.987, (0.38, -4.751, 27.419)), (' A  29  VAL HG13', ' A  34  MET  HG3', -0.94, (4.68, -12.785, 43.482)), (' E 452  LEU HD23', ' E 494  SER  HA ', -0.768, (-0.87, -8.044, 20.021)), (' B  33  LEU HD22', ' B  71  PHE  CG ', -0.759, (-13.02, 3.48, 32.691)), (' A 170  LEU HD13', ' A 176  TYR  CE1', -0.721, (-6.138, 7.026, 66.325)), (' A 170  LEU HD13', ' A 176  TYR  CZ ', -0.709, (-6.084, 6.042, 66.737)), (' B 142  ARG  HB2', ' B 173  TYR  CE1', -0.663, (-26.014, 7.621, 55.752)), (' A   6  GLU  N  ', ' A   6  GLU  OE1', -0.658, (-1.601, -12.041, 53.519)), (' B 136  LEU HD21', ' B 196  VAL HG13', -0.633, (-28.202, 16.825, 63.817)), (' B 201  LEU HD13', ' B 205  VAL HG23', -0.628, (-34.18, 19.648, 63.931)), (' A   2  VAL HG21', ' E 486  PHE  CZ ', -0.619, (-5.233, -19.79, 41.077)), (' A 178  LEU  C  ', ' A 178  LEU HD23', -0.619, (-16.725, 5.645, 72.332)), (' B 185  ASP  HA ', ' B 188  LYS  HE2', -0.615, (-12.285, 29.583, 79.683)), (' A  75  LYS  HB2', ' A  75  LYS  NZ ', -0.612, (11.155, -19.737, 52.402)), (' A 139  GLY  HA2', ' A 154  TRP  CH2', -0.604, (-24.278, 4.335, 77.74)), (' B  12  SER  O  ', ' B  13  LEU HD23', -0.602, (-30.555, 5.195, 44.61)), (' B  81  GLU  N  ', ' B  81  GLU  OE1', -0.596, (-27.206, -8.321, 48.41)), (' B 193  ALA  HB2', ' B 208  SER  HB3', -0.594, (-28.016, 24.897, 73.434)), (' A 145  TYR  CE2', ' A 150  VAL HG13', -0.588, (-9.678, 0.889, 72.47)), (' B  47  LEU  C  ', ' B  48  ILE HD12', -0.586, (-15.889, -6.413, 36.829)), (' E 346  ARG HH12', ' E 450  ASN  HB3', -0.585, (-0.495, -7.237, 12.023)), (' B 175  LEU HD23', ' B 176  SER  N  ', -0.571, (-22.098, 12.046, 65.911)), (' B 100  GLN  N  ', ' B 100  GLN  OE1', -0.569, (-11.582, 8.659, 43.912)), (' E 346  ARG HH12', ' E 450  ASN  CB ', -0.562, (-1.43, -6.94, 11.892)), (' E 336  CYS  SG ', ' E 363  ALA  HB2', -0.559, (25.332, 2.205, 4.835)), (' B 105  GLU  HG2', ' B 106  ILE  H  ', -0.559, (-27.946, 3.156, 51.697)), (' A 117  LYS  HD3', ' A 175  LEU HD13', -0.555, (-3.595, 7.847, 76.457)), (' E 497  PHE  HB3', ' E 507  PRO  HD3', -0.551, (-1.796, 2.473, 17.547)), (' A   2  VAL HG21', ' E 486  PHE  HZ ', -0.547, (-5.693, -19.337, 41.474)), (' A 150  VAL HG12', ' A 200  HIS  CD2', -0.547, (-9.065, -0.191, 74.102)), (' E 334  ASN  O  ', ' E 362  VAL HG12', -0.535, (27.613, 2.504, -1.35)), (' A 150  VAL HG12', ' A 200  HIS  HD2', -0.534, (-9.243, -0.685, 73.986)), (' A  94  ARG HH21', ' E 489  TYR  HE2', -0.532, (-2.18, -15.106, 35.604)), (' B 125  LEU  O  ', ' B 183  LYS  HD2', -0.527, (-11.259, 19.26, 86.01)), (' A  12  ILE HD12', ' A  13  GLN  H  ', -0.526, (7.958, 0.953, 65.836)), (' A 159  LEU HD21', ' A 182  VAL HG21', -0.522, (-28.797, -0.485, 76.572)), (' B  10  THR HG22', ' B 103  LYS  HB3', -0.518, (-21.414, 6.79, 49.695)), (' B  55  ALA  HB3', ' B  58  ILE HG13', -0.515, (-15.549, -10.385, 38.199)), (' E 517  LEU  N  ', ' E 517  LEU HD12', -0.513, (32.11, -1.815, 16.214)), (' A  28  ILE  O  ', ' A  32  ASN  ND2', -0.512, (3.519, -17.023, 40.186)), (' B  49  TYR  O  ', ' B  53  SER  HB2', -0.511, (-12.314, -6.395, 30.808)), (' B 181  LEU HD23', ' B 185  ASP  OD2', -0.511, (-13.891, 26.252, 75.894)), (' E 478  THR HG22', ' E 479  PRO  O  ', -0.506, (-2.24, -27.839, 34.905)), (' E 449  TYR  HB3', ' E 494  SER  OG ', -0.504, (-4.518, -7.423, 18.657)), (' B  75  ILE HG21', ' B  78  LEU HD12', -0.504, (-26.371, -3.66, 42.297)), (' A  96  TYR  O  ', ' A  99  TYR  HB2', -0.504, (-2.722, -6.714, 33.866)), (' A  51  ILE  O  ', ' A  51  ILE HG23', -0.5, (7.236, -9.482, 41.385)), (' B 124  GLN  HG2', ' B 129  THR  O  ', -0.498, (-12.875, 16.096, 81.307)), (' B  33  LEU HD22', ' B  71  PHE  CB ', -0.498, (-14.252, 3.574, 32.658)), (' B 136  LEU HD21', ' B 196  VAL  CG1', -0.495, (-28.387, 16.704, 64.045)), (' E 362  VAL  O  ', ' E 362  VAL HG13', -0.495, (26.899, 4.319, 0.3)), (' B 193  ALA  CB ', ' B 208  SER  HB3', -0.494, (-27.676, 24.864, 73.1)), (' B 179  LEU  HG ', ' B 181  LEU HD11', -0.493, (-16.187, 21.963, 73.668)), (' E 418  ILE  HA ', ' E 422  ASN HD22', -0.493, (8.775, -6.247, 26.024)), (' B  33  LEU HD22', ' B  71  PHE  CD2', -0.492, (-13.763, 3.216, 32.138)), (' A  22  CYS  HB3', ' A  78  LEU  HB3', -0.491, (3.621, -11.945, 49.603)), (' A  94  ARG  NH2', ' E 489  TYR  OH ', -0.489, (-3.56, -15.151, 36.27)), (' B   6  GLN  N  ', ' B 100  GLN HE22', -0.488, (-14.713, 9.923, 41.594)), (' B  47  LEU HD23', ' B  58  ILE HD12', -0.484, (-16.773, -9.152, 40.801)), (' A 150  VAL  O  ', ' A 150  VAL HG23', -0.483, (-13.669, -0.036, 72.392)), (' A  33  TYR  CD2', ' A  97  GLY  HA2', -0.481, (2.698, -9.27, 34.931)), (' A 178  LEU  O  ', ' A 178  LEU HD23', -0.478, (-16.475, 5.584, 73.084)), (' E 403  ARG  CZ ', ' E 505  TYR  CD1', -0.476, (-0.016, 1.563, 26.0)), (' B 142  ARG  HG2', ' B 142  ARG  O  ', -0.476, (-24.212, 11.448, 56.792)), (' A  27  PHE  O  ', ' A  28  ILE HD13', -0.474, (3.124, -20.83, 43.591)), (' E 371  SER  O  ', ' E 372  ALA  HB3', -0.473, (12.784, 16.367, 9.156)), (' B 113  PRO  HB3', ' B 139  PHE  HB3', -0.471, (-31.096, 12.132, 62.858)), (' A  51  ILE HG13', ' A  57  THR HG22', -0.47, (10.456, -7.185, 41.827)), (' A  33  TYR  CE2', ' A  97  GLY  HA2', -0.469, (2.578, -9.45, 34.418)), (' B 201  LEU HD13', ' B 205  VAL  CG2', -0.461, (-34.336, 19.245, 64.819)), (' A  99  TYR  OH ', ' E 453  TYR  OH ', -0.46, (0.19, -4.917, 28.724)), (' E 403  ARG  NH1', ' E 505  TYR  HE1', -0.459, (-0.393, 0.186, 26.463)), (' E 403  ARG  CZ ', ' E 505  TYR  HD1', -0.459, (0.323, 2.142, 26.528)), (' B 186  TYR  HA ', ' B 192  TYR  OH ', -0.457, (-17.019, 25.624, 79.084)), (' B 175  LEU  C  ', ' B 175  LEU HD23', -0.456, (-23.105, 12.039, 65.911)), (' E 398  ASP  O  ', ' E 511  VAL  HA ', -0.456, (15.075, -1.13, 13.953)), (' B 181  LEU  N  ', ' B 181  LEU HD12', -0.452, (-13.925, 21.423, 75.355)), (' A   3  GLN  O  ', ' A   4  LEU HD23', -0.451, (-2.034, -16.688, 47.821)), (' A  39  GLN  C  ', ' A  88  ALA  HB1', -0.448, (-3.954, 1.902, 54.207)), (' A 184  VAL  HB ', ' A 185  PRO  HD2', -0.445, (-34.47, 1.856, 78.032)), (' B 142  ARG  HB2', ' B 173  TYR  CD1', -0.445, (-26.413, 8.087, 56.717)), (' A 148  GLU  HB3', ' A 149  PRO  HA ', -0.444, (-9.231, -0.545, 69.04)), (' B  80  PRO  HA ', ' B  83  PHE  CE1', -0.443, (-28.923, -4.734, 49.312)), (' A  36  TRP  CZ3', ' A  92  CYS  HB3', -0.44, (1.174, -8.25, 50.603)), (' B 154  LEU  N  ', ' B 154  LEU HD12', -0.439, (-21.709, 30.859, 67.293)), (' E 452  LEU  CD2', ' E 494  SER  HA ', -0.438, (-1.467, -8.862, 20.363)), (' E 366  SER  OG ', ' E 388  ASN  ND2', -0.436, (27.301, 11.917, 7.944)), (' B 167  ASP  HB3', ' B 170  ASP  OD1', -0.436, (-30.832, 0.877, 61.19)), (' A  48  VAL HG13', ' A  63  VAL HG21', -0.436, (5.445, 1.773, 48.175)), (' B 163  VAL HG22', ' B 175  LEU HD12', -0.433, (-22.125, 11.417, 61.41)), (' A 124  LEU  HB3', ' B 118  PHE  CD1', -0.428, (-24.41, 11.274, 77.842)), (' B  61  ARG  CZ ', ' B  79  GLU  HG3', -0.426, (-26.531, -9.869, 42.919)), (' B  47  LEU  O  ', ' B  48  ILE HD12', -0.426, (-16.237, -7.076, 36.55)), (' A  99  TYR  CE1', ' E 417  LYS  NZ ', -0.426, (0.616, -4.241, 31.064)), (' B  21  LEU  HG ', ' B 102  THR HG21', -0.426, (-21.201, 4.66, 42.078)), (' E 350  VAL  HA ', ' E 400  PHE  HB2', -0.424, (8.999, -5.056, 17.835)), (' B  75  ILE HG21', ' B  78  LEU  CD1', -0.424, (-25.983, -3.589, 41.942)), (' B  35  TRP  CZ3', ' B  88  CYS  HB3', -0.423, (-15.086, 2.595, 38.52)), (' B  11  LEU  N  ', ' B 103  LYS  O  ', -0.42, (-23.753, 5.74, 46.963)), (' A   2  VAL HG21', ' E 486  PHE  CE2', -0.419, (-5.529, -20.256, 41.136)), (' A  32  ASN  OD1', ' E 475  ALA  HB1', -0.416, (0.847, -16.766, 37.466)), (' B  85  VAL  HA ', ' B 102  THR  O  ', -0.416, (-18.862, 2.431, 46.791)), (' B   6  GLN  H  ', ' B 100  GLN HE22', -0.414, (-14.326, 9.664, 41.817)), (' A  63  VAL HG11', ' A  67  PHE  CE2', -0.414, (5.287, 2.642, 50.763)), (' E 419  ALA  O  ', ' E 424  LYS  HD3', -0.412, (15.625, -6.053, 28.671)), (' A  59  TYR  CE1', ' A  69  ILE HG22', -0.411, (9.87, -2.647, 45.832)), (' A  36  TRP  HD1', ' A  69  ILE HD12', -0.411, (5.54, -5.663, 46.699)), (' E 431  GLY  HA3', ' E 513  LEU  O  ', -0.409, (23.892, 1.097, 17.512)), (' B  89  GLN  HG2', ' B  90  GLN  N  ', -0.408, (-6.585, 1.964, 37.795)), (' B  23  CYS  HB2', ' B  35  TRP  CH2', -0.407, (-15.917, 4.368, 37.535)), (' B 179  LEU  HG ', ' B 181  LEU  CD1', -0.406, (-16.097, 22.066, 74.204)), (' E 390  LEU  N  ', ' E 390  LEU HD22', -0.406, (33.247, 7.349, 11.871)), (' A   2  VAL  HA ', ' A  25  SER  O  ', -0.404, (-3.54, -20.413, 45.728)), (' E 364  ASP  OD1', ' E 367  VAL HG13', -0.403, (23.488, 11.041, 4.249)), (' A 139  GLY  HA2', ' A 154  TRP  CZ2', -0.401, (-23.843, 3.936, 77.579)), (' E 335  LEU  N  ', ' E 335  LEU HD12', -0.4, (25.419, 2.926, -2.751)), (' E 416  GLY  O  ', ' E 420  ASP  HB2', -0.4, (10.452, -5.887, 30.266))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
