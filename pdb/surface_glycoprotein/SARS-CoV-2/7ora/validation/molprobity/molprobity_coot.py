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
data['rama'] = [('A', ' 109 ', 'ASP', 0.00515036553227743, (1.7086099999999993, -10.685429999999998, 84.58586)), ('D', ' 109 ', 'ASP', 0.018304760769616624, (8.66406, 5.51177, 131.26785))]
data['omega'] = [('A', ' 155 ', 'PRO', None, (20.987649999999995, 14.68085, 75.06608)), ('A', ' 157 ', 'PRO', None, (20.425469999999997, 12.30848, 80.86250000000004)), ('B', '   8 ', 'PRO', None, (-9.95048, 9.04725, 94.44989)), ('B', '  95 ', 'PRO', None, (-9.061800000000005, -3.41943, 73.97988)), ('B', ' 141 ', 'PRO', None, (0.12224999999999753, 21.98711, 100.91303)), ('D', ' 155 ', 'PRO', None, (26.095099999999995, -19.62793, 142.8203)), ('D', ' 157 ', 'PRO', None, (25.9643, -17.2718, 136.98055)), ('E', '   8 ', 'PRO', None, (-3.6791800000000077, -14.042049999999998, 121.87772)), ('E', '  95 ', 'PRO', None, (-2.984170000000005, -0.9503799999999993, 142.01927)), ('E', ' 141 ', 'PRO', None, (6.998039999999997, -27.10731, 115.77522)), ('F', ' 157 ', 'PRO', None, (-53.37859000000001, -42.5873, 40.91328)), ('F', ' 159 ', 'PRO', None, (-48.44034000000002, -40.92337999999997, 37.61824)), ('G', '   8 ', 'PRO', None, (-41.8337, -10.34808, 28.68168)), ('G', '  96 ', 'PRO', None, (-40.50743, -12.432429999999998, 52.54704)), ('G', ' 142 ', 'PRO', None, (-49.050520000000006, -20.65711999999999, 15.56899)), ('H', ' 157 ', 'PRO', None, (-49.93187, 37.22484, 171.49355)), ('H', ' 159 ', 'PRO', None, (-45.225030000000004, 35.94666999999999, 175.23535)), ('L', '   8 ', 'PRO', None, (-38.64131000000001, 5.101149999999996, 184.57275)), ('L', '  96 ', 'PRO', None, (-34.86398, 7.517459999999999, 160.9248)), ('L', ' 142 ', 'PRO', None, (-46.78143000000001, 15.839799999999991, 197.56977))]
data['rota'] = [('R', ' 417 ', 'LYS', 0.011314721525851544, (-18.92824, -26.416739999999997, 67.47082)), ('R', ' 518 ', 'LEU', 0.08013300678947151, (7.204399999999996, -21.558119999999985, 85.64323)), ('B', '  11 ', 'LEU', 0.19077647171076875, (-5.013510000000006, 12.09399, 98.29189000000004)), ('F', '   4 ', 'LEU', 0.13426937409706927, (-29.98980000000002, -32.64012999999999, 47.08736)), ('F', '  89 ', 'GLU', 0.28698919690476193, (-55.14964000000004, -26.720509999999983, 46.02958)), ('G', '  61 ', 'ASP', 0.1983059691640034, (-21.07788000000001, -16.88911, 28.92166)), ('C', ' 332 ', 'HIS', 0.028486824472648043, (8.18485, 16.955579999999998, 113.15615)), ('C', ' 417 ', 'LYS', 0.29431970741351393, (-12.309080000000002, 22.25257, 147.53862)), ('C', ' 518 ', 'LEU', 0.06437836273039863, (14.313099999999999, 16.38242, 130.24571)), ('H', '  89 ', 'GLU', 0.2741236865460336, (-50.47433000000002, 21.27496, 166.3108200000001)), ('H', ' 203 ', 'THR', 0.06964993955326795, (-49.150760000000034, 48.59455, 198.93826000000007)), ('H', ' 214 ', 'ASN', 0.2683658217823454, (-46.434370000000015, 46.9032, 173.97737)), ('L', '  61 ', 'ASP', 0.17635531452457834, (-18.390240000000002, 11.523529999999996, 186.71094000000005)), ('L', '  76 ', 'ILE', 0.1776058703136565, (-26.55873000000001, 8.86545, 188.97557000000006)), ('L', ' 101 ', 'GLN', 0.1262664947688297, (-40.38834000000002, 10.41449, 176.00616))]
data['cbeta'] = []
data['probe'] = [(' D  13  GLN  HB2', ' D  16  ARG  HD3', -0.776, (20.118, -15.147, 154.3)), (' L  46  ARG  NH2', ' L 401  HOH  O  ', -0.744, (-25.113, 19.204, 184.156)), (' E  39  LYS  NZ ', ' E 301  HOH  O  ', -0.664, (14.685, -5.876, 117.566)), (' D  50  VAL HG21', ' D 105  TYR  HB3', -0.634, (3.161, 5.782, 141.299)), (' G  32  SER  HB3', ' R 478  LYS  HG2', -0.625, (-24.653, -9.668, 46.574)), (' F 100  HIS  HB3', ' F 112  ILE HD11', -0.614, (-24.077, -26.333, 46.726)), (' A  13  GLN  HB2', ' A  16  ARG  HG3', -0.604, (14.769, 10.308, 61.726)), (' A 127  PRO  HB3', ' A 153  TYR  HB3', -0.603, (22.651, 21.426, 79.244)), (' E  61  ARG  NH1', ' E  82  ASP  OD2', -0.601, (8.064, -5.601, 112.777)), (' B 103  LYS  NZ ', ' B 406  HOH  O  ', -0.599, (1.845, 15.367, 94.994)), (' F 203  THR  OG1', ' F 220  LYS  NZ ', -0.595, (-51.319, -56.003, 14.918)), (' G  61  ASP  N  ', ' G  61  ASP  OD1', -0.594, (-20.764, -18.622, 27.866)), (' C 444  LYS  HD2', ' C 448  ASN  HA ', -0.591, (-27.252, 16.543, 133.905)), (' A  50  VAL HG21', ' A 105  TYR  HB3', -0.59, (-3.242, -10.649, 73.884)), (' H 100  HIS  HB3', ' H 112  ILE HD11', -0.584, (-19.639, 22.192, 167.9)), (' L  61  ASP  N  ', ' L  61  ASP  OD1', -0.582, (-18.075, 12.913, 187.703)), (' C 509  ARG  NH1', ' C 803  HOH  O  ', -0.571, (-16.455, 19.663, 124.619)), (' A  34  MET  HB3', ' A  79  LEU HD22', -0.571, (5.761, -9.677, 73.745)), (' H  38  ARG  HB3', ' H  48  ILE HD11', -0.571, (-39.824, 20.642, 165.124)), (' A 131  PRO  HD3', ' A 217  LYS  HE2', -0.565, (26.708, 31.215, 85.354)), (' D 131  PRO  HD3', ' D 217  LYS  HE2', -0.56, (32.781, -36.371, 132.445)), (' C 383  SER  HB3', ' C 386  LYS  HG2', -0.559, (7.856, 33.365, 126.18)), (' A  51  LEU HD11', ' A  55  GLY  HA2', -0.557, (2.22, -13.071, 66.404)), (' A  83  MET  HB3', ' A  86  LEU HD21', -0.554, (8.2, 3.648, 66.632)), (' D 127  PRO  HB3', ' D 153  TYR  HB3', -0.544, (27.824, -25.921, 138.909)), (' G  40  LYS  NZ ', ' G  82  GLU  O  ', -0.543, (-32.602, -26.226, 26.925)), (' R 383  SER  HB3', ' R 386  LYS  HG2', -0.537, (-0.048, -38.877, 88.676)), (' L  49  ILE HD13', ' L  55  GLY  HA2', -0.534, (-21.223, 11.278, 179.465)), (' D   2  VAL  HB ', ' D 110  VAL HG21', -0.534, (14.673, 7.754, 130.019)), (' G  38  GLN  HB2', ' G  48  LEU HD11', -0.532, (-31.979, -20.331, 32.142)), (' B  39  LYS  HG3', ' B  84  ALA  HB2', -0.53, (4.992, 3.887, 94.91)), (' F 174  HIS  ND1', ' F 403   CL CL  ', -0.524, (-45.629, -34.657, 19.685)), (' E  21  ILE HG21', ' E 102  THR HG21', -0.52, (0.53, -11.815, 120.864)), (' H  41  ARG  NH2', ' H 402  HOH  O  ', -0.517, (-52.164, 25.194, 177.22)), (' A 167  LEU HD21', ' A 190  VAL HG21', -0.515, (23.899, 24.99, 99.016)), (' B  35  TRP  CE2', ' B  73  PHE  HB2', -0.515, (-8.043, -0.966, 93.623)), (' R 393  THR  HA ', ' R 522  ALA  HA ', -0.513, (4.419, -22.267, 91.587)), (' R 383  SER  HB3', ' R 386  LYS  HE2', -0.51, (0.842, -38.894, 87.712)), (' E  39  LYS  HG3', ' E  84  ALA  HB2', -0.501, (11.736, -9.534, 121.313)), (' D  83  MET  HB3', ' D  86  LEU HD21', -0.501, (13.253, -8.276, 149.616)), (' I   1  NAG  H82', ' R 342  PHE  HB2', -0.501, (-16.945, -26.897, 93.482)), (' L  16  GLY  N  ', ' L  79  LEU  O  ', -0.496, (-28.616, 14.171, 195.795)), (' D  34  MET  HB3', ' D  79  LEU HD22', -0.495, (12.602, 5.114, 142.187)), (' G   6  GLN  O  ', ' G 101  GLN  NE2', -0.494, (-44.663, -11.289, 33.818)), (' C 518  LEU HD21', ' D  98  LYS  NZ ', -0.494, (11.225, 11.739, 131.954)), (' H 129  PRO  HB3', ' H 155  TYR  HB3', -0.492, (-53.194, 39.795, 177.732)), (' A  98  LYS  NZ ', ' R 518  LEU HD21', -0.489, (4.046, -17.204, 83.565)), (' C 383  SER  HB3', ' C 386  LYS  HE2', -0.487, (8.714, 33.693, 127.31)), (' L 163  SER  HB3', ' L 301  GOL  H31', -0.487, (-52.698, 28.249, 185.688)), (' F 129  PRO  HB3', ' F 155  TYR  HB3', -0.48, (-56.095, -44.851, 34.198)), (' G   2  ILE HD13', ' G  29  VAL HG12', -0.477, (-37.369, -6.303, 46.694)), (' E  35  TRP  CE2', ' E  73  PHE  HB2', -0.475, (-1.65, -3.783, 122.239)), (' B  46  LEU HD21', ' B  49  TYR  HB3', -0.472, (-2.952, -9.927, 89.912)), (' G  19  ALA  HB3', ' G  76  ILE  HB ', -0.471, (-31.699, -14.951, 24.972)), (' E  27  GLN  NE2', ' E 303  HOH  O  ', -0.467, (-12.095, -3.617, 138.351)), (' H  11  VAL HG21', ' H 157  PRO  HG3', -0.462, (-47.529, 36.242, 168.758)), (' C 417  LYS  HE3', ' C 455  LEU HD12', -0.459, (-16.856, 19.821, 149.69)), (' G  49  ILE HD13', ' G  55  GLY  HA2', -0.458, (-25.191, -15.93, 35.288)), (' H  73  ASP  HB3', ' H  76  THR HG22', -0.458, (-26.257, 31.146, 154.434)), (' F 161  THR HG23', ' F 209  ASN  HB3', -0.454, (-46.11, -47.531, 31.613)), (' R 478  LYS  HD2', ' R 478  LYS  N  ', -0.452, (-21.179, -11.167, 48.254)), (' D  51  LEU HD11', ' D  55  GLY  HA2', -0.451, (8.845, 8.791, 148.953)), (' F  91  THR HG23', ' F 120  THR  HA ', -0.45, (-51.333, -33.887, 44.248)), (' B  15  VAL HG11', ' E  60  SER  HB2', -0.45, (4.124, 4.511, 110.19)), (' G   8  PRO  HG3', ' G  11  LEU HD13', -0.448, (-41.204, -11.342, 25.088)), (' L  60  PRO  HB2', ' L  62  ARG  HG2', -0.446, (-21.681, 13.79, 188.72)), (' C 379  CYS  HA ', ' C 432  CYS  HA ', -0.446, (-0.253, 28.504, 131.253)), (' B  54  LEU HD21', ' B  60  SER  HA ', -0.445, (-2.333, -8.54, 102.18)), (' L   5  THR  HA ', ' L 101  GLN  OE1', -0.445, (-39.868, 5.495, 175.576)), (' R 331  HIS  O  ', ' R 332  HIS  ND1', -0.442, (2.365, -22.049, 101.015)), (' A 208  HIS  CD2', ' A 210  PRO  HD2', -0.441, (24.459, 14.448, 79.085)), (' F 106  CYS  N  ', ' R 475  ALA  O  ', -0.44, (-20.299, -18.885, 52.436)), (' F  60  TYR  HE1', ' F  70  ILE HG13', -0.438, (-41.182, -24.226, 56.903)), (' R 401  VAL HG22', ' R 509  ARG  HG2', -0.437, (-22.984, -24.969, 83.813)), (' C 345  THR  O  ', ' C 801  HOH  O  ', -0.435, (-19.211, 16.206, 125.076)), (' H 161  THR HG23', ' H 209  ASN  HB3', -0.434, (-43.57, 42.48, 181.232)), (' F  73  ASP  HB3', ' F  76  THR HG22', -0.433, (-31.654, -35.446, 60.088)), (' D 208  HIS  CD2', ' D 210  PRO  HD2', -0.433, (29.942, -19.046, 139.067)), (' R 334  ASN  N  ', ' R 334  ASN  OD1', -0.433, (-3.452, -20.901, 103.012)), (' L 114  PRO  HB3', ' L 140  PHE  CD2', -0.431, (-51.236, 22.488, 197.572)), (' C 475  ALA  O  ', ' H 106  CYS  N  ', -0.43, (-15.126, 14.704, 163.043)), (' L 194  ALA  HB2', ' L 209  SER  HB3', -0.43, (-67.39, 27.162, 198.941)), (' D  91  THR HG23', ' D 118  THR  HA ', -0.428, (16.556, -15.182, 142.902)), (' B 115  VAL  HA ', ' B 135  LEU  O  ', -0.428, (9.531, 31.348, 96.019)), (' B  37  GLN  HB2', ' B  47  LEU HD11', -0.427, (0.884, -1.039, 94.974)), (' L  48  LEU HD11', ' L  87  TYR  HE2', -0.426, (-28.141, 13.878, 183.252)), (' B  21  ILE HG21', ' B 102  THR HG21', -0.426, (-6.233, 6.733, 95.449)), (' E  80  PRO  O  ', ' E  83  ILE HD12', -0.425, (13.071, -12.148, 114.791)), (' C 393  THR  HA ', ' C 522  ALA  HA ', -0.424, (11.585, 16.709, 124.099)), (' E 140  TYR  CG ', ' E 141  PRO  HA ', -0.423, (7.888, -25.082, 115.731)), (' R 417  LYS  HA ', ' R 417  LYS  HD3', -0.422, (-18.775, -24.962, 65.928)), (' E  35  TRP  HB2', ' E  48  ILE  HB ', -0.419, (1.855, -0.654, 122.897)), (' A  52  SER  O  ', ' A  72  ARG  NH1', -0.419, (3.141, -15.162, 70.793)), (' H 194  VAL HG11', ' H 204  TYR  CE1', -0.416, (-47.459, 41.741, 199.767)), (' C 424  LYS  HD3', ' C 819  HOH  O  ', -0.415, (-3.383, 21.097, 147.138)), (' C 477  SER  OG ', ' H 108  ASP  OD2', -0.414, (-15.296, 9.642, 168.579)), (' D  34  MET  HE1', ' D  98  LYS  HG3', -0.414, (12.227, 9.115, 137.253)), (' F  50  TRP  CD1', ' F  59  ASN  HB2', -0.414, (-37.146, -17.602, 55.695)), (' C 455  LEU HD21', ' H  54  GLY  C  ', -0.414, (-20.859, 18.209, 151.175)), (' C 401  VAL HG22', ' C 509  ARG  HG2', -0.412, (-15.781, 20.424, 131.223)), (' L  15  PRO  HD3', ' L 107  ILE HG23', -0.412, (-34.757, 16.369, 197.077)), (' A   2  VAL  HB ', ' A 110  VAL HG21', -0.411, (7.588, -13.116, 86.028)), (' L  32  SER  HA ', ' L  51  GLY  HA2', -0.411, (-21.655, 5.282, 171.265)), (' B  47  LEU  HA ', ' B  58  VAL HG21', -0.411, (0.43, -6.964, 94.886)), (' B 145  LYS  HB3', ' B 197  THR  OG1', -0.41, (-2.176, 30.1, 92.467)), (' E 140  TYR  CD1', ' E 141  PRO  HA ', -0.409, (8.233, -24.472, 115.815)), (' L 141  TYR  CG ', ' L 142  PRO  HA ', -0.408, (-44.882, 16.473, 196.562)), (' F  64  PHE  HB3', ' F  68  VAL  CG2', -0.408, (-46.594, -23.662, 54.494)), (' R 379  CYS  SG ', ' R 384  PRO  HB3', -0.407, (-6.783, -36.432, 87.386)), (' F 193  THR HG21', ' G 138  ASN  ND2', -0.406, (-50.17, -35.587, 12.902)), (' A  60  TYR  CZ ', ' A  70  ILE HG22', -0.405, (1.227, -5.91, 66.089)), (' G  36  TRP  CE2', ' G  74  LEU  HB2', -0.404, (-32.777, -12.477, 33.74)), (' B 183  LYS  O  ', ' B 187  GLU  HG2', -0.404, (16.687, 42.765, 75.993)), (' F  38  ARG  HB3', ' F  48  ILE HD11', -0.404, (-44.575, -25.757, 47.839)), (' B  80  PRO  O  ', ' B  83  ILE HD12', -0.404, (6.351, 6.312, 102.091)), (' G 121  PRO  HD3', ' G 133  VAL HG22', -0.403, (-67.762, -40.054, 20.539)), (' A  91  THR HG23', ' A 118  THR  HA ', -0.402, (11.434, 9.971, 73.791)), (' B 193  ALA  HB2', ' B 208  SER  HB3', -0.4, (7.229, 42.308, 90.326)), (' F 164  TRP  CH2', ' F 206  CYS  HB3', -0.4, (-51.31, -46.952, 21.019)), (' B  45  LYS  HA ', ' B  45  LYS  HD3', -0.4, (5.029, -4.779, 89.407)), (' B  35  TRP  HB2', ' B  48  ILE  HB ', -0.4, (-5.025, -4.943, 92.662))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
