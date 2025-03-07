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
data['omega'] = [('A', ' 163 ', 'PRO', None, (41.598, 18.734, 47.008))]
data['rota'] = [('A', ' 108 ', 'GLN', 0.0, (40.066, 70.754, 57.63300000000002)), ('A', ' 133 ', 'GLU', 0.18205858641104944, (21.823000000000008, 38.28399999999999, 63.564)), ('A', ' 162 ', 'GLU', 0.1847913840271873, (40.19600000000001, 20.738, 46.854)), ('A', ' 240 ', 'LEU', 0.11777670851939319, (41.152, 43.28, 25.479)), ('A', ' 308 ', 'GLN', 0.017951637788770916, (62.849000000000004, 17.552, 43.678)), ('A', ' 314 ', 'ARG', 0.0, (59.277, 25.651999999999994, 50.296)), ('A', ' 375 ', 'LEU', 0.058024229839010844, (53.22100000000001, 25.803, 39.324)), ('A', ' 394 ', 'TYR', 0.24133711578823375, (51.026, 50.035, 55.951)), ('A', ' 463 ', 'LEU', 0.05609521565428624, (31.315000000000023, 38.991, 34.364)), ('A', ' 539 ', 'GLN', 0.08867990962226464, (61.619, 49.955, 33.063)), ('A', ' 585 ', 'PRO', 0.05982517643103198, (47.416, 58.225, 37.098))]
data['cbeta'] = []
data['probe'] = [(' A 613  LYS  HE2', ' A 617  PRO  HG2', -0.818, (28.979, 33.646, 12.998)), (' A 148  VAL HG12', ' A 349  GLU  HG2', -0.786, (33.2, 21.016, 55.882)), (' A 231  GLN  HG3', ' A2178  HOH  O  ', -0.725, (29.956, 55.216, 33.627)), (' A 304  ALA  O  ', ' A 308  GLN  HG2', -0.706, (61.866, 19.135, 40.915)), (' A  56  GLN  HG2', ' A 399  VAL HG21', -0.68, (44.747, 49.014, 64.889)), (' A 560  GLN  O  ', ' A 564  THR HG23', -0.655, (58.562, 53.304, 46.897)), (' A 317  LYS  HD2', ' A 336  TRP  CH2', -0.653, (59.003, 30.891, 53.617)), (' A 116  ILE  O  ', ' A 120  GLN  HG3', -0.65, (32.801, 59.051, 58.67)), (' A  82  LEU  HA ', ' A  85  ASN HD22', -0.65, (29.104, 35.419, 64.097)), (' A 399  VAL  HA ', ' A 402  ARG  HG3', -0.639, (44.694, 50.545, 59.581)), (' A  45  SER  O  ', ' A  49  GLU  HG3', -0.627, (43.019, 61.666, 67.209)), (' A  96  GLY  HA3', ' A 122  LEU  CD2', -0.617, (28.932, 53.746, 62.172)), (' A  54  THR  O  ', ' A  58  VAL HG12', -0.607, (38.493, 48.284, 68.859)), (' A 134  GLU  O  ', ' A 138  ILE HG12', -0.606, (21.118, 35.739, 58.036)), (' A 148  VAL HG12', ' A 349  GLU  CG ', -0.601, (33.811, 21.124, 55.945)), (' A  79  LYS  O  ', ' A  83  GLN  HG3', -0.586, (28.405, 32.914, 69.053)), (' A 179  LEU HD11', ' A 499  VAL HG23', -0.58, (26.756, 18.033, 30.886)), (' A 317  LYS  HD2', ' A 336  TRP  CZ2', -0.577, (59.251, 31.575, 54.402)), (' A 613  LYS  CE ', ' A 617  PRO  HG2', -0.565, (29.25, 33.757, 12.548)), (' A  59  TRP  CZ3', ' A 399  VAL HG12', -0.564, (40.765, 48.657, 60.837)), (' A 424  PRO  HA ', ' A 433  LEU HD12', -0.561, (61.066, 28.481, 32.073)), (' A 107  LEU HD21', ' A 116  ILE HD12', -0.553, (36.744, 64.382, 61.365)), (' A 531  PHE  CE1', ' A 592  MET  HE3', -0.539, (47.755, 40.418, 32.119)), (' A 117  LYS  HD3', ' A 117  LYS  O  ', -0.537, (32.4, 57.99, 54.792)), (' A 597  LYS  HB3', ' A 598  PRO  HD3', -0.537, (54.094, 41.953, 21.612)), (' A 523  TYR  CD2', ' A 702  MCO HC51', -0.537, (41.883, 37.413, 42.457)), (' A  79  LYS  HG2', ' A  83  GLN HE21', -0.532, (29.095, 31.297, 70.394)), (' A 154  PRO  HD2', ' A2102  HOH  O  ', -0.524, (30.142, 5.087, 40.992)), (' A 514  ILE  HB ', ' A 515  PRO  CD ', -0.521, (28.927, 31.998, 45.344)), (' A 333  PRO  HD2', ' A2241  HOH  O  ', -0.519, (58.091, 36.915, 63.999)), (' A  79  LYS  HG2', ' A  83  GLN  NE2', -0.515, (28.86, 30.731, 70.591)), (' A 543  HIS  CD2', ' A 550  CYS  HB2', -0.511, (61.609, 42.955, 30.776)), (' A 463  LEU  C  ', ' A 463  LEU HD23', -0.505, (30.132, 37.331, 35.438)), (' A 511  LYS  O  ', ' A 515  PRO  HD2', -0.505, (30.411, 31.401, 45.291)), (' A 562  LEU  HB3', ' A 566  MET  HE2', -0.503, (55.269, 46.718, 46.723)), (' A 173  ARG  NH1', ' A 288  ASP  OD1', -0.499, (45.929, 19.502, 29.395)), (' A 488  LEU HD22', ' A 492  TYR  HE1', -0.498, (27.886, 40.481, 31.261)), (' A 301  THR HG21', ' A 375  LEU  HG ', -0.498, (55.595, 26.103, 37.04)), (' A 462  TYR  O  ', ' A 466  GLN  HG2', -0.494, (31.582, 42.077, 34.668)), (' A 485  TRP  CD2', ' A 508  PRO  HG3', -0.49, (25.847, 32.48, 37.904)), (' A 295  SER  HB2', ' A2227  HOH  O  ', -0.484, (57.278, 22.081, 16.713)), (' A 155  ASN  OD1', ' A 156  GLY  N  ', -0.481, (31.263, 4.904, 45.914)), (' A 560  GLN HE21', ' A 564  THR  CG2', -0.474, (59.703, 54.061, 47.781)), (' A 275  LEU  N  ', ' A 275  LEU HD22', -0.474, (37.437, 24.235, 29.132)), (' A  84  LYS  HD3', ' A  87  GLN  OE1', -0.467, (33.388, 38.881, 71.071)), (' A 572  ARG  HD3', ' A2381  HOH  O  ', -0.467, (47.051, 62.879, 51.716)), (' A 159  LEU  N  ', ' A 159  LEU HD12', -0.464, (34.472, 12.428, 45.735)), (' A 476  ILE HG12', ' A 484  GLU  HG3', -0.463, (19.355, 38.732, 35.125)), (' A 107  LEU  CD2', ' A 116  ILE HD12', -0.457, (36.589, 64.628, 60.758)), (' A 117  LYS  C  ', ' A 117  LYS  HD3', -0.456, (33.354, 58.342, 55.195)), (' A 292  PRO  HD2', ' A 445  ASN  OD1', -0.454, (53.097, 26.589, 22.051)), (' A 463  LEU HD11', ' A 489  ARG  HA ', -0.453, (29.687, 34.551, 32.003)), (' A  52  ASP  O  ', ' A  56  GLN  HG3', -0.453, (42.944, 50.735, 66.797)), (' A 103  ASP  OD1', ' A 105  ASN  HB2', -0.452, (30.154, 69.547, 55.998)), (' A 325  SER  O  ', ' A 554  GLN  HA ', -0.45, (66.445, 41.784, 44.63)), (' A 597  LYS  HE3', ' A 601  ASP  OD2', -0.45, (52.518, 42.25, 16.576)), (' A 169  MET  O  ', ' A 276  GLY  HA2', -0.445, (40.484, 21.118, 33.308)), (' A  96  GLY  HA3', ' A 122  LEU HD21', -0.443, (28.31, 54.166, 62.567)), (' A 363  LYS  HG3', ' A2267  HOH  O  ', -0.442, (55.386, 40.117, 65.079)), (' A 554  GLN  HG2', ' A 554  GLN  O  ', -0.438, (68.646, 42.631, 42.951)), (' A 209  ARG  HA ', ' A 213  TYR  O  ', -0.437, (21.145, 52.362, 50.544)), (' A 574  TRP  CG ', ' A 575  PRO  HD3', -0.436, (42.636, 55.62, 42.643)), (' A 152  CYS  HA ', ' A 158  CYS  HA ', -0.433, (31.671, 11.176, 46.081)), (' A 523  TYR  CE2', ' A 702  MCO HC51', -0.431, (41.335, 37.45, 43.361)), (' A 195  GLN  HB2', ' A 195  GLN HE21', -0.431, (16.736, 27.545, 51.88)), (' A 376  GLU  HG3', ' A2276  HOH  O  ', -0.429, (47.153, 29.13, 39.451)), (' A 557  GLU  HG2', ' A2362  HOH  O  ', -0.427, (65.904, 52.465, 38.85)), (' A 609  LEU  C  ', ' A 609  LEU HD12', -0.426, (45.118, 28.255, 8.49)), (' A  56  GLN  HG2', ' A 399  VAL  CG2', -0.423, (44.631, 49.471, 64.521)), (' A 579  GLN HE21', ' A 583  GLY  C  ', -0.423, (52.935, 59.333, 36.515)), (' A 380  VAL  O  ', ' A 383  HIS  HB3', -0.42, (48.981, 33.763, 45.596)), (' A 522  ARG  HB3', ' A 704   CL CL  ', -0.419, (37.457, 43.702, 44.375)), (' A 457  PHE  CE2', ' A 461  SER  HB3', -0.416, (39.209, 37.879, 36.812)), (' A 507  ASP  N  ', ' A 508  PRO  CD ', -0.411, (24.513, 29.465, 39.53)), (' A 308  GLN  H  ', ' A 308  GLN  HG2', -0.409, (61.66, 18.367, 41.625)), (' A 353  HIS  HD2', ' A2255  HOH  O  ', -0.406, (39.683, 33.047, 49.38)), (' A 404  GLY  O  ', ' A 405  ALA  C  ', -0.406, (43.441, 51.171, 48.061)), (' A 579  GLN  HA ', ' A 584  GLN  O  ', -0.405, (50.697, 57.499, 38.169)), (' A 130  GLN  HG2', ' A2086  HOH  O  ', -0.402, (15.115, 39.213, 62.15))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
