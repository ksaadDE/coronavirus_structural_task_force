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
data['rama'] = [('A', '  28 ', 'ASN', 0.032428818145238056, (-0.5470000000000164, -81.33699999999997, 32.345)), ('B', '  28 ', 'ASN', 0.03331408086653337, (72.867, -38.481, -17.375))]
data['omega'] = []
data['rota'] = [('A', '  34 ', 'LYS', 0.2848553446748057, (-6.705000000000011, -66.927, 27.781)), ('A', ' 103 ', 'SER', 0.004019992775283754, (17.733999999999995, -68.814, 35.25299999999999)), ('A', ' 245 ', 'LEU', 0.20031124026895442, (15.67100000000002, -107.26599999999998, 3.883)), ('A', ' 325 ', 'THR', 0.09825704167066474, (32.935, -87.93999999999997, 12.737999999999998)), ('B', '  34 ', 'LYS', 0.05554464082222686, (71.40899999999999, -22.801, -12.788)), ('B', ' 147 ', 'SER', 0.07568188043153726, (32.168, -42.146, 8.238)), ('B', ' 173 ', 'LYS', 0.0, (45.357, -38.152, 10.914)), ('B', ' 226 ', 'LYS', 0.26769324798830374, (53.736, -69.076, 28.933999999999997)), ('B', ' 245 ', 'LEU', 0.2484436359676529, (71.186, -68.642, 11.196)), ('B', ' 307 ', 'LYS', 0.0, (48.821, -69.831, 19.959)), ('B', ' 308 ', 'SER', 0.12946874760707264, (45.749000000000024, -70.335, 17.756)), ('B', ' 346 ', 'GLN', 0.043652321453180265, (57.626000000000005, -69.818, -2.291))]
data['cbeta'] = []
data['probe'] = [(' B 280  ILE HG13', ' B 501  HOH  O  ', -0.864, (71.523, -59.795, 8.476)), (' B 263  PHE  HD1', ' B 501  HOH  O  ', -0.718, (71.443, -58.275, 9.443)), (' B  12  LYS  HD2', ' B  18  GLN  HG3', -0.653, (54.225, -21.812, -5.839)), (' B  14  HIS  CE1', ' B  63  ILE HD13', -0.65, (53.005, -30.454, -1.948)), (' B 127  VAL  HB ', ' B 130  GLN  HG3', -0.643, (39.863, -36.619, -3.995)), (' A 127  VAL  HB ', ' A 130  GLN  HG3', -0.639, (27.572, -64.1, 18.663)), (' A  12  LYS  HD2', ' A  18  GLN  HG3', -0.639, (8.121, -57.065, 20.634)), (' B 344  LYS  HZ3', ' B 346  GLN HE21', -0.628, (54.065, -71.786, -1.567)), (' B  57  LEU HD11', ' B 105  THR HG21', -0.625, (54.964, -40.923, -15.502)), (' A 212  ASP  O  ', ' A 216  LEU  HB2', -0.615, (19.635, -94.479, -14.218)), (' B 344  LYS  NZ ', ' B 346  GLN HE21', -0.613, (53.244, -71.659, -1.315)), (' A  57  LEU HD11', ' A 105  THR HG21', -0.608, (16.82, -75.315, 30.33)), (' A  14  HIS  CE1', ' A  63  ILE HD13', -0.594, (12.87, -64.495, 16.154)), (' B  84  VAL HG23', ' B 101  VAL HG11', -0.584, (50.934, -37.884, -11.024)), (' B 200  LEU HD11', ' B 254  LEU  HB3', -0.58, (66.544, -56.612, 13.073)), (' B 264  GLU  O  ', ' B 501  HOH  O  ', -0.575, (71.793, -59.361, 8.185)), (' A 200  LEU HD11', ' A 254  LEU  HB3', -0.568, (14.13, -94.492, 1.282)), (' A  84  VAL HG23', ' A 101  VAL HG11', -0.564, (18.124, -70.275, 25.912)), (' B 344  LYS  NZ ', ' B 346  GLN  NE2', -0.563, (53.139, -71.15, -1.37)), (' A 402  WUJ  C08', ' A 572  HOH  O  ', -0.543, (39.604, -75.568, 11.379)), (' B 344  LYS  HZ2', ' B 346  GLN  NE2', -0.523, (52.889, -71.474, -0.929)), (' A 189  LEU  H  ', ' A 402  WUJ  C08', -0.502, (40.146, -78.392, 11.485)), (' A 148  VAL HG11', ' A 151  LEU HD12', -0.499, (39.185, -67.344, 14.519)), (' B 249  HIS  NE2', ' B 401  CIT  O5 ', -0.491, (63.54, -68.94, 9.056)), (' B 303  VAL  O  ', ' B 307  LYS  HB2', -0.487, (49.49, -67.169, 20.128)), (' B 148  VAL HG11', ' B 151  LEU HD12', -0.478, (31.641, -44.519, 0.898)), (' A 266  GLU  HB3', ' A 279  PHE  HB3', -0.472, (11.295, -100.177, 12.855)), (' B   8  ASN  HB3', ' B  15  PHE  HA ', -0.465, (55.773, -27.558, -8.175)), (' B 266  GLU  HB3', ' B 279  PHE  HB3', -0.455, (71.876, -60.408, 1.81)), (' B  84  VAL  CG2', ' B 101  VAL HG11', -0.446, (51.558, -38.25, -10.875)), (' A   8  ASN  HB3', ' A  15  PHE  HA ', -0.443, (9.494, -63.519, 22.937)), (' B 264  GLU  C  ', ' B 501  HOH  O  ', -0.439, (71.892, -58.468, 8.316)), (' A 226  LYS  HD3', ' A 226  LYS  N  ', -0.42, (30.549, -97.502, -14.974)), (' B  74  ASN  HB3', ' B 325  THR  HB ', -0.415, (47.55, -57.626, 0.754)), (' A  84  VAL  CG2', ' A 101  VAL HG11', -0.411, (18.039, -70.95, 25.773)), (' A  74  ASN  HB3', ' A 325  THR  HB ', -0.405, (30.982, -86.186, 14.121)), (' B 305  ILE  O  ', ' B 309  GLN  HG2', -0.402, (48.724, -70.064, 15.19)), (' B 246  GLY  HA2', ' B 401  CIT  O4 ', -0.401, (67.029, -71.335, 11.403))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
