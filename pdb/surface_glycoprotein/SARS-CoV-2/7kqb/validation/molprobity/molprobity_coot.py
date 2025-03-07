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
data['rama'] = [('B', ' 524 ', 'VAL', 0.09419906161429036, (205.4650000000003, 250.839, 253.22100000000012)), ('B', ' 527 ', 'PRO', 0.02651208497909417, (213.64100000000028, 254.22599999999997, 249.18400000000008)), ('C', ' 633 ', 'TRP', 0.00487873318798567, (176.9649999999999, 228.197, 219.824)), ('H', ' 200 ', 'TYR', 0.031151452497226357, (317.152, 191.06600000000012, 309.9000000000002)), ('L', ' 107 ', 'LEU', 0.017337459951139576, (286.27, 189.04100000000008, 314.12100000000015)), ('L', ' 108 ', 'GLY', 0.012104555996052035, (285.32800000000003, 185.91300000000012, 316.112)), ('L', ' 110 ', 'VAL', 0.00512602, (287.215, 184.119, 321.75500000000005)), ('L', ' 152 ', 'ASN', 0.046974852639684365, (311.266, 203.882, 338.177)), ('L', ' 210 ', 'ASN', 0.03979975059734212, (317.649, 200.2009999999999, 330.6440000000001))]
data['omega'] = [('J', '  95 ', 'PRO', None, (237.01700000000014, 170.0270000000001, 274.603)), ('L', '  95 ', 'PRO', None, (270.746, 219.316, 308.063))]
data['rota'] = [('A', '  81 ', 'ASN', 0.08516569103278113, (205.48900000000017, 153.937, 242.80600000000007)), ('A', ' 120 ', 'VAL', 0.24686108260471132, (189.89100000000013, 163.35, 246.87100000000004)), ('A', ' 156 ', 'GLU', 0.13792495050579706, (189.22800000000018, 151.313, 252.45200000000006)), ('A', ' 267 ', 'VAL', 0.06398202936803225, (203.20300000000017, 163.861, 234.311)), ('A', ' 298 ', 'GLU', 0.29292066613059153, (211.162, 182.352, 217.55400000000003)), ('A', ' 580 ', 'GLN', 0.12566500588724847, (253.32900000000018, 192.443, 237.4940000000001)), ('A', ' 597 ', 'VAL', 0.09122928499699554, (216.637, 183.081, 210.439)), ('A', ' 633 ', 'TRP', 0.14706666241788008, (217.16700000000003, 174.565, 218.821)), ('A', ' 703 ', 'ASN', 0.06871198929614211, (227.80600000000007, 185.60999999999996, 176.029)), ('A', ' 767 ', 'LEU', 0.18441849731361099, (199.95, 216.203, 209.947)), ('A', ' 935 ', 'GLN', 0.20149037688616567, (195.511, 189.845, 182.6630000000001)), ('A', ' 973 ', 'ILE', 0.0688902126594457, (203.29000000000013, 204.058, 238.76600000000005)), ('B', ' 153 ', 'MET', 0.12984298676142178, (283.905, 220.09, 246.95400000000004)), ('B', ' 267 ', 'VAL', 0.05498636553976582, (260.3260000000001, 230.829, 235.2110000000001)), ('B', ' 346 ', 'ARG', 0.08935460295430196, (204.6100000000003, 266.884, 271.5880000000002)), ('B', ' 753 ', 'LEU', 0.10609739590204285, (214.78900000000002, 200.221, 229.64500000000004)), ('B', ' 785 ', 'VAL', 0.27163075970428113, (222.232, 194.419, 181.58)), ('B', ' 935 ', 'GLN', 0.09343479966200524, (243.71800000000002, 209.534, 183.37300000000002)), ('C', '  66 ', 'HIS', 0.1314118252759023, (166.39300000000011, 253.44999999999996, 236.05800000000008)), ('C', '  78 ', 'ARG', 0.13383385340744158, (158.97200000000012, 254.582, 241.353)), ('C', ' 203 ', 'ILE', 0.26887609420788616, (188.4690000000003, 249.7, 238.652)), ('C', ' 267 ', 'VAL', 0.0638959119820379, (174.83400000000012, 245.84199999999998, 235.1410000000001)), ('C', ' 367 ', 'VAL', 0.2817005781668859, (189.45000000000013, 204.501, 261.54800000000006)), ('C', ' 572 ', 'THR', 0.07915132670867517, (191.967, 198.784, 226.44600000000003)), ('C', ' 739 ', 'THR', 0.07893161729663813, (224.123, 228.20099999999994, 223.4320000000001)), ('C', ' 753 ', 'LEU', 0.07914709289847396, (224.61900000000003, 222.434, 229.148)), ('C', ' 990 ', 'GLU', 0.2493707105072497, (220.05700000000013, 222.956, 239.06400000000002)), ('C', '1004 ', 'LEU', 0.08935778026622568, (215.692, 223.66, 218.9860000000001)), ('H', ' 158 ', 'VAL', 0.2264815838415213, (307.398, 198.25700000000012, 306.084)), ('H', ' 161 ', 'ASN', 0.19923202135737314, (314.198, 190.57300000000006, 305.876)), ('L', '  18 ', 'ARG', 0.2983565690304885, (271.76, 186.731, 315.0730000000001)), ('L', ' 104 ', 'LEU', 0.11241202829936474, (281.404, 194.92400000000006, 314.883)), ('L', ' 117 ', 'ILE', 0.13138028555148062, (307.685, 194.059, 325.8300000000001)), ('L', ' 154 ', 'LEU', 0.21556032458990476, (305.405, 205.53999999999996, 335.83)), ('L', ' 164 ', 'THR', 0.13754459965441065, (296.106, 196.28700000000012, 314.78700000000015)), ('L', ' 186 ', 'TYR', 0.14418678117428063, (316.881, 209.649, 327.498)), ('K', '  33 ', 'GLU', 0.06777784233149553, (222.52500000000015, 173.42100000000005, 272.4320000000002)), ('K', '  73 ', 'ASP', 0.11859817850794407, (213.38900000000015, 165.51200000000003, 273.1760000000001)), ('K', ' 111 ', 'GLN', 0.11726442890246982, (219.41300000000015, 173.24800000000008, 290.64300000000014)), ('K', ' 141 ', 'THR', 0.07497893269974187, (237.311, 176.0869999999999, 327.44400000000013)), ('K', ' 161 ', 'ASN', 0.2187281761215485, (220.25300000000016, 169.894, 324.859)), ('K', ' 184 ', 'LEU', 0.07715766748973193, (231.14900000000014, 164.195, 311.9420000000001)), ('K', ' 213 ', 'VAL', 0.2906935882190692, (219.63000000000017, 158.29400000000007, 319.032)), ('K', ' 214 ', 'ASP', 0.2450595369859673, (219.85500000000016, 161.45, 321.196)), ('J', ' 186 ', 'TYR', 0.21919565546931946, (244.38700000000014, 152.809, 322.785))]
data['cbeta'] = [('A', ' 158 ', 'ARG', ' ', 0.2619227890096975, (194.52800000000016, 152.22, 254.02100000000004)), ('A', ' 282 ', 'ASN', ' ', 0.2613960115740486, (182.971, 183.252, 220.6930000000001)), ('A', ' 540 ', 'ASN', ' ', 0.26189528539207446, (234.92600000000013, 189.961, 234.575)), ('A', ' 597 ', 'VAL', ' ', 0.2570127272657948, (215.726, 182.274, 211.3960000000001)), ('A', ' 977 ', 'LEU', ' ', 0.31172123968724647, (196.75800000000018, 209.33899999999994, 233.24100000000013)), ('B', '  20 ', 'THR', ' ', 0.26758394047369227, (279.863, 241.89299999999997, 247.0550000000001)), ('B', ' 590 ', 'CYS', ' ', 0.26236336151963224, (223.75100000000018, 245.489, 223.66700000000006)), ('B', ' 636 ', 'TYR', ' ', 0.3241985505478147, (242.44500000000016, 242.27399999999994, 215.53300000000002)), ('C', ' 571 ', 'ASP', ' ', 0.2511702048909519, (196.231, 196.017, 225.908)), ('C', ' 633 ', 'TRP', ' ', 0.2795059891346927, (177.8519999999999, 228.64299999999997, 218.6520000000001)), ('C', ' 950 ', 'ASP', ' ', 0.2602747113820356, (203.333, 229.289, 200.61200000000002)), ('L', ' 151 ', 'ASP', ' ', 0.2892155388401252, (314.44399999999996, 207.47799999999998, 336.4030000000002)), ('K', '  96 ', 'CYS', ' ', 0.25765351443679646, (220.45500000000015, 170.322, 283.5460000000001)), ('J', ' 151 ', 'ASP', ' ', 0.2734891987158081, (253.14400000000015, 156.325, 324.58800000000025))]
data['probe'] = [(' J 110  VAL HG22', ' J 111  ALA  H  ', -0.548, (240.863, 190.218, 313.15)), (' C 201  PHE  CD2', ' C 203  ILE HD11', -0.545, (187.515, 249.544, 243.038)), (' A 983  ARG  HD3', ' C 517  LEU HD13', -0.52, (196.402, 201.717, 244.13)), (' L 110  VAL HG22', ' L 111  ALA  H  ', -0.514, (289.373, 182.868, 322.165)), (' L 148  TRP  CZ3', ' L 194  CYS  SG ', -0.472, (305.921, 201.196, 327.223)), (' H 170  HIS  CE1', ' L 174  SER  HG ', -0.469, (299.56, 190.954, 315.664)), (' H 129  PRO  HB3', ' H 217  VAL HG22', -0.463, (315.394, 196.841, 311.932)), (' A 983  ARG  CD ', ' C 517  LEU HD13', -0.441, (196.401, 202.097, 243.816)), (' J 107  LEU  H  ', ' J 107  LEU HD12', -0.432, (234.129, 185.985, 303.75)), (' L 119  PRO  HA ', ' L 209  PHE  CD2', -0.432, (312.228, 198.884, 326.301)), (' J 118  PHE  CG ', ' J 119  PRO  HD2', -0.43, (238.387, 166.869, 325.067)), (' B 363  ALA  HB2', ' B 524  VAL HG12', -0.428, (207.402, 252.34, 254.801)), (' J 150  VAL HG22', ' J 192  TYR  CD2', -0.428, (246.668, 159.213, 322.444)), (' C 366  SER  HA ', ' C 369  TYR  CZ ', -0.424, (190.471, 207.009, 257.073)), (' H 170  HIS  CD2', ' L 137  ASN HD21', -0.42, (302.264, 189.611, 316.364)), (' K 144  LEU HD22', ' K 200  TYR  CG ', -0.419, (226.79, 169.374, 328.597)), (' A 404  GLY  HA2', ' A 508  TYR  CD1', -0.419, (253.212, 191.541, 282.334)), (' B 551  VAL HG23', ' B 590  CYS  HB2', -0.405, (223.93, 247.425, 223.841)), (' B 546  LEU  C  ', ' B 546  LEU HD23', -0.404, (212.915, 244.915, 233.499)), (' C 404  GLY  HA2', ' C 508  TYR  CD1', -0.403, (210.838, 202.665, 267.631)), (' B 669  GLY  HA2', ' C 869  MET  HE1', -0.4, (228.14, 238.566, 194.559))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
