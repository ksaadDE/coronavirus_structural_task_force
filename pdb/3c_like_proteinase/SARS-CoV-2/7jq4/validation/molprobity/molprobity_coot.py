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
data['rama'] = [('A', ' 154 ', 'TYR', 0.012540777730235056, (11.124000000000006, -10.38, -8.013)), ('A', ' 217 ', 'ARG', 0.030442173869419258, (6.353000000000001, 20.619999999999997, 0.356)), ('A', ' 222 ', 'ARG', 0.04873558568766095, (1.1340000000000003, 28.591, -7.299))]
data['omega'] = [('A', ' 222 ', 'ARG', None, (2.299000000000001, 27.731999999999996, -7.197))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' A   6  MET  HE3', ' A 299  GLN HE21', -0.929, (14.232, 2.62, 0.132)), (' A 191  ALA  HA ', ' A 401  XM2  C5 ', -0.835, (43.483, 9.473, -20.059)), (' A   6  MET  HE3', ' A 299  GLN  NE2', -0.773, (14.026, 3.209, -0.469)), (' A 208  LEU HD13', ' A 264  MET  HE2', -0.753, (9.101, 19.816, -8.2)), (' A 217  ARG  HG3', ' A 220  LEU HD12', -0.744, (4.053, 20.916, -1.602)), (' A   6  MET  CE ', ' A 299  GLN HE21', -0.738, (13.796, 2.339, 0.119)), (' A 209  TYR  O  ', ' A 213  ILE HG13', -0.707, (5.208, 12.404, -4.105)), (' A 165  MET  SD ', ' A 624  HOH  O  ', -0.706, (39.658, 1.678, -19.063)), (' A 191  ALA  HA ', ' A 401  XM2  C6 ', -0.696, (43.641, 10.228, -19.415)), (' A 166  GLU  O  ', ' A 401  XM2  N10', -0.679, (40.334, 5.596, -15.522)), (' A 221  ASN  OD1', ' A 222  ARG  N  ', -0.633, (2.756, 27.015, -7.876)), (' A 228  ASN  O  ', ' A 232  LEU HD23', -0.62, (10.356, 26.826, -24.078)), (' A 264  MET  HE3', ' A 267  SER  HB2', -0.598, (7.283, 21.335, -8.45)), (' A 167  LEU  O  ', ' A 169  THR  N  ', -0.547, (38.854, 11.047, -13.256)), (' A 188  ARG  HD2', ' A 190  THR  CG2', -0.538, (44.375, 5.622, -24.905)), (' A 217  ARG  HG2', ' A 217  ARG  O  ', -0.537, (4.738, 22.033, -0.433)), (' A 190  THR  O  ', ' A 192  GLN  HG3', -0.537, (41.942, 8.177, -21.957)), (' A  27  LEU HD13', ' A  39  PRO  HD2', -0.523, (37.728, -8.527, -14.397)), (' A  45  THR  O  ', ' A  49  MET  HG3', -0.52, (48.599, -2.723, -18.267)), (' A 137  LYS  HG2', ' A 171  VAL HG12', -0.518, (30.949, 10.49, -11.405)), (' A 191  ALA  CA ', ' A 401  XM2  C5 ', -0.518, (42.971, 9.793, -20.487)), (' A 188  ARG  HD2', ' A 190  THR HG21', -0.51, (43.925, 6.132, -25.372)), (' A 219  PHE  HE1', ' A 264  MET  HE1', -0.503, (7.013, 19.811, -5.45)), (' A 219  PHE  CE1', ' A 264  MET  HE1', -0.495, (7.674, 20.053, -5.567)), (' A 305  PHE  O  ', ' A 306  GLN  HB3', -0.489, (12.78, -12.314, -2.326)), (' A 191  ALA  CA ', ' A 401  XM2  C6 ', -0.485, (43.81, 10.085, -20.372)), (' A 218  TRP  HB2', ' A 279  ARG  NH1', -0.483, (8.998, 26.252, 1.595)), (' A 233  VAL HG21', ' A 269  LYS  HE2', -0.48, (11.358, 28.813, -16.78)), (' A 165  MET  HB3', ' A 624  HOH  O  ', -0.477, (39.403, 1.479, -17.809)), (' A  49  MET  HG2', ' A 401  XM2  C28', -0.474, (45.89, -1.933, -18.473)), (' A   3  PHE  CD1', ' A 299  GLN  OE1', -0.471, (11.952, 6.654, -1.217)), (' A  49  MET  HB3', ' A 401  XM2  C28', -0.464, (45.701, -0.425, -18.913)), (' A 190  THR  C  ', ' A 401  XM2  C5 ', -0.455, (43.541, 8.823, -20.622)), (' A 225  THR  OG1', ' A 229  ASP  OD2', -0.45, (6.942, 27.565, -18.24)), (' A  86  VAL HG13', ' A 179  GLY  HA2', -0.448, (32.618, -6.69, -21.527)), (' A 218  TRP  CE3', ' A 279  ARG  CZ ', -0.439, (10.754, 26.69, 0.077)), (' A 401  XM2  C3 ', ' A 401  XM2  C9 ', -0.433, (42.996, 6.065, -17.359)), (' A 190  THR  O  ', ' A 401  XM2  C5 ', -0.428, (42.837, 8.577, -20.156)), (' A  21  THR  HB ', ' A  67  LEU  HB2', -0.427, (44.508, -16.143, -10.758)), (' A 217  ARG  CG ', ' A 217  ARG  O  ', -0.423, (4.877, 21.818, -0.443)), (' A 230  PHE  CD1', ' A 265  CYS  HB3', -0.414, (9.294, 22.538, -15.738)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.412, (24.772, -2.73, -9.512)), (' A 118  TYR  CE2', ' A 144  SER  HB3', -0.412, (37.273, -1.878, -5.593)), (' A 257  THR  O  ', ' A 259  ILE HD12', -0.412, (-1.014, 15.855, -5.588)), (' A 153  ASP  O  ', ' A 155  ASP  N  ', -0.405, (12.151, -11.193, -9.871)), (' A 233  VAL HG21', ' A 269  LYS  HG3', -0.401, (11.602, 28.075, -15.502))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
