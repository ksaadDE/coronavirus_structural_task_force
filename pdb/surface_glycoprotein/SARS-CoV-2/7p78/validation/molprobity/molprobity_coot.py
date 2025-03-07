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
data['rama'] = [('C', ' 332 ', 'ILE', 0.09522159126434201, (217.0350000000001, 243.879, 182.006))]
data['omega'] = [('A', ' 383 ', 'SER', None, (186.082, 190.524, 181.984)), ('C', ' 802 ', 'PHE', None, (172.11099999999996, 198.453, 253.746)), ('C', ' 982 ', 'SER', None, (189.829, 192.224, 184.814)), ('C', '1101 ', 'HIS', None, (189.543, 229.4270000000001, 280.224)), ('E', ' 333 ', 'THR', None, (234.597, 166.573, 183.862)), ('W', ' 106 ', 'PRO', None, (202.44899999999993, 252.83300000000006, 151.561)), ('Y', ' 106 ', 'PRO', None, (239.237, 181.346, 153.889))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' E1101  HIS  CE1', ' R   1  NAG  H5 ', -0.858, (224.231, 206.472, 285.721)), (' E1101  HIS  CE1', ' R   1  NAG  C5 ', -0.739, (224.155, 207.056, 285.02)), (' E1101  HIS  ND1', ' R   1  NAG  O6 ', -0.731, (223.391, 206.423, 283.641)), (' E1101  HIS  ND1', ' R   1  NAG  C5 ', -0.73, (224.376, 206.803, 284.399)), (' E1101  HIS  ND1', ' R   1  NAG  C6 ', -0.7, (223.452, 206.822, 283.972)), (' E1101  HIS  HE1', ' R   1  NAG  H5 ', -0.699, (224.325, 206.755, 286.422)), (' E 769  GLY  O  ', ' E 773  GLU  HB2', -0.664, (193.586, 212.993, 224.254)), (' C  52  GLN  HG2', ' C  52  GLN  O  ', -0.655, (176.438, 214.915, 194.942)), (' E1101  HIS  ND1', ' R   1  NAG  O5 ', -0.634, (224.848, 206.186, 284.372)), (' C1029  MET  O  ', ' C1033  VAL  HB ', -0.615, (188.393, 196.507, 247.253)), (' C 662  CYS  HB2', ' C 697  MET  HE1', -0.611, (186.529, 228.764, 231.569)), (' E 113  LYS  HD2', ' E 114  THR HG23', -0.596, (242.234, 219.095, 169.276)), (' E 360  ASN  H  ', ' E 523  THR  HB ', -0.595, (223.285, 164.26, 177.89)), (' C 329  PHE  HB2', ' C 530  SER  HB3', -0.593, (209.512, 243.117, 184.513)), (' C 563  GLN  HG2', ' E  43  PHE  HB2', -0.589, (221.523, 235.957, 201.32)), (' C 136  CYS  SG ', ' C 137  ASN  N  ', -0.586, (151.587, 232.771, 168.06)), (' E 401  VAL HG22', ' E 509  ARG  HG3', -0.579, (235.099, 165.535, 156.782)), (' C 596  SER  HB2', ' C 611  LEU  HB2', -0.571, (185.372, 231.461, 217.61)), (' C  56  LEU  O  ', ' C 273  ARG  NH2', -0.569, (169.042, 224.249, 198.891)), (' H  52  GLN  O  ', ' H  71  ARG  NH2', -0.561, (238.65, 180.374, 137.314)), (' Y  36  TRP  HB2', ' Y  49  ALA  HB3', -0.553, (245.52, 191.607, 156.502)), (' A 413  GLY  HA3', ' E 987  PRO  HG2', -0.552, (195.313, 209.453, 179.163)), (' C 909  ILE HD12', ' C1047  TYR  HB3', -0.548, (190.123, 209.395, 257.411)), (' A 498  GLN  HG3', ' A 500  THR  H  ', -0.545, (193.794, 203.915, 147.601)), (' A1098  ASN  ND2', ' F   1  NAG  O6 ', -0.544, (187.337, 182.343, 280.471)), (' Y  40  ALA  HB3', ' Y  43  LYS  HB2', -0.54, (242.75, 194.715, 141.701)), (' C 706  ALA  O  ', ' E 895  GLN  NE2', -0.54, (193.66, 232.38, 261.128)), (' E1028  LYS  NZ ', ' E1042  PHE  O  ', -0.539, (208.111, 209.9, 244.572)), (' A 788  ILE HD11', ' E 699  LEU  HB2', -0.539, (228.163, 198.984, 243.834)), (' Y  33  TYR  HB3', ' Y  99  ALA  HB3', -0.538, (235.866, 188.041, 162.891)), (' E 402  ILE HD11', ' E 418  ILE HD12', -0.536, (228.186, 170.037, 149.609)), (' A 101  ILE  HA ', ' A 242  LEU  HA ', -0.534, (207.911, 143.053, 188.169)), (' E 129  LYS  HB3', ' E 169  GLU  HG2', -0.532, (238.13, 236.88, 173.683)), (' C 655  HIS  HA ', ' C 694  ALA  HB3', -0.53, (182.348, 241.284, 226.533)), (' A 521  PRO  HD3', ' C  41  LYS  HE3', -0.529, (167.724, 201.09, 188.692)), (' C 346  ARG  NH1', ' C 347  PHE  O  ', -0.526, (227.036, 249.231, 153.656)), (' C  37  TYR  H  ', ' C  55  PHE  HE1', -0.525, (165.596, 216.349, 196.092)), (' W  40  ALA  HB3', ' W  43  LYS  HB2', -0.523, (189.887, 255.925, 139.627)), (' W  91  THR HG23', ' W 122  THR  HA ', -0.521, (179.544, 260.176, 144.399)), (' W  33  TYR  HB3', ' W  99  ALA  HB3', -0.517, (196.949, 246.589, 159.517)), (' C 970  PHE  O  ', ' C 995  ARG  NE ', -0.516, (195.458, 203.829, 195.294)), (' Y  50  ALA  HB3', ' Y  59  TYR  HB2', -0.516, (244.197, 184.838, 158.198)), (' C  99  ASN  OD1', ' C 190  ARG  NH2', -0.514, (144.373, 220.467, 188.897)), (' E 139  PRO  HB3', ' E 159  VAL HG23', -0.513, (252.166, 232.227, 176.597)), (' E 106  PHE  HB2', ' E 117  LEU  HB3', -0.513, (240.899, 228.025, 179.091)), (' C 542  ASN  HA ', ' C 547  THR HG22', -0.513, (206.304, 235.181, 189.999)), (' Y  67  ARG  NH1', ' Y  85  SER  O  ', -0.512, (256.831, 192.957, 149.038)), (' E 456  PHE  HB2', ' E 491  PRO  HB3', -0.51, (219.848, 163.794, 141.159)), (' C 314  GLN  NE2', ' C 317  ASN  OD1', -0.51, (190.064, 225.261, 210.501)), (' B  51  ILE HG12', ' B  57  THR HG22', -0.508, (207.987, 205.862, 150.681)), (' C 867  ASP  N  ', ' C 867  ASP  OD1', -0.507, (177.045, 188.528, 233.157)), (' Y  83  MET  HB3', ' Y  86  LEU HD21', -0.503, (254.241, 196.838, 152.24)), (' E  96  GLU  OE1', ' E 190  ARG  NH1', -0.501, (248.321, 239.005, 192.327)), (' E 332  ILE HG22', ' E 362  VAL HG21', -0.501, (232.89, 168.327, 181.713)), (' C 703  ASN  ND2', ' E 787  GLN  OE1', -0.501, (187.82, 229.185, 249.993)), (' B   4  LEU HD11', ' B  94  VAL HG12', -0.5, (205.073, 217.757, 159.062)), (' C 172  SER  OG ', ' C 173  GLN  N  ', -0.499, (150.324, 208.487, 182.429)), (' C 733  LYS  HB2', ' C 861  LEU  HB3', -0.498, (186.138, 188.822, 222.357)), (' E 136  CYS  SG ', ' E 137  ASN  N  ', -0.493, (256.574, 229.357, 172.931)), (' A 642  VAL HG22', ' A 651  ILE HG12', -0.493, (179.03, 168.461, 218.32)), (' E 357  ARG HH22', ' E 395  VAL  HB ', -0.493, (223.095, 167.058, 173.32)), (' A 230  PRO  HG2', ' E 521  PRO  HB3', -0.492, (216.602, 167.049, 181.202)), (' C1100  THR  HB ', ' C1101  HIS  CG ', -0.492, (187.489, 228.601, 280.763)), (' C1123  SER  OG ', ' E 914  ASN  ND2', -0.492, (210.704, 216.642, 274.924)), (' A 364  ASP  OD1', ' A 388  ASN  ND2', -0.49, (177.988, 184.374, 174.047)), (' A 374  PHE  HA ', ' A 436  TRP  HB3', -0.489, (188.201, 193.731, 162.014)), (' E 435  ALA  HB1', ' E 508  TYR  HB3', -0.488, (235.139, 173.458, 155.721)), (' E 357  ARG HH12', ' E 395  VAL  H  ', -0.486, (220.91, 167.765, 172.441)), (' C 193  VAL  HB ', ' C 204  TYR  HB2', -0.485, (161.522, 215.333, 191.138)), (' C 995  ARG  NH1', ' E 994  ASP  OD1', -0.484, (198.811, 204.526, 195.396)), (' A 353  TRP  O  ', ' A 466  ARG  NH1', -0.484, (178.14, 211.063, 166.825)), (' E 574  ASP  N  ', ' E 574  ASP  OD1', -0.483, (223.542, 177.47, 207.1)), (' C1148  PHE  HB3', ' C1149  LYS  HZ2', -0.483, (189.039, 206.356, 301.895)), (' C 402  ILE HD11', ' C 418  ILE HD12', -0.482, (216.198, 245.035, 145.495)), (' W  52  ILE HD12', ' W  57  HIS  HB2', -0.482, (200.945, 254.532, 163.609)), (' E 726  ILE HD13', ' E 945  LEU HD13', -0.481, (213.14, 220.111, 235.756)), (' A 501  ASN  ND2', ' A 505  TYR  O  ', -0.48, (195.228, 205.297, 153.625)), (' E1129  VAL  HB ', ' E1132  ILE HD11', -0.48, (212.673, 187.367, 277.823)), (' C 711  SER  OG ', ' E 895  GLN  NE2', -0.48, (194.166, 231.739, 263.044)), (' C 945  LEU HD12', ' C 948  LEU HD12', -0.479, (179.621, 203.018, 233.758)), (' A 189  LEU  HB3', ' A 208  THR  HB ', -0.479, (210.935, 148.257, 204.407)), (' A 357  ARG  NH2', ' A 394  ASN  OD1', -0.478, (170.387, 202.165, 177.494)), (' A  50  SER  OG ', ' A 304  LYS  NZ ', -0.477, (205.026, 175.956, 209.581)), (' E 329  PHE  O  ', ' E 580  GLN  NE2', -0.477, (235.139, 172.003, 190.772)), (' C 741  TYR  OH ', ' C 962  LEU  O  ', -0.475, (187.293, 198.365, 207.123)), (' C1106  GLN HE21', ' C1109  PHE  HB3', -0.475, (187.076, 214.055, 268.478)), (' C 364  ASP  HA ', ' C 527  PRO  HD3', -0.474, (212.534, 244.476, 173.396)), (' E 364  ASP  HA ', ' E 527  PRO  HD3', -0.474, (234.047, 172.333, 177.299)), (' C  34  ARG  NH2', ' C 217  PRO  O  ', -0.473, (154.49, 224.955, 202.054)), (' A 452  LEU HD21', ' A 492  LEU  HB3', -0.472, (186.487, 219.678, 158.58)), (' D  29  VAL  O  ', ' D  71  ARG  NH1', -0.472, (202.397, 254.045, 132.644)), (' A 382  VAL  O  ', ' C 983  ARG  NE ', -0.471, (185.1, 192.743, 179.755)), (' E 542  ASN  HA ', ' E 547  THR HG22', -0.471, (228.454, 181.882, 193.264)), (' C 280  ASN HD22', ' C1301  NAG  H82', -0.471, (158.956, 205.94, 209.301)), (' A 816  SER  OG ', ' A 817  PHE  N  ', -0.471, (220.773, 181.849, 246.426)), (' C 294  ASP  N  ', ' C 294  ASP  OD1', -0.47, (172.621, 226.561, 208.618)), (' C 726  ILE HD13', ' C 945  LEU HD13', -0.469, (179.552, 205.229, 235.562)), (' A1028  LYS  NZ ', ' A1042  PHE  O  ', -0.469, (202.35, 193.602, 245.981)), (' A  34  ARG  NH1', ' A 191  GLU  OE2', -0.469, (208.32, 152.238, 204.9)), (' C 129  LYS  HG2', ' C 169  GLU  HG2', -0.467, (153.727, 212.002, 171.223)), (' E 346  ARG  NH1', ' E 347  PHE  O  ', -0.466, (231.668, 158.777, 155.725)), (' E1127  ASP  N  ', ' E1127  ASP  OD1', -0.466, (210.062, 183.471, 281.677)), (' A1012  LEU HD23', ' E1013  ILE HG21', -0.465, (206.36, 204.203, 220.631)), (' C 452  LEU HD23', ' C 492  LEU  HB3', -0.464, (228.824, 246.951, 140.796)), (' C 802  PHE  HD1', ' C 805  ILE HD11', -0.464, (176.076, 198.713, 251.971)), (' C 498  GLN  O  ', ' C 506  GLN  NE2', -0.464, (216.595, 260.101, 146.468)), (' B  68  THR  HB ', ' B  81  GLN  HB3', -0.464, (210.881, 210.559, 142.605)), (' A 284  THR HG22', ' E 560  LEU HD11', -0.464, (219.073, 161.494, 208.095)), (' C 442  ASP  OD2', ' C 509  ARG  NH2', -0.464, (220.413, 255.119, 154.518)), (' E 172  SER  OG ', ' E 173  GLN  N  ', -0.463, (234.965, 243.526, 184.158)), (' E 574  ASP  HA ', ' E 587  ILE  HB ', -0.463, (226.603, 179.539, 205.685)), (' H  87  THR HG23', ' H 108  THR  HA ', -0.462, (238.17, 157.076, 122.641)), (' C 880  GLY  O  ', ' C 884  SER  HB3', -0.462, (183.895, 190.551, 255.584)), (' A 215  ASP  N  ', ' A 215  ASP  OD1', -0.461, (200.712, 143.815, 207.803)), (' Y  51  LEU HD21', ' Y  72  LEU  HB2', -0.461, (246.341, 190.672, 166.526)), (' W  20  LEU HD12', ' W  81  LEU HD23', -0.46, (185.772, 257.192, 154.219)), (' C 780  GLU  O  ', ' C 784  GLN  NE2', -0.459, (192.915, 192.189, 241.413)), (' C 715  PRO  HA ', ' C1072  GLU  HA ', -0.458, (184.746, 222.709, 263.105)), (' A 890  ALA  HA ', ' E1046  GLY  HA2', -0.457, (214.69, 208.015, 254.006)), (' E 763  LEU HD22', ' E1008  VAL HG11', -0.457, (197.48, 208.635, 212.31)), (' E  39  PRO  HG3', ' E  51  THR HG21', -0.456, (226.431, 224.183, 201.593)), (' E 810  SER  OG ', ' E 811  LYS  NZ ', -0.456, (209.331, 241.705, 241.281)), (' H  47  TRP  HE1', ' H  50  ALA  HB2', -0.455, (238.354, 170.7, 137.978)), (' E 105  ILE HD11', ' E 241  LEU HD22', -0.455, (249.775, 232.34, 178.882)), (' E 826  VAL  HB ', ' E1057  PRO  HG2', -0.455, (210.425, 225.374, 230.539)), (' C 650  LEU HD21', ' C 653  ALA  HB3', -0.454, (181.652, 237.563, 222.784)), (' C 357  ARG  NH2', ' C 523  THR  OG1', -0.454, (221.425, 234.885, 169.4)), (' C 858  LEU HD11', ' C 959  LEU HD22', -0.454, (184.459, 195.416, 213.138)), (' C 389  ASP  N  ', ' C 389  ASP  OD1', -0.453, (206.078, 239.347, 173.657)), (' A 715  PRO  HA ', ' A1072  GLU  HA ', -0.453, (191.435, 182.93, 265.937)), (' A 106  PHE  HB2', ' A 117  LEU  HB2', -0.452, (207.645, 157.06, 182.243)), (' C 433  VAL HG12', ' C 512  VAL HG22', -0.451, (213.288, 240.814, 155.96)), (' A  93  ALA  HB3', ' A 266  TYR  HB2', -0.451, (202.934, 149.905, 199.366)), (' H  66  ARG  NH2', ' H  86  ASP  OD2', -0.45, (245.782, 161.382, 127.916)), (' C 312  ILE HD13', ' C 666  ILE HD11', -0.449, (184.512, 228.474, 221.115)), (' A 656  VAL HG12', ' A 658  ASN  H  ', -0.449, (178.601, 168.462, 236.65)), (' E 324  GLU  H  ', ' E 539  VAL HG23', -0.447, (237.215, 186.862, 198.74)), (' C 729  VAL  H  ', ' C1059  GLY  HA2', -0.446, (185.631, 198.056, 233.978)), (' A 968  SER  OG ', ' A 969  ASN  N  ', -0.445, (207.156, 187.51, 201.005)), (' E 159  VAL HG13', ' E 160  TYR  HD1', -0.445, (249.187, 234.912, 173.487)), (' A 792  PRO  HG3', ' E 707  TYR  HB3', -0.443, (226.101, 191.874, 261.627)), (' A  92  PHE  O  ', ' A 192  PHE  N  ', -0.443, (208.13, 152.789, 197.385)), (' C 598  ILE HD13', ' C 609  ALA  HB3', -0.443, (179.924, 233.118, 220.52)), (' A 699  LEU  HB2', ' C 788  ILE HD11', -0.443, (182.433, 181.503, 243.832)), (' C1086  LYS  HB2', ' C1086  LYS  HE3', -0.443, (206.474, 220.237, 285.438)), (' E 969  ASN  HB3', ' E 972  ALA  H  ', -0.443, (210.556, 210.304, 193.912)), (' C 826  VAL  HB ', ' C1057  PRO  HG2', -0.442, (176.577, 199.752, 231.045)), (' E 328  ARG  HA ', ' E 328  ARG  HD2', -0.442, (235.324, 175.894, 192.797)), (' W   6  GLU  O  ', ' W 117  GLN  NE2', -0.441, (178.356, 248.517, 154.89)), (' C1046  GLY  HA2', ' E 890  ALA  HA ', -0.44, (189.357, 214.777, 252.417)), (' E 318  PHE  HZ ', ' E 615  VAL HG21', -0.44, (233.011, 196.158, 213.701)), (' Y  88  PRO  HA ', ' Y 123  VAL HG23', -0.439, (253.44, 198.926, 144.368)), (' E 627  ASP  N  ', ' E 627  ASP  OD1', -0.439, (243.437, 202.569, 204.454)), (' E  37  TYR  OH ', ' E  53  ASP  OD1', -0.438, (231.609, 222.885, 195.928)), (' E 327  VAL  HA ', ' E 542  ASN  HB3', -0.438, (232.52, 180.918, 192.24)), (' A 417  LYS  HE3', ' B  98  ARG  HB2', -0.438, (197.391, 219.136, 165.131)), (' E 389  ASP  N  ', ' E 389  ASP  OD1', -0.438, (230.201, 179.42, 178.314)), (' C1127  ASP  N  ', ' C1127  ASP  OD1', -0.438, (212.138, 226.871, 279.637)), (' E1106  GLN  NE2', ' E1111  GLU  OE2', -0.437, (211.95, 212.265, 271.913)), (' A 805  ILE HG22', ' A 818  ILE HD12', -0.437, (215.739, 182.572, 249.085)), (' Y  91  THR HG23', ' Y 122  THR  HA ', -0.435, (249.699, 202.851, 145.524)), (' A 500  THR  OG1', ' B  61  ASP  OD1', -0.435, (194.704, 203.862, 144.931)), (' E 909  ILE HG12', ' E1047  TYR  HB3', -0.435, (210.049, 210.468, 258.554)), (' H  40  ALA  HB3', ' H  43  LYS  HB2', -0.435, (235.921, 155.281, 131.915)), (' E 310  LYS  HG2', ' E 664  ILE HD11', -0.435, (230.046, 212.17, 229.522)), (' A 187  LYS  HG2', ' A 211  ASN HD21', -0.434, (213.18, 138.953, 206.811)), (' C 319  ARG  HA ', ' C 592  PHE  HA ', -0.433, (193.338, 231.74, 205.819)), (' C 747  THR  O  ', ' C 751  ASN  HB2', -0.433, (194.994, 184.063, 193.745)), (' E 500  THR HG21', ' H  64  LYS  HD2', -0.433, (248.661, 166.616, 140.444)), (' A 424  LYS  NZ ', ' A 425  LEU  O  ', -0.433, (190.424, 210.576, 177.832)), (' A 329  PHE  O  ', ' A 580  GLN  NE2', -0.433, (165.556, 184.914, 184.063)), (' A 707  TYR  HE1', ' C 897  PRO  HA ', -0.432, (178.673, 192.33, 262.826)), (' A 467  ASP  N  ', ' A 467  ASP  OD1', -0.432, (183.276, 218.594, 168.537)), (' E 328  ARG HH21', ' E 580  GLN  HB2', -0.43, (236.847, 171.798, 195.082)), (' D  66  ARG  NH2', ' D  86  ASP  OD2', -0.429, (221.381, 269.418, 129.38)), (' T   1  NAG  H62', ' T   2  NAG  H61', -0.427, (227.165, 246.856, 209.668)), (' A 382  VAL  H  ', ' C 983  ARG  CZ ', -0.427, (185.043, 194.408, 180.368)), (' W  36  TRP  HB2', ' W  49  ALA  HB3', -0.427, (191.574, 255.828, 155.082)), (' E 355  ARG  HA ', ' E 355  ARG  HD3', -0.427, (221.696, 164.058, 163.893)), (' E 915  VAL  O  ', ' E 919  ASN  ND2', -0.427, (214.471, 219.451, 268.378)), (' E 858  LEU HD13', ' E 959  LEU HD23', -0.427, (204.533, 221.326, 213.788)), (' C 226  LEU  HB3', ' C 227  VAL HG23', -0.426, (156.729, 209.614, 186.785)), (' A 106  PHE  HD2', ' A 235  ILE HG21', -0.426, (203.773, 158.725, 184.518)), (' C 725  GLU  OE1', ' C1064  HIS  NE2', -0.425, (187.368, 205.871, 244.635)), (' C1082  CYS  HB2', ' C1132  ILE HG12', -0.425, (204.276, 226.931, 280.194)), (' C 740  MET  HA ', ' C 744  GLY  HA2', -0.425, (187.22, 187.426, 202.191)), (' A 970  PHE  HA ', ' C 756  TYR  HA ', -0.424, (203.937, 190.444, 199.477)), (' A 676  THR  OG1', ' A 690  GLN  NE2', -0.424, (189.494, 160.577, 235.882)), (' E 376  THR  HB ', ' E 435  ALA  HB3', -0.424, (234.125, 176.196, 157.171)), (' A 902  MET  HB3', ' A 902  MET  HE3', -0.424, (209.36, 189.679, 263.317)), (' C 193  VAL HG23', ' C 223  LEU HD22', -0.424, (160.037, 217.399, 193.278)), (' H  22  CYS  N  ', ' H  78  VAL  O  ', -0.424, (235.097, 174.812, 126.215)), (' C 327  VAL  HA ', ' C 542  ASN  HB3', -0.423, (204.999, 238.616, 188.528)), (' D  47  TRP  HE1', ' D  50  ALA  HB2', -0.422, (213.652, 257.522, 136.523)), (' C 187  LYS  HA ', ' C 187  LYS  HD2', -0.422, (142.35, 223.644, 199.207)), (' A  37  TYR  OH ', ' A  53  ASP  OD2', -0.421, (206.496, 166.74, 198.161)), (' C1015  ALA  HA ', ' C1018  ILE HG22', -0.42, (192.889, 198.266, 226.64)), (' A 743  CYS  HB3', ' A 749  CYS  HB3', -0.42, (219.649, 197.999, 198.592)), (' E  40  ASP  N  ', ' E  40  ASP  OD1', -0.419, (224.56, 227.807, 198.53)), (' A 804  GLN  OE1', ' A 935  GLN  NE2', -0.419, (216.504, 176.943, 250.374)), (' A 806  LEU  HA ', ' A 806  LEU HD23', -0.419, (221.72, 186.828, 251.001)), (' E1029  MET  O  ', ' E1033  VAL  HB ', -0.419, (199.817, 217.406, 246.685)), (' A 722  VAL HG22', ' A1065  VAL HG22', -0.418, (208.697, 185.171, 253.86)), (' C 969  ASN  HB2', ' C 972  ALA  HB3', -0.417, (189.506, 200.885, 192.528)), (' E 430  THR  OG1', ' E 515  PHE  O  ', -0.417, (219.433, 176.273, 168.635)), (' E 102  ARG  HA ', ' E 102  ARG  HD3', -0.417, (248.605, 239.519, 185.832)), (' B   5  VAL HG12', ' C 428  ASP  HB3', -0.416, (208.123, 227.398, 156.303)), (' C 458  LYS  HE3', ' C 473  TYR  HA ', -0.414, (226.954, 235.992, 134.139)), (' A1018  ILE  HA ', ' A1018  ILE HD13', -0.414, (207.401, 195.061, 231.177)), (' C 627  ASP  N  ', ' C 627  ASP  OD1', -0.413, (180.831, 237.809, 200.087)), (' A 979  ASP  HB3', ' A 983  ARG  HE ', -0.413, (216.76, 185.648, 190.245)), (' C 414  GLN  NE2', ' C 415  THR  O  ', -0.412, (207.138, 238.464, 142.898)), (' E1005  GLN  HA ', ' E1008  VAL HG12', -0.412, (200.014, 208.136, 211.179)), (' A  64  TRP  HE1', ' A 264  ALA  HB1', -0.412, (200.271, 143.255, 199.039)), (' C 305  SER  OG ', ' C 306  PHE  N  ', -0.412, (171.721, 214.677, 215.862)), (' C 736  VAL HG12', ' C 858  LEU  HA ', -0.412, (186.15, 190.819, 212.007)), (' A 805  ILE  HB ', ' A1054  GLN HE22', -0.411, (216.997, 185.86, 248.78)), (' D  40  ALA  HB3', ' D  43  LYS  HB2', -0.411, (229.463, 260.315, 131.99)), (' C1129  VAL HG13', ' E 917  TYR  HB3', -0.411, (208.489, 224.066, 271.92)), (' A  92  PHE  HB3', ' A 192  PHE  HB2', -0.411, (207.807, 152.953, 195.051)), (' A 375  SER  N  ', ' A 435  ALA  O  ', -0.411, (190.249, 194.097, 163.763)), (' E 945  LEU HD12', ' E 948  LEU HD12', -0.411, (211.854, 221.399, 233.788)), (' C1100  THR HG21', ' L   1  NAG  H3 ', -0.411, (184.508, 230.137, 282.048)), (' H  20  LEU HD12', ' H  80  LEU HD23', -0.411, (238.926, 168.416, 127.399)), (' C 323  THR  OG1', ' C 537  LYS  NZ ', -0.41, (194.465, 240.419, 196.127)), (' A 231  ILE HD12', ' A 233  ILE  HB ', -0.41, (207.377, 162.974, 181.331)), (' E  34  ARG  NH2', ' E 218  GLN  O  ', -0.409, (243.615, 232.844, 207.574)), (' C 316  SER  OG ', ' C 317  ASN  N  ', -0.409, (187.88, 224.359, 206.686)), (' Y  52  ILE HD12', ' Y  57  HIS  HB2', -0.409, (243.586, 181.762, 164.877)), (' A1086  LYS  HB2', ' A1086  LYS  HE2', -0.408, (183.398, 206.395, 284.339)), (' C 733  LYS  HE2', ' C 771  ALA  HB1', -0.408, (188.789, 187.987, 224.366)), (' E 467  ASP  N  ', ' E 467  ASP  OD1', -0.408, (218.602, 164.184, 153.261)), (' A 900  MET  HB3', ' A 900  MET  HE2', -0.408, (214.867, 196.479, 268.736)), (' E 454  ARG HH12', ' E 457  ARG HH11', -0.408, (215.682, 163.973, 149.077)), (' Y  97  ALA  HB1', ' Y 113  TRP  HB3', -0.408, (234.768, 193.181, 158.431)), (' C 121  ASN  HA ', ' C 126  VAL HG12', -0.407, (148.494, 215.624, 180.608)), (' C 729  VAL HG11', ' C 781  VAL HG11', -0.407, (187.725, 195.961, 237.605)), (' E 415  THR  OG1', ' E 416  GLY  N  ', -0.407, (220.051, 178.062, 147.314)), (' D  87  THR HG23', ' D 108  THR  HA ', -0.407, (227.038, 264.124, 122.736)), (' A 699  LEU  HB3', ' C 873  TYR  HE1', -0.406, (183.836, 183.339, 241.967)), (' A 717  ASN  HB3', ' A1071  GLN  HB2', -0.406, (195.88, 179.481, 265.677)), (' H  56  GLU  OE1', ' H  58  TYR  OH ', -0.405, (245.079, 177.19, 143.924)), (' Y  38  ARG  NH1', ' Y  90  ASP  OD1', -0.405, (250.265, 193.382, 147.342)), (' C 453  TYR  HE2', ' C 455  LEU HD13', -0.405, (219.581, 245.544, 139.355)), (' E 605  SER  OG ', ' E 606  ASN  N  ', -0.405, (239.742, 216.819, 225.02)), (' C 906  PHE  HB3', ' C 911  VAL HG23', -0.404, (187.097, 208.207, 264.756)), (' A1145  LEU HD11', ' C1144  GLU  HB3', -0.403, (191.946, 206.261, 297.486)), (' A1091  ARG  NH1', ' A1118  ASP  O  ', -0.403, (195.382, 202.882, 279.683)), (' D  43  LYS  HB3', ' D  43  LYS  HE3', -0.403, (229.701, 260.831, 134.835)), (' E 204  TYR  HB3', ' E 223  LEU  HB3', -0.402, (235.029, 231.561, 196.738)), (' B  66  ARG  NH2', ' B  86  ASP  OD2', -0.402, (201.742, 214.658, 137.074)), (' A 430  THR  OG1', ' A 515  PHE  O  ', -0.402, (182.266, 200.961, 181.087)), (' E 438  SER  OG ', ' E 507  PRO  O  ', -0.402, (238.625, 169.068, 153.66)), (' A 894  LEU HD13', ' E 715  PRO  HD3', -0.401, (219.442, 205.69, 263.474)), (' A1139  ASP  HB3', ' A1142  GLN  HG2', -0.4, (191.13, 201.342, 292.138)), (' E 355  ARG  HD2', ' E 396  TYR  HB3', -0.4, (220.594, 166.012, 165.917)), (' E 725  GLU  OE1', ' E1064  HIS  NE2', -0.4, (209.015, 213.629, 244.735)), (' E 310  LYS  NZ ', ' E 663  ASP  OD1', -0.4, (230.046, 211.643, 232.66))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
