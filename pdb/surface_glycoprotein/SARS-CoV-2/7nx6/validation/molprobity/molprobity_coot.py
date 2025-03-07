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
data['rama'] = [('H', '  99 ', 'ASP', 0.021062876811510794, (26.882, -26.759, -7.7059999999999995))]
data['omega'] = [('A', ' 108 ', 'PRO', None, (2.907999999999998, -40.194, -56.711)), ('A', ' 153 ', 'PRO', None, (-17.728, -19.675999999999984, -54.163999999999994)), ('A', ' 155 ', 'PRO', None, (-13.998000000000001, -23.092, -57.775)), ('B', '   8 ', 'PRO', None, (15.85099999999999, -17.820000000000007, -65.59799999999997)), ('B', ' 141 ', 'PRO', None, (0.932, -11.520999999999995, -80.951)), ('H', ' 155 ', 'PRO', None, (28.252999999999997, 4.8089999999999975, -15.540999999999999)), ('H', ' 157 ', 'PRO', None, (26.411999999999992, 1.1799999999999997, -10.953)), ('L', '   8 ', 'PRO', None, (1.3419999999999992, -18.241, -13.363999999999999)), ('L', ' 142 ', 'PRO', None, (-2.519999999999998, 0.771, -3.235))]
data['rota'] = [('L', '  45 ', 'LYS', 0.014313479445423556, (18.358, -18.326, -3.8099999999999996)), ('L', ' 182 ', 'LEU', 0.21762980383406602, (13.736999999999998, 21.497, -17.049999999999994)), ('E', ' 370 ', 'ASN', 0.07741949201520827, (38.898, -32.951, -22.985)), ('E', ' 469 ', 'SER', 0.06740197163905762, (17.361, -56.069, -42.60999999999999)), ('A', ' 185 ', 'SER', 0.23486891661416348, (-17.256, -17.62, -70.24)), ('B', '  34 ', 'LEU', 0.06135894068675219, (17.797999999999995, -32.073, -56.44899999999999)), ('B', '  49 ', 'ILE', 0.15555074620123055, (13.813, -35.275999999999975, -63.077)), ('B', '  78 ', 'ARG', 0.0, (13.609000000000004, -29.663, -78.529)), ('B', '  93 ', 'ASP', 0.28861633227659145, (17.656999999999996, -29.992, -46.263999999999996)), ('B', ' 176 ', 'SER', 0.047381761956996976, (-13.003, -12.144, -73.659))]
data['cbeta'] = []
data['probe'] = [(' A  82  MET  HB3', ' A  85  LEU HD21', -0.744, (-6.558, -25.088, -43.008)), (' E 498  GLN  HB3', ' E 707   CL CL  ', -0.636, (31.729, -33.364, -53.71)), (' E 376  THR  HB ', ' E 435  ALA  HB3', -0.629, (27.184, -33.332, -32.052)), (' B 106  ILE  O  ', ' B 166  GLN  NE2', -0.621, (3.852, -18.593, -77.18)), (' E 340  GLU  OE1', ' E 356  LYS  NZ ', -0.62, (37.73, -51.965, -27.74)), (' E 412  PRO  HG3', ' E 429  PHE  HB3', -0.611, (17.736, -39.384, -23.842)), (' H  83  MET  HB3', ' H  86  LEU HD21', -0.584, (32.716, -10.685, -22.065)), (' L  39  LYS  HD3', ' L  84  ALA  HB2', -0.556, (12.396, -11.745, -2.99)), (' B  62  ARG  NH1', ' B 305  SO4  O3 ', -0.545, (9.324, -34.964, -77.021)), (' E 455  LEU HD22', ' E 493  GLN  HG3', -0.539, (16.158, -42.83, -49.811)), (' L 109  ARG HH12', ' L 112  ALA  HB2', -0.531, (-1.028, 0.406, 3.333)), (' L 187  TYR  O  ', ' L 193  TYR  OH ', -0.522, (10.115, 28.052, -13.551)), (' A  87  ALA  N  ', ' A 302   CL CL  ', -0.503, (-6.992, -14.776, -44.008)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.498, (12.09, -18.776, -3.612)), (' B  81  PRO  HA ', ' B 106  ILE HD13', -0.498, (5.092, -24.356, -77.265)), (' H   6  GLU  H  ', ' H 113  GLN HE22', -0.496, (31.545, -10.861, -5.323)), (' L  39  LYS  HB2', ' L  42  LYS  HD3', -0.492, (16.526, -9.92, -2.408)), (' L 147  VAL HG21', ' L 176  LEU HD22', -0.491, (4.301, 9.959, -8.737)), (' H  91  THR HG23', ' H 118  THR  HA ', -0.487, (26.759, -3.408, -19.432)), (' L 109  ARG  HD2', ' L 172  SER  HB2', -0.486, (2.145, -4.154, 2.19)), (' E 379  CYS  SG ', ' E 384  PRO  HG3', -0.486, (27.832, -34.139, -20.74)), (' E 439  ASN  O  ', ' E 443  SER  OG ', -0.478, (34.877, -35.334, -46.484)), (' B 185  ASP  HA ', ' B 188  LYS  HE2', -0.478, (-30.422, 2.346, -70.424)), (' H 131  PRO  HD3', ' H 217  LYS  HD3', -0.476, (23.496, 19.593, -2.074)), (' B 166  GLN  HG3', ' B 173  TYR  CZ ', -0.474, (0.485, -16.497, -75.07)), (' E 350  VAL HG22', ' E 422  ASN  HB3', -0.46, (20.691, -44.888, -37.999)), (' E 393  THR  HA ', ' E 522  ALA  HA ', -0.457, (28.085, -51.949, -12.038)), (' B  19  ALA  HB3', ' B  76  ILE  HB ', -0.456, (13.507, -26.665, -73.134)), (' B  11  LEU  O  ', ' B 105  ASP  N  ', -0.451, (8.508, -18.988, -71.93)), (' H 208  HIS  CD2', ' H 210  PRO  HD2', -0.45, (29.714, 4.35, -10.677)), (' B  55  ARG  HG2', ' B  59  ILE  HB ', -0.448, (11.889, -38.506, -67.812)), (' E 499  PRO  HD2', ' E 707   CL CL  ', -0.445, (33.229, -33.616, -53.038)), (' B 183  LYS  O  ', ' B 187  GLU  HG2', -0.443, (-33.255, -3.033, -71.787)), (' L   4  MET  HE1', ' L  25  ALA  HB2', -0.439, (10.175, -27.965, -17.661)), (' A  11  LEU  HB2', ' A 153  PRO  HG3', -0.438, (-16.284, -21.099, -51.373)), (' L  35  TRP  CD2', ' L  73  LEU  HB2', -0.434, (8.219, -23.766, -7.681)), (' H  36  TRP  CE2', ' H  81  LEU  HB2', -0.434, (33.296, -16.32, -14.758)), (' H  12  VAL HG11', ' H  86  LEU HD13', -0.431, (33.073, -6.218, -21.594)), (' A 155  PRO  HA ', ' A 301   CL CL  ', -0.428, (-13.903, -21.267, -60.455)), (' B  90  GLN  HG2', ' B  97  ARG  O  ', -0.427, (11.811, -28.228, -52.993)), (' B 145  LYS  HB3', ' B 197  THR  OG1', -0.425, (-6.503, -1.864, -80.11)), (' B 197  THR HG22', ' B 204  PRO  HG3', -0.421, (-7.668, -0.347, -84.808)), (' A  29  VAL HG13', ' A  34  MET  HG3', -0.419, (-0.658, -41.45, -47.024)), (' E 342  PHE  CD1', ' E 368  LEU HD11', -0.419, (35.936, -41.17, -26.207)), (' E 393  THR HG21', ' E 518  LEU  HB2', -0.419, (23.345, -53.47, -12.649)), (' B  34  LEU  HG ', ' B  72  PHE  CG ', -0.418, (20.444, -29.08, -58.669)), (' B  93  ASP  OD1', ' B  94  THR  N  ', -0.412, (16.162, -28.815, -44.804)), (' L 126  LEU  HB3', ' L 184  LYS  NZ ', -0.411, (19.696, 28.764, -10.81)), (' A  50  VAL HG21', ' A  99  GLU  HG3', -0.409, (7.676, -35.806, -45.953)), (' B 113  PRO  HB3', ' B 139  PHE  HB3', -0.405, (-6.256, -12.465, -82.019)), (' H 167  LEU HD21', ' H 190  VAL HG21', -0.405, (17.241, 9.181, 7.324)), (' L  35  TRP  CE2', ' L  73  LEU  HB2', -0.404, (7.911, -24.156, -7.875))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
