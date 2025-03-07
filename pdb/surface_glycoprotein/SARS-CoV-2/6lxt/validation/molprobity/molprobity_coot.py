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
data['rama'] = [('F', '1200 ', 'LEU', 0.008563640717596868, (-14.426, 5.78, -50.641))]
data['omega'] = []
data['rota'] = [('A', ' 933 ', 'LYS', 0.23492491813297253, (8.431, -9.084, -34.353)), ('A', ' 979 ', 'ASP', 0.05107379522590067, (-7.680000000000003, -8.509999999999996, 33.069)), ('A', ' 986 ', 'LYS', 0.00687674750788791, (-8.927, -4.989, 43.183)), ('A', '1166 ', 'LEU', 0.2387418414717601, (-9.607, -0.4600000000000001, 20.351)), ('A', '1172 ', 'ILE', 0.18047186100625265, (-9.593, -3.9879999999999995, 5.576)), ('A', '1175 ', 'SER', 0.11481275678251351, (-8.856, -7.6800000000000015, -3.604)), ('A', '1185 ', 'ARG', 0.012644355849032517, (-6.150000000000003, -14.007999999999996, -25.730999999999995)), ('A', '1199 ', 'ASP', 0.0008524462481643209, (3.354999999999999, -17.352, -49.351)), ('A', '1201 ', 'GLN', 0.11019118955631038, (2.313, -17.244, -55.831)), ('B', ' 914 ', 'ASN', 0.004466693930472884, (-2.4000000000000012, -11.858, -64.413)), ('B', ' 915 ', 'VAL', 0.02835479099303484, (-1.3050000000000002, -13.593, -61.104)), ('B', ' 939 ', 'SER', 0.2171028274892816, (-7.9410000000000025, -4.051000000000002, -26.667)), ('B', ' 982 ', 'SER', 0.2487283145130967, (1.8340000000000005, 5.085, 36.46099999999999)), ('B', '1163 ', 'ASP', 0.013128660184326103, (7.828000000000003, 5.346999999999999, 29.554)), ('B', '1165 ', 'ASP', 0.26570022742421423, (7.321, 4.164999999999998, 23.362)), ('B', '1169 ', 'ILE', 0.06496098942733916, (4.517, 3.1149999999999993, 11.504)), ('B', '1172 ', 'ILE', 0.2586402802041551, (4.798, 3.898, 5.848)), ('B', '1202 ', 'GLU', 0.055397914294889515, (-11.446, -3.427, -58.30599999999999)), ('C', ' 914 ', 'ASN', 0.04717908774504235, (-1.5000000000000009, 1.977, -63.392999999999994)), ('C', ' 979 ', 'ASP', 0.09553057743790061, (6.471, -7.2159999999999975, 33.362)), ('C', ' 985 ', 'ASP', 0.2593416565559888, (1.6960000000000002, -11.154999999999996, 41.152)), ('C', '1199 ', 'ASP', 0.0648985720044463, (10.428, 2.841, -48.978)), ('C', '1200 ', 'LEU', 0.1189489872202966, (9.872, 5.475, -51.748)), ('D', ' 937 ', 'SER', 0.05359990173019469, (-28.249000000000006, 7.752, -29.117)), ('D', ' 968 ', 'SER', 0.15496088518084028, (-32.493, 17.396, 16.694)), ('D', ' 986 ', 'LYS', 0.0, (-25.775000000000002, 15.517, 44.5)), ('D', '1164 ', 'VAL', 0.2129383397032888, (-21.37, 19.346, 26.708)), ('D', '1165 ', 'ASP', 0.23917981471551472, (-18.663, 19.111, 23.949999999999996)), ('D', '1172 ', 'ILE', 0.2578411646132031, (-23.35000000000001, 20.178, 6.627)), ('D', '1185 ', 'ARG', 0.0, (-32.392, 20.426999999999992, -25.393)), ('E', ' 939 ', 'SER', 0.11171901271031318, (-21.784000000000006, 20.698, -25.558)), ('E', ' 967 ', 'SER', 0.019507953559141818, (-17.831, 9.747999999999996, 14.988)), ('E', ' 979 ', 'ASP', 0.2866162598110806, (-18.236000000000008, 8.861000000000002, 33.502)), ('E', '1175 ', 'SER', 0.11409327465875954, (-16.139, 7.920999999999998, -3.054)), ('F', ' 967 ', 'SER', 0.02947994798887521, (-30.14600000000001, 3.9629999999999996, 14.206)), ('F', '1172 ', 'ILE', 0.2999152865417926, (-34.292, 7.842999999999997, 5.519)), ('F', '1175 ', 'SER', 0.09016097319772488, (-32.219, 5.085, -3.855)), ('F', '1181 ', 'LYS', 0.0, (-28.842, -0.45300000000000007, -20.577)), ('F', '1200 ', 'LEU', 0.07605201150584392, (-14.426, 5.78, -50.641)), ('F', '1201 ', 'GLN', 0.007285082423739811, (-13.615000000000006, 3.3080000000000007, -53.50599999999999))]
data['cbeta'] = [('E', '1168 ', 'ASP', ' ', 0.2638493125801488, (-16.737000000000002, 1.667, 14.276))]
data['probe'] = [(' A1184  ASP  OD2', ' A1303  PG4  H52', -1.094, (-8.073, -17.57, -24.545)), (' A 920  GLN  HG2', ' C 920  GLN HE22', -1.013, (3.018, -6.714, -55.523)), (' B 920  GLN  NE2', ' C 920  GLN  HG2', -0.908, (0.51, -3.198, -56.711)), (' A1188  GLU  HG2', ' A1303  PG4  O1 ', -0.906, (-8.136, -17.981, -28.657)), (' B 920  GLN HE21', ' C 920  GLN HE21', -0.881, (0.548, -4.534, -56.253)), (' D1185  ARG  HA ', ' D1185  ARG HH11', -0.862, (-33.13, 21.224, -25.725)), (' B 927  PHE  CZ ', ' B 931  ILE HD11', -0.83, (-2.761, -3.058, -42.453)), (' A1184  ASP  OD1', ' A1303  PG4  C6 ', -0.784, (-6.376, -19.497, -25.228)), (' A 983  ARG  HD2', ' C 984  LEU HD23', -0.782, (-3.062, -7.619, 37.17)), (' F 927  PHE  CZ ', ' F 931  ILE HD11', -0.774, (-22.227, 8.498, -42.221)), (' A1303  PG4  H42', ' A1303  PG4  O5 ', -0.764, (-10.517, -21.0, -25.832)), (' D 927  PHE  CZ ', ' D 931  ILE HD11', -0.755, (-28.334, 14.294, -42.141)), (' A 927  PHE  CZ ', ' A 931  ILE HD11', -0.75, (0.877, -10.149, -42.078)), (' A1184  ASP  OD1', ' A1303  PG4  H62', -0.749, (-6.06, -19.102, -25.482)), (' E 927  PHE  CZ ', ' E 931  ILE HD11', -0.739, (-20.791, 16.958, -41.23)), (' D1189  VAL HG13', ' E 933  LYS  HB3', -0.733, (-29.962, 18.585, -33.393)), (' A 920  GLN  CG ', ' C 920  GLN HE22', -0.715, (3.173, -6.3, -55.975)), (' D 984  LEU HD21', ' E 983  ARG  HB3', -0.714, (-21.746, 11.022, 38.504)), (' B 920  GLN HE22', ' C 920  GLN  HG2', -0.694, (-0.276, -2.923, -56.293)), (' E1166  LEU HD11', ' F 973  ILE HG13', -0.693, (-25.848, 5.328, 21.451)), (' A1184  ASP  CG ', ' A1303  PG4  H52', -0.674, (-7.424, -18.018, -24.31)), (' D1185  ARG  CA ', ' D1185  ARG HH11', -0.669, (-32.535, 21.709, -25.45)), (' D 912  THR  HB ', ' F 917  TYR  OH ', -0.662, (-18.128, 8.82, -64.54)), (' D 984  LEU HD21', ' E 983  ARG  HD3', -0.654, (-20.752, 12.262, 38.288)), (' D 984  LEU  CD2', ' E 983  ARG  HD3', -0.641, (-20.815, 12.715, 38.076)), (' D 933  LYS  NZ ', ' F1192  ASN  O  ', -0.634, (-23.502, 1.63, -37.914)), (' A1303  PG4  C4 ', ' A1303  PG4  C8 ', -0.631, (-9.821, -20.576, -26.489)), (' D 984  LEU HD21', ' E 983  ARG  CB ', -0.615, (-21.074, 10.853, 38.227)), (' A1303  PG4  C4 ', ' A1303  PG4  H82', -0.596, (-10.211, -20.483, -26.924)), (' B1189  VAL HG13', ' C 933  LYS  HB3', -0.594, (-2.167, 2.642, -34.278)), (' A 984  LEU HD21', ' B 983  ARG  HD3', -0.588, (-5.106, 1.473, 37.814)), (' B 920  GLN HE21', ' C 920  GLN  HG2', -0.582, (0.435, -4.115, -55.84)), (' D 984  LEU HD21', ' E 983  ARG  CD ', -0.577, (-20.61, 11.496, 38.505)), (' A 920  GLN  HG2', ' C 920  GLN  NE2', -0.565, (2.122, -6.199, -55.8)), (' B 984  LEU HD11', ' C 984  LEU HD12', -0.565, (0.797, -3.927, 38.965)), (' D 932  GLY  HA2', ' D 935  GLN HE21', -0.563, (-32.47, 8.86, -36.795)), (' E1182  GLU  OE1', ' F 943  SER  HB3', -0.562, (-15.111, 8.44, -19.526)), (' A1188  GLU  CG ', ' A1303  PG4  O1 ', -0.559, (-6.885, -17.393, -28.715)), (' A 933  LYS  HB3', ' C1189  VAL HG13', -0.549, (9.141, -6.606, -33.669)), (' E1164  VAL  CG1', ' F 976  VAL HG21', -0.549, (-24.738, 3.206, 26.274)), (' A 984  LEU HD11', ' B 983  ARG  HD3', -0.547, (-3.712, 0.925, 37.895)), (' C1200  LEU  H  ', ' C1200  LEU HD12', -0.544, (10.619, 5.875, -49.433)), (' D 984  LEU  O  ', ' D 984  LEU HD23', -0.539, (-23.003, 13.683, 39.776)), (' D1185  ARG  HA ', ' D1185  ARG  NH1', -0.538, (-33.857, 21.818, -26.028)), (' D 974  SER  HB2', ' D1164  VAL HG11', -0.533, (-24.82, 19.453, 24.486)), (' A1303  PG4  C4 ', ' A1303  PG4  O5 ', -0.528, (-10.983, -20.485, -25.887)), (' F 949  GLN  NE2', ' F1179  ILE  H  ', -0.523, (-27.631, 2.005, -14.611)), (' E1179  ILE HG22', ' F 947  LYS  HD2', -0.521, (-16.209, 9.296, -15.855)), (' A 984  LEU HD11', ' B 983  ARG  CB ', -0.52, (-2.859, 1.646, 37.73)), (' D1193  LEU HD23', ' E 933  LYS  HD2', -0.515, (-30.003, 17.756, -37.174)), (' B 920  GLN HE21', ' C 920  GLN  NE2', -0.513, (1.217, -4.489, -55.878)), (' C1200  LEU  N  ', ' C1200  LEU HD12', -0.51, (10.18, 5.909, -49.666)), (' D 916  LEU HD13', ' F 916  LEU HD13', -0.507, (-22.675, 14.389, -61.922)), (' A 984  LEU  CD2', ' B 983  ARG  HD3', -0.503, (-4.938, 0.779, 37.889)), (' A 984  LEU HD11', ' B 983  ARG  HB3', -0.493, (-2.808, 1.002, 38.138)), (' A1303  PG4  H41', ' A1303  PG4  H82', -0.488, (-10.943, -20.138, -26.847)), (' A1303  PG4  C2 ', ' A1303  PG4  O3 ', -0.484, (-9.545, -17.849, -26.476)), (' C1200  LEU  CD1', ' C1200  LEU  H  ', -0.482, (10.615, 6.077, -49.895)), (' E1164  VAL HG11', ' F 976  VAL HG21', -0.482, (-25.239, 3.43, 26.602)), (' A1201  GLN HE21', ' B 915  VAL HG22', -0.481, (-1.576, -16.747, -59.681)), (' D 936  ASP  HB3', ' F1185  ARG HH21', -0.48, (-31.63, 4.285, -30.795)), (' D 978  ASN  OD1', ' D1164  VAL HG23', -0.475, (-23.961, 19.497, 28.947)), (' D 984  LEU  CD2', ' E 983  ARG  CD ', -0.475, (-20.889, 12.204, 37.81)), (' E1200  LEU HD12', ' F 919  ASN  CG ', -0.47, (-19.338, 19.962, -54.627)), (' D1185  ARG  HG2', ' D1185  ARG  NH1', -0.469, (-32.819, 22.494, -24.734)), (' B 980  ILE  O  ', ' B 984  LEU HD23', -0.467, (0.066, -0.185, 36.187)), (' B 974  SER  O  ', ' B 978  ASN  ND2', -0.465, (1.505, 4.514, 26.874)), (' A 926  GLN  HB3', ' C1196  SER  O  ', -0.464, (8.216, -3.999, -44.426)), (' D1185  ARG  CG ', ' D1185  ARG HH11', -0.463, (-32.504, 22.447, -25.172)), (' A 987  VAL HG11', ' C 987  VAL HG11', -0.461, (-0.901, -3.864, 43.908)), (' A 972  ALA  O  ', ' A 976  VAL HG23', -0.459, (-4.463, -10.709, 25.702)), (' F1199  ASP  C  ', ' F1201  GLN  H  ', -0.458, (-15.31, 3.462, -51.094)), (' A 984  LEU  CD1', ' B 983  ARG  HD3', -0.457, (-4.176, 1.128, 37.527)), (' B 972  ALA  O  ', ' B 976  VAL HG23', -0.455, (-4.881, 2.699, 25.614)), (' A1303  PG4  H22', ' A1303  PG4  O3 ', -0.453, (-9.225, -17.814, -25.961)), (' A 923  ILE HG12', ' C1198  ILE HD13', -0.452, (5.254, -2.822, -49.097)), (' B 920  GLN  NE2', ' C 920  GLN HE21', -0.452, (0.402, -4.746, -56.263)), (' C 917  TYR  CE2', ' C 921  LYS  HE3', -0.447, (3.499, 4.906, -58.181)), (' B 914  ASN  N  ', ' B 914  ASN  OD1', -0.441, (-1.203, -10.568, -64.851)), (' F 928  ASN  ND2', ' F1200  LEU  CD2', -0.432, (-15.368, 7.513, -46.416)), (' A 986  LYS  HA ', ' A 986  LYS  HD3', -0.428, (-10.934, -4.636, 43.561)), (' B1169  ILE  H  ', ' B1169  ILE HD13', -0.427, (3.617, 3.779, 13.47)), (' F1199  ASP  O  ', ' F1201  GLN  N  ', -0.421, (-15.167, 3.928, -51.992)), (' A1185  ARG  NH1', ' A1301  PG4  H32', -0.42, (-11.113, -12.584, -30.1)), (' A1189  VAL HG13', ' B 933  LYS  HB3', -0.411, (-4.44, -11.56, -33.87)), (' E1164  VAL HG13', ' F 976  VAL HG21', -0.407, (-24.734, 2.681, 26.251)), (' C 978  ASN  HA ', ' C 978  ASN HD22', -0.405, (3.637, -11.03, 31.163)), (' F1195  GLU  HG3', ' F1195  GLU  O  ', -0.403, (-23.66, 0.185, -42.111)), (' D 932  GLY  HA2', ' D 935  GLN  NE2', -0.401, (-32.866, 9.241, -36.775))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
