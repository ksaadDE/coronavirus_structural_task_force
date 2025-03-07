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
data['rama'] = [('A', '1102 ', 'TRP', 0.03120945680565958, (220.10101, 191.14601, 149.07001)), ('C', '1102 ', 'TRP', 0.0018948957513657831, (190.65101, 214.56500999999994, 148.26901))]
data['omega'] = []
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' A 226  LEU  HG ', ' A 227  VAL HG23', -0.839, (180.554, 174.733, 243.243)), (' B 555  SER  HB3', ' B 586  ASP  HB2', -0.822, (215.88, 250.753, 226.897)), (' C  65  PHE  O  ', ' C 264  ALA  HA ', -0.807, (169.776, 256.328, 236.714)), (' A  65  PHE  O  ', ' A 264  ALA  HA ', -0.799, (191.042, 153.439, 236.897)), (' A 315  THR HG22', ' A 316  SER  H  ', -0.785, (210.216, 182.957, 219.054)), (' A 984  LEU HD21', ' A 988  GLU  HG2', -0.764, (198.529, 209.628, 246.233)), (' A 724  THR HG23', ' A 934  ILE HD11', -0.751, (196.494, 193.549, 183.783)), (' A 126  VAL HG13', ' A 174  PRO  HA ', -0.743, (176.561, 166.988, 246.394)), (' A 725  GLU  OE2', ' A1064  HIS  NE2', -0.732, (202.357, 201.349, 183.782)), (' C 826  VAL HG11', ' C1057  PRO  HG2', -0.725, (209.682, 236.671, 197.862)), (' B  65  PHE  O  ', ' B 264  ALA  HA ', -0.721, (270.256, 224.186, 239.175)), (' A 555  SER  HB3', ' A 586  ASP  HB2', -0.712, (243.372, 186.479, 224.228)), (' B  64  TRP  HE1', ' B 264  ALA  HB1', -0.709, (270.434, 223.704, 236.572)), (' C 448  ASN  HB2', ' C 497  PHE  HB2', -0.706, (203.618, 193.491, 280.549)), (' C 226  LEU  HG ', ' C 227  VAL HG23', -0.702, (192.621, 254.191, 243.388)), (' A  99  ASN  O  ', ' A 102  ARG  NH2', -0.683, (178.126, 157.787, 243.61)), (' A 567  ARG  NH1', ' A 571  ASP  OD1', -0.68, (237.132, 201.279, 230.486)), (' C 560  LEU  HG ', ' C 561  PRO  HD2', -0.679, (176.027, 179.899, 231.97)), (' B 349  SER  OG ', ' B 452  ARG  O  ', -0.674, (191.723, 228.249, 271.277)), (' C 384  PRO  HA ', ' C 387  LEU HD23', -0.673, (189.863, 206.006, 254.219)), (' C 126  VAL HG13', ' C 174  PRO  HA ', -0.67, (188.894, 262.069, 246.597)), (' B 457  ARG  NH1', ' B 460  ASN  O  ', -0.67, (184.874, 223.602, 257.455)), (' B 319  ARG  NH1', ' C 745  ASP  OD2', -0.667, (226.727, 232.698, 228.579)), (' B 126  VAL HG13', ' B 174  PRO  HA ', -0.662, (266.129, 203.189, 245.817)), (' A 457  ARG  NH1', ' A 467  ASP  OD2', -0.66, (247.735, 206.795, 286.674)), (' C 403  ARG  NH1', ' C 504  GLY  O  ', -0.66, (210.202, 201.218, 274.246)), (' A 393  THR  HB ', ' A 522  ALA  HA ', -0.659, (243.449, 199.906, 256.598)), (' B 560  LEU HD23', ' B 562  PHE  HE1', -0.655, (198.387, 252.353, 232.807)), (' B 974  SER  HB3', ' B 980  ILE HD11', -0.655, (224.417, 202.682, 240.017)), (' C 555  SER  HB3', ' C 586  ASP  HB2', -0.644, (173.059, 196.591, 226.062)), (' B 809  PRO  O  ', ' B 814  LYS  NZ ', -0.641, (237.763, 181.794, 186.638)), (' B 108  THR  O  ', ' B 237  ARG  NH1', -0.638, (254.958, 224.851, 255.908)), (' B 598  ILE HG23', ' B 664  ILE HD13', -0.636, (239.303, 227.579, 205.05)), (' B  46  SER  HA ', ' B 279  TYR  O  ', -0.632, (247.803, 202.889, 218.577)), (' A 726  ILE HG12', ' A1061  VAL HG22', -0.631, (196.463, 197.662, 190.388)), (' C 905  ARG  NH1', ' C1049  LEU  O  ', -0.629, (212.376, 225.242, 173.235)), (' B 353  TRP  O  ', ' B 466  ARG  NH1', -0.628, (194.266, 235.539, 264.648)), (' C 724  THR HG23', ' C 934  ILE HD11', -0.627, (203.537, 233.232, 183.632)), (' B 905  ARG  NH1', ' B1049  LEU  O  ', -0.626, (224.057, 203.579, 173.311)), (' B 121  ASN HD21', ' B 176  LEU  H  ', -0.625, (267.64, 205.977, 243.414)), (' A 153  MET  SD ', ' A 154  LYS  NZ ', -0.622, (168.372, 150.014, 249.711)), (' A1104  VAL HG13', ' A1115  ILE HG12', -0.621, (218.014, 197.521, 149.34)), (' A  21  ARG  NH1', ' A  23  GLN  OE1', -0.619, (199.804, 146.237, 246.052)), (' C 239  GLN  HG3', ' C 240  THR  H  ', -0.614, (173.732, 252.755, 249.195)), (' A 387  LEU  HA ', ' A 390  LEU HD12', -0.606, (235.24, 190.048, 260.618)), (' A 170  TYR  HE2', ' A 172  SER  HB2', -0.601, (178.16, 174.541, 249.102)), (' C  99  ASN  O  ', ' C 102  ARG  NH2', -0.601, (179.884, 265.512, 243.932)), (' C 388  ASN  O  ', ' C 528  LYS  NZ ', -0.6, (180.753, 203.721, 251.24)), (' B 331  ASN  OD1', ' B2003  NAG  N2 ', -0.6, (214.406, 256.034, 247.932)), (' A 523  THR HG23', ' A 524  VAL HG23', -0.599, (247.314, 196.337, 257.433)), (' C1135  ASN  OD1', ' C1136  THR  N  ', -0.596, (192.298, 209.62, 142.977)), (' C1104  VAL HG13', ' C1115  ILE HG12', -0.591, (197.141, 213.244, 148.574)), (' C 129  LYS  HG2', ' C 169  GLU  HG3', -0.59, (189.213, 255.598, 258.198)), (' B  18  LEU HD11', ' B 140  PHE  HZ ', -0.588, (273.705, 223.737, 253.417)), (' C 426  PRO  HG2', ' C 429  PHE  HB2', -0.583, (201.899, 194.726, 252.051)), (' A 984  LEU  O  ', ' C 386  LYS  NZ ', -0.582, (191.447, 210.531, 246.942)), (' B 339  GLY  HA2', ' R   1  NAG  H82', -0.581, (211.675, 240.109, 268.194)), (' A 379  CYS  HA ', ' A 432  CYS  HA ', -0.579, (235.987, 190.701, 270.187)), (' B 786  LYS  HG3', ' B 787  GLN  HG3', -0.577, (216.141, 185.851, 179.388)), (' A 383  SER  H  ', ' A 386  LYS  HE3', -0.576, (230.201, 190.152, 262.904)), (' C 726  ILE HG12', ' C1061  VAL HG22', -0.576, (207.334, 231.504, 190.5)), (' A 988  GLU  N  ', ' A 988  GLU  OE1', -0.574, (199.303, 211.905, 247.739)), (' C 974  SER  HB3', ' C 980  ILE HD11', -0.57, (210.93, 228.172, 239.861)), (' C  64  TRP  HE1', ' C 264  ALA  HB1', -0.569, (170.293, 257.497, 234.417)), (' A  96  GLU  HG2', ' A 101  ILE HG12', -0.569, (183.168, 157.407, 240.789)), (' B 214  ARG  NH1', ' B 266  TYR  OH ', -0.56, (268.834, 222.847, 232.205)), (' A 375  SER  N  ', ' A 435  ALA  O  ', -0.56, (240.537, 181.735, 276.447)), (' C 729  VAL HG22', ' C1059  GLY  HA2', -0.559, (213.935, 228.243, 195.13)), (' A 329  PHE  HB2', ' A 330  PRO  HD3', -0.559, (241.448, 186.992, 245.506)), (' A1087  ALA  HB2', ' A1126  CYS  HB3', -0.558, (231.733, 202.872, 148.918)), (' C 344  ALA  HB3', ' C 347  PHE  HE1', -0.557, (190.751, 192.367, 270.882)), (' C 560  LEU HD23', ' C 562  PHE  HE1', -0.555, (180.352, 180.221, 232.077)), (' B 770  ILE HD11', ' B1012  LEU HD23', -0.555, (212.379, 202.96, 208.735)), (' A 641  ASN HD21', ' A 654  GLU  HG3', -0.554, (218.214, 166.035, 204.814)), (' C 640  SER  OG ', ' C 641  ASN  N  ', -0.554, (168.624, 228.095, 208.421)), (' I   1  NAG  H3 ', ' I   1  NAG  H83', -0.553, (235.357, 189.197, 157.338)), (' B  18  LEU  HB2', ' B  21  ARG HH22', -0.553, (272.82, 228.037, 254.862)), (' A 121  ASN  HA ', ' A 126  VAL HG12', -0.55, (178.299, 165.247, 247.8)), (' A 905  ARG  NH1', ' A1049  LEU  O  ', -0.549, (199.054, 204.751, 172.653)), (' B  18  LEU  O  ', ' B  21  ARG  NH1', -0.549, (273.826, 230.282, 256.048)), (' A  25  PRO  HD2', ' A  66  HIS  HB3', -0.548, (194.356, 148.962, 237.399)), (' C 143  VAL HG23', ' C 154  LYS  HB3', -0.546, (176.973, 272.069, 251.141)), (' A 408  ARG  NH2', ' A 414  GLN  OE1', -0.544, (233.009, 194.154, 285.99)), (' B 540  ASN  HB3', ' B 549  THR HG22', -0.544, (225.475, 239.277, 235.566)), (' A 108  THR  O  ', ' A 237  ARG  NH1', -0.544, (200.997, 164.054, 254.567)), (' A 733  LYS  HD2', ' A 771  ALA  HB1', -0.544, (192.097, 215.049, 205.789)), (' B 726  ILE HG12', ' B1061  VAL HG22', -0.542, (230.666, 204.91, 191.015)), (' B 418  ILE  HA ', ' B 422  ASN HD22', -0.539, (192.329, 222.058, 265.217)), (' B 214  ARG HH22', ' B 266  TYR  HE2', -0.537, (266.904, 224.961, 232.725)), (' C 358  ILE HG23', ' C 395  VAL  HB ', -0.536, (186.534, 192.186, 256.893)), (' C 457  ARG  NH1', ' C 467  ASP  OD2', -0.535, (210.401, 181.338, 261.545)), (' C 733  LYS  HD2', ' C 771  ALA  HB1', -0.535, (223.453, 226.095, 206.785)), (' B 763  LEU HD22', ' B1008  VAL HG21', -0.534, (212.824, 201.392, 217.937)), (' B 759  PHE  HA ', ' B 762  GLN HE22', -0.534, (206.794, 200.346, 222.051)), (' B1105  THR HG22', ' B1112  PRO  HA ', -0.533, (226.937, 221.475, 153.809)), (' A 989  ALA  O  ', ' A 993  ILE HG12', -0.533, (197.338, 211.236, 240.326)), (' A 398  ASP  OD2', ' A 423  TYR  OH ', -0.533, (243.534, 198.221, 275.018)), (' C 903  ALA  HB1', ' C 913  GLN  HB2', -0.53, (211.684, 226.399, 160.371)), (' C 866  THR HG22', ' C 869  MET  HE3', -0.527, (226.991, 236.97, 196.134)), (' A 640  SER  OG ', ' A 641  ASN  N  ', -0.527, (217.637, 166.193, 209.54)), (' B 358  ILE  HB ', ' B 395  VAL  HB ', -0.522, (205.739, 241.325, 256.874)), (' C 139  PRO  HB3', ' C 159  VAL  HB ', -0.522, (174.832, 257.774, 255.0)), (' A 985  ASP  OD2', ' A 987  PRO  HD2', -0.522, (196.211, 213.903, 249.706)), (' C 758  SER  O  ', ' C 762  GLN  NE2', -0.522, (223.9, 211.967, 221.898)), (' C 516  GLU  OE1', ' C 519  HIS  ND1', -0.522, (190.625, 191.944, 244.543)), (' A 490  PHE  CE2', ' A 492  LEU  HB2', -0.52, (253.7, 199.209, 293.155)), (' A 568  ASP  OD1', ' A 572  THR  OG1', -0.52, (235.503, 197.02, 223.77)), (' C 809  PRO  O  ', ' C 814  LYS  NZ ', -0.519, (223.254, 248.963, 186.615)), (' B 444  LYS  HD2', ' B 446  GLY  H  ', -0.519, (198.611, 226.758, 288.549)), (' A 452  ARG  HG3', ' A 494  SER  HA ', -0.519, (252.489, 192.26, 292.535)), (' A 170  TYR  CE2', ' A 172  SER  HB2', -0.518, (177.824, 174.693, 249.342)), (' A1043  CYS  HB2', ' A1064  HIS  CE1', -0.517, (202.252, 202.545, 181.738)), (' C  81  ASN  HB3', ' C 239  GLN HE21', -0.517, (170.59, 253.498, 248.901)), (' B 403  ARG  HG3', ' B 497  PHE  HE1', -0.516, (199.587, 221.071, 275.413)), (' A 729  VAL HG22', ' A1059  GLY  HA2', -0.516, (195.472, 205.348, 194.941)), (' C 442  ASP  OD2', ' C 509  ARG  NE ', -0.516, (195.372, 195.351, 275.301)), (' B 319  ARG  HE ', ' B 592  PHE  HB3', -0.515, (227.492, 234.85, 224.528)), (' C  18  LEU HD22', ' C 140  PHE  HZ ', -0.514, (165.536, 260.573, 251.549)), (' C 737  ASP  OD1', ' C 738  CYS  N  ', -0.514, (223.916, 224.658, 222.521)), (' A 374  PHE  HA ', ' A 436  TRP  HB3', -0.514, (243.051, 181.067, 275.601)), (' B 804  GLN  NE2', ' B 935  GLN  OE1', -0.514, (242.204, 199.609, 182.609)), (' A 642  VAL HG13', ' A 651  ILE HG22', -0.512, (220.371, 171.514, 212.829)), (' B 344  ALA  O  ', ' B 509  ARG  NH1', -0.511, (204.678, 235.882, 274.398)), (' C 433  VAL HG23', ' C 512  VAL HG12', -0.51, (198.43, 198.895, 262.121)), (' C 452  ARG  HG3', ' C 494  SER  HA ', -0.509, (208.349, 187.628, 276.443)), (' B  83  VAL HG11', ' B 237  ARG HH21', -0.509, (258.051, 226.662, 253.783)), (' A  64  TRP  HE1', ' A 264  ALA  HB1', -0.507, (190.38, 153.514, 234.819)), (' C 770  ILE HD11', ' C1012  LEU HD23', -0.507, (217.561, 217.506, 208.638)), (' A 316  SER  O  ', ' A 595  VAL HG22', -0.507, (213.618, 183.215, 218.872)), (' C 391  CYS  SG ', ' C 522  ALA  HB1', -0.507, (181.274, 195.446, 247.253)), (' B1125  ASN  ND2', ' B1127  ASP  OD2', -0.506, (205.342, 236.96, 145.552)), (' B 103  GLY  H  ', ' B 241  LEU  HB2', -0.505, (267.289, 214.491, 248.641)), (' B1002  GLN  NE2', ' C1005  GLN  OE1', -0.505, (214.634, 212.372, 223.776)), (' C 103  GLY  H  ', ' C 241  LEU  HB2', -0.505, (178.325, 258.553, 248.038)), (' C1088  HIS  CE1', ' C1122  VAL HG22', -0.504, (201.524, 203.575, 145.068)), (' C 349  SER  OG ', ' C 452  ARG  O  ', -0.503, (205.072, 188.209, 271.71)), (' A 540  ASN  HB3', ' A 549  THR HG22', -0.5, (228.497, 185.533, 234.211)), (' B 568  ASP  OD1', ' B 572  THR  OG1', -0.498, (210.971, 239.166, 225.575)), (' B 605  SER  OG ', ' B 606  ASN  N  ', -0.497, (250.939, 225.622, 207.804)), (' A 117  LEU HD21', ' A 119  ILE HD11', -0.496, (186.969, 170.058, 250.537)), (' B 517  LEU  H  ', ' B 519  HIS  CE1', -0.495, (203.531, 236.239, 245.308)), (' B 112  SER  HA ', ' B 132  GLU  HB3', -0.494, (256.777, 216.294, 264.25)), (' A 310  LYS  HE3', ' A 664  ILE HD11', -0.494, (207.733, 178.722, 201.363)), (' B 906  PHE  CD2', ' B 916  LEU  HB2', -0.494, (228.845, 206.851, 163.627)), (' C 985  ASP  OD1', ' C 986  PRO  HD2', -0.493, (220.941, 223.979, 249.703)), (' A 707  TYR  HD2', ' B 883  THR HG23', -0.492, (226.818, 190.047, 169.431)), (' A 201  PHE  HD2', ' A 203  ILE HD11', -0.492, (188.413, 173.7, 247.17)), (' C 376  THR  HB ', ' C 435  ALA  HB3', -0.492, (198.997, 204.11, 266.265)), (' A 189  LEU HD23', ' A 210  ILE  HB ', -0.489, (183.063, 160.976, 228.768)), (' C1043  CYS  HB2', ' C1064  HIS  CE1', -0.489, (208.001, 224.355, 182.164)), (' C 619  GLU  HG2', ' C 619  GLU  O  ', -0.489, (173.344, 215.89, 219.88)), (' C 916  LEU HD12', ' C 923  ILE HD13', -0.486, (206.022, 231.439, 164.167)), (' A 659  SER  HB2', ' A 698  SER  HB2', -0.485, (219.818, 177.316, 191.187)), (' A 715  PRO  HA ', ' A1072  GLU  HA ', -0.485, (212.212, 187.292, 164.107)), (' C 157  PHE  HE1', ' C 159  VAL HG22', -0.485, (178.189, 259.45, 256.672)), (' B1053  PRO  O  ', ' B1054  GLN  NE2', -0.484, (230.084, 196.941, 185.055)), (' B 897  PRO  HG2', ' B 900  MET  HG3', -0.484, (226.353, 195.423, 162.015)), (' C 353  TRP  O  ', ' C 466  ARG  NH2', -0.483, (197.81, 185.385, 264.075)), (' C 233  ILE HG22', ' C 234  ASN  N  ', -0.483, (183.703, 241.328, 254.519)), (' B 916  LEU HD12', ' B 923  ILE HD13', -0.483, (232.152, 206.524, 164.861)), (' C 490  PHE  CE2', ' C 492  LEU  HB2', -0.483, (210.51, 181.915, 272.853)), (' B1028  LYS  NZ ', ' B1042  PHE  O  ', -0.482, (221.071, 210.476, 184.624)), (' A 605  SER  OG ', ' A 606  ASN  N  ', -0.482, (202.568, 170.29, 207.267)), (' B 455  LEU  N  ', ' B 491  PRO  O  ', -0.482, (186.198, 221.827, 269.283)), (' A 896  ILE HD12', ' A 897  PRO  HD2', -0.482, (190.245, 210.108, 162.35)), (' B 393  THR  HB ', ' B 522  ALA  HA ', -0.481, (206.878, 244.124, 247.789)), (' B 234  ASN  HB2', ' B2002  NAG  H2 ', -0.481, (244.966, 217.208, 255.891)), (' C 329  PHE  O  ', ' C 580  GLN  NE2', -0.481, (170.641, 197.266, 245.577)), (' C 988  GLU  O  ', ' C 992  GLN  HG2', -0.481, (214.657, 221.396, 243.139)), (' B1115  ILE HG22', ' B1137  VAL HG23', -0.481, (218.82, 223.566, 144.764)), (' B 452  ARG  NH2', ' B 492  LEU  O  ', -0.48, (185.042, 224.88, 274.829)), (' B 742  ILE HD11', ' B 753  LEU HD22', -0.48, (213.457, 196.706, 229.099)), (' B 290  ASP  OD1', ' B 291  CYS  N  ', -0.479, (245.487, 220.762, 225.104)), (' C 365  TYR  CD2', ' C 387  LEU  HB3', -0.478, (185.531, 202.729, 255.266)), (' B 866  THR HG22', ' B 869  MET  HG3', -0.477, (225.557, 185.246, 195.105)), (' A 490  PHE  CD1', ' A 491  PRO  HD2', -0.477, (253.912, 201.983, 295.353)), (' A 412  PRO  HG3', ' A 429  PHE  HB3', -0.476, (234.01, 198.109, 274.305)), (' B 825  LYS  HD2', ' B 945  LEU HD13', -0.476, (237.526, 204.898, 194.964)), (' C 398  ASP  HB2', ' C 512  VAL HG22', -0.476, (197.059, 193.553, 261.336)), (' A 200  TYR  HE1', ' C 357  ARG HH12', -0.476, (189.042, 183.696, 251.007)), (' B 543  PHE  HE2', ' B 578  ASP  HB3', -0.475, (217.274, 250.581, 238.107)), (' A 578  ASP  N  ', ' A 578  ASP  OD1', -0.475, (246.313, 186.62, 234.89)), (' C  53  ASP  HB3', ' C  55  PHE  CE2', -0.475, (190.458, 239.216, 233.208)), (' A 188  ASN  HA ', ' A 209  PRO  HA ', -0.475, (179.056, 160.597, 230.386)), (' B 287  ASP  HB3', ' B 306  PHE  HE2', -0.475, (250.252, 211.53, 218.624)), (' A1038  LYS  HB2', ' A1038  LYS  HE2', -0.474, (208.206, 208.622, 172.669)), (' C 950  ASP  OD1', ' C 951  VAL  N  ', -0.473, (205.094, 227.305, 202.415)), (' C 233  ILE HG22', ' C 234  ASN  H  ', -0.472, (183.813, 241.732, 254.991)), (' B 664  ILE  O  ', ' B 671  CYS  HB2', -0.471, (236.084, 229.792, 201.073)), (' A 822  LEU HD22', ' A 945  LEU HD21', -0.471, (192.749, 195.627, 192.635)), (' B 822  LEU HD22', ' B 945  LEU HD21', -0.469, (234.132, 203.038, 193.717)), (' B 989  ALA  O  ', ' B 993  ILE HG12', -0.468, (216.659, 200.414, 240.83)), (' B 403  ARG  HG2', ' B 505  TYR  HA ', -0.468, (201.022, 218.514, 275.665)), (' B 619  GLU  HG2', ' B 619  GLU  O  ', -0.468, (233.377, 241.1, 221.063)), (' C 691  SER  OG ', ' C 692  ILE  N  ', -0.467, (173.95, 232.433, 203.21)), (' C1087  ALA  HB2', ' C1126  CYS  HB3', -0.467, (194.894, 199.068, 148.146)), (' B 228  ASP  OD1', ' B 229  LEU  N  ', -0.466, (250.255, 205.297, 246.988)), (' C 578  ASP  OD1', ' C 583  GLU  N  ', -0.466, (169.947, 192.892, 236.069)), (' C 403  ARG  NH1', ' C 405  ASP  OD2', -0.465, (210.881, 201.392, 273.604)), (' B 770  ILE  O  ', ' B 774  GLN  HG2', -0.465, (216.282, 197.889, 204.531)), (' C 383  SER  HB3', ' C 386  LYS  HD2', -0.465, (190.733, 209.231, 249.952)), (' B 552  LEU HD23', ' B 585  LEU HD23', -0.465, (219.992, 250.068, 233.609)), (' C 641  ASN HD21', ' C 654  GLU  HG3', -0.464, (167.894, 227.126, 204.022)), (' C 328  ARG HH21', ' C 580  GLN  HB2', -0.463, (169.32, 195.828, 241.451)), (' C 931  ILE  O  ', ' C 934  ILE HG22', -0.463, (204.186, 238.591, 180.753)), (' A 707  TYR  HB3', ' B 792  PRO  HG3', -0.462, (229.792, 186.935, 170.169)), (' C 742  ILE HD11', ' C 753  LEU HD22', -0.462, (221.705, 221.094, 228.661)), (' A 401  VAL HG22', ' A 509  ARG  HG2', -0.461, (249.591, 186.235, 280.791)), (' B 444  LYS  HD2', ' B 446  GLY  N  ', -0.46, (198.553, 226.584, 288.335)), (' A 131  CYS  HB2', ' A 133  PHE  CD1', -0.46, (187.369, 167.682, 260.869)), (' B 560  LEU HD23', ' B 562  PHE  CE1', -0.46, (199.021, 252.645, 233.26)), (' B 826  VAL HG11', ' B1057  PRO  HG2', -0.459, (233.289, 199.561, 198.222)), (' A1096  VAL  O  ', ' A1102  TRP  HA ', -0.459, (219.903, 191.197, 151.114)), (' A  30  ASN  HB3', ' A  32  PHE  CE2', -0.459, (196.111, 160.367, 224.809)), (' C 796  ASP  N  ', ' C 796  ASP  OD1', -0.459, (218.744, 242.387, 167.303)), (' A 713  ALA  HB3', ' B 894  LEU  HB3', -0.458, (218.105, 189.16, 166.161)), (' B 125  ASN HD21', ' O   2  NAG  H82', -0.458, (267.498, 197.188, 252.895)), (' A  37  TYR  HA ', ' A 223  LEU  H  ', -0.458, (186.914, 174.975, 231.672)), (' B 650  LEU HD21', ' B 653  ALA  HB3', -0.458, (241.127, 235.824, 206.705)), (' A 897  PRO  HG2', ' A 900  MET  SD ', -0.458, (190.747, 207.87, 160.694)), (' A 665  PRO  HA ', ' A 671  CYS  HB3', -0.458, (215.302, 182.51, 200.582)), (' A1105  THR HG22', ' A1112  PRO  HA ', -0.457, (213.403, 193.18, 153.178)), (' B 328  ARG  HG3', ' B 579  PRO  HD2', -0.457, (216.979, 250.305, 241.732)), (' A 295  PRO  HB2', ' A 608  VAL HG21', -0.456, (208.069, 174.881, 213.974)), (' B 729  VAL HG22', ' B1059  GLY  HA2', -0.455, (224.193, 200.606, 195.5)), (' C 444  LYS  N  ', ' C 448  ASN  OD1', -0.455, (200.747, 194.491, 283.438)), (' B 796  ASP  N  ', ' B 796  ASP  OD1', -0.455, (235.148, 189.787, 167.807)), (' B 560  LEU  O  ', ' B 562  PHE  N  ', -0.455, (202.521, 253.529, 235.577)), (' C 567  ARG  HD3', ' C 571  ASP  HA ', -0.455, (188.008, 194.349, 227.964)), (' A 360  ASN  H  ', ' A 523  THR HG23', -0.454, (248.615, 196.895, 257.311)), (' B 699  LEU HD21', ' C 869  MET  HB3', -0.453, (227.315, 234.486, 191.881)), (' A 490  PHE  HE2', ' A 492  LEU  HB2', -0.453, (253.927, 198.746, 293.135)), (' B 858  LEU  H  ', ' B 858  LEU HD23', -0.453, (224.227, 193.868, 220.291)), (' A 317  ASN  HA ', ' A 594  GLY  HA2', -0.453, (216.201, 184.827, 219.238)), (' A 796  ASP  N  ', ' A 796  ASP  OD1', -0.452, (181.289, 201.744, 166.735)), (' A 402  ILE HD11', ' A 510  VAL HG21', -0.452, (241.946, 188.47, 281.669)), (' B 977  LEU  H  ', ' B 977  LEU HD23', -0.452, (223.699, 197.535, 235.536)), (' C 188  ASN  OD1', ' C 189  LEU  N  ', -0.452, (182.404, 261.979, 232.184)), (' A 612  TYR  HB2', ' A 649  CYS  SG ', -0.452, (221.225, 177.524, 214.948)), (' A 816  SER  OG ', ' A 819  GLU  OE1', -0.452, (185.441, 199.902, 185.999)), (' B1118  ASP  OD1', ' B1119  ASN  N  ', -0.452, (216.986, 216.916, 147.087)), (' B 408  ARG  NH1', ' B 415  THR  O  ', -0.45, (198.365, 215.195, 261.282)), (' A 105  ILE  HB ', ' A 239  GLN  HB2', -0.45, (191.659, 161.711, 251.329)), (' C 988  GLU  N  ', ' C 988  GLU  OE1', -0.45, (217.003, 221.018, 247.825)), (' B  83  VAL HG11', ' B 237  ARG  HE ', -0.449, (257.081, 226.16, 253.239)), (' B 967  SER  O  ', ' B 967  SER  OG ', -0.449, (229.203, 205.704, 231.215)), (' C 748  GLU  N  ', ' C 748  GLU  OE1', -0.449, (225.971, 225.53, 238.558)), (' C 770  ILE  O  ', ' C 774  GLN  HG2', -0.449, (220.194, 222.862, 205.068)), (' C 106  PHE  HB3', ' C 235  ILE HD12', -0.449, (181.877, 245.821, 251.654)), (' A1029  MET  HB2', ' A1062  PHE  HZ ', -0.449, (197.882, 207.613, 186.359)), (' C 214  ARG  NH1', ' C 266  TYR  OH ', -0.447, (170.73, 255.462, 230.438)), (' A 130  VAL  HB ', ' A 168  PHE  HB3', -0.445, (186.722, 174.456, 257.322)), (' A 877  LEU HD13', ' A1029  MET  HE2', -0.444, (193.096, 209.947, 184.352)), (' A1028  LYS  NZ ', ' A1042  PHE  O  ', -0.444, (205.912, 203.29, 184.339)), (' A  31  SER  HB3', ' A  60  SER  H  ', -0.444, (198.91, 165.35, 228.27)), (' B 878  LEU  HA ', ' B 881  THR HG22', -0.444, (226.064, 195.087, 179.109)), (' B 197  ILE  HB ', ' B 202  LYS  HZ1', -0.443, (245.183, 211.207, 243.86)), (' B 329  PHE  O  ', ' B 580  GLN  NE2', -0.443, (218.328, 252.057, 246.612)), (' C 112  SER  HA ', ' C 132  GLU  HB3', -0.442, (179.865, 247.926, 263.645)), (' A 125  ASN  HA ', ' A 174  PRO  HD3', -0.442, (173.159, 168.246, 248.037)), (' A 453  TYR  HE2', ' A 455  LEU HD13', -0.441, (244.447, 195.591, 294.638)), (' B 475  ALA  N  ', ' B 487  ASN  O  ', -0.441, (174.736, 216.128, 268.707)), (' B 445  VAL  HA ', ' B 499  PRO  HG3', -0.44, (201.998, 224.202, 288.248)), (' C 552  LEU HD23', ' C 585  LEU HD13', -0.44, (172.597, 199.918, 233.09)), (' B 190  ARG  HB3', ' B 192  PHE  HE1', -0.44, (264.751, 211.456, 239.104)), (' B1090  PRO  HD3', ' B1095  PHE  CE2', -0.44, (216.175, 225.865, 153.465)), (' A 560  LEU  O  ', ' A 562  PHE  N  ', -0.44, (252.692, 196.387, 232.164)), (' A  29  THR HG23', ' A  62  VAL HG13', -0.439, (196.308, 159.383, 230.978)), (' B 336  CYS  HB2', ' B 361  CYS  HB3', -0.439, (211.384, 245.18, 258.928)), (' C 398  ASP  OD2', ' C 423  TYR  OH ', -0.439, (198.509, 191.609, 258.935)), (' C1039  ARG  HG3', ' C1042  PHE  HB2', -0.438, (207.605, 216.026, 180.943)), (' B 737  ASP  OD1', ' B 738  CYS  N  ', -0.438, (215.66, 193.189, 223.074)), (' B 106  PHE  HB3', ' B 235  ILE HD13', -0.438, (254.11, 215.648, 251.155)), (' C 555  SER  OG ', ' C 585  LEU  O  ', -0.438, (173.071, 194.709, 228.249)), (' B 214  ARG HH11', ' B 215  ASP  HA ', -0.438, (268.639, 223.521, 230.084)), (' A 369  TYR  HE1', ' A 384  PRO  HB2', -0.437, (234.007, 183.576, 265.944)), (' A 327  VAL HG12', ' A 542  ASN  HB3', -0.436, (235.105, 186.676, 241.281)), (' B 930  ALA  O  ', ' B 934  ILE HG12', -0.436, (238.145, 206.812, 180.258)), (' A 376  THR  HB ', ' A 435  ALA  HB3', -0.436, (239.134, 184.815, 277.65)), (' A 802  PHE  CD2', ' A 882  ILE HD11', -0.436, (187.329, 201.055, 173.325)), (' B1043  CYS  HB2', ' B1064  HIS  CE1', -0.435, (224.268, 207.791, 182.444)), (' A 986  PRO  HA ', ' A 989  ALA  HB3', -0.435, (195.504, 212.818, 244.619)), (' C 455  LEU  N  ', ' C 491  PRO  O  ', -0.435, (213.122, 186.191, 269.451)), (' C 984  LEU HD12', ' C 985  ASP  H  ', -0.435, (216.164, 225.747, 248.875)), (' A 973  ILE HD11', ' A 980  ILE HD13', -0.434, (196.521, 205.014, 243.403)), (' C 722  VAL HG22', ' C1065  VAL HG22', -0.434, (205.978, 231.996, 176.496)), (' A 616  ASN  OD1', ' A 617  CYS  N  ', -0.434, (228.501, 176.125, 214.45)), (' B  89  GLY  HA3', ' B 270  LEU HD12', -0.433, (250.636, 217.775, 240.2)), (' B  99  ASN  O  ', ' B 102  ARG  NH2', -0.433, (273.392, 210.879, 244.768)), (' B 354  ASN  O  ', ' B 398  ASP  HA ', -0.433, (198.895, 235.412, 263.916)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.433, (206.712, 220.188, 185.187)), (' A 906  PHE  CD2', ' A 916  LEU  HB2', -0.432, (199.625, 198.982, 163.384)), (' C 231  ILE HG22', ' C 233  ILE HD11', -0.432, (188.653, 245.372, 254.755)), (' A 363  ALA  O  ', ' A 527  PRO  HD3', -0.432, (243.203, 187.103, 257.312)), (' C 121  ASN  HA ', ' C 126  VAL HG12', -0.432, (186.17, 261.573, 248.535)), (' A  53  ASP  HB3', ' A  55  PHE  CE2', -0.432, (196.069, 179.88, 233.294)), (' C 998  THR  O  ', ' C1002  GLN  HG2', -0.431, (211.706, 216.933, 228.44)), (' B 715  PRO  HA ', ' B1072  GLU  HA ', -0.43, (232.486, 223.797, 164.541)), (' B 344  ALA  HB3', ' B 347  PHE  CE1', -0.43, (202.999, 237.255, 271.737)), (' B 721  SER  OG ', ' B1066  THR  OG1', -0.429, (230.645, 212.427, 177.161)), (' A 705  VAL HG13', ' B 883  THR HG21', -0.429, (225.003, 187.403, 171.609)), (' A 290  ASP  O  ', ' A 297  SER  HB3', -0.429, (201.665, 176.215, 221.193)), (' C 299  THR  OG1', ' C 597  VAL HG21', -0.428, (185.604, 229.828, 213.575)), (' B  91  TYR  OH ', ' B 191  GLU  OE1', -0.428, (260.128, 216.246, 232.995)), (' A 417  LYS  HA ', ' A 417  LYS  HD3', -0.428, (240.271, 198.492, 291.658)), (' B 928  ASN  O  ', ' B 931  ILE HG22', -0.426, (240.461, 203.146, 176.745)), (' A 295  PRO  HA ', ' A 298  GLU  OE2', -0.426, (208.022, 177.03, 218.242)), (' C 485  GLY  H  ', ' C 488  CYS  HB2', -0.426, (222.81, 177.022, 275.383)), (' A 949  GLN  NE2', ' A 953  ASN  OD1', -0.425, (194.658, 194.392, 205.441)), (' B 159  VAL HG23', ' B 160  TYR  HD1', -0.425, (266.284, 213.64, 259.79)), (' A 811  LYS  HB2', ' A 811  LYS  HE3', -0.424, (177.321, 196.889, 187.232)), (' C  14  GLN  O  ', ' C 158  ARG  HB2', -0.424, (172.338, 262.727, 260.437)), (' C  30  ASN  HB3', ' C  32  PHE  CZ ', -0.423, (173.178, 248.431, 224.464)), (' C 310  LYS  HG3', ' C 600  PRO  HA ', -0.423, (184.756, 232.785, 203.046)), (' C  18  LEU  O  ', ' C  21  ARG  NH1', -0.422, (160.563, 256.897, 253.249)), (' A 988  GLU  O  ', ' A 992  GLN  HG2', -0.422, (199.614, 209.516, 243.076)), (' A 365  TYR  CD2', ' A 387  LEU  HB3', -0.421, (239.221, 187.803, 261.215)), (' C 766  ALA  O  ', ' C 770  ILE HG12', -0.421, (220.441, 219.182, 210.28)), (' A 578  ASP  OD2', ' A 581  THR  HB ', -0.421, (247.649, 182.95, 235.22)), (' B 699  LEU HD22', ' C 873  TYR  CZ ', -0.421, (227.762, 231.795, 190.116)), (' B 402  ILE HG22', ' B 403  ARG  O  ', -0.421, (200.832, 221.627, 270.361)), (' B 612  TYR  HB2', ' B 649  CYS  SG ', -0.42, (234.949, 237.639, 215.276)), (' C 200  TYR  CD1', ' C 230  PRO  HA ', -0.42, (195.228, 243.408, 250.348)), (' B 312  ILE  HB ', ' B 664  ILE HD11', -0.42, (236.639, 226.492, 206.199)), (' B 344  ALA  HB3', ' B 347  PHE  HE1', -0.42, (203.241, 237.358, 271.53)), (' C  25  PRO  HA ', ' C  26  PRO  HD3', -0.418, (161.72, 251.139, 238.785)), (' B 988  GLU  O  ', ' B 992  GLN  HG2', -0.418, (216.824, 203.694, 243.57)), (' A 353  TRP  CZ3', ' A 355  ARG  HB2', -0.418, (248.901, 198.963, 274.936)), (' C 605  SER  OG ', ' C 606  ASN  N  ', -0.417, (179.448, 238.752, 207.046)), (' B 959  LEU  HA ', ' B 959  LEU HD23', -0.417, (224.53, 201.832, 216.581)), (' A 315  THR HG22', ' A 316  SER  N  ', -0.417, (210.549, 183.324, 219.241)), (' B 234  ASN  HB2', ' B2002  NAG  C2 ', -0.415, (244.854, 217.342, 255.663)), (' C 103  GLY  N  ', ' C 241  LEU  HB2', -0.415, (178.822, 258.318, 248.405)), (' B1104  VAL HG13', ' B1115  ILE HG12', -0.415, (221.406, 223.768, 149.513)), (' B 425  LEU  HA ', ' B 425  LEU HD23', -0.414, (198.181, 226.794, 255.814)), (' B 142  ASP  OD2', ' B 158  ARG  NE ', -0.414, (276.014, 217.207, 258.861)), (' A 931  ILE  O  ', ' A 934  ILE HG22', -0.414, (191.54, 190.949, 180.343)), (' B 102  ARG  HG3', ' B 141  LEU HD22', -0.414, (272.565, 212.538, 250.021)), (' A 707  TYR  CD2', ' B 883  THR HG23', -0.414, (227.164, 189.806, 169.592)), (' B  46  SER  CA ', ' B 279  TYR  O  ', -0.414, (247.397, 202.516, 219.127)), (' A 350  VAL HG22', ' A 422  ASN  HB3', -0.413, (245.888, 196.578, 285.246)), (' B 352  ALA  HB1', ' B 466  ARG HH21', -0.413, (191.078, 235.218, 267.651)), (' A 341  VAL HG13', ' A 342  PHE  CD1', -0.413, (249.25, 187.48, 269.746)), (' A 991  VAL  O  ', ' A 995  ARG  HG2', -0.413, (203.035, 209.857, 238.694)), (' A 403  ARG  NH1', ' A 405  ASP  HB2', -0.413, (240.1, 188.128, 290.889)), (' B 367  VAL HG13', ' B 368  LEU HD22', -0.413, (215.97, 238.155, 264.465)), (' A 336  CYS  HB3', ' A 338  PHE  HE1', -0.412, (248.243, 187.748, 260.862)), (' B 168  PHE  CZ ', ' B 170  TYR  HB2', -0.411, (256.085, 202.323, 253.225)), (' C  96  GLU  HG2', ' C 101  ILE HG12', -0.411, (176.953, 261.462, 240.793)), (' B 164  ASN  OD1', ' B 165  ASN  N  ', -0.411, (256.741, 211.628, 266.98)), (' C 377  PHE  CD1', ' C 434  ILE HD12', -0.411, (192.608, 204.055, 262.794)), (' A 916  LEU HD12', ' A 923  ILE HD13', -0.41, (197.441, 196.317, 164.279)), (' A 168  PHE  CE2', ' A 170  TYR  HB2', -0.41, (181.74, 175.627, 253.904)), (' C 128  ILE  HB ', ' C 170  TYR  HB3', -0.409, (190.8, 255.069, 252.651)), (' B 766  ALA  O  ', ' B 770  ILE HG12', -0.409, (212.654, 199.136, 210.052)), (' B 475  ALA  HB3', ' B 487  ASN  HA ', -0.409, (175.768, 213.778, 270.461)), (' B 401  VAL HG22', ' B 509  ARG  HG2', -0.408, (202.085, 230.302, 273.166)), (' C  40  ASP  N  ', ' C  40  ASP  OD1', -0.408, (197.878, 243.401, 233.764)), (' B 137  ASN  OD1', ' B 138  ASP  N  ', -0.408, (268.829, 224.585, 258.216)), (' A 770  ILE  O  ', ' A 774  GLN  HG2', -0.407, (196.426, 213.653, 204.58)), (' A 212  LEU HD23', ' A 213  VAL  N  ', -0.407, (186.357, 154.084, 225.249)), (' A1079  PRO  HD2', ' A1131  GLY  O  ', -0.406, (229.796, 195.351, 154.599)), (' C1073  LYS  HB3', ' C1073  LYS  HE2', -0.406, (186.819, 222.38, 158.472)), (' B 409  GLN  NE2', ' B 417  LYS  H  ', -0.406, (195.564, 217.356, 265.381)), (' C 212  LEU HD23', ' C 213  VAL  N  ', -0.405, (173.359, 260.333, 224.915)), (' B 922  LEU  O  ', ' B 926  GLN  HG3', -0.405, (239.013, 208.104, 168.12)), (' C1082  CYS  SG ', ' C1132  ILE HD12', -0.405, (190.578, 199.774, 147.44)), (' C 396  TYR  HB2', ' C 514  SER  OG ', -0.405, (193.752, 191.653, 255.574)), (' A 352  ALA  HB1', ' A 466  ARG HH21', -0.405, (254.123, 198.081, 281.343)), (' C1145  LEU  HA ', ' C1145  LEU HD23', -0.405, (210.001, 213.812, 129.589)), (' B 733  LYS  HD2', ' B 771  ALA  HB1', -0.404, (217.267, 193.429, 206.653)), (' A 599  THR  HB ', ' A 608  VAL HG12', -0.404, (206.055, 176.284, 209.769)), (' C 664  ILE  O  ', ' C 671  CYS  HB2', -0.404, (182.944, 223.504, 200.46)), (' A1101  ASP  O  ', ' A1102  TRP  HB2', -0.404, (220.861, 191.387, 146.947)), (' C 560  LEU  O  ', ' C 562  PHE  N  ', -0.404, (177.142, 183.347, 234.553)), (' A 752  LEU  O  ', ' A 755  GLN  HG2', -0.403, (200.471, 220.609, 234.32)), (' C 290  ASP  OD1', ' C 291  CYS  N  ', -0.403, (184.939, 236.606, 225.273)), (' A 418  ILE  HB ', ' A 422  ASN  HB2', -0.403, (243.794, 196.754, 286.232)), (' C 578  ASP  N  ', ' C 578  ASP  OD1', -0.403, (171.671, 194.112, 236.629)), (' A1039  ARG  HG3', ' A1042  PHE  HB2', -0.402, (209.439, 205.722, 181.102)), (' A 640  SER  HG ', ' A 641  ASN  N  ', -0.402, (217.314, 166.657, 209.394)), (' C 928  ASN  O  ', ' C 931  ILE HG22', -0.401, (204.684, 240.32, 175.868)), (' C 524  VAL  O  ', ' C 524  VAL HG13', -0.401, (183.225, 195.418, 251.793)), (' C 746  SER  HB3', ' C 749  CYS  HB3', -0.401, (222.577, 225.91, 234.468)), (' B 417  LYS  O  ', ' B 421  TYR  HB2', -0.4, (190.426, 220.023, 264.087)), (' B 662  CYS  HB2', ' B 697  MET  HG3', -0.4, (233.905, 230.883, 194.526)), (' A  64  TRP  CH2', ' A 214  ARG  HD2', -0.4, (192.762, 151.248, 230.537)), (' A 189  LEU  HG ', ' A 208  THR  O  ', -0.4, (181.378, 162.692, 230.239))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
