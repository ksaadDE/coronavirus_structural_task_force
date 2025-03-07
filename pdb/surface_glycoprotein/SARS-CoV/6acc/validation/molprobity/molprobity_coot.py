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
data['rama'] = [('A', ' 632 ', 'GLN', 0.0027392645123282787, (159.98800000000003, 178.44, 202.884)), ('A', ' 691 ', 'ASN', 0.03183456710824357, (162.42700000000008, 183.894, 248.01700000000005)), ('A', ' 692 ', 'ASN', 0.004226385771693795, (165.19500000000008, 182.96, 250.477)), ('A', ' 797 ', 'ARG', 0.04659215851706502, (206.612, 163.838, 221.90900000000002)), ('A', ' 925 ', 'THR', 0.019919538497897123, (184.772, 165.041, 213.83800000000005)), ('A', '1072 ', 'PRO', 0.00904105, (178.52900000000005, 189.145, 256.04)), ('A', '1075 ', 'GLY', 0.08667307492808438, (181.0300000000001, 187.104, 249.561)), ('B', ' 632 ', 'GLN', 0.0026829322953327143, (215.19200000000006, 169.853, 202.892)), ('B', ' 691 ', 'ASN', 0.03193532511426322, (209.24900000000005, 169.232, 248.025)), ('B', ' 692 ', 'ASN', 0.004191753754573462, (208.67400000000006, 172.095, 250.485)), ('B', ' 925 ', 'THR', 0.020257280588441166, (214.403, 198.014, 213.84900000000005)), ('B', '1072 ', 'PRO', 0.00904105, (196.6500000000001, 180.549, 256.049)), ('B', '1075 ', 'GLY', 0.08678066523060651, (197.16700000000006, 183.736, 249.571)), ('C', ' 632 ', 'GLN', 0.002710822254741556, (195.04100000000005, 221.97, 202.888)), ('C', ' 691 ', 'ASN', 0.03185623856664023, (198.5440000000001, 217.11, 248.018)), ('C', ' 692 ', 'ASN', 0.004250865979626883, (196.35100000000006, 215.179, 250.477)), ('C', ' 925 ', 'THR', 0.019995355718391717, (171.045, 207.202, 213.83400000000003)), ('C', '1072 ', 'PRO', 0.00904105, (195.03900000000004, 200.537, 256.034)), ('C', '1075 ', 'GLY', 0.08725341828268193, (192.02200000000005, 199.394, 249.55500000000006))]
data['omega'] = [('A', ' 470 ', 'PRO', None, (180.40400000000005, 232.024, 136.421)), ('A', ' 528 ', 'ASN', None, (158.073, 183.922, 171.51)), ('A', ' 632 ', 'GLN', None, (159.96500000000006, 178.256, 204.339)), ('A', ' 727 ', 'ASP', None, (206.72400000000005, 176.395, 179.926)), ('A', '1075 ', 'GLY', None, (180.67200000000008, 188.469, 249.22200000000007)), ('B', ' 470 ', 'PRO', None, (158.58000000000007, 160.746, 136.427)), ('B', ' 528 ', 'ASN', None, (211.403, 165.456, 171.518)), ('B', ' 632 ', 'GLN', None, (215.364, 169.924, 204.347)), ('B', ' 727 ', 'ASP', None, (193.593, 211.351, 179.939)), ('B', '1075 ', 'GLY', None, (196.16300000000007, 182.744, 249.23100000000002)), ('C', ' 470 ', 'PRO', None, (231.24, 177.526, 136.406)), ('C', ' 528 ', 'ASN', None, (200.747, 220.901, 171.513)), ('C', ' 632 ', 'GLN', None, (194.893, 222.082, 204.343)), ('C', ' 727 ', 'ASP', None, (169.902, 182.528, 179.911)), ('C', '1075 ', 'GLY', None, (193.38300000000007, 199.021, 249.215))]
data['rota'] = [('A', ' 373 ', 'LYS', 0.25359838589076894, (168.23900000000006, 185.131, 161.53700000000003)), ('A', ' 699 ', 'ASN', 0.2558328975896347, (180.05300000000008, 168.263, 245.36900000000006)), ('A', ' 797 ', 'ARG', 0.11810517997088182, (206.612, 163.838, 221.90900000000002)), ('A', '1097 ', 'ILE', 0.09423454273001729, (179.10500000000002, 183.267, 262.966)), ('B', ' 373 ', 'LYS', 0.2534577222579418, (205.27200000000005, 173.657, 161.546)), ('B', ' 699 ', 'ASN', 0.25734680580719554, (213.97200000000007, 192.313, 245.38000000000005)), ('B', '1097 ', 'ILE', 0.09352932518472075, (201.453, 183.987, 262.975)), ('C', ' 373 ', 'LYS', 0.25291405441160775, (196.712, 211.497, 161.536)), ('C', ' 699 ', 'ASN', 0.2541520184644343, (176.19300000000007, 209.663, 245.366)), ('C', ' 797 ', 'ARG', 0.0, (159.2, 188.832, 222.05)), ('C', ' 805 ', 'PHE', 0.15140799025912444, (162.395, 195.107, 215.03700000000003)), ('C', '1097 ', 'ILE', 0.09562437960826722, (189.66100000000006, 202.97399999999996, 262.961))]
data['cbeta'] = [('C', ' 797 ', 'ARG', ' ', 0.2749756134399855, (159.462, 189.89, 221.028))]
data['probe'] = [(' A 797  ARG  NH1', ' A 805  PHE  HD2', -1.276, (203.684, 162.814, 216.12)), (' A 797  ARG  NH1', ' A 805  PHE  CD2', -1.149, (202.759, 163.478, 215.549)), (' C 797  ARG  NH1', ' C 805  PHE  CD1', -1.039, (159.459, 190.601, 215.016)), (' A 797  ARG  CZ ', ' A 805  PHE  CD2', -1.033, (204.366, 164.015, 215.765)), (' B 797  ARG  CZ ', ' B 805  PHE  HD2', -1.019, (206.471, 215.546, 215.984)), (' B 797  ARG  CZ ', ' B 805  PHE  CD2', -0.998, (205.857, 215.571, 215.871)), (' A 797  ARG  CZ ', ' A 805  PHE  HD2', -0.971, (204.196, 163.39, 216.391)), (' A 789  PRO  HB3', ' A 797  ARG  O  ', -0.957, (207.95, 163.732, 224.896)), (' A 797  ARG HH11', ' A 805  PHE  HD2', -0.927, (203.44, 162.679, 216.86)), (' A 789  PRO  CB ', ' A 797  ARG  O  ', -0.927, (207.857, 164.21, 224.676)), (' C 789  PRO  HB3', ' C 797  ARG  O  ', -0.914, (157.7, 188.452, 224.012)), (' C 797  ARG HH12', ' C 805  PHE  HD1', -0.903, (159.496, 192.158, 215.091)), (' B 797  ARG  NH2', ' B 805  PHE  HD2', -0.851, (207.166, 215.377, 216.447)), (' C 800  ILE  O  ', ' C 804  LEU  HG ', -0.81, (163.701, 196.423, 219.769)), (' A 797  ARG  CZ ', ' A 805  PHE  CE2', -0.789, (204.402, 164.971, 216.416)), (' C 789  PRO  CB ', ' C 797  ARG  O  ', -0.788, (158.787, 187.985, 224.78)), (' C 797  ARG  HG3', ' C 797  ARG  NH2', -0.786, (158.581, 190.559, 218.582)), (' A 797  ARG  NE ', ' A 805  PHE  CE2', -0.767, (204.531, 165.012, 217.181)), (' B 789  PRO  HB3', ' B 797  ARG  O  ', -0.758, (204.397, 218.893, 224.724)), (' C 797  ARG  NH1', ' C 805  PHE  CE1', -0.749, (159.545, 190.773, 214.447)), (' A 789  PRO  HG3', ' A 797  ARG  O  ', -0.715, (206.844, 164.881, 224.451)), (' C 797  ARG  HG3', ' C 797  ARG HH21', -0.711, (159.133, 190.533, 219.189)), (' A 789  PRO  CG ', ' A 797  ARG  O  ', -0.708, (207.152, 164.649, 224.936)), (' A 797  ARG  NE ', ' A 805  PHE  HE2', -0.661, (204.46, 165.109, 217.41)), (' C1060  ALA  HB2', ' C1080  ASN HD22', -0.657, (196.626, 212.018, 257.174)), (' B1060  ALA  HB2', ' B1080  ASN HD22', -0.652, (205.785, 173.316, 257.205)), (' C 348  CYS  SG ', ' C 349  VAL  N  ', -0.651, (209.468, 219.69, 154.932)), (' A 348  CYS  SG ', ' A 349  VAL  N  ', -0.648, (154.68, 192.552, 154.488)), (' B 348  CYS  SG ', ' B 349  VAL  N  ', -0.648, (205.677, 158.292, 154.467)), (' A1060  ALA  HB2', ' A1080  ASN HD22', -0.641, (167.746, 184.871, 257.229)), (' B 769  GLN HE21', ' C 685  SER  HB2', -0.636, (187.241, 220.105, 231.872)), (' A 685  SER  HB2', ' C 769  GLN HE21', -0.635, (165.503, 172.65, 231.819)), (' A1030  HIS  HE1', ' A1033  SER  HB2', -0.632, (193.38, 176.91, 231.027)), (' A 769  GLN HE21', ' B 685  SER  HB2', -0.629, (217.166, 178.032, 231.797)), (' B1030  HIS  HE1', ' B1033  SER  HB2', -0.628, (199.379, 200.082, 230.838)), (' B 987  GLN  NE2', ' C 988  THR  OG1', -0.624, (186.11, 193.286, 190.343)), (' C1030  HIS  HE1', ' C1033  SER  HB2', -0.62, (176.64, 193.398, 230.763)), (' B 797  ARG  CZ ', ' B 805  PHE  CE2', -0.62, (205.124, 214.916, 216.606)), (' A 797  ARG  NE ', ' A 805  PHE  CD2', -0.62, (204.09, 163.942, 217.494)), (' B  58  LEU  HB2', ' B 188  LYS  HE3', -0.618, (224.521, 197.6, 173.253)), (' B 302  THR HG23', ' B 581  VAL HG23', -0.612, (217.618, 184.761, 193.735)), (' A 575  PRO  O  ', ' C 835  GLN  NE2', -0.61, (158.815, 181.122, 188.277)), (' B  47  PHE  HB3', ' C 552  GLY  HA2', -0.609, (214.68, 215.222, 180.891)), (' C  58  LEU  HB2', ' C 188  LYS  HE3', -0.606, (166.412, 215.546, 172.852)), (' A  58  LEU  HB2', ' A 188  LYS  HE3', -0.605, (179.37, 156.783, 173.056)), (' A 302  THR HG23', ' A 581  VAL HG23', -0.605, (171.67, 168.837, 193.757)), (' C 302  THR HG23', ' C 581  VAL HG23', -0.601, (180.987, 215.985, 193.849)), (' A  47  PHE  HB3', ' B 552  GLY  HA2', -0.594, (199.754, 156.637, 180.855)), (' A 987  GLN  NE2', ' B 988  THR  OG1', -0.593, (194.797, 191.958, 190.266)), (' A 988  THR  OG1', ' C 987  GLN  NE2', -0.591, (190.002, 185.26, 190.525)), (' A 835  GLN  NE2', ' B 575  PRO  O  ', -0.59, (213.424, 167.443, 188.271)), (' B 895  GLN  HG3', ' C1074  GLU  HG2', -0.587, (198.097, 197.631, 250.468)), (' A 960  ASN  H  ', ' A 963  LEU HD13', -0.583, (203.1, 174.876, 173.733)), (' A 968  LYS  HG3', ' A 969  VAL HG23', -0.583, (203.294, 186.564, 163.256)), (' C 960  ASN  H  ', ' C 963  LEU HD13', -0.581, (170.373, 186.327, 173.791)), (' C 797  ARG  CG ', ' C 797  ARG HH21', -0.578, (159.402, 190.465, 219.41)), (' B 797  ARG  NH1', ' B 805  PHE  CD2', -0.578, (205.602, 215.551, 215.87)), (' B 968  LYS  HG3', ' B 969  VAL HG23', -0.576, (186.529, 202.761, 163.377)), (' A1074  GLU  HG2', ' C 895  GLN  HG3', -0.575, (179.504, 193.33, 250.509)), (' B 960  ASN  H  ', ' B 963  LEU HD13', -0.573, (196.473, 208.573, 173.456)), (' C 968  LYS  HG3', ' C 969  VAL HG23', -0.572, (180.431, 180.377, 163.256)), (' A 552  GLY  HA2', ' C  47  PHE  HB3', -0.572, (155.512, 198.506, 180.938)), (' A 895  GLN  HG3', ' B1074  GLU  HG2', -0.571, (193.138, 179.154, 250.349)), (' B 364  PHE  HD1', ' B 421  LEU HD13', -0.57, (196.646, 173.438, 150.106)), (' B1063  ILE  HB ', ' B1070  TYR  HB2', -0.57, (197.836, 176.033, 260.653)), (' A 364  PHE  HD1', ' A 421  LEU HD13', -0.569, (172.056, 192.908, 149.677)), (' C 364  PHE  HD1', ' C 421  LEU HD13', -0.566, (201.203, 204.173, 150.073)), (' C 804  LEU  O  ', ' C 805  PHE  C  ', -0.565, (163.221, 196.812, 214.319)), (' B 789  PRO  CB ', ' B 797  ARG  O  ', -0.565, (204.243, 218.204, 224.914)), (' B 797  ARG  CD ', ' B 805  PHE  HE2', -0.564, (204.35, 215.696, 217.646)), (' C1063  ILE  HB ', ' C1070  TYR  HB2', -0.564, (198.545, 203.403, 260.718)), (' A1063  ILE  HB ', ' A1070  TYR  HB2', -0.562, (174.214, 190.78, 260.814)), (' B 835  GLN  NE2', ' C 575  PRO  O  ', -0.56, (197.971, 221.744, 188.132)), (' C 707  GLU  OE2', ' C1010  LYS  NZ ', -0.556, (181.052, 196.701, 222.346)), (' B 138  PHE  HB2', ' B 236  THR  HA ', -0.554, (249.989, 207.235, 162.096)), (' B  38  ARG  NH1', ' B 184  GLU  OE2', -0.552, (237.557, 205.287, 182.13)), (' C 138  PHE  HB2', ' C 236  THR  HA ', -0.552, (145.575, 233.067, 161.673)), (' A 631  THR  O  ', ' A 633  ALA  N  ', -0.55, (161.606, 177.014, 203.42)), (' A 138  PHE  HB2', ' A 236  THR  HA ', -0.547, (175.031, 129.489, 162.083)), (' A  38  ARG  NH1', ' A 184  GLU  OE2', -0.547, (179.292, 141.26, 182.057)), (' B 385  ASP  HB2', ' B 498  VAL  HB ', -0.544, (188.416, 165.03, 152.59)), (' C 626  ASN  ND2', ' C 640  GLU  OE2', -0.543, (180.413, 233.201, 203.695)), (' C  38  ARG  NH1', ' C 184  GLU  OE2', -0.543, (153.048, 223.576, 181.598)), (' A 575  PRO  HG2', ' C 835  GLN  HG2', -0.541, (160.218, 183.34, 188.931)), (' B 340  TRP  O  ', ' B 453  ARG  NH1', -0.536, (183.677, 157.599, 149.967)), (' C 385  ASP  HB2', ' C 498  VAL  HB ', -0.536, (212.219, 200.942, 152.584)), (' A 385  ASP  HB2', ' A 498  VAL  HB ', -0.536, (169.69, 203.917, 152.575)), (' B 631  THR  O  ', ' B 633  ALA  N  ', -0.535, (215.667, 172.052, 203.41)), (' B 100  GLY  HA3', ' B 234  ILE  HB ', -0.532, (242.985, 204.787, 162.005)), (' A 196  VAL  HB ', ' A 220  PHE  HB2', -0.531, (186.025, 147.171, 166.341)), (' C 631  THR  O  ', ' C 633  ALA  N  ', -0.53, (192.948, 221.366, 203.386)), (' A 887  ARG  NH1', ' A1032  MET  SD ', -0.528, (197.195, 175.707, 236.805)), (' C 100  GLY  HA3', ' C 234  ILE  HB ', -0.528, (150.917, 228.151, 162.13)), (' C 196  VAL  HB ', ' C 220  PHE  HB2', -0.527, (155.0, 215.072, 166.3)), (' B 887  ARG  NH1', ' B1032  MET  SD ', -0.524, (198.976, 202.692, 236.673)), (' B 536  GLY  HA2', ' B 574  SER  HA ', -0.524, (211.18, 166.77, 182.148)), (' C 887  ARG  NH1', ' C1032  MET  SD ', -0.523, (174.708, 191.458, 236.679)), (' A 536  GLY  HA2', ' A 574  SER  HA ', -0.523, (159.253, 183.453, 182.201)), (' A 100  GLY  HA3', ' A 234  ILE  HB ', -0.522, (176.366, 136.873, 161.985)), (' B 626  ASN  ND2', ' B 640  GLU  OE2', -0.521, (232.188, 176.984, 203.738)), (' C 536  GLY  HA2', ' C 574  SER  HA ', -0.52, (199.169, 220.133, 181.984)), (' A 707  GLU  OE2', ' A1010  LYS  NZ ', -0.52, (188.962, 178.97, 222.445)), (' A 626  ASN  ND2', ' A 640  GLU  OE2', -0.517, (157.751, 160.013, 203.73)), (' B 745  LEU HD22', ' B 990  VAL HG21', -0.516, (189.212, 200.298, 193.434)), (' A 835  GLN  HG2', ' B 575  PRO  HG2', -0.515, (210.774, 167.207, 188.965)), (' C 745  LEU HD22', ' C 990  VAL HG21', -0.514, (181.682, 184.308, 193.399)), (' B 777  LYS  NZ ', ' B 790  ASP  OD1', -0.514, (206.585, 220.051, 230.193)), (' B 196  VAL  HB ', ' B 220  PHE  HB2', -0.513, (229.131, 207.978, 166.388)), (' A 444  ARG  NH1', ' A 447  LYS  O  ', -0.512, (177.025, 219.607, 156.27)), (' B 128  CYS  SG ', ' B 129  ASN  N  ', -0.509, (233.649, 201.044, 148.463)), (' A 745  LEU HD22', ' A 990  VAL HG21', -0.507, (199.005, 186.145, 193.244)), (' A 340  TRP  O  ', ' A 453  ARG  NH1', -0.506, (165.18, 211.939, 149.81)), (' A 128  CYS  SG ', ' A 129  ASN  N  ', -0.504, (178.299, 146.897, 148.347)), (' A 837  PHE  HB3', ' B 575  PRO  HD3', -0.504, (207.452, 169.127, 186.0)), (' C 128  CYS  SG ', ' C 129  ASN  N  ', -0.502, (158.592, 221.897, 148.335)), (' B 835  GLN  HG2', ' C 575  PRO  HG2', -0.501, (199.571, 219.057, 188.664)), (' C 445  HIS  HE1', ' C 462  PRO  HA ', -0.501, (228.133, 176.863, 151.853)), (' B 445  HIS  HE1', ' B 462  PRO  HA ', -0.501, (159.642, 163.929, 151.675)), (' B 194  LEU HD23', ' B 222  LEU HD12', -0.501, (229.11, 204.326, 161.641)), (' A 445  HIS  HE1', ' A 462  PRO  HA ', -0.5, (182.609, 229.55, 151.708)), (' C 340  TRP  O  ', ' C 453  ARG  NH1', -0.5, (221.403, 200.802, 150.022)), (' C 402  THR  HB ', ' C 407  ASP  HB2', -0.499, (213.34, 185.505, 154.691)), (' C 777  LYS  NZ ', ' C 790  ASP  OD1', -0.498, (155.99, 189.447, 230.115)), (' A 777  LYS  NZ ', ' A 790  ASP  OD1', -0.496, (207.72, 160.795, 230.22)), (' B 797  ARG  NH1', ' B 805  PHE  CE2', -0.496, (205.094, 215.494, 216.431)), (' B 402  THR  HB ', ' B 407  ASP  HB2', -0.495, (174.537, 172.196, 154.697)), (' A1061  PRO  HD2', ' A1113  GLY  H  ', -0.494, (167.162, 189.292, 254.729)), (' C 444  ARG  NH1', ' C 447  LYS  O  ', -0.492, (222.315, 186.488, 156.344)), (' C 796  LYS  HD2', ' C 850  ASP  HB3', -0.492, (158.864, 182.42, 218.843)), (' A 642  VAL  HB ', ' A 677  TYR  HB3', -0.492, (160.929, 164.874, 213.318)), (' B 707  GLU  OE2', ' B1010  LYS  NZ ', -0.491, (200.255, 194.801, 222.399)), (' C 194  LEU HD23', ' C 222  LEU HD12', -0.49, (158.349, 216.666, 161.775)), (' A 797  ARG  CD ', ' A 805  PHE  HE2', -0.49, (205.193, 165.2, 217.822)), (' A 575  PRO  HD3', ' C 837  PHE  HB3', -0.489, (162.738, 185.083, 185.962)), (' B1061  PRO  HD2', ' B1113  GLY  H  ', -0.489, (202.47, 170.178, 254.978)), (' B 323  CYS  N  ', ' B 348  CYS  SG ', -0.487, (204.824, 157.943, 152.364)), (' B 796  LYS  HD2', ' B 850  ASP  HB3', -0.487, (199.201, 220.783, 218.378)), (' B 642  VAL  HB ', ' B 677  TYR  HB3', -0.486, (226.046, 177.112, 213.584)), (' B 444  ARG  NH1', ' B 447  LYS  O  ', -0.486, (171.205, 163.818, 156.341)), (' A 402  THR  HB ', ' A 407  ASP  HB2', -0.486, (182.647, 212.355, 155.146)), (' B 529  PHE  HE2', ' B 562  VAL HG21', -0.482, (208.798, 159.977, 176.423)), (' A 194  LEU HD23', ' A 222  LEU HD12', -0.482, (182.472, 148.902, 161.885)), (' C 529  PHE  HE2', ' C 562  VAL HG21', -0.482, (206.629, 221.308, 176.523)), (' B 797  ARG  NH2', ' B 805  PHE  CD2', -0.481, (206.745, 214.772, 215.891)), (' A 962  ILE HG13', ' A 963  LEU HD12', -0.481, (200.975, 176.408, 171.932)), (' C1061  PRO  HD2', ' C1113  GLY  H  ', -0.481, (200.934, 210.564, 254.584)), (' B 962  ILE HG13', ' B 963  LEU HD12', -0.481, (196.223, 206.739, 172.01)), (' C 642  VAL  HB ', ' C 677  TYR  HB3', -0.48, (183.174, 227.634, 213.541)), (' B 837  PHE  HB3', ' C 575  PRO  HD3', -0.479, (199.393, 215.732, 185.907)), (' A 704  ILE HG12', ' A1047  VAL HG22', -0.479, (192.056, 169.002, 232.781)), (' A 529  PHE  HE2', ' A 562  VAL HG21', -0.478, (154.877, 188.938, 176.505)), (' B 704  ILE HG12', ' B1047  VAL HG22', -0.478, (206.919, 202.282, 233.093)), (' A 796  LYS  HD2', ' A 850  ASP  HB3', -0.477, (212.279, 166.809, 218.841)), (' C 323  CYS  N  ', ' C 348  CYS  SG ', -0.477, (210.49, 218.875, 152.361)), (' C  18  ARG  NE ', ' C  20  THR  OG1', -0.475, (148.548, 239.422, 149.89)), (' C 962  ILE HG13', ' C 963  LEU HD12', -0.475, (172.69, 187.551, 171.979)), (' A 848  THR  HB ', ' A 851  MET  HG2', -0.474, (212.677, 171.651, 214.955)), (' B 848  THR  HB ', ' B 851  MET  HG2', -0.474, (194.721, 219.123, 215.358)), (' C 127  ALA  HB3', ' C 161  PHE  HB3', -0.473, (157.85, 216.652, 153.529)), (' B  95  SER  H  ', ' B 181  HIS  CD2', -0.473, (247.589, 214.328, 173.572)), (' B 797  ARG  HD2', ' B 805  PHE  HE2', -0.472, (204.102, 215.297, 218.288)), (' A 267  ASP  OD1', ' A 271  THR  N  ', -0.472, (194.3, 149.75, 187.314)), (' A 953  GLY  O  ', ' A 977  ARG  NH1', -0.472, (189.641, 181.326, 171.783)), (' A 323  CYS  N  ', ' A 348  CYS  SG ', -0.471, (154.659, 193.209, 152.387)), (' C  95  SER  H  ', ' C 181  HIS  CD2', -0.471, (140.293, 227.877, 173.636)), (' B  94  LYS  NZ ', ' B 249  ALA  O  ', -0.47, (252.405, 207.045, 176.123)), (' B 953  GLY  O  ', ' B 977  ARG  NH1', -0.468, (197.734, 194.047, 171.901)), (' C 953  GLY  O  ', ' C 977  ARG  NH1', -0.467, (182.907, 194.909, 171.876)), (' A  95  SER  H  ', ' A 181  HIS  CD2', -0.465, (182.444, 128.484, 173.912)), (' C 848  THR  HB ', ' C 851  MET  HG2', -0.464, (162.854, 179.698, 215.409)), (' A 350  ALA  N  ', ' A 511  CYS  O  ', -0.464, (157.49, 190.224, 156.749)), (' C 185  PHE  HE1', ' C 198  LYS  HG3', -0.463, (150.205, 218.655, 172.555)), (' B 832  ILE  O  ', ' C 632  GLN  NE2', -0.463, (198.398, 223.721, 200.481)), (' C 704  ILE HG12', ' C1047  VAL HG22', -0.462, (170.988, 198.53, 233.013)), (' A  94  LYS  NZ ', ' A 249  ALA  O  ', -0.462, (173.681, 127.735, 176.287)), (' A 127  ALA  HB3', ' A 161  PHE  HB3', -0.461, (182.859, 148.682, 153.79)), (' A 185  PHE  HE1', ' A 198  LYS  HG3', -0.461, (185.275, 141.25, 172.607)), (' B 185  PHE  HE1', ' B 198  LYS  HG3', -0.461, (234.984, 210.583, 172.404)), (' B 127  ALA  HB3', ' B 161  PHE  HB3', -0.459, (229.447, 204.463, 153.774)), (' C 321  ASN  HB3', ' C 348  CYS  HA ', -0.459, (212.245, 221.146, 154.854)), (' C  94  LYS  NZ ', ' C 249  ALA  O  ', -0.459, (144.486, 235.931, 176.32)), (' A 948  LEU HD13', ' B 558  PHE  HZ ', -0.458, (199.483, 172.526, 185.48)), (' C 553  ARG  HG2', ' C 559  THR  HA ', -0.457, (208.463, 212.708, 180.863)), (' B 188  LYS  HB3', ' B 195  TYR  HB2', -0.457, (226.107, 202.012, 169.333)), (' C  33  HIS  HB2', ' C  66  VAL  HB ', -0.457, (159.573, 233.185, 181.202)), (' C 267  ASP  OD1', ' C 271  THR  N  ', -0.457, (152.988, 206.697, 187.329)), (' B 439  LYS  NZ ', ' B 480  ASP  OD1', -0.457, (173.26, 164.053, 135.823)), (' A 959  LEU HD23', ' A 962  ILE HD11', -0.456, (199.672, 177.222, 174.216)), (' C 959  LEU HD23', ' C 962  ILE HD11', -0.455, (174.182, 187.865, 174.56)), (' B  33  HIS  HB2', ' B  66  VAL  HB ', -0.455, (242.613, 195.008, 181.201)), (' A 321  ASN  HB3', ' A 348  CYS  HA ', -0.454, (151.663, 193.766, 154.778)), (' C 807  LYS  NZ ', ' C 920  LEU  O  ', -0.453, (164.57, 204.425, 217.649)), (' B 959  LEU HD23', ' B 962  ILE HD11', -0.453, (196.006, 205.082, 174.475)), (' B 646  TYR  HB2', ' B 677  TYR  CZ ', -0.452, (223.12, 181.264, 215.586)), (' C 598  TYR  HB2', ' C 635  CYS  HB2', -0.452, (187.86, 223.796, 196.164)), (' B  72  ILE HG13', ' B  74  HIS  H  ', -0.452, (258.483, 198.489, 171.198)), (' A 741  PHE  HD2', ' A 983  LEU HD21', -0.452, (198.939, 189.677, 184.88)), (' C 188  LYS  HB3', ' C 195  TYR  HB2', -0.452, (161.935, 215.681, 169.582)), (' C 789  PRO  CA ', ' C 797  ARG  O  ', -0.451, (158.215, 188.9, 225.573)), (' B 553  ARG  HG2', ' B 559  THR  HA ', -0.451, (200.456, 162.805, 180.898)), (' C 350  ALA  N  ', ' C 511  CYS  O  ', -0.451, (206.581, 218.133, 156.753)), (' B 720  CYS  SG ', ' B 746  ASN  ND2', -0.45, (186.146, 206.808, 190.733)), (' A  96  ASN  HA ', ' A 183  ARG HH12', -0.45, (181.245, 132.984, 170.423)), (' A 646  TYR  HB2', ' A 677  TYR  CZ ', -0.449, (165.901, 165.717, 215.488)), (' C  96  ASN  HA ', ' C 183  ARG HH12', -0.449, (144.624, 226.409, 170.213)), (' A 598  TYR  HB2', ' A 635  CYS  HB2', -0.448, (161.676, 171.084, 196.41)), (' C 646  TYR  HB2', ' C 677  TYR  CZ ', -0.447, (181.266, 223.268, 215.587)), (' C 720  CYS  SG ', ' C 746  ASN  ND2', -0.447, (177.603, 178.227, 190.603)), (' A 188  LYS  HB3', ' A 195  TYR  HB2', -0.446, (181.985, 152.969, 169.549)), (' A 832  ILE  O  ', ' B 632  GLN  NE2', -0.446, (214.825, 166.233, 200.703)), (' A 720  CYS  SG ', ' A 746  ASN  ND2', -0.445, (206.736, 185.346, 191.057)), (' B 598  TYR  HB2', ' B 635  CYS  HB2', -0.445, (220.821, 175.097, 196.399)), (' B1087  THR HG22', ' B1094  PRO  HA ', -0.445, (206.551, 186.562, 255.443)), (' B 741  PHE  HD2', ' B 983  LEU HD21', -0.443, (185.616, 197.837, 185.124)), (' A 553  ARG  HG2', ' A 559  THR  HA ', -0.443, (161.163, 194.304, 180.997)), (' C 777  LYS  NZ ', ' C 789  PRO  O  ', -0.442, (156.126, 188.667, 229.881)), (' B 321  ASN  HB3', ' B 348  CYS  HA ', -0.442, (205.803, 155.306, 154.941)), (' C  72  ILE HG13', ' C  74  HIS  H  ', -0.441, (148.526, 245.08, 171.209)), (' B 350  ALA  N  ', ' B 511  CYS  O  ', -0.441, (206.032, 161.883, 156.746)), (' A  33  HIS  HB2', ' A  66  VAL  HB ', -0.441, (168.103, 142.438, 180.867)), (' C 741  PHE  HD2', ' C 983  LEU HD21', -0.44, (185.503, 182.309, 185.054)), (' A  72  ILE HG13', ' A  74  HIS  H  ', -0.44, (163.036, 127.002, 171.477)), (' A 797  ARG  HD3', ' A 797  ARG HH21', -0.44, (206.933, 164.716, 217.268)), (' B  96  ASN  HA ', ' B 183  ARG HH12', -0.44, (244.216, 211.334, 170.222)), (' A1087  THR HG22', ' A1094  PRO  HA ', -0.44, (179.017, 177.385, 255.778)), (' C 439  LYS  NZ ', ' C 480  ASP  OD1', -0.439, (221.023, 188.563, 135.84)), (' B 678  THR  OG1', ' B 679  MET  N  ', -0.438, (220.214, 174.992, 215.25)), (' A 558  PHE  HZ ', ' C 948  LEU HD13', -0.438, (170.172, 190.685, 185.419)), (' C1087  THR HG22', ' C1094  PRO  HA ', -0.438, (184.776, 205.808, 255.761)), (' A 710  PRO  HB2', ' A1000  ILE HD11', -0.438, (193.973, 177.901, 211.997)), (' B 777  LYS  NZ ', ' B 789  PRO  O  ', -0.437, (205.882, 220.045, 229.893)), (' B 797  ARG  HD3', ' B 797  ARG HH11', -0.434, (203.674, 216.922, 217.074)), (' A 678  THR  OG1', ' A 679  MET  N  ', -0.433, (161.904, 171.358, 215.176)), (' A 632  GLN  NE2', ' C 832  ILE  O  ', -0.433, (156.905, 180.541, 200.601)), (' C  99  ARG  HD3', ' C 118  ASN  HB2', -0.432, (144.822, 224.444, 162.658)), (' C 804  LEU  N  ', ' C 804  LEU HD23', -0.432, (164.162, 198.452, 218.525)), (' B  18  ARG  NE ', ' B  20  THR  OG1', -0.431, (253.736, 201.431, 149.922)), (' C 209  LEU HD12', ' C 210  PRO  HD2', -0.431, (152.516, 228.711, 182.362)), (' A 209  LEU HD12', ' A 210  PRO  HD2', -0.431, (175.384, 138.261, 182.382)), (' B1068  LYS  HE2', ' B1104  VAL HG13', -0.431, (189.139, 174.374, 263.958)), (' A  99  ARG  HD3', ' A 118  ASN  HB2', -0.43, (182.586, 133.528, 162.558)), (' A 789  PRO  CA ', ' A 797  ARG  O  ', -0.43, (206.984, 163.009, 225.546)), (' A 626  ASN  ND2', ' A 639  ALA  O  ', -0.429, (158.75, 161.477, 203.748)), (' A1068  LYS  HE2', ' A1104  VAL HG13', -0.429, (177.317, 198.659, 263.731)), (' B 267  ASP  OD1', ' B 271  THR  N  ', -0.428, (222.675, 213.996, 187.313)), (' B 869  THR  OG1', ' C1089  ARG  NH1', -0.427, (187.152, 205.13, 241.256)), (' C1068  LYS  HE2', ' C1104  VAL HG13', -0.427, (203.94, 196.825, 263.682)), (' C 678  THR  OG1', ' C 679  MET  N  ', -0.427, (188.011, 223.801, 215.143)), (' B 209  LEU HD12', ' B 210  PRO  HD2', -0.426, (242.412, 203.471, 182.762)), (' C 626  ASN  ND2', ' C 639  ALA  O  ', -0.426, (181.209, 231.253, 203.987)), (' A 282  PRO  HB2', ' A 594  VAL HG21', -0.426, (170.039, 161.265, 196.319)), (' B 900  GLU  HG2', ' C1110  VAL HG21', -0.425, (208.829, 202.054, 255.063)), (' B  99  ARG  HD3', ' B 118  ASN  HB2', -0.425, (242.482, 212.185, 162.503)), (' C 103  PHE  HB2', ' C 114  VAL HG12', -0.425, (159.975, 222.428, 160.101)), (' C 797  ARG  HB3', ' C 801  GLU  OE1', -0.424, (161.145, 189.977, 221.196)), (' B 710  PRO  HB2', ' B1000  ILE HD11', -0.424, (198.844, 199.477, 211.9)), (' B 948  LEU HD13', ' C 558  PHE  HZ ', -0.423, (200.884, 207.285, 185.301)), (' A  18  ARG  NE ', ' A  20  THR  OG1', -0.423, (168.007, 129.36, 149.872)), (' C 710  PRO  HB2', ' C1000  ILE HD11', -0.422, (177.446, 192.884, 211.903)), (' B 103  PHE  HB2', ' B 114  VAL HG12', -0.422, (232.937, 200.298, 159.843)), (' B 626  ASN  ND2', ' B 639  ALA  O  ', -0.421, (230.403, 177.244, 203.602)), (' C 282  PRO  HB2', ' C 594  VAL HG21', -0.42, (175.278, 221.831, 196.44)), (' A 103  PHE  HB2', ' A 114  VAL HG12', -0.42, (177.127, 147.9, 160.066)), (' A1089  ARG  NH1', ' C 869  THR  OG1', -0.42, (178.502, 180.146, 241.189)), (' B 282  PRO  HB2', ' B 594  VAL HG21', -0.419, (225.119, 187.133, 196.281)), (' A 713  MET  HG2', ' A1000  ILE HG21', -0.417, (197.03, 180.296, 207.832)), (' B 966  LEU  HB2', ' B 971  ALA  HB2', -0.416, (193.484, 204.233, 166.858)), (' A 869  THR  OG1', ' B1089  ARG  NH1', -0.416, (204.216, 185.327, 241.361)), (' A  25  VAL  HA ', ' A  76  PHE  HB3', -0.415, (162.496, 131.586, 164.94)), (' B1097  ILE  H  ', ' B1097  ILE HG13', -0.414, (203.628, 183.922, 263.978)), (' B 317  PRO  HG3', ' B 565  PRO  HB3', -0.413, (207.475, 154.99, 167.284)), (' C 299  ILE HG12', ' C 584  ILE HG13', -0.413, (181.017, 217.591, 203.517)), (' A 469  PRO  HA ', ' A 471  ALA  H  ', -0.413, (181.1, 233.274, 138.53)), (' B  25  VAL  HA ', ' B  76  PHE  HB3', -0.412, (254.71, 195.103, 164.859)), (' A 966  LEU  HB2', ' A 971  ALA  HB2', -0.412, (200.54, 180.026, 166.919)), (' B 299  ILE HG12', ' B 584  ILE HG13', -0.411, (218.821, 184.194, 203.464)), (' A 114  VAL HG23', ' A 127  ALA  HB2', -0.41, (181.489, 147.738, 156.162)), (' B  94  LYS  HB2', ' B  94  LYS  HE2', -0.41, (251.696, 210.436, 173.958)), (' C 114  VAL HG23', ' C 127  ALA  HB2', -0.41, (157.614, 218.717, 156.112)), (' C 355  LEU  HA ', ' C 361  PHE  HE2', -0.409, (201.206, 208.482, 148.126)), (' A 355  LEU  HA ', ' A 361  PHE  HE2', -0.409, (168.388, 190.21, 148.288)), (' C  25  VAL  HA ', ' C  76  PHE  HB3', -0.408, (153.143, 243.282, 164.91)), (' B 114  VAL HG23', ' B 127  ALA  HB2', -0.408, (231.108, 203.817, 156.128)), (' C 713  MET  HG2', ' C1000  ILE HG21', -0.408, (178.09, 188.913, 207.87)), (' C 966  LEU  HB2', ' C 971  ALA  HB2', -0.407, (175.745, 186.155, 166.744)), (' A 700  PHE  HA ', ' A1051  PRO  HA ', -0.406, (180.891, 170.053, 241.371)), (' B 713  MET  HG2', ' B1000  ILE HG21', -0.404, (194.834, 200.662, 207.975)), (' B 355  LEU  HA ', ' B 361  PHE  HE2', -0.404, (200.778, 171.209, 148.329)), (' B1030  HIS  CE1', ' B1033  SER  HB2', -0.404, (199.713, 199.81, 231.661)), (' A 968  LYS  HG3', ' A 969  VAL  H  ', -0.404, (202.524, 185.696, 163.891)), (' B 700  PHE  HA ', ' B1051  PRO  HA ', -0.403, (211.784, 191.834, 241.227)), (' B 469  PRO  HA ', ' B 471  ALA  H  ', -0.403, (157.535, 160.665, 138.688)), (' A  99  ARG  HG3', ' A 138  PHE  HE2', -0.403, (178.646, 133.747, 162.442)), (' C 317  PRO  HG3', ' C 565  PRO  HB3', -0.403, (211.696, 222.886, 167.659)), (' A 900  GLU  HG2', ' B1110  VAL HG21', -0.402, (191.367, 167.648, 255.295)), (' A 299  ILE HG12', ' A 584  ILE HG13', -0.402, (170.514, 168.183, 203.409)), (' C 469  PRO  HA ', ' C 471  ALA  H  ', -0.402, (232.045, 176.338, 138.436)), (' C  99  ARG  HG3', ' C 138  PHE  HE2', -0.401, (147.119, 228.129, 162.476)), (' A1110  VAL HG21', ' C 900  GLU  HG2', -0.4, (169.892, 200.304, 254.519))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
