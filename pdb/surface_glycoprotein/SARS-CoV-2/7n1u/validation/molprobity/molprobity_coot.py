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
data['rama'] = [('A', ' 381 ', 'GLY', 0.03448814719322107, (193.376, 183.057, 168.132)), ('A', ' 744 ', 'GLY', 0.00514628, (212.086, 212.76400000000004, 186.633)), ('B', '  32 ', 'PHE', 0.037700955748812236, (193.1740000000001, 244.48000000000002, 192.047)), ('B', ' 381 ', 'GLY', 0.041048270066277134, (213.381, 201.336, 168.064)), ('B', ' 744 ', 'GLY', 0.018361616827797484, (178.068, 202.671, 186.697)), ('B', ' 855 ', 'PHE', 0.011066848791776008, (175.827, 207.884, 191.075)), ('C', ' 148 ', 'ASN', 0.013527543179707856, (143.37299999999988, 140.106, 170.636)), ('C', ' 855 ', 'PHE', 0.008786372644386536, (200.554, 174.053, 191.14600000000002))]
data['omega'] = []
data['rota'] = [('A', '  21 ', 'ARG', 0.12174257665365912, (257.472, 165.188, 170.929)), ('A', '  87 ', 'ASN', 0.016400132571830407, (232.52100000000002, 177.841, 173.01)), ('A', ' 109 ', 'THR', 0.03572430664269998, (237.697, 175.136, 159.552)), ('A', ' 125 ', 'ASN', 0.12192136554555266, (254.878, 194.397, 167.117)), ('A', ' 136 ', 'CYS', 0.16607431863655497, (250.037, 174.947, 158.39)), ('A', ' 137 ', 'ASN', 0.21380978954134686, (249.125, 171.5, 159.797)), ('A', ' 159 ', 'VAL', 0.03898720307720259, (251.82999999999998, 179.826, 160.445)), ('A', ' 241 ', 'LEU', 0.1076828228552333, (251.25, 178.899, 168.949)), ('A', ' 289 ', 'VAL', 0.17383879048862338, (231.46400000000003, 185.591, 194.335)), ('A', ' 318 ', 'PHE', 0.037092793018652925, (214.023, 174.239, 194.01)), ('A', ' 391 ', 'CYS', 0.0650866163763879, (194.015, 169.426, 169.028)), ('A', ' 646 ', 'ARG', 0.0, (208.738, 168.05200000000002, 209.40699999999998)), ('A', '1107 ', 'ARG', 0.030464878507972845, (206.14400000000006, 187.617, 252.745)), ('B', '  15 ', 'CYS', 0.04842321795877069, (189.91600000000014, 259.543, 155.784)), ('B', '  21 ', 'ARG', 0.13109746113309909, (196.87500000000009, 265.73099999999994, 170.228)), ('B', '  24 ', 'LEU', 0.16621344663372992, (202.35400000000013, 262.2080000000001, 177.05)), ('B', '  87 ', 'ASN', 0.03965808780785556, (198.45700000000005, 238.213, 172.976)), ('B', ' 108 ', 'THR', 0.06314832190349687, (197.76200000000014, 241.278, 162.329)), ('B', ' 125 ', 'ASN', 0.12004632360543671, (172.7220000000001, 249.08300000000006, 167.115)), ('B', ' 137 ', 'ASN', 0.21412545171619304, (195.4280000000001, 255.543, 159.79)), ('B', ' 159 ', 'VAL', 0.038899161961776084, (186.86500000000012, 253.724, 160.439)), ('B', ' 166 ', 'CYS', 0.04842321795877069, (183.43200000000013, 240.718, 153.793)), ('B', ' 289 ', 'VAL', 0.26933289914311515, (192.12500000000003, 233.217, 194.291)), ('B', ' 318 ', 'PHE', 0.23042504502403155, (210.528, 223.594, 193.673)), ('B', ' 357 ', 'ARG', 0.027849402313163643, (230.35599999999997, 198.445, 159.477)), ('B', ' 396 ', 'TYR', 0.03895179757457258, (225.948, 197.496, 161.005)), ('B', ' 546 ', 'LEU', 0.2611190910070291, (222.939, 210.83300000000006, 177.127)), ('B', ' 745 ', 'ASP', 0.007145016841919069, (174.978, 201.20400000000006, 184.89)), ('B', ' 854 ', 'LYS', 0.0, (175.048, 209.52000000000004, 194.44899999999998)), ('C', '  15 ', 'CYS', 0.06658192723989487, (149.03299999999987, 161.252, 155.973)), ('C', '  21 ', 'ARG', 0.0, (140.0859999999999, 162.997, 170.716)), ('C', '  24 ', 'LEU', 0.16352697332918123, (140.15199999999987, 169.69, 177.022)), ('C', ' 125 ', 'ASN', 0.016900562355608755, (166.517, 150.401, 167.221)), ('C', ' 129 ', 'LYS', 0.10966279515401678, (166.998, 161.543, 160.75)), ('C', ' 136 ', 'CYS', 0.09684643591754138, (152.048, 164.054, 158.577)), ('C', ' 166 ', 'CYS', 0.0703582023730298, (168.346, 163.886, 153.724)), ('C', ' 316 ', 'SER', 0.10772734224933506, (173.439, 190.858, 195.17)), ('C', ' 318 ', 'PHE', 0.2645303308351545, (169.749, 196.077, 193.72600000000003)), ('C', ' 319 ', 'ARG', 0.08446096013194586, (168.822, 199.17600000000002, 191.736)), ('C', ' 326 ', 'ILE', 0.2735372683000422, (163.43, 209.872, 177.097)), ('C', ' 391 ', 'CYS', 0.11274576697032473, (175.366, 215.92, 168.963)), ('C', ' 466 ', 'ARG', 0.02355319465913357, (196.902, 227.92, 156.779)), ('C', ' 547 ', 'THR', 0.23408552731225343, (173.234, 209.915, 178.522)), ('C', ' 854 ', 'LYS', 0.0, (199.45, 172.498, 194.46800000000002))]
data['cbeta'] = [('A', ' 516 ', 'GLU', ' ', 0.2531434116649798, (185.841, 175.874, 170.273)), ('A', ' 745 ', 'ASP', ' ', 0.278445554444446, (213.807, 216.671, 185.141)), ('A', '1041 ', 'ASP', ' ', 0.2714033908241382, (207.02400000000014, 190.047, 233.79600000000002)), ('A', '1146 ', 'ASP', ' ', 0.26547713806948714, (202.95, 189.85600000000014, 285.394)), ('B', '  98 ', 'SER', ' ', 0.2635898529049182, (178.0280000000001, 261.4840000000001, 177.862)), ('B', ' 745 ', 'ASP', ' ', 0.36483285173876184, (173.86200000000002, 202.27500000000006, 184.887)), ('C', ' 198 ', 'ASP', ' ', 0.26229734901747526, (177.864, 176.27000000000004, 169.37))]
data['probe'] = [(' B 165  ASN HD21', ' Q   1  NAG  C1 ', -1.583, (189.327, 239.887, 147.345)), (' B  17  ASN  ND2', ' O   1  NAG  C1 ', -1.558, (198.116, 260.832, 157.084)), (' B 331  ASN HD21', ' B1403  NAG  C1 ', -1.546, (238.764, 217.67, 169.129)), (' C 616  ASN HD21', ' e   1  NAG  C1 ', -1.531, (158.891, 207.079, 201.915)), (' A 165  ASN HD21', ' F   1  NAG  C1 ', -1.523, (238.576, 184.675, 147.348)), (' B 454  ARG  HD3', ' B 492  LEU  CD1', -1.5, (220.214, 180.853, 147.503)), (' A  17  ASN HD21', ' D   1  NAG  C1 ', -1.483, (251.474, 165.34, 156.567)), (' B 149  ASN  ND2', ' B1402  NAG  C1 ', -1.483, (171.156, 274.869, 165.336)), (' C 616  ASN  ND2', ' e   1  NAG  C1 ', -1.478, (159.524, 207.319, 201.129)), (' B 331  ASN  ND2', ' B1403  NAG  C1 ', -1.452, (237.531, 217.857, 168.437)), (' B 234  ASN HD21', ' R   1  NAG  C1 ', -1.448, (199.861, 234.761, 162.315)), (' B 165  ASN  ND2', ' Q   1  NAG  C1 ', -1.368, (188.362, 239.49, 148.46)), (' A 234  ASN HD21', ' G   1  NAG  C1 ', -1.359, (229.79, 177.283, 162.624)), (' B 454  ARG  CD ', ' B 492  LEU  CD1', -1.351, (220.241, 179.381, 148.553)), (' B1158  ASN HD21', ' B1408  NAG  C1 ', -1.344, (190.31, 205.935, 302.346)), (' A1158  ASN HD21', ' A1408  NAG  C1 ', -1.33, (208.575, 201.025, 302.266)), (' C 122  ASN  ND2', ' a   1  NAG  C1 ', -1.301, (162.801, 151.183, 161.434)), (' C 149  ASN HD21', ' C1402  NAG  C1 ', -1.292, (148.463, 135.531, 165.64)), (' A  17  ASN  ND2', ' D   1  NAG  C1 ', -1.282, (252.762, 166.294, 157.299)), (' A 122  ASN  ND2', ' E   1  NAG  C1 ', -1.273, (255.507, 190.975, 161.502)), (' B 343  ASN  ND2', ' B1404  NAG  C1 ', -1.265, (224.218, 208.576, 143.844)), (' C 738  CYS  SG ', ' C 760  CYS  SG ', -1.262, (209.146, 185.943, 192.115)), (' C 343  ASN  ND2', ' C1404  NAG  C1 ', -1.261, (175.917, 215.454, 144.316)), (' A 165  ASN  ND2', ' F   1  NAG  C1 ', -1.258, (238.474, 185.448, 148.318)), (' B 234  ASN  ND2', ' R   1  NAG  C1 ', -1.243, (198.995, 235.282, 161.759)), (' C  15  CYS  SG ', ' C 136  CYS  HA ', -1.234, (151.37, 164.097, 156.511)), (' C 343  ASN HD21', ' C1404  NAG  C1 ', -1.232, (175.62, 214.645, 144.949)), (' A 140  PHE  CE2', ' A 244  LEU  CD1', -1.218, (260.179, 175.268, 164.255)), (' B 149  ASN HD22', ' B1402  NAG  C1 ', -1.21, (171.143, 274.164, 165.313)), (' B 343  ASN HD21', ' B1404  NAG  C1 ', -1.21, (223.403, 209.251, 144.53)), (' C 149  ASN  ND2', ' C1402  NAG  C1 ', -1.203, (147.544, 136.621, 165.955)), (' A 149  ASN  ND2', ' A1402  NAG  C1 ', -1.195, (278.208, 182.219, 166.235)), (' A 122  ASN HD21', ' E   1  NAG  C1 ', -1.194, (255.6, 191.743, 161.676)), (' B1158  ASN  ND2', ' B1408  NAG  C1 ', -1.185, (191.315, 206.055, 301.672)), (' B 454  ARG  CD ', ' B 492  LEU HD11', -1.171, (220.881, 179.982, 148.898)), (' A 234  ASN  ND2', ' G   1  NAG  C1 ', -1.168, (229.8, 178.19, 161.972)), (' C 391  CYS  SG ', ' C 525  CYS  SG ', -1.168, (172.054, 217.42, 168.638)), (' B 453  TYR  CD1', ' B 495  TYR  CZ ', -1.167, (213.806, 184.828, 144.337)), (' B 454  ARG  CD ', ' B 492  LEU HD13', -1.138, (219.704, 179.565, 148.615)), (' A 343  ASN HD21', ' A1404  NAG  C1 ', -1.137, (194.783, 170.552, 144.695)), (' C  15  CYS  HA ', ' C 136  CYS  SG ', -1.134, (150.702, 161.365, 156.941)), (' B 122  ASN  ND2', ' P   1  NAG  C1 ', -1.128, (175.994, 250.866, 162.33)), (' A  15  CYS  HA ', ' A 136  CYS  SG ', -1.123, (253.188, 174.963, 156.627)), (' C 472  ILE HG21', ' C 488  CYS  SG ', -1.11, (214.785, 232.173, 145.6)), (' A 141  LEU  CD1', ' A 241  LEU  CD1', -1.107, (252.571, 181.668, 165.62)), (' A 662  CYS  SG ', ' A 697  MET  HE3', -1.093, (214.083, 176.236, 220.437)), (' B 454  ARG  HD2', ' B 492  LEU HD13', -1.085, (218.952, 179.634, 148.618)), (' A1158  ASN  ND2', ' A1408  NAG  C1 ', -1.075, (208.684, 199.897, 301.787)), (' A 343  ASN  ND2', ' A1404  NAG  C1 ', -1.072, (193.593, 170.285, 144.447)), (' A 129  LYS  HE2', ' A 169  GLU  HB3', -1.07, (246.766, 193.852, 158.712)), (' A 149  ASN HD22', ' A1402  NAG  C1 ', -1.068, (277.351, 183.298, 165.321)), (' A 140  PHE  CE2', ' A 244  LEU HD11', -1.057, (259.052, 175.436, 163.824)), (' B 454  ARG  NE ', ' B 492  LEU HD21', -1.034, (221.216, 179.466, 149.295)), (' C 122  ASN HD21', ' a   1  NAG  C1 ', -1.033, (163.341, 150.586, 161.591)), (' A 140  PHE  CE2', ' A 244  LEU HD12', -1.03, (260.018, 176.446, 164.951)), (' C 165  ASN HD21', ' b   1  NAG  C1 ', -1.02, (166.383, 169.298, 146.887)), (' C 472  ILE  CG2', ' C 488  CYS  SG ', -1.004, (213.966, 231.521, 146.122)), (' B  15  CYS  SG ', ' B 136  CYS  SG ', -0.993, (190.358, 255.698, 157.343)), (' A 662  CYS  SG ', ' A 697  MET  CE ', -0.983, (213.012, 176.33, 220.141)), (' A 662  CYS  SG ', ' A 697  MET  SD ', -0.981, (213.647, 174.866, 219.821)), (' C  19  THR  O  ', ' C  21  ARG  HD3', -0.966, (140.296, 164.216, 166.489)), (' C 165  ASN  ND2', ' b   1  NAG  C1 ', -0.966, (165.755, 169.48, 147.806)), (' A 904  TYR  OH ', ' B1094  VAL  HB ', -0.96, (207.412, 209.519, 253.995)), (' B 351  TYR  HB2', ' B 454  ARG HH11', -0.952, (221.861, 181.727, 150.181)), (' B 149  ASN HD21', ' B1402  NAG  C1 ', -0.952, (170.71, 275.704, 166.626)), (' B 738  CYS  SG ', ' B 760  CYS  SG ', -0.946, (181.794, 194.319, 192.536)), (' B 454  ARG  NE ', ' B 492  LEU  CD2', -0.939, (220.966, 179.077, 148.262)), (' C  15  CYS  SG ', ' C 136  CYS  SG ', -0.934, (150.701, 161.828, 156.968)), (' C 480  CYS  SG ', ' C 488  CYS  SG ', -0.927, (216.353, 232.673, 147.366)), (' B 453  TYR  HD1', ' B 495  TYR  CE2', -0.922, (214.141, 185.629, 144.389)), (' A 141  LEU HD12', ' A 241  LEU HD13', -0.916, (253.537, 180.764, 164.996)), (' A 140  PHE  CD2', ' A 244  LEU  CD1', -0.909, (258.549, 176.005, 164.566)), (' C 396  TYR  HB2', ' C 514  SER  OG ', -0.909, (186.973, 221.056, 161.955)), (' C 131  CYS  SG ', ' C 166  CYS  SG ', -0.905, (167.361, 162.986, 155.414)), (' A 140  PHE  CD2', ' A 244  LEU  HG ', -0.9, (258.823, 176.853, 165.159)), (' A1107  ARG  HD3', ' C 904  TYR  CZ ', -0.892, (201.883, 185.099, 252.119)), (' B 351  TYR  CD1', ' B 454  ARG  NH1', -0.889, (222.622, 181.62, 149.087)), (' A 141  LEU HD13', ' A 241  LEU  CD1', -0.884, (253.696, 182.602, 166.357)), (' B 904  TYR  OH ', ' C1094  VAL  HB ', -0.88, (183.324, 200.408, 253.977)), (' B 122  ASN HD21', ' P   1  NAG  C1 ', -0.879, (174.223, 251.217, 162.345)), (' A 141  LEU  CD1', ' A 241  LEU HD13', -0.875, (252.694, 181.318, 165.353)), (' A1082  CYS  SG ', ' A1126  CYS  SG ', -0.874, (193.235, 176.305, 267.746)), (' B 357  ARG  HG2', ' B 357  ARG HH11', -0.865, (232.302, 199.748, 161.145)), (' C 122  ASN HD22', ' a   1  NAG  C1 ', -0.864, (162.566, 151.989, 162.358)), (' A 662  CYS  SG ', ' A 697  MET  CB ', -0.863, (214.314, 174.506, 219.805)), (' B 454  ARG  CZ ', ' B 492  LEU HD21', -0.858, (221.618, 179.832, 149.105)), (' A  17  ASN  CG ', ' D   1  NAG  C1 ', -0.857, (252.603, 166.783, 157.575)), (' B 331  ASN  CG ', ' B1403  NAG  C1 ', -0.851, (238.08, 217.411, 168.021)), (' C 140  PHE  CE2', ' C 158  ARG  HD2', -0.844, (149.105, 156.55, 161.225)), (' A 140  PHE  CD2', ' A 244  LEU  CG ', -0.841, (259.381, 176.591, 165.452)), (' A 140  PHE  HD2', ' A 244  LEU  HG ', -0.84, (257.953, 177.091, 165.574)), (' B 453  TYR  CD1', ' B 495  TYR  CE2', -0.84, (214.45, 184.912, 145.235)), (' C 149  ASN  ND2', ' C1402  NAG  O5 ', -0.835, (148.761, 136.399, 166.167)), (' B 122  ASN HD22', ' P   1  NAG  C1 ', -0.833, (176.213, 251.864, 162.215)), (' C 140  PHE  CZ ', ' C 158  ARG  HD2', -0.829, (148.466, 156.965, 161.771)), (' P   1  NAG  H61', ' P   2  NAG  C7 ', -0.818, (177.692, 248.693, 156.977)), (' A  15  CYS  CA ', ' A 136  CYS  SG ', -0.818, (253.082, 174.095, 156.365)), (' A  15  CYS  SG ', ' A 136  CYS  SG ', -0.817, (252.758, 175.663, 156.263)), (' B  17  ASN HD22', ' O   1  NAG  C1 ', -0.814, (198.223, 261.657, 158.285)), (' A  97  LYS  NZ ', ' A 183  GLN  O  ', -0.813, (264.104, 177.965, 184.088)), (' A 140  PHE  CD2', ' A 244  LEU HD11', -0.813, (258.192, 175.532, 164.333)), (' C 617  CYS  HG ', ' C 649  CYS  HG ', -0.81, (160.225, 199.46, 203.794)), (' B 453  TYR  HD1', ' B 495  TYR  CZ ', -0.807, (214.154, 184.893, 144.849)), (' C 743  CYS  O  ', ' C 977  LEU  CD2', -0.802, (203.587, 180.046, 182.975)), (' A 149  ASN HD21', ' A1402  NAG  C1 ', -0.801, (278.57, 182.675, 166.383)), (' A  17  ASN  OD1', ' D   1  NAG  C1 ', -0.8, (251.937, 166.841, 157.548)), (' C  34  ARG  NH2', ' C 191  GLU  OE2', -0.79, (164.023, 162.67, 187.374)), (' A 122  ASN HD22', ' E   1  NAG  C1 ', -0.786, (255.099, 190.472, 162.402)), (' B 454  ARG  HD3', ' B 492  LEU HD11', -0.785, (220.591, 181.66, 147.942)), (' A 141  LEU  CD1', ' A 241  LEU HD11', -0.782, (252.609, 182.539, 165.901)), (' A1107  ARG  HD3', ' C 904  TYR  CE1', -0.774, (202.304, 186.166, 252.236)), (' A 140  PHE  HE2', ' A 244  LEU HD12', -0.771, (259.953, 176.679, 164.009)), (' C 140  PHE  CZ ', ' C 158  ARG  CD ', -0.771, (148.143, 157.504, 161.096)), (' C1082  CYS  SG ', ' C1126  CYS  SG ', -0.769, (181.598, 212.914, 267.735)), (' B 234  ASN HD21', ' R   1  NAG  C2 ', -0.768, (199.948, 234.493, 162.774)), (' C  28  TYR  CE2', ' C1401  NAG  H5 ', -0.766, (148.871, 178.27, 183.296)), (' A1107  ARG  CD ', ' C 904  TYR  CE1', -0.764, (201.623, 186.409, 251.352)), (' A 129  LYS  HE2', ' A 169  GLU  CB ', -0.758, (246.281, 193.333, 158.518)), (' A 662  CYS  SG ', ' A 697  MET  HB2', -0.756, (214.536, 175.414, 220.837)), (' C 896  ILE HD11', ' C 904  TYR  HE2', -0.745, (202.312, 182.165, 250.823)), (' A  17  ASN HD21', ' D   1  NAG  C2 ', -0.741, (252.002, 165.725, 156.16)), (' C1082  CYS  HG ', ' C1126  CYS  HG ', -0.74, (181.652, 212.958, 269.198)), (' C  15  CYS  HA ', ' C 136  CYS  HG ', -0.738, (149.767, 162.225, 157.228)), (' B 129  LYS  HE2', ' B 169  GLU  CG ', -0.737, (178.888, 242.429, 157.701)), (' A 141  LEU HD12', ' A 241  LEU  CD1', -0.731, (253.147, 180.936, 166.05)), (' B 453  TYR  CE1', ' B 495  TYR  CE1', -0.719, (212.925, 184.471, 143.977)), (' B 357  ARG  HG2', ' B 357  ARG  NH1', -0.715, (232.546, 199.654, 160.667)), (' C 472  ILE HG22', ' C 488  CYS  SG ', -0.713, (214.124, 231.332, 147.37)), (' A  45  SER  O  ', ' A  47  VAL HG23', -0.707, (230.609, 201.28, 193.809)), (' C  15  CYS  CA ', ' C 136  CYS  HG ', -0.703, (149.941, 161.922, 156.344)), (' B 453  TYR  CE1', ' B 495  TYR  CZ ', -0.701, (213.14, 184.564, 144.576)), (' A 669  GLY  HA2', ' C 869  MET  HE1', -0.7, (209.521, 172.433, 218.161)), (' B 391  CYS  HB2', ' B 544  ASN  O  ', -0.699, (224.61, 209.881, 171.683)), (' C  34  ARG HH21', ' C 191  GLU  CD ', -0.698, (164.486, 162.827, 186.571)), (' A 141  LEU HD13', ' A 241  LEU HD11', -0.697, (252.981, 182.48, 166.559)), (' C 329  PHE  CE2', ' C 525  CYS  SG ', -0.691, (171.292, 214.717, 167.95)), (' A 662  CYS  SG ', ' A 697  MET  HB3', -0.69, (215.364, 174.495, 220.061)), (' C 474  GLN  NE2', ' C 480  CYS  SG ', -0.69, (216.51, 233.387, 148.02)), (' B1082  CYS  SG ', ' B1126  CYS  SG ', -0.689, (218.951, 204.841, 267.777)), (' B 351  TYR  HD1', ' B 454  ARG  NH1', -0.687, (223.226, 182.085, 150.091)), (' B1082  CYS  HG ', ' B1126  CYS  HG ', -0.685, (218.805, 204.557, 269.31)), (' B 351  TYR  CB ', ' B 454  ARG HH11', -0.684, (221.261, 182.274, 149.577)), (' B 322  PRO  HA ', ' B 538  CYS  SG ', -0.684, (220.336, 224.03, 185.406)), (' C  15  CYS  HG ', ' C 136  CYS  HA ', -0.681, (151.699, 163.027, 157.049)), (' C 353  TRP  CE2', ' C 466  ARG  HG3', -0.678, (194.493, 225.592, 155.695)), (' B 131  CYS  SG ', ' B 166  CYS  SG ', -0.677, (183.776, 242.827, 155.495)), (' B1082  CYS  CB ', ' B1126  CYS  HG ', -0.671, (217.885, 205.363, 267.818)), (' B 854  LYS  O  ', ' B 856  ASN  N  ', -0.664, (177.707, 208.516, 192.224)), (' A 391  CYS  SG ', ' A 525  CYS  SG ', -0.66, (194.492, 166.733, 168.456)), (' B 351  TYR  HB2', ' B 454  ARG  NH1', -0.66, (222.035, 181.901, 150.443)), (' A 869  MET  HE1', ' B 669  GLY  HA2', -0.654, (214.167, 220.689, 218.329)), (' C 616  ASN HD22', ' e   1  NAG  C1 ', -0.653, (161.05, 207.752, 202.251)), (' C 336  CYS  HB3', ' C 337  PRO  HD2', -0.653, (174.7, 221.469, 156.609)), (' B 480  CYS  SG ', ' B 488  CYS  SG ', -0.65, (218.374, 163.415, 145.886)), (' A 662  CYS  HG ', ' A 671  CYS  HG ', -0.65, (214.3, 176.375, 218.679)), (' C 742  ILE  HA ', ' C1000  ARG  HD3', -0.649, (200.597, 183.915, 187.495)), (' C  15  CYS  CB ', ' C 136  CYS  HG ', -0.649, (149.697, 162.345, 156.362)), (' B 480  CYS  HG ', ' B 488  CYS  HG ', -0.648, (218.88, 163.425, 145.346)), (' C 322  PRO  HA ', ' C 538  CYS  SG ', -0.646, (164.51, 203.503, 185.144)), (' B 351  TYR  HD1', ' B 454  ARG HH12', -0.642, (223.573, 181.422, 150.569)), (' C  15  CYS  SG ', ' C 136  CYS  CA ', -0.641, (151.872, 163.437, 157.651)), (' A1094  VAL  HB ', ' C 904  TYR  OH ', -0.637, (203.377, 183.864, 254.398)), (' B 336  CYS  SG ', ' B 361  CYS  SG ', -0.636, (230.294, 207.99, 159.089)), (' A 403  ARG  NH2', ' A 505  TYR  CE1', -0.635, (185.52, 197.198, 141.572)), (' B 454  ARG  NH2', ' B 469  SER  O  ', -0.633, (223.28, 177.887, 150.36)), (' C 743  CYS  O  ', ' C 977  LEU HD23', -0.632, (203.217, 179.825, 183.036)), (' A  14  GLN  O  ', ' A 136  CYS  SG ', -0.63, (253.772, 175.903, 156.263)), (' A 617  CYS  SG ', ' A 642  VAL HG12', -0.628, (217.262, 162.727, 203.938)), (' C1082  CYS  CB ', ' C1126  CYS  HG ', -0.627, (181.439, 211.876, 267.767)), (' B 453  TYR  CD1', ' B 495  TYR  OH ', -0.627, (212.893, 185.371, 146.074)), (' B 357  ARG  HB2', ' B 396  TYR  HE1', -0.627, (230.463, 195.966, 161.345)), (' A1156  PHE  CZ ', ' C1155  TYR  HB3', -0.62, (196.162, 194.509, 297.707)), (' B 538  CYS  SG ', ' B 590  CYS  SG ', -0.618, (219.955, 222.222, 187.636)), (' B 983  ARG  O  ', ' C 382  VAL  HA ', -0.616, (183.102, 207.321, 167.927)), (' C  19  THR  C  ', ' C  21  ARG  HD3', -0.615, (140.544, 163.786, 166.47)), (' A 391  CYS  SG ', ' A 525  CYS  HB2', -0.614, (193.753, 166.694, 168.48)), (' C 395  VAL  O  ', ' C 395  VAL HG12', -0.608, (181.321, 220.609, 160.016)), (' A1082  CYS  HG ', ' A1126  CYS  HG ', -0.608, (192.917, 176.202, 269.191)), (' C 353  TRP  NE1', ' C 466  ARG  HG3', -0.606, (194.755, 225.578, 155.695)), (' C  15  CYS  CA ', ' C 136  CYS  SG ', -0.603, (150.218, 161.466, 156.445)), (' C 617  CYS  SG ', ' C 649  CYS  SG ', -0.6, (160.319, 199.271, 202.588)), (' A  15  CYS  CB ', ' A 136  CYS  SG ', -0.599, (253.017, 174.274, 156.191)), (' B 869  MET  HE1', ' C 669  GLY  CA ', -0.596, (169.432, 201.102, 217.598)), (' B 454  ARG  HD2', ' B 492  LEU  CD1', -0.596, (219.672, 179.685, 147.632)), (' A 129  LYS  CD ', ' A 169  GLU  HG3', -0.596, (245.377, 191.744, 157.991)), (' B 866  THR  H  ', ' B 869  MET  HE3', -0.594, (171.057, 202.71, 218.67)), (' C  21  ARG  CG ', ' C  21  ARG HH11', -0.594, (141.239, 166.068, 168.452)), (' A 108  THR  O  ', ' A 108  THR HG23', -0.592, (234.193, 175.508, 160.152)), (' A 617  CYS  SG ', ' A 642  VAL  CG1', -0.59, (217.28, 163.104, 203.482)), (' B 454  ARG  HE ', ' B 492  LEU  CD2', -0.587, (220.615, 178.346, 149.232)), (' A 140  PHE  CZ ', ' A 244  LEU HD11', -0.586, (258.933, 174.72, 163.714)), (' A 662  CYS  SG ', ' A 671  CYS  SG ', -0.584, (214.808, 176.284, 218.338)), (' B 617  CYS  SG ', ' B 649  CYS  SG ', -0.583, (217.98, 229.915, 202.988)), (' C 471  GLU  N  ', ' C 471  GLU  OE1', -0.581, (206.218, 234.776, 149.752)), (' C 196  ASN HD21', ' C 235  ILE HD12', -0.58, (167.463, 171.874, 166.972)), (' C 140  PHE  CZ ', ' C 158  ARG  HD3', -0.578, (148.174, 157.567, 160.531)), (' B  78  ARG  HG2', ' B  78  ARG HH11', -0.576, (196.385, 263.416, 176.584)), (' A 329  PHE  CE2', ' A 525  CYS  SG ', -0.575, (197.39, 166.524, 167.793)), (' B 336  CYS  HG ', ' B 361  CYS  HG ', -0.575, (230.331, 207.105, 160.244)), (' B 336  CYS  HG ', ' B 361  CYS  CB ', -0.575, (231.171, 208.498, 159.581)), (' C 329  PHE  HD2', ' C 525  CYS  HG ', -0.572, (170.046, 215.285, 167.929)), (' C 147  LYS  C  ', ' C 149  ASN  H  ', -0.572, (145.258, 140.57, 169.154)), (' C 391  CYS  SG ', ' C 525  CYS  CB ', -0.572, (172.801, 217.035, 167.773)), (' B 454  ARG  NE ', ' B 492  LEU HD22', -0.572, (220.282, 178.503, 148.543)), (' C 395  VAL HG23', ' C 524  VAL HG11', -0.569, (178.635, 219.594, 163.458)), (' C 854  LYS  O  ', ' C 856  ASN  N  ', -0.569, (199.215, 175.178, 192.276)), (' B 331  ASN  ND2', ' B1403  NAG  O5 ', -0.569, (238.267, 218.585, 168.206)), (' A 109  THR  OG1', ' A 114  THR  OG1', -0.566, (236.784, 178.223, 158.564)), (' C 431  GLY  HA2', ' C 515  PHE  CZ ', -0.563, (184.164, 213.034, 163.84)), (' B 129  LYS  HE2', ' B 169  GLU  HG2', -0.562, (178.586, 242.548, 157.536)), (' A 904  TYR  CE1', ' B1107  ARG  NH1', -0.561, (207.016, 206.159, 252.734)), (' B 454  ARG  CD ', ' B 492  LEU  CD2', -0.56, (220.712, 179.474, 148.018)), (' B 462  LYS  NZ ', ' G   1  NAG  H83', -0.558, (224.51, 180.192, 163.703)), (' C 329  PHE  CD2', ' C 525  CYS  SG ', -0.556, (171.033, 215.608, 168.791)), (' C 738  CYS  SG ', ' C 760  CYS  O  ', -0.554, (208.656, 186.891, 193.628)), (' A 129  LYS  HD3', ' A 169  GLU  HG3', -0.552, (245.362, 191.423, 158.623)), (' C  96  GLU  OE1', ' C 101  ILE HG12', -0.551, (156.762, 157.313, 176.983)), (' C  34  ARG  O  ', ' C  56  LEU HD23', -0.55, (163.689, 170.714, 185.965)), (' B 480  CYS  CB ', ' B 488  CYS  SG ', -0.547, (218.889, 163.047, 146.789)), (' A1107  ARG  NE ', ' C 904  TYR  CE1', -0.545, (201.638, 186.972, 252.021)), (' A1156  PHE  CE2', ' C1155  TYR  HB3', -0.543, (196.525, 194.811, 297.427)), (' B 129  LYS  HZ3', ' B 169  GLU  HG2', -0.541, (178.225, 242.682, 156.668)), (' C 332  ILE HG21', ' C 361  CYS  HA ', -0.54, (169.166, 222.2, 162.165)), (' A 336  CYS  HB3', ' A 337  PRO  HD2', -0.538, (189.286, 166.239, 156.77)), (' C 743  CYS  O  ', ' C 977  LEU HD22', -0.535, (202.772, 180.611, 183.752)), (' B  15  CYS  SG ', ' B 136  CYS  CB ', -0.533, (191.217, 255.967, 157.691)), (' C 569  ILE  H  ', ' C 569  ILE HD12', -0.532, (178.088, 219.31, 194.15)), (' C 129  LYS  HE2', ' a   1  NAG  H62', -0.53, (164.44, 155.686, 159.043)), (' B 905  ARG  HD2', ' B1049  LEU  O  ', -0.526, (188.356, 206.633, 242.661)), (' D   1  NAG  H62', ' D   2  NAG  C7 ', -0.524, (247.185, 163.494, 157.994)), (' C 140  PHE  HZ ', ' C 158  ARG  CD ', -0.52, (147.942, 157.338, 161.089)), (' A 854  LYS  O  ', ' B 589  PRO  HG3', -0.518, (219.887, 214.29, 192.573)), (' C 391  CYS  SG ', ' C 525  CYS  HB2', -0.517, (172.344, 217.73, 167.893)), (' A  45  SER  O  ', ' A  47  VAL  CG2', -0.517, (230.209, 201.426, 194.035)), (' B 357  ARG  HB2', ' B 396  TYR  CE1', -0.516, (230.196, 196.02, 161.114)), (' B 357  ARG  NH1', ' B 359  SER  HB3', -0.516, (233.623, 201.859, 161.992)), (' C 480  CYS  HG ', ' C 488  CYS  HG ', -0.514, (216.965, 233.243, 146.279)), (' A 404  GLY  HA3', ' A 508  TYR  CD1', -0.513, (189.956, 189.463, 144.736)), (' A 391  CYS  HG ', ' A 525  CYS  CB ', -0.509, (194.891, 166.372, 167.984)), (' C 102  ARG  HA ', ' C 102  ARG  NE ', -0.509, (158.155, 155.082, 170.793)), (' C  34  ARG  NH2', ' C 191  GLU  CD ', -0.504, (163.7, 162.542, 187.213)), (' C 200  TYR  HD2', ' C 228  ASP  OD1', -0.499, (176.874, 167.847, 168.848)), (' C 197  ILE HG13', ' C 202  LYS  HZ1', -0.498, (175.188, 174.489, 172.29)), (' A 854  LYS  C  ', ' B 589  PRO  HG3', -0.497, (219.747, 213.524, 192.842)), (' B 357  ARG  CG ', ' B 357  ARG HH11', -0.495, (232.499, 199.565, 161.883)), (' B 480  CYS  CB ', ' B 488  CYS  HG ', -0.495, (218.815, 162.627, 146.695)), (' B 129  LYS  HE2', ' B 169  GLU  HB3', -0.494, (178.015, 242.153, 158.884)), (' C 156  GLU  HB3', ' C 158  ARG  HG3', -0.493, (150.702, 154.986, 160.017)), (' A 141  LEU HD13', ' A 241  LEU HD12', -0.491, (253.772, 181.642, 166.962)), (' A 525  CYS  SG ', ' A 526  GLY  N  ', -0.49, (196.507, 166.983, 166.379)), (' A 865  LEU  HA ', ' A 869  MET  HE3', -0.488, (214.015, 218.236, 219.117)), (' B 129  LYS  CE ', ' B 169  GLU  HG2', -0.488, (178.465, 243.183, 157.549)), (' A 462  LYS  HZ1', ' c   1  NAG  H81', -0.486, (169.467, 183.108, 163.029)), (' A 903  ALA  HB1', ' A 913  GLN  HB2', -0.486, (211.557, 202.365, 253.588)), (' B 129  LYS  HE2', ' B 169  GLU  CB ', -0.485, (178.315, 242.015, 158.628)), (' C 865  LEU  HA ', ' C 869  MET  HE3', -0.484, (208.075, 173.699, 219.157)), (' A 904  TYR  CE2', ' B1107  ARG  HD3', -0.482, (206.006, 207.693, 251.054)), (' C  21  ARG  CG ', ' C  21  ARG  NH1', -0.481, (141.49, 166.227, 168.669)), (' A 437  ASN  HB2', ' A 508  TYR  CZ ', -0.479, (192.96, 187.415, 143.817)), (' B  34  ARG  O  ', ' B  56  LEU HD23', -0.478, (191.076, 241.072, 186.274)), (' A 905  ARG  HD2', ' A1049  LEU  O  ', -0.477, (210.406, 202.016, 242.798)), (' C  21  ARG  HG2', ' C  21  ARG HH11', -0.477, (140.914, 165.709, 169.005)), (' B 738  CYS  SG ', ' B 760  CYS  O  ', -0.477, (182.732, 194.504, 193.938)), (' A 408  ARG  O  ', ' A 414  GLN  NE2', -0.476, (188.237, 194.079, 157.009)), (' A 129  LYS  CE ', ' A 169  GLU  HB3', -0.476, (246.871, 193.099, 158.761)), (' A 462  LYS  NZ ', ' c   1  NAG  H83', -0.473, (169.386, 183.61, 163.988)), (' A 462  LYS  HZ1', ' c   1  NAG  C8 ', -0.47, (169.287, 183.148, 163.277)), (' B 869  MET  HE1', ' C 669  GLY  HA2', -0.468, (169.599, 200.522, 218.183)), (' C 322  PRO  CA ', ' C 538  CYS  SG ', -0.467, (164.712, 203.35, 185.137)), (' e   1  NAG  H62', ' e   2  NAG  C7 ', -0.461, (155.317, 210.052, 199.508)), (' A 404  GLY  CA ', ' A 508  TYR  CD1', -0.461, (189.693, 189.283, 145.19)), (' A 901  GLN  O  ', ' A 905  ARG  HG2', -0.46, (211.263, 204.388, 247.188)), (' C 336  CYS  CB ', ' C 337  PRO  HD2', -0.458, (174.353, 221.209, 157.323)), (' A 141  LEU  CD1', ' A 241  LEU HD12', -0.455, (253.778, 181.491, 166.766)), (' I   1  NAG  H62', ' I   2  NAG  C7 ', -0.455, (208.799, 155.46, 199.324)), (' C 395  VAL  CG2', ' C 524  VAL HG11', -0.453, (178.087, 219.695, 163.18)), (' A1050  MET  HE2', ' A1052  PHE  CE1', -0.452, (215.706, 206.146, 239.4)), (' A1107  ARG  CD ', ' C 904  TYR  CZ ', -0.451, (202.208, 185.622, 251.508)), (' A 669  GLY  CA ', ' C 869  MET  HE1', -0.449, (209.9, 172.227, 217.874)), (' B 748  GLU  CD ', ' B 748  GLU  H  ', -0.449, (177.303, 197.591, 178.498)), (' B 380  TYR  CE2', ' B 412  PRO  HD3', -0.449, (211.31, 195.648, 161.409)), (' C 149  ASN  C  ', ' C 151  SER  N  ', -0.448, (148.797, 139.106, 170.622)), (' B 462  LYS  HZ3', ' G   1  NAG  H83', -0.448, (224.493, 180.34, 163.459)), (' C 149  ASN  C  ', ' C 151  SER  H  ', -0.447, (148.222, 138.991, 170.453)), (' B 743  CYS  HB3', ' B 749  CYS  HB3', -0.445, (180.133, 199.162, 183.655)), (' B 332  ILE HG21', ' B 361  CYS  HA ', -0.445, (233.175, 210.732, 162.418)), (' C  21  ARG  NH1', ' C  23  GLN HE22', -0.444, (140.721, 167.312, 168.456)), (' A 391  CYS  HB2', ' A 544  ASN  O  ', -0.44, (194.77, 168.753, 171.58)), (' A 592  PHE  CD2', ' C 740  MET  HE1', -0.439, (207.148, 174.873, 194.036)), (' G   1  NAG  H62', ' G   2  NAG  H82', -0.438, (231.129, 171.707, 163.634)), (' A 403  ARG  CZ ', ' A 505  TYR  CD1', -0.438, (184.783, 195.991, 141.989)), (' C 129  LYS  HD3', ' a   2  NAG  C8 ', -0.438, (165.224, 158.033, 157.245)), (' A 129  LYS  CD ', ' A 169  GLU  CG ', -0.437, (245.739, 192.267, 158.224)), (' C  95  THR  O  ', ' C 186  PHE  CD1', -0.437, (153.42, 156.657, 183.261)), (' A 124  THR  HB ', ' E   1  NAG  H82', -0.436, (258.512, 194.174, 163.196)), (' C  15  CYS  HG ', ' C 136  CYS  CA ', -0.435, (151.868, 163.143, 157.718)), (' C  15  CYS  HG ', ' C 136  CYS  CB ', -0.435, (151.479, 162.882, 157.94)), (' I   1  NAG  H62', ' I   2  NAG  H82', -0.435, (209.018, 155.769, 198.763)), (' e   1  NAG  H62', ' e   2  NAG  H82', -0.434, (155.653, 209.707, 198.548)), (' A 391  CYS  SG ', ' A 525  CYS  CB ', -0.434, (194.525, 166.546, 168.02)), (' C  21  ARG HH11', ' C  23  GLN HE22', -0.431, (140.749, 167.073, 168.67)), (' C 129  LYS  HD3', ' a   2  NAG  H81', -0.431, (165.457, 157.993, 156.736)), (' C 395  VAL HG23', ' C 524  VAL  CG1', -0.431, (178.059, 219.494, 164.203)), (' B 453  TYR  HE1', ' B 495  TYR  CE1', -0.43, (212.41, 184.364, 143.71)), (' A 403  ARG  CZ ', ' A 505  TYR  CE1', -0.43, (184.94, 196.648, 141.648)), (' A 343  ASN  CG ', ' A1404  NAG  C1 ', -0.429, (193.707, 170.923, 144.726)), (' B 343  ASN  CG ', ' B1404  NAG  C1 ', -0.429, (223.588, 207.866, 144.64)), (' B 351  TYR  CG ', ' B 454  ARG  NH1', -0.429, (222.185, 182.101, 149.422)), (' B  78  ARG  HG2', ' B  78  ARG  NH1', -0.428, (196.576, 263.064, 176.847)), (' A 462  LYS  HZ2', ' c   1  NAG  H83', -0.426, (169.047, 183.936, 164.507)), (' A 159  VAL HG23', ' A 160  TYR  CD1', -0.426, (251.045, 182.669, 158.767)), (' B 157  PHE  CD1', ' B 157  PHE  O  ', -0.426, (182.905, 255.579, 158.194)), (' A1082  CYS  CB ', ' A1126  CYS  HG ', -0.426, (194.324, 177.004, 268.256)), (' B 454  ARG  HE ', ' B 492  LEU HD22', -0.425, (220.681, 177.935, 148.802)), (' A 157  PHE  CD1', ' A 157  PHE  O  ', -0.425, (255.391, 182.288, 158.157)), (' A 749  CYS  SG ', ' A 997  ILE HD11', -0.425, (205.025, 210.01, 182.832)), (' C 140  PHE  HZ ', ' C 158  ARG  HD3', -0.423, (147.902, 157.677, 160.941)), (' B 404  GLY  HA3', ' B 508  TYR  CE1', -0.423, (208.924, 195.613, 144.813)), (' T   1  NAG  H62', ' T   2  NAG  H82', -0.422, (228.625, 229.071, 198.755)), (' C 858  LEU HD13', ' C 959  LEU HD22', -0.421, (197.478, 179.804, 199.068)), (' A 858  LEU HD13', ' A 959  LEU HD22', -0.418, (214.201, 206.743, 199.192)), (' B 129  LYS  NZ ', ' B 169  GLU  HG2', -0.418, (178.272, 243.284, 157.048)), (' B 904  TYR  HH ', ' C1094  VAL  HB ', -0.417, (183.438, 200.19, 254.047)), (' C 742  ILE HG12', ' C1000  ARG  HB3', -0.417, (200.881, 186.556, 188.849)), (' B 159  VAL HG23', ' B 160  TYR  CD1', -0.416, (184.84, 251.879, 159.141)), (' C 391  CYS  HB2', ' C 544  ASN  O  ', -0.415, (174.259, 215.393, 171.77)), (' A  44  ARG  O  ', ' A 283  GLY  CA ', -0.411, (235.348, 201.711, 191.092)), (' B 379  CYS  SG ', ' B 384  PRO  HD3', -0.41, (212.076, 205.557, 161.54)), (' A 462  LYS  NZ ', ' c   1  NAG  C8 ', -0.409, (169.356, 183.152, 163.916)), (' B 740  MET  HE1', ' C 592  PHE  CG ', -0.409, (172.926, 202.034, 193.548)), (' B  36  VAL HG21', ' B 220  PHE  CE2', -0.409, (186.602, 237.337, 190.207)), (' B 742  ILE  HA ', ' B1000  ARG  HD3', -0.407, (184.834, 202.735, 187.682)), (' B 281  GLU  CD ', ' B 281  GLU  H  ', -0.406, (175.176, 230.554, 197.704)), (' C 474  GLN HE22', ' C 480  CYS  HG ', -0.406, (217.195, 232.98, 147.351)), (' A 274  THR HG22', ' A 291  CYS  SG ', -0.404, (225.037, 185.962, 191.163)), (' B 453  TYR  CD1', ' B 495  TYR  CE1', -0.404, (213.182, 185.123, 144.139)), (' B 129  LYS  CE ', ' B 169  GLU  CG ', -0.404, (178.935, 242.954, 157.745)), (' A 474  GLN  NE2', ' A 480  CYS  H  ', -0.403, (155.943, 194.918, 150.467)), (' A 904  TYR  CD2', ' B1107  ARG  HD3', -0.402, (206.176, 207.221, 250.784)), (' A 117  LEU HD12', ' A 231  ILE HD12', -0.401, (239.072, 188.344, 164.242))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
