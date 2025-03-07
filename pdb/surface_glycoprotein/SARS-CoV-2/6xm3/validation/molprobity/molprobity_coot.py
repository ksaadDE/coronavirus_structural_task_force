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
data['rama'] = [('A', ' 521 ', 'PRO', 0.04504929323582687, (155.393, 173.772, 161.217)), ('B', ' 210 ', 'ILE', 0.06014458791052373, (129.25099999999995, 186.06, 180.864)), ('B', ' 213 ', 'VAL', 0.093907050767646, (125.844, 192.265, 181.711)), ('B', ' 487 ', 'ASN', 0.02924021760716675, (199.266, 209.384, 100.203)), ('C', ' 198 ', 'ASP', 0.031236684644056566, (203.08, 210.042, 159.617))]
data['omega'] = []
data['rota'] = [('A', ' 402 ', 'ILE', 0.012286112932136078, (172.72099999999995, 193.055, 136.941)), ('A', ' 563 ', 'GLN', 0.18495882401222552, (152.719, 172.41900000000007, 169.576)), ('A', '1141 ', 'LEU', 0.08436592384801468, (186.208, 179.128, 271.544)), ('B', ' 210 ', 'ILE', 0.0, (129.25099999999995, 186.06, 180.864)), ('B', ' 493 ', 'GLN', 0.195245779178087, (193.064, 219.04000000000005, 111.626)), ('B', ' 493 ', 'GLN', 0.07730303148425866, (193.04, 219.027, 111.614)), ('B', ' 617 ', 'CYS', 0.12688591295421872, (163.263, 217.425, 192.447)), ('B', ' 878 ', 'LEU', 0.01944572766190098, (171.23799999999994, 169.254, 227.895)), ('B', ' 988 ', 'GLU', 0.005563856730100539, (182.339, 177.704, 160.384)), ('B', ' 991 ', 'VAL', 0.132508511681649, (183.953, 180.03000000000006, 165.441)), ('C', '  33 ', 'THR', 0.08002036200166447, (217.624, 219.58200000000002, 181.133)), ('C', ' 244 ', 'LEU', 0.17971746847171619, (227.877, 235.832, 155.07)), ('C', ' 336 ', 'CYS', 0.19403624758516644, (214.922, 170.666, 144.107)), ('C', ' 362 ', 'VAL', 0.007351242675213143, (217.352, 173.07600000000005, 149.322)), ('C', ' 440 ', 'ASN', 0.2363322831220011, (197.044, 177.325, 124.101)), ('C', ' 581 ', 'THR', 0.2378761701980786, (226.964, 166.603, 164.017)), ('C', ' 630 ', 'THR', 0.24539831834063847, (222.94699999999995, 205.589, 180.719)), ('C', ' 738 ', 'CYS', 0.07405267521129116, (176.515, 198.99300000000005, 184.085))]
data['cbeta'] = [('B', ' 616 ', 'ASN', ' ', 0.39775420288042124, (167.778, 219.65400000000005, 192.587)), ('B', ' 620 ', 'VAL', ' ', 0.2540692759833432, (161.303, 214.46200000000005, 189.51)), ('C', ' 361 ', 'CYS', ' ', 0.2906043748867278, (215.24299999999994, 169.70500000000007, 148.038))]
data['probe'] = [(' B1100  THR  HG1', ' B1101  HIS  HD1', -0.773, (169.055, 205.23, 262.42)), (' A 350  VAL HG11', ' A 402  ILE HG23', -0.727, (170.339, 194.467, 138.333)), (' C 318  PHE  HZ ', ' C 615  VAL HG21', -0.653, (219.917, 187.967, 188.403)), (' A 350  VAL HG12', ' A 400  PHE  HB2', -0.634, (167.774, 192.611, 138.488)), (' B 323  THR  OG1', ' B 537  LYS  NZ ', -0.625, (167.892, 221.447, 174.173)), (' B 391  CYS  HA ', ' B 525  CYS  HB3', -0.622, (187.785, 216.244, 150.872)), (' B 374  PHE  HA ', ' B 436  TRP  HB3', -0.616, (176.502, 224.647, 130.357)), (' A 106  PHE  HB2', ' A 117  LEU  HB3', -0.615, (196.037, 146.792, 150.943)), (' B 448  ASN  HB2', ' B 497  PHE  HB2', -0.594, (184.284, 227.819, 114.431)), (' B 188  ASN  HA ', ' B 209  PRO  HA ', -0.589, (129.697, 183.382, 177.306)), (' A  99  ASN  O  ', ' A 102  ARG  NH2', -0.589, (209.12, 133.143, 155.458)), (' A  88  ASP  N  ', ' A  88  ASP  OD1', -0.587, (188.145, 149.998, 162.448)), (' B 689  SER  OG ', ' B 690  GLN  N  ', -0.582, (144.601, 204.48, 206.725)), (' B  83  VAL HG11', ' B 237  ARG HH11', -0.582, (138.373, 203.166, 156.282)), (' A 328  ARG  NH2', ' A 531  THR  O  ', -0.579, (160.139, 156.138, 160.753)), (' A 516  GLU  OE2', ' A 519  HIS  NE2', -0.576, (161.604, 182.342, 161.75)), (' C  88  ASP  N  ', ' C  88  ASP  OD1', -0.572, (215.767, 209.989, 164.318)), (' B 675  GLN  O  ', ' B 690  GLN  NE2', -0.567, (147.983, 203.098, 209.609)), (' C 366  SER  O  ', ' C 370  ASN  ND2', -0.565, (210.237, 185.16, 144.017)), (' C 440  ASN  N  ', ' C 440  ASN  OD1', -0.565, (197.317, 177.783, 125.731)), (' A 100  ILE HG22', ' A 242  LEU HD22', -0.563, (203.242, 130.821, 156.813)), (' B 353  TRP  O  ', ' B 466  ARG  NH1', -0.562, (197.042, 219.969, 128.173)), (' B 448  ASN  ND2', ' B 497  PHE  O  ', -0.56, (183.47, 230.572, 113.439)), (' C  65  PHE  O  ', ' C 264  ALA  N  ', -0.56, (228.353, 227.2, 165.641)), (' B  96  GLU  O  ', ' B 186  PHE  N  ', -0.552, (124.82, 188.111, 172.947)), (' A 134  GLN  O  ', ' A 160  TYR  OH ', -0.548, (195.623, 138.075, 141.017)), (' B 438  SER  HB3', ' B 442  ASP  HB2', -0.544, (182.792, 228.968, 122.416)), (' A  34  ARG  NH2', ' A 191  GLU  OE1', -0.544, (204.145, 142.52, 171.931)), (' B1141  LEU HD12', ' B1142  GLN  HG3', -0.541, (185.365, 189.915, 273.239)), (' A 393  THR HG21', ' A 519  HIS  HB2', -0.541, (158.816, 178.728, 160.974)), (' A 792  PRO  O  ', ' A 795  LYS  NZ ', -0.539, (219.89, 177.309, 233.097)), (' A 162  SER  OG ', ' A 163  ALA  N  ', -0.537, (198.636, 142.112, 137.431)), (' C 516  GLU  OE2', ' C 519  HIS  ND1', -0.536, (203.807, 168.523, 162.948)), (' B 379  CYS  HB3', ' B 432  CYS  HA ', -0.535, (181.436, 212.718, 137.495)), (' A 796  ASP  N  ', ' A 796  ASP  OD1', -0.533, (216.973, 175.512, 239.73)), (' B 316  SER  OG ', ' B 317  ASN  N  ', -0.532, (165.791, 203.077, 185.661)), (' B 293  LEU  O  ', ' B 632  THR  OG1', -0.53, (150.768, 202.889, 185.565)), (' C 605  SER  OG ', ' C 606  ASN  N  ', -0.528, (220.548, 211.076, 198.863)), (' B 466  ARG  HE ', ' B 468  ILE HD11', -0.526, (200.098, 217.655, 125.969)), (' B 605  SER  OG ', ' B 606  ASN  N  ', -0.526, (149.124, 198.886, 199.559)), (' C 127  VAL HG12', ' C 171  VAL HG22', -0.524, (207.011, 232.862, 151.95)), (' C 328  ARG  NH2', ' C 580  GLN  OE1', -0.524, (226.804, 171.982, 161.561)), (' B 478  THR  HB ', ' B 487  ASN HD21', -0.524, (203.272, 206.149, 98.501)), (' B 462  LYS  HD2', ' B 465  GLU  HG3', -0.523, (199.967, 208.349, 126.955)), (' A 334  ASN  N  ', ' A 334  ASN  OD1', -0.521, (154.681, 167.342, 147.507)), (' B 626  ALA  O  ', ' B 634  ARG  NH2', -0.518, (153.106, 211.602, 181.396)), (' B 287  ASP  N  ', ' B 287  ASP  OD1', -0.517, (148.913, 184.073, 185.982)), (' A 102  ARG  HD2', ' A 141  LEU HD11', -0.517, (207.167, 133.854, 150.947)), (' B 401  VAL HG22', ' B 509  ARG HH12', -0.516, (187.068, 224.6, 124.716)), (' B 280  ASN  ND2', ' B 281  GLU  O  ', -0.516, (148.495, 173.89, 184.576)), (' C 501  ASN  O  ', ' C 506  GLN  NE2', -0.515, (187.793, 180.866, 126.102)), (' A1091  ARG  NH1', ' A1118  ASP  O  ', -0.515, (184.141, 181.466, 257.927)), (' B 301  CYS  O  ', ' B 304  LYS  NZ ', -0.514, (161.853, 190.554, 185.731)), (' B 310  LYS  HG3', ' B 600  PRO  HA ', -0.512, (156.507, 197.396, 203.264)), (' A 448  ASN  OD1', ' A 450  ASN  ND2', -0.51, (165.736, 195.225, 125.831)), (' A 642  VAL HG22', ' A 651  ILE HG12', -0.51, (174.48, 146.764, 193.596)), (' B 707  TYR  HB3', ' C 792  PRO  HG2', -0.51, (175.651, 213.318, 237.599)), (' B 248  TYR  HB3', ' B 250  THR HG23', -0.509, (120.145, 200.898, 150.498)), (' B  40  ASP  N  ', ' B  40  ASP  OD1', -0.509, (154.584, 181.701, 172.147)), (' C 494  SER  OG ', ' C 495  TYR  N  ', -0.508, (185.827, 166.743, 127.77)), (' B 825  LYS  NZ ', ' B 938  LEU  O  ', -0.507, (157.116, 181.47, 215.104)), (' B 472  ILE HD11', ' B 484  GLU  HB3', -0.501, (202.723, 214.668, 105.741)), (' C 574  ASP  N  ', ' C 574  ASP  OD1', -0.501, (213.25, 170.587, 176.227)), (' C 827  THR  OG1', ' C 828  LEU  N  ', -0.501, (192.752, 214.471, 202.567)), (' B 421  TYR  O  ', ' B 457  ARG  NH1', -0.5, (195.672, 208.908, 120.698)), (' B 142  GLY  H  ', ' B 159  VAL HG11', -0.5, (122.694, 190.798, 152.769)), (' A 777  ASN  OD1', ' A1019  ARG  NH1', -0.499, (198.571, 189.107, 209.647)), (' A 172  SER  OG ', ' A 173  GLN  N  ', -0.497, (214.222, 148.902, 152.61)), (' C 832  GLY  HA3', ' C 956  ALA  HB1', -0.497, (191.08, 207.894, 194.908)), (' B 491  PRO  HB2', ' B 492  LEU HD12', -0.496, (196.568, 213.542, 114.286)), (' B 642  VAL HG22', ' B 651  ILE HG12', -0.491, (157.302, 214.733, 194.749)), (' C 214  ARG  NH1', ' C 266  TYR  OH ', -0.491, (228.141, 226.157, 173.211)), (' C 206  LYS  HE2', ' C 221  SER  HB2', -0.49, (210.828, 228.304, 178.482)), (' A 376  THR  HB ', ' A 435  ALA  HB3', -0.49, (177.018, 184.683, 141.508)), (' C1084  ASP  N  ', ' C1084  ASP  OD1', -0.488, (202.031, 174.996, 265.837)), (' B  81  ASN HD21', ' B 242  LEU  HB2', -0.487, (127.169, 195.916, 160.94)), (' B 102  ARG  HD2', ' B 121  ASN  HB3', -0.486, (128.775, 184.867, 158.826)), (' B 160  TYR  OH ', ' B 248  TYR  O  ', -0.483, (122.829, 196.826, 149.962)), (' B 758  SER  O  ', ' B 758  SER  OG ', -0.482, (193.157, 173.048, 184.424)), (' C 393  THR HG21', ' C 520  ALA  HB3', -0.482, (208.835, 165.712, 160.013)), (' B 128  ILE  HB ', ' B 170  TYR  HB3', -0.481, (140.281, 182.23, 153.601)), (' B 294  ASP  N  ', ' B 294  ASP  OD1', -0.48, (152.008, 199.633, 187.214)), (' B 328  ARG  NH1', ' B 531  THR  O  ', -0.48, (178.043, 228.222, 165.888)), (' A 408  ARG  NH1', ' A 414  GLN  OE1', -0.479, (180.052, 195.677, 148.925)), (' C 112  SER  OG ', ' C 133  PHE  O  ', -0.479, (217.667, 220.901, 142.532)), (' B 189  LEU  HG ', ' B 210  ILE HG12', -0.474, (131.134, 187.577, 177.711)), (' C  31  SER  HB3', ' C  34  ARG  HB3', -0.474, (219.39, 219.586, 176.885)), (' B 162  SER  OG ', ' B 163  ALA  N  ', -0.473, (134.315, 190.96, 142.274)), (' A 326  ILE HD11', ' A 534  VAL HG22', -0.47, (165.6, 154.619, 166.238)), (' B 493 BGLN  OE1', ' B 494  SER  N  ', -0.466, (191.694, 221.0, 110.967)), (' B 422  ASN HD21', ' B 454  ARG  HD2', -0.466, (193.161, 211.599, 118.283)), (' C 747  THR  O  ', ' C 751  ASN  ND2', -0.465, (170.717, 199.42, 170.694)), (' A 743  CYS  HB3', ' A 749  CYS  HB3', -0.462, (205.124, 189.064, 173.96)), (' A 105  ILE HD11', ' A 241  LEU HD21', -0.462, (198.027, 137.548, 149.694)), (' A 131  CYS  HA ', ' A 166  CYS  HA ', -0.459, (198.946, 149.737, 140.145)), (' C 417  LYS  NZ ', ' C 455  LEU  O  ', -0.458, (178.383, 164.543, 138.656)), (' A 498  GLN  O  ', ' A 501  ASN  ND2', -0.457, (178.95, 194.184, 125.376)), (' B 986  PRO  O  ', ' B 990  GLU  HG2', -0.457, (184.659, 174.006, 162.539)), (' B 357  ARG  NH1', ' C 167  THR  O  ', -0.455, (201.675, 222.72, 143.824)), (' B 452  LEU  HA ', ' B 494  SER  HA ', -0.455, (191.817, 221.627, 114.801)), (' B1103  PHE  HZ ', ' O   1  NAG  H62', -0.455, (168.615, 199.67, 260.675)), (' B 128  ILE HD13', ' B 170  TYR  HD2', -0.453, (139.763, 180.59, 155.792)), (' C 422  ASN HD21', ' C 454  ARG  H  ', -0.452, (185.306, 163.527, 137.863)), (' A 391  CYS  HB3', ' A 522  ALA  HB1', -0.452, (160.151, 171.308, 158.029)), (' B 462  LYS  HB2', ' B 465  GLU  HB2', -0.451, (198.064, 207.947, 127.529)), (' B 101  ILE HG22', ' B 242  LEU HD12', -0.45, (127.391, 193.116, 163.52)), (' C1116  THR  OG1', ' C1118  ASP  OD1', -0.449, (195.405, 187.96, 261.787)), (' C1114  ILE  O  ', ' C1119  ASN  ND2', -0.447, (199.314, 189.465, 259.758)), (' C1118  ASP  N  ', ' C1118  ASP  OD1', -0.447, (193.915, 186.305, 261.973)), (' B 716  THR  OG1', ' B1071  GLN  O  ', -0.447, (164.531, 197.051, 244.436)), (' B  83  VAL HG22', ' B 239  GLN  HB2', -0.445, (135.436, 200.662, 157.368)), (' A 319  ARG  NH1', ' A 592  PHE  O  ', -0.444, (178.067, 158.093, 184.319)), (' C 406  GLU  HB3', ' C 418  ILE HG13', -0.442, (186.444, 172.238, 139.446)), (' C 964  LYS  HB3', ' C 964  LYS  HE2', -0.442, (193.933, 204.556, 183.06)), (' A 787  GLN  NE2', ' C 703  ASN HD22', -0.441, (215.726, 193.5, 230.555)), (' C 328  ARG HH21', ' C 580  GLN  HB2', -0.441, (226.005, 171.024, 161.673)), (' C 318  PHE  CD2', ' C 623  ALA  HB1', -0.44, (221.04, 190.593, 185.187)), (' B 452  LEU HD21', ' B 492  LEU  HB3', -0.439, (195.804, 218.352, 115.025)), (' B 659  SER  HB3', ' B 698  SER  HB3', -0.439, (162.91, 209.889, 216.625)), (' B 314  GLN  NE2', ' B 316  SER  O  ', -0.437, (167.838, 202.386, 189.442)), (' C 833  PHE  HD2', ' C 959  LEU HD13', -0.436, (184.635, 207.2, 192.808)), (' B 627  ASP  N  ', ' B 627  ASP  OD1', -0.434, (156.04, 212.942, 179.787)), (' C 443  SER  HB2', ' C 497  PHE  HB3', -0.434, (190.804, 173.489, 125.758)), (' C 294  ASP  N  ', ' C 294  ASP  OD1', -0.433, (218.017, 207.969, 186.704)), (' B 401  VAL HG22', ' B 509  ARG HH22', -0.432, (187.314, 225.769, 123.943)), (' B 332  ILE HD13', ' B 527  PRO  HB3', -0.431, (182.814, 226.182, 154.404)), (' C 828  LEU HD23', ' C 835  LYS  HB2', -0.43, (188.928, 213.026, 197.7)), (' B 607  GLN  H  ', ' B 607  GLN  HG2', -0.429, (149.625, 200.859, 199.781)), (' C1048  HIS  HA ', ' C1066  THR HG22', -0.428, (193.994, 198.001, 231.873)), (' C 808  ASP  N  ', ' C 808  ASP  OD1', -0.428, (182.193, 220.174, 223.59)), (' B  97  LYS  HB2', ' B 100  ILE HD11', -0.428, (122.349, 189.387, 168.635)), (' C 102  ARG  HA ', ' C 102  ARG  HD3', -0.427, (218.416, 233.504, 159.882)), (' B 345  THR  OG1', ' B 346  ARG  N  ', -0.424, (191.627, 232.879, 127.878)), (' C 501  ASN  HB3', ' C 505  TYR  HB2', -0.423, (185.243, 178.045, 127.402)), (' B 129  LYS  HE3', ' B 133  PHE  HZ ', -0.422, (135.672, 187.197, 148.245)), (' B 438  SER  HB2', ' B 507  PRO  HB2', -0.421, (182.434, 226.318, 121.621)), (' A 112  SER  O  ', ' A 112  SER  OG ', -0.42, (190.683, 144.747, 137.818)), (' C 776  LYS  HB3', ' C 776  LYS  HE2', -0.42, (176.125, 194.436, 208.474)), (' A 413  GLY  HA3', ' C 987  PRO  HG2', -0.42, (176.622, 194.75, 155.95)), (' B 377  PHE  HE2', ' B 384  PRO  HG3', -0.419, (176.855, 215.944, 140.425)), (' B 119  ILE HG23', ' B 128  ILE HG13', -0.418, (138.203, 184.873, 156.258)), (' C 743  CYS  HB3', ' C 749  CYS  HB3', -0.418, (176.897, 201.489, 174.087)), (' C 363  ALA  O  ', ' C 527  PRO  HD3', -0.418, (214.787, 177.144, 149.482)), (' B 498  GLN  HB2', ' B 501  ASN HD21', -0.418, (178.347, 228.21, 110.331)), (' B 131  CYS  HA ', ' B 166  CYS  HB3', -0.417, (140.941, 189.417, 144.988)), (' A 294  ASP  N  ', ' A 294  ASP  OD1', -0.416, (189.004, 149.784, 184.964)), (' C 630  THR HG23', ' C 633  TRP  HB2', -0.415, (221.875, 204.015, 183.324)), (' C 172  SER  O  ', ' C 172  SER  OG ', -0.415, (204.124, 234.639, 159.316)), (' A  83  VAL HG11', ' A 237  ARG HH21', -0.415, (187.792, 139.098, 150.941)), (' C 703  ASN  OD1', ' C 704  SER  N  ', -0.414, (217.741, 189.79, 232.115)), (' A 394  ASN  N  ', ' A 394  ASN  OD1', -0.413, (159.532, 180.086, 155.987)), (' C 804  GLN  OE1', ' C 935  GLN  NE2', -0.413, (192.499, 218.19, 225.898)), (' B 443  SER  HB2', ' B 497  PHE  HB3', -0.412, (181.964, 229.017, 115.879)), (' B 402  ILE HG13', ' B 508  TYR  HB2', -0.412, (182.465, 219.989, 123.23)), (' A 326  ILE  HA ', ' A 326  ILE HD13', -0.41, (166.388, 156.989, 163.194)), (' B 900  MET  HB3', ' B 900  MET  HE2', -0.408, (174.819, 172.22, 245.643)), (' A 945  LEU HD23', ' A 948  LEU HD12', -0.408, (203.524, 171.797, 211.971)), (' A 808  ASP  HA ', ' A 809  PRO  HD3', -0.408, (221.124, 173.464, 225.513)), (' B 404  GLY  HA3', ' B 504  GLY  HA2', -0.407, (176.427, 219.29, 118.508)), (' B 713  ALA  HB3', ' C 894  LEU  HB3', -0.406, (171.915, 202.666, 241.748)), (' B 429  PHE  HE1', ' B 464  PHE  HZ ', -0.406, (189.871, 209.97, 135.122)), (' A 384  PRO  HA ', ' A 387  LEU HD12', -0.405, (173.241, 174.4, 151.131)), (' A 713  ALA  HB3', ' B 894  LEU  HB3', -0.404, (180.461, 164.179, 240.78)), (' B 404  GLY  HA2', ' B 508  TYR  CE1', -0.402, (177.725, 220.317, 121.61)), (' C 130  VAL HG13', ' C 233  ILE HD11', -0.402, (208.886, 219.229, 150.256)), (' C 134  GLN  O  ', ' C 160  TYR  OH ', -0.401, (220.956, 225.506, 145.142)), (' A 568  ASP  N  ', ' A 568  ASP  OD2', -0.4, (163.022, 173.648, 178.973)), (' B 198  ASP  N  ', ' B 198  ASP  OD1', -0.4, (155.409, 189.193, 160.16))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
