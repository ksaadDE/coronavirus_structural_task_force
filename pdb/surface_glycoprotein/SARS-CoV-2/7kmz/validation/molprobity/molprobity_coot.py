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
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' A 540  ASN  OD1', ' A 549  THR  OG1', -0.776, (216.049, 195.364, 219.409)), (' B 323  THR  OG1', ' B 324  GLU  OE1', -0.774, (200.514, 249.862, 216.422)), (' B1129  VAL  HB ', ' B1132  ILE HD11', -0.772, (209.175, 244.568, 298.347)), (' A 676  THR  O  ', ' A 690  GLN  N  ', -0.733, (236.882, 181.835, 257.023)), (' B 676  THR  O  ', ' B 690  GLN  N  ', -0.726, (177.232, 231.945, 247.729)), (' B 535  LYS  NZ ', ' B 554  GLU  OE2', -0.721, (205.378, 264.151, 223.35)), (' B 811  LYS  NZ ', ' B 815  ARG  O  ', -0.71, (200.519, 196.735, 262.811)), (' A 206  LYS  NZ ', ' A 208  THR  OG1', -0.707, (262.833, 189.055, 229.582)), (' E 388  GLN  O  ', ' E 393  ARG  NH1', -0.706, (217.244, 189.071, 153.701)), (' C 493  GLN  NE2', ' C 494  SER  O  ', -0.702, (239.043, 203.219, 178.982)), (' B 675  GLN  OE1', ' B 690  GLN  N  ', -0.701, (178.221, 233.732, 246.927)), (' C  34  ARG  NH1', ' C 191  GLU  OE2', -0.701, (242.174, 271.062, 228.814)), (' A 929  SER  OG ', ' A 933  LYS  NZ ', -0.694, (240.631, 202.962, 281.277)), (' C 619  GLU  N  ', ' C 619  GLU  OE2', -0.686, (261.515, 237.435, 240.285)), (' D 388  GLN  NE2', ' D 559  ARG  O  ', -0.684, (218.7, 246.823, 151.926)), (' A1129  VAL  HB ', ' A1132  ILE HD11', -0.677, (197.435, 208.429, 296.421)), (' C 299  THR HG22', ' C 597  VAL HG21', -0.672, (242.686, 246.571, 243.407)), (' C 644  GLN  NE2', ' C 648  GLY  O  ', -0.671, (255.723, 235.344, 249.27)), (' D 185  VAL HG13', ' D 186  LEU HD12', -0.669, (228.833, 265.466, 117.921)), (' C 729  VAL HG22', ' C1059  GLY  HA2', -0.663, (213.891, 237.57, 256.594)), (' A 675  GLN  OE1', ' A 690  GLN  N  ', -0.662, (235.196, 181.07, 256.509)), (' D  27  THR  O  ', ' D  31  LYS  NZ ', -0.656, (238.412, 256.489, 154.541)), (' C 357  ARG  NH2', ' C 358  ILE  O  ', -0.654, (258.868, 209.66, 205.217)), (' D 159  ASN  OD1', ' D 160  GLU  N  ', -0.654, (190.119, 270.989, 112.873)), (' E 501  ALA  O  ', ' E 507  SER  OG ', -0.65, (216.219, 170.883, 124.386)), (' E  67  ASP  OD1', ' E  68  LYS  N  ', -0.65, (198.374, 183.956, 139.684)), (' C 134  GLN  N  ', ' C 161  SER  OG ', -0.647, (250.584, 269.829, 196.479)), (' C 866  THR HG22', ' C 869  MET  HE3', -0.645, (200.519, 243.51, 252.998)), (' A 478  THR  OG1', ' A 487  ASN  ND2', -0.639, (202.908, 212.114, 144.991)), (' B 212  LEU HD23', ' B 217  PRO  HA ', -0.634, (171.835, 216.293, 221.31)), (' B 414  GLN  NE2', ' B 415  THR  O  ', -0.63, (227.697, 248.225, 168.338)), (' A 729  VAL HG22', ' A1059  GLY  HA2', -0.629, (237.237, 221.537, 260.538)), (' C 371  SER  HG ', ' C 373  SER  HG ', -0.622, (253.831, 224.338, 190.328)), (' D 471  ASP  O  ', ' D 475  LYS  NZ ', -0.62, (216.412, 259.467, 104.562)), (' C1118  ASP  OD2', ' C1119  ASN  N  ', -0.618, (219.221, 226.204, 304.94)), (' C 736  VAL  O  ', ' C 764  ASN  ND2', -0.617, (210.189, 230.903, 233.167)), (' A 231  ILE  H  ', ' A 231  ILE HD12', -0.614, (257.404, 197.263, 208.158)), (' D 388  GLN  N  ', ' D 388  GLN  OE1', -0.612, (220.433, 249.677, 153.674)), (' A 405  ASP  N  ', ' A 504  GLY  O  ', -0.611, (212.882, 187.645, 164.833)), (' E  37  GLU  OE2', ' E 393  ARG  NH2', -0.609, (213.273, 189.279, 153.397)), (' B1092  GLU  N  ', ' B1092  GLU  OE1', -0.607, (208.374, 227.5, 295.377)), (' D 431  ASP  N  ', ' D 434  THR  OG1', -0.606, (180.081, 242.152, 137.402)), (' A 398  ASP  OD2', ' A 423  TYR  OH ', -0.601, (205.485, 201.479, 176.965)), (' D  19  SER  N  ', ' D  23  GLU  OE2', -0.6, (246.51, 246.805, 155.1)), (' B 394  ASN  OD1', ' B 518  LEU HD13', -0.599, (233.936, 253.339, 193.012)), (' A 394  ASN  OD1', ' A 518  LEU HD13', -0.599, (205.793, 207.653, 188.309)), (' B1090  PRO  O  ', ' C 913  GLN  NE2', -0.596, (210.254, 233.079, 294.637)), (' C 474  GLN  NE2', ' C 478  THR  O  ', -0.596, (227.342, 184.982, 187.952)), (' B1116  THR  OG1', ' B1118  ASP  OD1', -0.595, (205.472, 226.692, 303.388)), (' B 978  ASN  OD1', ' B 979  ASP  N  ', -0.593, (216.712, 204.476, 213.517)), (' C1135  ASN  OD1', ' C1136  THR  N  ', -0.591, (230.926, 226.783, 311.322)), (' E 159  ASN  OD1', ' E 160  GLU  N  ', -0.591, (222.421, 145.107, 120.764)), (' C 328  ARG  NH1', ' C 580  GLN  OE1', -0.59, (270.863, 222.67, 218.732)), (' A 395  VAL  O  ', ' A 395  VAL HG12', -0.589, (203.258, 198.102, 186.351)), (' A1118  ASP  OD1', ' A1119  ASN  N  ', -0.587, (213.032, 216.085, 304.244)), (' D  30  ASP  OD1', ' D  31  LYS  N  ', -0.583, (234.586, 256.046, 155.422)), (' C1050  MET  HE3', ' C1052  PHE  CZ ', -0.583, (212.39, 242.399, 276.308)), (' D 300  GLN  O  ', ' D 306  ARG  NH2', -0.582, (183.167, 262.177, 155.065)), (' C  96  GLU  HG2', ' C 100  ILE HD12', -0.582, (249.297, 282.207, 218.331)), (' C 802  PHE  CZ ', ' C 882  ILE HD11', -0.581, (209.213, 245.093, 277.203)), (' B1135  ASN  OD1', ' B1136  THR  N  ', -0.581, (199.571, 238.929, 305.87)), (' A 117  LEU  CD1', ' A 233  ILE HD11', -0.581, (256.411, 191.55, 204.918)), (' B1091  ARG  NE ', ' B1118  ASP  O  ', -0.58, (210.587, 227.618, 301.432)), (' B 353  TRP  O  ', ' B 466  ARG  NE ', -0.579, (234.692, 264.44, 178.956)), (' D 511  SER  O  ', ' D 514  ARG  NH1', -0.578, (214.466, 255.966, 132.234)), (' C1302  NAG  H3 ', ' C1302  NAG  H83', -0.578, (240.201, 217.709, 311.267)), (' B 724  THR  OG1', ' B 934  ILE HD11', -0.577, (198.796, 213.524, 264.515)), (' D  48  TRP  HE1', ' D 351  LEU HD11', -0.575, (212.298, 266.241, 150.601)), (' B1028  LYS  NZ ', ' B1042  PHE  O  ', -0.571, (210.147, 220.509, 266.235)), (' B 714  ILE HD12', ' B1096  VAL HG11', -0.57, (197.545, 233.161, 290.872)), (' D 103  ASN  OD1', ' D 104  GLY  N  ', -0.57, (234.004, 259.594, 133.096)), (' A 371  SER  OG ', ' A 373  SER  OG ', -0.57, (207.898, 180.808, 182.592)), (' C 141  LEU HD11', ' C 242  LEU  O  ', -0.568, (250.675, 280.558, 212.488)), (' D 511  SER  OG ', ' D 514  ARG  NH2', -0.567, (216.766, 255.916, 133.321)), (' B 557  LYS  NZ ', ' B 586  ASP  OD1', -0.565, (213.669, 258.923, 229.635)), (' C 316  SER  OG ', ' C 317  ASN  N  ', -0.563, (245.699, 239.696, 236.404)), (' C 780  GLU  O  ', ' C 784  GLN  NE2', -0.562, (207.53, 229.857, 262.786)), (' C 115  GLN  HB2', ' C 233  ILE  CD1', -0.562, (243.719, 259.594, 199.743)), (' A1082  CYS  SG ', ' A1132  ILE HG21', -0.56, (198.447, 206.82, 300.017)), (' B 357  ARG  NH1', ' B 393  THR  OG1', -0.559, (230.739, 257.912, 196.019)), (' B 566  GLY  N  ', ' B 575  ALA  O  ', -0.558, (218.721, 257.047, 223.826)), (' C 478  THR  OG1', ' C 487  ASN  ND2', -0.557, (225.689, 185.566, 185.438)), (' D  67  ASP  OD2', ' D  68  LYS  N  ', -0.556, (228.194, 274.506, 143.656)), (' C 365  TYR  HB2', ' C 387  LEU HD22', -0.553, (254.957, 222.71, 202.039)), (' B1082  CYS  SG ', ' B1132  ILE HG21', -0.552, (206.554, 243.927, 301.285)), (' A 724  THR HG23', ' A 934  ILE HD11', -0.551, (237.332, 210.459, 271.309)), (' C1010  GLN  OE1', ' C1014  ARG  NH1', -0.55, (223.571, 233.449, 242.547)), (' C 214  ARG  NE ', ' C 214  ARG  O  ', -0.549, (254.029, 275.863, 230.138)), (' A 176  LEU HD23', ' A 207  HIS  ND1', -0.549, (269.654, 189.515, 224.679)), (' E 299  ASP  OD1', ' E 300  GLN  N  ', -0.548, (227.428, 146.731, 161.965)), (' C 767  LEU HD21', ' C1008  VAL HG22', -0.545, (215.542, 229.857, 236.879)), (' C 979  ASP  OD2', ' C 980  ILE  N  ', -0.542, (220.681, 240.234, 213.188)), (' A  36  VAL HG11', ' A 220  PHE  CE1', -0.542, (254.221, 193.798, 232.951)), (' C 110  LEU  HB3', ' C 135  PHE  HB2', -0.54, (253.54, 266.989, 200.582)), (' C 128  ILE HD13', ' C 170  TYR  HD2', -0.54, (234.634, 270.058, 206.35)), (' A  53  ASP  OD2', ' A 195  LYS  NZ ', -0.538, (248.949, 197.519, 220.898)), (' A 724  THR  CG2', ' A 934  ILE HD11', -0.538, (237.762, 210.711, 271.214)), (' D 111  ASP  OD1', ' D 112  LYS  N  ', -0.537, (235.677, 272.398, 125.361)), (' C 802  PHE  CE2', ' C 882  ILE HD11', -0.534, (208.751, 246.109, 277.522)), (' D 503  LEU HD23', ' D 505  HIS  H  ', -0.533, (210.613, 261.563, 127.13)), (' D 261  CYS  HB2', ' D 488  VAL HG23', -0.531, (197.609, 252.575, 109.47)), (' A  81  ASN  HB2', ' A 239  GLN HE22', -0.53, (258.743, 176.216, 211.364)), (' C 102  ARG  HD3', ' C 121  ASN  O  ', -0.53, (242.605, 279.739, 209.641)), (' A 787  GLN  OE1', ' C 703  ASN  ND2', -0.528, (241.83, 237.446, 280.453)), (' D 488  VAL HG21', ' D 612  PRO  HG2', -0.527, (196.832, 253.909, 107.292)), (' E 183  TYR  OH ', ' E 187  LYS  NZ ', -0.525, (213.255, 180.401, 127.153)), (' D 217  TYR  OH ', ' D 225  ASP  OD2', -0.524, (217.592, 238.685, 130.071)), (' B 108  THR  OG1', ' B 234  ASN  O  ', -0.52, (191.622, 219.071, 194.322)), (' B 967  SER  O  ', ' B 975  SER  OG ', -0.517, (212.199, 213.635, 219.623)), (' E 121  ASN  OD1', ' E 122  THR  N  ', -0.517, (203.88, 172.356, 126.879)), (' B1118  ASP  OD1', ' B1119  ASN  N  ', -0.516, (207.2, 226.782, 303.035)), (' A 611  LEU HD22', ' A 666  ILE HG23', -0.512, (224.014, 193.417, 246.153)), (' D 364  VAL  O  ', ' D 364  VAL HG23', -0.51, (187.345, 265.622, 142.572)), (' C 409  GLN  OE1', ' C 418  ILE  N  ', -0.51, (234.688, 207.76, 192.594)), (' C 389  ASP  N  ', ' C 389  ASP  OD1', -0.509, (256.911, 226.383, 209.987)), (' E 544  ILE  O  ', ' E 547  SER  OG ', -0.508, (239.234, 173.982, 159.65)), (' A 902  MET  HE1', ' A1050  MET  HE2', -0.508, (234.644, 217.954, 283.525)), (' A 369  TYR  OH ', ' A 384  PRO  O  ', -0.507, (214.081, 190.158, 190.944)), (' C 100  ILE HG22', ' C 242  LEU  O  ', -0.507, (251.3, 280.332, 213.742)), (' A 214  ARG  NE ', ' A 214  ARG  O  ', -0.507, (257.835, 172.772, 230.421)), (' E 364  VAL  O  ', ' E 364  VAL HG23', -0.506, (222.615, 151.475, 150.899)), (' A 493  GLN  NE2', ' A 494  SER  O  ', -0.503, (201.878, 191.463, 156.689)), (' B 137  ASN  OD1', ' B 138  ASP  N  ', -0.503, (172.304, 221.732, 187.008)), (' C 532  ASN  OD1', ' C 533  LEU  N  ', -0.502, (270.655, 226.496, 222.582)), (' D 365  THR  OG1', ' D 368  ASP  OD2', -0.501, (192.293, 264.091, 140.585)), (' E 503  LEU HD23', ' E 505  HIS  H  ', -0.5, (220.045, 170.606, 129.764)), (' D  45  LEU HD12', ' D  46  ALA  N  ', -0.499, (217.581, 272.712, 151.995)), (' A 982  SER  CB ', ' C 386  LYS  HZ2', -0.499, (250.2, 224.275, 214.477)), (' D 480  MET  HE2', ' D 484  ILE HD12', -0.498, (209.67, 247.532, 114.225)), (' D 188  ASN  ND2', ' D 464  PHE  O  ', -0.492, (226.959, 255.882, 119.53)), (' C  48  LEU HD12', ' C 276  LEU HD21', -0.492, (233.375, 254.563, 236.961)), (' C 430  THR  OG1', ' C 515  PHE  O  ', -0.491, (247.927, 214.423, 209.754)), (' E 117  ASN  OD1', ' E 118  THR  N  ', -0.491, (201.959, 178.691, 126.955)), (' A 591  SER  HB2', ' A 615  VAL HG23', -0.491, (217.75, 190.311, 233.885)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.491, (221.331, 232.163, 268.247)), (' E 481  LYS  O  ', ' E 486  GLY  N  ', -0.486, (236.898, 164.662, 119.945)), (' A 950  ASP  OD1', ' A 951  VAL  N  ', -0.485, (235.745, 213.264, 253.742)), (' A 478  THR  O  ', ' A 487  ASN  ND2', -0.483, (202.441, 212.588, 146.496)), (' A 659  SER  OG ', ' A 697  MET  O  ', -0.483, (220.104, 189.57, 261.142)), (' D 107  VAL HG21', ' D 193  ALA  HB1', -0.48, (235.38, 260.93, 128.145)), (' D 499  ASP  N  ', ' D 499  ASP  OD1', -0.48, (209.726, 264.303, 114.882)), (' A  81  ASN  HB2', ' A 239  GLN  NE2', -0.48, (259.377, 175.951, 211.24)), (' A 327  VAL  N  ', ' A 531  THR  OG1', -0.479, (210.213, 188.32, 212.138)), (' B1054  GLN  N  ', ' B1061  VAL  O  ', -0.478, (206.363, 208.294, 264.148)), (' C 290  ASP  OD1', ' C 291  CYS  N  ', -0.477, (243.207, 252.059, 233.319)), (' E 115  ARG  NH1', ' E 182  GLU  OE2', -0.477, (205.093, 177.31, 118.226)), (' C 210  ILE HG21', ' C 217  PRO  CG ', -0.476, (244.366, 275.528, 232.594)), (' D 437  ASN  OD1', ' D 438  PHE  N  ', -0.475, (185.52, 246.929, 134.064)), (' B 751  ASN  OD1', ' B 752  LEU  N  ', -0.475, (232.554, 207.311, 218.555)), (' A 765  ARG  O  ', ' A 769  GLY  N  ', -0.474, (233.93, 233.949, 245.162)), (' B 605  SER  OG ', ' B 606  ASN  N  ', -0.473, (182.609, 226.52, 240.384)), (' C 985  ASP  N  ', ' C 985  ASP  OD1', -0.472, (221.334, 232.874, 204.651)), (' D 590  PRO  O  ', ' D 593  THR  OG1', -0.472, (188.804, 235.639, 128.189)), (' E 132  VAL  HB ', ' E 148  LEU HD21', -0.472, (213.467, 152.803, 127.898)), (' E  82  MET  N  ', ' E  82  MET  SD ', -0.471, (209.818, 204.713, 137.617)), (' B1050  MET  HE2', ' B1052  PHE  CE1', -0.469, (205.187, 208.345, 274.556)), (' A 332  ILE  O  ', ' A 332  ILE HG23', -0.468, (199.036, 186.302, 202.118)), (' C 569  ILE  O  ', ' C 572  THR HG22', -0.467, (249.745, 216.933, 231.926)), (' B 312  ILE HD12', ' B 598  ILE HD11', -0.467, (195.485, 233.504, 241.929)), (' C 141  LEU HD21', ' C 242  LEU  C  ', -0.467, (250.639, 278.574, 211.649)), (' C  40  ASP  N  ', ' C  40  ASP  OD1', -0.467, (230.38, 257.137, 222.934)), (' A 324  GLU  N  ', ' A 324  GLU  OE1', -0.466, (217.119, 185.731, 218.447)), (' B 328  ARG  NH2', ' B 581  THR  OG1', -0.463, (208.931, 264.279, 213.77)), (' C 369  TYR  OH ', ' C 387  LEU HD21', -0.461, (252.61, 225.143, 202.416)), (' A 957  GLN  OE1', ' B 765  ARG  NH2', -0.461, (235.49, 212.456, 241.173)), (' B 493  GLN  NE2', ' B 494  SER  O  ', -0.461, (229.061, 266.915, 160.448)), (' D 223  ILE  H  ', ' D 223  ILE HD12', -0.459, (220.488, 243.818, 124.864)), (' C  34  ARG  NE ', ' C 219  GLY  O  ', -0.459, (242.039, 268.994, 232.357)), (' A 805  ILE HG22', ' A 818  ILE HD12', -0.459, (243.295, 214.803, 274.115)), (' B 422  ASN  OD1', ' B 454  ARG  N  ', -0.458, (233.752, 261.411, 167.973)), (' B 622  VAL  O  ', ' B 622  VAL HG23', -0.456, (196.243, 243.819, 224.663)), (' C 395  VAL  O  ', ' C 395  VAL HG12', -0.455, (255.671, 212.698, 202.762)), (' A 137  ASN  OD1', ' A 138  ASP  N  ', -0.455, (260.652, 172.388, 203.096)), (' B 979  ASP  OD2', ' B 980  ILE  N  ', -0.454, (218.258, 207.847, 212.529)), (' D 229  THR HG22', ' D 581  VAL  HB ', -0.453, (209.831, 236.839, 128.202)), (' A 881  THR  O  ', ' A 901  GLN  NE2', -0.453, (235.41, 223.642, 283.482)), (' A 389  ASP  OD1', ' A 390  LEU  N  ', -0.452, (213.169, 195.98, 197.872)), (' C 386  LYS  HZ1', ' C 390  LEU HD22', -0.452, (252.266, 222.108, 212.715)), (' C 697  MET  N  ', ' C 697  MET  SD ', -0.451, (247.541, 237.47, 262.132)), (' C  28  TYR  HB2', ' C1309  NAG  H82', -0.449, (259.27, 265.595, 229.344)), (' A 974  SER  O  ', ' A 980  ILE HD11', -0.448, (242.337, 220.024, 220.425)), (' D 432  ASN  HB2', ' D 703  NAG  O5 ', -0.448, (178.756, 238.358, 131.886)), (' A 332  ILE HG22', ' A1301  NAG  H82', -0.447, (201.135, 185.319, 204.418)), (' B 546  LEU  H  ', ' B 546  LEU HD23', -0.445, (218.019, 253.346, 215.459)), (' B1104  VAL HG23', ' B1115  ILE  CD1', -0.444, (201.163, 232.474, 299.756)), (' A 902  MET  HE1', ' A1050  MET  CE ', -0.444, (234.638, 218.371, 283.622)), (' A  31  SER  O  ', ' A  59  PHE  N  ', -0.444, (248.046, 184.114, 231.868)), (' D  87  GLU  N  ', ' D  87  GLU  OE1', -0.444, (242.458, 243.732, 142.673)), (' E 292  ASP  N  ', ' E 292  ASP  OD1', -0.444, (235.483, 149.608, 150.361)), (' E 474  MET  SD ', ' E 478  TRP  NE1', -0.444, (225.884, 166.014, 114.259)), (' D  53  ASN  O  ', ' D  58  ASN  ND2', -0.443, (211.68, 279.674, 146.203)), (' A 642  VAL HG12', ' A 651  ILE HG22', -0.442, (224.79, 182.317, 241.244)), (' C  57  PRO  HB2', ' C  60  SER  HB3', -0.442, (249.71, 258.187, 228.773)), (' B 742  ILE HG21', ' B 753  LEU HD13', -0.442, (226.566, 209.977, 224.681)), (' B1039  ARG  NH2', ' C1031  GLU  OE2', -0.442, (215.667, 224.354, 268.823)), (' A1047  TYR  HH ', ' B 886  TRP  HZ3', -0.441, (218.094, 210.629, 283.023)), (' A 130  VAL  O  ', ' A 130  VAL HG12', -0.441, (260.164, 192.798, 201.023)), (' A 985  ASP  O  ', ' A 989  ALA  N  ', -0.441, (241.407, 228.789, 211.119)), (' C1011  GLN  OE1', ' C1014  ARG  NH2', -0.441, (220.279, 234.424, 242.892)), (' E 142  LEU  H  ', ' E 142  LEU HD23', -0.441, (209.745, 150.146, 130.221)), (' A 332  ILE HD11', ' A 362  VAL HG11', -0.441, (201.405, 189.425, 198.238)), (' B1129  VAL HG13', ' C 917  TYR  HB3', -0.439, (210.681, 244.237, 294.706)), (' C1054  GLN  N  ', ' C1061  VAL  O  ', -0.437, (213.353, 241.881, 265.524)), (' B1128  VAL HG13', ' B1129  VAL HG23', -0.436, (213.154, 245.046, 298.1)), (' B 410  ILE HG22', ' B 425  LEU HD11', -0.436, (226.675, 253.562, 177.268)), (' C 758  SER  O  ', ' C 758  SER  OG ', -0.434, (210.958, 220.439, 230.256)), (' C 902  MET  HA ', ' C 902  MET  HE2', -0.434, (212.161, 239.351, 282.733)), (' E 586  ASN  OD1', ' E 587  TYR  N  ', -0.434, (246.857, 171.486, 142.474)), (' A 650  LEU  H  ', ' A 650  LEU HD23', -0.432, (223.128, 186.781, 245.336)), (' D 248  LEU HD22', ' D 262  LEU HD22', -0.432, (190.686, 254.212, 114.846)), (' E 132  VAL  O  ', ' E 132  VAL HG22', -0.432, (212.707, 149.679, 124.998)), (' A 294  ASP  O  ', ' A 298  GLU  N  ', -0.431, (237.895, 192.409, 237.421)), (' C 884  SER  OG ', ' C 894  LEU  N  ', -0.43, (199.277, 235.215, 278.393)), (' A 563  GLN  N  ', ' A 563  GLN  OE1', -0.428, (192.675, 199.601, 217.525)), (' B 582  LEU  O  ', ' B 582  LEU HD23', -0.427, (214.124, 268.14, 219.767)), (' A 940  SER  O  ', ' A 941  THR  OG1', -0.427, (245.392, 200.323, 263.38)), (' B 130  VAL  O  ', ' B 130  VAL HG12', -0.426, (191.068, 211.303, 189.475)), (' D 295  ASP  OD1', ' D 296  ALA  N  ', -0.424, (178.963, 259.02, 145.04)), (' A 312  ILE HD12', ' A 598  ILE HD11', -0.423, (227.435, 194.64, 246.765)), (' B  84  LEU HD22', ' B 267  VAL HG11', -0.423, (180.204, 222.442, 205.114)), (' A1128  VAL HG23', ' A1129  VAL HG23', -0.422, (195.448, 211.503, 294.859)), (' A 323  THR  OG1', ' A 537  LYS  NZ ', -0.422, (218.829, 186.213, 220.507)), (' B 620  VAL  N  ', ' B 621  PRO  HD2', -0.421, (192.613, 244.954, 228.182)), (' C1092  GLU  HA ', ' C1092  GLU  OE2', -0.421, (221.633, 224.54, 294.81)), (' A 712  ILE HD11', ' B 896  ILE HD12', -0.42, (211.476, 205.445, 288.208)), (' E 366  MET  O  ', ' E 370  LEU HD23', -0.42, (228.171, 158.783, 148.069)), (' A1091  ARG  NE ', ' A1118  ASP  O  ', -0.419, (210.963, 219.374, 301.76)), (' B 619  GLU  N  ', ' B 619  GLU  OE2', -0.419, (195.754, 248.114, 229.362)), (' B 485  GLY  N  ', ' B 488  CYS  SG ', -0.419, (245.726, 266.577, 153.969)), (' A 393  THR  OG1', ' A 394  ASN  N  ', -0.418, (203.549, 204.651, 191.013)), (' A 101  ILE HD11', ' A 263  ALA  HB1', -0.418, (264.247, 176.245, 219.829)), (' C 210  ILE HG21', ' C 217  PRO  HG3', -0.417, (244.7, 275.682, 232.834)), (' E 208  GLU  OE2', ' E 210  ASN  ND2', -0.416, (227.133, 196.714, 133.18)), (' D 107  VAL HG23', ' D 108  LEU HD12', -0.415, (234.517, 264.002, 127.93)), (' A 576  VAL HG22', ' A 587  ILE HD11', -0.414, (204.389, 193.354, 220.951)), (' B1104  VAL HG23', ' B1115  ILE HD12', -0.413, (201.546, 232.812, 299.77)), (' C 712  ILE  O  ', ' C1075  PHE  N  ', -0.413, (236.63, 234.121, 295.304)), (' A 725  GLU  OE1', ' A1064  HIS  NE2', -0.41, (229.698, 215.103, 270.284)), (' A 802  PHE  HD1', ' A 805  ILE HD11', -0.41, (241.766, 217.903, 279.923)), (' E 511  SER  OG ', ' E 514  ARG  NH2', -0.41, (221.673, 179.347, 135.705)), (' B 300  LYS  O  ', ' B 304  LYS  N  ', -0.409, (196.562, 219.037, 232.933)), (' D 574  VAL HG23', ' D 576  ALA  H  ', -0.408, (211.807, 233.115, 139.724)), (' C 485  GLY  N  ', ' C 488  CYS  SG ', -0.407, (230.922, 187.005, 181.702)), (' D 503  LEU HD23', ' D 505  HIS  N  ', -0.407, (210.995, 261.652, 127.43)), (' C 905  ARG  NH1', ' C1049  LEU  O  ', -0.407, (212.974, 235.393, 278.302)), (' B1050  MET  HE2', ' B1052  PHE  CZ ', -0.407, (204.774, 208.463, 274.811)), (' A1129  VAL HG13', ' B 917  TYR  HB3', -0.407, (198.193, 209.495, 292.382)), (' C 467  ASP  N  ', ' C 467  ASP  OD1', -0.407, (243.358, 198.074, 195.235)), (' B 645  THR  OG1', ' B 648  GLY  O  ', -0.406, (196.081, 243.384, 241.705)), (' D 266  LEU  C  ', ' D 267  LEU HD22', -0.406, (194.501, 256.574, 118.983)), (' C 369  TYR  OH ', ' C 384  PRO  O  ', -0.405, (251.98, 225.728, 203.518)), (' A  46  SER  N  ', ' A 279  TYR  O  ', -0.405, (254.636, 205.815, 239.495)), (' B 332  ILE  O  ', ' B 332  ILE HG23', -0.405, (214.453, 264.383, 203.26)), (' A 658  ASN  OD1', ' A 659  SER  N  ', -0.404, (222.242, 184.707, 262.473)), (' C 333  THR HG22', ' C 361  CYS  O  ', -0.404, (264.827, 216.272, 207.465)), (' B  62  VAL HG23', ' B 268  GLY  HA2', -0.402, (180.667, 222.898, 211.422)), (' A 914  ASN  ND2', ' A1111  GLU  OE2', -0.402, (224.06, 212.187, 299.369)), (' A 982  SER  OG ', ' A 983  ARG  N  ', -0.402, (248.989, 223.735, 214.379)), (' B 294  ASP  N  ', ' B 294  ASP  OD1', -0.401, (187.914, 226.991, 228.579)), (' C1053  PRO  O  ', ' C1054  GLN  NE2', -0.401, (210.429, 243.994, 267.017)), (' B1133  VAL  O  ', ' B1133  VAL HG23', -0.4, (201.719, 241.563, 300.543)), (' E  87  GLU  N  ', ' E  87  GLU  OE1', -0.4, (220.888, 209.589, 139.349))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
