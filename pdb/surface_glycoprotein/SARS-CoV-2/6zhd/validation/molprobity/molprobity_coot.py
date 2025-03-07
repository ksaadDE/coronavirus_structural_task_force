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
data['rama'] = [('A', ' 528 ', 'LYS', 0.025101932413191856, (142.078, 130.333, 185.468))]
data['omega'] = [('A', ' 544 ', 'ASN', None, (146.38300000000007, 129.607, 175.585))]
data['rota'] = [('A', ' 226 ', 'LEU', 0.07502080715266084, (122.23600000000003, 182.273, 176.795)), ('A', ' 519 ', 'HIS', 0.14931359202137892, (163.81500000000005, 135.021, 191.754)), ('A', ' 791 ', 'THR', 0.19897185681013083, (154.45400000000006, 189.299, 113.948)), ('A', '1094 ', 'VAL', 0.22684328129809342, (150.83700000000005, 152.617, 95.25)), ('A', '1107 ', 'ARG', 0.025617279255644807, (149.568, 156.738, 99.619)), ('B', ' 224 ', 'GLU', 0.26736899695231475, (196.55400000000006, 181.69499999999994, 173.415)), ('B', ' 226 ', 'LEU', 0.27284288117673144, (197.79600000000002, 181.449, 179.79)), ('B', ' 335 ', 'LEU', 0.20936718129521864, (140.215, 187.215, 197.576)), ('B', ' 574 ', 'ASP', 0.26594628429446293, (143.58600000000004, 185.80899999999994, 165.881)), ('B', ' 791 ', 'THR', 0.25133775900099004, (191.00300000000004, 153.754, 114.09499999999998)), ('B', ' 900 ', 'MET', 0.17712026733135705, (181.02900000000005, 160.236, 101.71099999999998)), ('B', ' 912 ', 'THR', 0.21862668282854153, (172.24, 167.997, 98.417)), ('B', ' 945 ', 'LEU', 0.25713122578076675, (181.18300000000002, 171.304, 133.822)), ('C', ' 226 ', 'LEU', 0.11334524605680617, (160.349, 116.53599999999997, 176.324)), ('C', ' 310 ', 'LYS', 0.015537588377757003, (175.73700000000005, 133.05599999999995, 141.15799999999996)), ('C', ' 335 ', 'LEU', 0.20798345262658907, (194.816, 160.697, 198.232)), ('C', ' 738 ', 'CYS', 0.052357881189664605, (147.201, 153.085, 159.581)), ('C', ' 790 ', 'LYS', 0.1836983001277652, (139.85, 142.093, 115.195)), ('C', ' 791 ', 'THR', 0.2111639828700633, (141.718, 140.13, 112.53)), ('C', ' 912 ', 'THR', 0.27294376058227576, (163.83800000000005, 149.829, 97.84)), ('C', '1012 ', 'LEU', 0.10357775404997416, (156.238, 156.62299999999993, 146.55))]
data['cbeta'] = [('A', ' 113 ', 'LYS', ' ', 0.34969324113478134, (113.62300000000003, 163.329, 199.36699999999996)), ('A', ' 913 ', 'GLN', ' ', 0.3014172030290088, (153.60000000000002, 170.86799999999997, 97.173)), ('B', ' 331 ', 'ASN', ' ', 0.27026259190722784, (138.885, 195.363, 186.862)), ('B', ' 519 ', 'HIS', ' ', 0.2652869426325499, (137.405, 177.558, 174.914)), ('B', ' 762 ', 'GLN', ' ', 0.39006391167023846, (165.032, 148.09699999999995, 154.943)), ('B', ' 913 ', 'GLN', ' ', 0.3450868377093235, (175.686, 164.538, 98.567)), ('C', ' 600 ', 'PRO', ' ', 0.33714788885102137, (180.24900000000005, 129.374, 141.265)), ('C', ' 762 ', 'GLN', ' ', 0.3690914998690601, (149.06600000000006, 162.712, 155.257)), ('C', ' 827 ', 'THR', ' ', 0.27909612790612853, (155.82300000000006, 132.886, 140.66899999999998)), ('C', ' 913 ', 'GLN', ' ', 0.31811655742575584, (159.13800000000006, 148.583, 97.776))]
data['probe'] = [(' C 112  SER  CB ', ' C 134  GLN  HG3', -1.075, (174.558, 114.779, 201.087)), (' C 809  PRO  HA ', ' C 814  LYS  NZ ', -1.073, (139.776, 133.423, 121.254)), (' C 328  ARG  HG3', ' C 579  PRO  HG2', -1.067, (198.721, 159.785, 180.368)), (' B  33  THR HG22', ' B 220  PHE  HD1', -0.985, (191.13, 189.424, 162.377)), (' A  81  ASN  O  ', ' A 239  GLN  NE2', -0.975, (104.634, 167.807, 183.171)), (' C 328  ARG  HG3', ' C 579  PRO  CG ', -0.947, (197.724, 159.444, 179.87)), (' C 809  PRO  HA ', ' C 814  LYS  HZ1', -0.919, (139.112, 132.872, 120.491)), (' B 770  ILE HD11', ' B1012  LEU HD23', -0.901, (167.887, 154.653, 145.971)), (' A1094  VAL HG11', ' C 904  TYR  OH ', -0.869, (150.155, 152.232, 99.12)), (' C 324  GLU  OE1', ' C 534  VAL HG21', -0.817, (199.913, 146.772, 173.629)), (' A1094  VAL  CG1', ' C 904  TYR  OH ', -0.807, (150.872, 152.055, 98.369)), (' C 599  THR HG22', ' C 601  GLY  H  ', -0.802, (177.338, 130.714, 144.177)), (' B 726  ILE HG13', ' B1061  VAL HG22', -0.788, (179.97, 167.944, 129.056)), (' C 770  ILE HD11', ' C1012  LEU HD12', -0.787, (154.138, 157.117, 146.499)), (' C 809  PRO  HA ', ' C 814  LYS  HZ2', -0.776, (139.065, 132.188, 121.889)), (' C 328  ARG  NH1', ' C 578  ASP  OD2', -0.759, (202.312, 157.468, 177.992)), (' A  33  THR HG22', ' A 220  PHE  HD1', -0.751, (120.401, 172.701, 159.183)), (' C  33  THR HG22', ' C 220  PHE  HD1', -0.744, (171.772, 118.56, 160.282)), (' B  33  THR HG22', ' B 220  PHE  CD1', -0.737, (192.044, 189.324, 162.395)), (' A  83  VAL HG22', ' A 239  GLN  OE1', -0.725, (106.437, 166.292, 184.825)), (' B 786  LYS  HG3', ' B 787  GLN  HG3', -0.716, (180.429, 144.393, 117.729)), (' A 900  MET  HE1', ' B1094  VAL  CG2', -0.711, (159.128, 178.418, 97.367)), (' C 786  LYS  HG3', ' C 787  GLN  HG3', -0.709, (138.915, 154.009, 117.051)), (' A 786  LYS  HG3', ' A 787  GLN  HG3', -0.701, (167.881, 184.86, 118.592)), (' B 327  VAL  H  ', ' B 531  THR HG22', -0.7, (149.754, 194.772, 180.368)), (' C 726  ILE  CG1', ' C1061  VAL HG22', -0.683, (159.225, 141.197, 127.916)), (' C 109  THR  O  ', ' C 110  LEU  HG ', -0.674, (179.013, 119.151, 193.011)), (' A 449  TYR  CD1', ' D 101  TYR  HD1', -0.673, (146.764, 120.537, 230.458)), (' B 413  GLY  HA3', ' C 987  PRO  HG3', -0.672, (147.422, 156.438, 186.14)), (' B 904  TYR  CE1', ' C1107  ARG  NH1', -0.67, (175.834, 158.224, 99.833)), (' A 726  ILE  CG1', ' A1061  VAL HG22', -0.669, (146.658, 173.217, 128.122)), (' C 308  VAL HG22', ' C 602  THR HG23', -0.668, (174.764, 129.207, 146.698)), (' B 905  ARG  HD2', ' B1049  LEU  O  ', -0.659, (176.064, 163.396, 110.438)), (' A 905  ARG  HD2', ' A1049  LEU  O  ', -0.659, (153.682, 171.763, 110.083)), (' B 726  ILE  CG1', ' B1061  VAL HG22', -0.654, (179.739, 167.646, 129.293)), (' C 905  ARG  HD2', ' C1049  LEU  O  ', -0.652, (158.036, 148.159, 110.032)), (' C 749  CYS  HB2', ' C 977  LEU HD21', -0.642, (147.434, 149.829, 170.908)), (' A  33  THR HG22', ' A 220  PHE  CD1', -0.632, (120.692, 173.243, 159.14)), (' C  33  THR HG22', ' C 220  PHE  CD1', -0.627, (171.686, 118.805, 160.293)), (' C 726  ILE HG12', ' C1061  VAL HG22', -0.625, (158.371, 141.02, 128.217)), (' A 563  GLN  OE1', ' C  43  PHE  HD1', -0.621, (154.308, 121.63, 163.688)), (' A 546  LEU  C  ', ' A 546  LEU HD12', -0.621, (146.401, 134.176, 171.826)), (' B  34  ARG  HD3', ' B 191  GLU  OE2', -0.611, (195.645, 193.274, 168.457)), (' A 900  MET  HE1', ' B1094  VAL HG23', -0.61, (159.05, 177.725, 98.026)), (' C 898  PHE  HZ ', ' C1050  MET  HE1', -0.61, (154.851, 142.221, 108.929)), (' A 726  ILE HG12', ' A1061  VAL HG22', -0.609, (146.427, 172.965, 128.804)), (' C 328  ARG  HG2', ' C 578  ASP  OD1', -0.607, (199.896, 158.897, 178.569)), (' B 484  GLU  OE2', ' F  52  ARG  NE ', -0.603, (126.538, 146.972, 208.556)), (' B 898  PHE  HZ ', ' B1050  MET  HE1', -0.6, (182.113, 163.937, 110.218)), (' A 196  ASN  HA ', ' A 200  TYR  O  ', -0.597, (125.846, 170.549, 181.55)), (' A 731  MET  N  ', ' A 774  GLN  OE1', -0.597, (156.789, 173.773, 139.942)), (' B 369  TYR  OH ', ' C 415  THR  HB ', -0.595, (159.441, 174.933, 194.721)), (' B 904  TYR  CE2', ' C1107  ARG  HD3', -0.595, (174.699, 156.018, 101.473)), (' B 496  GLY  O  ', ' B 501  ASN  ND2', -0.594, (145.365, 154.747, 213.731)), (' A  34  ARG  HD3', ' A 191  GLU  OE2', -0.594, (113.987, 175.216, 164.803)), (' B1029  MET  HE2', ' B1053  PRO  HB3', -0.594, (179.315, 159.372, 123.413)), (' C 731  MET  N  ', ' C 774  GLN  OE1', -0.593, (152.419, 149.596, 139.208)), (' A1028  LYS  O  ', ' A1032  CYS  HB3', -0.591, (156.616, 170.317, 120.204)), (' A 449  TYR  CD1', ' D 101  TYR  CD1', -0.591, (146.647, 121.303, 231.137)), (' B1028  LYS  O  ', ' B1032  CYS  HB3', -0.591, (173.527, 160.798, 120.386)), (' C 496  GLY  O  ', ' C 501  ASN  ND2', -0.591, (164.214, 168.366, 216.141)), (' C1028  LYS  O  ', ' C1032  CYS  HB3', -0.589, (156.863, 151.398, 119.761)), (' A1029  MET  HE2', ' A1053  PRO  HB3', -0.584, (155.328, 175.857, 123.342)), (' A 898  PHE  HZ ', ' A1050  MET  HE1', -0.582, (149.715, 177.141, 109.812)), (' B 731  MET  N  ', ' B 774  GLN  OE1', -0.579, (175.81, 157.908, 139.984)), (' B 749  CYS  HB2', ' B 977  LEU HD21', -0.578, (176.059, 151.887, 171.492)), (' A 449  TYR  CZ ', ' D 112  TRP  HZ2', -0.578, (144.623, 119.552, 232.745)), (' C1029  MET  HE2', ' C1053  PRO  HB3', -0.578, (152.135, 147.305, 122.483)), (' C 804  GLN  NE2', ' C 935  GLN  OE1', -0.578, (154.027, 129.236, 118.606)), (' B 533  LEU HD11', ' B 585  LEU HD11', -0.577, (143.422, 196.061, 173.37)), (' C 110  LEU  O  ', ' C 110  LEU HD12', -0.573, (177.989, 116.154, 194.458)), (' A 749  CYS  HB2', ' A 977  LEU HD21', -0.57, (159.156, 176.205, 171.694)), (' C 809  PRO  CA ', ' C 814  LYS  HZ1', -0.569, (139.537, 132.504, 120.254)), (' C 328  ARG  HD2', ' C 580  GLN  CG ', -0.568, (201.131, 158.494, 181.82)), (' C 328  ARG  NH2', ' C 533  LEU  HB2', -0.563, (201.934, 154.687, 177.302)), (' A  29  THR HG22', ' A  30  ASN  H  ', -0.56, (108.856, 166.563, 161.51)), (' C 726  ILE HG13', ' C1061  VAL HG22', -0.556, (159.223, 141.737, 127.684)), (' F   6  GLU  OE1', ' F 119  GLN  OE1', -0.556, (121.47, 151.913, 231.795)), (' B 903  ALA  HB1', ' B 913  GLN  HB2', -0.554, (176.986, 163.812, 99.267)), (' A 904  TYR  CE2', ' B1107  ARG  HD3', -0.554, (160.76, 174.685, 101.551)), (' E   6  GLU  OE1', ' E 119  GLN  OE1', -0.553, (174.664, 188.744, 236.362)), (' B 577  ARG  NH1', ' B 584  ILE HD11', -0.552, (133.778, 190.908, 171.48)), (' C 299  THR HG22', ' C 308  VAL HG11', -0.55, (174.335, 132.994, 149.558)), (' B1093  GLY  O  ', ' B1107  ARG  NH2', -0.547, (160.476, 173.159, 97.654)), (' A 904  TYR  CZ ', ' B1107  ARG  HD3', -0.546, (160.446, 174.423, 101.035)), (' A1028  LYS  O  ', ' A1032  CYS  CB ', -0.545, (157.252, 170.136, 120.426)), (' A 449  TYR  HB2', ' D 100  HIS  CD2', -0.543, (146.979, 117.572, 228.359)), (' B1028  LYS  O  ', ' B1032  CYS  CB ', -0.542, (172.747, 160.84, 120.232)), (' C 328  ARG HH22', ' C 533  LEU  HB2', -0.541, (202.344, 154.637, 177.264)), (' C 490  PHE  HB3', ' E 104  TYR  HA ', -0.54, (163.99, 185.767, 211.628)), (' D   6  GLU  OE1', ' D 119  GLN  OE1', -0.539, (150.525, 99.822, 239.379)), (' C  44  ARG  O  ', ' C 283  GLY  HA2', -0.539, (156.379, 123.298, 159.647)), (' C 484  GLU  OE1', ' E 106  LEU  HB2', -0.536, (162.489, 190.794, 215.075)), (' C 280  ASN  ND2', ' C 284  THR  OG1', -0.536, (159.568, 117.093, 158.18)), (' B 200  TYR  OH ', ' C 516  GLU  OE1', -0.536, (184.786, 174.92, 188.744)), (' B  41  LYS  HD3', ' C 562  PHE  O  ', -0.533, (194.999, 173.013, 176.835)), (' C1028  LYS  O  ', ' C1032  CYS  CB ', -0.533, (156.642, 151.779, 120.088)), (' C 809  PRO  CA ', ' C 814  LYS  NZ ', -0.53, (139.285, 132.12, 120.786)), (' A 726  ILE HG13', ' A1061  VAL HG22', -0.53, (146.779, 172.584, 127.8)), (' A1094  VAL HG13', ' C 904  TYR  OH ', -0.529, (151.31, 152.304, 98.475)), (' A 563  GLN  NE2', ' C  43  PHE  HA ', -0.527, (155.246, 123.785, 163.983)), (' A 501  ASN HD21', ' A 505  TYR  HB3', -0.527, (139.438, 127.256, 227.879)), (' C 231  ILE HD12', ' C 233  ILE  HB ', -0.526, (167.363, 123.861, 188.779)), (' B1031  GLU  OE1', ' B1039  ARG  NH1', -0.526, (165.468, 160.901, 120.658)), (' A  42  VAL HG22', ' B 519  HIS  CE1', -0.523, (136.818, 180.343, 172.036)), (' C 903  ALA  HB1', ' C 913  GLN  HB2', -0.518, (157.762, 147.937, 98.414)), (' C 865  LEU  N  ', ' C 865  LEU HD12', -0.515, (142.149, 148.319, 134.352)), (' A  81  ASN  N  ', ' A 265  TYR  HH ', -0.515, (104.065, 169.171, 178.125)), (' A  44  ARG  O  ', ' A 283  GLY  HA2', -0.508, (132.632, 182.842, 161.726)), (' A 449  TYR  HB2', ' D 100  HIS  HD2', -0.507, (147.428, 117.101, 228.132)), (' A1031  GLU  OE1', ' A1039  ARG  NH1', -0.506, (160.702, 163.629, 120.759)), (' A 105  ILE HG13', ' A 241  LEU HD11', -0.504, (108.831, 173.801, 186.294)), (' A 501  ASN  ND2', ' A 505  TYR  HB3', -0.504, (139.259, 127.658, 227.426)), (' B 231  ILE HD12', ' B 233  ILE  HB ', -0.503, (187.241, 185.834, 191.845)), (' A 377  PHE  HE2', ' A 384  PRO  HG3', -0.502, (138.788, 135.56, 201.073)), (' C1031  GLU  OE1', ' C1039  ARG  NH1', -0.501, (160.626, 158.093, 120.685)), (' B 578  ASP  OD2', ' B 581  THR  HB ', -0.495, (139.225, 196.384, 177.168)), (' A1107  ARG  HD3', ' C 904  TYR  CE2', -0.494, (152.08, 153.439, 101.506)), (' A 494  SER  OG ', ' D 102  VAL  HB ', -0.49, (151.008, 121.305, 228.881)), (' C 393  THR HG21', ' C 518  LEU  HB2', -0.49, (189.484, 172.619, 184.315)), (' A 533  LEU HD11', ' A 585  LEU HD11', -0.489, (138.623, 125.834, 169.127)), (' A  83  VAL HG11', ' A 237  ARG  HD3', -0.488, (110.182, 162.659, 185.854)), (' B 413  GLY  HA3', ' C 987  PRO  CG ', -0.487, (148.203, 156.145, 186.191)), (' A 377  PHE  HD1', ' A 434  ILE HG12', -0.487, (140.125, 131.704, 204.844)), (' C 749  CYS  CB ', ' C 977  LEU HD21', -0.485, (147.135, 150.227, 170.682)), (' A 912  THR  HB ', ' A 914  ASN  OD1', -0.484, (150.926, 166.575, 95.518)), (' A 722  VAL HG22', ' A1065  VAL HG22', -0.483, (145.999, 173.406, 114.781)), (' A 916  LEU HD12', ' A 923  ILE HD13', -0.482, (146.679, 172.546, 102.586)), (' C 105  ILE HG13', ' C 241  LEU HD11', -0.481, (173.119, 111.836, 188.933)), (' A 449  TYR  HB3', ' D 101  TYR  HA ', -0.48, (147.989, 119.462, 229.622)), (' B 105  ILE HG13', ' B 241  LEU HD11', -0.48, (196.138, 196.173, 190.792)), (' C1029  MET  HE2', ' C1053  PRO  CB ', -0.48, (152.142, 146.753, 122.474)), (' C 310  LYS  HB2', ' C 600  PRO  O  ', -0.48, (177.036, 131.331, 140.045)), (' B 904  TYR  CZ ', ' C1107  ARG  HD3', -0.479, (175.252, 156.162, 101.168)), (' A 484  GLU  HB2', ' D  57  SER  OG ', -0.479, (163.482, 121.874, 237.681)), (' C 125  ASN HD22', ' S   1  NAG  H3 ', -0.479, (159.183, 103.374, 189.466)), (' C 326  ILE HD12', ' C 539  VAL HG21', -0.478, (196.764, 151.12, 172.613)), (' A  64  TRP  HE1', ' A 264  ALA  HB1', -0.475, (102.597, 170.846, 168.712)), (' B 326  ILE HD12', ' B 539  VAL HG21', -0.474, (149.886, 195.055, 173.591)), (' B 722  VAL HG22', ' B1065  VAL HG22', -0.474, (181.118, 168.924, 115.543)), (' B 439  ASN  O  ', ' B 443  SER  OG ', -0.474, (146.055, 163.11, 216.72)), (' B  44  ARG  O  ', ' B 283  GLY  HA2', -0.473, (194.702, 173.921, 163.593)), (' C 898  PHE  CZ ', ' C1050  MET  HE1', -0.473, (154.722, 142.452, 108.939)), (' B1029  MET  HE2', ' B1053  PRO  CB ', -0.472, (179.473, 159.16, 123.404)), (' B 384  PRO  O  ', ' B 387  LEU  HB2', -0.472, (150.688, 179.053, 191.151)), (' A 699  LEU HD22', ' C 873  TYR  CZ ', -0.47, (140.185, 148.825, 126.967)), (' A 384  PRO  O  ', ' A 387  LEU  HB2', -0.47, (141.853, 134.362, 195.775)), (' C 105  ILE HD12', ' C 241  LEU HD21', -0.469, (175.316, 111.789, 189.577)), (' B 449  TYR  HB2', ' F 100  HIS  CD2', -0.468, (135.115, 155.865, 215.693)), (' A 105  ILE HD12', ' A 241  LEU HD21', -0.468, (107.321, 171.825, 186.507)), (' A 484  GLU  HB2', ' D  57  SER  CB ', -0.468, (162.606, 122.025, 237.358)), (' C 324  GLU  CD ', ' C 534  VAL HG21', -0.467, (200.09, 146.533, 174.84)), (' B  33  THR  CG2', ' B 220  PHE  HD1', -0.466, (191.483, 189.607, 162.196)), (' A1029  MET  HE2', ' A1053  PRO  CB ', -0.466, (154.964, 176.636, 123.26)), (' A 369  TYR  HB3', ' A 377  PHE  CZ ', -0.466, (138.927, 133.165, 200.72)), (' A 326  ILE HD12', ' A 539  VAL HG21', -0.465, (136.143, 132.415, 169.22)), (' C 916  LEU HD12', ' C 923  ILE HD13', -0.465, (161.163, 141.46, 102.712)), (' B 916  LEU HD12', ' B 923  ILE HD13', -0.464, (180.714, 169.422, 103.593)), (' C 728  PRO  HD2', ' C1021  SER  OG ', -0.464, (159.163, 149.578, 132.884)), (' A 803  SER  OG ', ' A 804  GLN  NE2', -0.463, (141.028, 185.962, 116.789)), (' C 916  LEU HD12', ' C 923  ILE  CD1', -0.462, (161.241, 141.234, 102.219)), (' C 722  VAL HG22', ' C1065  VAL HG22', -0.462, (160.219, 140.505, 114.386)), (' A  83  VAL  CG1', ' A 237  ARG  HG2', -0.462, (110.864, 163.713, 184.725)), (' A 703  ASN  O  ', ' C 789  TYR  HA ', -0.461, (138.7, 145.776, 114.859)), (' A 371  SER  O  ', ' B 486  PHE  CZ ', -0.461, (132.714, 130.17, 203.7)), (' C 328  ARG  CD ', ' C 580  GLN  CD ', -0.46, (200.713, 156.992, 181.748)), (' A 904  TYR  CE1', ' B1107  ARG  NH2', -0.46, (159.645, 174.018, 99.715)), (' A  83  VAL  CG1', ' A 237  ARG  CG ', -0.458, (110.313, 163.153, 184.641)), (' C 384  PRO  O  ', ' C 387  LEU  HB2', -0.457, (182.609, 155.891, 191.146)), (' O   1  NAG  H62', ' O   2  NAG  H82', -0.457, (184.77, 180.968, 107.152)), (' A 916  LEU HD12', ' A 923  ILE  CD1', -0.457, (146.431, 172.903, 102.541)), (' B 117  LEU  HG ', ' B 130  VAL HG12', -0.457, (192.288, 186.54, 192.775)), (' A 377  PHE  CZ ', ' A 384  PRO  HB3', -0.454, (139.846, 134.172, 200.784)), (' C 490  PHE  O  ', ' E 104  TYR  HB2', -0.454, (162.881, 185.525, 209.751)), (' A 101  ILE  HA ', ' A 242  LEU  HA ', -0.454, (103.746, 176.774, 179.633)), (' A 108  THR  HB ', ' H   1  NAG  H62', -0.453, (117.182, 160.478, 189.546)), (' B 916  LEU HD12', ' B 923  ILE  CD1', -0.453, (180.967, 169.57, 103.336)), (' B 413  GLY  O  ', ' C 987  PRO  HG2', -0.453, (148.685, 155.419, 187.137)), (' A 193  VAL HG13', ' A 270  LEU HD11', -0.452, (120.619, 170.37, 173.265)), (' B 287  ASP  OD1', ' B 288  ALA  N  ', -0.451, (189.687, 185.645, 159.904)), (' A  29  THR HG22', ' A  30  ASN  N  ', -0.451, (109.075, 166.51, 161.991)), (' B 749  CYS  CB ', ' B 977  LEU HD21', -0.449, (175.834, 152.017, 171.243)), (' B 898  PHE  CZ ', ' B1050  MET  HE1', -0.449, (182.635, 163.937, 110.038)), (' E   1  GLN  HA ', ' E 116  TYR  CZ ', -0.448, (175.966, 177.445, 227.415)), (' A 449  TYR  CB ', ' D 101  TYR  HA ', -0.448, (148.14, 118.968, 229.98)), (' A 898  PHE  CZ ', ' A1050  MET  HE1', -0.448, (150.031, 177.075, 109.576)), (' F   1  GLN  HA ', ' F 116  TYR  CZ ', -0.447, (131.246, 159.786, 223.87)), (' B  41  LYS  HG3', ' C 519  HIS  CE1', -0.447, (191.746, 175.233, 176.754)), (' B 104  TRP  HB3', ' B 106  PHE  CE1', -0.447, (193.487, 192.941, 186.368)), (' B1008  VAL  O  ', ' B1012  LEU  HG ', -0.447, (167.725, 156.937, 149.659)), (' D   1  GLN  HA ', ' D 116  TYR  CZ ', -0.445, (144.739, 107.917, 228.775)), (' B 721  SER  OG ', ' B1066  THR  OG1', -0.445, (175.913, 173.229, 115.363)), (' A 570  ALA  HB1', ' C 963  VAL HG11', -0.444, (153.515, 139.324, 158.044)), (' B 519  HIS  CD2', ' B 565  PHE  CZ ', -0.444, (139.907, 180.6, 173.279)), (' C 287  ASP  OD1', ' C 288  ALA  N  ', -0.443, (169.679, 121.984, 157.322)), (' B  41  LYS  HE2', ' C 519  HIS  O  ', -0.442, (192.265, 174.874, 180.211)), (' A 749  CYS  CB ', ' A 977  LEU HD21', -0.442, (159.656, 176.281, 171.559)), (' A 366  SER  HA ', ' A 369  TYR  CE2', -0.442, (137.246, 130.739, 195.989)), (' A 449  TYR  HH ', ' D 112  TRP  HZ2', -0.441, (144.035, 119.474, 233.637)), (' B 900  MET  HB2', ' B 900  MET  HE3', -0.44, (182.895, 158.564, 100.491)), (' A 377  PHE  CD2', ' A 377  PHE  O  ', -0.44, (138.877, 135.325, 204.202)), (' C 193  VAL HG13', ' C 270  LEU HD11', -0.439, (171.528, 122.343, 174.326)), (' B 105  ILE HD12', ' B 241  LEU HD21', -0.438, (195.546, 198.619, 191.082)), (' B  31  SER  HB3', ' B  62  VAL HG13', -0.438, (188.162, 197.833, 169.602)), (' C 721  SER  OG ', ' C1066  THR  OG1', -0.438, (166.432, 142.706, 114.369)), (' A 287  ASP  OD1', ' A 288  ALA  N  ', -0.438, (124.839, 173.274, 157.031)), (' A 557  LYS  HE2', ' A 586  ASP  OD1', -0.437, (145.28, 126.199, 159.543)), (' B 392  PHE  CD1', ' B 515  PHE  HB3', -0.437, (143.003, 175.982, 186.318)), (' C 328  ARG  HD2', ' C 580  GLN  CD ', -0.437, (200.89, 157.629, 181.644)), (' A 804  GLN  OE1', ' A 935  GLN  NE2', -0.437, (139.258, 183.409, 119.588)), (' C 489  TYR  HB3', ' E 104  TYR  HD2', -0.434, (160.167, 186.438, 210.337)), (' A 900  MET  HB3', ' A 900  MET  HE2', -0.434, (157.032, 177.889, 100.53)), (' A1089  PHE  HE2', ' C 917  TYR  CD2', -0.433, (157.57, 144.54, 94.644)), (' C 104  TRP  HB3', ' C 106  PHE  CE1', -0.432, (172.02, 115.232, 184.157)), (' A 439  ASN  O  ', ' A 443  SER  OG ', -0.431, (136.395, 119.908, 222.204)), (' B 193  VAL HG13', ' B 270  LEU HD11', -0.43, (188.285, 188.81, 176.528)), (' C 533  LEU HD11', ' C 585  LEU HD11', -0.43, (200.599, 157.006, 173.865)), (' A  83  VAL HG12', ' A 237  ARG  CG ', -0.429, (110.374, 163.04, 184.393)), (' C 822  LEU HD21', ' C 938  LEU HD13', -0.429, (157.694, 136.441, 127.021)), (' A1056  ALA  HB1', ' A1057  PRO  HD2', -0.429, (147.239, 178.263, 132.376)), (' B 554  GLU  N  ', ' B 554  GLU  OE1', -0.429, (142.357, 198.411, 165.591)), (' C 117  LEU  HG ', ' C 130  VAL HG12', -0.428, (165.853, 119.325, 190.169)), (' A 878  LEU  HA ', ' A 878  LEU HD12', -0.428, (153.837, 180.186, 117.458)), (' B 759  PHE  O  ', ' B 763  LEU  HG ', -0.427, (167.379, 151.194, 158.139)), (' A 642  VAL HG22', ' A 651  ILE HG12', -0.427, (124.376, 146.464, 148.764)), (' B 358  ILE  HB ', ' B 395  VAL  HB ', -0.427, (138.671, 177.523, 192.55)), (' A 575  ALA  HA ', ' A 585  LEU  O  ', -0.426, (144.915, 128.027, 163.785)), (' B 186  PHE  N  ', ' B 213  VAL HG12', -0.426, (205.84, 203.937, 169.524)), (' A 201  PHE  HE2', ' A 203  ILE HD11', -0.425, (119.136, 175.771, 181.869)), (' C 328  ARG  HD2', ' C 580  GLN  HG3', -0.425, (200.665, 158.702, 181.829)), (' A  33  THR  CG2', ' A 220  PHE  HD1', -0.423, (120.201, 172.85, 158.965)), (' A 914  ASN  ND2', ' A1111  GLU  OE2', -0.423, (148.235, 166.932, 92.754)), (' B 714  ILE  CD1', ' B1096  VAL HG11', -0.423, (164.9, 180.708, 97.409)), (' A 854  LYS  HE2', ' A 855  PHE  CE2', -0.423, (148.568, 186.476, 157.189)), (' C 358  ILE  HB ', ' C 395  VAL  HB ', -0.422, (187.076, 167.255, 194.192)), (' A  31  SER  HB3', ' A  62  VAL HG13', -0.422, (113.294, 166.096, 165.683)), (' B 329  PHE  CD1', ' B 391  CYS  SG ', -0.421, (143.918, 186.844, 184.665)), (' B1018  ILE  HA ', ' B1018  ILE HD13', -0.421, (171.225, 162.249, 137.589)), (' A  83  VAL  CG2', ' A 239  GLN  OE1', -0.419, (106.266, 165.547, 185.298)), (' C 914  ASN  ND2', ' C1111  GLU  OE2', -0.418, (165.695, 145.553, 93.34)), (' B 329  PHE  HD1', ' B 391  CYS  SG ', -0.417, (143.418, 186.59, 184.506)), (' C  33  THR  CG2', ' C 220  PHE  HD1', -0.417, (172.426, 118.488, 160.237)), (' C 109  THR  C  ', ' C 110  LEU  HG ', -0.417, (178.357, 119.272, 193.541)), (' B 543  PHE  O  ', ' B 546  LEU  HB3', -0.417, (144.848, 185.202, 177.398)), (' A 566  GLY  HA2', ' C  43  PHE  HB3', -0.416, (152.134, 126.085, 164.023)), (' C 773  GLU  OE2', ' C1019  ARG  HB2', -0.416, (154.372, 156.824, 138.442)), (' A 493  GLN  HA ', ' D 102  VAL HG12', -0.415, (153.231, 123.773, 230.308)), (' A 501  ASN  ND2', ' A 505  TYR  CB ', -0.415, (138.634, 127.876, 227.677)), (' B 822  LEU HD21', ' B 938  LEU HD13', -0.414, (185.138, 169.198, 128.325)), (' C 316  SER  OG ', ' C 317  ASN  N  ', -0.414, (180.354, 141.393, 158.497)), (' C 543  PHE  O  ', ' C 546  LEU  HB3', -0.413, (190.731, 160.387, 177.879)), (' B 327  VAL  H  ', ' B 531  THR  CG2', -0.413, (149.89, 195.239, 180.568)), (' C 714  ILE  CD1', ' C1096  VAL HG11', -0.412, (178.543, 149.937, 97.118)), (' C 328  ARG  NH1', ' C 578  ASP  CG ', -0.41, (201.434, 158.302, 178.183)), (' B 642  VAL HG22', ' B 651  ILE HG12', -0.409, (166.357, 199.89, 151.108)), (' A1139  ASP  HA ', ' A1140  PRO  HD3', -0.409, (156.438, 156.573, 79.347)), (' C  31  SER  HB3', ' C  62  VAL HG13', -0.408, (180.248, 117.772, 168.246)), (' A 715  PRO  HD3', ' C 894  LEU HD13', -0.408, (143.868, 155.949, 103.576)), (' C 392  PHE  CD1', ' C 515  PHE  HB3', -0.408, (183.662, 165.068, 187.652)), (' C 329  PHE  CD1', ' C 391  CYS  SG ', -0.406, (192.562, 159.865, 185.152)), (' C 575  ALA  HA ', ' C 585  LEU  O  ', -0.406, (196.32, 161.516, 168.854)), (' C 105  ILE  CD1', ' C 241  LEU HD21', -0.405, (174.866, 111.547, 189.773)), (' C 578  ASP  HB3', ' C 581  THR  O  ', -0.405, (202.253, 162.061, 176.902)), (' C 645  THR  OG1', ' C 646  ARG  N  ', -0.405, (191.67, 145.927, 143.23)), (' B 900  MET  HE2', ' C1079  PRO  HB3', -0.405, (182.643, 160.249, 97.779)), (' B1004  LEU  HA ', ' B1004  LEU HD23', -0.404, (171.877, 158.273, 157.708)), (' B 984  LEU HD13', ' B 988  GLU  HG3', -0.404, (172.084, 157.496, 182.779)), (' A 329  PHE  HE1', ' A 544  ASN  O  ', -0.403, (146.943, 131.11, 179.103)), (' C 329  PHE  HD1', ' C 391  CYS  SG ', -0.403, (192.94, 159.717, 184.867)), (' C 535  LYS  HD3', ' C 554  GLU  OE2', -0.403, (205.592, 155.247, 168.4)), (' C 280  ASN  ND2', ' C 284  THR  HG1', -0.402, (158.869, 117.768, 158.209)), (' B 105  ILE  CD1', ' B 241  LEU HD21', -0.402, (195.788, 198.348, 191.236)), (' A 714  ILE  CD1', ' A1096  VAL HG11', -0.401, (145.144, 153.493, 96.256)), (' A 900  MET  CE ', ' B1094  VAL HG23', -0.401, (158.332, 177.83, 97.942)), (' A 996  LEU  HA ', ' A 996  LEU HD23', -0.401, (154.608, 168.36, 170.208)), (' A  31  SER  O  ', ' A  59  PHE  N  ', -0.4, (115.839, 165.693, 161.026)), (' B 519  HIS  NE2', ' B 565  PHE  CE2', -0.4, (139.603, 181.269, 173.431))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
