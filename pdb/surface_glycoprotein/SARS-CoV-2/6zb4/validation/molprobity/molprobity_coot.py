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
data['rama'] = [('A', ' 754 ', 'GLY', 0.05405388082207563, (118.68000000000005, 131.673, 119.335)), ('C', ' 754 ', 'GLY', 0.07313804600501926, (98.896, 111.694, 115.377))]
data['omega'] = []
data['rota'] = [('C', '  45 ', 'SER', 0.29533041868250226, (106.228, 144.315, 131.336)), ('C', '  63 ', 'THR', 0.1567273276211577, (132.38299999999998, 165.509, 119.44300000000001)), ('C', ' 124 ', 'THR', 0.20530761830664304, (105.77000000000002, 180.429, 116.789)), ('C', ' 167 ', 'THR', 0.2506509957980492, (107.282, 168.16500000000005, 97.531)), ('C', ' 169 ', 'GLU', 0.27671398062701336, (105.186, 170.39499999999998, 104.057)), ('C', ' 189 ', 'LEU', 0.1921044524543484, (119.155, 168.268, 127.513)), ('C', ' 227 ', 'VAL', 0.19191382627182044, (107.34500000000001, 161.436, 113.658)), ('C', ' 233 ', 'ILE', 0.19260043209706013, (115.64, 161.79200000000006, 99.203)), ('C', ' 282 ', 'ASN', 0.25274624610384705, (104.88, 149.767, 134.056)), ('C', ' 326 ', 'ILE', 0.2789609927165935, (139.259, 143.042, 95.985)), ('C', ' 335 ', 'LEU', 0.2803648295404229, (131.073, 144.23999999999995, 73.642)), ('C', ' 389 ', 'ASP', 0.2871192896549736, (128.277, 140.79400000000004, 89.03)), ('C', ' 398 ', 'ASP', 0.09747946073985407, (118.728, 129.91999999999993, 70.401)), ('C', ' 483 ', 'VAL', 0.24917723968499364, (102.18800000000003, 110.10400000000001, 48.521)), ('C', ' 514 ', 'SER', 0.261012673764839, (121.79, 128.95999999999995, 77.995)), ('C', ' 604 ', 'THR', 0.2113889059280828, (131.48899999999995, 142.287, 144.331)), ('C', ' 638 ', 'THR', 0.2058570088200715, (146.95400000000006, 144.601, 126.273)), ('C', ' 699 ', 'GLU', 0.2350340537089279, (153.91800000000003, 116.151, 151.898)), ('C', ' 702 ', 'VAL', 0.27228930361841636, (156.24400000000003, 108.73399999999997, 157.12699999999998)), ('C', ' 706 ', 'ASN', 0.18899791119854453, (162.197, 98.199, 159.57)), ('C', ' 721 ', 'THR', 0.22445747641643282, (126.782, 113.209, 156.549)), ('C', ' 737 ', 'MET', 0.24770087814574218, (97.52000000000005, 122.35299999999997, 123.721)), ('C', ' 798 ', 'ASN', 0.2563963501936704, (120.392, 110.77599999999997, 173.174)), ('C', ' 837 ', 'CYS', 0.21856767025056262, (95.491, 132.87100000000004, 137.709)), ('C', ' 856 ', 'THR', 0.045687138904154954, (101.27500000000003, 119.59700000000001, 134.179)), ('C', ' 875 ', 'LEU', 0.0006462081900922019, (115.258, 103.90399999999997, 163.496)), ('C', ' 881 ', 'SER', 0.28894061953234024, (116.756, 95.07399999999997, 168.019)), ('C', ' 898 ', 'GLN', 0.29676625099554554, (124.94800000000001, 95.92499999999997, 170.78400000000002)), ('C', ' 913 ', 'LEU', 0.29679166997167494, (133.36099999999993, 99.797, 175.443)), ('C', ' 935 ', 'LEU', 0.29878764289469395, (122.76100000000002, 122.525, 159.85)), ('C', '1074 ', 'THR', 0.1320618631879901, (158.69000000000005, 95.0, 167.112)), ('C', '1078 ', 'ILE', 0.2878441771029691, (160.091, 84.722, 169.862)), ('C', '1091 ', 'VAL', 0.25388718250187936, (151.60000000000005, 92.09, 167.789)), ('C', '1119 ', 'VAL', 0.2712623717784016, (154.479, 77.533, 168.06)), ('C', '1126 ', 'VAL', 0.2011415098602065, (162.478, 83.51699999999997, 160.19100000000003)), ('C', '1133 ', 'THR', 0.2194742882407895, (161.08500000000006, 83.78199999999997, 177.712)), ('B', '  16 ', 'VAL', 0.24243499664632265, (44.051, 120.903, 99.221)), ('B', '  18 ', 'LEU', 0.1594078368798748, (44.162, 118.881, 105.715)), ('B', '  29 ', 'THR', 0.1299193307384467, (64.404, 108.593, 121.621)), ('B', '  62 ', 'VAL', 0.18313575733744927, (66.141, 111.65199999999997, 118.183)), ('B', '  88 ', 'ASP', 0.2909472877416949, (74.53900000000003, 120.031, 108.308)), ('B', ' 108 ', 'THR', 0.09048177180269293, (65.732, 127.28799999999997, 101.68)), ('B', ' 111 ', 'ASP', 0.24409442275374246, (58.49, 128.831, 96.897)), ('B', ' 124 ', 'THR', 0.20997249425793665, (56.421, 103.237, 89.551)), ('B', ' 173 ', 'GLN', 0.24369746704106604, (62.376, 103.14799999999997, 84.852)), ('B', ' 208 ', 'THR', 0.2250601888018091, (67.46399999999997, 95.652, 107.392)), ('B', ' 210 ', 'ILE', 0.17056987511417318, (63.232000000000006, 92.93499999999997, 111.147)), ('B', ' 287 ', 'ASP', 0.16734248692356926, (81.917, 98.08699999999999, 115.26400000000001)), ('B', ' 298 ', 'GLU', 0.27182515137335556, (88.88100000000004, 108.69, 124.443)), ('B', ' 398 ', 'ASP', 0.18167564369364694, (101.385, 155.86100000000005, 94.729)), ('B', ' 466 ', 'ARG', 0.25008966415124734, (112.874, 159.77800000000005, 94.10100000000001)), ('B', ' 478 ', 'THR', 0.2533906435077674, (135.533, 165.274, 78.12)), ('B', ' 500 ', 'THR', 0.18023588447262542, (96.794, 152.951, 67.131)), ('B', ' 514 ', 'SER', 0.2124002098784456, (101.417, 150.186, 101.185)), ('B', ' 516 ', 'GLU', 0.2002743185593234, (101.124, 147.51899999999998, 107.986)), ('B', ' 613 ', 'GLN', 0.2895933951937373, (93.34500000000004, 117.54100000000003, 139.399)), ('B', ' 638 ', 'THR', 0.29242963367106617, (78.345, 115.471, 138.533)), ('B', ' 661 ', 'GLU', 0.27398349035968667, (96.811, 97.678, 150.249)), ('B', ' 699 ', 'GLU', 0.00849728848778899, (102.047, 98.56, 163.06899999999996)), ('B', ' 720 ', 'THR', 0.2639853505330157, (113.537, 82.564, 147.399)), ('B', ' 742 ', 'ASP', 0.2191712884314673, (112.025, 100.11699999999999, 95.113)), ('B', ' 744 ', 'THR', 0.29369672483243614, (115.123, 104.74799999999999, 91.734)), ('B', ' 788 ', 'THR', 0.14233895362569293, (127.75000000000003, 65.103, 136.934)), ('B', ' 817 ', 'ASP', 0.26482044181592246, (111.438, 73.919, 130.672)), ('B', ' 825 ', 'LEU', 0.0006042992114182179, (108.86300000000004, 84.462, 121.74800000000002)), ('B', ' 875 ', 'LEU', 0.004751849073906769, (125.789, 73.75400000000003, 139.08)), ('B', '1035 ', 'LYS', 0.0, (128.19599999999997, 88.48399999999998, 153.844)), ('B', '1071 ', 'ASN', 0.2861569177219837, (112.82, 85.573, 176.531)), ('B', '1088 ', 'ARG', 0.0, (134.58199999999994, 85.85599999999997, 174.294)), ('B', '1102 ', 'THR', 0.2286748828868957, (125.084, 80.77799999999999, 174.758)), ('B', '1117 ', 'THR', 0.2631768483004858, (135.88, 83.598, 179.42600000000002)), ('B', '1133 ', 'THR', 0.21707740089816882, (130.41299999999998, 81.61399999999998, 190.013)), ('A', '  31 ', 'SER', 0.2879705313183524, (137.853, 94.91199999999999, 80.34)), ('A', '  84 ', 'LEU', 0.060854376824412026, (127.04, 98.37, 66.009)), ('A', ' 118 ', 'LEU', 0.2477545305009315, (130.83, 112.25699999999998, 60.663)), ('A', ' 120 ', 'VAL', 0.22785590386149293, (137.264, 111.914, 60.120000000000005)), ('A', ' 124 ', 'THR', 0.2970044743721976, (145.90000000000003, 116.51899999999998, 56.374)), ('A', ' 281 ', 'GLU', 0.28946053715760484, (148.57800000000003, 115.033, 96.085)), ('A', ' 309 ', 'GLU', 0.2531526623118183, (139.721, 94.725, 108.151)), ('A', ' 315 ', 'THR', 0.26756776996407544, (125.24400000000001, 94.494, 103.11200000000001)), ('A', ' 323 ', 'THR', 0.1401480546555596, (112.096, 91.854, 83.12900000000002)), ('A', ' 388 ', 'ASN', 0.2904890013514628, (98.442, 110.85699999999997, 78.562)), ('A', ' 438 ', 'SER', 0.22374742252434415, (86.102, 134.49799999999993, 70.891)), ('A', ' 469 ', 'SER', 0.273325690833215, (67.267, 134.211, 91.334)), ('A', ' 500 ', 'THR', 0.27494556537760756, (86.383, 147.048, 68.192)), ('A', ' 514 ', 'SER', 0.23065128817193503, (87.09100000000002, 118.65599999999998, 87.235)), ('A', ' 529 ', 'LYS', 0.19055986651159001, (97.61, 100.539, 74.197)), ('A', ' 597 ', 'VAL', 0.20963899310042222, (129.924, 89.146, 103.97)), ('A', ' 604 ', 'THR', 0.22243454128811424, (146.217, 88.656, 103.27)), ('A', ' 702 ', 'VAL', 0.24894944837879993, (135.153, 65.803, 139.257)), ('A', ' 716 ', 'THR', 0.2400770824444617, (151.524, 80.566, 143.63)), ('A', ' 718 ', 'SER', 0.2961093635954928, (149.871, 85.77000000000002, 140.648)), ('A', ' 776 ', 'GLN', 0.24719374485178777, (139.21, 113.83300000000001, 141.295)), ('A', ' 788 ', 'THR', 0.1772253708583308, (159.26600000000005, 107.45700000000002, 149.546)), ('A', ' 807 ', 'SER', 0.2711651930134539, (165.917, 110.76800000000003, 135.838)), ('A', ' 846 ', 'LEU', 0.15273301141255213, (142.796, 117.32, 110.282)), ('A', ' 875 ', 'LEU', 0.011828591467469127, (151.863, 103.547, 146.658)), ('A', ' 934 ', 'SER', 0.28924516226073077, (154.722, 91.638, 127.984)), ('A', '1034 ', 'SER', 0.29724749440066256, (138.554, 92.86800000000002, 149.74)), ('A', '1035 ', 'LYS', 0.12998906697463372, (136.78899999999993, 89.597, 150.505)), ('A', '1078 ', 'ILE', 0.10933392051987226, (135.61, 61.78600000000001, 165.817)), ('A', '1125 ', 'VAL', 0.27223768875589777, (123.487, 60.445, 165.331)), ('A', '1130 ', 'VAL', 0.1286074811479634, (134.81799999999996, 57.404, 162.977)), ('A', '1136 ', 'ASP', 0.2558427519653749, (145.771, 65.975, 176.038))]
data['cbeta'] = []
data['probe'] = [(' B 616  ASN HD21', ' B1305  NAG  C1 ', -1.253, (89.809, 121.63, 148.587)), (' B 616  ASN  ND2', ' B1305  NAG  C1 ', -1.103, (89.684, 123.122, 147.844)), (' B 714  ASN  ND2', ' B1301  NAG  C1 ', -1.007, (112.675, 74.765, 164.257)), (' C 343  ASN  ND2', ' C1401  NAG  O5 ', -0.974, (118.992, 147.999, 65.279)), (' A2102  NAG  O4 ', ' A2103  NAG  C1 ', -0.964, (160.306, 75.202, 142.459)), (' A 339  GLY  O  ', ' A 343  ASN  OD1', -0.952, (82.41, 120.959, 68.745)), (' A 462  LYS  NZ ', ' B1309  NAG  H82', -0.9, (76.613, 129.458, 101.656)), (' C 975  ASN  O  ', ' C 979  SER  OG ', -0.834, (95.004, 136.207, 112.521)), (' B 714  ASN  CG ', ' B1301  NAG  C1 ', -0.822, (112.956, 73.385, 164.564)), (' A 226  LEU  HG ', ' A 227  VAL HG23', -0.819, (137.919, 116.819, 71.282)), (' C 343  ASN  ND2', ' C1401  NAG  C1 ', -0.806, (119.504, 147.709, 66.041)), (' B 616  ASN  OD1', ' B1305  NAG  C1 ', -0.805, (89.24, 122.433, 148.582)), (' A 798  ASN  ND2', ' A2107  NAG  O7 ', -0.805, (165.764, 95.526, 143.574)), (' B 616  ASN HD21', ' B1305  NAG  C2 ', -0.769, (90.93, 122.063, 149.164)), (' B 616  ASN  CG ', ' B1305  NAG  C1 ', -0.767, (89.431, 122.616, 147.765)), (' A  81  ASN  ND2', ' A  81  ASN  O  ', -0.752, (132.139, 98.255, 57.938)), (' B 700  ASN  OD1', ' B 701  SER  N  ', -0.73, (105.259, 95.979, 166.898)), (' B1310  NAG  O3 ', ' B1310  NAG  O7 ', -0.726, (47.631, 129.851, 102.437)), (' B 999  GLN  NE2', ' C 999  GLN  OE1', -0.723, (112.374, 115.704, 114.758)), (' A 339  GLY  C  ', ' A 343  ASN  OD1', -0.72, (82.838, 119.966, 69.084)), (' B 808  LYS  NZ ', ' B 817  ASP  OD2', -0.693, (111.428, 69.386, 129.547)), (' A 339  GLY  CA ', ' A 343  ASN  OD1', -0.69, (83.136, 120.282, 68.351)), (' C 898  GLN  OE1', ' C 902  ARG  NH2', -0.683, (122.882, 97.932, 165.41)), (' B1301  NAG  O4 ', ' B1302  NAG  C1 ', -0.675, (108.807, 69.781, 163.088)), (' B  17  ASN  OD1', ' B1310  NAG  O5 ', -0.673, (45.313, 125.301, 101.773)), (' A 339  GLY  HA2', ' A 343  ASN  OD1', -0.667, (83.8, 120.672, 68.475)), (' C 439  ASN  O  ', ' C 443  SER  OG ', -0.66, (103.298, 142.464, 60.644)), (' B  17  ASN  OD1', ' B1310  NAG  H61', -0.654, (44.494, 124.266, 100.551)), (' A 467  ASP  OD1', ' A 469  SER  OG ', -0.653, (69.314, 133.866, 92.774)), (' A 462  LYS  HZ2', ' B1309  NAG  H82', -0.651, (76.458, 128.929, 102.084)), (' C 309  GLU  N  ', ' C 309  GLU  OE1', -0.65, (125.977, 135.085, 138.437)), (' B 486  PHE  O  ', ' B 487  ASN  ND2', -0.645, (129.625, 160.454, 72.811)), (' A 614  ASP  OD2', ' B 851  LYS  NZ ', -0.643, (114.28, 87.949, 105.904)), (' A 462  LYS  CE ', ' B1309  NAG  H82', -0.633, (77.674, 129.338, 101.852)), (' A 734  ASP  OD2', ' C 319  ARG  NH2', -0.632, (131.919, 131.94, 116.215)), (' A  17  ASN HD21', ' A2109  NAG  HN2', -0.629, (128.006, 97.943, 45.914)), (' C 105  ILE HG22', ' C 118  LEU HD12', -0.627, (117.867, 173.883, 106.654)), (' C  99  ASN  O  ', ' C 102  ARG  NH2', -0.626, (116.204, 180.324, 119.948)), (' A 975  ASN  O  ', ' A 979  SER  OG ', -0.623, (127.849, 133.966, 95.899)), (' B 127  VAL HG13', ' B 171  VAL HG22', -0.622, (60.977, 112.24, 87.256)), (' C 520  ALA  HB1', ' C 521  PRO  HD2', -0.617, (135.498, 126.214, 82.429)), (' C 599  THR HG22', ' C 601  GLY  H  ', -0.613, (132.213, 138.0, 138.75)), (' B 520  ALA  HB1', ' B 521  PRO  HD2', -0.61, (99.143, 152.285, 115.944)), (' A 520  ALA  HB1', ' A 521  PRO  HD2', -0.609, (85.649, 104.037, 91.272)), (' C 486  PHE  O  ', ' C 487  ASN  ND2', -0.606, (93.445, 108.931, 56.076)), (' C 798  ASN HD21', ' C1404  NAG  H2 ', -0.605, (119.513, 114.797, 176.181)), (' A 968  GLY  O  ', ' A 992  ARG  NH1', -0.589, (115.979, 122.496, 98.478)), (' B 111  ASP  N  ', ' B 111  ASP  OD1', -0.585, (59.849, 129.156, 97.95)), (' B 876  ALA  O  ', ' B 880  THR  OG1', -0.583, (130.888, 69.57, 141.037)), (' B 335  LEU HD23', ' B 336  CYS  O  ', -0.579, (85.255, 156.03, 99.179)), (' B 123  ALA  O  ', ' B 124  THR HG23', -0.579, (54.895, 101.659, 90.042)), (' B  31  SER  HB3', ' B  62  VAL HG21', -0.578, (68.316, 108.656, 116.666)), (' B  37  TYR  CD1', ' B  37  TYR  O  ', -0.577, (79.44, 106.938, 105.504)), (' C1025  LYS  NZ ', ' C1039  PHE  O  ', -0.576, (128.666, 104.868, 151.247)), (' A 568  ASP  N  ', ' A 572  THR  O  ', -0.574, (97.261, 99.342, 101.136)), (' A 867  ILE  O  ', ' A 871  THR HG23', -0.57, (149.067, 109.392, 139.591)), (' B  17  ASN HD21', ' B1310  NAG  H5 ', -0.567, (44.081, 126.281, 102.064)), (' B 438  SER  O  ', ' B 438  SER  OG ', -0.567, (94.754, 156.433, 79.617)), (' C 876  ALA  O  ', ' C 880  THR  OG1', -0.563, (113.898, 98.946, 167.729)), (' A1079  CYS  HB2', ' A1129  ILE HD11', -0.557, (132.56, 59.365, 167.365)), (' B 520  ALA  HB1', ' B 521  PRO  CD ', -0.557, (98.865, 151.924, 115.695)), (' A 244  LEU  O  ', ' A 244  LEU HD12', -0.555, (143.483, 101.221, 50.758)), (' C 845  ASP  OD1', ' C 846  LEU  N  ', -0.552, (104.284, 131.662, 137.982)), (' A 108  THR HG21', ' A 234  ASN  OD1', -0.55, (117.937, 108.265, 65.792)), (' B1101  VAL HG23', ' B1112  ILE HG12', -0.55, (129.068, 81.46, 181.175)), (' B 353  TRP  O  ', ' B 466  ARG  NH1', -0.548, (106.481, 161.73, 94.172)), (' C1071  ASN  OD1', ' C1405  NAG  C1 ', -0.546, (158.334, 107.381, 166.639)), (' B  34  ARG  NH2', ' B 191  GLU  OE1', -0.545, (70.242, 100.324, 111.114)), (' C 244  LEU  O  ', ' C 244  LEU HD12', -0.542, (121.851, 186.987, 115.988)), (' C 109  THR  O  ', ' C 109  THR HG23', -0.541, (123.528, 169.475, 96.083)), (' A  37  TYR  CD1', ' A  37  TYR  O  ', -0.541, (134.613, 110.974, 82.624)), (' B 468  ILE HD12', ' C1402  NAG  H82', -0.541, (111.695, 168.048, 90.736)), (' C 911  ASN  N  ', ' C 911  ASN  OD1', -0.539, (136.649, 94.747, 175.985)), (' B 437  ASN  OD1', ' B 438  SER  N  ', -0.539, (95.214, 152.059, 78.553)), (' B 617  CYS  N  ', ' B 644  GLN  OE1', -0.539, (86.733, 119.995, 145.371)), (' A1097  THR  OG1', ' A1098  HIS  ND1', -0.538, (149.03, 55.436, 160.079)), (' B1092  PHE  CD1', ' B1101  VAL HG22', -0.536, (128.448, 83.412, 179.561)), (' C1405  NAG  H2 ', ' C1405  NAG  H61', -0.534, (159.216, 110.63, 165.808)), (' A 340  GLU  N  ', ' A 340  GLU  OE1', -0.534, (80.946, 117.729, 69.604)), (' B 201  PHE  HB2', ' B 231  ILE HD11', -0.534, (72.257, 118.499, 96.357)), (' C 875  LEU HD23', ' C 879  ILE HD11', -0.532, (117.186, 105.761, 166.423)), (' A 851  LYS  NZ ', ' C 614  ASP  OD2', -0.528, (142.057, 126.995, 118.761)), (' A 616  ASN HD21', ' A2106  NAG  C7 ', -0.524, (115.96, 74.689, 106.454)), (' C  96  GLU  O  ', ' C 187  LYS  N  ', -0.524, (119.401, 174.682, 129.512)), (' B 467  ASP  OD1', ' B 469  SER  OG ', -0.524, (117.932, 163.572, 89.839)), (' B1078  ILE HD12', ' B1112  ILE HD13', -0.523, (129.027, 83.382, 183.878)), (' A 234  ASN  CG ', ' A2101  NAG  C1 ', -0.522, (116.49, 109.061, 67.728)), (' C 798  ASN HD21', ' C1404  NAG  C2 ', -0.521, (118.542, 114.86, 176.183)), (' A 437  ASN  OD1', ' A 438  SER  N  ', -0.521, (87.827, 136.051, 71.25)), (' C 564  GLN  NE2', ' C 577  ARG  O  ', -0.52, (141.427, 132.159, 87.983)), (' C 294  ASP  N  ', ' C 294  ASP  OD1', -0.519, (131.568, 144.338, 126.184)), (' A 428  ASP  N  ', ' A 428  ASP  OD1', -0.518, (89.85, 122.722, 97.8)), (' B 977  ILE HG23', ' B 981  LEU HD12', -0.517, (104.381, 114.068, 93.864)), (' C  82  PRO  HG2', ' C  84  LEU HD21', -0.516, (130.602, 170.286, 111.605)), (' A 794  PHE  HD1', ' C 704  TYR  HH ', -0.516, (160.474, 97.243, 153.636)), (' B  17  ASN  ND2', ' B1310  NAG  C1 ', -0.516, (44.75, 125.502, 103.035)), (' A2109  NAG  O3 ', ' A2109  NAG  O7 ', -0.516, (124.751, 98.746, 44.694)), (' A 961  LYS  HG2', ' C 569  ILE HD11', -0.511, (134.573, 114.26, 104.921)), (' C 324  GLU  OE1', ' C 534  VAL HG11', -0.508, (145.048, 144.752, 100.447)), (' C  94  SER  HB2', ' C 101  ILE HD12', -0.507, (121.629, 172.676, 121.079)), (' B 638  THR HG22', ' B 639  GLY  H  ', -0.505, (77.679, 115.248, 140.936)), (' B 343  ASN  ND2', ' B1303  NAG  O5 ', -0.505, (85.162, 158.579, 87.544)), (' C  40  ASP  OD2', ' C  44  ARG  NH2', -0.504, (108.76, 144.399, 120.406)), (' B 130  VAL HG21', ' B 231  ILE HG22', -0.504, (69.883, 119.325, 91.722)), (' B 294  ASP  N  ', ' B 294  ASP  OD1', -0.501, (83.058, 108.734, 125.63)), (' C 520  ALA  HB1', ' C 521  PRO  CD ', -0.501, (135.897, 127.054, 82.874)), (' B  30  ASN  O  ', ' B  31  SER  OG ', -0.501, (70.032, 108.18, 119.332)), (' B 109  THR  O  ', ' B 109  THR HG23', -0.5, (62.351, 129.551, 98.696)), (' A 717  ILE HG13', ' A 920  ILE HG23', -0.497, (154.148, 85.189, 146.816)), (' C 156  GLU  N  ', ' C 156  GLU  OE1', -0.495, (113.953, 188.735, 112.204)), (' B1309  NAG  O4 ', ' B1309  NAG  O6 ', -0.494, (69.975, 132.623, 104.163)), (' B 438  SER  OG ', ' B 442  ASP  OD2', -0.493, (95.515, 156.854, 80.462)), (' B  17  ASN HD21', ' B1310  NAG  C5 ', -0.49, (44.26, 126.102, 102.056)), (' B 919  LEU  CD1', ' B1302  NAG  H82', -0.49, (111.899, 69.36, 159.56)), (' C 105  ILE HG22', ' C 118  LEU  CD1', -0.489, (117.464, 174.136, 106.499)), (' B1092  PHE  CE1', ' B1101  VAL HG22', -0.489, (129.002, 83.494, 180.06)), (' C1405  NAG  H3 ', ' C1405  NAG  O7 ', -0.487, (156.254, 109.052, 164.249)), (' C 118  LEU  O  ', ' C 128  ILE  O  ', -0.487, (112.462, 171.971, 106.468)), (' B 439  ASN  O  ', ' B 443  SER  OG ', -0.486, (94.168, 156.88, 73.602)), (' A 441  LEU  O  ', ' A 444  LYS  NZ ', -0.486, (78.441, 135.951, 67.325)), (' A 234  ASN  OD1', ' A2101  NAG  C1 ', -0.484, (116.075, 108.284, 67.368)), (' C 798  ASN  ND2', ' C1404  NAG  H2 ', -0.482, (119.496, 114.633, 175.636)), (' B 788  THR HG22', ' B 789  PRO  HD2', -0.482, (127.004, 64.552, 139.197)), (' A 753  TYR  O  ', ' A 755  SER  N  ', -0.481, (117.021, 130.327, 119.603)), (' A 234  ASN  OD1', ' A2101  NAG  O5 ', -0.479, (116.182, 107.952, 66.841)), (' B 732  SER  HB3', ' B 856  THR HG23', -0.477, (119.057, 93.787, 110.194)), (' A 401  VAL HG22', ' A 509  ARG  HG2', -0.472, (82.386, 131.969, 75.652)), (' B1116  ASN  O  ', ' B1117  THR HG23', -0.472, (133.452, 82.898, 179.369)), (' C 437  ASN  OD1', ' C 438  SER  N  ', -0.472, (105.096, 141.3, 67.009)), (' B 569  ILE HD11', ' C 961  LYS  HG2', -0.471, (109.897, 133.072, 128.23)), (' C 675  GLN  HG3', ' C 690  ILE HD11', -0.471, (144.246, 135.722, 146.194)), (' B  17  ASN  CG ', ' B1310  NAG  O5 ', -0.47, (45.169, 124.661, 102.53)), (' A 850  GLN  HB2', ' A 855  LEU HD12', -0.469, (135.893, 120.356, 113.698)), (' B 517  LEU HD13', ' C 980  ARG  HD2', -0.469, (98.722, 141.124, 107.387)), (' B 947  ASP  OD2', ' B 948  VAL  N  ', -0.468, (110.48, 93.513, 129.064)), (' A 675  GLN  HG2', ' A 676  THR  H  ', -0.468, (144.121, 75.694, 108.201)), (' A 334  ASN  N  ', ' A 334  ASN  OD1', -0.468, (84.436, 104.572, 72.367)), (' A 415  THR  O  ', ' A 415  THR HG22', -0.467, (88.213, 140.281, 95.373)), (' A1122  ASN  N  ', ' A1122  ASN  OD1', -0.466, (125.688, 62.377, 172.287)), (' B 173  GLN  HB2', ' B 174  PRO  CD ', -0.466, (61.293, 101.016, 84.271)), (' A  28  TYR  O  ', ' A  29  THR  OG1', -0.464, (138.487, 89.656, 73.428)), (' A 393  THR  HA ', ' A 522  ALA  HA ', -0.464, (86.834, 107.487, 87.047)), (' C 798  ASN HD21', ' C1404  NAG  C1 ', -0.464, (118.543, 114.571, 175.564)), (' B 470  THR  O  ', ' B 470  THR HG23', -0.462, (117.746, 169.267, 84.8)), (' B 481  ASN  N  ', ' B 481  ASN  OD1', -0.462, (130.423, 171.488, 79.066)), (' A 108  THR HG22', ' A 236  THR  HB ', -0.46, (119.302, 105.692, 65.769)), (' B 937  SER  OG ', ' B 938  THR  N  ', -0.458, (99.19, 78.671, 138.167)), (' B 774  ASN  O  ', ' B 778  VAL HG23', -0.457, (126.037, 88.572, 131.02)), (' A 100  ILE  O  ', ' A 100  ILE HG22', -0.457, (142.558, 101.599, 59.395)), (' A 462  LYS  HZ1', ' B1309  NAG  H82', -0.455, (76.835, 129.805, 102.94)), (' B 799  PHE  CD1', ' B 802  ILE HD11', -0.455, (120.136, 71.04, 142.929)), (' B1077  ALA  O  ', ' B1129  ILE HD12', -0.454, (130.585, 91.854, 185.664)), (' C 227  VAL HG12', ' C 228  ASP  H  ', -0.453, (106.557, 161.769, 111.195)), (' A 454  ARG  NH2', ' A 469  SER  O  ', -0.452, (69.751, 135.626, 90.328)), (' B 227  VAL HG22', ' B 228  ASP  H  ', -0.451, (74.345, 109.807, 92.81)), (' A1071  ASN  ND2', ' A2108  NAG  C1 ', -0.45, (142.009, 61.474, 143.964)), (' B 714  ASN HD21', ' B1301  NAG  C1 ', -0.45, (113.012, 73.709, 163.528)), (' B 234  ASN  OD1', ' B1309  NAG  C1 ', -0.448, (72.521, 128.979, 101.776)), (' B 484  GLU  HA ', ' B 488  CYS  HB2', -0.448, (125.667, 167.405, 75.604)), (' B 753  TYR  O  ', ' B 755  SER  N  ', -0.445, (124.856, 111.496, 104.044)), (' A  29  THR HG22', ' A  30  ASN  N  ', -0.445, (138.859, 91.264, 77.426)), (' A1102  THR HG23', ' A1103  GLN  O  ', -0.443, (143.985, 71.115, 156.457)), (' A1077  ALA  O  ', ' A1129  ILE HG13', -0.442, (132.505, 60.83, 165.079)), (' C 886  GLY  HA3', ' C1031  LEU HD23', -0.442, (117.294, 93.679, 157.717)), (' A  63  THR  HG1', ' A  65  PHE  HE2', -0.442, (133.286, 94.831, 68.589)), (' A 774  ASN  O  ', ' A 778  VAL HG23', -0.442, (137.557, 109.608, 138.889)), (' C  31  SER  HB2', ' C  62  VAL HG21', -0.442, (128.349, 160.373, 122.849)), (' A 108  THR HG22', ' A 236  THR  CB ', -0.441, (119.242, 105.788, 66.055)), (' A  17  ASN  O  ', ' A  18  LEU HD23', -0.44, (135.476, 96.571, 47.482)), (' B 334  ASN  N  ', ' B 334  ASN  OD1', -0.439, (83.931, 158.26, 107.528)), (' A 616  ASN  ND2', ' A2106  NAG  C7 ', -0.439, (115.826, 74.904, 106.463)), (' B  29  THR HG22', ' B  30  ASN  H  ', -0.438, (65.465, 106.264, 121.106)), (' C 448  ASN  OD1', ' C 450  ASN  ND2', -0.437, (107.798, 135.231, 54.087)), (' B  17  ASN  O  ', ' B  18  LEU HD12', -0.435, (43.446, 117.98, 103.412)), (' A 911  ASN  N  ', ' A 911  ASN  OD1', -0.435, (152.413, 80.538, 160.301)), (' A 599  THR HG22', ' A 601  GLY  H  ', -0.434, (138.897, 90.176, 104.908)), (' C 753  TYR  O  ', ' C 755  SER  N  ', -0.431, (100.616, 110.503, 114.455)), (' C 108  THR HG23', ' C 109  THR  H  ', -0.431, (123.286, 166.296, 97.653)), (' A 603  ASN  OD1', ' A 604  THR HG23', -0.43, (145.411, 90.446, 105.389)), (' A 109  THR  O  ', ' A 111  ASP  N  ', -0.43, (120.907, 107.084, 56.996)), (' A 712  PRO  HA ', ' A1068  GLN  O  ', -0.429, (147.477, 70.737, 147.108)), (' C 139  PRO  HB2', ' C 159  VAL HG23', -0.429, (121.212, 178.453, 107.176)), (' C 799  PHE  HD1', ' C 802  ILE HD11', -0.428, (119.256, 108.474, 167.347)), (' A 339  GLY  HA2', ' A 343  ASN  CG ', -0.428, (84.128, 120.626, 68.267)), (' A 439  ASN  O  ', ' A 443  SER  OG ', -0.428, (83.719, 140.065, 67.701)), (' A 173  GLN  O  ', ' A 175  PHE  N  ', -0.427, (145.132, 119.733, 61.134)), (' A 280  ASN  OD1', ' A 284  THR  N  ', -0.427, (146.055, 112.875, 91.348)), (' C1029  CYS  O  ', ' C1048  SER  OG ', -0.427, (124.338, 101.763, 158.481)), (' B 483  VAL HG22', ' B 484  GLU  H  ', -0.426, (126.434, 171.129, 74.077)), (' A 223  LEU  N  ', ' A 223  LEU HD12', -0.425, (140.753, 108.408, 81.196)), (' B 802  ILE HD12', ' B 875  LEU HD21', -0.425, (120.694, 72.913, 141.019)), (' A 616  ASN  ND2', ' A2106  NAG  O7 ', -0.424, (115.221, 75.289, 106.806)), (' C 743  SER  OG ', ' C 745  GLU  OE2', -0.423, (93.315, 127.38, 114.177)), (' A 474  GLN  NE2', ' A 476  GLY  O  ', -0.423, (67.33, 148.097, 102.779)), (' B 187  LYS  O  ', ' B 210  ILE  N  ', -0.422, (62.724, 94.085, 109.852)), (' C  54  LEU HD22', ' C  88  ASP  OD2', -0.422, (123.035, 152.48, 110.867)), (' A 227  VAL HG12', ' A 228  ASP  N  ', -0.421, (133.311, 118.49, 71.957)), (' B 919  LEU HD12', ' B1302  NAG  H82', -0.42, (111.981, 69.131, 159.294)), (' A 568  ASP  OD2', ' B 843  ALA  HB1', -0.42, (99.487, 94.547, 104.269)), (' B 223  LEU  N  ', ' B 223  LEU HD12', -0.419, (74.937, 101.899, 107.2)), (' C1405  NAG  C2 ', ' C1405  NAG  H61', -0.419, (159.684, 110.193, 165.916)), (' A 912  VAL  O  ', ' A 912  VAL HG12', -0.419, (153.177, 80.341, 153.757)), (' A1091  VAL HG22', ' A1092  PHE  N  ', -0.419, (138.919, 67.169, 158.421)), (' C 108  THR HG23', ' C 109  THR  N  ', -0.418, (123.674, 166.518, 97.878)), (' B  17  ASN  ND2', ' B1310  NAG  O5 ', -0.417, (44.649, 125.433, 102.805)), (' C 899  MET  SD ', ' C1047  MET  HE1', -0.416, (125.738, 101.997, 168.407)), (' B 468  ILE  CD1', ' C1402  NAG  H82', -0.416, (111.407, 167.773, 91.164)), (' A 905  GLY  O  ', ' A1035  LYS  NZ ', -0.416, (140.324, 87.612, 153.646)), (' B 240  THR HG22', ' B 241  LEU  N  ', -0.415, (57.798, 112.445, 103.573)), (' C1069  GLU  N  ', ' C1069  GLU  OE1', -0.415, (149.024, 108.688, 167.704)), (' B 723  ILE HG13', ' B1058  VAL HG22', -0.415, (114.105, 84.326, 137.634)), (' B 445  VAL HG23', ' B 446  GLY  H  ', -0.415, (97.678, 163.967, 67.141)), (' B  94  SER  HB2', ' B 101  ILE HD12', -0.415, (59.463, 105.966, 107.169)), (' B 457  ARG  NH1', ' B 467  ASP  OD2', -0.415, (118.899, 160.39, 90.448)), (' B 805  ASP  N  ', ' B 805  ASP  OD1', -0.414, (117.087, 66.37, 131.879)), (' A 760  LEU HD22', ' A1005  VAL HG21', -0.414, (124.105, 120.018, 121.061)), (' B 398  ASP  N  ', ' B 398  ASP  OD1', -0.414, (101.607, 155.122, 96.289)), (' B  36  VAL HG21', ' B 220  PHE  CZ ', -0.413, (78.499, 101.865, 112.567)), (' C  63  THR HG22', ' C  64  TRP  H  ', -0.412, (132.845, 167.841, 118.814)), (' A 616  ASN HD21', ' A2106  NAG  C1 ', -0.412, (115.41, 73.859, 105.78)), (' A 643  PHE  CD2', ' A 645  THR HG22', -0.412, (127.044, 76.342, 108.186)), (' C 988  VAL  O  ', ' C 992  ARG  HG3', -0.411, (105.79, 126.545, 107.164)), (' A 240  THR HG22', ' A 241  LEU  N  ', -0.41, (136.281, 103.28, 61.243)), (' C 109  THR  O  ', ' C 111  ASP  N  ', -0.41, (123.138, 171.236, 97.596)), (' C  96  GLU  OE2', ' C 101  ILE  N  ', -0.41, (119.636, 176.417, 120.646)), (' B 875  LEU HD23', ' B 879  ILE HD11', -0.408, (123.212, 71.88, 141.058)), (' A 553  THR HG22', ' A 554  GLU  N  ', -0.407, (97.912, 85.249, 93.512)), (' B 966  ASN  N  ', ' B 966  ASN  OD1', -0.404, (100.78, 111.378, 105.328)), (' B 566  GLY  O  ', ' C  43  PHE  O  ', -0.404, (103.282, 143.618, 125.183)), (' A1087  PRO  O  ', ' A1116  ASN  O  ', -0.403, (139.516, 71.752, 166.31)), (' A  37  TYR  O  ', ' A  38  TYR  C  ', -0.403, (135.485, 112.394, 84.503)), (' B 227  VAL HG22', ' B 228  ASP  N  ', -0.403, (74.513, 109.883, 93.357)), (' B 231  ILE HD12', ' B 233  ILE HG12', -0.402, (70.941, 121.104, 95.596)), (' C 484  GLU  HA ', ' C 488  CYS  HB2', -0.402, (99.372, 111.114, 51.812)), (' B 401  VAL HG22', ' B 509  ARG  HG2', -0.401, (98.295, 156.433, 84.048)), (' A 745  GLU  N  ', ' A 745  GLU  OE2', -0.401, (124.641, 137.751, 105.557))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
