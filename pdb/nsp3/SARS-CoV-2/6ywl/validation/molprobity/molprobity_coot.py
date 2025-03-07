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
data['omega'] = [('C', '  47 ', 'GLY', None, (20.412000000000006, 30.062000000000015, 56.019000000000005)), ('D', '  47 ', 'GLY', None, (22.32, 47.61300000000001, 41.018))]
data['rota'] = [('A', '   5 ', 'SER', 0.015739494160213804, (24.539000000000005, 79.73000000000003, 13.515000000000002)), ('B', ' 122 ', 'LEU', 0.274908304727265, (35.198, -17.477000000000007, 32.37)), ('C', ' 107 ', 'GLN', 0.06455119109373354, (3.630999999999999, 14.348, 56.87)), ('D', '   7 ', 'SER', 0.07520773309000378, (38.226, 29.943, 27.990000000000002))]
data['cbeta'] = []
data['probe'] = [(' E 147  VAL HG11', ' E 151  VAL  CG2', -0.775, (46.346, 23.034, 16.307)), (' B  99  ASN  OD1', ' B 102  LYS  CE ', -0.769, (51.05, 0.794, 29.078)), (' C 147  VAL HG11', ' C 151  VAL  CG2', -0.694, (13.313, 12.242, 42.271)), (' C  28  LYS  O  ', ' C  31  LYS  HE2', -0.602, (28.529, 25.611, 35.376)), (' E 147  VAL HG11', ' E 151  VAL HG21', -0.601, (46.351, 22.621, 17.277)), (' D  79  GLY  HA2', ' D 203  EDO  H22', -0.595, (30.509, 58.521, 25.539)), (' B  99  ASN  OD1', ' B 102  LYS  HE3', -0.58, (50.109, 1.255, 29.551)), (' C  42  TYR  CE1', ' C  74  PRO  HG3', -0.57, (4.363, 35.204, 53.237)), (' E   6  PHE  CE2', ' E  30  VAL HG11', -0.568, (37.293, 25.771, 9.181)), (' B  47  GLY  O  ', ' B 201  APR  O1D', -0.56, (42.996, -2.209, 23.772)), (' B  99  ASN  C  ', ' B  99  ASN HD22', -0.549, (53.055, -2.489, 30.266)), (' B  99  ASN  OD1', ' B 102  LYS  HE2', -0.545, (50.876, 1.289, 28.838)), (' C 147  VAL HG11', ' C 151  VAL HG21', -0.528, (13.421, 12.204, 43.258)), (' E  99  ASN  OD1', ' E 101  ASN  HB2', -0.511, (46.155, 0.335, 16.497)), (' E  99  ASN  ND2', ' E 102  LYS  HD3', -0.479, (48.063, -0.078, 13.994)), (' B  99  ASN HD21', ' B 101  ASN  HB2', -0.477, (53.445, -1.058, 28.062)), (' C  46  GLY  O  ', ' C  51  GLY  HA3', -0.475, (21.686, 30.934, 52.981)), (' C  42  TYR  CZ ', ' C  74  PRO  HG3', -0.47, (4.243, 35.294, 54.162)), (' B  34  VAL HG11', ' B 122  LEU HD23', -0.464, (34.914, -14.253, 34.549)), (' A 161  TYR  CZ ', ' A 203  EDO  H22', -0.459, (29.076, 74.208, -1.753)), (' E 158  LYS  HE3', ' E 325  HOH  O  ', -0.457, (25.844, 18.194, 22.661)), (' C 128  SER  HA ', ' C 132  PHE  HB2', -0.439, (14.034, 20.921, 56.932)), (' A 124  ALA  O  ', ' A 153  LEU  HA ', -0.432, (32.863, 69.749, 7.823)), (' D  46  GLY  O  ', ' D  51  GLY  HA3', -0.431, (25.577, 46.773, 42.094)), (' C 170  GLU  CG ', ' C 171  MET  N  ', -0.431, (20.591, -1.491, 56.087)), (' E 124  ALA  O  ', ' E 153  LEU  HA ', -0.43, (39.419, 19.189, 14.85)), (' D 124  ALA  O  ', ' D 153  LEU  HA ', -0.429, (30.488, 40.473, 27.893)), (' E   9  TYR  HB3', ' E  17  TYR  HB3', -0.428, (36.345, 26.46, 18.516)), (' C 105  ASP  OD2', ' C 107  GLN  NE2', -0.428, (-0.131, 15.524, 58.731)), (' C 124  ALA  O  ', ' C 153  LEU  HA ', -0.425, (20.291, 15.945, 45.78)), (' E  46  GLY  O  ', ' E  51  GLY  HA3', -0.418, (37.234, 5.843, 5.841)), (' D  79  GLY  CA ', ' D 203  EDO  H22', -0.415, (30.529, 58.708, 26.285)), (' D  80  SER  HA ', ' D  94  HIS  O  ', -0.413, (31.803, 55.158, 29.92)), (' B 124  ALA  O  ', ' B 153  LEU  HA ', -0.412, (40.668, -16.739, 26.915)), (' B   2  MET  HB2', ' B   5  SER  HB3', -0.411, (25.238, -24.062, 25.481)), (' C   9  TYR  HB3', ' C  17  TYR  HB3', -0.41, (23.639, 9.521, 41.496)), (' C 167  SER  O  ', ' C 171  MET  HG3', -0.408, (19.219, 0.931, 56.462)), (' C  80  SER  HA ', ' C  94  HIS  O  ', -0.407, (8.105, 25.185, 46.025)), (' A   9  TYR  HB2', ' A 202  EDO  O2 ', -0.403, (24.031, 74.726, 5.959)), (' A  47  GLY  O  ', ' A 201  APR  O1D', -0.401, (47.706, 70.428, 8.806)), (' D   9  TYR  HB3', ' D  17  TYR  HB3', -0.4, (33.395, 33.258, 23.191))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
