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
data['rota'] = [('A', '  46 ', 'SER', 0.015435585700206058, (14.754999999999995, 26.238000000000003, 37.00700000000001)), ('A', '  93 ', 'THR', 0.0014372516579003927, (13.447000000000001, -5.662000000000001, 37.183)), ('A', ' 217 ', 'ARG', 0.0, (-9.328000000000003, 13.964, -10.14)), ('B', '  22 ', 'CYS', 0.29733543559535547, (-17.87600000000001, -19.40500000000001, 9.593)), ('B', '  27 ', 'LEU', 0.23149310793625952, (-14.244, -11.115, 10.206000000000003)), ('B', '  75 ', 'LEU', 0.2664669635250008, (-11.318000000000003, -20.192, 21.633000000000003)), ('B', '  86 ', 'VAL', 0.2626681656228144, (-24.667000000000005, -8.577000000000002, 16.382)), ('B', ' 125 ', 'VAL', 0.25009287208700004, (-5.894, 3.5230000000000006, 14.701000000000002)), ('B', ' 190 ', 'THR', 0.11011797083188915, (-28.641, -4.043, -1.252))]
data['cbeta'] = []
data['probe'] = [(' B  22 BCYS  SG ', ' B  61  LYS  HE3', -0.742, (-21.784, -20.788, 9.396)), (' A  60  ARG  NE ', ' A 501  HOH  O  ', -0.68, (27.222, 20.533, 39.478)), (' A  86 AVAL HG13', ' A 179  GLY  HA2', -0.582, (18.51, 10.933, 22.997)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.564, (8.968, 14.2, 4.539)), (' B  15  GLY  O  ', ' B 402  PG4  H61', -0.545, (-7.48, -9.556, 24.152)), (' A   6  MET  HE2', ' B 126  TYR  CD1', -0.53, (-7.471, 4.184, 9.646)), (' B  86 AVAL HG13', ' B 179  GLY  HA2', -0.528, (-24.636, -5.263, 16.317)), (' B  75  LEU HD22', ' B  91  VAL  HB ', -0.525, (-14.047, -18.535, 23.978)), (' A   5  LYS  NZ ', ' A 506  HOH  O  ', -0.511, (-0.615, 16.008, 8.302)), (' B 115  LEU HD11', ' B 122  PRO  HB3', -0.48, (-4.931, -2.455, 16.045)), (' B  48  ASP  CB ', ' B 508  HOH  O  ', -0.469, (-26.124, -17.093, 3.168)), (' B 126  TYR  CE2', ' B 128  CYS  SG ', -0.469, (-11.926, 6.197, 10.981)), (' B  45  THR  O  ', ' B  49  MET  HG3', -0.464, (-24.006, -13.564, 1.972)), (' B 248  ASP  OD2', ' B 501  HOH  O  ', -0.459, (-28.476, 19.452, 28.12)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.446, (-20.241, 15.65, 14.038)), (' B  31  TRP  CE2', ' B  75  LEU HD11', -0.443, (-11.582, -15.218, 23.852)), (' A  83  GLN  O  ', ' A  86 AVAL HG22', -0.43, (21.527, 9.654, 24.956)), (' B 167  LEU HD11', ' B 185  PHE  CE1', -0.418, (-25.498, 4.386, 4.591)), (' B 126  TYR  HE2', ' B 128  CYS  SG ', -0.417, (-12.087, 6.235, 10.776)), (' B 113  SER  O  ', ' B 149  GLY  HA2', -0.414, (-13.121, 3.474, 17.542)), (' A  40  ARG  HD3', ' A  85  CYS  HA ', -0.408, (21.383, 14.426, 26.758)), (' A  31  TRP  CE2', ' A  95  ASN  HB2', -0.408, (10.359, -2.672, 32.357)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.405, (6.083, 7.688, 17.69))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
