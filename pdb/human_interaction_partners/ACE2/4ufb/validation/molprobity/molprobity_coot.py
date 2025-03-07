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
data['rama'] = [('A', '  78 ', 'PRO', 0.057491265739622, (10.274000000000001, 10.782000000000002, -33.985)), ('A', ' 416 ', 'ASN', 0.01587277043737806, (19.562, 36.292, 21.825)), ('B', '  45 ', 'ASN', 0.038143227526317026, (-49.286999999999985, 78.304, -65.127))]
data['omega'] = [('A', ' 141 ', 'PRO', None, (-13.512999999999991, 33.5, 6.155)), ('A', ' 608 ', 'PRO', None, (-24.780000000000005, 16.643, 18.891)), ('B', ' 141 ', 'PRO', None, (-44.438, 75.419, -50.387)), ('B', ' 608 ', 'PRO', None, (-54.897999999999996, 58.872, -37.168)), ('C', ' 141 ', 'PRO', None, (8.137, 70.316, 18.196)), ('C', ' 608 ', 'PRO', None, (0.47999999999999865, 89.213, 30.065)), ('D', ' 141 ', 'PRO', None, (-37.796, 11.645999999999999, -39.59)), ('D', ' 608 ', 'PRO', None, (-45.092000000000006, 30.203, -27.69))]
data['rota'] = [('A', ' 147 ', 'LEU', 0.0957269316681718, (-10.004, 26.073999999999998, 14.062)), ('A', ' 368 ', 'TYR', 0.2517203390791505, (8.844999999999999, 34.04, -11.009)), ('A', ' 372 ', 'TYR', 0.055512632839902876, (10.524999999999999, 34.615, -17.04)), ('A', ' 377 ', 'VAL', 0.06361953331118544, (5.123999999999999, 30.487, -23.36)), ('B', '  25 ', 'GLN', 0.13794262566727947, (-30.158999999999995, 73.929, -87.165)), ('B', ' 187 ', 'LYS', 0.03929136852625598, (-36.975, 49.966, -79.39)), ('B', ' 368 ', 'TYR', 0.2893064730512139, (-23.436, 76.005, -69.121)), ('B', ' 372 ', 'TYR', 0.05575836166755524, (-22.148999999999994, 76.797, -75.33000000000001)), ('B', ' 377 ', 'VAL', 0.15819049310494315, (-28.016999999999996, 73.024, -81.538)), ('B', ' 418 ', 'THR', 0.17542341902468456, (-10.503, 70.443, -35.269)), ('B', ' 421 ', 'ASP', 0.23082440322879072, (-13.704999999999997, 71.217, -38.826)), ('C', ' 372 ', 'TYR', 0.0578780020372409, (23.276999999999997, 63.476, -10.844000000000001)), ('C', ' 388 ', 'HIS', 0.12382716075312995, (16.244, 72.025, -6.592)), ('C', ' 414 ', 'VAL', 0.149870345591133, (-15.21, 62.257, -4.312)), ('C', ' 421 ', 'ASP', 0.28369838471086434, (-13.158999999999997, 73.067, -6.86)), ('D', '   2 ', 'ASP', 0.2354308287816335, (1.104, 6.964999999999999, -54.32)), ('D', ' 326 ', 'ARG', 0.04222984190818831, (-26.739999999999995, 6.711999999999998, -35.011)), ('D', ' 372 ', 'TYR', 0.05688339687176444, (-22.921, 4.759999999999999, -68.651)), ('D', ' 377 ', 'VAL', 0.13036222697275857, (-14.703, 8.242999999999999, -65.927)), ('D', ' 388 ', 'HIS', 0.18080932187301801, (-29.823999999999998, 13.383999999999997, -64.411)), ('C', '1303 ', 'LYS', 0.031995342394133805, (12.045, 73.13600000000001, 3.39))]
data['cbeta'] = []
data['probe'] = [(' D 235  ARG HH11', ' D1201  P6G H172', -0.921, (-62.859, 26.541, -52.238)), (' C 365  HIS  HD1', ' C 388  HIS  HD2', -0.88, (16.676, 69.762, -4.434)), (' B 292  HIS  HE2', ' B1203  P6G  H31', -0.833, (-32.636, 94.014, -51.319)), (' C 236  ARG  HD2', ' C 267  MET  HE3', -0.793, (-10.666, 82.651, 13.568)), (' C 365  HIS  HD1', ' C 388  HIS  CD2', -0.77, (16.966, 70.215, -4.324)), (' D 235  ARG  NH1', ' D1201  P6G H172', -0.754, (-63.082, 25.841, -51.987)), (' A 157  LEU HD11', ' A 477  VAL HG13', -0.683, (-16.395, 14.978, 15.241)), (' B 274  LYS  HB3', ' B 275  PRO  HD2', -0.675, (-18.05, 76.462, -33.519)), (' D 157  LEU HD11', ' D 477  VAL HG13', -0.67, (-43.65, 31.532, -37.015)), (' A 147  LEU HD22', ' A 256  MET  HA ', -0.66, (-9.625, 22.718, 10.305)), (' D1100  NAG  H3 ', ' D1100  NAG  H83', -0.63, (-31.395, 38.433, -32.807)), (' C 539  LYS  HE3', ' C 559  MET  O  ', -0.618, (8.794, 69.355, -21.112)), (' D 155  MET  HA ', ' D 155  MET  HE3', -0.607, (-46.863, 22.463, -33.266)), (' B 233  LEU HD23', ' B 267  MET  HE1', -0.605, (-33.205, 62.897, -35.082)), (' D 482  THR  OG1', ' D1100  NAG  H81', -0.584, (-28.753, 38.91, -34.643)), (' C 157  LEU HD11', ' C 477  VAL HG13', -0.583, (2.176, 90.712, 20.855)), (' B 539  LYS  HE3', ' B 559  MET  O  ', -0.581, (-8.294, 70.534, -64.895)), (' C 274  LYS  HB3', ' C 275  PRO  CD ', -0.579, (-17.331, 69.153, -1.143)), (' A 206  THR HG23', ' A 210  ASP  OD2', -0.572, (15.568, 10.052, -7.815)), (' B 157  LEU HD11', ' B 477  VAL HG13', -0.565, (-47.058, 56.31, -41.526)), (' C 236  ARG  CD ', ' C 267  MET  HE3', -0.551, (-10.975, 82.226, 13.549)), (' D 228  PHE  CZ ', ' D1201  P6G H142', -0.547, (-61.182, 25.269, -55.291)), (' D 268  VAL HG12', ' D 426  LEU HD11', -0.543, (-56.264, 21.814, -55.382)), (' A  31  VAL  O  ', ' A  34  GLN  HG3', -0.541, (-6.883, 32.037, -24.834)), (' D 274  LYS  HB3', ' D 275  PRO  CD ', -0.54, (-62.808, 10.299, -58.809)), (' B 522  GLU  OE1', ' B1106  BMA  H3 ', -0.539, (2.174, 76.059, -50.276)), (' D 482  THR  OG1', ' D1100  NAG  C8 ', -0.538, (-29.214, 38.445, -35.115)), (' C 117  GLN HE22', ' C 120  ARG  HE ', -0.527, (26.993, 78.449, 21.224)), (' A 172  LYS  O  ', ' A 176  GLU  HG3', -0.523, (-16.888, 10.778, -7.471)), (' B 292  HIS  NE2', ' B1203  P6G  H31', -0.522, (-32.877, 93.099, -51.028)), (' B  71  LYS  O  ', ' B  75  LEU  HB2', -0.52, (-30.958, 61.332, -95.903)), (' D 541 BARG  HE ', ' D 545  ARG  HD2', -0.519, (-27.576, 0.875, -73.775)), (' B 139  LEU HD22', ' B 163  TRP  CZ2', -0.515, (-44.586, 66.361, -54.117)), (' D 236  ARG  HD3', ' D 267  MET  SD ', -0.512, (-56.886, 23.149, -45.133)), (' A 495  VAL  O  ', ' A 495  VAL HG12', -0.511, (-5.438, 19.943, -11.329)), (' C 191  PHE  CZ ', ' C1200  PEG  H31', -0.505, (31.52, 86.086, -9.162)), (' B 157  LEU HD13', ' B 476  PRO  HB2', -0.502, (-44.417, 57.138, -40.593)), (' D  31  VAL  O  ', ' D  34  GLN  HG3', -0.501, (-10.244, 7.54, -53.852)), (' A 510  GLN  HG2', ' A 569  PRO  HG2', -0.497, (19.544, 21.45, 0.959)), (' B1201  PEG  H32', ' D 465  TYR  CE2', -0.495, (-34.845, 41.376, -55.9)), (' B 292  HIS  NE2', ' B1203  P6G  H51', -0.495, (-32.621, 92.619, -50.114)), (' C  31  VAL  O  ', ' C  34  GLN  HG3', -0.493, (35.883, 66.143, 3.953)), (' D 495  VAL  O  ', ' D 495  VAL HG12', -0.492, (-21.731, 22.209, -53.794)), (' A 362  GLU  OE2', ' A1303  LYS  N  ', -0.489, (-1.06, 30.472, -2.573)), (' D 414  VAL HG13', ' D2320  HOH  O  ', -0.486, (-58.514, 3.768, -63.724)), (' A 157  LEU HD13', ' A 476  PRO  HB2', -0.481, (-14.334, 15.514, 16.418)), (' A 292  HIS  HE2', ' A1202  P6G  H82', -0.477, (-1.803, 51.549, 3.974)), (' C 117  GLN  NE2', ' C 120  ARG  HE ', -0.471, (26.772, 78.662, 20.734)), (' B 296  VAL HG22', ' B1203  P6G H172', -0.471, (-24.51, 88.712, -53.169)), (' A 141  PRO  HB3', ' A 350  ARG  HD3', -0.469, (-11.113, 35.202, 7.537)), (' B 582  GLN  HG2', ' B 586  GLN  NE2', -0.463, (-14.323, 52.783, -37.347)), (' C 157  LEU HD13', ' C 476  PRO  HB2', -0.463, (0.463, 89.396, 19.246)), (' B 292  HIS  CE1', ' B1203  P6G  H51', -0.459, (-33.01, 92.768, -49.613)), (' B1201  PEG  H42', ' B2382  HOH  O  ', -0.458, (-31.839, 43.959, -57.619)), (' D 231  ARG  HG3', ' D1201  P6G H171', -0.456, (-61.941, 28.879, -51.743)), (' B 426  LEU  HG ', ' B 426  LEU  O  ', -0.455, (-22.496, 65.93, -40.633)), (' A  49  GLU  HG2', ' A1103  NAG  H82', -0.454, (-23.634, 36.237, -17.829)), (' B 495  VAL  O  ', ' B 495  VAL HG12', -0.454, (-38.114, 61.799, -68.378)), (' C 274  LYS  HB3', ' C 275  PRO  HD2', -0.451, (-16.538, 68.999, -0.85)), (' B 270  PRO  HD3', ' B 426  LEU HD22', -0.447, (-22.418, 66.593, -36.677)), (' D 235  ARG HH11', ' D1201  P6G  C17', -0.447, (-62.985, 27.272, -51.558)), (' A 324  ASP  OD1', ' A 326  ARG  HB2', -0.443, (-18.674, 40.173, -4.251)), (' A 389  GLU  HB2', ' A 504  SER  HB2', -0.442, (7.37, 24.197, -3.392)), (' A 233  LEU HD23', ' A 267  MET  HE1', -0.442, (-3.19, 21.351, 22.997)), (' C 372  TYR  OH ', ' C 388  HIS  HE1', -0.44, (21.693, 68.777, -6.187)), (' D 389  GLU  HB2', ' D 504  SER  HB2', -0.438, (-33.709, 17.533, -63.15)), (' A 372  TYR  HB2', ' A 375  LEU HD12', -0.437, (10.853, 32.132, -18.14)), (' A 333  SER  HB2', ' A1204  P6G  H22', -0.437, (-3.635, 30.618, -8.109)), (' B 267  MET  HB3', ' B 267  MET  HE2', -0.436, (-31.211, 64.898, -33.772)), (' D1101  FUC  H5 ', ' D2359  HOH  O  ', -0.435, (-38.826, 36.336, -34.506)), (' D 453  ARG  HD2', ' D2347  HOH  O  ', -0.434, (-26.743, 43.486, -58.095)), (' B 570  LEU  C  ', ' B 570  LEU HD23', -0.433, (-15.194, 61.984, -50.618)), (' B 232  ALA  CB ', ' B 268  VAL HG12', -0.429, (-28.537, 62.812, -34.226)), (' D 362  GLU  OE2', ' D1303  LYS  N  ', -0.428, (-33.064, 12.247, -54.332)), (' A 270  PRO  HD2', ' A 423  ASN  OD1', -0.428, (9.36, 28.558, 23.726)), (' B 465  TYR  CE2', ' B1201  PEG  H31', -0.427, (-33.409, 43.643, -54.562)), (' D   9 AGLN  NE2', ' D  75  LEU HD21', -0.425, (5.382, 15.516, -70.699)), (' A 267  MET  HB3', ' A 267  MET  HE2', -0.425, (-0.781, 23.629, 23.174)), (' B 489  LYS  O  ', ' B 493  PRO  HD2', -0.424, (-41.274, 61.73, -59.496)), (' D 332  ALA  HB3', ' D1303  LYS  HB2', -0.423, (-34.632, 12.514, -52.189)), (' A  69  GLY  HA3', ' A  98  LEU HD11', -0.422, (-1.221, 17.728, -29.867)), (' C 598  GLN  HB2', ' C2420  HOH  O  ', -0.421, (-1.405, 104.002, 9.956)), (' B 212  GLU  HG2', ' D 453  ARG  NH2', -0.42, (-22.082, 45.975, -58.879)), (' C  77  GLU  HA ', ' C  77  GLU  OE1', -0.418, (42.275, 82.158, -14.092)), (' B 141  PRO  HB3', ' B 350  ARG  HD3', -0.418, (-41.511, 76.944, -49.102)), (' B 390  ALA  O  ', ' B 394  VAL HG23', -0.418, (-19.821, 71.082, -59.575)), (' D 521  TYR  CD2', ' D 528  CYS  HB2', -0.418, (-50.024, 8.884, -73.529)), (' D 274  LYS  HB3', ' D 275  PRO  HD2', -0.416, (-62.592, 10.447, -58.803)), (' A 376  PRO  HD2', ' A 379  LEU HD12', -0.412, (11.569, 29.51, -23.738)), (' B 292  HIS  HE2', ' B1203  P6G  C3 ', -0.411, (-32.081, 94.186, -50.812)), (' B  25  GLN  OE1', ' B 376  PRO  HA ', -0.411, (-25.597, 74.558, -84.372)), (' A 607  TYR  HA ', ' A 608  PRO  HA ', -0.408, (-23.502, 17.832, 20.572)), (' B 172  LYS  O  ', ' B 176  GLU  HG3', -0.407, (-49.106, 52.718, -63.744)), (' B 409  GLY  HA2', ' B2277  HOH  O  ', -0.407, (-20.364, 88.254, -42.357)), (' D 607  TYR  HA ', ' D 608  PRO  HA ', -0.406, (-47.145, 29.334, -28.449)), (' C 117  GLN  NE2', ' C 120  ARG HH21', -0.405, (26.759, 79.66, 21.161)), (' B 270  PRO  HB3', ' B 580  TRP  CH2', -0.404, (-19.213, 65.137, -33.732)), (' D 139  LEU HD22', ' D 163  TRP  CZ2', -0.403, (-33.797, 19.695, -42.065)), (' C 489  LYS  O  ', ' C 493  PRO  HD2', -0.403, (17.143, 82.189, 10.609)), (' D  32  LEU HD23', ' D2023  HOH  O  ', -0.402, (-13.116, 11.633, -56.336)), (' B 218  LEU HD13', ' B 436  LEU HD13', -0.401, (-20.706, 58.182, -52.487)), (' C 117  GLN HE21', ' C 120  ARG HH21', -0.401, (26.431, 80.004, 21.194)), (' C1202  P6G H111', ' C2279  HOH  O  ', -0.401, (17.591, 70.825, 2.24)), (' D 268  VAL  CG1', ' D 426  LEU HD11', -0.4, (-55.8, 22.041, -55.372))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
