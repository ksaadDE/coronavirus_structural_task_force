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
data['omega'] = [('H', ' 166 ', 'PRO', None, (-3.6220000000000008, -26.769999999999985, -7.835)), ('H', ' 168 ', 'PRO', None, (-9.498, -28.293, -6.794)), ('L', '   8 ', 'PRO', None, (-29.218000000000007, -5.212000000000003, 2.727)), ('L', ' 143 ', 'PRO', None, (-24.403000000000002, -16.60899999999999, 16.459))]
data['rota'] = [('H', '  79 ', 'MET', 0.025515543862242508, (-20.362, -21.015, -28.574)), ('H', ' 115 ', 'ASN', 0.17532113473401328, (-32.463, -5.002, -25.096)), ('H', ' 159 ', 'CYS', 0.007601845230251353, (-6.691999999999995, -33.673, 9.256000000000007)), ('L', ' 107 ', 'GLU', 0.22955690971510137, (-28.978, -16.585, 6.251)), ('L', ' 108 ', 'ILE', 0.07625393870436015, (-31.061000000000003, -18.457, 8.885))]
data['cbeta'] = []
data['probe'] = [(' A 516  GLU  HG2', ' A 518  LEU  CD1', -1.216, (-36.664, -8.798, -57.164)), (' A 516  GLU  CG ', ' A 518  LEU HD11', -1.121, (-36.02, -8.646, -56.313)), (' A 516  GLU  HG2', ' A 518  LEU HD11', -1.033, (-36.157, -8.422, -56.303)), (' L 203  LEU HD13', ' L 207  VAL HG23', -0.787, (-15.496, -19.051, 25.982)), (' A 424  LYS  HD3', ' A 706  HOH  O  ', -0.778, (-15.584, -12.063, -54.512)), (' H 173  TRP  HB3', ' H 178  LEU HD23', -0.696, (-15.326, -39.819, 8.706)), (' L   2  ILE HG12', ' L  27  GLN  HG2', -0.694, (-27.317, 4.556, -14.272)), (' A 364  ASP  OD2', ' A 367  VAL HG23', -0.674, (-36.542, 14.008, -49.808)), (' A 345  THR HG22', ' H 308  HOH  O  ', -0.672, (-28.265, -0.843, -31.711)), (' A 393  THR  HB ', ' A 518  LEU HD13', -0.668, (-38.745, -7.594, -56.687)), (' H  47  TRP  CG ', ' L  98 BVAL  CG2', -0.653, (-23.19, -8.227, -19.53)), (' L  94  THR  O  ', ' L  94  THR HG22', -0.643, (-28.316, 3.992, -21.083)), (' L 109  LYS  HB3', ' L 109  LYS  NZ ', -0.637, (-33.511, -14.897, 12.311)), (' H 145  PRO  HG2', ' H 232  PRO  HA ', -0.631, (-7.008, -39.455, 18.959)), (' L   8  PRO  O  ', ' L 104  THR HG23', -0.618, (-27.93, -7.519, 1.557)), (' L 147  LYS  HB3', ' L 199  THR  HB ', -0.588, (-14.07, -12.196, 19.808)), (' A 335  LEU  HG ', ' A 362  VAL  O  ', -0.585, (-41.1, 6.934, -48.162)), (' A 360  ASN  HA ', ' A 523  THR  OG1', -0.583, (-44.233, -1.843, -50.568)), (' H  83  MET  HE2', ' H  86  LEU HD21', -0.562, (-9.176, -16.354, -19.951)), (' A 345  THR  CG2', ' H 308  HOH  O  ', -0.561, (-28.18, -0.935, -31.337)), (' A 516  GLU  CD ', ' A 518  LEU HD11', -0.556, (-36.351, -9.686, -55.414)), (' A 368  LEU  HA ', ' A 371  SER  OG ', -0.55, (-30.904, 11.131, -46.202)), (' L 109  LYS  HB3', ' L 109  LYS  HZ1', -0.545, (-33.735, -15.071, 12.011)), (' H  79 BMET  HG2', ' H  80  PHE  N  ', -0.529, (-18.852, -19.327, -27.958)), (' H  47  TRP  CB ', ' L  98 BVAL HG23', -0.528, (-22.115, -7.928, -18.396)), (' A 449  TYR  HD1', ' H  65  GLN  HG3', -0.527, (-10.266, -4.227, -27.767)), (' L 203  LEU HD13', ' L 207  VAL  CG2', -0.522, (-15.692, -19.434, 25.732)), (' A 503  VAL  HA ', ' A 506  GLN  NE2', -0.52, (-8.965, 7.961, -39.805)), (' A 380  TYR  O  ', ' A 430  THR  HA ', -0.517, (-26.37, -0.31, -60.224)), (' L 127  LEU  O  ', ' L 185  LYS  HD2', -0.511, (10.439, -29.49, 11.911)), (' H 171  VAL  HA ', ' H 216  ASN  O  ', -0.506, (-11.115, -36.417, 1.464)), (' L 160  ASN  O  ', ' L 181  LEU HD12', -0.497, (0.031, -17.65, 13.514)), (' A 440  ASN  ND2', ' A 441  LEU  HG ', -0.497, (-19.6, 8.234, -33.585)), (' H  79 BMET  HG2', ' H  80 BPHE  H  ', -0.493, (-19.225, -18.925, -27.939)), (' H  34  MET  HB3', ' H  79 BMET  SD ', -0.49, (-23.243, -17.658, -26.418)), (' H  70  ILE HD11', ' H  79 AMET  HE1', -0.486, (-20.537, -16.239, -25.978)), (' L  95  SER  OG ', ' L  96  PRO  HD2', -0.485, (-24.023, 1.623, -19.268)), (' L  40  LYS  NZ ', ' L  82  GLU  O  ', -0.483, (-32.434, -22.327, -2.202)), (' A 517  LEU  C  ', ' A 518  LEU HD12', -0.481, (-37.531, -8.299, -58.83)), (' H  47  TRP  CG ', ' L  98 BVAL HG21', -0.474, (-22.897, -8.612, -19.601)), (' L 153  ASP  OD1', ' L 193  VAL HG23', -0.469, (4.074, -20.663, 27.521)), (' H  79 AMET  HB2', ' H  79 AMET  HE2', -0.468, (-20.344, -18.453, -27.798)), (' A 393  THR  CB ', ' A 518  LEU HD13', -0.466, (-39.307, -7.471, -56.558)), (' A 518  LEU  N  ', ' A 518  LEU HD12', -0.465, (-38.103, -8.4, -58.628)), (' H  71  TYR  CE1', ' H  80  PHE  HB2', -0.464, (-15.045, -19.843, -30.196)), (' H 232  PRO  O  ', ' H 233  LYS  HB3', -0.461, (-2.961, -38.432, 20.425)), (' L 152  VAL  O  ', ' L 153  ASP  HB2', -0.455, (4.675, -16.825, 24.406)), (' L 114  ALA  HB1', ' L 203  LEU HD21', -0.451, (-19.494, -20.08, 24.191)), (' L 142  TYR  CD1', ' L 143  PRO  HA ', -0.448, (-25.234, -17.326, 14.197)), (' L  49  ILE HD13', ' L  65  GLY  N  ', -0.446, (-39.816, -9.899, -8.274)), (' L 114  ALA  HB1', ' L 203  LEU  CD2', -0.444, (-19.919, -20.235, 24.053)), (' H 197  LEU  C  ', ' H 197  LEU HD12', -0.444, (-8.299, -28.381, 4.998)), (' A 520  ALA  HB1', ' A 521  PRO  HD2', -0.443, (-45.299, -9.826, -56.454)), (' L 188  TYR  HA ', ' L 194  TYR  OH ', -0.44, (6.332, -22.501, 18.826)), (' L 142  TYR  CG ', ' L 143  PRO  HA ', -0.435, (-25.327, -17.317, 14.551)), (' H 138  PRO  HB3', ' H 164  TYR  HB3', -0.43, (-2.641, -30.237, -1.209)), (' A 449  TYR  HB2', ' H  65  GLN  OE1', -0.429, (-11.919, -6.137, -28.494)), (' A 467  ASP  HB3', ' A 708  HOH  O  ', -0.428, (-17.394, -15.346, -44.851)), (' L 121  PRO  HB3', ' L 211  PHE  CE1', -0.427, (0.456, -27.719, 20.791)), (' H 220  LYS  N  ', ' H 221  PRO  HD2', -0.427, (-7.109, -33.459, -7.851)), (' H   2  VAL  C  ', ' H   3  GLN  HG2', -0.426, (-31.05, -28.327, -20.773)), (' L  51  GLY  O  ', ' L  52  ALA  HB3', -0.423, (-39.627, -4.547, -13.528)), (' L  19  ALA  HB2', ' L  79  LEU HD11', -0.423, (-36.309, -13.786, 4.26)), (' A 449  TYR  CD1', ' H  65  GLN  HG3', -0.422, (-10.16, -4.461, -27.65)), (' A 417  LYS  HA ', ' A 417  LYS  HD3', -0.421, (-9.281, -10.553, -47.807)), (' A 490  PHE  CE2', ' A 492  LEU  HB2', -0.418, (-12.099, -15.682, -35.399)), (' A 438  SER  HB3', ' A 509  ARG  HG3', -0.417, (-19.613, 3.954, -38.243)), (' A 417  LYS  O  ', ' A 421  TYR  HB2', -0.417, (-12.069, -10.891, -47.387)), (' L 121  PRO  HB3', ' L 211  PHE  CZ ', -0.417, (0.196, -27.491, 20.318)), (' A 347  PHE  CE2', ' A 509  ARG  HB3', -0.406, (-22.855, 1.651, -40.316)), (' L  21  LEU  N  ', ' L  21  LEU HD12', -0.405, (-35.027, -8.922, 0.385)), (' A 357  ARG  HG3', ' A 357  ARG HH11', -0.405, (-37.311, -8.333, -48.553)), (' A 357  ARG  HG3', ' A 357  ARG  NH1', -0.404, (-37.159, -8.616, -48.359)), (' L 109  LYS  HA ', ' L 142  TYR  OH ', -0.403, (-29.424, -16.103, 12.578)), (' L  49  ILE  HA ', ' L  54  SER  O  ', -0.403, (-39.198, -11.9, -12.965)), (' H 181  GLY  O  ', ' H 201  VAL  HA ', -0.401, (-16.778, -33.705, 12.381)), (' A 439  ASN  ND2', ' A 506  GLN  OE1', -0.4, (-10.932, 8.273, -36.156))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
