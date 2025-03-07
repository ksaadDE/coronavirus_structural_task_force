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
data['rama'] = [('A', ' 943 ', 'SER', 0.0, (194.75000000000006, 184.937, 193.67399999999998)), ('B', ' 231 ', 'ILE', 0.02443467409128853, (165.966, 128.88400000000004, 138.582)), ('B', ' 525 ', 'CYS', 0.00029934180995516555, (142.793, 165.653, 136.097)), ('B', ' 624 ', 'ILE', 0.04239697661771033, (136.50799999999995, 142.163, 165.901)), ('C', '  16 ', 'VAL', 0.001681280119316371, (126.39600000000003, 213.137, 124.298)), ('C', ' 210 ', 'ILE', 0.0033644541436714274, (119.767, 197.83, 158.255)), ('C', ' 834 ', 'ILE', 0.054657563838448414, (143.89999999999995, 160.34000000000006, 180.293)), ('C', ' 844 ', 'ILE', 0.00256301, (130.05999999999995, 168.459, 168.033)), ('C', ' 944 ', 'ALA', 0.031345068690616755, (149.95499999999996, 185.224, 194.695))]
data['omega'] = [('C', ' 333 ', 'THR', None, (192.392, 203.126, 133.09))]
data['rota'] = [('C', '  81 ', 'ASN', 0.14987366935387764, (132.87599999999995, 211.685, 136.997))]
data['cbeta'] = []
data['probe'] = [(' B 391  CYS  HA ', ' B 525  CYS  HB3', -0.978, (143.886, 165.883, 137.872)), (' C 226  LEU HD23', ' C 227  VAL HG13', -0.828, (130.595, 187.307, 140.835)), (' C 336  CYS  HB3', ' C 358  ILE HD11', -0.826, (194.935, 197.336, 123.333)), (' B 433  VAL HG12', ' B 512  VAL HG12', -0.81, (159.466, 173.832, 128.395)), (' B 350  VAL HG21', ' B 418  ILE HD11', -0.738, (163.516, 182.651, 121.762)), (' C  15  CYS  O  ', ' C  17  ASN  N  ', -0.728, (128.549, 213.55, 124.282)), (' A 142  ASP  HB2', ' A 156  GLU  HB2', -0.728, (231.363, 187.111, 129.077)), (' B 724  THR HG23', ' B 934  ILE HD11', -0.728, (173.565, 150.014, 208.381)), (' C 244  LEU HD11', ' C 258  TRP  HB2', -0.727, (119.562, 212.761, 133.796)), (' C 363  ALA  HB2', ' C 524  VAL  HB ', -0.722, (192.329, 193.556, 126.836)), (' B 206  LYS  HE2', ' B 221  SER  HB3', -0.711, (167.963, 120.931, 165.017)), (' A1017  GLU  OE1', ' B1019  ARG  NH2', -0.71, (178.183, 172.34, 186.805)), (' B 323  THR HG23', ' B 324  GLU  HG3', -0.704, (137.224, 147.894, 155.065)), (' C 490  PHE  HB3', ' C 493  ARG HH12', -0.703, (199.659, 187.006, 86.5)), (' A 409  GLN  HG2', ' A 418  ILE  HB ', -0.701, (159.661, 148.255, 126.663)), (' A  18  LEU  HB2', ' A  21  ARG HH21', -0.691, (232.497, 175.044, 133.405)), (' B 170  TYR  HE1', ' B 172  SER  HB2', -0.685, (174.487, 118.275, 144.471)), (' C 208  THR  O  ', ' C 214  ARG  NH1', -0.68, (123.529, 199.574, 155.977)), (' B1126  CYS  HB2', ' B1132  ILE HD13', -0.666, (148.43, 179.677, 241.103)), (' A  34  ARG  HD2', ' A 216  LEU HD13', -0.661, (218.09, 181.384, 156.797)), (' B 246  ARG  HG2', ' B 258  TRP  HB3', -0.656, (153.799, 99.131, 143.011)), (' B 114  THR HG22', ' B 115  GLN  H  ', -0.656, (159.515, 127.361, 133.16)), (' B1002  GLN HE22', ' C 759  PHE  HZ ', -0.655, (170.861, 160.735, 165.529)), (' A 562  PHE  HB2', ' B  41  LYS  HE2', -0.653, (177.178, 128.442, 154.305)), (' B 107  GLY  HA2', ' B 235  ILE HG23', -0.646, (155.88, 127.161, 143.159)), (' C1074  ASN  OD1', ' C1301  NAG  N2 ', -0.646, (164.378, 204.379, 222.558)), (' C 170  TYR  HE2', ' C 172  SER  HB2', -0.641, (127.429, 186.116, 136.873)), (' A 329  PHE  O  ', ' A 580  GLN  NE2', -0.637, (194.613, 133.857, 145.824)), (' A 595  VAL HG22', ' A 596  SER  H  ', -0.635, (198.09, 165.007, 175.684)), (' B 121  ASN  HB2', ' B 126  VAL HG22', -0.634, (169.912, 111.951, 146.756)), (' N   1  NAG  H61', ' N   2  NAG  HN2', -0.63, (145.527, 194.755, 223.17)), (' B 109  THR  O  ', ' B 237  ARG  NH1', -0.628, (149.903, 123.536, 138.146)), (' C 756  TYR  OH ', ' C 994  ASP  OD1', -0.624, (167.131, 160.416, 156.634)), (' C  83  VAL  HB ', ' C 237  ARG  HD2', -0.624, (141.06, 208.09, 134.235)), (' B 115  GLN  NE2', ' B 116  SER  O  ', -0.622, (162.076, 121.559, 135.571)), (' A 126  VAL HG22', ' A 173  GLN  H  ', -0.621, (212.786, 195.734, 135.806)), (' B 940  SER  OG ', ' B 941  THR  N  ', -0.621, (170.348, 141.553, 200.411)), (' B 409  GLN HE21', ' B 416  GLY  HA3', -0.618, (170.977, 182.269, 127.613)), (' C 328  ARG HH12', ' C 533  LEU HD12', -0.618, (186.028, 207.563, 146.933)), (' B 142  ASP  HA ', ' B 244  LEU  HB2', -0.617, (157.364, 103.009, 141.352)), (' C1116  THR HG22', ' C1118  ASP  H  ', -0.615, (169.439, 185.927, 244.975)), (' A 742  ILE  O  ', ' A1000  ARG  NH1', -0.615, (174.94, 183.401, 157.566)), (' B  87  ASN  OD1', ' B  88  ASP  N  ', -0.614, (153.677, 130.103, 150.719)), (' B 189  LEU  HB3', ' B 208  THR  HB ', -0.611, (165.338, 113.675, 163.686)), (' B 519  HIS  ND1', ' B 519  HIS  O  ', -0.61, (142.774, 170.576, 145.322)), (' A 130  VAL HG21', ' A 231  ILE HD12', -0.605, (205.689, 183.801, 131.416)), (' C 409  GLN  HB2', ' C 418  ILE HD12', -0.605, (185.295, 188.007, 100.191)), (' B 246  ARG  NH2', ' B 254  SER  O  ', -0.605, (151.389, 101.591, 137.893)), (' C 375  PHE  HD1', ' C 436  TRP  HB3', -0.605, (184.534, 201.282, 108.813)), (' C 303  LEU HD22', ' C 308  VAL HG12', -0.603, (151.56, 191.056, 174.388)), (' B 187  LYS  HA ', ' B 210  ILE HG22', -0.602, (167.429, 106.78, 165.035)), (' A 328  ARG  NH2', ' A 580  GLN  OE1', -0.601, (197.614, 133.227, 148.611)), (' B 117  LEU HD11', ' B 231  ILE HG21', -0.601, (162.828, 125.815, 138.619)), (' B 520  ALA  HB3', ' B 521  PRO  HD3', -0.6, (142.437, 176.413, 144.401)), (' C 722  VAL HG22', ' C1065  VAL HG22', -0.597, (150.23, 181.473, 212.127)), (' B 742  ILE  O  ', ' B1000  ARG  NH1', -0.595, (182.44, 156.363, 160.73)), (' A  99  ASN  HB3', ' A 179  LEU  HB3', -0.594, (226.794, 193.331, 141.132)), (' A 740  MET  HA ', ' A 744  GLY  HA2', -0.593, (172.07, 189.838, 159.649)), (' A  72  GLY  O  ', ' A  76  THR  OG1', -0.59, (241.677, 181.503, 142.535)), (' B 351  TYR  HE1', ' B 452  LEU  HB2', -0.589, (160.244, 187.117, 115.191)), (' C 277  LEU HD12', ' C 285  ILE HD13', -0.588, (139.403, 187.769, 158.635)), (' B 244  LEU HD23', ' B 246  ARG  HE ', -0.584, (154.241, 101.56, 140.677)), (' B 523  THR HG23', ' B 524  VAL HG13', -0.583, (141.292, 172.057, 135.377)), (' A 277  LEU HD12', ' A 285  ILE HG12', -0.582, (204.108, 186.076, 160.233)), (' C 662  CYS  HB2', ' C 697  MET  HG3', -0.581, (163.109, 200.046, 191.355)), (' B 567  ARG  NH1', ' B 571  ASP  O  ', -0.581, (147.051, 171.144, 156.611)), (' A 229  LEU  HB3', ' A 231  ILE HG12', -0.58, (204.359, 184.975, 135.536)), (' A 314  GLN  OE1', ' A 595  VAL HG21', -0.579, (194.964, 164.996, 174.443)), (' A 349  SER  OG ', ' A 450  ASN  O  ', -0.578, (163.346, 135.603, 117.874)), (' C 142  ASP  OD2', ' C 246  ARG  NH2', -0.576, (119.89, 209.94, 128.834)), (' B 614  GLY  HA2', ' C 834  ILE HG23', -0.573, (144.227, 157.137, 178.553)), (' B 519  HIS  CE1', ' B 544  ASN  HB3', -0.571, (141.034, 167.65, 144.472)), (' A  73  THR  OG1', ' A  74  ASN  N  ', -0.569, (243.41, 182.075, 143.884)), (' C 475  ALA  O  ', ' C 487  ASN  ND2', -0.569, (197.344, 173.445, 82.449)), (' C 362  VAL HG13', ' C 526  GLY  HA2', -0.568, (190.559, 197.477, 130.918)), (' C 445  VAL  HA ', ' C 498  ARG  HG2', -0.567, (193.098, 205.911, 90.027)), (' C 543  PHE  HZ ', ' C 552  LEU HD21', -0.567, (184.299, 203.282, 150.387)), (' B 618  THR HG23', ' B 620  VAL HG13', -0.561, (135.637, 150.715, 172.404)), (' B 277  LEU HD12', ' B 285  ILE HD13', -0.56, (169.388, 131.64, 165.776)), (' A 379  CYS  HA ', ' A 432  CYS  HA ', -0.559, (174.886, 149.458, 134.498)), (' C  68  ILE HG12', ' C  72  GLY  H  ', -0.559, (122.084, 217.776, 145.01)), (' B 328  ARG HH21', ' B 580  GLN  HB2', -0.558, (130.21, 162.12, 144.345)), (' A 986  PRO  HG2', ' B 413  GLY  HA3', -0.558, (167.454, 179.401, 137.964)), (' B 902  MET  HE1', ' B1049  LEU HD13', -0.557, (175.246, 157.92, 222.067)), (' A1309  NAG  H3 ', ' A1309  NAG  H83', -0.556, (199.512, 168.267, 131.179)), (' B 140  PHE  HB2', ' B 244  LEU HD11', -0.552, (154.646, 105.705, 141.927)), (' A 284  THR HG22', ' C 560  LEU HD11', -0.55, (204.844, 195.177, 157.761)), (' A 128  ILE HG21', ' A 229  LEU HD21', -0.546, (208.238, 187.066, 134.709)), (' C 330  PRO  HA ', ' C 579  PRO  HB2', -0.545, (191.705, 201.474, 141.863)), (' B 343  ASN  OD1', ' B1306  NAG  N2 ', -0.545, (147.965, 164.94, 117.154)), (' C 454  ARG HH11', ' C 492  LEU HD21', -0.545, (200.494, 184.681, 95.198)), (' B 645  THR  OG1', ' B 648  GLY  O  ', -0.544, (142.567, 152.014, 184.112)), (' A 773  GLU  OE2', ' A1019  ARG  NH1', -0.543, (166.738, 179.782, 186.426)), (' B 379  CYS  HA ', ' B 432  CYS  HB3', -0.543, (158.804, 168.648, 133.5)), (' C  16  VAL HG11', ' C 140  PHE  HE1', -0.542, (126.102, 211.265, 127.907)), (' C 246  ARG  NH1', ' C 254  SER  O  ', -0.54, (120.045, 213.412, 129.093)), (' A 345  THR  O  ', ' A 509  ARG  NH2', -0.539, (173.14, 138.475, 115.118)), (' B 115  GLN  NE2', ' B 131  CYS  O  ', -0.539, (162.412, 121.801, 134.212)), (' B  91  TYR  OH ', ' B 191  GLU  OE1', -0.539, (161.601, 120.598, 162.507)), (' B 327  VAL HG12', ' B 542  ASN  HB3', -0.538, (141.119, 157.903, 145.59)), (' A 642  VAL HG12', ' A 651  ILE HG12', -0.538, (209.117, 156.917, 178.221)), (' A 374  PHE  CE2', ' A 377  PHE  HB2', -0.535, (178.641, 151.801, 126.957)), (' C 418  ILE  HA ', ' C 422  ASN  HB2', -0.533, (190.098, 185.474, 99.932)), (' C 804  GLN  OE1', ' R   1  NAG  O6 ', -0.533, (135.857, 179.875, 209.818)), (' C 811  LYS  HG2', ' C 812  PRO  HD2', -0.529, (131.821, 169.51, 200.014)), (' C 906  PHE  HD2', ' C 916  LEU  HB2', -0.528, (154.061, 181.511, 226.404)), (' C 299  THR HG22', ' C 308  VAL HG11', -0.526, (151.487, 193.459, 173.017)), (' B 132  GLU  HB2', ' B 165  ASN  HB2', -0.526, (162.593, 122.629, 127.873)), (' C 853  GLN  HG2', ' C 963  VAL HG21', -0.524, (149.521, 169.981, 170.255)), (' A 659  SER  HB3', ' A 698  SER  HB3', -0.524, (203.319, 162.147, 200.653)), (' B 524  VAL HG23', ' B 525  CYS  H  ', -0.523, (142.891, 167.83, 135.833)), (' A 318  PHE  HA ', ' A 632  THR HG21', -0.523, (200.199, 159.933, 168.038)), (' A  56  LEU HD12', ' A  57  PRO  HD2', -0.523, (211.735, 174.323, 154.777)), (' A 770  ILE  O  ', ' A 774  GLN  HG2', -0.522, (170.017, 186.022, 184.161)), (' C 410  ILE HD13', ' C 418  ILE HG21', -0.52, (187.106, 188.324, 103.005)), (' B 159  VAL HG23', ' B 160  TYR  HD1', -0.519, (159.811, 112.535, 134.671)), (' C 657  ASN  OD1', ' C1303  NAG  N2 ', -0.518, (163.044, 217.849, 190.245)), (' B 324  GLU  HB2', ' B 539  VAL HG23', -0.518, (137.363, 150.933, 153.051)), (' C 906  PHE  CD2', ' C 916  LEU  HB2', -0.518, (153.915, 181.811, 225.727)), (' B 379  CYS  HA ', ' B 432  CYS  CB ', -0.517, (159.476, 168.485, 133.272)), (' B 763  LEU HD22', ' B1008  VAL HG21', -0.517, (180.909, 166.107, 172.874)), (' C 142  ASP  N  ', ' C 142  ASP  OD1', -0.516, (121.24, 206.131, 129.779)), (' C 142  ASP  HB3', ' C 244  LEU  HB3', -0.515, (121.579, 208.577, 132.314)), (' C 246  ARG  HG3', ' C 258  TRP  HB3', -0.514, (117.931, 213.688, 131.962)), (' B 906  PHE  CD2', ' B 916  LEU  HB2', -0.514, (174.078, 158.544, 228.357)), (' C1130  ILE HG22', ' M   1  NAG  H81', -0.512, (183.894, 201.584, 229.987)), (' C  27  ALA  HB3', ' C  64  TRP  HB3', -0.511, (135.575, 213.696, 149.663)), (' B 985  ASP  N  ', ' B 985  ASP  OD1', -0.51, (181.144, 157.37, 141.876)), (' B 368  LEU HD21', ' B 434  ILE HD13', -0.51, (154.151, 166.292, 125.606)), (' A 819  GLU  OE1', ' A1055  SER  OG ', -0.51, (181.066, 196.154, 197.436)), (' A 398  ASP  OD2', ' A 423  TYR  OH ', -0.508, (167.456, 140.515, 132.1)), (' A 429  PHE  HE1', ' A 514  SER  HB2', -0.507, (170.62, 143.021, 136.793)), (' B 393  THR  HA ', ' B 523  THR HG22', -0.506, (142.54, 173.125, 137.773)), (' B 422  ASN HD21', ' B 454  ARG  H  ', -0.506, (163.66, 187.638, 120.548)), (' A 442  ASP  HB3', ' A 509  ARG  HE ', -0.506, (171.591, 141.49, 116.266)), (' B 215  ASP  N  ', ' B 266  TYR  HH ', -0.505, (154.507, 113.752, 164.585)), (' A 736  VAL HG21', ' A1004  LEU HD11', -0.504, (172.134, 183.716, 168.603)), (' C 290  ASP  OD1', ' C 291  CYS  N  ', -0.504, (149.753, 196.057, 161.294)), (' B  72  GLY  HA2', ' B 260  ALA  HB3', -0.502, (149.999, 99.782, 152.99)), (' C 620  VAL HG23', ' C 621  PRO  HD3', -0.5, (164.666, 209.446, 166.121)), (' C  30  ASN  HA ', ' C  61  ASN  HA ', -0.5, (140.591, 207.907, 155.817)), (' A 735  SER  OG ', ' A 859  THR  OG1', -0.5, (171.08, 191.215, 172.482)), (' A 357  ARG  NH2', ' A 394  ASN  OD1', -0.499, (174.465, 133.748, 140.651)), (' A 519  HIS  ND1', ' B  41  LYS  HB2', -0.499, (176.78, 134.066, 154.132)), (' A 327  VAL  O  ', ' A 327  VAL HG12', -0.498, (195.618, 141.285, 146.318)), (' C 387  LEU HD12', ' C 390  LEU HD11', -0.498, (182.35, 191.481, 123.994)), (' C 988  GLU  N  ', ' C 988  GLU  OE1', -0.497, (163.537, 160.284, 142.735)), (' A 341  VAL HG13', ' A 342  PHE  HD1', -0.496, (179.145, 138.726, 125.818)), (' B 569  ILE  O  ', ' C 964  LYS  NZ ', -0.496, (147.877, 175.283, 164.534)), (' C 452  LEU HD13', ' C 492  LEU  HB3', -0.496, (199.719, 188.982, 93.791)), (' B 303  LEU HD22', ' B 308  VAL HG22', -0.495, (162.214, 142.348, 180.46)), (' A 449  TYR  HB3', ' A 494  SER  HB3', -0.495, (158.895, 138.903, 112.752)), (' C1006  THR  O  ', ' C1010  GLN  HG2', -0.494, (164.561, 171.006, 174.449)), (' C 287  ASP  N  ', ' C 287  ASP  OD1', -0.494, (137.585, 190.116, 165.481)), (' C 993  ILE  O  ', ' C 997  ILE HG12', -0.493, (162.02, 161.76, 155.745)), (' B 721  SER  OG ', ' B1066  THR  OG1', -0.492, (168.081, 154.732, 215.879)), (' B 931  ILE  HA ', ' B 934  ILE HG22', -0.491, (175.667, 147.655, 213.512)), (' B 173  GLN  HB2', ' B 174  PRO  HD3', -0.491, (179.377, 114.915, 148.124)), (' C 804  GLN  NE2', ' C 935  GLN  OE1', -0.49, (138.478, 180.674, 207.267)), (' A 937  SER  O  ', ' A 941  THR  OG1', -0.49, (198.108, 189.156, 199.062)), (' A 156  GLU  HB3', ' A 158  ARG  HE ', -0.488, (230.312, 185.95, 126.695)), (' C 718  PHE  HA ', ' C1069  PRO  HA ', -0.487, (156.805, 191.542, 220.426)), (' C 280  ASN  ND2', ' C1306  NAG  H61', -0.487, (129.732, 184.461, 164.791)), (' C 210  ILE HD11', ' C 214  ARG  HG2', -0.486, (122.113, 201.91, 158.421)), (' C 214  ARG HH21', ' C 217  PRO  HG3', -0.486, (126.875, 201.749, 157.297)), (' A 391  CYS  HB3', ' A 525  CYS  HA ', -0.486, (187.087, 140.141, 141.865)), (' B 740  MET  HA ', ' B 744  GLY  HA2', -0.484, (188.979, 156.983, 163.8)), (' B 202  LYS  NZ ', ' B 226  LEU  O  ', -0.484, (172.863, 127.267, 150.578)), (' A 115  GLN  HA ', ' A 132  GLU  HG3', -0.484, (209.079, 177.397, 125.579)), (' C  91  TYR  OH ', ' C 191  GLU  OE2', -0.483, (133.217, 198.598, 153.549)), (' C 715  PRO  HA ', ' C1072  GLU  HA ', -0.482, (160.177, 196.923, 223.723)), (' A 316  SER  OG ', ' A 317  ASN  N  ', -0.481, (197.561, 164.19, 169.298)), (' A 519  HIS  CE1', ' B  41  LYS  H  ', -0.481, (175.057, 134.649, 154.923)), (' A 102  ARG  NH1', ' A 122  ASN  HA ', -0.479, (222.933, 192.084, 134.713)), (' C 726  ILE HG13', ' C1061  VAL HG22', -0.477, (151.317, 177.799, 198.795)), (' B 104  TRP  HD1', ' B 238  PHE  HZ ', -0.477, (158.622, 117.84, 149.206)), (' C  74  ASN  HB2', ' C  78  ARG  HG2', -0.477, (125.7, 221.906, 141.208)), (' B 986  PRO  N  ', ' B 987  PRO  HD2', -0.475, (183.321, 160.718, 142.377)), (' B 112  SER  HB3', ' B 135  PHE  H  ', -0.475, (154.164, 119.973, 131.227)), (' B 127  VAL HG23', ' B 171  VAL HG12', -0.475, (173.235, 113.828, 139.379)), (' A 196  ASN  ND2', ' A 200  TYR  O  ', -0.473, (202.88, 179.97, 139.554)), (' B 524  VAL HG23', ' B 525  CYS  N  ', -0.473, (142.819, 168.29, 135.461)), (' C 843  ASP  N  ', ' C 843  ASP  OD1', -0.473, (132.843, 164.19, 168.392)), (' B 989  ALA  O  ', ' B 993  ILE HG12', -0.472, (181.355, 159.707, 150.701)), (' B 121  ASN  ND2', ' B 176  LEU HD13', -0.472, (167.133, 113.495, 149.182)), (' B 620  VAL  N  ', ' B 621  PRO  HD2', -0.472, (137.398, 147.173, 173.455)), (' B 228  ASP  N  ', ' B 228  ASP  OD1', -0.472, (172.629, 127.096, 146.953)), (' C 645  THR HG23', ' C 670  ILE HD12', -0.472, (168.076, 205.017, 183.066)), (' A 985  ASP  N  ', ' A 985  ASP  OD1', -0.471, (173.85, 177.861, 140.051)), (' C 446  SER  H  ', ' C 498  ARG  HE ', -0.471, (194.266, 205.374, 88.545)), (' C 858  LEU HD13', ' C 959  LEU HD22', -0.471, (152.67, 168.107, 172.985)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.471, (162.114, 178.37, 205.068)), (' B 736  VAL HG23', ' B 858  LEU  HG ', -0.47, (183.929, 158.029, 172.534)), (' B 377  PHE  HD1', ' B 434  ILE HG12', -0.469, (156.839, 166.075, 127.61)), (' C 848  ASP  N  ', ' C 848  ASP  OD1', -0.469, (139.436, 170.216, 171.776)), (' C 736  VAL HG23', ' C 858  LEU HD23', -0.467, (154.29, 163.413, 171.452)), (' C 822  LEU HD22', ' C 945  LEU HD21', -0.466, (147.401, 177.852, 196.866)), (' B  84  LEU  O  ', ' B 238  PHE  N  ', -0.464, (152.056, 122.757, 146.181)), (' A 319  ARG  HG2', ' A 592  PHE  HB2', -0.461, (195.507, 155.988, 167.295)), (' B 815  ARG  HG2', ' B 819  GLU  HB2', -0.461, (186.477, 148.253, 203.737)), (' A 316  SER  H  ', ' A 595  VAL HG23', -0.461, (196.948, 165.293, 173.264)), (' A 121  ASN HD21', ' A 175  PHE  HB2', -0.459, (217.93, 193.326, 141.191)), (' C 331  ASN  OD1', ' C 332  ILE HG12', -0.459, (193.484, 207.263, 136.796)), (' A 368  LEU HD13', ' A 371  LEU HD12', -0.458, (182.817, 144.148, 125.047)), (' B 200  TYR  HB3', ' B 230  PRO  HA ', -0.458, (168.328, 131.984, 142.194)), (' B 572  THR  OG1', ' C 856  LYS  NZ ', -0.457, (148.032, 167.281, 161.896)), (' A 180  GLU  HG2', ' A 181  GLY  H  ', -0.457, (232.464, 199.4, 141.429)), (' C 676  THR  HA ', ' C 690  GLN  HG3', -0.456, (147.139, 208.946, 186.182)), (' A 578  ASP  N  ', ' A 578  ASP  OD1', -0.455, (191.715, 132.779, 155.14)), (' A 102  ARG HH21', ' A 179  LEU HD21', -0.455, (226.869, 192.885, 136.745)), (' B 844  ILE  HB ', ' B 847  ARG  HB2', -0.455, (187.66, 137.462, 175.935)), (' A 118  LEU HD21', ' A 120  VAL HG23', -0.455, (217.562, 185.893, 131.282)), (' A  96  GLU  O  ', ' A 188  ASN  HB3', -0.454, (226.545, 191.017, 150.205)), (' C 328  ARG HH12', ' C 533  LEU  HB2', -0.454, (185.274, 207.923, 146.036)), (' C 770  ILE  O  ', ' C 774  GLN  HG2', -0.453, (158.205, 163.088, 186.587)), (' C 568  ASP  OD1', ' C 572  THR  OG1', -0.453, (186.217, 192.586, 162.595)), (' C 931  ILE  HA ', ' C 934  ILE HG22', -0.453, (144.918, 182.949, 208.917)), (' B 126  VAL HG23', ' B 177  MET  HE1', -0.453, (173.295, 110.879, 148.266)), (' B1072  GLU  HG2', ' C 894  LEU HD22', -0.452, (154.617, 158.059, 224.769)), (' B 170  TYR  CE1', ' B 172  SER  HB2', -0.451, (174.984, 118.422, 144.477)), (' A1116  THR HG22', ' A1118  ASP  H  ', -0.451, (177.584, 174.444, 246.568)), (' B 355  ARG  HA ', ' B 398  ASP  OD2', -0.451, (150.729, 180.373, 126.014)), (' A  43  PHE  HB3', ' C 566  GLY  HA2', -0.45, (194.168, 195.295, 156.763)), (' B 101  ILE  O  ', ' B 102  ARG  HG3', -0.45, (162.761, 110.616, 150.537)), (' A 129  LYS  HB3', ' A 131  CYS  SG ', -0.45, (210.985, 185.423, 127.016)), (' A 132  GLU  O  ', ' A 163  ALA  HA ', -0.45, (213.721, 179.558, 121.947)), (' C 945  LEU HD23', ' C 948  LEU HD12', -0.45, (149.551, 177.401, 194.447)), (' C 419  ALA  HA ', ' C 424  LYS  HA ', -0.449, (189.135, 182.405, 104.204)), (' B 519  HIS  NE2', ' B 544  ASN  HB3', -0.448, (141.44, 167.397, 144.211)), (' C 253  ASP  N  ', ' C 253  ASP  OD1', -0.448, (117.585, 219.877, 127.414)), (' A 108  THR  OG1', ' A 234  ASN  O  ', -0.447, (207.682, 173.137, 133.146)), (' C1129  VAL  HB ', ' C1132  ILE HD11', -0.447, (184.373, 195.533, 236.004)), (' C 401  VAL HG22', ' C 509  ARG  HD2', -0.447, (192.771, 198.588, 102.652)), (' C 277  LEU HD13', ' C 288  ALA  HB2', -0.446, (140.845, 190.333, 160.985)), (' B 112  SER  HB2', ' B 134  GLN  HA ', -0.446, (155.144, 120.751, 129.875)), (' A 595  VAL HG22', ' A 596  SER  N  ', -0.446, (197.883, 164.738, 175.905)), (' B 316  SER  OG ', ' B 317  ASN  N  ', -0.446, (152.778, 149.391, 170.188)), (' B 141  LEU  HB2', ' B 241  LEU HD11', -0.445, (158.782, 109.972, 141.694)), (' A 149  ASN  O  ', ' A 151  SER  N  ', -0.445, (235.012, 199.462, 133.588)), (' C 719  THR  N  ', ' C1068  VAL  O  ', -0.445, (154.815, 190.647, 218.49)), (' C 426  PRO  HG2', ' C 429  PHE  HB2', -0.444, (187.423, 181.445, 113.174)), (' B 617  CYS  O  ', ' B 620  VAL HG22', -0.444, (137.085, 149.24, 174.325)), (' B 139  PRO  HB3', ' B 159  VAL  HA ', -0.444, (154.977, 112.441, 137.52)), (' B 976  VAL HG12', ' B 979  ASP  H  ', -0.444, (183.016, 150.223, 153.311)), (' A 185  ASN  HB3', ' A 212  ILE HG22', -0.443, (228.571, 195.985, 157.346)), (' C  64  TRP  HE1', ' C 264  ALA  HB1', -0.443, (129.792, 210.737, 149.144)), (' A 313  TYR  O  ', ' A 596  SER  HA ', -0.443, (198.394, 166.806, 177.616)), (' B 844  ILE  HA ', ' B 847  ARG HH11', -0.442, (188.567, 134.886, 174.816)), (' C 462  LYS  HA ', ' C 462  LYS  HD3', -0.442, (192.64, 174.549, 105.946)), (' A 770  ILE HG23', ' A 774  GLN HE21', -0.442, (171.021, 183.704, 184.113)), (' A 445  VAL HG12', ' A 499  PRO  HB3', -0.442, (169.508, 146.148, 103.781)), (' C1105  THR HG22', ' C1112  PRO  HA ', -0.441, (163.493, 193.179, 235.242)), (' C  99  ASN  HB2', ' C 177  MET  HE3', -0.441, (118.426, 200.248, 143.216)), (' C 907  ASN  HA ', ' C 911  VAL  O  ', -0.44, (160.565, 180.39, 227.377)), (' C 342  PHE  CE2', ' C 371  LEU HD11', -0.44, (189.054, 202.342, 112.486)), (' C 586  ASP  OD1', ' C 587  ILE  N  ', -0.44, (186.108, 201.35, 158.703)), (' B 725  GLU  OE1', ' B1064  HIS  NE2', -0.439, (172.426, 159.448, 207.54)), (' C 642  VAL HG22', ' C 651  ILE HG12', -0.439, (162.614, 210.206, 172.545)), (' A 391  CYS  HB2', ' A 525  CYS  H  ', -0.439, (185.918, 138.956, 141.462)), (' C 149  ASN  N  ', ' C 149  ASN  OD1', -0.438, (109.838, 206.356, 131.238)), (' B 592  PHE  CD1', ' C 740  MET  HE1', -0.438, (145.741, 158.092, 167.042)), (' C 117  LEU  O  ', ' C 118  LEU HD23', -0.438, (134.311, 198.06, 130.744)), (' B  39  PRO  HG2', ' B  51  THR HG21', -0.438, (168.92, 135.983, 162.464)), (' A 412  PRO  HB3', ' A 427  ASP  HA ', -0.437, (165.154, 150.634, 138.546)), (' B 190  ARG  HB3', ' B 192  PHE  HE1', -0.437, (164.949, 115.43, 155.513)), (' C1050  MET  HE2', ' C1052  PHE  CE1', -0.436, (150.057, 174.349, 214.529)), (' C 333  THR  HA ', ' C 362  VAL HG11', -0.436, (192.04, 201.148, 131.338)), (' A 538  CYS  HB2', ' A 590  CYS  HB3', -0.436, (199.624, 147.536, 164.354)), (' B 246  ARG  NH1', ' B 253  ASP  O  ', -0.435, (150.22, 98.867, 139.003)), (' B  24  LEU HD23', ' B  78  ARG  HD2', -0.434, (143.742, 108.43, 153.363)), (' B1103  PHE  HZ ', ' K   1  NAG  H62', -0.434, (155.614, 159.564, 245.16)), (' A 201  PHE  HB3', ' A 229  LEU  HB2', -0.434, (205.378, 184.333, 138.0)), (' A 662  CYS  HB2', ' A 671  CYS  HB3', -0.434, (202.021, 165.968, 192.134)), (' A 931  ILE  HA ', ' A 934  ILE HG22', -0.433, (191.616, 191.709, 208.251)), (' C 127  VAL HG12', ' C 171  VAL HG22', -0.433, (124.733, 188.667, 131.447)), (' C1086  LYS  HB2', ' C1086  LYS  HE3', -0.433, (181.941, 190.794, 245.965)), (' B 357  ARG HH12', ' C 230  PRO  HB2', -0.432, (141.317, 182.152, 133.549)), (' C1104  VAL HG23', ' C1115  ILE HD13', -0.432, (169.393, 192.529, 238.904)), (' A 374  PHE  CZ ', ' A 377  PHE  HB2', -0.432, (178.975, 151.442, 127.178)), (' A  96  GLU  OE1', ' A  98  SER  N  ', -0.431, (228.641, 191.083, 146.19)), (' C 375  PHE  CE1', ' C 434  ILE HG23', -0.431, (185.282, 198.774, 110.968)), (' C 361  CYS  O  ', ' C 524  VAL HG12', -0.43, (194.722, 194.218, 128.864)), (' B 452  LEU HD13', ' B 492  LEU HD23', -0.429, (160.682, 190.133, 113.93)), (' C 742  ILE  O  ', ' C1000  ARG  NH1', -0.428, (155.768, 163.519, 159.926)), (' C 110  LEU HD22', ' C 237  ARG HH22', -0.427, (139.458, 205.164, 130.915)), (' B 121  ASN HD21', ' B 176  LEU HD13', -0.427, (167.027, 113.792, 149.697)), (' C 105  ILE HG21', ' C 239  GLN HE21', -0.427, (133.866, 204.201, 132.202)), (' C 717  ASN  HB3', ' C 718  PHE  H  ', -0.427, (153.144, 192.761, 222.044)), (' B 126  VAL HG21', ' B 175  PHE  HB3', -0.427, (172.245, 113.936, 148.728)), (' C 128  ILE  HB ', ' C 170  TYR  HB3', -0.426, (130.655, 188.264, 133.267)), (' A  71  SER  HA ', ' A 261  GLY  H  ', -0.426, (236.37, 184.956, 142.777)), (' C 101  ILE HD11', ' C 240  THR  CG2', -0.425, (129.933, 204.597, 139.703)), (' B 245  HIS  H  ', ' B 258  TRP  HB2', -0.424, (155.323, 100.05, 145.17)), (' A 125  ASN  HB3', ' A 172  SER  HB3', -0.424, (215.271, 196.559, 132.738)), (' B 474  GLN  HB3', ' B 479  PRO  HA ', -0.424, (168.746, 206.65, 119.681)), (' B 629  LEU  HG ', ' B 631  PRO  HD2', -0.424, (145.985, 145.739, 167.894)), (' C 385  THR  O  ', ' C 386  LYS  HG3', -0.424, (177.704, 193.593, 126.346)), (' C 426  PRO  HB3', ' C 463  PRO  HB3', -0.423, (190.219, 178.425, 111.272)), (' A 801  ASN  OD1', ' E   1  NAG  N2 ', -0.423, (191.042, 202.461, 214.02)), (' C 909  ILE  O  ', ' C 909  ILE HG13', -0.423, (161.229, 182.529, 222.765)), (' C 841  LEU  H  ', ' C 841  LEU HD23', -0.422, (134.181, 162.019, 169.783)), (' C1125  ASN  OD1', ' C1126  CYS  N  ', -0.421, (187.423, 193.915, 241.875)), (' A 523  THR HG23', ' A 524  VAL HG23', -0.421, (182.456, 136.293, 139.937)), (' C 375  PHE  CD1', ' C 436  TRP  HB3', -0.421, (184.905, 201.032, 109.242)), (' A 231  ILE HG22', ' A 233  ILE HG23', -0.421, (203.986, 180.022, 132.14)), (' A 498  ARG  HB2', ' A 501  TYR  HB2', -0.42, (163.976, 150.176, 107.478)), (' B 867  ASP  N  ', ' B 867  ASP  OD1', -0.42, (192.046, 152.781, 196.142)), (' B 389  ASP  OD1', ' B 390  LEU  N  ', -0.42, (148.385, 161.576, 139.926)), (' A  91  TYR  OH ', ' A 191  GLU  OE1', -0.419, (216.054, 183.932, 154.864)), (' C1045  LYS  HB3', ' C1045  LYS  HE3', -0.419, (160.563, 189.044, 209.641)), (' B1082  CYS  HB2', ' B1126  CYS  HB2', -0.418, (148.405, 179.053, 242.441)), (' B 555  SER  HB2', ' B 557  LYS  HG2', -0.418, (131.239, 169.165, 160.041)), (' B 906  PHE  HD2', ' B 916  LEU  HB2', -0.418, (174.134, 158.827, 229.051)), (' A 182  LYS  HA ', ' A 182  LYS  HD2', -0.417, (231.391, 199.051, 146.948)), (' A  14  GLN  HB2', ' A 158  ARG HH12', -0.417, (229.965, 182.308, 123.453)), (' C1082  CYS  HB2', ' C1126  CYS  HB2', -0.417, (183.533, 196.426, 240.45)), (' B 328  ARG  HD2', ' B 533  LEU HD12', -0.417, (132.666, 159.829, 149.188)), (' B 985  ASP  HB2', ' B 987  PRO  HD2', -0.416, (182.615, 160.543, 141.179)), (' A 620  VAL  N  ', ' A 621  PRO  HD2', -0.416, (206.997, 152.21, 172.821)), (' B 244  LEU  HA ', ' B 258  TRP  CE3', -0.416, (155.217, 102.463, 145.866)), (' B 906  PHE  HE1', ' B1049  LEU HD11', -0.415, (172.506, 158.484, 223.388)), (' A 203  ILE  HB ', ' A 227  VAL HG22', -0.415, (208.438, 187.916, 142.414)), (' B 187  LYS  HA ', ' B 187  LYS  HD3', -0.415, (168.242, 105.916, 164.387)), (' B 168  PHE  CZ ', ' B 170  TYR  HB2', -0.415, (173.138, 121.754, 139.258)), (' C 906  PHE  HE1', ' C1049  LEU HD11', -0.415, (155.088, 182.188, 220.229)), (' B 454  ARG HH12', ' B 467  ASP  HB3', -0.415, (159.055, 191.939, 125.286)), (' C  71  SER  HA ', ' C  75  GLY  HA2', -0.415, (121.641, 218.519, 140.854)), (' A 942  ALA  O  ', ' A 943  SER  HB3', -0.415, (196.822, 185.083, 192.883)), (' B 206  LYS  HD3', ' B 222  ALA  O  ', -0.412, (170.424, 122.216, 162.961)), (' C 107  GLY  H  ', ' C 235  ILE HG23', -0.412, (141.888, 198.841, 133.893)), (' B 603  ASN  OD1', ' B1309  NAG  N2 ', -0.411, (161.856, 134.47, 191.575)), (' A  99  ASN HD22', ' A 178  ASP  HA ', -0.411, (224.062, 194.855, 141.588)), (' B 770  ILE  O  ', ' B 774  GLN  HG2', -0.411, (184.113, 165.145, 186.239)), (' B 134  GLN  N  ', ' B 162  SER  OG ', -0.411, (157.781, 117.665, 128.984)), (' C 280  ASN  OD1', ' C 284  THR HG22', -0.411, (131.951, 183.979, 162.967)), (' C 578  ASP  N  ', ' C 578  ASP  OD1', -0.411, (191.933, 204.301, 149.063)), (' B 853  GLN  HG2', ' B 963  VAL HG21', -0.41, (181.306, 150.776, 173.254)), (' C 928  ASN  O  ', ' C 931  ILE HG22', -0.41, (142.32, 183.491, 213.017)), (' B 140  PHE  CE2', ' B 158  ARG  HG3', -0.41, (153.933, 105.24, 137.364)), (' B 519  HIS  CE1', ' B 522  ALA  HB2', -0.409, (141.429, 169.177, 143.774)), (' B 461  LEU  H  ', ' B 461  LEU HD23', -0.409, (163.609, 188.917, 130.05)), (' C 971  GLY  O  ', ' C 995  ARG  NH1', -0.409, (165.004, 170.95, 150.576)), (' C 456  PHE  HB2', ' C 491  PRO  HB3', -0.409, (197.085, 181.81, 90.798)), (' C 560  LEU  H  ', ' C 563  GLN  HG3', -0.409, (200.107, 197.715, 155.41)), (' C1079  PRO  HD2', ' C1131  GLY  O  ', -0.408, (179.613, 198.74, 233.593)), (' A 350  VAL HG11', ' A 422  ASN HD21', -0.408, (160.496, 142.407, 123.191)), (' B 403  ARG  HD2', ' B 505  HIS  CE1', -0.407, (170.91, 178.957, 114.615)), (' A 242  LEU  HA ', ' A 242  LEU HD12', -0.407, (226.258, 184.407, 138.983)), (' B 630  THR  HB ', ' B 631  PRO  HD3', -0.407, (147.933, 147.015, 167.38)), (' B 546  LEU  O  ', ' B 546  LEU HD23', -0.407, (143.246, 163.2, 151.48)), (' C 806  LEU  HA ', ' C 806  LEU HD23', -0.407, (142.268, 170.187, 210.591)), (' C 805  ILE HD12', ' C 878  LEU HD11', -0.406, (146.229, 173.014, 210.061)), (' A 632  THR  OG1', ' A 633  TRP  N  ', -0.406, (204.191, 162.757, 168.446)), (' A 907  ASN  OD1', ' A 913  GLN  HG2', -0.406, (177.828, 185.81, 229.302)), (' C 770  ILE  HA ', ' C 773  GLU  HG2', -0.405, (161.578, 162.427, 186.208)), (' A 206  LYS  HB3', ' A 223  LEU HD23', -0.405, (212.9, 189.073, 153.096)), (' C 396  TYR  HB2', ' C 514  SER  HB3', -0.405, (193.205, 187.416, 116.207)), (' A 855  PHE  CE2', ' C 589  PRO  HD2', -0.404, (179.953, 198.286, 162.001)), (' B1039  ARG  H  ', ' B1039  ARG  HG2', -0.404, (170.51, 169.635, 213.007)), (' C 115  GLN  NE2', ' C 132  GLU  OE2', -0.404, (141.05, 193.326, 122.841)), (' A 456  PHE  HB3', ' A 473  TYR  CD2', -0.404, (146.31, 139.986, 126.068)), (' B 442  ASP  OD1', ' B 451  TYR  OH ', -0.403, (158.034, 176.16, 110.909)), (' C 378  LYS  HB3', ' C 378  LYS  HE2', -0.403, (178.489, 190.627, 109.592)), (' B 178  ASP  N  ', ' B 178  ASP  OD1', -0.403, (171.641, 107.421, 155.332)), (' B 699  LEU  HB3', ' C 873  TYR  HE1', -0.403, (148.867, 157.444, 203.662)), (' A 970  PHE  HD2', ' A 999  GLY  HA3', -0.402, (176.139, 174.229, 159.617)), (' B  90  VAL HG12', ' B  92  PHE  H  ', -0.402, (158.694, 122.036, 153.866)), (' C 409  GLN  NE2', ' C 415  THR  O  ', -0.402, (182.07, 184.434, 99.056)), (' A 214A GLU  OE2', ' A 214C GLU  HB3', -0.402, (229.355, 184.077, 162.542)), (' C 363  ALA  O  ', ' C 526  GLY  HA3', -0.401, (189.46, 197.32, 128.521)), (' B 844  ILE HG22', ' B 847  ARG HH11', -0.401, (187.825, 134.322, 175.541)), (' C 131  CYS  HB3', ' C 165  ASN  O  ', -0.401, (134.739, 192.462, 121.999)), (' A 426  PRO  HD3', ' A 463  PRO  HB3', -0.401, (162.4, 142.724, 138.814)), (' A 578  ASP  OD2', ' A 581  THR  HB ', -0.401, (195.415, 131.242, 154.638)), (' A 553  THR  OG1', ' A 554  GLU  N  ', -0.4, (197.845, 136.227, 165.582)), (' C  74  ASN  HB3', ' C  77  LYS  HB2', -0.4, (125.364, 223.034, 139.161)), (' B 475  ALA  HB1', ' B 489  TYR  CZ ', -0.4, (172.869, 198.398, 119.647)), (' A 457  ARG  NH1', ' A 459  SER  O  ', -0.4, (151.119, 139.188, 134.058))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
