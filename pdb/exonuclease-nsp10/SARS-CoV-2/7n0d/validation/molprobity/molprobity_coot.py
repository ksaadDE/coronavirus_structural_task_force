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
data['probe'] = [(' D 127  THR HG23', ' D 128  PRO  HD2', -0.78, (175.262, 208.331, 209.829)), (' D 127  THR  CG2', ' D 128  PRO  HD2', -0.777, (174.462, 208.288, 209.62)), (' H 127  THR HG23', ' H 128  PRO  HD2', -0.769, (170.578, 137.784, 209.987)), (' H 127  THR  CG2', ' H 128  PRO  HD2', -0.763, (171.582, 137.841, 209.612)), (' G  39  THR HG22', ' G  40  ASN  N  ', -0.69, (192.881, 146.679, 204.141)), (' C  39  THR HG22', ' C  40  ASN  N  ', -0.683, (152.812, 198.97, 203.664)), (' P  67    C  H42', ' T   4    G  H1 ', -0.627, (165.61, 180.918, 188.264)), (' H 313  GLN  NE2', ' H 340  CYS  SG ', -0.621, (179.025, 138.436, 137.333)), (' D 313  GLN  NE2', ' D 340  CYS  SG ', -0.615, (166.981, 207.737, 137.335)), (' D  17  GLY  H  ', ' D  30  ASP  HB3', -0.594, (166.789, 193.829, 214.062)), (' H  17  GLY  H  ', ' H  30  ASP  HB3', -0.591, (179.227, 152.317, 214.09)), (' F  30  ASP  OD2', ' F  32  LYS  NZ ', -0.591, (201.097, 145.538, 188.974)), (' D 518  ASN HD22', ' D 521  ASN HD21', -0.579, (180.055, 210.281, 119.329)), (' H 397  ILE HG12', ' H 510  VAL HG23', -0.578, (169.039, 140.951, 132.712)), (' B 313  GLN  NE2', ' B 340  CYS  SG ', -0.574, (139.398, 132.77, 142.163)), (' H 518  ASN HD22', ' H 521  ASN HD21', -0.573, (166.294, 135.533, 119.013)), (' D 397  ILE HG12', ' D 510  VAL HG23', -0.571, (176.572, 204.923, 132.708)), (' B  30  ASP  OD2', ' B  32  LYS  NZ ', -0.567, (144.882, 200.561, 188.821)), (' F 313  GLN  NE2', ' F 340  CYS  SG ', -0.567, (206.927, 212.595, 142.319)), (' C  39  THR HG22', ' C  40  ASN  H  ', -0.556, (152.607, 199.379, 204.416)), (' C  94  GLY  O  ', ' D  47  LYS  NZ ', -0.556, (165.895, 210.289, 217.91)), (' G  39  THR HG22', ' G  40  ASN  H  ', -0.554, (193.433, 146.586, 204.343)), (' G  94  GLY  O  ', ' H  47  LYS  NZ ', -0.554, (180.134, 135.563, 217.937)), (' B 352  ASP  O  ', ' B 366  LEU  N  ', -0.553, (135.398, 128.87, 157.6)), (' G  75  LEU HD22', ' G 112  LEU HD11', -0.553, (189.509, 132.788, 199.245)), (' C  75  LEU HD22', ' C 112  LEU HD11', -0.553, (156.536, 213.212, 199.278)), (' F  98  ARG  NH1', ' H 249  PHE  O  ', -0.545, (181.316, 159.839, 175.934)), (' E  25  LYS  NZ ', ' E  29  ASP  OD2', -0.545, (218.766, 161.987, 156.775)), (' A  25  LYS  NZ ', ' A  29  ASP  OD2', -0.543, (127.381, 183.947, 156.803)), (' B  98  ARG  NH1', ' D 249  PHE  O  ', -0.541, (164.717, 186.085, 175.981)), (' A  42  VAL HG23', ' A  69  GLY  H  ', -0.538, (133.167, 199.41, 178.503)), (' A  75  LEU HD22', ' A 112  LEU HD11', -0.535, (131.326, 191.056, 164.732)), (' F 352  ASP  O  ', ' F 366  LEU  N  ', -0.534, (210.487, 217.085, 157.703)), (' D 218  SER  OG ', ' D 221  SER  O  ', -0.533, (171.35, 224.129, 186.728)), (' E  42  VAL HG23', ' E  69  GLY  H  ', -0.53, (213.199, 146.286, 178.346)), (' D 234  ASP  N  ', ' D 234  ASP  OD1', -0.528, (174.529, 218.349, 185.631)), (' F  88  GLY  H  ', ' F 112  SER  HB3', -0.527, (197.473, 184.319, 160.327)), (' E  75  LEU HD22', ' E 112  LEU HD11', -0.525, (214.092, 154.966, 164.944)), (' H 234  ASP  N  ', ' H 234  ASP  OD1', -0.522, (171.445, 127.538, 185.654)), (' B 163  ARG  NH1', ' B 197  TYR  O  ', -0.517, (149.116, 181.503, 161.041)), (' C  54  ALA  O  ', ' C  98  GLN  NE2', -0.517, (154.353, 213.823, 216.791)), (' B  88  GLY  H  ', ' B 112  SER  HB3', -0.514, (148.955, 161.51, 160.285)), (' H 218  SER  OG ', ' H 221  SER  O  ', -0.514, (174.694, 122.002, 186.78)), (' G  54  ALA  O  ', ' G  98  GLN  NE2', -0.514, (191.396, 132.648, 217.141)), (' F 468  LEU  HB3', ' F 483  VAL HG11', -0.511, (193.269, 209.309, 119.078)), (' B 468  LEU  HB3', ' B 483  VAL HG11', -0.506, (152.816, 137.324, 119.076)), (' D  15  ILE HG23', ' D  16  THR HG23', -0.504, (172.343, 191.48, 215.485)), (' D 266  ASN  H  ', ' F 266  ASN  H  ', -0.504, (184.968, 190.283, 170.657)), (' F 163  ARG  NH1', ' F 197  TYR  O  ', -0.503, (197.227, 164.773, 161.459)), (' F 449  ASP  O  ', ' F 476  ARG  NH2', -0.502, (204.582, 219.791, 121.746)), (' B 449  ASP  O  ', ' B 476  ARG  NH2', -0.498, (142.043, 126.139, 121.468)), (' H  15  ILE HG23', ' H  16  THR HG23', -0.498, (174.177, 154.672, 215.901)), (' H 208  CYS  O  ', ' H 209  LEU  HB2', -0.497, (177.181, 117.534, 177.221)), (' C  39  THR  CG2', ' C  40  ASN  N  ', -0.497, (152.471, 199.366, 203.682)), (' E  42  VAL HG12', ' F  26  HIS  HA ', -0.495, (211.516, 151.132, 182.129)), (' H 302  GLU  HG2', ' H 409  LEU HD21', -0.491, (176.917, 131.425, 154.934)), (' F 234  ASP  N  ', ' F 234  ASP  OD1', -0.49, (197.853, 164.951, 152.706)), (' D 208  CYS  O  ', ' D 209  LEU  HB2', -0.489, (168.728, 227.944, 177.395)), (' H 257  HIS  CE1', ' H 264  HIS  HB2', -0.484, (167.326, 153.408, 166.613)), (' C  48  HIS  HB3', ' C  63  MET  HA ', -0.483, (144.546, 207.832, 221.614)), (' I   4    G  H1 ', ' J  67    C  H42', -0.482, (179.884, 165.281, 188.604)), (' D 127  THR  CG2', ' D 128  PRO  CD ', -0.48, (174.053, 208.168, 210.126)), (' D 257  HIS  CE1', ' D 264  HIS  HB2', -0.479, (178.928, 193.006, 166.683)), (' H 442  LEU HD22', ' H 508  LEU HD23', -0.479, (167.984, 135.297, 137.568)), (' B 266  ASN  H  ', ' H 266  ASN  H  ', -0.478, (160.539, 155.561, 170.482)), (' G  39  THR  CG2', ' G  40  ASN  N  ', -0.478, (193.627, 146.624, 203.738)), (' B 488  ALA  HB1', ' B 492  ARG HH12', -0.478, (150.652, 140.959, 119.337)), (' G  48  HIS  HB3', ' G  63  MET  HA ', -0.476, (201.914, 137.955, 221.546)), (' H 127  THR  CG2', ' H 128  PRO  CD ', -0.475, (171.992, 137.764, 210.233)), (' D  35  THR  N  ', ' D  38  LEU  O  ', -0.475, (155.861, 194.917, 217.322)), (' D 442  LEU HD22', ' D 508  LEU HD23', -0.475, (177.679, 210.363, 137.873)), (' D 302  GLU  HG2', ' D 409  LEU HD21', -0.474, (169.119, 214.567, 154.986)), (' D  13  LYS  NZ ', ' D  98  ARG  O  ', -0.473, (182.5, 192.679, 204.644)), (' F 488  ALA  HB1', ' F 492  ARG HH12', -0.47, (195.394, 205.513, 119.129)), (' D 378  THR  O  ', ' D 395  ASN  ND2', -0.468, (174.85, 194.997, 127.275)), (' D 329  LEU HD11', ' D 348  TRP  CE2', -0.468, (164.304, 203.697, 131.864)), (' D 332  ILE  HA ', ' D 351  TYR  HB2', -0.467, (164.754, 196.544, 136.745)), (' C  98  GLN  O  ', ' C 123  TRP  NE1', -0.466, (151.157, 215.02, 213.442)), (' G  98  GLN  O  ', ' G 123  TRP  NE1', -0.462, (194.884, 131.154, 213.096)), (' A  42  VAL HG12', ' B  26  HIS  HA ', -0.461, (134.296, 195.278, 181.933)), (' F 321  LEU HD22', ' F 346  VAL HG11', -0.459, (204.772, 224.471, 139.37)), (' B 115  VAL HG21', ' B 169  MET  HG3', -0.459, (155.169, 167.269, 154.997)), (' H  10  ASP  OD2', ' H  53  ARG  NH1', -0.459, (175.449, 148.95, 208.282)), (' D 516  THR HG23', ' F 471  ALA  HB3', -0.458, (185.822, 214.436, 125.645)), (' H 241  MET  HB3', ' H 241  MET  HE2', -0.458, (179.65, 141.26, 178.522)), (' D 127  THR HG22', ' D 128  PRO  HD2', -0.457, (174.139, 208.999, 210.235)), (' H 332  ILE  HA ', ' H 351  TYR  HB2', -0.457, (181.014, 149.332, 137.105)), (' H 329  LEU HD11', ' H 348  TRP  CE2', -0.457, (181.229, 142.089, 131.627)), (" L  64    A  H2'", ' L  65    A  C8 ', -0.455, (200.336, 175.291, 198.395)), (' B 321  LEU HD22', ' B 346  VAL HG11', -0.455, (140.822, 121.316, 139.382)), (' F 252  ASN  O  ', ' F 256  ASN  ND2', -0.454, (198.889, 190.307, 176.662)), (' D 127  THR HG22', ' D 128  PRO  CD ', -0.454, (173.943, 208.625, 210.497)), (' H 378  THR  O  ', ' H 395  ASN  ND2', -0.452, (171.185, 151.076, 127.415)), (' F 241  MET  HB3', ' F 241  MET  HE2', -0.451, (205.187, 177.268, 162.785)), (' A  40  ASN HD21', ' B  27  LEU  HG ', -0.448, (134.581, 189.299, 182.632)), (' G  39  THR  CG2', ' G  40  ASN  H  ', -0.446, (193.704, 146.915, 204.031)), (' C  39  THR  CG2', ' C  40  ASN  H  ', -0.445, (152.258, 199.29, 203.988)), (' H 127  THR HG22', ' H 128  PRO  CD ', -0.444, (172.102, 137.328, 210.586)), (' D  53  ARG  HB2', ' D 126  ASP  HB2', -0.444, (172.308, 201.813, 206.476)), (' B 169  MET  HB3', ' B 169  MET  HE3', -0.443, (153.158, 170.46, 155.319)), (" K  64    A  H2'", ' K  65    A  C8 ', -0.443, (145.389, 170.712, 198.534)), (' D 328  VAL HG23', ' D 347  GLU  HG3', -0.441, (164.004, 199.16, 125.468)), (" T   6    U H5''", " T   7    G  H5'", -0.441, (154.975, 179.231, 186.086)), (' H 328  VAL HG23', ' H 347  GLU  HG3', -0.441, (181.945, 146.846, 125.441)), (' F 318  LYS  O  ', ' F 322  LEU  HG ', -0.44, (202.821, 221.223, 133.848)), (' B 318  LYS  O  ', ' B 322  LEU  HG ', -0.439, (143.088, 124.511, 133.536)), (' E  40  ASN HD21', ' F  27  LEU  HG ', -0.438, (211.628, 156.578, 182.75)), (" L  63    A  H2'", ' L  64    A  C8 ', -0.438, (202.253, 170.652, 199.313)), (' C  42  VAL HG12', ' D  26  HIS  HA ', -0.436, (158.259, 198.902, 210.497)), (" K  63    A  H2'", ' K  64    A  C8 ', -0.435, (143.432, 175.182, 199.038)), (' H  35  THR  N  ', ' H  38  LEU  O  ', -0.435, (190.525, 151.021, 217.598)), (' H 252  ASN  O  ', ' H 256  ASN  ND2', -0.434, (174.478, 159.759, 172.894)), (' D  54  LEU HD13', ' D 136  VAL HG11', -0.434, (178.167, 201.581, 200.11)), (' H  54  LEU HD13', ' H 136  VAL HG11', -0.433, (168.3, 144.499, 200.211)), (' D 605  1N7  H14', ' D 605  1N7  H29', -0.433, (188.835, 218.107, 122.503)), (' H 315  MET  HB2', ' H 315  MET  HE3', -0.432, (174.253, 128.657, 134.449)), (' H  53  ARG  HB2', ' H 126  ASP  HB2', -0.432, (173.952, 143.882, 206.317)), (' G  42  VAL HG23', ' G  69  GLY  H  ', -0.432, (188.85, 141.473, 213.2)), (' I   3    G  O6 ', ' J  68    C  N4 ', -0.432, (177.019, 163.659, 187.713)), (" L  59    U  H2'", ' L  60    A  C8 ', -0.431, (219.309, 169.769, 196.246)), (' D 473  CYS  O  ', ' D 478  ASN  ND2', -0.43, (182.225, 223.994, 127.9)), (' H 118  VAL HG21', ' H 152  LEU HD22', -0.43, (157.619, 144.603, 183.681)), (' B 350  PHE  HB2', ' B 363  ILE  HA ', -0.43, (131.337, 127.146, 150.899)), (" K  59    U  H2'", ' K  60    A  C8 ', -0.43, (126.044, 176.363, 195.907)), (" I   6    U H5''", " I   7    G  H5'", -0.429, (190.757, 166.901, 185.875)), (' F 350  PHE  HB2', ' F 363  ILE  HA ', -0.428, (214.486, 218.952, 150.497)), (' F 257  HIS  NE2', ' F 261  CYS  HB3', -0.426, (194.264, 194.673, 167.5)), (' B 471  ALA  HB3', ' H 516  THR HG23', -0.426, (160.492, 131.464, 125.96)), (' D 118  VAL HG21', ' D 152  LEU HD22', -0.426, (188.151, 201.757, 183.653)), (' C  42  VAL HG23', ' C  69  GLY  H  ', -0.425, (157.419, 204.227, 213.034)), (' D  30  ASP  N  ', ' D  30  ASP  OD1', -0.425, (164.322, 195.535, 215.081)), (" T  11    U  H2'", ' T  12    U  H6 ', -0.424, (136.575, 165.823, 191.602)), (' H  30  ASP  N  ', ' H  30  ASP  OD1', -0.424, (181.589, 150.402, 215.484)), (" I  11    U  H2'", ' I  12    U  C6 ', -0.424, (208.806, 180.633, 191.202)), (' G  42  VAL HG12', ' H  26  HIS  HA ', -0.423, (187.709, 147.001, 210.403)), (' D 153  MET  HB3', ' D 153  MET  HE3', -0.423, (188.362, 198.189, 192.761)), (' H 249  PHE  HZ ', ' H 284  GLU  HG3', -0.423, (179.988, 154.445, 167.943)), (' H 384  PHE  HB2', ' H 398  VAL HG22', -0.422, (171.878, 145.802, 138.456)), (' D 384  PHE  HB2', ' D 398  VAL HG22', -0.422, (174.159, 200.103, 138.451)), (" K  59    U  H2'", ' K  60    A  H8 ', -0.421, (126.415, 175.907, 196.077)), (" T  11    U  H2'", ' T  12    U  C6 ', -0.421, (136.903, 165.974, 191.481)), (' H 396  SER  HB2', ' H 439  LEU HD21', -0.42, (168.153, 146.946, 134.883)), (' H 153  MET  HB3', ' H 153  MET  HE3', -0.419, (157.657, 147.714, 192.79)), (' D 396  SER  HB2', ' D 439  LEU HD21', -0.418, (177.432, 199.094, 134.804)), (' D 351  TYR  HD2', ' D 366  LEU  HB2', -0.416, (163.379, 192.259, 136.343)), (' B 241  MET  HB3', ' B 241  MET  HE2', -0.416, (141.16, 168.837, 163.187)), (' B  42  ILE  HA ', ' B  43  PRO  HD3', -0.416, (136.792, 209.789, 187.676)), (' E  39  THR  O  ', ' E  78  ARG  NH2', -0.416, (214.182, 156.101, 177.064)), (" L  59    U  H2'", ' L  60    A  H8 ', -0.416, (219.649, 170.237, 195.93)), (" L  61    U  H2'", ' L  62    U  C6 ', -0.414, (210.254, 166.121, 196.618)), (' F 115  VAL HG21', ' F 169  MET  HG3', -0.414, (190.906, 178.738, 155.206)), (' B 257  HIS  NE2', ' B 261  CYS  HB3', -0.412, (151.565, 151.343, 167.353)), (' D 252  ASN  O  ', ' D 256  ASN  ND2', -0.412, (171.453, 186.232, 173.055)), (' H 701  1N7  H14', ' H 701  1N7  H29', -0.412, (157.092, 127.787, 122.402)), (' H 351  TYR  HD2', ' H 366  LEU  HB2', -0.411, (182.869, 153.509, 136.086)), (" T  14    U  H2'", ' T  15    A  C8 ', -0.41, (137.668, 170.024, 204.403)), (" K  61    U  H2'", ' K  62    U  C6 ', -0.409, (135.704, 179.814, 196.772)), (' D 383  LEU  HA ', ' D 383  LEU HD12', -0.409, (171.458, 202.743, 135.128)), (' B 234  ASP  N  ', ' B 234  ASP  OD1', -0.408, (148.283, 181.196, 152.606)), (' D 249  PHE  HZ ', ' D 284  GLU  HG3', -0.408, (166.234, 191.366, 168.281)), (' D 169  MET  HB3', ' D 169  MET  HE3', -0.407, (178.657, 211.156, 177.264)), (' E  10  ASN  HB3', ' E  14  LEU  HG ', -0.407, (213.09, 160.925, 174.31)), (' D 326  PHE  CD2', ' D 381  VAL  HB ', -0.406, (173.233, 201.771, 128.112)), (' H 169  MET  HB3', ' H 169  MET  HE3', -0.405, (167.5, 134.801, 177.18)), (' B  21  THR  O  ', ' B  22  GLN  HG2', -0.404, (141.611, 200.746, 178.525)), (' C   1  ALA  HB1', ' D 101  VAL HG12', -0.404, (175.727, 189.542, 200.661)), (" I  14    U  H2'", ' I  15    A  C8 ', -0.404, (208.237, 175.881, 204.452)), (' F 423  LYS  HB3', ' F 423  LYS  HE2', -0.404, (211.803, 197.383, 146.283)), (' D  83  VAL HG21', ' D 286  PHE  CE2', -0.403, (165.361, 202.765, 163.484)), (" I  11    U  H2'", ' I  12    U  H6 ', -0.403, (209.167, 180.254, 191.579)), (' A  10  ASN  HB3', ' A  14  LEU  HG ', -0.402, (132.903, 185.17, 174.299)), (' H  13  LYS  NZ ', ' H  98  ARG  O  ', -0.402, (163.542, 153.289, 204.523)), (' H  83  VAL HG21', ' H 286  PHE  CE2', -0.402, (180.66, 142.922, 163.718)), (' F  21  THR  O  ', ' F  22  GLN  HG2', -0.402, (204.788, 145.345, 178.744)), (' G   1  ALA  HB1', ' H 101  VAL HG12', -0.401, (170.701, 156.554, 200.812)), (' D 315  MET  HB2', ' D 315  MET  HE3', -0.401, (171.854, 217.382, 134.586))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
