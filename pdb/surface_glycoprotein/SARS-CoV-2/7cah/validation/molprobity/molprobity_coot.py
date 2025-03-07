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
data['rama'] = [('D', '  91 ', 'ASN', 0.02064436918055996, (101.062, 101.11, 97.63699999999997))]
data['omega'] = [('A', ' 362 ', 'VAL', None, (85.917, 113.246, 118.736)), ('A', ' 433 ', 'VAL', None, (96.28699999999998, 114.317, 102.67799999999997)), ('E', ' 103 ', 'PRO', None, (102.404, 107.915, 92.319))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' A 379  CYS  HA ', ' A 432  CYS  HB2', -0.869, (99.248, 114.912, 104.055)), (' A 379  CYS  HA ', ' A 432  CYS  CB ', -0.751, (98.6, 115.736, 104.624)), (' E 102  ASP  O  ', ' E 104  TYR  N  ', -0.722, (104.486, 106.755, 90.867)), (' A 365  TYR  HA ', ' A 368  LEU HD13', -0.722, (93.059, 108.949, 112.015)), (' A 456  PHE  H  ', ' A 491  PRO  HB2', -0.72, (85.428, 119.917, 80.316)), (' E  60  ASP  OD2', ' E  65  LYS  NZ ', -0.705, (106.825, 110.433, 111.386)), (' A 470  THR  HB ', ' A 490  PHE  HB2', -0.699, (77.661, 120.311, 81.063)), (' E 119  SER  OG ', ' E 121  ALA  O  ', -0.649, (129.749, 108.143, 121.044)), (' A 437  ASN  OD1', ' A 438  SER  N  ', -0.642, (92.109, 100.808, 92.434)), (' D  34  TRP  O  ', ' D  46  LEU  N  ', -0.638, (115.655, 96.634, 90.867)), (' E   6  GLN  H  ', ' E 112  GLN HE22', -0.627, (126.458, 112.338, 99.051)), (' A 362  VAL  HB ', ' A 526  GLY  HA2', -0.623, (88.946, 111.895, 120.258)), (' A 418  ILE  HA ', ' A 422  ASN  HB2', -0.613, (90.288, 118.421, 88.196)), (' E  35  HIS  CD2', ' E  99  SER  HB2', -0.611, (111.125, 107.535, 96.401)), (' E   6  GLN  H  ', ' E 112  GLN  NE2', -0.593, (126.52, 112.087, 99.23)), (' E  36  TRP  O  ', ' E  48  ILE HG12', -0.593, (113.635, 107.269, 104.847)), (' E  47  TRP  CE3', ' E  61  ASN  HB2', -0.572, (107.262, 104.583, 106.118)), (' A 448  ASN  OD1', ' A 449  TYR  N  ', -0.571, (81.496, 103.081, 85.238)), (' A 353  TRP  CZ3', ' A 355  ARG  HB2', -0.564, (83.494, 119.343, 98.785)), (' D  26  GLN  NE2', ' D  27  SER  OG ', -0.56, (97.3, 93.317, 102.758)), (' A 354  ASN  O  ', ' A 398  ASP  HA ', -0.555, (84.844, 115.61, 100.446)), (' D  21  THR  HA ', ' D  71  THR HG22', -0.553, (110.298, 83.868, 94.21)), (' E  50  TYR  CE1', ' E  59  SER  HB3', -0.546, (104.775, 110.18, 101.67)), (' D  84  ILE  HA ', ' D 102  LYS  HA ', -0.544, (121.824, 89.384, 98.635)), (' D  79  ALA  HA ', ' D  82  PHE  CE2', -0.543, (128.924, 84.509, 91.918)), (' A 405  ASP  N  ', ' A 504  GLY  O  ', -0.54, (96.651, 107.834, 86.723)), (' E  16  ALA  O  ', ' E  86  LEU  HG ', -0.532, (119.331, 112.921, 118.906)), (' A 446  GLY  O  ', ' A 498  GLN  NE2', -0.531, (86.418, 99.013, 79.271)), (' D  65  GLY  HA3', ' D  70  PHE  HA ', -0.526, (105.342, 86.878, 91.017)), (' A 374  PHE  HA ', ' A 436  TRP  HB3', -0.522, (94.876, 103.345, 99.452)), (' E  67  ALA  HB3', ' E  84  SER  HB3', -0.515, (112.268, 113.523, 116.695)), (' E  35  HIS  HD2', ' E  99  SER  HB2', -0.513, (111.383, 107.537, 96.401)), (' D  90  THR  OG1', ' D  91  ASN  N  ', -0.51, (102.516, 100.34, 96.143)), (' D  85  TYR  O  ', ' D 101  THR  N  ', -0.509, (117.204, 89.736, 98.893)), (' D  31  ASN  OD1', ' D  32  LEU  N  ', -0.509, (104.991, 97.657, 91.92)), (' E  39  GLN  O  ', ' E  92  ALA  HB1', -0.507, (120.946, 101.567, 109.137)), (' A 337  PRO  O  ', ' A 340  GLU  HG3', -0.506, (81.953, 108.625, 108.178)), (' E  87  ARG  O  ', ' E 118  VAL HG11', -0.504, (121.625, 104.702, 118.324)), (' E  75  SER  OG ', ' E  76  THR  N  ', -0.501, (118.922, 126.564, 98.291)), (' E  91  THR  HA ', ' E 116  VAL  O  ', -0.501, (123.553, 105.661, 114.024)), (' A 424  LYS  NZ ', ' A 427  ASP  OD2', -0.496, (97.743, 127.347, 96.078)), (' D  12  VAL HG11', ' D  18  VAL HG11', -0.496, (121.423, 79.376, 92.235)), (' A 433  VAL HG22', ' A 512  VAL HG13', -0.485, (94.09, 115.914, 100.153)), (' E  24  VAL HG11', ' E  29  PHE  CD1', -0.481, (116.466, 118.342, 94.207)), (' A 350  VAL HG22', ' A 453  TYR  HA ', -0.481, (85.841, 115.066, 86.988)), (' E  35  HIS  ND1', ' E  50  TYR  HB3', -0.476, (109.827, 108.337, 99.951)), (' D  25  SER  OG ', ' D  26  GLN  N  ', -0.476, (99.658, 89.211, 103.607)), (' A 412  PRO  HB3', ' A 427  ASP  OD1', -0.476, (100.271, 125.101, 97.196)), (' A 340  GLU  OE1', ' A 356  LYS  HE3', -0.473, (81.228, 111.053, 105.034)), (' A 404  GLY  O  ', ' A 407  VAL HG22', -0.472, (97.641, 109.556, 90.479)), (' A 383  SER  O  ', ' A 386  LYS  N  ', -0.471, (101.625, 114.113, 113.498)), (' E  61  ASN  OD1', ' E  63  LYS  HG2', -0.471, (106.432, 102.356, 109.672)), (' A 386  LYS  HG3', ' A 390  LEU HD11', -0.469, (101.335, 118.755, 114.908)), (' D  61  PHE  HA ', ' D  74  ILE  HA ', -0.46, (118.18, 86.493, 87.061)), (' E  87  ARG  NH2', ' E  89  GLU  OE1', -0.455, (115.176, 103.637, 119.882)), (' E  41  PRO  HD2', ' E  43  LYS  NZ ', -0.454, (120.482, 97.333, 112.511)), (' E  51  ILE HG13', ' E  58  THR HG22', -0.454, (108.585, 116.355, 103.446)), (' E  47  TRP  HE3', ' E  61  ASN  HB2', -0.451, (107.493, 104.33, 105.692)), (' E  71  THR HG23', ' E  80  TYR  HB2', -0.451, (115.787, 119.979, 106.193)), (' A 377  PHE  HB3', ' D  93  TRP  CE2', -0.448, (100.782, 107.584, 104.873)), (' A 502  GLY  HA3', ' A 505  TYR  HD1', -0.448, (97.255, 103.572, 81.966)), (' D  67  GLY  O  ', ' D  70  PHE  HE1', -0.445, (101.156, 90.119, 93.206)), (' E  13  LYS  HZ1', ' E  14  PRO  HD2', -0.441, (124.78, 109.703, 125.178)), (' E   6  GLN  NE2', ' E 113  GLY  H  ', -0.441, (123.533, 108.169, 101.273)), (' E  27  TYR  CD2', ' E  32  TYR  HD2', -0.44, (114.356, 115.443, 88.994)), (' A 348  ALA  HB1', ' A 352  ALA  O  ', -0.44, (81.307, 113.851, 94.196)), (' D  93  TRP  HB3', ' D  94  PRO  HD3', -0.438, (100.705, 102.427, 105.338)), (' D  85  TYR  N  ', ' D 101  THR  O  ', -0.437, (119.818, 89.923, 97.581)), (' E  40  ALA  HB1', ' E  43  LYS  NZ ', -0.436, (119.516, 96.733, 111.398)), (' E  13  LYS  HB3', ' E  13  LYS  HE3', -0.435, (124.575, 111.791, 124.52)), (' E  13  LYS  NZ ', ' E  14  PRO  HD2', -0.432, (125.097, 109.6, 124.975)), (' A 339  GLY  O  ', ' A 343  ASN  N  ', -0.432, (84.19, 104.738, 105.114)), (' A 448  ASN  HB3', ' A 497  PHE  CD2', -0.431, (84.814, 103.055, 86.534)), (' E  51  ILE HD12', ' E  70  LEU  HB3', -0.43, (111.115, 116.477, 104.595)), (' A 405  ASP  O  ', ' A 408  ARG  HG2', -0.429, (99.286, 111.944, 88.095)), (' E  48  ILE  HB ', ' E  64  PHE  HZ ', -0.428, (113.126, 106.447, 109.792)), (' E  30  SER  O  ', ' E  53  PRO  HG2', -0.428, (109.545, 119.39, 93.687)), (' E  29  PHE  HE2', ' E  74  THR  HA ', -0.427, (115.05, 122.628, 96.568)), (' D  10  GLN  HB3', ' D 103  LEU  HA ', -0.427, (122.414, 83.632, 96.937)), (' D  91  ASN  OD1', ' D  92  PHE  N  ', -0.419, (100.343, 99.361, 98.701)), (' A 401  VAL HG22', ' A 509  ARG  HA ', -0.418, (88.035, 107.333, 94.142)), (' E  41  PRO  HG3', ' E  91  THR  O  ', -0.418, (123.41, 100.889, 112.826)), (' A 456  PHE  HB2', ' A 491  PRO  HB3', -0.417, (84.98, 121.845, 79.325)), (' A 448  ASN  HB3', ' A 497  PHE  HD2', -0.417, (85.132, 103.108, 86.902)), (' E  61  ASN  OD1', ' E  62  LEU  N  ', -0.417, (105.809, 104.314, 109.955)), (' A 385  THR HG21', ' E  65  LYS  HD2', -0.417, (106.178, 111.296, 115.371)), (' D  94  PRO  O  ', ' D  96  ILE  N  ', -0.417, (106.063, 99.279, 103.465)), (' A 335  LEU  HA ', ' A 362  VAL  O  ', -0.416, (86.001, 110.266, 117.976)), (' E  40  ALA  HB3', ' E  43  LYS  HB2', -0.414, (119.436, 95.551, 109.717)), (' A 449  TYR  O  ', ' A 494  SER  OG ', -0.413, (82.251, 107.598, 83.089)), (' A 354  ASN  HB3', ' A 399  SER  HB3', -0.412, (83.249, 112.148, 99.771)), (' A 425  LEU  HA ', ' A 425  LEU HD23', -0.41, (93.629, 121.73, 98.112)), (' A 341  VAL HG23', ' A 342  PHE  CD1', -0.41, (87.125, 108.591, 105.752)), (' E  47  TRP  HZ2', ' E  50  TYR  HD1', -0.41, (107.78, 108.332, 101.511)), (' A 353  TRP  HZ3', ' A 355  ARG  HB2', -0.409, (83.953, 119.825, 99.417)), (' E  34  ILE  HA ', ' E  34  ILE HD13', -0.407, (113.937, 111.596, 96.346)), (' D  60  ARG  O  ', ' D  75  ASN  N  ', -0.406, (119.045, 85.024, 85.258)), (' A 461  LEU HD11', ' A 467  ASP  H  ', -0.403, (84.0, 123.106, 90.701)), (' A 338  PHE  CE2', ' A 363  ALA  HB1', -0.402, (89.199, 111.057, 113.416)), (' D  90  THR  O  ', ' D  92  PHE  N  ', -0.401, (101.707, 99.706, 99.551)), (' E  20  ILE HG12', ' E  21  SER  H  ', -0.401, (122.435, 114.42, 105.699))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
