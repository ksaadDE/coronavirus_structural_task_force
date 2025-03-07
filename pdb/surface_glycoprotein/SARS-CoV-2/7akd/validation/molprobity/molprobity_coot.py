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
data['omega'] = [('E', '   8 ', 'PRO', None, (205.15300000000005, 267.377, 275.906)), ('L', '   8 ', 'PRO', None, (269.12, 200.43500000000006, 270.973))]
data['rota'] = [('B', ' 338 ', 'PHE', 0.26444190621069014, (249.51100000000008, 227.52, 261.376)), ('B', ' 488 ', 'CYS', 0.012204796803416684, (220.6420000000001, 258.2400000000001, 269.713)), ('B', ' 489 ', 'TYR', 0.18077595588898784, (222.55700000000013, 255.66800000000006, 271.764)), ('C', ' 338 ', 'PHE', 0.1638553381783406, (194.24500000000015, 236.255, 265.082)), ('D', '  33 ', 'TYR', 0.13140095851083144, (185.34300000000013, 241.11600000000007, 273.125)), ('H', '  33 ', 'TYR', 0.1282808774025635, (259.675, 231.70000000000005, 268.312))]
data['cbeta'] = []
data['probe'] = [(' B  61  ASN  HB3', ' B1301  NAG  HN2', -0.894, (249.65, 177.064, 227.854)), (' E  24  ARG  HB3', ' E  70  GLU  HG2', -0.8, (209.505, 258.965, 275.853)), (' L  24  ARG  HB3', ' L  70  GLU  HG2', -0.786, (259.847, 201.879, 272.22)), (' B 343  ASN  OD1', ' O   1  NAG  N2 ', -0.729, (250.776, 226.64, 271.544)), (' B  61  ASN  HB3', ' B1301  NAG  N2 ', -0.721, (250.213, 177.688, 227.477)), (' A 123  ALA  HB3', ' A1302  NAG  H82', -0.712, (154.505, 236.972, 254.443)), (' A1005  GLN  OE1', ' C1002  GLN  NE2', -0.695, (216.962, 219.88, 222.206)), (' A 905  ARG  NH1', ' A1049  LEU  O  ', -0.691, (200.855, 224.326, 171.626)), (' C 336  CYS  N  ', ' C 361  CYS  SG ', -0.686, (192.142, 241.963, 260.855)), (' C 287  ASP  OD1', ' C 288  ALA  N  ', -0.672, (240.751, 246.637, 217.534)), (' C 708  SER  HG ', ' C 711  SER  HG ', -0.667, (201.203, 241.37, 160.141)), (' B 360  ASN  OD1', ' B 523  THR  OG1', -0.665, (255.551, 231.217, 248.824)), (' T   1  NAG  H61', ' T   6  FUC  H3 ', -0.657, (199.6, 234.502, 280.168)), (' C 401  VAL HG22', ' C 509  ARG  HG2', -0.657, (200.131, 223.063, 272.868)), (' D  64  LYS  HE2', ' D 201  MAN  H5 ', -0.657, (191.269, 242.454, 297.892)), (' C 708  SER  OG ', ' C 711  SER  OG ', -0.655, (201.861, 241.255, 159.548)), (' B  46  SER  HA ', ' B 279  TYR  O  ', -0.653, (219.486, 177.576, 218.372)), (' C 742  ILE  O  ', ' C1000  ARG  NH1', -0.636, (232.429, 215.398, 227.129)), (' A 314  GLN  N  ', ' A 314  GLN  OE1', -0.628, (190.093, 207.502, 213.036)), (' C 335  LEU HD23', ' D 101  LEU HD21', -0.627, (194.372, 245.38, 266.122)), (' B 406  GLU  OE1', ' B 409  GLN  NE2', -0.624, (222.761, 235.428, 263.963)), (' A 825  LYS  HD2', ' A 942  ALA  HB2', -0.623, (184.752, 227.535, 195.53)), (' B 233  ILE  HA ', ' B1304  NAG  H82', -0.622, (233.668, 184.408, 254.986)), (' A 358  ILE  HB ', ' A 395  VAL HG13', -0.612, (216.277, 180.46, 265.312)), (' B 905  ARG  NH1', ' B1049  LEU  O  ', -0.607, (208.038, 200.314, 172.042)), (' A 361  CYS  H  ', ' A 524  VAL HG12', -0.607, (215.387, 179.041, 258.982)), (' B  42  VAL HG23', ' B  44  ARG  HE ', -0.605, (217.785, 182.567, 228.835)), (' B 212  LEU HD12', ' B 217  PRO  HB3', -0.603, (241.317, 162.556, 224.538)), (' C 106  PHE  O  ', ' C 116  SER  N  ', -0.602, (243.239, 256.677, 251.285)), (' A 122  ASN  HB3', ' A 125  ASN  O  ', -0.594, (160.138, 234.446, 254.616)), (' C  91  TYR  OH ', ' C 191  GLU  OE2', -0.591, (245.32, 256.691, 227.553)), (' B 335  LEU HD23', ' H 101  LEU HD21', -0.589, (256.559, 221.824, 261.912)), (' A 951  VAL  O  ', ' A 955  ASN  ND2', -0.588, (200.986, 225.153, 205.4)), (' A 713  ALA  HA ', ' A1073  LYS  O  ', -0.587, (188.957, 200.685, 161.688)), (' C 125  ASN  ND2', ' C 172  SER  O  ', -0.582, (264.933, 252.031, 246.264)), (' C 361  CYS  SG ', ' C 362  VAL  N  ', -0.581, (192.06, 242.509, 258.325)), (' B 780  GLU  O  ', ' B 784  GLN  NE2', -0.572, (200.387, 205.844, 188.126)), (' C 760  CYS  SG ', ' C 764  ASN  ND2', -0.571, (229.106, 204.885, 218.743)), (' C 664  ILE  O  ', ' C 671  CYS  HB2', -0.571, (215.984, 245.597, 197.205)), (' A 406  GLU  OE1', ' A 409  GLN  NE2', -0.566, (212.25, 190.128, 289.346)), (' A 760  CYS  HA ', ' A 763  LEU HD12', -0.564, (217.403, 229.138, 219.482)), (' D  29  ILE HG23', ' D  34  TRP  HE1', -0.564, (179.92, 239.956, 272.258)), (' F   2  NAG  H3 ', ' F   2  NAG  H83', -0.563, (178.489, 205.234, 256.639)), (' J   2  NAG  H3 ', ' J   2  NAG  H83', -0.553, (194.89, 169.946, 271.496)), (' I   2  NAG  H3 ', ' I   2  NAG  H83', -0.549, (201.171, 163.3, 241.89)), (' J   1  NAG  H3 ', ' J   1  NAG  H83', -0.549, (201.757, 173.661, 271.326)), (' C 108  THR  O  ', ' C 237  ARG  NH1', -0.547, (236.663, 262.24, 250.215)), (' H  29  ILE HG23', ' H  34  TRP  HE1', -0.546, (261.603, 236.952, 266.962)), (' B 616  ASN  HB3', ' B1307  NAG  HN2', -0.539, (253.194, 209.097, 209.299)), (' A1307  NAG  H3 ', ' A1307  NAG  H83', -0.537, (180.418, 214.854, 166.845)), (' T   3  BMA  H4 ', ' U   1  MAN  H5 ', -0.535, (195.541, 238.541, 290.52)), (' V   2  NAG  H3 ', ' V   2  NAG  H83', -0.532, (233.145, 240.363, 161.155)), (' C  92  PHE  HE1', ' C  94  SER  HB3', -0.531, (248.639, 262.044, 234.297)), (' C 675  GLN HE21', ' C 693  ILE HD13', -0.528, (220.123, 256.637, 193.44)), (' O   1  NAG  O3 ', ' O   2  NAG  N2 ', -0.527, (250.489, 225.794, 276.94)), (' W   1  NAG  H4 ', ' W   2  NAG  HN2', -0.526, (207.688, 247.695, 160.674)), (' A 770  ILE HG23', ' A 774  GLN HE21', -0.523, (210.749, 227.968, 203.813)), (' C 980  ILE HG23', ' C 984  LEU HD12', -0.521, (232.958, 218.64, 240.602)), (' B 618  THR HG21', ' B1307  NAG  H62', -0.519, (258.038, 206.75, 211.992)), (' B 709  ASN  OD1', ' B 710  ASN  N  ', -0.515, (238.291, 212.382, 155.611)), (' A 661  GLU  O  ', ' A 695  TYR  OH ', -0.515, (181.587, 201.917, 196.261)), (' B 558  LYS  HE2', ' S   4  FUC  H2 ', -0.507, (260.104, 238.039, 220.296)), (' B 108  THR HG22', ' B 236  THR  H  ', -0.507, (240.664, 181.833, 251.871)), (' C 760  CYS  O  ', ' C 764  ASN  ND2', -0.506, (227.733, 205.539, 217.209)), (' A 930  ALA  O  ', ' A 934  ILE HG12', -0.506, (186.82, 224.158, 179.666)), (' A  61  ASN  HB3', ' A1301  NAG  HN2', -0.503, (164.029, 207.315, 231.901)), (' B 729  VAL HG13', ' B 781  VAL HG21', -0.501, (204.852, 202.603, 193.135)), (' L  13  VAL HG11', ' L  78  LEU HD13', -0.501, (274.294, 200.829, 258.765)), (' A 655  HIS  ND1', ' A1305  NAG  H82', -0.501, (176.951, 189.132, 201.165)), (' B 879  ALA  O  ', ' B 883  THR  OG1', -0.499, (196.238, 194.479, 173.795)), (' C  96  GLU  HA ', ' C 263  ALA  N  ', -0.497, (253.882, 267.374, 231.435)), (' E  13  VAL HG11', ' E  78  LEU HD13', -0.491, (200.153, 272.338, 264.628)), (' B1123  SER  OG ', ' C 914  ASN  ND2', -0.49, (222.221, 224.299, 149.52)), (' B  99  ASN  O  ', ' B 102  ARG  NE ', -0.49, (238.772, 157.918, 245.973)), (' E   6  GLN HE21', ' E  21  LEU HD21', -0.489, (200.459, 263.684, 273.426)), (' D  93  TYR  O  ', ' D 114  GLY  HA2', -0.487, (179.575, 256.03, 277.351)), (' C 709  ASN  ND2', ' C1306  NAG  O5 ', -0.487, (192.968, 239.828, 157.064)), (' H  93  TYR  O  ', ' H 114  GLY  HA2', -0.486, (275.591, 227.418, 270.378)), (' C  99  ASN  OD1', ' C 190  ARG  NH2', -0.486, (259.167, 261.054, 234.295)), (' A1031  GLU  OE2', ' C1039  ARG  NH2', -0.485, (212.885, 218.129, 180.997)), (' E  86  TYR  O  ', ' E 101  GLY  HA2', -0.482, (197.601, 262.817, 274.81)), (' L  86  TYR  O  ', ' L 101  GLY  HA2', -0.481, (269.929, 209.293, 269.356)), (' L   6  GLN  NE2', ' L  21  LEU HD21', -0.48, (268.331, 206.667, 268.074)), (' A 713  ALA  HB3', ' B 894  LEU HD22', -0.48, (190.384, 201.008, 165.464)), (' E   6  GLN  NE2', ' E  21  LEU HD21', -0.479, (200.523, 263.322, 272.845)), (' A 759  PHE  O  ', ' A 762  GLN  HG2', -0.478, (220.342, 227.583, 218.182)), (' L   6  GLN HE21', ' L  21  LEU HD21', -0.477, (268.451, 206.19, 268.351)), (' C 930  ALA  O  ', ' C 934  ILE HG12', -0.475, (233.518, 231.3, 175.773)), (' A 360  ASN  OD1', ' A 523  THR  OG1', -0.474, (219.737, 179.368, 257.425)), (' W   1  NAG  H4 ', ' W   2  NAG  N2 ', -0.473, (206.937, 247.686, 161.003)), (' B 656  VAL HG12', ' B 658  ASN  H  ', -0.471, (251.266, 193.686, 190.251)), (' B  94  SER  O  ', ' B 189  LEU HD12', -0.47, (239.16, 164.302, 234.825)), (' C1086  LYS  HD2', ' C1122  VAL HG11', -0.469, (195.25, 219.656, 142.327)), (' C 327  VAL  H  ', ' C 531  THR HG22', -0.469, (198.766, 252.221, 243.206)), (' L  18  ARG HH21', ' L  74  THR HG21', -0.466, (263.855, 199.684, 256.429)), (' A 359  SER  OG ', ' A 394  ASN  OD1', -0.466, (221.123, 181.658, 262.43)), (' H  58  ASN  HB3', ' L  94  TRP  CH2', -0.466, (257.384, 227.001, 279.82)), (' C 662  CYS  HB2', ' C 697  MET  HG2', -0.463, (213.76, 245.183, 192.698)), (' C 336  CYS  SG ', ' C 363  ALA  HB2', -0.462, (194.764, 239.719, 259.003)), (' C1050  MET  HE2', ' C1052  PHE  CZ ', -0.461, (231.951, 220.189, 171.368)), (' E  18  ARG HH21', ' E  74  THR HG21', -0.46, (207.406, 265.327, 260.706)), (' C 777  ASN  O  ', ' C 781  VAL HG23', -0.46, (227.86, 210.559, 191.039)), (' H  86  THR  N  ', ' H  89  ASP  OD2', -0.459, (277.2, 226.272, 287.12)), (' B 122  ASN  OD1', ' B 123  ALA  N  ', -0.456, (234.088, 156.431, 250.337)), (' H  21  THR HG22', ' H  79  SER  HB2', -0.455, (272.026, 239.09, 275.017)), (' A 523  THR HG23', ' A 524  VAL HG13', -0.454, (217.324, 180.983, 259.774)), (' A 715  PRO  HA ', ' A1071  GLN  O  ', -0.452, (188.268, 206.738, 164.391)), (' A 418  ILE  HA ', ' A 422  ASN HD22', -0.45, (217.843, 187.793, 287.834)), (' B 713  ALA  HB3', ' C 894  LEU HD22', -0.449, (232.356, 202.482, 162.175)), (' B 612  TYR  O  ', ' B 648  GLY  HA3', -0.449, (245.875, 203.455, 208.08)), (' L  66  GLY  HA3', ' L  71  PHE  CD2', -0.449, (255.758, 205.288, 266.036)), (' A 558  LYS  NZ ', ' N   1  NAG  H62', -0.446, (212.164, 164.994, 222.502)), (' C 927  PHE  CE1', ' C 931  ILE HD11', -0.443, (235.353, 225.608, 171.437)), (' E  66  GLY  HA3', ' E  71  PHE  CD2', -0.442, (208.654, 254.748, 269.196)), (' D  21  THR HG22', ' D  79  SER  HB2', -0.441, (172.749, 245.78, 281.414)), (' A 357  ARG HH11', ' A 394  ASN HD21', -0.439, (224.175, 182.585, 262.789)), (' B 616  ASN  N  ', ' B 616  ASN  OD1', -0.438, (251.395, 207.612, 211.853)), (' C 712  ILE HD11', ' C1096  VAL HG12', -0.438, (206.361, 234.098, 155.164)), (' A 403  ARG  NH2', ' A 406  GLU  OE2', -0.438, (210.601, 187.684, 292.767)), (' K   1  NAG  H4 ', ' K   2  NAG  H2 ', -0.437, (179.361, 237.551, 175.01)), (' G   1  NAG  H61', ' G   2  NAG  N2 ', -0.437, (170.299, 244.426, 222.874)), (' B 191  GLU  O  ', ' B 205  SER  HA ', -0.436, (232.152, 169.766, 237.087)), (' B1074  ASN HD21', ' P   1  NAG  C7 ', -0.435, (238.688, 199.333, 160.982)), (' A 927  PHE  CE2', ' A 931  ILE HD11', -0.434, (190.058, 228.831, 174.368)), (' H  60  ASN  OD1', ' H  62  SER  N  ', -0.432, (263.393, 222.761, 284.731)), (' D 109  GLU  OE1', ' E  46  LEU HD23', -0.43, (191.624, 250.634, 265.47)), (' C 780  GLU  O  ', ' C 784  GLN  NE2', -0.43, (226.511, 208.154, 186.253)), (' D  60  ASN  OD1', ' D  62  SER  N  ', -0.43, (191.897, 248.186, 289.421)), (' H 105  GLU  HB2', ' L  91  TYR  HB2', -0.428, (256.608, 220.009, 271.534)), (' C1097  SER  HB2', ' C1102  TRP  CD2', -0.427, (203.608, 235.959, 147.443)), (' C1006  THR  O  ', ' C1010  GLN  HG2', -0.427, (221.663, 219.546, 213.663)), (' B 298  GLU  OE2', ' B 315  THR  OG1', -0.426, (236.965, 195.313, 215.61)), (' D  86  THR  N  ', ' D  89  ASP  OD2', -0.426, (180.965, 256.711, 293.777)), (' C 676  THR  HA ', ' C 677  GLN  HA ', -0.426, (226.165, 259.233, 195.406)), (' A 328  ARG  HA ', ' A 530  SER  OG ', -0.425, (200.654, 179.618, 244.795)), (' A 599  THR  HB ', ' A 608  VAL HG12', -0.422, (179.531, 208.318, 211.583)), (' C 121  ASN  OD1', ' C 126  VAL HG22', -0.421, (259.781, 257.149, 241.782)), (' A 105  ILE HD12', ' A 241  LEU HD21', -0.419, (160.858, 220.245, 255.521)), (' C 430  THR  O  ', ' C 430  THR HG22', -0.419, (200.697, 227.878, 251.214)), (' C 106  PHE  HB3', ' C 235  ILE HG21', -0.417, (241.284, 256.898, 247.538)), (' B 359  SER  OG ', ' B 394  ASN  OD1', -0.412, (250.44, 234.362, 250.378)), (' A 703  ASN  OD1', ' A 704  SER  N  ', -0.412, (186.997, 194.441, 175.751)), (' C  92  PHE  CE1', ' C  94  SER  HB3', -0.41, (248.468, 262.238, 234.306)), (' C 347  PHE  CE2', ' C 399  SER  HB2', -0.409, (197.425, 225.309, 269.149)), (' A 957  GLN  O  ', ' A 961  THR HG23', -0.408, (198.705, 222.821, 216.327)), (' D   1  GLN  N  ', ' D   1  GLN  OE1', -0.407, (177.864, 246.788, 258.328)), (' A 115  GLN  HA ', ' A 132  GLU  HA ', -0.407, (170.809, 220.919, 264.291)), (' B 676  THR HG23', ' B 677  GLN  HG2', -0.407, (246.368, 180.41, 195.358)), (' C 826  VAL HG21', ' C1057  PRO  HG2', -0.405, (238.038, 223.722, 194.138)), (' B 703  ASN  OD1', ' B 704  SER  N  ', -0.405, (241.188, 202.313, 171.022)), (' C1083  HIS  HB3', ' C1088  HIS  NE2', -0.404, (197.381, 224.804, 141.533)), (' D  90  THR  HA ', ' D 117  VAL  O  ', -0.403, (179.072, 261.027, 286.767)), (' C  63  THR  O  ', ' C 266  TYR  HA ', -0.403, (241.906, 265.511, 231.407)), (' B 350  VAL HG11', ' B 402  ILE HG22', -0.402, (230.502, 236.927, 265.986)), (' A 108  THR HG22', ' A 234  ASN  O  ', -0.402, (174.444, 215.557, 257.23)), (' D  29  ILE HG12', ' D  34  TRP  HE1', -0.401, (179.078, 240.472, 272.241)), (' B 199  GLY  HA2', ' B 232  GLY  HA2', -0.4, (229.86, 184.72, 251.175)), (' C 320  VAL HG12', ' C 321  GLN  N  ', -0.4, (208.223, 251.304, 226.879)), (' B 276  LEU  O  ', ' B 288  ALA  HA ', -0.4, (229.6, 180.885, 221.75)), (' C 905  ARG  NH1', ' C1049  LEU  O  ', -0.4, (225.94, 218.417, 170.364))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
