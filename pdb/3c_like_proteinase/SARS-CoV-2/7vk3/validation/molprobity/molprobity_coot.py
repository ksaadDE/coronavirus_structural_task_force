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
data['rama'] = [('A', ' 119 ', 'ASN', 0.012229567645332968, (-22.685, 0.569, -15.23)), ('A', ' 119 ', 'ASN', 0.013221335339806871, (-22.685, 0.569, -15.23)), ('A', ' 154 ', 'TYR', 0.027020991047908605, (-4.191999999999999, 22.356, -15.407999999999998))]
data['omega'] = [('A', '  33 ', 'ASP', None, (-23.26, 19.582, -17.235)), ('A', ' 166 ', 'GLU', None, (-17.011, -2.3059999999999996, -30.419000000000004))]
data['rota'] = [('A', ' 155 ', 'ASP', 0.04693318917182385, (-7.890999999999998, 22.325, -14.384999999999998)), ('A', ' 222 ', 'ARG', 0.0, (27.088999999999995, 9.396999999999997, -39.044)), ('B', '  86 ', 'VAL', 0.06801480498806263, (7.591999999999999, 8.094, 8.598)), ('B', '  86 ', 'VAL', 0.07168195809148209, (7.587999999999998, 8.088, 8.605))]
data['cbeta'] = [('A', '  84 ', 'ASN', ' ', 0.3211872935523643, (-23.881, 13.149, -35.239)), ('A', ' 119 ', 'ASN', ' ', 0.30262869482551197, (-23.367, -0.572, -14.474)), ('B', '  33 ', 'ASP', ' ', 0.2535488284524936, (-8.390000000000004, 10.704, 10.537)), ('B', '  76 ', 'ARG', ' ', 0.25443497288699096, (-1.5809999999999995, 24.594, 12.818))]
data['probe'] = [(' A 228  ASN  OD1', ' A 401  HOH  O  ', -0.916, (12.499, 15.33, -50.577)), (' B 140  PHE  HD2', ' B 172  HIS  HD1', -0.8, (9.551, 6.135, -9.03)), (' B 178  GLU  OE1', ' B 403  HOH  O  ', -0.772, (2.832, -2.226, 9.089)), (' B   3  PHE  O  ', ' B 402  HOH  O  ', -0.77, (-3.238, -5.479, -24.494)), (' B 233  VAL HG11', ' B 269  LYS  HG3', -0.705, (12.704, -25.287, -19.31)), (' A 153  ASP  OD1', ' A 402  HOH  O  ', -0.674, (-3.167, 18.583, -21.909)), (' A 217  ARG  HD3', ' A 220  LEU HD12', -0.666, (24.987, 9.673, -29.975)), (' A 221  ASN  OD1', ' A 403  HOH  O  ', -0.655, (22.809, 9.243, -38.587)), (' B 198  THR  OG1', ' B 240  GLU  OE1', -0.649, (12.526, -13.644, -8.966)), (' A 263  ASP  OD1', ' A 403  HOH  O  ', -0.646, (23.12, 10.787, -38.491)), (' B 233  VAL HG21', ' B 269  LYS  HD2', -0.632, (13.022, -27.459, -18.662)), (' B  97  LYS  NZ ', ' B 401  HOH  O  ', -0.603, (-9.52, 17.705, -3.405)), (' B 166  GLU  HG3', ' B 172  HIS  CD2', -0.585, (13.981, 6.702, -9.015)), (' A 293  PRO  O  ', ' A 297  VAL HG13', -0.578, (7.678, 17.719, -27.7)), (' B 140  PHE  HB2', ' B 172  HIS  CE1', -0.573, (10.655, 8.129, -9.197)), (' B  52  PRO  HD2', ' B 188  ARG  HG2', -0.561, (21.678, 9.173, 7.383)), (' B 245  ASP  O  ', ' B 249  ILE HG12', -0.553, (-0.719, -20.782, -5.424)), (' A   8  PHE  HB3', ' A 152  ILE HD13', -0.546, (-6.172, 13.693, -16.594)), (' A 166  GLU  OE2', ' A 170  GLY  HA2', -0.543, (-12.366, -7.356, -30.755)), (' A   2  GLY  HA3', ' A 407  HOH  O  ', -0.542, (13.602, 3.576, -16.454)), (' B  17  MET  HG3', ' B 117  CYS  SG ', -0.536, (-1.031, 12.918, -4.593)), (' A 111  THR HG22', ' A 129  ALA  HB2', -0.535, (-0.933, 7.92, -28.189)), (' B 140  PHE  HD1', ' B 144  SER  HB2', -0.53, (7.425, 10.342, -7.515)), (' B  27  LEU HD21', ' B  42  VAL  HB ', -0.526, (9.904, 15.442, 3.763)), (' A 221  ASN  HB2', ' A 222 AARG  NH1', -0.521, (25.705, 5.363, -39.612)), (' A  27  LEU HD21', ' A  42  VAL  HB ', -0.509, (-26.746, 3.285, -25.223)), (' A 136  ILE HD11', ' A 140  PHE  HE2', -0.508, (-11.843, 2.177, -26.458)), (' A 300  CYS  SG ', ' A 450  HOH  O  ', -0.498, (12.761, 20.942, -21.224)), (' A  33  ASP  O  ', ' A  94  ALA  HA ', -0.493, (-26.587, 19.41, -14.591)), (' A  52  PRO  HD2', ' A 188  ARG  HG2', -0.49, (-27.47, -0.34, -39.06)), (' A  55  GLU  CD ', ' A  55  GLU  H  ', -0.489, (-33.663, 7.611, -38.038)), (' B 140  PHE  H  ', ' B 172  HIS  HE1', -0.488, (11.064, 7.73, -10.698)), (' B 129  ALA  HB3', ' B 290  GLU  HG2', -0.485, (5.116, -6.208, -11.613)), (' A 299  GLN  HG2', ' A 299  GLN  O  ', -0.477, (9.629, 14.618, -18.349)), (' A 167  LEU HD12', ' A 171  VAL HG23', -0.471, (-11.27, -1.768, -34.604)), (' B 109  GLY  HA2', ' B 200  ILE HD13', -0.468, (5.968, -9.917, -9.098)), (' B 130  MET  HE1', ' B 182  TYR  CG ', -0.465, (7.833, -2.898, -0.503)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.459, (0.03, 8.092, -33.132)), (' B 166  GLU  HG3', ' B 172  HIS  NE2', -0.459, (14.118, 7.229, -8.847)), (' B 114  VAL HG11', ' B 140  PHE  HZ ', -0.456, (5.106, 6.067, -7.218)), (' B  70  ALA  O  ', ' B  73  VAL HG22', -0.454, (-5.859, 23.213, 1.692)), (' B 222  ARG  NH2', ' B 408  HOH  O  ', -0.434, (0.545, -37.089, -27.591)), (' B  49  MET  HA ', ' B  52  PRO  HG3', -0.432, (20.983, 12.183, 5.921)), (' B  92  ASP  CB ', ' B 407  HOH  O  ', -0.432, (-5.799, 23.975, 14.302)), (' A 115  LEU HD11', ' A 122  PRO  HB3', -0.429, (-13.368, 5.121, -13.41)), (' B  27  LEU HD13', ' B  39  PRO  HD2', -0.427, (7.543, 12.899, 2.299)), (' A 140  PHE  HB2', ' A 172  HIS  NE2', -0.426, (-13.081, -2.625, -25.951)), (' B 178  GLU  OE2', ' B 404  HOH  O  ', -0.424, (-0.256, 0.259, 11.233)), (' B 294  PHE  O  ', ' B 298  ARG  HG3', -0.423, (-8.32, -9.601, -10.375)), (' B 165 AMET  HB2', ' B 165 AMET  HE2', -0.423, (15.173, 4.709, -1.563)), (' B  75  LEU HD23', ' B  91  VAL HG11', -0.42, (-2.783, 18.901, 8.551)), (' A 136  ILE HD11', ' A 140  PHE  CE2', -0.419, (-11.539, 2.154, -26.253)), (' B 162  MET  HB2', ' B 162  MET  HE3', -0.418, (3.624, 6.275, 2.16)), (' B 288  GLU  OE2', ' B 290  GLU  N  ', -0.414, (4.347, -7.791, -15.755)), (' B 276  MET  HB3', ' B 276  MET  HE2', -0.413, (6.986, -16.067, -29.822)), (' B 171  VAL  O  ', ' B 172  HIS  HD2', -0.407, (14.426, 4.6, -8.447)), (' A  37  TYR  CE2', ' A  88  LYS  HD3', -0.406, (-24.526, 16.851, -25.664)), (' B  90  LYS  HB2', ' B  90  LYS  HE3', -0.406, (-0.702, 13.995, 16.362)), (' B 114  VAL HG11', ' B 140  PHE  CZ ', -0.405, (5.165, 6.076, -7.467)), (' A 140  PHE  HD2', ' A 172  HIS  CG ', -0.404, (-12.712, -0.67, -27.156)), (' B 108  PRO  HA ', ' B 130  MET  HG2', -0.404, (7.161, -7.366, -4.025)), (' A  27  LEU HD13', ' A  39  PRO  HD2', -0.403, (-23.891, 5.158, -23.957)), (' A  33  ASP  OD1', ' A  98  THR HG21', -0.402, (-20.989, 21.411, -15.767)), (' B 220  LEU  O  ', ' B 405  HOH  O  ', -0.402, (0.198, -26.358, -29.121))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
