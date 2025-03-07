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
data['rama'] = [('A', ' 257 ', 'ASN', 0.034026303516169476, (1.8029999999999893, -7.559000000000005, -66.132)), ('A', ' 351 ', 'THR', 0.009638302243038415, (-10.940000000000007, 12.684000000000001, -50.575)), ('A', ' 484 ', 'VAL', 0.016347227668110247, (-32.764, 37.687, -80.998)), ('B', '   9 ', 'ASN', 0.007822716917028103, (8.068999999999999, 6.101, -34.657)), ('B', ' 161 ', 'ARG', 0.033908977602114275, (-43.51000000000002, 24.401, -38.068))]
data['omega'] = []
data['rota'] = [('A', '   7 ', 'LEU', 0.09819432730620596, (6.269999999999995, 41.997, -63.136999999999986)), ('A', '  12 ', 'THR', 0.0069040531198026325, (7.598999999999997, 47.139999999999986, -52.54299999999999)), ('A', '  20 ', 'ILE', 0.25868804387021316, (-9.271000000000008, 46.196, -60.61699999999998)), ('A', '  35 ', 'ILE', 0.07024771176692156, (3.4069999999999947, 57.366, -66.685)), ('A', '  46 ', 'ASN', 0.014939904735856806, (-2.0189999999999992, 54.94499999999999, -46.90699999999998)), ('A', '  76 ', 'LYS', 0.24415500983700666, (3.783000000000004, 71.029, -50.903)), ('A', '  81 ', 'PHE', 0.010424695108074707, (10.543000000000006, 65.46799999999998, -53.29)), ('A', ' 173 ', 'ARG', 0.13259042426500772, (-31.539000000000016, 40.641999999999996, -71.244)), ('A', ' 209 ', 'VAL', 0.009070819764369882, (-40.44200000000001, 30.300999999999995, -72.216)), ('A', ' 226 ', 'VAL', 0.2971456071140945, (-30.249, 36.676, -61.153999999999996)), ('A', ' 231 ', 'THR', 0.16233519226823817, (-16.104000000000003, 36.782, -56.057)), ('A', ' 255 ', 'THR', 0.0013599335943581536, (3.643999999999995, -3.2709999999999972, -63.635)), ('A', ' 416 ', 'THR', 0.2623868628645772, (-11.507000000000005, 35.033999999999985, -83.31199999999998)), ('A', ' 502 ', 'ARG', 0.23569268659941822, (-36.835000000000015, 8.25699999999999, -97.36)), ('A', ' 530 ', 'THR', 0.021981978655166073, (-31.208, 17.732, -80.042)), ('B', '   7 ', 'LEU', 0.299614881687036, (3.7939999999999965, 3.701999999999999, -30.805999999999997)), ('B', '   8 ', 'CYS', 0.2980180629779128, (7.547999999999999, 3.594999999999996, -31.771)), ('B', '  12 ', 'THR', 0.0027198671887163073, (7.078999999999995, 0.7039999999999953, -41.691)), ('B', '  26 ', 'CYS', 0.2839744989614092, (6.342999999999994, -1.2569999999999997, -36.807)), ('B', '  35 ', 'ILE', 0.2998813722749804, (-1.5620000000000047, -11.359000000000009, -31.458)), ('B', '  76 ', 'LYS', 0.0, (0.5449999999999875, -21.62399999999999, -50.563999999999986)), ('B', '  95 ', 'ASN', 0.005519052018370991, (15.587999999999996, -3.8160000000000007, -40.47099999999999)), ('B', ' 124 ', 'ASN', 0.055508939572196325, (-6.357000000000001, 12.269, -22.868)), ('B', ' 144 ', 'THR', 0.21636923125864987, (-20.197000000000013, 6.087999999999998, -38.735)), ('B', ' 164 ', 'HIS', 0.05802707696520563, (-45.843, 13.768999999999997, -39.382)), ('B', ' 195 ', 'ILE', 0.26498021653334947, (-33.04000000000001, 21.202, -49.053)), ('B', ' 215 ', 'THR', 0.08781925081927454, (-33.926, 27.738, -44.368)), ('B', ' 220 ', 'ASN', 0.032101535779357655, (-43.75900000000001, 18.597999999999992, -49.18999999999998)), ('B', ' 353 ', 'GLU', 0.03465773026881207, (-6.209999999999999, 40.608, -43.58299999999999)), ('B', ' 484 ', 'VAL', 0.1774727997853319, (-38.20800000000001, 8.305999999999997, -25.721999999999998)), ('B', ' 486 ', 'SER', 0.2539286901582246, (-35.954, 13.106, -22.314))]
data['cbeta'] = [('B', ' 136 ', 'GLU', ' ', 0.2642170181534287, (-8.106000000000003, 9.812999999999997, -35.971))]
data['probe'] = [(' B  23  PRO  CA ', ' B  23  PRO  N  ', -1.462, (-2.619, 4.077, -38.553)), (' B  23  PRO  C  ', ' B  23  PRO  N  ', -0.666, (-2.153, 2.663, -38.868)), (' A 352  LEU HD11', ' B 234  PRO  HD3', -0.638, (-7.615, 11.953, -44.335)), (' B 238  PRO  HB2', ' B 240  LEU  O  ', -0.631, (1.572, 19.303, -29.955)), (' B   6  VAL  HA ', ' B 129  ARG  HE ', -0.625, (2.397, 7.435, -34.251)), (' B 510  VAL HG21', ' B 541  TYR  CD1', -0.62, (-33.352, 34.239, -21.622)), (' B   8  CYS  SG ', ' B  99  GLY  N  ', -0.618, (9.648, 0.143, -31.675)), (' B  13  SER  O  ', ' B  44  SER  HA ', -0.602, (2.181, -2.155, -46.1)), (' A 293  ILE HG13', ' A 320  LYS  HB3', -0.595, (-11.876, 5.409, -68.037)), (' B 477  LYS  NZ ', ' B 551  GLU  OE2', -0.585, (-33.693, 13.836, -4.736)), (' B 474 BMET  HG2', ' B 590  LEU  HB2', -0.581, (-39.439, 28.362, -2.799)), (' A 510  VAL HG21', ' A 541  TYR  CD1', -0.56, (-26.323, 11.458, -80.341)), (' B 103  VAL  O  ', ' B 103  VAL HG12', -0.553, (-1.309, -2.003, -28.123)), (' B 474 AMET  SD ', ' B 495  VAL HG11', -0.543, (-41.273, 24.633, -5.65)), (' A  12  THR HG21', ' A  26  CYS  HA ', -0.542, (8.128, 48.49, -56.217)), (' A 281  GLN  HB2', ' A 429  MET  HE2', -0.541, (-2.417, 17.825, -78.085)), (' A 445  PRO  HB3', ' A 468  SER  HB3', -0.538, (-18.79, 5.489, -91.968)), (' A 277  TYR  HA ', ' A 396  TYR  O  ', -0.532, (2.425, 16.3, -66.661)), (' A 368  ALA  O  ', ' A 393  ALA  HA ', -0.531, (1.031, 14.739, -56.87)), (' B  31  TYR  CZ ', ' B  35  ILE HG21', -0.518, (2.548, -12.742, -32.765)), (' B 195  ILE  O  ', ' B 195  ILE HG23', -0.518, (-34.724, 21.46, -47.595)), (' A 260  ASP  HA ', ' A 263  SER  OG ', -0.517, (-1.399, -5.096, -74.61)), (' B 120  TYR  CE2', ' B 409  ARG  HG2', -0.513, (-16.679, 11.416, -26.144)), (' B 277  TYR  HA ', ' B 396  TYR  O  ', -0.511, (-0.387, 30.22, -26.826)), (' B 333  ILE  HB ', ' B 358  CYS  SG ', -0.504, (-11.991, 31.008, -41.675)), (' A 512  ILE  O  ', ' A 546  PHE  HA ', -0.501, (-26.675, 19.503, -87.471)), (' A 304  ILE HG12', ' A 370  ILE  HB ', -0.497, (-2.14, 9.138, -61.415)), (' A 519  ASN  HB3', ' A 530  THR HG23', -0.495, (-31.181, 20.983, -80.09)), (' A  60  VAL  HB ', ' A 923  HOH  O  ', -0.491, (-0.516, 58.449, -57.221)), (' A  59  ASP  OD1', ' A  61  THR  OG1', -0.482, (0.03, 62.479, -62.326)), (' A  12  THR  CG2', ' A  26  CYS  HA ', -0.48, (8.18, 48.131, -55.899)), (' B 252  LEU  HB3', ' B 299  TYR  CD1', -0.479, (2.702, 42.288, -29.081)), (' A 519  ASN  HB3', ' A 530  THR  CG2', -0.475, (-31.626, 20.96, -79.858)), (' B 127  THR HG23', ' B 970  HOH  O  ', -0.473, (1.108, 6.483, -24.313)), (' B   8  CYS  O  ', ' B   9  ASN  HB2', -0.473, (8.868, 6.511, -32.828)), (' B 544  VAL  O  ', ' B 572  ILE  HA ', -0.465, (-33.99, 33.107, -11.828)), (' B 504  PRO  HB3', ' B 507  ARG HH21', -0.464, (-48.205, 38.087, -12.81)), (' A 215  THR HG22', ' B 193  VAL HG21', -0.463, (-31.457, 20.997, -55.626)), (' B 183  THR  OG1', ' B 228  THR  OG1', -0.461, (-27.025, 17.254, -43.47)), (' B 124  ASN  OD1', ' B 381  ASN  ND2', -0.461, (-7.801, 14.743, -25.514)), (' A 183  THR  O  ', ' A 225  PHE  HA ', -0.461, (-32.648, 34.113, -59.861)), (' B 508  LYS  HD3', ' B 905  HOH  O  ', -0.451, (-36.856, 41.475, -17.917)), (' A 304  ILE  HA ', ' A 370  ILE  O  ', -0.45, (-3.158, 11.209, -59.896)), (' A 367  THR  HA ', ' A 392  ARG  O  ', -0.447, (-0.53, 16.412, -53.996)), (' A 120  TYR  CE2', ' A 409  ARG  HG2', -0.447, (-11.327, 35.463, -73.656)), (' A 252  LEU  HB3', ' A 299  TYR  CD2', -0.441, (4.491, 4.734, -62.086)), (' B 376  ILE  HA ', ' B 376  ILE HD12', -0.44, (-11.231, 25.449, -26.919)), (' A 456  VAL HG23', ' A 457  TYR  CD2', -0.439, (-8.243, 17.826, -86.92)), (' A 152  ALA  HB2', ' A 167  TRP  CZ3', -0.438, (-34.548, 37.497, -66.652)), (' B 376  ILE HG12', ' B 425  VAL HG11', -0.435, (-7.59, 25.55, -24.196)), (' A  14  LEU  HB2', ' A  25  LEU  O  ', -0.432, (4.961, 49.14, -56.135)), (' B 121  ILE HG23', ' B 421  TYR  CE1', -0.427, (-8.587, 10.826, -17.336)), (' B  13  SER  HB2', ' B  92  LEU  HB2', -0.426, (7.349, -1.302, -46.65)), (' A 296  ALA  O  ', ' A 300  PRO  HA ', -0.426, (-2.36, 1.321, -61.333)), (' B 533  VAL HG11', ' B 560  ARG  O  ', -0.426, (-25.893, 24.004, -16.663)), (' B  86  ASN  HB3', ' B 913  HOH  O  ', -0.424, (12.953, -12.905, -33.911)), (' B 143  GLU  HA ', ' B 146  LYS  HD2', -0.423, (-21.052, 10.961, -37.662)), (' B 451  THR HG21', ' B 585  LEU HD23', -0.417, (-25.969, 27.57, -6.095)), (' A  64  TYR  O  ', ' A  70  TYR  HA ', -0.415, (3.586, 64.408, -50.643)), (' A  13  SER  O  ', ' A  44  SER  HA ', -0.414, (2.135, 50.515, -50.619)), (' A 472  PHE  HA ', ' A 588  THR  O  ', -0.414, (-23.47, 12.799, -99.006)), (' A 157  VAL HG21', ' A 219  LEU  O  ', -0.41, (-45.543, 29.725, -60.568)), (' A 269  TYR  OH ', ' A 294  GLY  HA3', -0.409, (-4.065, 3.178, -69.67)), (' A  16  CYS  O  ', ' A  22  ARG  HA ', -0.408, (-4.164, 48.172, -57.597)), (' A 152  ALA  HB2', ' A 167  TRP  CH2', -0.405, (-34.698, 37.283, -66.776)), (' B 167  TRP  CZ3', ' B 174  PRO  HD2', -0.404, (-34.737, 9.201, -36.628)), (' B  69  SER  OG ', ' B  71  TYR  OH ', -0.404, (0.467, -15.302, -56.076)), (' A 182  PHE  HB3', ' A 225  PHE  HB3', -0.403, (-32.625, 33.476, -62.725)), (' B 377  SER  O  ', ' B 406  PRO  HA ', -0.403, (-16.311, 21.256, -23.592)), (' B 266  VAL  O  ', ' B 270  GLN  HG3', -0.402, (1.162, 43.176, -20.298)), (' A 278  SER  HB2', ' A 436  MET  HE2', -0.4, (2.882, 13.939, -72.271))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
