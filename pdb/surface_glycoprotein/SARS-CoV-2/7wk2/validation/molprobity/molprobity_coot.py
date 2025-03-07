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
data['omega'] = [('A', ' 157 ', 'PHE', None, (252.25400000000008, 175.935, 241.264)), ('A', ' 158 ', 'ARG', None, (254.55400000000012, 176.234, 238.44399999999996)), ('B', ' 157 ', 'PHE', None, (151.67000000000007, 161.672, 242.254)), ('B', ' 158 ', 'ARG', None, (150.8300000000001, 159.103, 239.81299999999996)), ('C', ' 157 ', 'PHE', None, (190.86500000000012, 254.266, 241.027)), ('C', ' 158 ', 'ARG', None, (189.3510000000001, 256.206, 238.334))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' B 405  ASP  O  ', ' B 408  ARG  NH1', -0.843, (206.631, 200.01, 246.82)), (' B 787  GLN  NE2', ' C 701  ALA  O  ', -0.826, (176.2, 217.621, 158.544)), (' B 200  TYR  OH ', ' C 516  GLU  OE2', -0.802, (172.284, 184.698, 231.483)), (' C  14  GLN  O  ', ' C 158  ARG  NH1', -0.796, (183.329, 255.32, 239.591)), (' B 273  ARG  NH2', ' B 292  ALA  O  ', -0.784, (176.314, 167.971, 205.337)), (' B 310  LYS  NZ ', ' B 663  ASP  OD2', -0.766, (176.842, 171.389, 177.62)), (' A 561  PRO  O  ', ' A 577  ARG  NH1', -0.756, (213.536, 234.006, 219.036)), (' C  96  GLU  OE1', ' C 190  ARG  NH2', -0.746, (194.982, 253.451, 219.729)), (' C 340  GLU  O  ', ' C 344  ALA  HB2', -0.736, (172.011, 190.66, 250.557)), (' C 561  PRO  O  ', ' C 577  ARG  NH1', -0.712, (157.797, 192.252, 219.782)), (' B 879  ALA  O  ', ' B 883  THR  OG1', -0.695, (175.236, 206.618, 152.67)), (' A 310  LYS  NZ ', ' A 663  ASP  OD2', -0.667, (229.547, 191.696, 177.188)), (' C 813  SER  OG ', ' C 868  GLU  OE2', -0.666, (220.924, 218.445, 170.894)), (' B 758  SER  OG ', ' C 965  GLN  NE2', -0.665, (197.79, 211.06, 200.94)), (' A 813  SER  OG ', ' A 868  GLU  OE2', -0.665, (204.315, 164.841, 171.15)), (' A  97  LYS  O  ', ' A 188  ASN  ND2', -0.664, (250.231, 166.378, 216.591)), (' B 344  ALA  HB3', ' B 347  PHE  HE1', -0.659, (215.586, 179.725, 251.466)), (' B 375  PHE  O  ', ' C 408  ARG  NH2', -0.659, (200.299, 186.93, 246.324)), (' C 883  THR  O  ', ' C 901  GLN  NE2', -0.657, (214.145, 208.554, 147.759)), (' B  32  PHE  CD2', ' B  33  THR HG23', -0.653, (164.48, 167.983, 201.675)), (' C 563  GLN  NE2', ' C 565  PHE  O  ', -0.647, (164.562, 192.569, 214.311)), (' A 408  ARG  NH2', ' C 375  PHE  O  ', -0.639, (188.788, 200.515, 246.332)), (' A  32  PHE  HD2', ' A  33  THR HG23', -0.639, (240.677, 181.34, 201.433)), (' B 340  GLU  O  ', ' B 344  ALA  HB2', -0.639, (215.571, 177.597, 250.95)), (' C 310  LYS  NZ ', ' C 663  ASP  OD2', -0.637, (185.189, 227.03, 177.276)), (' A1135  ASN  OD1', ' A1136  THR  N  ', -0.632, (212.544, 206.34, 121.867)), (' C  34  ARG  NH2', ' C 218  GLN  O  ', -0.626, (194.164, 247.283, 205.601)), (' B 457  ARG  NH1', ' B 459  SER  OG ', -0.624, (226.593, 201.38, 237.444)), (' A  96  GLU  OE1', ' A 190  ARG  NH2', -0.622, (249.212, 171.89, 219.942)), (' A 125  ASN  OD1', ' A 172  SER  OG ', -0.618, (237.696, 165.55, 229.566)), (' A 879  ALA  O  ', ' A 883  THR  OG1', -0.615, (199.115, 172.078, 152.644)), (' B 981  PHE  O  ', ' C 386  LYS  NZ ', -0.611, (180.748, 205.552, 224.568)), (' B  67  VAL HG23', ' B  79  PHE  CD1', -0.609, (152.27, 154.14, 223.919)), (' B 439  ASN  O  ', ' B 443  SER  OG ', -0.606, (207.719, 189.474, 261.351)), (' B1012  LEU  CD2', ' C1013  ILE HD13', -0.606, (195.859, 200.919, 188.36)), (' C 951  VAL  O  ', ' C 955  ASN  ND2', -0.605, (205.371, 211.07, 184.254)), (' B 905  ARG  NH1', ' B1049  LEU  O  ', -0.603, (183.233, 197.137, 151.86)), (' A 787  GLN  NE2', ' B 701  ALA  O  ', -0.602, (189.458, 167.535, 159.741)), (' A 287  ASP  OD1', ' A 288  ALA  N  ', -0.6, (231.49, 179.609, 201.152)), (' C1135  ASN  OD1', ' C1136  THR  N  ', -0.598, (178.735, 205.088, 121.689)), (' B  43  PHE  CB ', ' C 563  GLN HE22', -0.598, (164.163, 191.726, 212.162)), (' B 287  ASP  OD1', ' B 288  ALA  N  ', -0.598, (165.735, 175.925, 202.033)), (' B1135  ASN  OD1', ' B1136  THR  N  ', -0.597, (198.013, 176.047, 121.81)), (' B  43  PHE  HB2', ' C 563  GLN HE22', -0.591, (163.74, 191.477, 212.272)), (' B 813  SER  OG ', ' B 868  GLU  OE2', -0.59, (165.899, 205.669, 171.637)), (' A  32  PHE  CD2', ' A  33  THR HG23', -0.59, (240.103, 181.726, 201.397)), (' A 951  VAL  O  ', ' A 955  ASN  ND2', -0.587, (205.974, 182.24, 184.49)), (' A 157  PHE  HB2', ' A 158  ARG  HA ', -0.577, (254.253, 178.198, 239.754)), (' A 961  THR HG21', ' C 762  GLN  NE2', -0.572, (209.173, 188.294, 197.373)), (' C 287  ASP  OD1', ' C 288  ALA  N  ', -0.572, (195.286, 235.065, 201.162)), (' B  96  GLU  OE1', ' B 190  ARG  NH2', -0.57, (150.472, 164.876, 221.077)), (' B 436  TRP  O  ', ' B 509  ARG  N  ', -0.566, (208.468, 187.531, 251.477)), (' C 451  TYR  C  ', ' C 452  LEU HD12', -0.564, (184.694, 179.046, 256.512)), (' C  67  VAL HG23', ' C  79  PHE  HD1', -0.558, (183.772, 257.299, 223.322)), (' B  34  ARG  NH1', ' B 191  GLU  OE2', -0.557, (157.682, 168.445, 210.036)), (' C 645  THR  OG1', ' C 648  GLY  O  ', -0.556, (170.832, 217.557, 186.529)), (' C 905  ARG  NH1', ' C1049  LEU  O  ', -0.555, (204.319, 207.626, 151.931)), (' B 742  ILE  O  ', ' B1000  ARG  NH1', -0.555, (182.945, 202.468, 209.008)), (' B 762  GLN  NE2', ' C 961  THR HG21', -0.554, (199.195, 210.6, 197.133)), (' A 415  THR HG21', ' C 369  TYR  CE1', -0.551, (184.072, 205.345, 237.354)), (' C 344  ALA  HB3', ' C 347  PHE  HE1', -0.549, (174.297, 190.074, 252.276)), (' A 555  SER  OG ', ' A 586  ASP  OD1', -0.548, (219.18, 228.676, 208.649)), (' C 567  ARG  NH1', ' C 571  ASP  O  ', -0.546, (174.088, 195.385, 213.085)), (' A 122  ASN  ND2', ' A 124  THR  OG1', -0.544, (243.967, 163.302, 231.9)), (' B 157  PHE  HB2', ' B 158  ARG  HA ', -0.54, (152.575, 158.23, 240.852)), (' A 916  LEU  O  ', ' A 920  GLN  N  ', -0.54, (212.371, 179.84, 139.408)), (' B 391  CYS  HA ', ' B 525  CYS  HB3', -0.539, (209.659, 172.033, 230.415)), (' C 411  ALA  HB3', ' C 414  GLN  CG ', -0.537, (192.592, 188.12, 237.206)), (' A  43  PHE  HB2', ' B 563  GLN HE22', -0.535, (219.371, 170.108, 212.083)), (' C 879  ALA  O  ', ' C 883  THR  OG1', -0.534, (217.315, 209.723, 152.12)), (' A 905  ARG  NH1', ' A1050  MET  SD ', -0.522, (204.936, 179.978, 151.158)), (' A 543  PHE  CE2', ' A 576  VAL HG11', -0.519, (219.977, 223.041, 216.105)), (' B 117  LEU HD13', ' B 130  VAL  CG2', -0.512, (162.897, 173.209, 234.302)), (' C 407  VAL HG11', ' C 508  TYR  HD2', -0.51, (189.925, 191.574, 249.563)), (' C 578  ASP  OD2', ' C 581  THR  OG1', -0.51, (155.886, 202.938, 221.693)), (' A 439  ASN  O  ', ' A 443  SER  OG ', -0.51, (200.127, 210.564, 261.903)), (' C 188  ASN  OD1', ' C 207  HIS  NE2', -0.509, (200.723, 253.212, 215.596)), (' B 916  LEU  O  ', ' B 920  GLN  N  ', -0.506, (175.236, 190.636, 139.617)), (' B 559  PHE  CD2', ' B 584  ILE HG21', -0.505, (217.592, 164.394, 212.111)), (' A 570  ALA  HB2', ' C 856  LYS  HE2', -0.504, (210.553, 216.545, 203.837)), (' B 559  PHE  CE2', ' B 584  ILE HG21', -0.501, (217.063, 163.94, 212.199)), (' C 916  LEU  O  ', ' C 920  GLN  N  ', -0.5, (202.918, 218.264, 139.417)), (' C 391  CYS  HA ', ' C 525  CYS  HB3', -0.5, (170.485, 199.931, 231.157)), (' A 324  GLU  H  ', ' A 539  VAL HG12', -0.5, (230.47, 214.762, 214.561)), (' B 645  THR  OG1', ' B 648  GLY  O  ', -0.499, (193.341, 162.919, 186.651)), (' A 340  GLU  O  ', ' A 344  ALA  HB2', -0.499, (206.845, 223.179, 250.464)), (' B 951  VAL  O  ', ' B 955  ASN  ND2', -0.494, (180.388, 196.508, 184.72)), (' A 965  GLN  NE2', ' C 758  SER  OG ', -0.493, (209.686, 188.876, 201.585)), (' A 415  THR  OG1', ' A 420  ASP  OD1', -0.493, (184.395, 208.677, 239.082)), (' C 403  ARG  O  ', ' C 407  VAL HG13', -0.492, (191.189, 188.716, 249.913)), (' C 555  SER  OG ', ' C 586  ASP  OD1', -0.483, (159.959, 199.858, 209.678)), (' C  99  ASN  OD1', ' C 190  ARG  NH1', -0.48, (196.973, 252.912, 221.268)), (' A 391  CYS  HA ', ' A 525  CYS  HB3', -0.48, (214.568, 219.254, 230.518)), (' C1091  ARG  NE ', ' C1118  ASP  O  ', -0.477, (192.452, 198.548, 129.336)), (' A1028  LYS  O  ', ' A1032  CYS  N  ', -0.476, (199.643, 186.216, 160.279)), (' C 634  ARG  O  ', ' C 637  SER  OG ', -0.476, (170.592, 228.125, 198.543)), (' C 631  PRO  O  ', ' C 634  ARG  NH1', -0.476, (174.96, 224.077, 202.871)), (' B1012  LEU HD21', ' C1013  ILE HD13', -0.474, (195.931, 201.325, 188.171)), (' A 983  ARG  HG2', ' B 390  LEU HD11', -0.472, (205.28, 178.429, 226.755)), (' B 631  PRO  O  ', ' B 634  ARG  NH1', -0.47, (184.131, 163.237, 202.539)), (' C  65  PHE  HE2', ' C  84  LEU HD11', -0.467, (181.637, 246.377, 221.766)), (' A 665  PRO  HB2', ' C 864  LEU HD13', -0.467, (222.516, 201.962, 179.804)), (' A 598  ILE HG23', ' A 664  ILE HG21', -0.466, (227.656, 196.685, 184.123)), (' A 454  ARG  NH1', ' A 469  SER  O  ', -0.466, (181.467, 223.481, 248.113)), (' B 880  GLY  O  ', ' B 884  SER  N  ', -0.466, (178.29, 206.237, 151.699)), (' A 125  ASN  ND2', ' A 172  SER  O  ', -0.466, (236.554, 163.731, 231.417)), (' B 559  PHE  HD2', ' B 584  ILE HD13', -0.463, (218.469, 164.038, 213.45)), (' C 157  PHE  HB2', ' C 158  ARG  HA ', -0.462, (187.804, 255.092, 239.64)), (' B 978  ASN  O  ', ' B 982  SER  N  ', -0.458, (179.597, 203.599, 221.438)), (' C  83  VAL HG12', ' C 237  ARG  HB3', -0.458, (180.145, 241.535, 229.054)), (' B1028  LYS  O  ', ' B1032  CYS  N  ', -0.458, (186.998, 199.121, 160.224)), (' C 802  PHE  CE2', ' C 882  ILE HG23', -0.456, (212.692, 215.541, 151.284)), (' B  67  VAL HG23', ' B  79  PHE  CE1', -0.455, (152.893, 154.684, 224.537)), (' A 610  VAL HG21', ' A 633  TRP  CH2', -0.455, (233.072, 199.944, 194.856)), (' A 457  ARG  NH1', ' A 459  SER  OG ', -0.452, (179.812, 219.544, 238.075)), (' B 598  ILE HG23', ' B 664  ILE HG21', -0.45, (182.412, 170.229, 184.45)), (' C 122  ASN  O  ', ' C 123  ALA  HB3', -0.449, (201.946, 256.337, 227.596)), (' C 543  PHE  CD2', ' C 576  VAL HG21', -0.449, (164.141, 202.863, 217.248)), (' B 543  PHE  CE2', ' B 576  VAL HG21', -0.447, (209.219, 164.82, 216.688)), (' C 422  ASN  O  ', ' C 461  LEU HD23', -0.445, (185.031, 177.154, 242.203)), (' B 436  TRP  N  ', ' B 509  ARG  O  ', -0.445, (207.696, 185.892, 249.362)), (' C  17  ASN  OD1', ' C 158  ARG  NH2', -0.445, (180.166, 254.869, 235.847)), (' B1082  CYS  N  ', ' B1133  VAL  O  ', -0.444, (203.537, 175.66, 125.484)), (' A 200  TYR  OH ', ' B 516  GLU  OE2', -0.443, (220.687, 180.526, 230.254)), (' B  96  GLU  O  ', ' B 188  ASN  HB2', -0.443, (147.458, 166.494, 216.594)), (' B 986  PRO  N  ', ' B 987  PRO  HD2', -0.443, (189.267, 205.667, 226.933)), (' C 902  MET  HE1', ' C 923  ILE HG21', -0.442, (203.107, 216.55, 145.903)), (' B  83  VAL HG12', ' B 237  ARG  HD3', -0.442, (168.027, 158.167, 230.111)), (' B 563  GLN  O  ', ' B 577  ARG  NH1', -0.441, (220.198, 166.04, 218.965)), (' A 904  TYR  OH ', ' B1094  VAL HG12', -0.44, (197.259, 181.033, 138.583)), (' C 435  ALA  HA ', ' C 509  ARG  O  ', -0.44, (183.98, 193.443, 248.409)), (' C 986  PRO  N  ', ' C 987  PRO  HD2', -0.44, (209.289, 200.093, 226.89)), (' B  65  PHE  HE2', ' B  84  LEU HD11', -0.439, (162.963, 157.943, 222.364)), (' A 645  THR  OG1', ' A 648  GLY  O  ', -0.439, (229.257, 208.852, 186.317)), (' B 375  PHE  HD2', ' B 376  THR  HG1', -0.438, (203.066, 189.109, 248.089)), (' B 117  LEU HD13', ' B 130  VAL HG22', -0.437, (163.05, 172.648, 234.787)), (' B 372  ALA  HB2', ' B 377  PHE  HE2', -0.437, (198.975, 180.391, 245.244)), (' C 324  GLU  H  ', ' C 539  VAL HG12', -0.435, (166.254, 216.099, 215.855)), (' C 365  TYR  HH ', ' C 392  PHE  HE2', -0.435, (173.292, 197.792, 235.334)), (' B 411  ALA  HB1', ' B 412  PRO  HD2', -0.433, (208.161, 193.187, 236.016)), (' A 158  ARG  NH2', ' A 255  SER  O  ', -0.432, (261.753, 176.179, 236.055)), (' A 986  PRO  N  ', ' A 987  PRO  HD2', -0.431, (195.245, 185.009, 226.832)), (' A 880  GLY  O  ', ' A 884  SER  N  ', -0.43, (198.078, 174.943, 152.171)), (' A1082  CYS  N  ', ' A1133  VAL  O  ', -0.429, (210.941, 211.893, 125.572)), (' C 194  PHE  HE1', ' C 203  ILE HG23', -0.427, (196.289, 241.093, 222.186)), (' B 122  ASN  O  ', ' B 123  ALA  HB3', -0.426, (144.146, 169.788, 231.194)), (' C 522  ALA  HB3', ' C 544  ASN  OD1', -0.426, (167.705, 197.583, 227.165)), (' B 344  ALA  HB3', ' B 347  PHE  CE1', -0.426, (215.434, 180.261, 251.567)), (' B 597  VAL HG12', ' B 610  VAL HG22', -0.426, (182.531, 166.5, 193.932)), (' B 731  MET  N  ', ' B 774  GLN  OE1', -0.425, (183.796, 201.481, 180.703)), (' A 869  MET  CE ', ' B 699  LEU HD21', -0.425, (193.01, 169.014, 171.327)), (' A 109  THR  OG1', ' A 111  ASP  OD1', -0.425, (242.48, 189.421, 239.515)), (' C  99  ASN  OD1', ' C 190  ARG  NH2', -0.425, (195.777, 253.278, 221.064)), (' C 154  GLU  N  ', ' C 154  GLU  OE1', -0.424, (198.021, 257.766, 234.126)), (' B 864  LEU HD13', ' C 665  PRO  HB2', -0.424, (179.805, 215.257, 179.994)), (' B 215  ASP  O  ', ' B 266  TYR  OH ', -0.423, (156.462, 158.641, 210.557)), (' B 410  ILE  O  ', ' B 411  ALA  HB2', -0.422, (208.106, 193.433, 239.289)), (' B1091  ARG  NE ', ' B1120  THR  O  ', -0.422, (200.254, 189.444, 128.081)), (' B 533  LEU HD21', ' B 585  LEU  CD1', -0.422, (209.245, 158.281, 215.336)), (' C 216  LEU HD12', ' C 217  PRO  HD2', -0.421, (186.94, 248.098, 208.21)), (' B 376  THR  HB ', ' B 435  ALA  HB3', -0.42, (205.108, 188.179, 246.652)), (' B 194  PHE  HE1', ' B 203  ILE HG23', -0.42, (160.449, 172.591, 223.461)), (' A 744  GLY  O  ', ' A 745  ASP  HB2', -0.419, (198.791, 173.038, 210.912)), (' A1116  THR  O  ', ' A1120  THR HG22', -0.419, (204.626, 202.624, 125.514)), (' B  20  THR  O  ', ' B  79  PHE  N  ', -0.417, (154.255, 148.496, 224.049)), (' C 376  THR  HB ', ' C 435  ALA  HB3', -0.417, (187.426, 196.003, 246.537)), (' A 758  SER  OG ', ' B 965  GLN  NE2', -0.416, (184.968, 190.322, 201.989)), (' B 985  ASP  OD1', ' C 383  SER  OG ', -0.415, (184.409, 203.643, 230.095)), (' A 474  GLN  NE2', ' A 478  LYS  O  ', -0.415, (164.818, 220.571, 248.54)), (' C 338  PHE  CE2', ' C 363  ALA  HB1', -0.415, (171.616, 199.315, 240.152)), (' B  83  VAL HG22', ' B 239  GLN HE21', -0.414, (163.451, 156.913, 231.727)), (' B 645  THR  N  ', ' B 648  GLY  O  ', -0.413, (193.029, 161.276, 186.423)), (' C 543  PHE  CE2', ' C 576  VAL HG21', -0.413, (164.069, 202.862, 216.682)), (' A 154  GLU  N  ', ' A 154  GLU  OE1', -0.412, (251.259, 167.713, 234.997)), (' B 188  ASN  OD1', ' B 207  HIS  NE2', -0.411, (147.653, 170.962, 216.41)), (' B 454  ARG  NH2', ' B 469  SER  O  ', -0.411, (229.171, 197.221, 248.051)), (' B 543  PHE  CD2', ' B 576  VAL HG21', -0.409, (209.29, 165.014, 217.287)), (' A 543  PHE  CD2', ' A 576  VAL HG11', -0.409, (219.585, 223.086, 216.568)), (' C 449  TYR  O  ', ' C 452  LEU HD11', -0.409, (184.132, 178.032, 258.689)), (' B 945  LEU  O  ', ' B 948  LEU  N  ', -0.408, (178.055, 191.005, 176.848)), (' B 744  GLY  O  ', ' B 745  ASP  HB2', -0.408, (176.693, 208.148, 210.896)), (' A 350  VAL HG23', ' A 351  TYR  N  ', -0.408, (189.536, 218.181, 247.641)), (' A 108  THR  O  ', ' A 237  ARG  NH2', -0.408, (243.275, 191.594, 233.777)), (' A 576  VAL HG22', ' A 577  ARG  N  ', -0.405, (217.667, 226.017, 217.398)), (' B 374  PHE  HA ', ' B 436  TRP  HD1', -0.404, (203.888, 182.405, 251.02)), (' A 699  LEU HD21', ' C 869  MET  CE ', -0.404, (222.935, 206.325, 170.565)), (' C 375  PHE  H  ', ' C 436  TRP  HA ', -0.404, (185.24, 198.454, 250.252)), (' C 102  ARG  NH2', ' C 121  ASN  O  ', -0.403, (198.145, 254.915, 229.053)), (' C 744  GLY  O  ', ' C 745  ASP  HB2', -0.403, (217.443, 209.661, 210.207)), (' A 553  THR  O  ', ' A 586  ASP  N  ', -0.402, (221.909, 226.893, 209.644)), (' A 597  VAL HG12', ' A 610  VAL HG22', -0.402, (230.659, 198.458, 193.146)), (' B 894  LEU HD23', ' C1072  GLU  CD ', -0.401, (183.218, 214.366, 146.484)), (' A  83  VAL HG22', ' A 239  GLN HE21', -0.401, (248.908, 187.698, 230.737)), (' B 372  ALA  HB2', ' B 377  PHE  CE2', -0.401, (199.049, 180.709, 245.399)), (' C 454  ARG  NH1', ' C 469  SER  O  ', -0.4, (184.068, 169.869, 248.585))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
