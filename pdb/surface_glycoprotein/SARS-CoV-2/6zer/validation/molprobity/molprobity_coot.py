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
data['rama'] = [('G', ' 139 ', 'ASN', 0.022931372500017436, (181.54772, 41.46565, 86.80501)), ('L', ' 139 ', 'ASN', 0.022167297069628823, (111.15296, 88.61158, 3.02626))]
data['omega'] = [('B', ' 155 ', 'PRO', None, (93.77562999999996, 14.63076, 60.01531)), ('B', ' 157 ', 'PRO', None, (91.43181999999996, 14.85521, 65.78226)), ('C', '   8 ', 'PRO', None, (108.29314, 35.18126, 86.35168)), ('C', ' 142 ', 'PRO', None, (109.49003999999996, 19.069709999999993, 89.1225)), ('F', ' 155 ', 'PRO', None, (184.18157, 29.22414, 59.99958)), ('F', ' 157 ', 'PRO', None, (185.1786, 27.149589999999993, 65.78944)), ('G', '   8 ', 'PRO', None, (159.08226, 31.719400000000004, 86.27425)), ('G', ' 142 ', 'PRO', None, (172.38498, 40.89948, 89.03033)), ('H', ' 155 ', 'PRO', None, (98.80022, 84.8674, 29.62447)), ('H', ' 157 ', 'PRO', None, (96.63679999999995, 84.67344, 23.7875)), ('L', '   8 ', 'PRO', None, (113.89086999999999, 64.27963, 3.597540000000001)), ('L', ' 142 ', 'PRO', None, (115.25682999999998, 80.38090999999999, 0.85873))]
data['rota'] = [('E', ' 392 ', 'PHE', 0.0014102257563966293, (95.14702, 31.95981, 16.46665)), ('L', '  99 ', 'PHE', 0.2413731978311997, (106.07127999999997, 59.430949999999996, 15.08212)), ('A', ' 392 ', 'PHE', 0.0013985938535096645, (89.73685999999998, 67.55759, 73.10159)), ('B', '  98 ', 'LYS', 0.046006454231269235, (84.13828999999998, 42.418650000000014, 72.92453)), ('C', '  99 ', 'PHE', 0.22401522971965204, (100.74145999999998, 40.08031, 74.70699)), ('D', ' 392 ', 'PHE', 0.0013822168510545876, (140.55229999999995, -0.8175199999999998, 73.34531)), ('F', '  98 ', 'LYS', 0.048484992776759994, (165.10951, 6.971969999999999, 73.1398)), ('G', '  99 ', 'PHE', 0.22785419391987213, (158.69727, 22.66008, 74.68257))]
data['cbeta'] = []
data['probe'] = [(' F  39  GLN  HB2', ' F  45  LEU HD23', -0.731, (167.482, 21.933, 71.204)), (' H  39  GLN  HB2', ' H  45  LEU HD23', -0.723, (100.812, 67.401, 17.858)), (' B  39  GLN  HB2', ' B  45  LEU HD23', -0.723, (95.566, 32.804, 71.103)), (' G 212  ARG  NH2', ' G 301  PO4  O3 ', -0.685, (185.023, 64.13, 62.738)), (' D 377  PHE  CD1', ' D 434  ILE HG12', -0.65, (146.037, 10.8, 60.065)), (' E 377  PHE  CD1', ' E 434  ILE HG12', -0.638, (102.174, 41.95, 29.011)), (' A 377  PHE  CD1', ' A 434  ILE HG12', -0.633, (96.926, 57.576, 59.972)), (' H 172  HIS  HB3', ' H 174  PHE  HE1', -0.62, (107.422, 89.288, 10.19)), (' H 145  ALA  HB2', ' H 191  THR HG22', -0.62, (110.776, 97.465, 7.177)), (' B 145  ALA  HB2', ' B 191  THR HG22', -0.618, (105.049, 2.369, 82.406)), (' F 172  HIS  HB3', ' F 174  PHE  HE1', -0.616, (183.911, 38.003, 79.141)), (' L  39  LYS  HD3', ' L  84  ALA  HB2', -0.616, (98.723, 71.596, 4.348)), (' F  83  MET  HB3', ' F  86  LEU HD21', -0.615, (168.918, 19.3, 56.49)), (' B  83  MET  HB3', ' B  86  LEU HD21', -0.61, (92.762, 32.559, 56.3)), (' B 172  HIS  HB3', ' B 174  PHE  HE1', -0.609, (101.379, 10.444, 79.252)), (' F  92  ALA  HB3', ' F  94  TYR  HE1', -0.608, (169.107, 22.318, 64.23)), (' E 358  ILE  HB ', ' E 395  VAL  HB ', -0.607, (98.724, 29.692, 23.316)), (' H  92  ALA  HB3', ' H  94  TYR  HE1', -0.605, (100.012, 68.615, 25.116)), (' C  39  LYS  HD3', ' C  84  ALA  HB2', -0.605, (93.42, 27.695, 84.793)), (' B  92  ALA  HB3', ' B  94  TYR  HE1', -0.604, (95.442, 31.129, 64.114)), (' G  39  LYS  HD3', ' G  84  ALA  HB2', -0.604, (172.427, 22.427, 84.762)), (' C  37  GLN  HB2', ' C  47  LEU HD11', -0.603, (93.23, 35.511, 85.448)), (' E 342  PHE  HE1', ' E 511  VAL HG11', -0.603, (102.512, 35.207, 31.118)), (' H  83  MET  HB3', ' H  86  LEU HD21', -0.602, (97.297, 66.961, 32.511)), (' A 358  ILE  HB ', ' A 395  VAL  HB ', -0.601, (93.489, 69.476, 65.761)), (' A 392  PHE  HD2', ' A 515  PHE  HB3', -0.601, (93.187, 65.0, 71.718)), (' F 145  ALA  HB2', ' F 191  THR HG22', -0.601, (189.136, 44.838, 82.452)), (' E 392  PHE  HD2', ' E 515  PHE  HB3', -0.601, (98.54, 34.7, 17.739)), (' D 392  PHE  HD2', ' D 515  PHE  HB3', -0.598, (140.89, 3.865, 71.45)), (' D 342  PHE  HE1', ' D 511  VAL HG11', -0.598, (139.259, 7.727, 58.421)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.596, (99.016, 64.599, 3.826)), (' D 358  ILE  HB ', ' D 395  VAL  HB ', -0.595, (136.705, 1.175, 65.688)), (' H 152  ASP  OD1', ' H 179  GLN  NE2', -0.595, (109.32, 89.305, 29.377)), (' G  37  GLN  HB2', ' G  47  LEU HD11', -0.593, (166.361, 18.587, 85.431)), (' D 378  LYS  HA ', ' G  95  LEU HD12', -0.592, (149.209, 13.424, 63.908)), (' A 342  PHE  HE1', ' A 511  VAL HG11', -0.592, (98.136, 64.283, 58.336)), (' E 392  PHE  CD2', ' E 515  PHE  HB3', -0.587, (98.624, 34.827, 17.511)), (' A 392  PHE  CD2', ' A 515  PHE  HB3', -0.586, (93.132, 64.485, 71.441)), (' D 392  PHE  CD2', ' D 515  PHE  HB3', -0.586, (141.571, 3.69, 71.555)), (' D 377  PHE  HD1', ' D 434  ILE HG12', -0.585, (145.517, 10.76, 60.091)), (' B 152  ASP  OD1', ' B 179  GLN  NE2', -0.585, (104.807, 10.264, 60.197)), (' F 152  ASP  OD1', ' F 179  GLN  NE2', -0.579, (182.131, 40.263, 60.34)), (' D 377  PHE  HE2', ' F  59  TYR  HE1', -0.574, (150.782, 8.978, 61.175)), (' F 156  GLU  HG2', ' F 184  TYR  CE2', -0.574, (180.851, 30.29, 64.214)), (' E 377  PHE  HD1', ' E 434  ILE HG12', -0.572, (102.595, 42.525, 29.103)), (' A 377  PHE  HD1', ' A 434  ILE HG12', -0.57, (97.432, 56.934, 60.164)), (' D 386  LYS  HE3', ' F 101  GLY  HA2', -0.569, (157.093, 4.437, 74.169)), (' B 156  GLU  HG2', ' B 184  TYR  CE2', -0.568, (96.471, 16.81, 64.332)), (' F  52  SER  HB3', ' F  57  ASN  HB2', -0.568, (156.581, 3.865, 63.228)), (' H 156  GLU  HG2', ' H 184  TYR  CE2', -0.567, (101.991, 82.188, 24.97)), (' F 156  GLU  HG2', ' F 184  TYR  HE2', -0.564, (180.911, 29.969, 64.596)), (' L  32  TYR  HB3', ' L  91  SER  HB2', -0.562, (101.576, 50.082, 12.515)), (' H  52  SER  HB3', ' H  57  ASN  HB2', -0.561, (91.069, 47.965, 26.042)), (' C  32  TYR  HB3', ' C  91  SER  HB2', -0.56, (96.643, 49.623, 76.748)), (' E 450  ASN  N  ', ' E 450  ASN HD22', -0.56, (120.04, 30.734, 43.675)), (' B 156  GLU  HG2', ' B 184  TYR  HE2', -0.56, (95.915, 17.258, 64.605)), (' A 418  ILE HD13', ' A 422  ASN HD22', -0.56, (116.24, 62.696, 60.476)), (' E 418  ILE HD13', ' E 422  ASN HD22', -0.559, (120.706, 37.148, 29.505)), (' B  52  SER  HB3', ' B  57  ASN  HB2', -0.558, (85.818, 51.381, 62.957)), (' H 205  ASN  ND2', ' H 216  ASP  OD1', -0.556, (96.149, 101.522, 19.091)), (' H  38  ARG  NH1', ' H  90  ASP  OD1', -0.554, (102.583, 65.825, 29.076)), (' D 418  ILE HD13', ' D 422  ASN HD22', -0.554, (131.501, 23.936, 60.223)), (' H 156  GLU  HG2', ' H 184  TYR  HE2', -0.551, (101.397, 82.094, 24.778)), (' B 205  ASN  ND2', ' B 216  ASP  OD1', -0.551, (90.205, -1.992, 70.394)), (' A 386  LYS  HE3', ' B 101  GLY  HA2', -0.55, (85.949, 50.707, 73.928)), (' C 167  GLN HE21', ' C 172  SER  HB3', -0.547, (101.116, 19.026, 90.408)), (' G  32  TYR  HB3', ' G  91  SER  HB2', -0.547, (152.426, 14.052, 76.628)), (' L 167  GLN HE21', ' L 172  SER  HB3', -0.546, (107.281, 80.428, -1.046)), (' A 391  CYS  C  ', ' A 392  PHE  HD1', -0.545, (88.005, 65.787, 72.5)), (' D 391  CYS  C  ', ' D 392  PHE  HD1', -0.539, (143.052, -1.397, 72.93)), (' F 205  ASN  ND2', ' F 216  ASP  OD1', -0.538, (200.138, 34.776, 70.375)), (' B  40  ALA  HB3', ' B  43  LYS  HB2', -0.537, (101.331, 30.117, 68.665)), (' E 391  CYS  C  ', ' E 392  PHE  HD1', -0.536, (93.791, 33.605, 16.552)), (' G 167  GLN HE21', ' G 172  SER  HB3', -0.536, (176.663, 33.84, 90.34)), (' B 108  PHE  HE2', ' C  99  PHE  HZ ', -0.536, (94.289, 40.387, 72.509)), (' A 401  VAL HG22', ' A 509  ARG  HG2', -0.534, (106.35, 64.361, 52.241)), (' D 396  TYR  HB2', ' D 514  SER  OG ', -0.534, (135.373, 8.077, 68.244)), (' D 401  VAL HG22', ' D 509  ARG  HG2', -0.533, (135.468, 14.632, 51.845)), (' E 401  VAL HG22', ' E 509  ARG  HG2', -0.533, (110.866, 35.661, 37.375)), (' E 407  VAL HG21', ' E 508  TYR  HD2', -0.532, (111.817, 44.089, 34.796)), (' F  91  THR HG23', ' F 118  THR  HA ', -0.53, (173.932, 25.949, 61.535)), (' B  91  THR HG23', ' B 118  THR  HA ', -0.529, (96.2, 24.95, 61.488)), (' A 407  VAL HG21', ' A 508  TYR  HD2', -0.529, (107.594, 55.562, 55.554)), (' D 407  VAL HG21', ' D 508  TYR  HD2', -0.529, (141.983, 20.196, 55.445)), (' H  40  ALA  HB3', ' H  43  LYS  HB2', -0.528, (106.094, 69.543, 21.518)), (' H  91  THR HG23', ' H 118  THR  HA ', -0.527, (100.919, 74.57, 27.735)), (' E 396  TYR  HB2', ' E 514  SER  OG ', -0.527, (105.045, 31.56, 21.424)), (' F  40  ALA  HB3', ' F  43  LYS  HB2', -0.527, (167.398, 28.089, 68.203)), (' A 396  TYR  HB2', ' A 514  SER  OG ', -0.525, (99.661, 67.778, 67.999)), (' B 167  LEU HD21', ' B 190  VAL HG21', -0.52, (97.392, 0.501, 81.018)), (' H 167  LEU HD21', ' H 190  VAL HG21', -0.519, (103.351, 99.206, 8.252)), (' F 167  LEU HD21', ' F 190  VAL HG21', -0.516, (194.601, 39.388, 81.088)), (' B 208  HIS  CD2', ' B 210  PRO  HD2', -0.515, (90.687, 11.313, 62.599)), (' F 208  HIS  CD2', ' F 210  PRO  HD2', -0.515, (188.719, 28.321, 62.669)), (' H 208  HIS  CD2', ' H 210  PRO  HD2', -0.515, (95.794, 88.509, 26.421)), (' E 377  PHE  HE2', ' H  59  TYR  HE1', -0.51, (98.348, 46.061, 28.266)), (' A 377  PHE  HE2', ' B  59  TYR  HE1', -0.507, (93.069, 53.229, 61.125)), (' E 344  ALA  HB3', ' E 347  PHE  HE1', -0.506, (105.217, 30.583, 37.276)), (' F 191  THR HG21', ' G 138  ASN  ND2', -0.504, (187.354, 43.526, 84.092)), (' H 191  THR HG21', ' L 138  ASN  ND2', -0.503, (110.058, 94.718, 5.309)), (' H  35  HIS  ND1', ' H  50  VAL HG22', -0.5, (95.218, 54.524, 20.792)), (' G  37  GLN  HG3', ' G  86  TYR  HE1', -0.5, (168.246, 21.363, 85.615)), (' E 367  VAL HG21', ' E 601  NAG  H83', -0.5, (94.455, 34.214, 34.584)), (' A 367  VAL HG21', ' A 601  NAG  H83', -0.499, (89.392, 65.157, 54.551)), (' B  35  HIS  ND1', ' B  50  VAL HG22', -0.499, (90.138, 44.554, 68.463)), (' A 344  ALA  HB3', ' A 347  PHE  HE1', -0.498, (100.521, 68.836, 52.224)), (' D 367  VAL HG21', ' D 601  NAG  H83', -0.498, (143.282, -0.374, 55.075)), (' D 344  ALA  HB3', ' D 347  PHE  HE1', -0.497, (134.003, 7.87, 52.704)), (' H 108  PHE  HE2', ' L  99  PHE  HZ ', -0.497, (99.558, 58.952, 16.67)), (' L  37  GLN  HG3', ' L  86  TYR  HE1', -0.496, (99.987, 67.044, 3.707)), (' C  37  GLN  HG3', ' C  86  TYR  HE1', -0.496, (94.4, 32.145, 85.357)), (' H 191  THR HG21', ' L 138  ASN HD22', -0.496, (110.358, 94.795, 5.37)), (' D 393  THR  HA ', ' D 522  ALA  HA ', -0.493, (136.967, -3.102, 74.284)), (' F  38  ARG  NH1', ' F  90  ASP  OD1', -0.492, (165.741, 22.4, 60.585)), (' F  35  HIS  ND1', ' F  50  VAL HG22', -0.491, (160.172, 11.019, 68.678)), (' E 429  PHE  O  ', ' L  92  TYR  OH ', -0.489, (107.107, 41.956, 15.808)), (' G   1  ASP  OD1', ' G   2  ILE  N  ', -0.488, (150.341, 23.77, 69.218)), (' F  45  LEU  HB2', ' G  99  PHE  CD2', -0.486, (163.276, 21.444, 73.671)), (' B  38  ARG  NH1', ' B  90  ASP  OD1', -0.485, (97.163, 34.13, 60.464)), (' G 145  ALA  HB2', ' G 199  HIS  HD2', -0.483, (172.87, 44.844, 84.988)), (' D 437  ASN  HA ', ' D 508  TYR  CD1', -0.482, (142.033, 18.765, 50.612)), (' A 393  THR  HA ', ' A 522  ALA  HA ', -0.481, (89.069, 71.302, 74.06)), (' A 392  PHE  HD1', ' A 392  PHE  N  ', -0.481, (88.743, 65.743, 72.395)), (' G 121  PRO  HD3', ' G 133  VAL HG22', -0.481, (183.906, 52.832, 68.065)), (' L 145  ALA  HB2', ' L 199  HIS  HD2', -0.481, (118.017, 82.62, 5.31)), (' E 437  ASN  HA ', ' E 508  TYR  CD1', -0.479, (110.703, 43.361, 38.938)), (' C 145  ALA  HB2', ' C 199  HIS  HD2', -0.479, (112.415, 16.615, 84.641)), (' C 159  ASN  ND2', ' D 468  ILE HD11', -0.478, (118.887, 13.752, 62.637)), (' E 386  LYS  HE3', ' H 101  GLY  HA2', -0.476, (91.428, 48.46, 15.289)), (' D 497  PHE  CE2', ' D 507  PRO  HB3', -0.476, (135.004, 20.629, 49.181)), (' E 392  PHE  HD1', ' E 392  PHE  N  ', -0.476, (94.123, 33.764, 17.126)), (' C 121  PRO  HD3', ' C 133  VAL HG22', -0.474, (114.226, 2.552, 68.06)), (' E 380  TYR  CE2', ' E 412  PRO  HD2', -0.473, (110.08, 44.071, 20.436)), (' L 121  PRO  HD3', ' L 133  VAL HG22', -0.473, (119.491, 96.823, 21.784)), (' F  18  LEU  HB3', ' F  83  MET  HE3', -0.473, (172.392, 17.316, 56.834)), (' A 437  ASN  HA ', ' A 508  TYR  CD1', -0.472, (106.282, 56.401, 50.861)), (' E 393  THR  HA ', ' E 522  ALA  HA ', -0.472, (94.613, 27.837, 15.278)), (' A 393  THR HG21', ' A 518  LEU  H  ', -0.47, (92.546, 70.562, 77.549)), (' D 392  PHE  HD1', ' D 392  PHE  N  ', -0.47, (142.394, -1.213, 72.692)), (' G  62  PHE  CD1', ' G  75  ILE HG12', -0.47, (164.847, 19.407, 91.856)), (' H 174  PHE  CE2', ' L 177  SER  HB3', -0.469, (111.038, 88.948, 13.29)), (' D 392  PHE  CD1', ' D 392  PHE  N  ', -0.469, (142.18, -1.02, 72.433)), (' A 497  PHE  CE2', ' A 507  PRO  HB3', -0.468, (111.525, 61.472, 49.387)), (' E 393  THR HG21', ' E 518  LEU  H  ', -0.468, (97.929, 29.144, 12.107)), (' B  20  LEU  HG ', ' B  83  MET  HE2', -0.467, (88.091, 31.715, 59.506)), (' G 149  TRP  NE1', ' G 178  SER  OG ', -0.467, (176.513, 48.558, 72.274)), (' A 380  TYR  CE2', ' A 412  PRO  HD2', -0.466, (104.894, 55.809, 69.299)), (' B 191  THR HG21', ' C 138  ASN  ND2', -0.465, (104.324, 4.77, 84.315)), (' H 103  LEU HD11', ' L  50  ALA  HB2', -0.465, (97.821, 49.437, 7.986)), (' D 380  TYR  CE2', ' D 412  PRO  HD2', -0.465, (143.041, 17.907, 69.2)), (' H  18  LEU  HB3', ' H  83  MET  HE3', -0.462, (94.577, 68.713, 32.285)), (' A 392  PHE  CD1', ' A 392  PHE  N  ', -0.462, (88.923, 65.85, 72.147)), (' D 393  THR HG21', ' D 518  LEU  H  ', -0.461, (136.448, -0.224, 77.458)), (' B  18  LEU  HB3', ' B  83  MET  HE3', -0.461, (89.835, 31.016, 57.028)), (' E 450  ASN  N  ', ' E 450  ASN  ND2', -0.461, (119.861, 30.203, 43.873)), (' E 497  PHE  CE2', ' E 507  PRO  HB3', -0.461, (115.924, 38.38, 40.402)), (' H  20  LEU  HG ', ' H  83  MET  HE2', -0.461, (93.415, 67.843, 30.056)), (' H  29  PHE  O  ', ' H  72  ARG  NH2', -0.46, (83.725, 54.161, 21.646)), (' B  29  PHE  O  ', ' B  72  ARG  NH2', -0.46, (78.484, 45.741, 67.358)), (' F  20  LEU  HG ', ' F  83  MET  HE2', -0.458, (171.846, 15.76, 59.325)), (' L   1  ASP  OD1', ' L   2  ILE  N  ', -0.458, (111.143, 52.797, 20.653)), (' C 149  TRP  NE1', ' C 178  SER  OG ', -0.457, (114.202, 11.715, 72.563)), (' C  62  PHE  CD1', ' C  75  ILE HG12', -0.457, (95.1, 36.213, 91.929)), (' E 392  PHE  CD1', ' E 392  PHE  N  ', -0.455, (94.374, 33.687, 17.122)), (' F 191  THR HG21', ' G 138  ASN HD22', -0.455, (187.289, 43.802, 84.244)), (' C   1  ASP  OD1', ' C   2  ILE  N  ', -0.455, (105.993, 46.686, 69.218)), (' F 124  THR HG22', ' F 155  PRO  HD3', -0.453, (184.54, 27.705, 57.658)), (' F  29  PHE  O  ', ' F  72  ARG  NH2', -0.453, (165.318, 0.437, 68.14)), (' H 124  THR HG22', ' H 155  PRO  HD3', -0.451, (97.241, 84.798, 31.784)), (' B  47  TRP  CZ2', ' B  50  VAL HG23', -0.45, (92.791, 45.292, 66.22)), (' H  47  TRP  CZ2', ' H  50  VAL HG23', -0.45, (97.382, 54.017, 23.028)), (' L  62  PHE  CD1', ' L  75  ILE HG12', -0.45, (100.383, 63.082, -2.467)), (' D 377  PHE  HE2', ' F  59  TYR  CE1', -0.448, (151.319, 8.723, 61.54)), (' H  45  LEU  HB2', ' L  99  PHE  CD2', -0.445, (102.913, 62.552, 15.533)), (' B 124  THR HG22', ' B 155  PRO  HD3', -0.442, (92.414, 14.952, 57.674)), (' F 108  PHE  HE2', ' G  99  PHE  HZ ', -0.441, (161.783, 17.175, 72.996)), (' F  47  TRP  CZ2', ' F  50  VAL HG23', -0.44, (158.131, 12.839, 66.423)), (' D 339  GLY  CA ', ' D 601  NAG  H82', -0.439, (140.088, -0.071, 53.822)), (' E 359  SER  OG ', ' E 394  ASN  OD1', -0.439, (98.835, 24.934, 19.997)), (' D 420  ASP  HB3', ' D 460  ASN  OD1', -0.438, (130.497, 27.768, 68.987)), (' E 339  GLY  CA ', ' E 601  NAG  H82', -0.436, (96.116, 31.808, 35.713)), (' A 339  GLY  CA ', ' A 601  NAG  H82', -0.435, (91.329, 67.823, 53.613)), (' D 502  GLY  O  ', ' D 506  GLN  HG3', -0.435, (141.758, 25.338, 47.262)), (' L 149  TRP  NE1', ' L 178  SER  OG ', -0.433, (119.658, 87.718, 17.503)), (' D 497  PHE  CD2', ' D 507  PRO  HB3', -0.431, (135.032, 20.638, 49.076)), (' E 497  PHE  CD2', ' E 507  PRO  HB3', -0.431, (116.067, 38.313, 40.996)), (' A 431  GLY  HA2', ' A 515  PHE  HD2', -0.431, (96.452, 61.443, 69.496)), (' B 191  THR HG21', ' C 138  ASN HD22', -0.431, (104.73, 5.112, 84.353)), (' B  47  TRP  HZ2', ' B  50  VAL HG23', -0.431, (92.351, 45.538, 66.406)), (' H  47  TRP  HZ2', ' H  50  VAL HG23', -0.43, (97.315, 53.97, 23.173)), (' A 359  SER  OG ', ' A 394  ASN  OD1', -0.43, (93.434, 74.626, 69.718)), (' A 502  GLY  O  ', ' A 506  GLN  HG3', -0.429, (112.782, 53.328, 47.528)), (' F  47  TRP  HZ2', ' F  50  VAL HG23', -0.429, (157.947, 12.655, 66.415)), (' G  99  PHE  CD1', ' G  99  PHE  N  ', -0.428, (159.116, 21.33, 73.444)), (' D 412  PRO  HB3', ' D 426  PRO  O  ', -0.428, (139.451, 17.811, 73.189)), (' C  99  PHE  CD1', ' C  99  PHE  N  ', -0.427, (99.374, 40.547, 73.257)), (' E 502  GLY  O  ', ' E 506  GLN  HG3', -0.427, (117.083, 46.724, 42.681)), (' E 420  ASP  HB3', ' E 460  ASN  OD1', -0.427, (124.745, 37.808, 21.178)), (' L  99  PHE  CD1', ' L  99  PHE  N  ', -0.427, (104.67, 58.957, 16.278)), (' E 412  PRO  HB3', ' E 426  PRO  O  ', -0.426, (111.693, 40.872, 17.088)), (' F 105  VAL HG12', ' F 106  TYR  N  ', -0.426, (153.933, 10.81, 73.835)), (' A 420  ASP  HB3', ' A 460  ASN  OD1', -0.426, (119.617, 61.759, 69.34)), (' A 497  PHE  CD2', ' A 507  PRO  HB3', -0.426, (111.499, 61.504, 49.285)), (' E 431  GLY  HA2', ' E 515  PHE  HD2', -0.425, (101.494, 38.308, 20.243)), (' B 103  LEU HD11', ' C  50  ALA  HB2', -0.424, (92.436, 50.124, 81.539)), (' A 412  PRO  HB3', ' A 426  PRO  O  ', -0.424, (106.352, 58.786, 72.971)), (' H 105  VAL HG12', ' H 106  TYR  N  ', -0.421, (98.253, 49.307, 15.882)), (' B 105  VAL HG12', ' B 106  TYR  N  ', -0.421, (93.145, 50.101, 73.465)), (' B  57  ASN  HB3', ' B  59  TYR  CE2', -0.42, (89.104, 51.576, 62.488)), (' G 109  ARG  HD3', ' G 110  THR  O  ', -0.419, (175.958, 39.43, 94.0)), (' F 192  VAL HG11', ' F 202  TYR  CE1', -0.419, (197.03, 43.037, 82.029)), (' D 431  GLY  HA2', ' D 515  PHE  HD2', -0.419, (142.5, 7.945, 69.447)), (' F  57  ASN  HB3', ' F  59  TYR  CE2', -0.418, (154.541, 6.408, 62.773)), (' H 192  VAL HG11', ' H 202  TYR  CE1', -0.418, (104.86, 102.901, 7.612)), (' H  57  ASN  HB3', ' H  59  TYR  CE2', -0.418, (93.929, 47.725, 26.902)), (' H  67  ARG  NH1', ' H  90  ASP  OD2', -0.418, (101.955, 65.705, 33.565)), (' H 145  ALA  HB3', ' L 117  PHE  CD2', -0.416, (113.278, 97.638, 8.618)), (' B 192  VAL HG11', ' B 202  TYR  CE1', -0.416, (99.021, -3.4, 82.208)), (' D 403  ARG  NH1', ' D 405  ASP  HB2', -0.415, (139.085, 28.42, 55.203)), (' B  45  LEU  HB2', ' C  99  PHE  CD2', -0.415, (97.555, 37.061, 73.964)), (' A 403  ARG  NH1', ' A 405  ASP  HB2', -0.414, (115.72, 53.903, 55.688)), (' F 103  LEU HD11', ' G  50  ALA  HB2', -0.413, (154.194, 10.467, 81.575)), (' L 109  ARG  HD3', ' L 110  THR  O  ', -0.413, (112.303, 82.703, -4.109)), (' A 351  TYR  HE1', ' A 452  LEU  HB2', -0.412, (116.16, 70.294, 55.611)), (' B 145  ALA  HB3', ' C 117  PHE  CD2', -0.411, (107.124, 1.857, 81.309)), (' D 388  ASN  O  ', ' D 527  PRO  HD2', -0.41, (148.546, -4.338, 66.254)), (' C 109  ARG  HD3', ' C 110  THR  O  ', -0.409, (106.433, 16.789, 94.002)), (' D 351  TYR  HE1', ' D 452  LEU  HB2', -0.408, (125.154, 20.607, 55.093)), (' B 174  PHE  CE2', ' C 177  SER  HB3', -0.408, (105.328, 10.627, 76.463)), (' E 403  ARG  NH1', ' E 405  ASP  HB2', -0.407, (120.869, 45.869, 34.823)), (' A 357  ARG  HG3', ' A 396  TYR  HE1', -0.407, (97.682, 73.712, 68.765)), (' A 388  ASN  O  ', ' A 527  PRO  HD2', -0.407, (82.909, 62.247, 66.246)), (' A 377  PHE  HE2', ' B  59  TYR  CE1', -0.405, (92.855, 53.353, 61.384)), (' F 174  PHE  CE2', ' G 177  SER  HB3', -0.404, (181.922, 41.771, 76.123)), (' E 378  LYS  HA ', ' L  95  LEU HD12', -0.401, (102.717, 46.761, 25.577)), (' B  34  MET  HB3', ' B  79  LEU HD22', -0.4, (83.464, 41.476, 66.479))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
