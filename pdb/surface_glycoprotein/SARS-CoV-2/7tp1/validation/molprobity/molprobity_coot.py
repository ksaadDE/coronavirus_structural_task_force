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
data['rama'] = [('A', '  32 ', 'PHE', 0.013624552127011825, (207.52499999999998, 152.68800000000005, 148.53300000000002)), ('A', '  81 ', 'ASN', 0.031020124415246184, (216.154, 149.13000000000005, 126.80300000000001)), ('A', ' 167 ', 'THR', 0.033408833993602005, (200.457, 164.92900000000006, 111.874)), ('A', ' 488 ', 'CYS', 0.022229825417687567, (124.17000000000006, 155.44900000000007, 106.339)), ('A', ' 571 ', 'ASP', 0.04835468796001239, (160.569, 139.358, 145.431)), ('A', ' 620 ', 'VAL', 0.01591585541061252, (185.525, 132.85, 153.21)), ('A', ' 622 ', 'VAL', 0.06515261067245277, (189.904, 130.598, 153.25100000000003)), ('B', '  32 ', 'PHE', 0.016723971145488285, (130.174, 128.784, 150.11100000000002)), ('B', '  98 ', 'SER', 0.0322940762417133, (127.20400000000004, 110.323, 132.95400000000004)), ('B', ' 123 ', 'ALA', 0.04931531174305211, (136.108, 114.33700000000003, 129.741)), ('B', ' 418 ', 'ILE', 0.07150476059682147, (158.551, 184.153, 114.73100000000001)), ('B', ' 459 ', 'SER', 0.02792091142351605, (164.127, 192.834, 120.92000000000002)), ('B', ' 478 ', 'LYS', 0.0, (175.1, 202.60200000000006, 109.909)), ('B', ' 487 ', 'ASN', 0.0448178791274741, (172.157, 197.05800000000005, 110.875)), ('B', ' 489 ', 'TYR', 0.019850911794841504, (167.33, 198.539, 106.40000000000002)), ('B', ' 603 ', 'ASN', 0.022406014274954478, (140.56, 131.98800000000006, 169.016)), ('B', ' 624 ', 'ILE', 0.02993477986632545, (129.04, 153.516, 154.302)), ('B', ' 631 ', 'PRO', 0.01944443521669068, (126.32200000000005, 141.107, 152.723)), ('B', '1041 ', 'ASP', 0.02592696314546058, (155.15, 153.976, 195.405)), ('C', ' 136 ', 'CYS', 0.02431211053829355, (137.641, 215.983, 118.97600000000003)), ('C', ' 456 ', 'PHE', 0.03591251011469437, (185.682, 145.857, 112.06000000000003)), ('C', ' 457 ', 'ARG', 0.03391052767718277, (189.282, 145.85, 113.47600000000003)), ('C', ' 458 ', 'LYS', 0.042098141453864146, (187.575, 143.20700000000005, 115.691)), ('C', ' 604 ', 'THR', 0.01862246587225712, (149.255, 198.09400000000005, 173.752)), ('C', ' 638 ', 'THR', 0.011031765831262147, (167.764, 204.548, 161.976)), ('C', ' 640 ', 'SER', 0.02988798066118291, (168.978, 207.998, 165.328))]
data['omega'] = [('B', '  98 ', 'SER', None, (127.886, 110.34600000000003, 134.255)), ('B', ' 625 ', 'HIS', None, (127.69400000000007, 152.636, 152.456))]
data['rota'] = [('A', '  63 ', 'THR', 0.11938699296678931, (210.946, 147.118, 137.11)), ('A', ' 105 ', 'ILE', 0.08846395396433313, (208.087, 155.947, 121.37900000000003)), ('A', ' 214 ', 'ARG', 0.0, (220.08, 152.22600000000006, 144.29)), ('A', ' 318 ', 'PHE', 0.04024594660905071, (182.733, 141.922, 152.561)), ('A', ' 366 ', 'SER', 0.10252365065834523, (170.276, 141.63500000000005, 114.96600000000002)), ('A', ' 458 ', 'LYS', 0.012420183789381914, (129.718, 151.58500000000006, 117.25600000000001)), ('A', ' 498 ', 'GLN', 0.007665197467945878, (148.649, 154.452, 92.92)), ('A', ' 523 ', 'THR', 0.22879091596514056, (160.407, 128.891, 123.72700000000003)), ('A', ' 586 ', 'ASP', 0.18287765453368934, (167.474, 126.49700000000003, 145.363)), ('A', ' 603 ', 'ASN', 0.010132306067927713, (201.086, 156.148, 168.231)), ('A', ' 608 ', 'VAL', 0.22200759243232326, (195.926, 145.49300000000005, 164.052)), ('A', ' 622 ', 'VAL', 0.008541984645562805, (189.904, 130.598, 153.25100000000003)), ('A', ' 760 ', 'CYS', 0.07292225477393645, (160.747, 176.358, 154.419)), ('A', ' 820 ', 'ASP', 0.14699241085050233, (189.241, 177.96600000000007, 184.72)), ('A', ' 886 ', 'TRP', 0.00553331175493336, (169.584, 174.16700000000006, 203.55600000000007)), ('A', ' 907 ', 'ASN', 0.24671304291758564, (173.775, 163.942, 212.19400000000002)), ('A', '1118 ', 'ASP', 0.08154586110237275, (168.59399999999994, 154.90100000000007, 229.82500000000005)), ('B', ' 193 ', 'VAL', 0.16907837005624346, (136.891, 129.099, 135.52)), ('B', ' 474 ', 'GLN', 0.048713960363056225, (167.703, 199.59100000000007, 112.96900000000002)), ('B', ' 493 ', 'GLN', 0.08731373794361418, (161.379, 189.77, 103.397)), ('B', ' 578 ', 'ASP', 0.09035076673731587, (124.32700000000006, 176.905, 139.308)), ('B', ' 760 ', 'CYS', 0.16147833979980453, (174.49, 155.91, 153.122)), ('B', ' 907 ', 'ASN', 0.08684314121959501, (162.821, 150.756, 212.34200000000004)), ('B', '1082 ', 'CYS', 0.16441001274004052, (146.34799999999996, 167.672, 231.028)), ('B', '1094 ', 'VAL', 0.24884305763135922, (149.333, 158.823, 219.77600000000007)), ('B', '1145 ', 'LEU', 0.06581050893777443, (161.226, 159.197, 247.035)), ('C', ' 105 ', 'ILE', 0.1083764857630399, (140.505, 208.57, 127.33200000000002)), ('C', ' 294 ', 'ASP', 0.09290012797197615, (156.665, 198.282, 157.75100000000003)), ('C', ' 324 ', 'GLU', 0.01161994248813621, (178.212, 196.565, 140.44600000000003)), ('C', ' 328 ', 'ARG', 0.2293406589809607, (186.93, 189.72400000000005, 133.28)), ('C', ' 343 ', 'ASN', 0.2011135741234931, (184.467, 176.102, 104.59200000000001)), ('C', ' 391 ', 'CYS', 0.2336097814156816, (184.101, 180.10200000000006, 127.61000000000001)), ('C', ' 455 ', 'LEU', 0.05350682929689584, (183.399, 147.849, 109.614)), ('C', ' 603 ', 'ASN', 0.05638188911131047, (146.966, 195.609, 171.821)), ('C', ' 641 ', 'ASN', 0.0675609362530516, (168.265, 205.312, 168.004)), ('C', ' 738 ', 'CYS', 0.22003685048657884, (146.659, 158.60400000000007, 154.04)), ('C', ' 907 ', 'ASN', 0.1713943876968446, (156.951, 166.55, 212.96800000000002))]
data['cbeta'] = [('B', ' 630 ', 'THR', ' ', 0.3717565233483047, (123.06800000000005, 144.756, 151.217)), ('C', ' 112 ', 'SER', ' ', 0.25058382964665876, (140.821, 208.345, 118.26000000000003)), ('C', ' 391 ', 'CYS', ' ', 0.25745108221555224, (184.787, 181.42200000000005, 127.27900000000002)), ('C', ' 638 ', 'THR', ' ', 0.3429515567201308, (168.589, 205.58700000000005, 161.18500000000003)), ('C', ' 773 ', 'GLU', ' ', 0.25593494273158734, (150.849, 156.273, 174.774))]
data['probe'] = [(' C 391  CYS  HB2', ' C 525  CYS  HA ', -0.558, (184.932, 181.782, 125.305)), (' C 130  VAL HG22', ' C 168  PHE  H  ', -0.462, (136.971, 199.525, 119.386)), (' B 620  VAL  HA ', ' B 623  ALA  HB3', -0.438, (125.989, 155.626, 158.097)), (' B 748  GLU  CD ', ' B 748  GLU  H  ', -0.433, (176.018, 147.593, 137.809)), (' A 620  VAL  H  ', ' A 621  PRO  CD ', -0.417, (185.901, 132.738, 155.407)), (' B 421  TYR  CG ', ' B 455  LEU HD13', -0.406, (161.086, 190.235, 115.853)), (' C 122  ASN  O  ', ' C1311  NAG  H82', -0.405, (123.396, 210.873, 126.957)), (' C 490  PHE  CG ', ' C 491  PRO  HD2', -0.401, (190.479, 146.655, 102.186))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
