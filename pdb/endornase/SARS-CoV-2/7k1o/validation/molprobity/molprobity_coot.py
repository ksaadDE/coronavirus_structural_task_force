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
data['rama'] = []
data['omega'] = []
data['rota'] = [('A', ' 132 ', 'VAL', 0.015862756611543575, (0.7050000000000001, 30.502, -39.501000000000005)), ('A', ' 150 ', 'LYS', 0.11768330370779578, (-6.822999999999999, 26.379999999999992, -33.848)), ('B', '  35 ', 'LYS', 0.02704671554326395, (56.979000000000006, 21.004, -55.135)), ('B', ' 136 ', 'ARG', 0.0, (14.687000000000003, 7.929, -70.45300000000002)), ('B', ' 186 ', 'VAL', 0.003150532575091347, (7.408, 13.768999999999997, -71.54800000000002)), ('B', ' 192 ', 'GLU', 0.15435703505711673, (14.101, 23.812999999999995, -86.01800000000003)), ('B', ' 225 ', 'ARG', 0.005381426992053379, (25.186, 40.723, -106.697)), ('B', ' 301 ', 'ASP', 0.08501208659812562, (23.348000000000006, 33.257, -95.86800000000002)), ('B', ' 308 ', 'LYS', 0.0939903756764003, (14.433, 38.731, -96.494)), ('C', '   1 ', 'MET', 0.22508554343437537, (63.358, 56.262999999999984, -43.442)), ('C', '  28 ', 'ILE', 0.005209334781247289, (51.924, 38.576, -45.387000000000015)), ('C', ' 174 ', 'LYS', 0.029654986668834767, (50.13300000000002, 65.374, -15.721000000000002)), ('C', ' 212 ', 'ILE', 0.21111530027279837, (28.686, 56.688, -4.0680000000000005)), ('C', ' 216 ', 'GLU', 0.17655301350967362, (24.855, 51.50899999999999, -2.357)), ('C', ' 227 ', 'LYS', 0.0, (15.041, 65.702, -4.401)), ('C', ' 266 ', 'LEU', 0.2527764454516979, (26.398999999999997, 45.90799999999998, -25.42))]
data['cbeta'] = []
data['probe'] = [(' A 267  GLU  HB3', ' A 280  PHE  HB3', -0.573, (40.645, 20.551, -27.246)), (' B 128  VAL  HB ', ' B 131  GLN  HG3', -0.538, (27.194, 8.462, -69.681)), (' C 149  VAL HG23', ' C 152  LEU  HB2', -0.534, (48.22, 81.789, -24.216)), (' C 267  GLU  HB3', ' C 280  PHE  HB3', -0.528, (24.403, 46.007, -30.564)), (' B 311  ASP  OD2', ' B 313  SER  OG ', -0.525, (4.016, 45.024, -93.35)), (' C 126  GLY  HA3', ' C 145  THR HG22', -0.516, (52.01, 73.959, -24.729)), (' C 223  ILE HG23', ' C 228  LEU  HB2', -0.504, (15.011, 61.733, -7.857)), (' A 219  MET  HG3', ' A 238  TYR  CE1', -0.501, (30.102, 13.288, -6.765)), (' B 220  ASP  N  ', ' B 220  ASP  OD1', -0.492, (30.147, 48.099, -103.063)), (' B 331  MET  HE3', ' B 333  TRP  NE1', -0.488, (13.463, 49.108, -82.826)), (' B 145  THR HG22', ' B 180  TYR  HE1', -0.487, (20.835, 11.535, -79.431)), (' B  90  LYS  HG3', ' B 273  ASP  HB2', -0.481, (31.06, 30.909, -73.349)), (' A  90  LYS  HG3', ' A 273  ASP  HB2', -0.475, (25.551, 27.694, -31.377)), (' C 136  ARG  O  ', ' C 182  LYS  NZ ', -0.473, (49.144, 82.1, -34.773)), (' C 219  MET  HE2', ' C 234  GLU  HA ', -0.472, (13.755, 54.723, -11.379)), (' C 246  LEU  O  ', ' C 290  LYS  HE2', -0.472, (14.71, 51.192, -24.068)), (' B 267  GLU  HB3', ' B 280  PHE  HB3', -0.466, (33.465, 48.062, -74.425)), (' B   9  ASN  HB3', ' B  16  PHE  HA ', -0.456, (43.495, 13.292, -62.455)), (' C 304  VAL  HA ', ' C 307  ILE HG22', -0.452, (19.914, 66.32, -13.473)), (' C 233  PHE  HZ ', ' C 304  VAL HG12', -0.45, (20.427, 63.241, -11.599)), (' C 131  GLN  HA ', ' C 134  LEU HD12', -0.438, (55.654, 73.65, -32.539)), (' B 150  LYS  HB3', ' B 150  LYS  HE2', -0.434, (14.209, 1.537, -80.72)), (' C 208  SER  O  ', ' C 212  ILE HD12', -0.434, (30.848, 59.384, -4.5)), (' C 265  GLU  O  ', ' C 281  ILE  HA ', -0.431, (23.319, 45.532, -24.803)), (' A 246  LEU  O  ', ' A 290  LYS  HE2', -0.43, (38.545, 10.87, -19.578)), (' C 235  HIS  O  ', ' C 248  GLY  HA3', -0.42, (15.621, 55.075, -18.72)), (' C 135  PHE  CZ ', ' C 182  LYS  HG3', -0.416, (45.654, 79.268, -31.125)), (' A  80  ILE HD12', ' A  98  SER  HB2', -0.416, (17.686, 28.841, -48.898)), (' B  66  PRO  O  ', ' B 127  ARG  NH2', -0.412, (31.618, 15.217, -75.823)), (' C 300  LEU  O  ', ' C 304  VAL HG13', -0.41, (23.228, 64.252, -11.113)), (' C 236  ILE HD13', ' C 342  PHE  HB3', -0.41, (16.176, 62.623, -18.823)), (' B 210  MET  HB3', ' B 301  ASP  OD2', -0.409, (26.249, 33.273, -98.065)), (' A 129  ASP  N  ', ' A 129  ASP  OD1', -0.408, (2.305, 38.936, -38.915)), (' A   4  GLU  HB3', ' A  22  GLU  HB3', -0.407, (24.145, 54.714, -49.865)), (' B 118  ALA  O  ', ' B 140  ASN  ND2', -0.407, (12.312, 17.526, -63.429)), (' C 128  VAL  HB ', ' C 131  GLN  HG3', -0.403, (55.908, 69.771, -29.457)), (' A   9  ASN  HB3', ' A  16  PHE  HA ', -0.401, (19.102, 48.865, -41.297))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
