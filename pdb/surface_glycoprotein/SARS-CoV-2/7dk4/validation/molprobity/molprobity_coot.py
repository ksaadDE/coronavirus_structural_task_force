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
data['omega'] = [('a', ' 151 ', 'PRO', None, (214.14899999999994, 138.795, 303.233)), ('a', ' 153 ', 'PRO', None, (211.799, 141.605, 297.9909999999999)), ('a', ' 193 ', 'PRO', None, (182.631, 130.203, 296.517)), ('b', '   8 ', 'PRO', None, (206.613, 172.04100000000003, 293.721)), ('b', '  28 ', 'SER', None, (224.69499999999994, 172.91200000000006, 285.74499999999995)), ('b', '  81 ', 'PRO', None, (195.894, 169.189, 278.939)), ('b', '  99 ', 'PRO', None, (227.474, 164.97400000000005, 289.4869999999999)), ('b', ' 145 ', 'PRO', None, (189.99699999999996, 161.16, 300.00499999999994)), ('c', ' 151 ', 'PRO', None, (148.835, 234.71000000000006, 308.393)), ('c', ' 153 ', 'PRO', None, (151.311, 234.753, 302.56999999999994)), ('c', ' 193 ', 'PRO', None, (155.75399999999996, 266.546, 300.43199999999996)), ('d', '   8 ', 'PRO', None, (181.671, 225.62300000000005, 296.837)), ('d', '  28 ', 'SER', None, (174.02199999999993, 207.788, 291.305)), ('d', '  81 ', 'PRO', None, (180.42600000000004, 236.067, 281.51899999999995)), ('d', '  99 ', 'PRO', None, (164.84099999999995, 210.07700000000006, 296.103)), ('d', ' 145 ', 'PRO', None, (179.98300000000003, 247.308, 302.052)), ('e', ' 151 ', 'PRO', None, (198.983, 218.66100000000006, 293.516)), ('e', ' 153 ', 'PRO', None, (202.363, 216.134, 288.7959999999999)), ('e', ' 193 ', 'PRO', None, (213.52199999999993, 189.409, 299.011)), ('f', '   8 ', 'PRO', None, (188.51599999999993, 208.75299999999993, 262.388)), ('f', '  28 ', 'SER', None, (192.78500000000005, 226.07599999999994, 254.69999999999996)), ('f', '  81 ', 'PRO', None, (203.01300000000006, 198.706, 257.059)), ('f', '  99 ', 'PRO', None, (194.01299999999998, 230.40799999999993, 264.133)), ('f', ' 145 ', 'PRO', None, (191.656, 192.806, 275.79199999999986))]
data['rota'] = [('a', '  95 ', 'CYS', 0.07956948787492289, (219.428, 149.864, 285.164)), ('c', '  95 ', 'CYS', 0.08882601683923558, (154.78299999999993, 223.66900000000004, 290.879)), ('c', ' 144 ', 'CYS', 0.030511990189552307, (154.40700000000004, 251.61200000000002, 304.6009999999999)), ('e', '  57 ', 'THR', 0.21374521984812161, (203.91700000000006, 236.513, 267.90499999999986)), ('e', '  95 ', 'CYS', 0.28052782373478935, (207.59699999999995, 223.755, 273.8559999999999)), ('e', ' 144 ', 'CYS', 0.06712637841701508, (203.959, 201.55000000000007, 296.19499999999994))]
data['cbeta'] = []
data['probe'] = [(' A1041  ASP  OD2', ' C 784  GLN  NE2', -0.693, (191.654, 196.297, 167.438)), (' A 968  SER  OG ', ' C 755  GLN  O  ', -0.693, (195.112, 202.481, 213.08)), (' A1032  CYS  SG ', ' A1051  SER  OG ', -0.683, (190.582, 210.254, 164.351)), (' C  33  THR  OG1', ' C 219  GLY  O  ', -0.675, (232.616, 166.021, 198.649)), (' A 755  GLN  O  ', ' B 968  SER  OG ', -0.673, (215.353, 212.315, 211.248)), (' C  78  ARG  NE ', ' C  80  ASP  OD1', -0.67, (251.194, 160.222, 216.085)), (' B 739  THR  OG1', ' C 319  ARG  NH2', -0.66, (226.586, 195.672, 203.1)), (' C1032  CYS  SG ', ' C1051  SER  OG ', -0.657, (203.533, 192.115, 161.838)), (' A 102  ARG  NH1', ' A 154  GLU  OE2', -0.64, (143.894, 204.799, 230.198)), (' a  66  ARG  NH2', ' a  84  SER  O  ', -0.637, (228.903, 151.425, 302.013)), (' d 152  TRP  NE1', ' d 181  SER  OG ', -0.624, (166.857, 249.21, 314.618)), (' A 398  ASP  OD2', ' A 423  TYR  OH ', -0.619, (215.289, 167.656, 250.074)), (' A 319  ARG  NH2', ' C 739  THR  OG1', -0.612, (191.829, 188.623, 206.54)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.595, (206.779, 195.991, 166.217)), (' d 112  ARG  NH1', ' d 175  SER  OG ', -0.59, (174.878, 246.824, 291.462)), (' d   7  SER  O  ', ' d  22  SER  OG ', -0.59, (182.368, 223.222, 294.755)), (' A 780  GLU  O  ', ' A 784  GLN  NE2', -0.581, (200.102, 217.262, 172.793)), (' c 142  LEU  O  ', ' c 185  VAL  N  ', -0.573, (159.337, 254.064, 299.782)), (' B 564  GLN  OE1', ' B 577  ARG  NH2', -0.572, (170.374, 219.753, 220.173)), (' b  65  ARG  NH2', ' b  86  ASP  OD1', -0.571, (198.787, 161.78, 282.535)), (' b 170  GLN  NE2', ' b 175  SER  O  ', -0.56, (192.982, 158.889, 292.592)), (' C  34  ARG  NH1', ' C 221  SER  OG ', -0.556, (230.84, 161.114, 201.678)), (' B 983  ARG  NH2', ' C 381  GLY  O  ', -0.554, (224.87, 208.353, 226.183)), (' A  29  THR  OG1', ' A 215  ASP  OD2', -0.553, (153.539, 188.932, 210.473)), (' B 909  ILE  O  ', ' B1108  ASN  ND2', -0.55, (202.379, 215.842, 150.416)), (' A1090  PRO  O  ', ' C 913  GLN  NE2', -0.548, (198.352, 195.67, 139.548)), (' A 645  THR  OG1', ' A 648  GLY  O  ', -0.545, (183.566, 178.066, 190.953)), (' b 134  ALA  N  ', ' b 185  LEU  O  ', -0.536, (197.659, 134.977, 315.62)), (' B 535  LYS  NZ ', ' B 554  GLU  OE1', -0.535, (172.722, 235.074, 209.816)), (' C 802  PHE  CD1', ' C 805  ILE HD11', -0.53, (200.143, 180.418, 158.006)), (' B 908  GLY  O  ', ' B1038  LYS  NZ ', -0.529, (203.977, 209.378, 152.236)), (' B 804  GLN  OE1', ' B 935  GLN  NE2', -0.528, (228.062, 223.146, 164.362)), (' C 287  ASP  OD1', ' C 288  ALA  N  ', -0.524, (226.373, 170.144, 197.1)), (' C 455  LEU  N  ', ' C 491  PRO  O  ', -0.523, (212.828, 224.408, 250.913)), (' C1000  ARG  O  ', ' C1003  SER  OG ', -0.523, (204.284, 192.256, 205.053)), (' B 553  THR  O  ', ' B 586  ASP  N  ', -0.52, (176.527, 228.383, 209.546)), (' c   6  GLN  NE2', ' c  95  CYS  SG ', -0.519, (152.174, 225.359, 293.103)), (' A  33  THR  OG1', ' A 219  GLY  O  ', -0.511, (160.12, 197.691, 206.066)), (' C 805  ILE HD12', ' C 878  LEU HD11', -0.509, (199.242, 181.594, 160.47)), (' C 717  ASN  OD1', ' C 718  PHE  N  ', -0.505, (215.624, 188.065, 146.281)), (' C 326  ILE HD12', ' C 539  VAL HG21', -0.503, (245.32, 205.183, 211.702)), (' C 762  GLN  OE1', ' C 765  ARG  NH2', -0.491, (192.048, 202.035, 199.769)), (' f  40  TYR  CE2', ' f  50  LEU HD13', -0.489, (204.979, 218.023, 262.869)), (' A 598  ILE HG23', ' A 664  ILE HG21', -0.487, (177.359, 187.647, 188.054)), (' A 908  GLY  O  ', ' A1038  LYS  NZ ', -0.48, (196.407, 205.794, 153.001)), (' A 758  SER  N  ', ' B 965  GLN  OE1', -0.475, (214.2, 213.705, 205.541)), (' A 108  THR  OG1', ' A 234  ASN  O  ', -0.472, (167.894, 194.933, 236.876)), (' B 611  LEU HD22', ' B 666  ILE HG23', -0.468, (199.133, 230.773, 192.36)), (' A 150  LYS  O  ', ' A 151  SER  OG ', -0.467, (132.609, 207.793, 231.201)), (' C 318  PHE  N  ', ' C 593  GLY  O  ', -0.467, (232.5, 195.454, 198.016)), (' C 880  GLY  O  ', ' C 885  GLY  N  ', -0.466, (192.147, 188.081, 156.419)), (' B 150  LYS  O  ', ' B 151  SER  OG ', -0.466, (250.268, 259.898, 229.392)), (' B 645  THR  OG1', ' B 648  GLY  O  ', -0.465, (194.31, 233.771, 193.135)), (' B 109  THR  OG1', ' B 111  ASP  OD1', -0.465, (221.005, 242.403, 241.38)), (' B 598  ILE HG23', ' B 664  ILE HG21', -0.463, (205.333, 233.237, 188.988)), (' A 287  ASP  OD1', ' A 288  ALA  N  ', -0.463, (166.152, 201.512, 203.483)), (' B 813  SER  OG ', ' B 868  GLU  OE1', -0.46, (234.135, 210.062, 171.854)), (' A 102  ARG  O  ', ' A 121  ASN  N  ', -0.459, (150.684, 204.58, 230.545)), (' A 611  LEU HD22', ' A 666  ILE HG23', -0.458, (183.018, 183.706, 189.972)), (' d  41  GLN  HB2', ' d  51  LEU HD11', -0.457, (171.432, 229.759, 287.682)), (' c 160  SER  N  ', ' c 200  ASN  OD1', -0.456, (148.516, 250.869, 294.378)), (' B 214  ARG  NH1', ' B 215  ASP  OD1', -0.454, (223.494, 254.92, 207.533)), (' A 487  ASN  ND2', ' b  96  ASN  O  ', -0.453, (227.505, 170.058, 281.28)), (' f  52  ILE HG23', ' f  57  ASN  O  ', -0.449, (205.925, 212.95, 255.656)), (' A1074  ASN  OD1', ' C 895  GLN  NE2', -0.448, (182.408, 186.393, 149.745)), (' A1081  ILE HD11', ' A1115  ILE HG21', -0.446, (192.568, 193.422, 131.841)), (' C 620  VAL HG21', ' C 651  ILE HD11', -0.446, (242.723, 192.445, 192.851)), (' C 366  SER  N  ', ' C 388  ASN  OD1', -0.446, (236.536, 203.736, 234.184)), (' A 280  ASN  OD1', ' A 284  THR  N  ', -0.443, (165.695, 213.207, 205.632)), (' b  41  GLN  HB2', ' b  51  LEU HD11', -0.443, (205.979, 161.597, 283.114)), (' C 708  SER  OG ', ' C 711  SER  OG ', -0.443, (227.494, 205.863, 143.294)), (' b  52  ILE HG23', ' b  57  ASN  O  ', -0.439, (209.889, 166.837, 275.97)), (' e 203  HIS  O  ', ' e 207  SER  N  ', -0.436, (207.897, 218.625, 294.869)), (' C 598  ILE HG23', ' C 664  ILE HG21', -0.436, (231.446, 187.723, 182.872)), (' B 975  SER  OG ', ' C 571  ASP  OD2', -0.434, (224.201, 212.354, 213.355)), (' e  99  GLY  N  ', ' e 103  ALA  O  ', -0.43, (208.815, 223.848, 262.769)), (' C 327  VAL HG12', ' C 542  ASN  HB3', -0.426, (240.48, 205.818, 219.252)), (' A 914  ASN  ND2', ' B1123  SER  OG ', -0.424, (183.77, 207.05, 139.621)), (' a  60  ASN  OD1', ' a  61  ALA  N  ', -0.418, (228.989, 161.378, 293.788)), (' A 717  ASN  OD1', ' A 718  PHE  N  ', -0.416, (177.884, 201.319, 151.928)), (' B 758  SER  OG ', ' C 965  GLN  NE2', -0.415, (211.392, 190.634, 202.201)), (' C 916  LEU  O  ', ' C 920  GLN  N  ', -0.411, (205.14, 184.842, 143.029)), (' a  90  THR HG23', ' a 114  THR  HA ', -0.41, (217.062, 146.879, 301.786)), (' A 489  TYR  OH ', ' b  96  ASN  OD1', -0.41, (223.627, 169.248, 279.691)), (' A 551  VAL  N  ', ' A 588  THR  O  ', -0.409, (195.279, 172.013, 206.789)), (' C 280  ASN  OD1', ' C 284  THR  N  ', -0.404, (217.209, 163.682, 199.918)), (' C 108  THR  OG1', ' C 234  ASN  O  ', -0.403, (234.211, 172.777, 229.898)), (' C1024  LEU  O  ', ' C1027  THR  OG1', -0.402, (201.804, 197.912, 170.658)), (' C  99  ASN  ND2', ' C 178  ASP  O  ', -0.401, (235.304, 145.359, 213.812))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
