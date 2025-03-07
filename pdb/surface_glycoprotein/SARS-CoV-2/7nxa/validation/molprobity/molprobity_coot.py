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
data['rama'] = [('H', ' 155 ', 'PRO', 0.1546248746791076, (26.715000000000007, 3.69, -16.347))]
data['omega'] = [('A', ' 108 ', 'PRO', None, (3.1260000000000003, -39.813, -56.63199999999999)), ('A', ' 153 ', 'PRO', None, (-17.29, -19.32, -53.98800000000001)), ('A', ' 155 ', 'PRO', None, (-13.508000000000006, -22.752000000000013, -57.62100000000001)), ('B', '   8 ', 'PRO', None, (16.155, -17.675000000000015, -65.269)), ('B', ' 141 ', 'PRO', None, (1.1320000000000003, -11.167, -80.472)), ('H', ' 155 ', 'PRO', None, (28.087, 4.195, -16.301)), ('H', ' 157 ', 'PRO', None, (26.087, 0.894, -11.725)), ('L', '   8 ', 'PRO', None, (1.495, -18.284000000000013, -13.379999999999999)), ('L', ' 142 ', 'PRO', None, (-2.35, 0.43700000000000017, -4.079))]
data['rota'] = [('H', '  11 ', 'VAL', 0.23526242587418394, (32.678, -0.6080000000000004, -18.319)), ('H', ' 190 ', 'VAL', 0.2585731861942887, (14.838, 9.629000000000001, 4.073)), ('L', '  31 ', 'SER', 0.05665553358531624, (12.386000000000001, -34.98200000000001, -11.895)), ('L', '  33 ', 'LEU', 0.17637502409221026, (13.381, -29.334000000000014, -11.878)), ('L', ' 182 ', 'LEU', 0.21132183995821943, (14.254000000000001, 21.500000000000007, -17.07)), ('E', ' 503 ', 'VAL', 0.08506486099431022, (28.199999999999996, -28.925, -43.193)), ('A', '  19 ', 'ARG', 0.29532437680725115, (-10.475, -30.883000000000003, -43.085)), ('A', ' 156 ', 'VAL', 0.20838746657771498, (-15.98200000000001, -23.718000000000007, -61.76)), ('B', '  49 ', 'ILE', 0.2255746759435173, (14.065000000000005, -35.016999999999975, -62.955000000000005)), ('B', ' 106 ', 'ILE', 0.12893232895805481, (7.011000000000006, -19.859, -76.279))]
data['cbeta'] = []
data['probe'] = [(' E 420  ASP  OD1', ' E 801  HOH  O  ', -0.851, (11.008, -42.143, -34.332)), (' H  83  MET  HB3', ' H  86  LEU HD21', -0.7, (32.952, -10.798, -22.519)), (' E 389  ASP  OD2', ' E 802  HOH  O  ', -0.652, (34.138, -38.203, -7.784)), (' E 412  PRO  HG3', ' E 429  PHE  HB3', -0.634, (18.022, -39.549, -23.742)), (' B  10  THR HG22', ' B 103  LYS  HB3', -0.627, (7.622, -16.868, -67.049)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.623, (12.17, -18.354, -4.1)), (' B   4  MET  HG3', ' B  91  HIS  CD2', -0.614, (17.011, -25.686, -53.036)), (' E 376  THR  HB ', ' E 435  ALA  HB3', -0.61, (27.67, -33.505, -32.116)), (' E 340  GLU  OE1', ' E 356  LYS  NZ ', -0.591, (37.281, -52.721, -27.907)), (' L 146  LYS  HB3', ' L 198  THR  HB ', -0.584, (-3.928, 9.876, -11.084)), (' L 152  ASP  OD1', ' L 192  VAL  N  ', -0.566, (4.47, 28.984, -11.752)), (' B  62  ARG  HB2', ' B  77  SER  O  ', -0.547, (13.984, -31.748, -76.203)), (' A  22  CYS  HB3', ' A  78  LEU  HB3', -0.529, (-4.322, -37.738, -48.259)), (' A   6  GLU  H  ', ' A 111  GLN HE22', -0.522, (-8.952, -35.105, -55.887)), (' B  81  PRO  HA ', ' B 106  ILE HD13', -0.522, (4.998, -23.832, -76.45)), (' B 106  ILE  O  ', ' B 166  GLN  NE2', -0.512, (4.275, -17.902, -76.941)), (' A  82  MET  HB3', ' A  85  LEU HD21', -0.51, (-6.214, -24.465, -42.741)), (' B  93  ASP  OD1', ' B  94  THR  N  ', -0.505, (16.83, -28.996, -44.758)), (' A  34  MET  HB3', ' A  78  LEU HD22', -0.505, (-0.638, -38.196, -47.858)), (' H  12  VAL HG21', ' H  86  LEU HD12', -0.503, (34.559, -6.181, -22.734)), (' L 125  GLN  O  ', ' L 128  SER  OG ', -0.493, (22.911, 23.243, -11.344)), (' A 125  PRO  HB3', ' A 151  TYR  HB3', -0.491, (-21.53, -19.23, -60.332)), (' A 149  LYS  NZ ', ' A 177  GLN  OE1', -0.485, (-21.214, -9.968, -63.78)), (' H  39  GLN  HB2', ' H  45  LEU HD23', -0.484, (20.272, -13.391, -14.31)), (' H 208  HIS  CD2', ' H 210  PRO  HD2', -0.483, (30.113, 3.531, -11.325)), (' B  11  LEU  O  ', ' B 105  ASP  N  ', -0.479, (8.8, -18.825, -72.006)), (' A 156  VAL HG22', ' A 184  LEU HD21', -0.475, (-15.33, -21.079, -64.254)), (' B 145  LYS  HB3', ' B 197  THR  OG1', -0.472, (-6.466, -1.7, -79.922)), (' E 379  CYS  SG ', ' E 384  PRO  HG3', -0.469, (28.163, -34.683, -20.503)), (' B   4  MET  HE2', ' B  29  VAL HG21', -0.467, (21.054, -26.945, -52.518)), (' H   6  GLU  OE1', ' H 114  GLY  N  ', -0.463, (28.045, -11.258, -7.549)), (' A 125  PRO  HD2', ' A 211  THR HG21', -0.462, (-24.295, -23.023, -59.643)), (' L 121  PRO  HD3', ' L 133  VAL HG22', -0.46, (11.979, 22.552, -9.205)), (' L 109  ARG  NH1', ' L 112  ALA  HB2', -0.453, (-1.44, 0.671, 2.504)), (' H  48  VAL HG13', ' H  64  VAL HG21', -0.451, (28.911, -17.946, -21.591)), (' B 163 AVAL HG22', ' B 175  LEU HD12', -0.451, (-6.495, -10.527, -72.867)), (' L 109  ARG HH12', ' L 112  ALA  HB2', -0.445, (-1.489, 0.373, 2.91)), (' E 501  TYR  OH ', ' E 704  PEG  H22', -0.445, (27.679, -35.706, -54.055)), (' L 152  ASP  HA ', ' L 192  VAL  HB ', -0.443, (2.017, 28.151, -12.202)), (' E 401  VAL HG22', ' E 509  ARG  HG2', -0.443, (31.505, -41.056, -38.214)), (' B 163 BVAL HG22', ' B 175  LEU HD12', -0.442, (-6.834, -10.25, -73.066)), (' A  29  VAL HG13', ' A  34  MET  HG3', -0.436, (-0.568, -41.361, -46.899)), (' E 342  PHE  CE1', ' E 368  LEU HD11', -0.434, (35.36, -41.192, -25.711)), (' L 150  LYS  HB2', ' L 194  ALA  HB3', -0.428, (0.726, 21.831, -11.174)), (' H  67  ARG  NH1', ' H  90  ASP  OD2', -0.428, (30.186, -11.109, -26.064)), (' L 147  VAL HG21', ' L 176  LEU HD22', -0.427, (4.695, 9.972, -9.204)), (' H 179  GLN  HB3', ' L 161  GLN HE22', -0.426, (16.627, 11.728, -16.677)), (' H 153  TYR  HB2', ' H 208  HIS  CE1', -0.421, (28.12, 7.696, -12.827)), (' B 185  ASP  HA ', ' B 188  LYS  HD3', -0.419, (-30.751, 2.039, -70.084)), (' H  52  SER  HB3', ' H  57  ASN  HB2', -0.418, (35.315, -30.679, -15.901)), (' H  97  ALA  HB1', ' H 108  PHE  HB3', -0.416, (24.395, -21.723, -8.893)), (' H 100  GLY  HA3', ' H 107  TYR  CZ ', -0.414, (23.495, -29.001, -5.36)), (' H  83  MET  HE1', ' H 117  VAL HG21', -0.413, (31.709, -8.847, -17.023)), (' A  11  LEU  HB2', ' A 153  PRO  HG3', -0.409, (-15.827, -20.389, -51.106)), (' H 154  PHE  HA ', ' H 155  PRO  HA ', -0.409, (25.743, 5.087, -16.617)), (' B  34  LEU HD13', ' B  72  PHE  CG ', -0.408, (20.485, -28.46, -58.005)), (' L  24  ARG  HA ', ' L  69  THR  O  ', -0.407, (5.861, -28.662, -17.411)), (' H 134  PRO  HD2', ' H 221  PRO  HA ', -0.405, (16.145, 21.5, 4.464)), (' E 455  LEU HD22', ' E 493  GLN  HG3', -0.403, (16.465, -42.941, -49.396))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
