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
data['omega'] = []
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' B  46  SER  HA ', ' B 279  TYR  O  ', -0.69, (231.99, 183.047, 211.572)), (' C  46  SER  HA ', ' C 279  TYR  O  ', -0.68, (198.356, 234.226, 215.754)), (' F  43  CYS  HB3', ' F  99  LEU  HB3', -0.67, (202.034, 170.589, 284.267)), (' D  43  CYS  HB3', ' D  99  LEU  HB3', -0.648, (244.226, 164.994, 302.339)), (' A 105  ILE  HB ', ' A 239  GLN  HB2', -0.633, (174.687, 159.483, 246.707)), (' B 901  GLN HE21', ' B 905  ARG HH21', -0.63, (207.513, 186.024, 167.146)), (' B 201  PHE  HB3', ' B 229  LEU  HB2', -0.628, (237.752, 186.512, 240.485)), (' E  43  CYS  HB3', ' E  99  LEU  HB3', -0.627, (170.906, 210.519, 283.823)), (' C  51  THR  O  ', ' C 274  THR  HA ', -0.607, (186.137, 225.291, 224.141)), (' A 365  TYR  H  ', ' A 388  ASN HD21', -0.601, (224.152, 167.857, 251.19)), (' A  94  SER  HB2', ' A 190  ARG  HB2', -0.594, (165.95, 161.335, 233.602)), (' B  64  TRP  HE1', ' B 264  ALA  HB1', -0.591, (257.913, 195.736, 227.672)), (' C 365  TYR  H  ', ' C 388  ASN HD21', -0.571, (171.467, 200.854, 250.195)), (' E  59  ARG  HB3', ' E  69  ILE HD11', -0.571, (159.603, 214.609, 280.544)), (' B 357  ARG  NH1', ' B 396  TYR  OH ', -0.558, (196.539, 232.868, 246.952)), (' F  80  TYR  HB2', ' F  85  LYS  HG2', -0.557, (193.483, 159.0, 277.327)), (' F  59  ARG  HB3', ' F  69  ILE HD11', -0.551, (204.078, 159.07, 281.092)), (' D  59  ARG  HB3', ' D  69  ILE HD11', -0.549, (249.911, 176.008, 306.565)), (' C 143  VAL  HA ', ' C 154  GLU  HA ', -0.542, (178.807, 260.6, 247.932)), (' B 289  VAL HG13', ' B 297  SER  HB3', -0.539, (234.028, 198.725, 213.576)), (' B 127  VAL HG21', ' B1302  NAG  H62', -0.539, (250.893, 178.571, 247.943)), (' B 821  LEU HD11', ' B 939  SER  HB2', -0.539, (227.4, 183.938, 183.573)), (' E  23  VAL HG11', ' E 118  ARG HH21', -0.536, (173.881, 201.018, 275.675)), (' B 193  VAL HG23', ' B 223  LEU HD22', -0.534, (242.579, 189.437, 228.159)), (' F  60  GLN  NE2', ' F  64  LYS  O  ', -0.53, (213.39, 155.217, 277.273)), (' C  22  THR  O  ', ' C  78  ARG  NH1', -0.529, (160.925, 250.501, 237.37)), (' B  26  PRO  HB3', ' B  65  PHE  HE1', -0.529, (254.866, 203.741, 233.201)), (' C 821  LEU HD11', ' C 939  SER  HB3', -0.527, (199.853, 232.201, 183.063)), (' D  80  TYR  HB2', ' D  85  LYS  HG2', -0.526, (254.278, 177.133, 295.451)), (' E  60  GLN  NE2', ' E  64  LYS  O  ', -0.525, (152.554, 208.475, 276.603)), (' C 278  LYS  HE3', ' C 287  ASP  HB2', -0.523, (190.661, 235.664, 214.881)), (' A 128  ILE HD13', ' A 170  TYR  HD2', -0.521, (166.916, 172.404, 246.601)), (' B 487  ASN  ND2', ' E 129  LEU  O  ', -0.521, (162.625, 209.672, 265.426)), (' B 762  GLN  OE1', ' B 765  ARG  NH1', -0.52, (189.208, 189.046, 210.141)), (' C 128  ILE HD13', ' C 170  TYR  HD2', -0.52, (190.743, 241.938, 246.86)), (' C1143  PRO  HA ', ' C1146  ASP  HB2', -0.519, (193.482, 206.2, 125.715)), (' C  34  ARG  NH2', ' C 221  SER  OG ', -0.518, (185.293, 243.922, 224.515)), (' A  22  THR  O  ', ' A  78  ARG  NH1', -0.517, (174.697, 142.604, 238.048)), (' B 276  LEU  HB3', ' B 289  VAL  HB ', -0.517, (232.402, 195.077, 214.518)), (' A1048  HIS  HA ', ' A1066  THR HG22', -0.517, (189.666, 190.932, 170.555)), (' C 357  ARG  NH1', ' C 396  TYR  OH ', -0.51, (171.703, 182.011, 246.665)), (' A 294  ASP  N  ', ' A 294  ASP  OD1', -0.509, (185.203, 167.028, 214.919)), (' A 289  VAL HG13', ' A 297  SER  HB3', -0.509, (182.37, 171.349, 214.964)), (' A 566  GLY  N  ', ' A 575  ALA  O  ', -0.509, (225.042, 175.698, 222.182)), (' C 103  GLY  HA3', ' C 119  ILE  O  ', -0.507, (181.572, 245.784, 245.161)), (' A1144  GLU  HG3', ' C1141  LEU HD21', -0.505, (196.967, 197.891, 130.397)), (' E  80  TYR  HB2', ' E  85  LYS  HG2', -0.503, (165.44, 223.742, 277.029)), (' C 226  LEU  HG ', ' C 227  VAL HG23', -0.502, (191.752, 241.15, 240.118)), (' B 191  GLU  O  ', ' B 205  SER  HA ', -0.498, (245.094, 185.714, 229.384)), (' B 156  GLU  OE2', ' B 246  ARG  NH2', -0.498, (266.38, 190.408, 248.26)), (' F  23  VAL HG11', ' F 118  ARG HH21', -0.497, (209.069, 178.446, 276.771)), (' C 294  ASP  N  ', ' C 294  ASP  OD1', -0.497, (177.001, 228.59, 214.536)), (' C 488  CYS  O  ', ' F  71  ARG  NH1', -0.496, (198.396, 166.193, 269.495)), (' B  46  SER  CA ', ' B 279  TYR  O  ', -0.496, (231.261, 182.325, 211.878)), (' C 142  GLY  HA3', ' C 156  GLU  HB3', -0.494, (175.318, 257.744, 249.836)), (' C  93  ALA  HB3', ' C 266  TYR  HB2', -0.493, (176.096, 243.63, 230.177)), (' A 334  ASN  ND2', ' A 360  ASN  O  ', -0.492, (236.537, 172.271, 245.861)), (' C  27  ALA  HB3', ' C  64  TRP  HB3', -0.492, (167.708, 245.802, 229.213)), (' B  93  ALA  HB3', ' B 266  TYR  HB2', -0.491, (250.393, 195.038, 227.654)), (' A1086  LYS  HD2', ' A1122  VAL HG11', -0.491, (213.708, 193.858, 139.622)), (' C  64  TRP  HE1', ' C 264  ALA  HB1', -0.49, (171.769, 249.291, 230.36)), (' D  60  GLN  NE2', ' D  64  LYS  O  ', -0.488, (246.411, 182.532, 313.141)), (' B 105  ILE  O  ', ' B 238  PHE  HA ', -0.487, (247.18, 195.221, 242.781)), (' B  27  ALA  HB3', ' B  64  TRP  HB3', -0.486, (256.374, 202.007, 227.671)), (' C  46  SER  CA ', ' C 279  TYR  O  ', -0.486, (198.442, 233.493, 216.133)), (' A 488  CYS  O  ', ' D  71  ARG  NH1', -0.485, (243.042, 179.395, 293.923)), (' B 125  ASN HD22', ' B 171  VAL HG13', -0.485, (248.947, 175.724, 244.671)), (' A 376  THR  HB ', ' A 435  ALA  HB3', -0.484, (224.162, 167.179, 269.793)), (' B1048  HIS  HA ', ' B1066  THR HG22', -0.484, (212.97, 195.749, 171.129)), (' D  23  VAL HG11', ' D 118  ARG HH21', -0.484, (232.052, 168.204, 301.637)), (' C1307  NAG  H82', ' E 125  PRO  HB2', -0.483, (168.808, 197.881, 265.24)), (' B  52  GLN  OE1', ' B 274  THR  OG1', -0.483, (227.706, 199.094, 222.888)), (' B 365  TYR  H  ', ' B 388  ASN HD21', -0.481, (212.623, 223.016, 250.752)), (' B 518  LEU HD21', ' B 546  LEU  HB2', -0.481, (208.866, 225.401, 234.517)), (' C 489  TYR  OH ', ' F 124  ARG  NH2', -0.481, (203.85, 169.441, 267.573)), (' B  36  VAL HG23', ' B 222  ALA  HA ', -0.478, (240.546, 188.128, 221.509)), (' A 489  TYR  OH ', ' D 124  ARG  NH2', -0.478, (236.621, 179.451, 296.25)), (' C1086  LYS  HD2', ' C1122  VAL HG11', -0.477, (188.14, 192.172, 139.655)), (' C 289  VAL HG13', ' C 297  SER  HB3', -0.476, (182.128, 229.016, 214.948)), (' C  78  ARG  NH2', ' C  80  ASP  OD1', -0.476, (164.899, 248.552, 237.04)), (' C1048  HIS  HA ', ' C1066  THR HG22', -0.474, (196.818, 213.744, 170.736)), (' B 720  ILE HG13', ' B 923  ILE HG23', -0.474, (219.622, 191.359, 164.077)), (' C  36  VAL HG13', ' C 222  ALA  HA ', -0.473, (187.756, 238.701, 225.071)), (' A 659  SER  HB3', ' A 698  SER  HB3', -0.471, (198.259, 166.971, 184.948)), (' C 144  TYR  N  ', ' C 153  MET  O  ', -0.47, (178.063, 262.872, 248.116)), (' B 376  THR  HB ', ' B 435  ALA  HB3', -0.469, (200.272, 212.21, 259.163)), (' A 821  LEU HD11', ' A 939  SER  HB3', -0.469, (171.832, 184.385, 182.882)), (' C 926  GLN  NE2', ' T   1  NAG  O6 ', -0.468, (191.842, 225.608, 162.644)), (' C  16  VAL  HB ', ' C 140  PHE  HZ ', -0.468, (168.94, 253.784, 252.213)), (' A 675  GLN  O  ', ' A 691  SER  N  ', -0.467, (185.405, 160.677, 195.44)), (' A 561  PRO  HA ', ' A 577  ARG HH22', -0.467, (235.698, 172.35, 224.858)), (' B 195  LYS  O  ', ' B 201  PHE  HA ', -0.467, (236.456, 189.635, 238.575)), (' C 376  THR  HB ', ' C 435  ALA  HB3', -0.467, (186.785, 195.57, 258.918)), (' A  27  ALA  HB3', ' A  64  TRP  HB3', -0.466, (175.414, 150.626, 229.465)), (' C 916  LEU HD22', ' C 923  ILE HD13', -0.464, (200.094, 220.087, 159.167)), (' A 164  ASN  OD1', ' A 165  ASN  N  ', -0.464, (176.205, 166.833, 262.104)), (' B  78  ARG  NH2', ' B  80  ASP  OD1', -0.463, (260.287, 202.299, 235.53)), (' E 114  TYR  O  ', ' E 138  GLY  HA2', -0.462, (162.065, 206.899, 283.459)), (' A 192  PHE  HA ', ' A 204  TYR  O  ', -0.462, (170.204, 168.945, 234.583)), (' B  94  SER  HB3', ' B 190  ARG  HB2', -0.459, (252.271, 187.534, 229.975)), (' E  61  ALA  HB3', ' E  64  LYS  HB2', -0.459, (151.019, 212.235, 277.74)), (' A 189  LEU  HB3', ' A 208  THR  HB ', -0.459, (163.861, 163.543, 227.142)), (' C  40  ASP  N  ', ' C  40  ASP  OD1', -0.458, (194.304, 230.276, 229.145)), (' C 659  SER  HB3', ' C 698  SER  HB3', -0.458, (171.639, 218.041, 184.444)), (' C  31  SER  HB3', ' C  60  SER  H  ', -0.458, (175.189, 236.946, 223.464)), (' B 189  LEU  HB3', ' B 208  THR  HB ', -0.455, (251.536, 185.82, 222.953)), (' A  78  ARG  NH2', ' A  80  ASP  OD1', -0.453, (174.129, 146.89, 237.588)), (' A 139  PRO  HB3', ' A 159  VAL  HA ', -0.453, (170.377, 155.789, 251.909)), (' A 756  TYR  OH ', ' A 994  ASP  OD1', -0.451, (194.199, 205.546, 227.876)), (' C 329  PHE  HE2', ' C 528  LYS  HB2', -0.45, (166.419, 202.538, 242.788)), (' F  41  LEU HD12', ' F 101  LEU HD23', -0.45, (202.679, 162.693, 286.225)), (' A 393  THR HG21', ' A 520  ALA  HB3', -0.45, (228.687, 185.316, 250.365)), (' B 294  ASP  N  ', ' B 294  ASP  OD1', -0.449, (236.114, 203.934, 214.439)), (' A 310  LYS  HG3', ' A 600  PRO  HA ', -0.449, (185.797, 171.917, 198.386)), (' B 599  THR  HB ', ' B 608  VAL HG12', -0.447, (233.679, 205.106, 204.466)), (' B 756  TYR  OH ', ' B 994  ASP  OD1', -0.447, (196.351, 193.888, 227.975)), (' C 189  LEU  HB3', ' C 208  THR  HB ', -0.447, (184.513, 248.731, 226.974)), (' A 175  PHE  O  ', ' A 207  HIS  NE2', -0.446, (161.476, 167.704, 235.95)), (' A 565  PHE  HD1', ' A 576  VAL HG23', -0.445, (224.399, 174.083, 226.615)), (' B 995  ARG  NH2', ' C 994  ASP  OD2', -0.444, (205.444, 200.711, 230.005)), (' B 354  ASN  O  ', ' B 398  ASP  HA ', -0.442, (194.14, 225.587, 256.794)), (' A 565  PHE  O  ', ' B  43  PHE  N  ', -0.441, (228.527, 178.205, 222.398)), (' B1086  LYS  HD2', ' B1122  VAL HG11', -0.441, (199.479, 214.985, 139.392)), (' B 192  PHE  HA ', ' B 204  TYR  O  ', -0.44, (243.679, 187.14, 231.058)), (' C 398  ASP  OD2', ' C 423  TYR  OH ', -0.44, (182.138, 184.944, 252.608)), (' B 926  GLN  OE1', ' N   1  NAG  O6 ', -0.439, (226.312, 194.8, 163.328)), (' A1029  MET  HB2', ' A1029  MET  HE2', -0.438, (185.785, 201.499, 181.264)), (' B 722  VAL HG22', ' B1065  VAL HG22', -0.438, (217.915, 189.943, 171.857)), (' B 907  ASN  ND2', ' B 911  VAL  O  ', -0.437, (209.579, 195.245, 156.779)), (' A 722  VAL HG22', ' A1065  VAL HG22', -0.437, (181.947, 190.386, 171.367)), (' C 487  ASN  OD1', ' F 124  ARG  NH1', -0.435, (205.891, 168.315, 264.994)), (' B 132  GLU  OE1', ' B 165  ASN  ND2', -0.434, (240.776, 190.432, 259.785)), (' A 895  GLN  NE2', ' C1074  ASN  OD1', -0.434, (176.111, 212.264, 158.496)), (' A  46  SER  HA ', ' A 279  TYR  O  ', -0.434, (170.299, 182.641, 216.032)), (' A  40  ASP  N  ', ' A  40  ASP  OD1', -0.434, (174.833, 181.48, 229.312)), (' A 128  ILE HG21', ' A 229  LEU HD13', -0.434, (170.921, 171.944, 246.902)), (' D  41  LEU HD12', ' D 101  LEU HD23', -0.434, (251.146, 168.952, 306.306)), (' A 278  LYS  HB2', ' A 278  LYS  HE3', -0.433, (174.618, 177.7, 214.838)), (' A 395  VAL  HA ', ' A 514  SER  O  ', -0.432, (229.488, 178.251, 257.439)), (' C  63  THR  O  ', ' C 266  TYR  HA ', -0.431, (171.946, 242.976, 231.818)), (' A 934  ILE  HA ', ' A 934  ILE HD13', -0.43, (179.259, 184.646, 177.903)), (' B  22  THR  O  ', ' B  78  ARG  NH1', -0.428, (263.742, 204.366, 236.686)), (' D  61  ALA  HB3', ' D  64  LYS  HB2', -0.426, (250.176, 183.068, 312.64)), (' B 278  LYS  HB2', ' B 278  LYS  HE3', -0.426, (233.611, 189.275, 211.242)), (' A 724  THR HG23', ' A 934  ILE HD12', -0.426, (181.072, 187.012, 178.742)), (' F  61  ALA  HB3', ' F  64  LYS  HB2', -0.425, (210.406, 152.442, 278.476)), (' B 329  PHE  HE2', ' B 528  LYS  HB2', -0.424, (216.616, 226.694, 243.392)), (' C 971  GLY  HA3', ' C 995  ARG HH21', -0.424, (196.245, 208.283, 230.487)), (' B 130  VAL  HB ', ' B 168  PHE  HB3', -0.423, (239.441, 185.227, 249.554)), (' C 722  VAL HG22', ' C1065  VAL HG22', -0.423, (199.763, 221.012, 171.522)), (' B 934  ILE  HA ', ' B 934  ILE HD13', -0.421, (223.769, 190.542, 178.629)), (' C 310  LYS  HG3', ' C 600  PRO  HA ', -0.42, (181.249, 226.194, 198.203)), (' C  94  SER  HB3', ' C 190  ARG  HB2', -0.42, (181.202, 248.091, 234.006)), (' A 125  ASN HD22', ' A 171  VAL HG13', -0.419, (160.17, 170.37, 250.369)), (' A 316  SER  OG ', ' A 317  ASN  N  ', -0.417, (196.342, 173.594, 215.516)), (' C 195  LYS  O  ', ' C 201  PHE  HA ', -0.417, (185.358, 232.014, 241.15)), (' B  38  TYR  HB2', ' B 225  PRO  HD3', -0.416, (236.306, 183.637, 226.642)), (' C 231  ILE HD12', ' C 233  ILE HG12', -0.416, (183.365, 232.016, 248.74)), (' B 900  MET  HB3', ' B 900  MET  HE2', -0.415, (207.653, 184.443, 156.811)), (' A 566  GLY  HA3', ' A 575  ALA  HB3', -0.415, (225.755, 175.703, 220.121)), (' C 724  THR HG23', ' C 934  ILE HD12', -0.412, (197.098, 223.28, 178.778)), (' A 722  VAL  HA ', ' A1064  HIS  O  ', -0.411, (184.143, 188.784, 173.053)), (' B  97  LYS  HG2', ' B 186  PHE  HD1', -0.411, (261.895, 188.233, 227.211)), (' A 907  ASN HD21', ' A 913  GLN  HG3', -0.41, (189.83, 197.546, 154.914)), (' A 971  GLY  HA3', ' A 995  ARG HH21', -0.41, (193.015, 194.05, 230.616)), (' B 866  THR  H  ', ' B 869  MET  HE3', -0.409, (205.458, 174.042, 190.94)), (' B1141  LEU HD23', ' B1145  LEU HD22', -0.409, (202.859, 204.433, 128.488)), (' B 885  GLY  HA2', ' B 901  GLN  NE2', -0.408, (207.425, 184.371, 166.449)), (' E  41  LEU HD12', ' E 101  LEU HD23', -0.406, (163.707, 213.909, 285.868)), (' A 487  ASN  OD1', ' D 124  ARG  NH1', -0.406, (235.441, 182.506, 297.307)), (' C1028  LYS  NZ ', ' C1042  PHE  O  ', -0.406, (197.681, 209.617, 179.469)), (' B  48  LEU  HB3', ' B 276  LEU HD11', -0.405, (228.563, 191.251, 213.531)), (' C 245  HIS  O  ', ' C 259  THR  N  ', -0.405, (169.741, 261.441, 244.46)), (' A 156  GLU  OE2', ' A 158  ARG  NH1', -0.405, (163.532, 148.781, 254.128)), (' A  93  ALA  HB3', ' A 266  TYR  HB2', -0.405, (172.219, 159.34, 230.471)), (' C 229  LEU  HG ', ' C 231  ILE HG23', -0.405, (187.823, 234.733, 247.418)), (' C1086  LYS  HB2', ' C1086  LYS  HE2', -0.405, (185.976, 194.526, 137.986)), (' A 599  THR  HB ', ' A 608  VAL HG12', -0.405, (186.847, 169.366, 204.941)), (' B 195  LYS  HE2', ' B 204  TYR  HE1', -0.404, (235.85, 189.617, 232.152)), (' A 193  VAL  HB ', ' A 204  TYR  HB2', -0.404, (173.337, 170.879, 233.378)), (' C  68  ILE HG22', ' C  78  ARG  HB2', -0.403, (166.12, 254.446, 234.96)), (' A  31  SER  HB3', ' A  60  SER  H  ', -0.403, (179.213, 161.426, 223.685)), (' A 903  ALA  HB2', ' A 916  LEU HD12', -0.402, (183.472, 195.253, 156.784)), (' C  64  TRP  HH2', ' C 214  ARG  HG2', -0.402, (169.913, 250.988, 225.228)), (' C 934  ILE  HA ', ' C 934  ILE HD13', -0.401, (195.838, 225.642, 177.821)), (' F  82  PRO  HA ', ' F  85  LYS  HG3', -0.401, (193.507, 156.695, 276.216)), (' F  60  GLN  HB2', ' F  66  LEU HD23', -0.401, (211.134, 159.79, 278.26)), (' B 127  VAL HG22', ' B 171  VAL HG22', -0.4, (248.445, 177.299, 245.992))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
