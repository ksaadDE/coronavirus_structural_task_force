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
data['omega'] = [('A', ' 505 ', 'PRO', None, (178.36799999999988, 178.979, 178.245)), ('B', ' 183 ', 'PRO', None, (157.97499999999977, 195.206, 182.67399999999998)), ('D', '  32 ', 'GLU', None, (164.87099999999998, 96.97699999999998, 162.049)), ('D', ' 183 ', 'PRO', None, (129.62899999999988, 200.204, 162.682)), ('E', ' 190 ', 'ASN', None, (189.12099999999998, 177.72499999999994, 145.411))]
data['rota'] = [('A', '  24 ', 'THR', 0.26646706676793214, (157.65299999999988, 189.76499999999993, 248.794)), ('A', ' 114 ', 'ILE', 0.025915472608976208, (176.37399999999988, 190.883, 247.515)), ('A', ' 320 ', 'VAL', 0.06779013977550327, (181.07799999999978, 194.538, 206.48199999999997)), ('A', ' 338 ', 'VAL', 0.13319522382398277, (196.09399999999985, 189.859, 171.88199999999998)), ('A', ' 341 ', 'VAL', 0.004246703795481673, (190.89499999999978, 189.33999999999995, 180.386)), ('A', ' 372 ', 'LEU', 0.13260465810834793, (187.16599999999997, 175.476, 177.30699999999996)), ('A', ' 402 ', 'THR', 0.0037107245027243724, (172.6369999999999, 190.85399999999998, 175.237)), ('A', ' 403 ', 'ASN', 0.1090725887499413, (171.1429999999999, 194.213, 174.28599999999997)), ('A', ' 538 ', 'THR', 0.028306845342740417, (181.50599999999977, 179.03, 185.948)), ('A', ' 686 ', 'THR', 0.008087669993983582, (176.4939999999999, 166.01799999999997, 193.915)), ('A', ' 687 ', 'THR', 0.07030644306557092, (173.1319999999999, 167.609, 194.71699999999998)), ('A', ' 736 ', 'ASP', 0.14552321581728805, (190.49399999999986, 167.78599999999997, 219.488)), ('A', ' 761 ', 'ASP', 0.14470710581595264, (162.80099999999987, 163.523, 202.717)), ('A', ' 776 ', 'VAL', 0.029185516177676618, (165.92199999999988, 162.92999999999995, 221.716)), ('A', ' 784 ', 'SER', 0.088047253577203, (164.24199999999988, 175.732, 216.68799999999996)), ('A', ' 871 ', 'LYS', 0.1577577671876235, (144.3589999999999, 147.285, 197.705)), ('A', ' 910 ', 'ASP', 0.21382451424347385, (151.385, 140.428, 169.845)), ('B', '  79 ', 'LYS', 0.2846117799284141, (182.786, 168.167, 165.287)), ('B', ' 186 ', 'VAL', 0.005967108044060702, (165.7229999999998, 201.777, 179.58399999999997)), ('D', '   9 ', 'LEU', 0.035924804160638514, (156.89999999999998, 125.752, 152.067)), ('D', '  95 ', 'LEU', 0.042214847714446106, (132.642, 174.888, 175.233)), ('D', ' 131 ', 'VAL', 0.003127019590465352, (131.12299999999988, 196.699, 169.221)), ('D', ' 160 ', 'VAL', 0.11933121561678611, (130.49799999999988, 206.136, 169.824)), ('D', ' 161 ', 'ASP', 0.13112053555669329, (130.54599999999988, 205.31999999999996, 166.115)), ('D', ' 163 ', 'ASP', 0.1751336174480649, (133.9669999999999, 208.115, 163.496)), ('E', '   7 ', 'LEU', 0.22198227292281628, (141.036, 162.632, 142.36)), ('E', '  63 ', 'LEU', 0.27789285320154894, (158.02199999999996, 143.642, 139.869)), ('E', ' 126 ', 'CYS', 0.25360951056604636, (137.903, 169.79399999999995, 134.958)), ('E', ' 130 ', 'LEU', 0.18913938840375372, (142.16999999999996, 168.598, 138.702)), ('E', ' 193 ', 'VAL', 0.06054728777226593, (180.13099999999986, 180.169, 145.656)), ('E', ' 209 ', 'VAL', 0.14877265097679138, (175.9059999999999, 195.695, 128.858)), ('E', ' 255 ', 'THR', 0.24802802866818724, (128.0479999999999, 205.355, 154.378)), ('E', ' 258 ', 'ILE', 0.014206266609160864, (129.4009999999999, 208.56799999999996, 150.113)), ('E', ' 371 ', 'VAL', 0.003127019590465352, (139.4969999999999, 191.75399999999996, 148.545)), ('E', ' 397 ', 'VAL', 0.11187886733948531, (135.21199999999988, 190.613, 143.941)), ('E', ' 426 ', 'CYS', 0.2565088565562006, (136.70099999999988, 184.405, 133.234)), ('E', ' 438 ', 'LEU', 0.0024251429294908787, (128.9999999999999, 198.687, 132.759)), ('E', ' 448 ', 'ILE', 0.21864630880414704, (139.8529999999999, 205.91599999999997, 119.108)), ('E', ' 456 ', 'VAL', 0.017087615905546128, (137.5019999999999, 193.192, 118.627)), ('E', ' 526 ', 'LEU', 0.06955639655671753, (163.95699999999988, 209.495, 122.394)), ('E', ' 562 ', 'ASN', 0.07021330612772701, (142.97499999999988, 197.119, 121.477))]
data['cbeta'] = []
data['probe'] = [(' E   5  CYS  HB3', ' E   8  CYS  SG ', -0.814, (142.058, 159.43, 145.616)), (' E 458  ASP  H  ', ' E 460  LYS  HE3', -0.803, (131.118, 193.752, 119.49)), (' E   5  CYS  CB ', ' E   8  CYS  SG ', -0.765, (142.596, 158.435, 145.522)), (' A 116  ARG  NH2', ' A1004  ADP  O3B', -0.762, (173.32, 187.514, 240.355)), (' E 189  LYS  H  ', ' E 190  ASN  HB2', -0.755, (189.603, 179.345, 142.697)), (' D  25  ALA  O  ', ' D  29  GLY  N  ', -0.722, (156.419, 99.705, 160.721)), (' A 653  TYR  O  ', ' A 657  ASN  ND2', -0.713, (189.208, 173.767, 192.795)), (' A  50  LYS  NZ ', ' A  53  CYS  SG ', -0.713, (170.127, 185.533, 240.716)), (' D  50  ASP  OD2', " P  19    A  O2'", -0.685, (164.662, 125.777, 165.357)), (' A  15  SER  OG ', ' A 118  ARG  NH2', -0.684, (172.619, 204.866, 241.763)), (' E 178  ARG  HD3', ' E 340  VAL HG22', -0.681, (160.63, 194.538, 136.961)), (' E 379  ALA  O  ', ' E 423  ASN  ND2', -0.676, (143.363, 184.108, 134.612)), (' E 549  THR HG22', ' E 550  THR HG23', -0.672, (159.67, 194.23, 114.079)), (' A  83  GLU  HG3', ' A 219  PHE  HB2', -0.671, (182.673, 187.213, 242.067)), (' A 239  SER  OG ', ' A 465  ASP  OD1', -0.665, (179.93, 177.428, 219.196)), (" P  24    C  H2'", ' P  25    C  H6 ', -0.647, (174.565, 140.162, 181.931)), (" P  24    C  H2'", ' P  25    C  C6 ', -0.633, (174.2, 139.961, 181.12)), (' E 465  LYS  NZ ', ' E 569  LYS  O  ', -0.631, (140.691, 212.275, 126.053)), (" P  13    U  H2'", ' P  14    A  H8 ', -0.625, (184.071, 113.639, 174.274)), (' E 303  ARG  NH2', ' E 351  THR  O  ', -0.624, (146.888, 194.353, 156.591)), (' E 443  ARG  NH2', ' E 706  AF3  F1 ', -0.62, (141.959, 201.068, 131.245)), (" T  42    U  H2'", ' T  43    A  H8 ', -0.618, (185.495, 112.212, 163.699)), (" T  50    U  H2'", ' T  51    A  H8 ', -0.613, (182.23, 87.307, 158.599)), (' E 405  LEU HD11', ' E 534  ASP  HA ', -0.613, (150.263, 192.976, 127.508)), (' E 497  ARG HH12', ' E 500  LEU HD22', -0.612, (161.466, 212.412, 119.765)), (' E 189  LYS  N  ', ' E 190  ASN  HB2', -0.612, (189.644, 178.524, 142.598)), (' E 300  PRO  O  ', ' E 354  GLN  NE2', -0.609, (137.848, 201.3, 155.89)), (' A 100  ASP  HB3', ' A 115  SER  HB3', -0.607, (175.055, 195.524, 246.531)), (' E 198  TYR  HE2', ' E 219  LEU HD11', -0.606, (179.207, 191.685, 138.108)), (' A 589  ILE HG12', ' A 758  LEU HD13', -0.605, (168.524, 159.102, 197.73)), (' D 147  PHE  HB3', ' D 154  TRP  HB2', -0.605, (125.526, 196.603, 179.391)), (' A 615  MET  HB2', ' A 766  PHE  HE1', -0.601, (158.721, 161.017, 214.905)), (' A 583  ARG  NH2', ' A 590  GLY  O  ', -0.6, (169.631, 150.756, 194.845)), (' A 691  ASN  HB3', ' A 759  SER  O  ', -0.599, (168.461, 166.704, 200.303)), (' E 114  TRP  HB2', ' E 411  LEU HD11', -0.596, (152.841, 173.807, 127.861)), (' B 130  VAL  HB ', ' B 186  VAL HG13', -0.595, (166.503, 201.454, 182.52)), (" T  35    A  H2'", ' T  36    A  H8 ', -0.594, (172.522, 125.06, 178.964)), (' A 124  MET  HE2', ' A 212  LEU HD23', -0.593, (171.898, 191.351, 225.032)), (" T  52    C  H2'", ' T  53    G  C8 ', -0.59, (192.298, 84.974, 156.333)), (' A  58  GLU  OE1', ' A 118  ARG  NH1', -0.587, (168.901, 202.906, 239.843)), (' E 184  GLY  HA2', ' E 225  PHE  HA ', -0.585, (177.12, 184.595, 137.817)), (' A 116  ARG  HG2', ' A 217  TYR  HB2', -0.583, (176.459, 191.057, 239.07)), (" T  34    G  H2'", ' T  35    A  H8 ', -0.582, (176.057, 129.293, 178.973)), (' E 321  ALA  O  ', ' E 325  LEU  N  ', -0.582, (142.202, 207.949, 147.169)), (' A 221  ASP  HB2', ' A1005  1N7  H2 ', -0.581, (184.376, 178.317, 238.73)), (' E 280  LEU  HB2', ' E 436  MET  HE3', -0.58, (131.456, 193.731, 139.263)), (' E 486  SER  HB2', ' E 517  SER  HB3', -0.579, (163.773, 192.616, 121.732)), (' A  18  ARG  NH2', ' A  63  ASP  OD1', -0.578, (158.995, 208.644, 241.265)), (" T  42    U  H2'", ' T  43    A  C8 ', -0.577, (185.936, 112.461, 163.881)), (" P  25    C  H2'", ' P  26    U  H6 ', -0.577, (176.518, 144.318, 179.509)), (' E 280  LEU  HB3', ' E 399  ILE HG22', -0.576, (134.898, 194.349, 138.688)), (' C  56  LEU HD23', ' D 106  ILE HD11', -0.576, (132.66, 183.098, 176.221)), (' E  70  TYR  OH ', ' E 707  1N7  O2 ', -0.573, (157.387, 149.493, 150.942)), (' A  18  ARG HH12', ' A  61  GLU  HA ', -0.573, (161.634, 209.691, 239.77)), (' E 109  ILE HD13', ' E 134  ALA  HB2', -0.572, (144.868, 169.86, 134.712)), (' E 576  MET  HB2', ' E 582  TYR  HD2', -0.571, (149.358, 201.333, 110.091)), (" T  47    U  H2'", ' T  48    G  H8 ', -0.571, (181.045, 94.265, 171.349)), (' A 149  TYR  HE2', ' A 212  LEU HD13', -0.57, (167.5, 193.071, 226.415)), (' D 143  ASP  N  ', ' D 143  ASP  OD1', -0.566, (118.135, 196.788, 177.12)), (' A 720  VAL HG11', ' A 775  LEU HD13', -0.562, (167.943, 160.384, 227.998)), (' A 468  GLN  HA ', ' A 731  LEU HD22', -0.561, (179.545, 170.975, 219.383)), (" T  35    A  H2'", ' T  36    A  C8 ', -0.561, (172.591, 125.536, 178.778)), (' A 123  THR  HA ', ' A 211  ASP  HA ', -0.556, (172.248, 190.199, 230.833)), (' E 103  VAL  O  ', ' E 107  ASN  ND2', -0.556, (143.109, 158.54, 132.877)), (" P  13    U  H2'", ' P  14    A  C8 ', -0.554, (184.035, 113.642, 173.679)), (' A  30  VAL HG22', ' A  51  THR HG22', -0.553, (162.885, 180.852, 243.552)), (' A 107  ASP  OD1', ' A 108  GLY  N  ', -0.551, (167.339, 186.351, 261.997)), (' A 726  ARG  NH2', ' A 744  GLU  OE1', -0.549, (180.082, 157.688, 226.772)), (' A  35  PHE  CZ ', ' A  50  LYS  HB3', -0.548, (168.919, 180.877, 238.163)), (' E 315  ASP  OD1', ' E 332  ARG  NH2', -0.546, (153.64, 198.738, 142.643)), (' A 685  ALA  O  ', " T  21    U  O2'", -0.545, (174.906, 164.95, 190.229)), (' E 287  GLY  O  ', ' E 291  PHE  N  ', -0.545, (135.453, 201.963, 138.92)), (" T  36    A  H2'", ' T  37    U  H6 ', -0.545, (169.686, 121.537, 177.321)), (' E 292  ALA  HB1', ' E 306  TYR  HE1', -0.539, (139.133, 198.223, 143.945)), (' A  35  PHE  HZ ', ' A  50  LYS  HB3', -0.537, (169.505, 181.4, 238.05)), (' E 451  THR HG22', ' E 586  GLN  H  ', -0.535, (138.969, 204.405, 112.755)), (' E 185  TYR  N  ', ' E 224  TYR  O  ', -0.535, (179.067, 182.963, 138.696)), (' A   3  ASP  OD1', ' A   4  ALA  N  ', -0.535, (160.461, 195.086, 256.661)), (' E 295  LEU HD21', ' E 370  ILE HD13', -0.535, (134.171, 196.036, 148.404)), (' A 358  ASP  OD1', ' A 533  ARG  NH1', -0.534, (200.046, 174.525, 188.219)), (' E 404  GLN  HG2', ' E 537  GLN HE21', -0.53, (143.277, 195.319, 130.181)), (' E 518  GLN  NE2', ' E 547  THR  OG1', -0.529, (158.134, 200.886, 118.078)), (' E 187  VAL HG12', ' E 192  LYS  HG3', -0.526, (182.012, 176.996, 141.293)), (' E 493  ILE  O  ', ' E 497  ARG  HG2', -0.523, (163.226, 208.066, 116.066)), (' E 283  PRO  HG2', ' E 286  THR HG21', -0.523, (133.446, 199.543, 128.545)), (' E 140  ALA  HA ', ' E 232  VAL HG21', -0.521, (157.009, 174.301, 138.374)), (" T  52    C  H2'", ' T  53    G  H8 ', -0.52, (192.026, 84.542, 156.314)), (" T  32    G  H2'", ' T  33    A  H8 ', -0.519, (178.35, 136.362, 174.402)), (' C  58  VAL HG22', ' D 119  ILE HG12', -0.519, (140.879, 189.342, 177.609)), (' E 233  MET  N  ', ' E 233  MET  SD ', -0.519, (156.997, 176.739, 144.949)), (' A 636  LEU HD21', ' A 655  LEU HD22', -0.518, (186.919, 172.014, 202.465)), (' A 538  THR  HB ', ' A 661  GLN  HG2', -0.517, (182.199, 176.659, 187.365)), (' A 746  TYR  CZ ', ' A 750  ARG  HD2', -0.516, (175.313, 154.646, 212.567)), (' E 284  PRO  HD3', ' E 404  GLN HE22', -0.516, (139.694, 196.421, 127.828)), (' E 495  VAL  HA ', ' E 498  GLU  HG2', -0.516, (161.015, 209.741, 111.022)), (' E 519  ASN  OD1', ' E 530  THR  OG1', -0.515, (159.43, 201.764, 126.085)), (' A 409  THR  OG1', ' C  23  GLU  OE2', -0.513, (155.769, 181.768, 176.595)), (" T  41    G  H2'", ' T  42    U  C6 ', -0.512, (180.938, 114.282, 161.909)), (' A1005  1N7  H15', ' A1005  1N7  H6 ', -0.511, (188.683, 177.447, 237.068)), (' A 469  LEU  O  ', ' A 473  VAL HG23', -0.511, (180.1, 170.199, 212.299)), (' E 563  VAL  O  ', ' E 567  ARG  NH1', -0.51, (144.769, 199.251, 126.727)), (' B 120  ILE  O  ', ' B 124  THR  OG1', -0.508, (184.175, 197.768, 182.587)), (" P  26    U  H2'", ' P  27    A  H8 ', -0.508, (176.104, 148.083, 176.182)), (" T  36    A  H2'", ' T  37    U  C6 ', -0.507, (169.714, 122.079, 176.693)), (' E 449  VAL  HA ', ' E 452  VAL HG12', -0.507, (137.771, 202.466, 120.647)), (' A 378  PRO  HD2', ' A 537  PRO  HB2', -0.507, (184.12, 182.392, 185.879)), (" T  50    U  H2'", ' T  51    A  C8 ', -0.506, (182.755, 87.913, 158.442)), (' E 409  ARG  NH2', ' E 422  PHE  O  ', -0.504, (143.895, 180.944, 131.74)), (' E 136  GLU  HB2', ' E 235  LEU HD21', -0.504, (149.421, 173.4, 141.849)), (' A 316  LEU  HB2', ' A 463  MET  SD ', -0.504, (180.423, 184.969, 211.833)), (" P  25    C  H2'", ' P  26    U  C6 ', -0.503, (175.973, 144.146, 179.097)), (' A 795  SER  HG ', ' A 798  LYS  HZ3', -0.502, (154.864, 175.025, 207.631)), (' A 615  MET  HB2', ' A 766  PHE  CE1', -0.5, (159.192, 160.89, 215.385)), (' E 322  LEU HD12', ' E 327  ILE HG12', -0.5, (147.475, 210.28, 148.714)), (' E 394  LYS  O  ', ' E 395  HIS  ND1', -0.499, (131.902, 188.77, 151.976)), (' A 388  LEU HD23', ' A 397  SER  HB2', -0.499, (172.121, 192.484, 186.083)), (' E 489  ASN  HB2', ' E 549  THR HG23', -0.498, (160.318, 196.612, 114.853)), (' E 375  GLU  OE2', ' E 706  AF3  F3 ', -0.497, (141.676, 196.89, 133.854)), (' D  31  SER  HB3', ' D  32  GLU  HB2', -0.496, (164.753, 96.198, 164.19)), (' E 493  ILE HD11', ' E 518  GLN  HG3', -0.496, (162.263, 200.201, 118.519)), (' E 428  LEU  HA ', ' E 431  THR HG22', -0.496, (131.168, 181.447, 134.207)), (' E 325  LEU HD12', ' E 326  PRO  HD2', -0.495, (139.742, 206.712, 151.207)), (' A 836  ARG  NH1', ' A 840  ALA  HB2', -0.495, (151.956, 162.354, 186.438)), (' E 187  VAL  HA ', ' E 192  LYS  HA ', -0.494, (183.059, 178.012, 142.61)), (" T  41    G  H2'", ' T  42    U  H6 ', -0.494, (181.027, 114.17, 161.706)), (" P  23    U  H2'", ' P  24    C  H6 ', -0.493, (170.81, 136.399, 182.359)), (' E  21  ARG  NE ', ' E 136  GLU  OE2', -0.493, (153.199, 170.418, 142.377)), (" T  37    U  H2'", ' T  38    G  H8 ', -0.493, (168.22, 119.121, 173.208)), (' A 915  TYR  O  ', ' A 921  TYR  OH ', -0.492, (149.044, 146.988, 181.654)), (" T  34    G  H2'", ' T  35    A  C8 ', -0.491, (175.496, 129.216, 178.805)), (' A 587  VAL HG12', ' A 589  ILE HG13', -0.49, (170.939, 158.413, 199.582)), (' A 686  THR  O  ', ' A 686  THR  OG1', -0.49, (176.738, 166.682, 195.892)), (' B 137  THR  O  ', ' B 141  THR HG22', -0.485, (163.468, 204.083, 188.757)), (' A 516  TYR  CZ ', ' A 566  MET  HG2', -0.481, (181.978, 165.331, 181.158)), (' A  75  HIS  CG ', ' A  76  THR  H  ', -0.479, (177.158, 181.461, 249.775)), (' A  97  ALA  O  ', ' A  99  HIS  ND1', -0.479, (179.75, 194.156, 240.042)), (' E 281  GLN HE21', ' E 402  PRO  HD2', -0.477, (134.306, 190.654, 128.777)), (" P  23    U  H2'", ' P  24    C  C6 ', -0.475, (170.956, 136.476, 181.759)), (' T  37    U  C2 ', ' T  38    G  C8 ', -0.475, (169.118, 120.607, 172.348)), (' A 223  ILE HD13', ' A1005  1N7  H25', -0.474, (190.578, 177.642, 239.571)), (' A 416  ASN  HA ', ' A 850  THR HG23', -0.473, (144.984, 164.43, 174.829)), (' A 523  ASP  N  ', ' A 523  ASP  OD1', -0.472, (192.161, 165.065, 177.091)), (" P   8    C  H2'", ' P   9    A  H8 ', -0.472, (176.918, 98.371, 162.757)), (" T  32    G  H2'", ' T  33    A  C8 ', -0.471, (178.165, 136.544, 174.41)), (' A 390  ASP  OD2', ' A 674  TYR  OH ', -0.471, (167.725, 190.992, 185.413)), (' E 288  LYS  N  ', ' E 704  ADP  O2B', -0.471, (137.504, 200.541, 135.071)), (' A1005  1N7  H14', ' A1005  1N7  H29', -0.468, (189.293, 176.916, 231.923)), (' E 503  ASN  HB3', ' E 506  TRP  CD1', -0.468, (152.652, 216.169, 118.885)), (' A 759  SER  OG ', " P  35    A  O3'", -0.468, (165.526, 164.434, 198.148)), (' E  48  TYR  OH ', ' E  90  PHE  O  ', -0.467, (152.951, 149.902, 146.784)), (" P  18    C  H2'", ' P  19    A  H8 ', -0.467, (170.449, 126.119, 164.846)), (' E 243  GLN  HB2', ' E 277  TYR  CE1', -0.467, (130.508, 181.826, 143.942)), (' E 328  ASP  N  ', ' E 328  ASP  OD1', -0.466, (145.257, 208.577, 155.168)), (" T  47    U  H2'", ' T  48    G  C8 ', -0.465, (180.911, 94.481, 171.332)), (" T  45    C  H2'", ' T  46    A  H8 ', -0.464, (186.334, 102.18, 173.147)), (' A 388  LEU HD22', ' A 672  SER  HB3', -0.464, (171.5, 191.044, 183.484)), (" T  25    U  H2'", ' T  26    U  H6 ', -0.464, (160.983, 149.634, 184.471)), (" P  22    C  H2'", ' P  23    U  H6 ', -0.463, (167.506, 133.08, 180.504)), (' A  53  CYS  HB3', ' A  71  VAL HG13', -0.462, (169.615, 188.099, 242.387)), (' E 285  GLY  HA2', ' E 443  ARG  HE ', -0.46, (139.465, 203.437, 130.569)), (' E 511  PHE  HZ ', ' E 518  GLN HE21', -0.459, (158.87, 201.312, 118.967)), (' E 419  PRO  HA ', ' E 422  PHE  CZ ', -0.459, (140.766, 184.654, 126.403)), (' A 161  ASP  N  ', ' A 161  ASP  OD1', -0.459, (152.136, 186.23, 210.419)), (' E 472  PHE  HB2', ' E 573  LEU  HG ', -0.458, (150.007, 210.48, 114.723)), (' D 160  VAL HG12', ' D 166  ILE HD13', -0.457, (131.434, 208.223, 172.0)), (' E 285  GLY  O  ', ' E 442  ARG  N  ', -0.457, (135.337, 204.913, 129.501)), (" T  20    A  H2'", ' T  21    U  C6 ', -0.456, (170.664, 167.459, 186.306)), (' A  86  ILE HG23', ' A 201  ILE HD13', -0.455, (188.732, 188.218, 239.68)), (' E 285  GLY  N  ', ' E 704  ADP  O1B', -0.454, (138.646, 200.819, 130.928)), (' B 132  ILE HG21', ' B 138  TYR  HB2', -0.453, (160.626, 202.456, 186.093)), (' E 518  GLN  HA ', ' E 521  VAL HG12', -0.453, (164.152, 199.012, 120.978)), (' D 147  PHE  N  ', ' D 154  TRP  O  ', -0.453, (123.465, 197.855, 180.593)), (' A 858  ARG  HG2', " P  32    G  H5'", -0.453, (154.934, 158.513, 179.813)), (' E 247  VAL HG13', ' E 248  ARG  HG3', -0.452, (119.689, 189.024, 155.212)), (" P  26    U  H2'", ' P  27    A  C8 ', -0.451, (175.551, 147.909, 176.187)), (' D 161  ASP  N  ', ' D 161  ASP  OD1', -0.45, (129.599, 206.319, 167.236)), (' E 497  ARG  HA ', ' E 497  ARG  NH1', -0.45, (161.811, 210.987, 118.305)), (' A 444  GLN  HB3', ' A 448  ALA  HB2', -0.45, (156.172, 182.199, 184.687)), (' E 707  1N7  H41', ' E 707  1N7  H9 ', -0.449, (151.356, 142.492, 153.025)), (' E 419  PRO  HA ', ' E 422  PHE  CE2', -0.448, (140.759, 185.319, 126.863)), (' B 120  ILE  HB ', ' B 121  PRO  HD3', -0.447, (183.239, 193.662, 184.791)), (' A 132  ARG  NH2', ' A 465  ASP  OD2', -0.446, (175.849, 176.498, 219.183)), (' E 376  ILE HG21', ' E 398  TYR  HB3', -0.446, (138.799, 188.075, 138.87)), (' D 175  ASP  O  ', ' D 178  PRO  HD2', -0.446, (116.751, 205.207, 160.044)), (' A 371  LEU HD21', ' B  88  GLN  HG3', -0.445, (189.393, 177.911, 169.963)), (' C  49  PHE  HE1', ' D  98  LEU HD23', -0.445, (131.617, 176.074, 181.475)), (' T  42    U  C2 ', ' T  43    A  C8 ', -0.445, (184.861, 113.111, 164.812)), (' A 170  ASP  OD2', ' A 173  ARG  NH2', -0.445, (159.803, 196.043, 211.302)), (' A 647  SER  OG ', ' A 648  LEU  N  ', -0.443, (197.364, 167.609, 199.934)), (' D  68  THR  O  ', ' D  72  LYS  HG2', -0.441, (154.996, 152.908, 165.323)), (' E 401  ASP  HB3', ' E 404  GLN  OE1', -0.441, (139.254, 193.704, 128.893)), (' A 558  ALA  O  ', ' A 683  GLY  HA3', -0.441, (171.369, 172.56, 187.682)), (" P  15    C  H2'", ' P  16    G  H8 ', -0.441, (183.659, 121.036, 167.955)), (' A 699  ALA  O  ', ' A 703  ASN  ND2', -0.44, (169.103, 164.571, 215.343)), (' D  19  GLN  HA ', ' D  42  LEU HD12', -0.44, (158.516, 112.029, 159.788)), (' C  52  MET  HG3', ' D 103  LEU HD21', -0.44, (133.8, 180.549, 179.616)), (' E  61  THR  HA ', ' E  84  CYS  HB3', -0.439, (152.56, 145.177, 138.204)), (' E 377  SER  OG ', ' E 401  ASP  O  ', -0.439, (140.08, 189.818, 130.886)), (' A 723  LEU HD21', ' A 745  PHE  HD1', -0.438, (175.468, 161.3, 223.326)), (" P  32    G  H2'", ' P  33    C  C6 ', -0.438, (157.694, 158.397, 185.801)), (' B  46  LYS  HB2', ' B  46  LYS  HE3', -0.436, (178.659, 120.779, 154.593)), (' A 382  ALA  HB3', ' B 117  LEU HD11', -0.435, (183.219, 189.868, 184.064)), (' A  82  HIS  NE2', ' A 222  PHE  O  ', -0.435, (187.694, 182.937, 243.034)), (' E 260  ASP  N  ', ' E 260  ASP  OD1', -0.435, (129.834, 213.081, 145.002)), (' E 707  1N7  H14', ' E 707  1N7  H29', -0.434, (154.719, 141.815, 155.747)), (" T  43    A  H2'", ' T  44    G  H8 ', -0.434, (188.038, 110.228, 166.744)), (' E 580  ASP  O  ', ' E 584  LYS  HD3', -0.434, (142.072, 196.331, 108.597)), (' A 116  ARG  HD3', ' A 116  ARG  N  ', -0.434, (174.679, 192.347, 243.028)), (' A 758  LEU HD23', ' A 813  CYS  SG ', -0.433, (162.673, 159.043, 198.384)), (" P  22    C  H2'", ' P  23    U  C6 ', -0.432, (167.689, 132.93, 180.383)), (" T  31    G  H2'", ' T  32    G  H8 ', -0.431, (176.767, 140.059, 171.078)), (' A  35  PHE  HD2', ' A  48  PHE  HB2', -0.43, (169.355, 177.536, 235.607)), (' A 153  ASP  N  ', ' A 153  ASP  OD1', -0.43, (156.436, 197.912, 218.086)), (" P  24    C  O2'", ' P  25    C  OP1', -0.43, (174.956, 139.537, 184.666)), (' A 398  VAL HG21', ' A 666  MET  SD ', -0.429, (178.53, 188.122, 188.162)), (' P   8    C  C2 ', ' P   9    A  C8 ', -0.429, (178.302, 97.483, 163.485)), (' A 601  MET  O  ', ' A 605  VAL HG23', -0.428, (163.521, 151.713, 206.534)), (' A 303  ASP  N  ', ' A 303  ASP  OD1', -0.428, (192.735, 171.364, 209.301)), (' E 417  LEU HD11', ' E 421  TYR  HB2', -0.427, (141.013, 178.533, 127.213)), (' E 707  1N7  H10', ' E 707  1N7  H33', -0.427, (151.193, 141.868, 154.919)), (" P  27    A  H2'", ' P  28    A  H8 ', -0.426, (173.161, 151.456, 173.71)), (' A 605  VAL HG22', ' A 756  MET  HB2', -0.426, (164.486, 154.539, 207.33)), (" T  29    U  H2'", ' T  30    A  H8 ', -0.425, (168.733, 144.529, 169.191)), (" P  27    A  H2'", ' P  28    A  C8 ', -0.424, (173.426, 151.077, 173.407)), (' E 268  ASN  HB3', ' E 436  MET  SD ', -0.424, (128.722, 195.813, 141.05)), (' A 200  GLY  HA3', ' A 227  PRO  HA ', -0.424, (197.456, 188.444, 237.833)), (' T  40    C  C2 ', ' T  41    G  C8 ', -0.424, (176.254, 116.445, 163.512)), (" P  19    A  H2'", ' P  20    U  C6 ', -0.423, (166.77, 126.735, 168.029)), (' E 372  VAL  HA ', ' E 397  VAL HG13', -0.423, (137.21, 192.847, 144.661)), (' E  90  PHE  HZ ', ' E 707  1N7  H7 ', -0.423, (151.737, 145.523, 152.831)), (' E 287  GLY  HA2', " E 704  ADP H5'1", -0.422, (137.228, 204.118, 135.398)), (' A1006  1N7  H14', ' A1006  1N7  H29', -0.421, (195.833, 182.896, 228.574)), (' A 831  TYR  HB3', ' A 868  PRO  HB2', -0.421, (149.782, 151.607, 196.555)), (' C  75  MET  HG2', ' D  96  ARG HH21', -0.421, (130.564, 171.222, 168.406)), (' A 202  VAL  HB ', ' A 223  ILE HG13', -0.421, (192.113, 180.634, 238.278)), (' B 106  ILE HG13', ' B 107  ILE  N  ', -0.42, (191.355, 198.564, 184.968)), (" T  48    G  H2'", ' T  49    C  H6 ', -0.42, (179.229, 90.934, 167.725)), (' E 252  LEU HD13', ' E 299  TYR  CE2', -0.419, (130.388, 196.119, 150.865)), (' A 771  ALA  HB2', ' A 776  VAL HG12', -0.419, (162.395, 161.833, 220.801)), (' E 443  ARG  NH1', ' E 567  ARG HH21', -0.419, (143.142, 202.074, 130.197)), (' E 296  ALA  HB1', ' E 355  TYR  HE2', -0.419, (138.57, 201.445, 150.318)), (' A  46  ALA  HB3', ' A  48  PHE  CE1', -0.419, (169.646, 173.732, 231.99)), (' E 526  LEU HD13', ' E 528  LEU  HB2', -0.418, (160.446, 208.088, 124.196)), (' E 309  CYS  SG ', ' E 378  MET  HB3', -0.418, (147.272, 189.805, 135.412)), (' E 444  CYS  SG ', ' E 449  VAL  HB ', -0.417, (136.987, 204.995, 123.441)), (' A 837  ILE HG22', ' A 884  TYR  CE2', -0.417, (146.542, 156.904, 186.312)), (" T  49    C  H2'", ' T  50    U  H6 ', -0.417, (179.894, 88.848, 163.01)), (' A 761  ASP  HB3', ' A 812  PHE  CE1', -0.416, (162.03, 160.632, 202.205)), (' A  34  ALA  HA ', ' A  47  LYS  HA ', -0.416, (167.327, 178.399, 231.195)), (' A1006  1N7  H10', ' A1006  1N7  H33', -0.415, (193.864, 180.926, 226.792)), (' E 477  LYS  HA ', ' E 477  LYS  HD2', -0.413, (156.087, 198.677, 105.34)), (' E 514  PRO  HA ', ' E 533  VAL HG12', -0.412, (153.279, 195.152, 123.647)), (' A 702  ALA  HA ', ' A 785  VAL HG21', -0.412, (168.383, 170.829, 216.334)), (' A 210  GLN HE21', ' A 214  GLY  HA2', -0.412, (177.776, 192.912, 228.15)), (" P  18    C  H2'", ' P  19    A  C8 ', -0.412, (170.388, 125.75, 165.363)), (' D 160  VAL HG22', ' D 185  ILE  HB ', -0.411, (132.516, 203.617, 170.242)), (" P  21    U  H2'", ' P  22    C  H6 ', -0.411, (165.126, 130.411, 176.931)), (' E 512  ILE  O  ', ' E 546  PHE  HA ', -0.411, (153.788, 201.855, 120.875)), (' A 106  ILE HG23', ' A 107  ASP  H  ', -0.41, (167.744, 187.006, 259.368)), (" P  21    U  H2'", ' P  22    C  C6 ', -0.41, (165.641, 130.486, 176.934)), (' A 417  LYS  HD2', ' D  90  MET  HG3', -0.41, (138.569, 168.049, 172.874)), (' D 133  PRO  HA ', ' D 183  PRO  HB3', -0.41, (128.525, 197.008, 163.773)), (" P   3    C  H2'", ' P   4    G  C8 ', -0.408, (194.419, 89.261, 165.337)), (' A 902  MET  SD ', ' D  71  TYR  HD1', -0.408, (149.814, 153.056, 160.466)), (' A 514  LEU HD13', ' B  79  LYS  HE3', -0.407, (180.261, 167.161, 168.445)), (" T  25    U  H2'", ' T  26    U  C6 ', -0.407, (161.106, 149.684, 184.482)), (' E 497  ARG HH22', ' E 500  LEU HD22', -0.406, (161.901, 213.205, 120.553)), (' E 452  VAL  HA ', ' E 455  LEU  HG ', -0.406, (138.826, 198.731, 116.915)), (' E 404  GLN  HG2', ' E 537  GLN  NE2', -0.406, (143.147, 195.078, 130.611)), (' E 363  LEU  O  ', ' E 390  ARG  HD3', -0.406, (150.671, 185.6, 150.416)), (' A 497  ASN  OD1', ' A 500  LYS  NZ ', -0.405, (168.496, 162.804, 178.831)), (' E 542  ASP  O  ', ' E 570  VAL HG12', -0.405, (146.732, 213.007, 125.4)), (" P  32    G  H2'", ' P  33    C  H6 ', -0.405, (157.729, 158.941, 185.973)), (" T  51    A  H2'", ' T  52    C  C6 ', -0.405, (187.098, 86.337, 156.19)), (' E 445  PRO  O  ', ' E 449  VAL HG12', -0.405, (136.901, 207.342, 121.731)), (' E 443  ARG  CZ ', ' E 567  ARG HH21', -0.404, (142.615, 201.808, 129.889)), (' T  49    C  C2 ', ' T  50    U  C5 ', -0.404, (180.911, 90.748, 163.714)), (' E 447  GLU  HB2', ' E 467  LYS  HB3', -0.404, (138.056, 211.159, 117.175)), (' E 325  LEU HD21', ' E 355  TYR  CG ', -0.404, (142.337, 202.342, 151.692)), (' E 277  TYR  HA ', ' E 396  TYR  O  ', -0.404, (133.088, 188.57, 146.035)), (' E 235  LEU HD12', ' E 385  SER  HB3', -0.403, (146.661, 177.589, 143.369)), (' B  44  VAL HG12', " T  42    U  H4'", -0.403, (184.965, 114.321, 158.408)), (' A 368  PHE  CE2', ' A 519  MET  HG2', -0.402, (187.033, 169.338, 174.331)), (' E 489  ASN  ND2', ' E 549  THR  O  ', -0.401, (158.943, 196.863, 111.861)), (' A 756  MET  O  ', ' A 762  ALA  HA ', -0.401, (164.451, 160.156, 205.838)), (' E 480  ILE HG12', ' E 550  THR HG22', -0.401, (159.845, 193.627, 111.631)), (' E 384  LEU HD11', ' E 425  VAL HG12', -0.401, (140.091, 183.411, 137.942)), (' P  26    U  C2 ', ' P  27    A  C8 ', -0.401, (174.821, 146.969, 175.945)), (' A 694  PHE  HZ ', ' A 790  ASN HD21', -0.401, (168.314, 173.646, 206.144)), (' B 145  THR  O  ', ' B 156  ILE HG12', -0.4, (168.492, 209.987, 179.562)), (' E 451  THR  CG2', ' E 586  GLN  H  ', -0.4, (139.382, 204.697, 113.492))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
