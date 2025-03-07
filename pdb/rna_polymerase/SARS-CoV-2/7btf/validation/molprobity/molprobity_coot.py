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
data['omega'] = [('A', ' 505 ', 'PRO', None, (134.38, 107.98000000000005, 138.864))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' A  28  THR HG21', ' A  55  ARG  HD3', -0.862, (104.573, 132.349, 85.362)), (' D 161  ASP  HB2', ' D 181  ALA  HB3', -0.818, (82.169, 106.35, 165.739)), (' D 162  ALA  HB2', ' D 183  PRO  HG2', -0.769, (86.544, 107.604, 166.122)), (' A  15  SER  HB3', ' A 118  ARG HH21', -0.722, (102.904, 116.188, 77.384)), (' A  28  THR  O  ', ' A  28  THR HG22', -0.717, (105.416, 134.038, 85.521)), (' C  66  VAL HG13', ' C  67  ASP  H  ', -0.71, (102.653, 123.604, 166.176)), (' A  28  THR  CG2', ' A  55  ARG  HD3', -0.706, (104.757, 132.533, 85.37)), (' A 540  THR  CG2', ' A 667  VAL HG22', -0.7, (127.824, 113.683, 130.882)), (' A 312  ASN HD21', ' A 464  CYS  H  ', -0.695, (128.109, 120.519, 107.645)), (' A 225  THR HG22', ' A 226  THR  H  ', -0.66, (136.542, 118.804, 75.412)), (' B 162  ALA  HB2', ' B 183  PRO  HG2', -0.644, (108.882, 107.353, 141.372)), (' A 684  ASP  HB3', ' A 687  THR HG23', -0.636, (133.396, 123.204, 129.19)), (' A 164  ASP  OD1', ' A 165  PHE  N  ', -0.63, (111.131, 126.188, 117.386)), (' A 279  ARG HH12', ' A 352  GLY  HA2', -0.62, (133.988, 107.3, 111.278)), (' A 380  MET  HE1', ' B  95  LEU  HB3', -0.612, (136.839, 94.076, 136.188)), (' A  35  PHE  HZ ', ' A  50  LYS  HD3', -0.61, (114.622, 133.697, 87.324)), (' C  16  VAL HG11', ' D  91  LEU HD22', -0.609, (106.185, 126.053, 158.983)), (' B 177  SER  HG ', ' B 182  TRP  HZ2', -0.596, (98.87, 104.788, 137.808)), (' D 135  TYR  HB3', ' D 182  TRP  CH2', -0.596, (78.551, 115.275, 168.946)), (' A 540  THR HG21', ' A 667  VAL HG22', -0.592, (128.009, 114.333, 131.089)), (' D 177  SER  HB3', ' D 182  TRP  HZ2', -0.59, (76.954, 113.41, 171.654)), (' A  18  ARG  HB3', ' A  59  LYS  HG3', -0.59, (93.472, 120.727, 81.369)), (' A   8  LEU  HA ', ' A  11  VAL HG12', -0.582, (100.306, 127.262, 73.609)), (' B  83  VAL HG22', ' B  87  MET  HE3', -0.578, (142.488, 107.305, 143.443)), (' A 493  VAL HG13', ' A 573  GLN HE21', -0.578, (146.949, 125.3, 134.712)), (' A 695  ASN HD21', ' A 762  ALA  HB2', -0.572, (127.374, 137.562, 121.532)), (' D 120  ILE HD11', ' D 149  TYR  HE2', -0.57, (90.804, 122.343, 155.991)), (' A   9  ASN  O  ', ' A  12  CYS  SG ', -0.56, (99.401, 122.583, 71.022)), (' A 631  ARG  HG2', ' A 663  LEU HD13', -0.554, (131.216, 119.723, 121.687)), (' C  58  VAL HG22', ' D 119  ILE HG12', -0.553, (99.153, 118.722, 151.521)), (' A 330  VAL HG11', ' B 117  LEU HD13', -0.549, (133.027, 98.627, 126.807)), (' D 182  TRP  O  ', ' D 184  LEU HD12', -0.547, (83.255, 112.651, 166.342)), (' D 172  ILE  HA ', ' D 180  LEU HD21', -0.546, (75.017, 112.37, 166.634)), (' A 601  MET  O  ', ' A 605  VAL HG23', -0.54, (133.37, 148.49, 124.598)), (' A 540  THR HG22', ' A 667  VAL  HA ', -0.538, (128.15, 111.86, 131.978)), (' A 196  MET  HE3', ' A 232  PRO  HB3', -0.53, (128.281, 118.635, 85.321)), (' A 795  SER  HB3', ' A 798  LYS  HE2', -0.524, (112.214, 134.894, 121.257)), (' D 147  PHE  HB3', ' D 154  TRP  HB2', -0.512, (81.641, 121.546, 153.762)), (' A 324  THR HG22', ' A 396  PHE  HZ ', -0.511, (122.16, 101.033, 122.339)), (' A 755  MET  HG2', ' A 764  VAL HG22', -0.507, (129.338, 142.159, 117.537)), (' A 468  GLN  HA ', ' A 731  LEU HD22', -0.504, (131.809, 129.588, 103.01)), (' A 335  VAL HG22', ' A 363  SER  HB2', -0.504, (147.442, 94.109, 133.003)), (' C  52  MET  HG3', ' D 103  LEU HD21', -0.501, (97.94, 130.221, 154.003)), (' A 412  PRO  HG3', ' C  14  LEU HD23', -0.499, (110.969, 124.768, 149.642)), (' A 335  VAL  O  ', ' A 338  VAL HG22', -0.499, (144.519, 90.091, 136.441)), (' A 414  ASN  ND2', ' A 846  ASP  HB2', -0.496, (119.916, 127.488, 154.179)), (' A  72  VAL  HA ', ' A 115  SER  HA ', -0.493, (109.38, 127.253, 76.704)), (' A 483  TYR  HE1', ' A 582  THR HG21', -0.489, (143.552, 139.042, 124.085)), (' C  44  ASP  OD1', ' C  46  THR HG22', -0.484, (93.351, 136.926, 143.172)), (' D 135  TYR  HA ', ' D 138  TYR  HB3', -0.483, (80.11, 118.07, 167.596)), (' A 105  ARG  HG2', ' A 110  MET  SD ', -0.476, (106.737, 132.667, 61.545)), (' A 388  LEU HD23', ' A 397  SER  OG ', -0.473, (119.454, 103.592, 131.182)), (' D 114  CYS  HA ', ' D 131  VAL  O  ', -0.472, (88.567, 117.63, 163.233)), (' D 117  LEU  HB2', ' D 129  MET  HG3', -0.47, (91.273, 113.169, 155.584)), (' A 830  PRO  O  ', ' A 868  PRO  HG2', -0.463, (126.968, 149.471, 138.605)), (' A 569  ARG  O  ', ' A 573  GLN  HB2', -0.461, (146.465, 124.604, 131.26)), (' A 572  HIS  O  ', ' A 576  LEU  HG ', -0.459, (143.112, 127.638, 128.361)), (' A 116  ARG  HG3', ' A 119  LEU HD11', -0.455, (111.097, 124.374, 82.35)), (' B  67  MET  HB3', ' B  67  MET  HE2', -0.454, (166.939, 116.716, 140.237)), (' C  66  VAL HG13', ' C  67  ASP  N  ', -0.454, (102.569, 123.351, 167.198)), (' A 612  PRO  O  ', ' A 613  HIS  HD2', -0.453, (122.992, 153.899, 115.823)), (' A 324  THR HG22', ' A 396  PHE  CZ ', -0.453, (122.394, 101.514, 121.983)), (' D  90  MET  O  ', ' D  94  MET  HG3', -0.453, (107.423, 133.446, 160.84)), (' A 722  ASN  HB3', ' A 726  ARG  NH1', -0.45, (136.379, 143.849, 94.745)), (' A 180  GLU  HA ', ' A 180  GLU  OE1', -0.449, (113.116, 110.159, 99.872)), (' A  74  ARG  HD3', ' A 111  VAL HG11', -0.448, (110.623, 136.929, 70.842)), (' A 483  TYR  CE1', ' A 582  THR HG21', -0.448, (143.746, 138.545, 124.27)), (' A  60  ASP  HB3', ' A  64  ASN  OD1', -0.445, (93.462, 117.279, 88.215)), (' A 605  VAL HG22', ' A 756  MET  HB2', -0.444, (132.238, 145.308, 122.984)), (' A 708  LEU  HA ', ' A 708  LEU HD23', -0.444, (126.818, 138.133, 98.821)), (' A 658  GLU  O  ', ' A 662  VAL HG22', -0.444, (135.514, 117.506, 125.35)), (' B  81  ALA  HA ', ' B  84  THR HG22', -0.443, (147.846, 104.19, 147.982)), (' A  52  ASN  HB3', ' A  73  LYS  HE2', -0.442, (112.774, 134.232, 81.147)), (' A 494  ILE HD11', ' A 577  LYS  HE3', -0.44, (147.057, 131.382, 135.979)), (' A  29  ASP  HB3', ' A  51  THR HG22', -0.437, (108.862, 139.839, 85.472)), (' A 611  ASN  ND2', ' A 769  THR  OG1', -0.436, (124.666, 155.841, 107.967)), (' A 603  LYS  HA ', ' A 603  LYS  HD2', -0.435, (133.09, 154.456, 124.449)), (' A 462  THR  CG2', ' A 627  PRO  HB3', -0.435, (124.436, 121.549, 114.789)), (' D 116  PRO  HD3', ' D 149  TYR  OH ', -0.433, (91.629, 121.48, 159.021)), (' C  22  VAL HG23', ' C  29  TRP  HE3', -0.431, (107.944, 117.319, 151.542)), (' A 426  LYS  HA ', ' A 426  LYS  HD3', -0.431, (113.47, 152.197, 157.643)), (' A 273  TYR  HB3', ' B 116  PRO  HG3', -0.43, (131.299, 98.642, 117.721)), (' B 161  ASP  HA ', ' B 184  LEU HD23', -0.43, (106.665, 102.375, 141.729)), (' A 749  LEU  HA ', ' A 749  LEU HD23', -0.427, (132.209, 143.762, 109.299)), (' A 466  ILE  HA ', ' A 466  ILE HD12', -0.427, (131.724, 123.606, 106.226)), (' D 160  VAL HG22', ' D 166  ILE HD13', -0.427, (80.898, 105.875, 156.629)), (' C  31  GLN  NE2', ' D 119  ILE HD12', -0.426, (98.544, 117.243, 147.956)), (' A 171  ILE  HA ', ' A 171  ILE HD12', -0.425, (106.688, 120.782, 111.419)), (' D 100  ASN  HB3', ' D 103  LEU HD12', -0.425, (95.513, 134.11, 155.692)), (' A 614  LEU  HB2', ' A 802  GLU  HB3', -0.425, (121.882, 150.092, 121.632)), (' C  50  GLU  O  ', ' C  53  VAL HG22', -0.424, (94.671, 128.018, 150.089)), (' D 117  LEU HD11', ' D 131  VAL HG23', -0.424, (90.3, 112.584, 160.064)), (' B  73  GLN  CD ', ' B  73  GLN  H  ', -0.423, (155.265, 111.384, 145.316)), (' A 610  GLU  O  ', ' A 612  PRO  HD3', -0.422, (127.943, 156.807, 113.662)), (' D 159  VAL HG13', ' D 167  VAL HG13', -0.421, (77.589, 110.108, 159.958)), (' D 122  LEU  HA ', ' D 190  ARG HH21', -0.419, (90.1, 124.574, 146.985)), (' A 540  THR  CG2', ' A 667  VAL  HA ', -0.418, (128.008, 112.725, 132.22)), (' A 588  VAL  O  ', ' A 588  VAL HG13', -0.418, (134.575, 140.517, 128.136)), (' C  23  GLU  HA ', ' C  29  TRP  HB2', -0.416, (108.854, 115.173, 149.722)), (' A  98  LYS  HB3', ' A  98  LYS  HE2', -0.415, (110.541, 117.224, 76.064)), (' A 366  LEU  HB3', ' A 371  LEU  HG ', -0.413, (146.634, 100.225, 138.767)), (' A 838  LEU  HA ', ' A 838  LEU HD23', -0.411, (117.691, 143.673, 148.983)), (' A 722  ASN  HB3', ' A 726  ARG HH12', -0.409, (136.575, 144.274, 94.791)), (' A 196  MET  CE ', ' A 232  PRO  HB3', -0.409, (127.778, 118.682, 85.21)), (' A 131  LEU  HA ', ' A 131  LEU HD23', -0.409, (113.393, 127.427, 105.595)), (' D 157  GLN  HG3', ' D 189  LEU HD13', -0.409, (81.123, 115.083, 147.712)), (' A 131  LEU HD13', ' A 247  LEU HD23', -0.408, (115.341, 123.033, 106.414)), (' A  89  LEU  HA ', ' A  89  LEU HD23', -0.408, (124.255, 115.177, 71.617)), (' A 634  ALA  HA ', ' A 693  VAL HG11', -0.408, (135.972, 127.675, 117.982)), (' A 665  GLU  H  ', ' A 665  GLU  HG2', -0.408, (129.761, 114.195, 126.732)), (' C  53  VAL HG12', ' D 103  LEU  HG ', -0.407, (94.922, 130.283, 154.641)), (' A 494  ILE  O  ', ' A 494  ILE HG13', -0.406, (146.497, 128.516, 137.39)), (' C  46  THR  O  ', ' C  50  GLU  HG2', -0.406, (93.137, 132.563, 147.215)), (' D 177  SER  O  ', ' D 182  TRP  NE1', -0.405, (78.714, 111.44, 171.828)), (' A 304  ASP  N  ', ' A 304  ASP  OD1', -0.405, (143.586, 122.316, 110.05)), (' A 619  TYR  HB2', ' A 622  CYS  HB2', -0.405, (122.534, 130.505, 123.296)), (' A 462  THR HG21', ' A 627  PRO  HB3', -0.404, (123.966, 121.614, 114.575)), (' B 103  LEU  HA ', ' B 103  LEU HD12', -0.404, (130.459, 89.311, 126.975)), (' A 331  ARG  O  ', ' A 341  VAL  HA ', -0.404, (138.077, 94.649, 128.232)), (' A 615  MET  HB3', ' A 615  MET  HE2', -0.403, (123.702, 144.804, 117.024)), (' D  97  LYS  HB3', ' D  97  LYS  HE2', -0.402, (103.816, 137.57, 159.822)), (' A 816  HIS  O  ', ' A 830  PRO  HA ', -0.402, (125.603, 149.098, 134.441)), (' A 164  ASP  OD2', ' A 167  GLU  HB2', -0.4, (108.094, 126.899, 120.527)), (' B  68  THR  O  ', ' B  72  LYS  HG2', -0.4, (160.11, 114.058, 144.561))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
