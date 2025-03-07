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
data['rama'] = [('A', '  45 ', 'ASN', 0.03511391673893046, (-17.092, 35.921, -9.064)), ('A', ' 326 ', 'ARG', 0.0200642901667226, (-19.901, 37.784, -4.531)), ('B', '  45 ', 'ASN', 0.028265051957013076, (-48.81300000000001, 78.18299999999998, -64.993)), ('B', ' 413 ', 'ARG', 0.002102496799087085, (-15.349000000000002, 83.846, -38.299000000000014)), ('C', '  45 ', 'ASN', 0.042956237977227835, (23.242, 65.94400000000002, 18.227)), ('D', '  45 ', 'ASN', 0.017406542793266977, (-22.46699999999999, 7.110999999999999, -39.67))]
data['omega'] = [('A', ' 141 ', 'PRO', None, (-13.613, 33.315, 6.247)), ('A', ' 608 ', 'PRO', None, (-24.815, 16.822, 18.976)), ('B', ' 141 ', 'PRO', None, (-43.950999999999986, 75.27599999999997, -50.27400000000001)), ('B', ' 608 ', 'PRO', None, (-54.368, 58.620000000000005, -36.851)), ('C', ' 141 ', 'PRO', None, (8.215999999999998, 70.266, 18.28000000000001)), ('C', ' 608 ', 'PRO', None, (0.38199999999999656, 89.135, 30.110000000000003)), ('D', ' 141 ', 'PRO', None, (-37.5, 11.503999999999998, -39.572)), ('D', ' 608 ', 'PRO', None, (-44.75199999999999, 30.04599999999999, -27.616000000000007))]
data['rota'] = [('A', ' 147 ', 'LEU', 0.26936056245992757, (-10.079, 25.920999999999996, 14.161000000000003)), ('A', ' 281 ', 'SER', 0.26531891624677756, (-1.8689999999999993, 41.434000000000005, 17.875)), ('A', ' 368 ', 'TYR', 0.264747218682239, (9.038999999999996, 33.967, -10.892)), ('A', ' 372 ', 'TYR', 0.09909130265487276, (10.771999999999997, 34.501, -16.949)), ('A', ' 388 ', 'HIS', 0.27245477137988683, (7.745000000000001, 27.486999999999995, -7.815000000000001)), ('A', ' 542 ', 'LYS', 0.11726665020000655, (19.549, 33.26, -11.914000000000003)), ('B', ' 187 ', 'LYS', 0.02225923072325701, (-36.484999999999985, 49.892999999999994, -79.34300000000002)), ('B', ' 368 ', 'TYR', 0.2893819921357882, (-22.933000000000007, 76.01899999999999, -69.19200000000001)), ('B', ' 372 ', 'TYR', 0.09548930294592044, (-21.713, 76.692, -75.27700000000003)), ('B', ' 388 ', 'HIS', 0.09728798869185759, (-23.912000000000003, 69.506, -66.143)), ('B', ' 535 ', 'LYS', 0.15304251295198631, (-7.028000000000001, 80.792, -63.445)), ('B', ' 606 ', 'ASN', 0.1685550596434093, (-54.033, 57.763, -31.572)), ('C', ' 174 ', 'LEU', 0.15127438024558518, (26.753, 87.33, 15.905000000000001)), ('C', ' 368 ', 'TYR', 0.2807028621721461, (18.214999999999996, 65.114, -7.617000000000001)), ('C', ' 372 ', 'TYR', 0.07035331819426091, (23.414999999999992, 63.45, -10.753)), ('C', ' 388 ', 'HIS', 0.1679483935957652, (16.347999999999995, 71.93299999999998, -6.4860000000000015)), ('C', ' 421 ', 'ASP', 0.28117602866237607, (-12.975, 73.054, -6.769)), ('C', ' 535 ', 'LYS', 0.10751658463916368, (6.797999999999997, 59.66300000000001, -19.866)), ('D', ' 187 ', 'LYS', 0.024925304890389532, (-10.689, 31.837999999999997, -59.79900000000001)), ('D', ' 236 ', 'ARG', 0.2799114375969726, (-59.369, 26.382, -43.134)), ('D', ' 368 ', 'TYR', 0.2909106022134086, (-27.83, 6.265999999999994, -65.53500000000001)), ('D', ' 372 ', 'TYR', 0.05615139836483723, (-22.614, 4.536999999999996, -68.675)), ('D', ' 388 ', 'HIS', 0.12020444888687018, (-29.496999999999996, 13.141999999999992, -64.381))]
data['cbeta'] = []
data['probe'] = [(' B 233  LEU HD23', ' B 267  MET  HE1', -0.803, (-33.252, 63.197, -35.077)), (' B 270  PRO  HD3', ' B 426  LEU HD22', -0.751, (-21.763, 66.59, -36.993)), (' A 233  LEU HD23', ' A 267  MET  HE1', -0.748, (-3.636, 21.083, 22.196)), (' A 147  LEU HD22', ' A 256  MET  HA ', -0.745, (-10.351, 22.311, 10.911)), (' C 206  THR HG23', ' C 210  ASP  OD2', -0.727, (16.388, 88.949, -16.774)), (' A 206  THR HG23', ' A 210  ASP  OD2', -0.706, (15.042, 10.012, -7.863)), (' B 365  HIS  HD1', ' B 388  HIS  CD2', -0.702, (-26.829, 71.823, -66.808)), (' D 206  THR HG23', ' D 210  ASP  OD2', -0.694, (-29.917, 29.89, -74.444)), (' C 453  ARG  NH1', ' C2414  HOH  O  ', -0.685, (23.684, 103.918, -0.778)), (' C 413  ARG  NH2', ' C2379  HOH  O  ', -0.66, (-9.689, 58.342, -7.798)), (' A 539  LYS  HE3', ' A 559  MET  O  ', -0.653, (23.367, 29.143, -5.324)), (' C 176  GLU  OE1', ' C2196  HOH  O  ', -0.651, (27.176, 95.21, 13.975)), (' B 354  ASP  OD2', ' B2315  HOH  O  ', -0.631, (-32.614, 72.901, -50.373)), (' B 206  THR HG23', ' B 210  ASP  OD2', -0.618, (-16.379, 51.424, -67.454)), (' C 426  LEU  HG ', ' C 426  LEU  O  ', -0.61, (-7.622, 78.959, -0.28)), (' A1201  PEG  O4 ', ' A1202  P6G  O19', -0.604, (5.787, 49.091, 7.771)), (' B 365  HIS  HD1', ' B 388  HIS  HD2', -0.601, (-26.098, 72.018, -66.376)), (' C 245  ARG  HG2', ' C 591  VAL HG11', -0.591, (-10.263, 99.014, 4.25)), (' B 596  GLU  OE2', ' D1100  NAG  O7 ', -0.589, (-31.55, 42.378, -34.023)), (' C1101  FUC  H4 ', ' C2505  HOH  O  ', -0.585, (5.079, 94.594, 24.493)), (' B 157  LEU HD11', ' B 477  VAL HG13', -0.581, (-46.672, 56.099, -41.342)), (' C 236  ARG  HD2', ' C 267  MET  HE3', -0.573, (-9.969, 82.437, 13.022)), (' D 235  ARG HH11', ' D1201  P6G H172', -0.57, (-62.778, 26.326, -51.985)), (' D 157  LEU HD11', ' D 477  VAL HG13', -0.547, (-43.156, 31.744, -36.855)), (' C 274  LYS  HB3', ' C 275  PRO  CD ', -0.535, (-16.724, 68.821, -1.158)), (' B 412  ASP  O  ', ' B 413  ARG  CB ', -0.532, (-15.317, 85.887, -38.239)), (' D 188  GLN  HG2', ' D2186  HOH  O  ', -0.53, (-4.954, 30.51, -59.741)), (' D 275  PRO  HG3', ' D 413  ARG  HG2', -0.522, (-62.837, 6.39, -58.739)), (' D 235  ARG HH12', ' D1201  P6G H112', -0.518, (-62.964, 24.315, -52.075)), (' A 172  LYS  O  ', ' A 176  GLU  HG3', -0.507, (-16.878, 10.663, -7.4)), (' B1100  NAG  O7 ', ' D 596  GLU  OE2', -0.502, (-54.095, 44.851, -49.315)), (' A 187  LYS  HE3', ' A2178  HOH  O  ', -0.501, (-3.661, 2.882, -18.583)), (' D 274  LYS  HB3', ' D 275  PRO  CD ', -0.499, (-62.833, 10.48, -58.953)), (' D 579  GLN  NE2', ' D 583  GLU  OE2', -0.497, (-61.355, 28.601, -69.421)), (' B 232  ALA  CB ', ' B 268  VAL HG12', -0.497, (-28.007, 62.814, -34.683)), (' C 539  LYS  HE3', ' C 559  MET  O  ', -0.494, (9.101, 69.32, -20.803)), (' A 389  GLU  HB2', ' A 504  SER  HB2', -0.493, (7.359, 24.088, -3.304)), (' C 151  ARG  HD2', ' C 267  MET  SD ', -0.492, (-8.433, 79.157, 13.887)), (' A  77  GLU  N  ', ' A  78  PRO  HD2', -0.492, (8.049, 13.352, -35.535)), (' A1201  PEG  H22', ' A2389  HOH  O  ', -0.489, (7.419, 50.558, 5.959)), (' B 412  ASP  O  ', ' B 413  ARG  HB3', -0.488, (-15.166, 85.853, -37.487)), (' D 340 BARG  HG2', ' D 373  LYS  O  ', -0.481, (-17.883, 1.519, -65.872)), (' B 489  LYS  O  ', ' B 493  PRO  HD2', -0.481, (-40.898, 61.81, -59.426)), (' D 270  PRO  HD3', ' D 426  LEU HD22', -0.48, (-57.671, 20.774, -56.577)), (' A 155  MET  HA ', ' A 155  MET  HE3', -0.48, (-18.117, 23.962, 17.855)), (' A 489  LYS  O  ', ' A 493  PRO  HD2', -0.478, (-9.636, 19.551, -2.756)), (' D  83  PHE  HA ', ' D2006  HOH  O  ', -0.469, (-5.797, 17.046, -81.95)), (' B  31  VAL  O  ', ' B  34  GLN  HG3', -0.46, (-40.407, 74.454, -81.322)), (' D 495  VAL  O  ', ' D 495  VAL HG12', -0.458, (-21.66, 21.754, -53.562)), (' D  31  VAL  O  ', ' D  34  GLN  HG3', -0.454, (-10.299, 7.605, -54.186)), (' C  77  GLU  OE2', ' C  96  ARG  NH2', -0.45, (40.479, 84.329, -11.896)), (' D 235  ARG  NH1', ' D1201  P6G H172', -0.448, (-63.033, 25.996, -51.623)), (' C 135  THR  O  ', ' C 135  THR HG23', -0.447, (7.216, 75.085, 31.631)), (' B 372  TYR  OH ', ' B 388  HIS  HE1', -0.443, (-25.936, 72.278, -71.026)), (' D  80  TRP  CE2', ' D  81  GLN  HG3', -0.441, (-8.221, 22.845, -74.576)), (' C 245  ARG  HG2', ' C 591  VAL  CG1', -0.439, (-9.876, 98.562, 4.01)), (' A 232  ALA  CB ', ' A 268  VAL HG12', -0.439, (1.118, 21.574, 23.817)), (' C 570  LEU  C  ', ' C 570  LEU HD23', -0.437, (-0.701, 81.097, -10.662)), (' C  25  GLN  OE1', ' C 376  PRO  HA ', -0.437, (33.139, 64.569, -11.183)), (' A  31  VAL  O  ', ' A  34  GLN  HG3', -0.436, (-6.778, 31.899, -24.56)), (' B 426  LEU  HG ', ' B 426  LEU  O  ', -0.434, (-21.953, 65.717, -40.732)), (' D 139  LEU HD22', ' D 163  TRP  CZ2', -0.434, (-33.32, 19.85, -41.754)), (' C 541 BARG  NH1', ' C2316  HOH  O  ', -0.434, (16.526, 56.784, -13.328)), (' A  49  GLU  HG2', ' A1102  NAG  H82', -0.432, (-23.497, 36.126, -17.584)), (' C 259  GLN  O  ', ' C 435  PHE  HA ', -0.432, (4.067, 82.143, 2.535)), (' B 157  LEU HD13', ' B 476  PRO  HB2', -0.426, (-44.537, 57.097, -40.429)), (' D 606  ASN  O  ', ' D 609  GLU  N  ', -0.425, (-47.085, 29.609, -25.893)), (' B  60  LEU HD11', ' B2001  HOH  O  ', -0.425, (-45.115, 72.249, -87.909)), (' C 332  ALA  HB3', ' R   7  ASP  HB2', -0.424, (11.8, 71.087, 5.346)), (' D 270  PRO  HD3', ' D 426  LEU  CD2', -0.42, (-57.296, 20.373, -56.345)), (' C 117  GLN HE22', ' C 120  ARG  HE ', -0.42, (26.61, 78.148, 21.164)), (' B2323  HOH  O  ', ' Q   7  ASP  N  ', -0.417, (-31.954, 71.155, -61.306)), (' A2288  HOH  O  ', ' P   7  ASP  N  ', -0.416, (-0.674, 29.032, -3.533)), (' A 157  LEU HD11', ' A 477  VAL HG13', -0.414, (-16.742, 14.327, 15.581)), (' B  77  GLU  HB3', ' B  78  PRO  HD3', -0.414, (-27.152, 54.805, -94.278)), (' D 324  ASP  OD1', ' D 326  ARG  HB2', -0.412, (-26.915, 3.958, -35.61)), (' C 489  LYS  O  ', ' C 493  PRO  HD2', -0.411, (17.228, 82.482, 10.622)), (' D 415  THR  OG1', ' D 417  ASP  OD2', -0.411, (-64.764, 9.145, -63.225)), (' C  31  VAL  O  ', ' C  34  GLN  HG3', -0.409, (35.52, 66.485, 3.945)), (' A 390  ALA  O  ', ' A 394  VAL HG23', -0.408, (11.929, 29.224, -0.934)), (' D 441  LEU  C  ', ' D 441  LEU HD12', -0.408, (-33.813, 30.677, -55.042)), (' A 139  LEU HD22', ' A 163  TRP  CZ2', -0.407, (-13.481, 24.468, 2.817)), (' C  77  GLU  HA ', ' C  77  GLU  OE1', -0.406, (42.437, 82.27, -13.661)), (' B 267  MET  HB3', ' B 267  MET  HE2', -0.402, (-30.855, 64.749, -33.773)), (' B 562  LEU HD23', ' B 564  ALA  O  ', -0.401, (-11.124, 59.919, -63.264)), (' A1203  PEG  H41', ' A2127  HOH  O  ', -0.4, (3.194, 25.364, -11.607)), (' B 390  ALA  O  ', ' B 394  VAL HG23', -0.4, (-19.25, 70.827, -60.215))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
