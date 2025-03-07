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
data['rota'] = [('A', '  41 ', 'VAL', 0.1100385994559042, (-18.085, -5.668, -17.011))]
data['cbeta'] = []
data['probe'] = [(' A  33  PRO  HA ', ' A  42  THR HG22', -0.68, (-18.692, -6.669, -11.394)), (' A 207  TYR  CE1', ' B  47  GLY  HA3', -0.606, (-30.466, 31.595, 8.971)), (' A 162  LEU HD13', ' B  74  ARG  HB3', -0.583, (-38.093, 17.876, -9.04)), (' A  26  THR HG23', ' A  29  GLN  H  ', -0.573, (-16.798, -13.614, -13.831)), (' A  11  VAL HG11', ' A  68  ALA  HB2', -0.568, (-11.031, 2.452, -2.919)), (' A 283  TYR  HE1', ' A 292  LYS  HE2', -0.557, (-21.967, 38.959, -21.852)), (' A 284  CYS  HB3', ' A 291  THR HG23', -0.556, (-29.063, 35.088, -19.851)), (' A 283  TYR  CE1', ' A 292  LYS  HE2', -0.555, (-21.933, 39.162, -21.637)), (' A 113  LEU HD11', ' A 152  LEU HD21', -0.541, (-25.777, 14.29, -11.211)), (' A  11  VAL HG23', ' A  64  LEU HD22', -0.536, (-8.68, -1.314, -5.685)), (' A 253  LEU  HB2', ' A 296  TYR  HB3', -0.51, (-29.867, 39.821, -11.738)), (' A  18  THR  O  ', ' A  19  GLN  NE2', -0.502, (-3.13, -8.401, -9.831)), (' A  26  THR HG22', ' A  29  GLN  HG3', -0.501, (-17.844, -15.608, -13.819)), (' A 147  PHE  CE2', ' A 151  ILE HD11', -0.493, (-18.183, 19.41, -9.445)), (' A 109  ASN  ND2', ' A 160  GLY  O  ', -0.491, (-34.216, 13.186, -14.361)), (' A  33  PRO  HA ', ' A  42  THR  CG2', -0.485, (-19.276, -6.594, -11.184)), (' A 207  TYR  HE2', ' A 210  THR HG22', -0.476, (-31.592, 35.376, 5.609)), (' A  13  ASN  HB2', ' A  56  TYR  OH ', -0.472, (-9.371, 5.548, -11.584)), (' A  59  PRO  HD3', ' A  80  LEU HD13', -0.466, (-14.432, 0.299, -3.863)), (' A 157  LYS  HE2', ' A 163  GLY  HA2', -0.458, (-31.169, 16.596, -7.128)), (' A 207  TYR  CE2', ' A 210  THR HG22', -0.45, (-31.053, 35.216, 5.997)), (' A 208  MET  HE2', ' B  70  VAL HG21', -0.441, (-35.489, 25.717, 3.067)), (' A  33  PRO  HB2', ' A  58  LEU  HG ', -0.441, (-17.545, -4.139, -7.253)), (' A 136  TYR  OH ', ' A 140  ARG  NH1', -0.434, (-12.977, 26.036, -9.09)), (' B  42  ARG  HB2', ' B  70  VAL HG23', -0.433, (-36.338, 23.138, 3.471)), (' A 181  CYS  HA ', ' A 238  GLU  O  ', -0.428, (-14.707, 31.774, 7.99)), (' A   8  PHE  CE2', ' A  18  THR HG22', -0.424, (0.041, -4.341, -14.372)), (' A 105  LYS  HG3', ' A 106 BTRP  N  ', -0.42, (-27.201, 20.317, -23.098)), (' A 105  LYS  HG3', ' A 106 ATRP  N  ', -0.419, (-27.204, 20.323, -23.099)), (' A 170  SER  O  ', ' A 174  GLN  HG2', -0.416, (-22.181, 19.558, 3.07)), (' A 255  HIS  NE2', ' A 279  LYS  O  ', -0.416, (-19.941, 43.65, -13.538)), (' A 185  LEU  O  ', ' A 196  GLN  HA ', -0.41, (-24.529, 36.165, 18.776)), (' A  95  TYR  CD2', ' A 144  ALA  HB3', -0.404, (-18.282, 18.616, -17.565))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
