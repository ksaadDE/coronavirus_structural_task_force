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
data['omega'] = [('H', ' 163 ', 'PRO', None, (22.001, 31.738999999999997, -31.692999999999998)), ('H', ' 165 ', 'PRO', None, (17.489, 27.507, -30.307)), ('L', ' 145 ', 'PRO', None, (18.769, 2.501999999999998, -45.601))]
data['rota'] = [('A', ' 484 ', 'GLU', 0.014827031363343315, (30.33599999999999, 10.615, 0.458)), ('H', '  72 ', 'ARG', 0.13872183013445383, (20.805, 23.443, -4.634))]
data['cbeta'] = [('L', '  52 ', 'ASP', ' ', 0.355037745119281, (17.367, -3.841, -7.878))]
data['probe'] = [(' A 472  ILE HD13', ' A 482  GLY  HA2', -0.851, (31.61, 13.895, 4.318)), (' L 198  GLN  HB2', ' L 207  GLU  HG3', -0.63, (22.678, 14.885, -59.338)), (' A 456  PHE  HB2', ' A 491  PRO  HA ', -0.621, (23.412, 9.398, 8.126)), (' L 136  LEU  HB2', ' L 182  LEU  HB3', -0.62, (22.797, 25.216, -53.596)), (' L  94  THR HG22', ' L  96  SER  H  ', -0.609, (34.285, 1.994, -6.24)), (' A 352  ALA  HB1', ' A 466  ARG HH21', -0.606, (19.357, 22.181, 17.011)), (' L  35  VAL HG12', ' L  53  VAL HG22', -0.606, (22.586, -6.573, -11.666)), (' A 422  ASN  OD1', ' A 454  ARG  N  ', -0.581, (16.715, 12.157, 13.036)), (' H 185  VAL  HB ', ' L 166  THR HG22', -0.575, (22.566, 20.218, -42.071)), (' H 125  ILE HG23', ' H 127  VAL  H  ', -0.568, (30.738, 31.721, -31.787)), (' A 418  ILE  HA ', ' A 422  ASN  HB2', -0.556, (14.572, 9.873, 16.27)), (' L  28  ASP  N  ', ' L  28  ASP  OD1', -0.541, (32.369, -4.13, -9.407)), (' H   6  GLN  H  ', ' H 118  ILE HG12', -0.538, (14.483, 20.133, -18.412)), (' H  48  MET  HE1', ' H  81  MET  SD ', -0.535, (26.94, 18.692, -15.152)), (' A 453  TYR  HB3', ' A 495  TYR  CZ ', -0.535, (12.256, 13.247, 11.297)), (' A 409  GLN HE22', ' A 416  GLY  HA3', -0.527, (11.117, 3.014, 16.189)), (' A 344  ALA  HB3', ' A 347  PHE  CE1', -0.522, (7.372, 26.135, 18.595)), (' H   2  VAL HG22', ' H  27  TYR  HB3', -0.519, (7.624, 12.921, -7.375)), (' L   5  THR  HB ', ' L  23  THR  HB ', -0.514, (33.215, -5.831, -20.247)), (' H 187  GLN HE21', ' H 191  LEU  HB2', -0.513, (25.053, 30.586, -40.795)), (' A 452  LEU  HA ', ' A 494  SER  HA ', -0.509, (14.77, 15.898, 7.231)), (' H  52 BASN  HB2', ' H  56  ASP  O  ', -0.506, (24.531, 17.368, 0.389)), (' A 431  GLY  HA2', ' A 515  PHE  CE2', -0.505, (5.832, 15.891, 34.207)), (' A 486  PHE  CG ', ' L  93  TYR  HE2', -0.504, (28.237, 1.499, -2.299)), (' A 486  PHE  CD1', ' L  93  TYR  HE2', -0.503, (28.032, 1.653, -2.293)), (' H  34  MET  HG2', ' H  79  VAL HG11', -0.496, (19.473, 18.434, -8.936)), (' A 492  LEU  O  ', ' A 493  GLN  NE2', -0.492, (19.773, 11.897, 4.442)), (' H 182  PHE  CD2', ' L 139  LEU HD22', -0.491, (14.285, 19.638, -45.401)), (' H  33  TYR  HB2', ' H 100  GLY  HA3', -0.483, (20.399, 9.542, -4.929)), (' A 447  GLY  HA3', ' A 449  TYR  CZ ', -0.482, (9.701, 18.973, -1.395)), (' H  33  TYR  CE2', ' H 101  SER  HB2', -0.481, (21.831, 8.963, -1.269)), (' L 114  LYS  HE2', ' L 201  HIS  CE1', -0.48, (18.217, 2.863, -50.456)), (' A 484  GLU  HA ', ' A 488  CYS  HB3', -0.477, (30.621, 9.382, 1.629)), (' H  13  LYS  NZ ', ' H 127  VAL  O  ', -0.475, (29.444, 34.303, -30.095)), (' A 486  PHE  HB3', ' L  97  SER  HA ', -0.468, (30.716, 4.485, -3.437)), (' H 175  LEU  HA ', ' H 175  LEU HD12', -0.465, (-3.992, 22.833, -40.381)), (' L 171  GLN  HG2', ' L 175  LYS  O  ', -0.465, (12.917, 9.427, -40.259)), (' H  29  PHE  HE1', ' H  34  MET  HE3', -0.459, (16.599, 17.128, -7.733)), (' L  50  ILE HD13', ' L  75  LEU  CD1', -0.454, (16.674, -4.964, -19.185)), (' H  47  TRP  HZ2', ' H  50  TRP  CD1', -0.454, (27.364, 10.984, -7.608)), (' A 376  THR  HB ', ' A 435  ALA  HB3', -0.453, (0.902, 12.56, 21.631)), (' H  35  HIS  HB2', ' H  97  ALA  HB3', -0.453, (21.759, 11.432, -11.825)), (' L  81  GLN  HB3', ' L  83  GLU  OE1', -0.452, (8.79, -2.922, -32.564)), (' L  27  SER  OG ', ' L  28  ASP  OD1', -0.45, (33.819, -3.624, -10.193)), (' H 188  SER  N  ', ' L 164  GLU  OE2', -0.447, (29.706, 25.691, -43.266)), (' L  25  THR  O  ', ' L  27  SER  N  ', -0.446, (34.68, -6.582, -9.594)), (' A 480  CYS  O  ', ' A 483  VAL  N  ', -0.445, (34.437, 12.102, 1.842)), (' L  30  GLY  HA2', ' L  70  GLY  O  ', -0.443, (30.687, -10.942, -10.424)), (' L 184  LEU HD23', ' L 189  TRP  HB2', -0.441, (23.388, 30.659, -58.081)), (' A 438  SER  OG ', ' A 442  ASP  OD2', -0.44, (3.766, 20.131, 11.97)), (' H  47  TRP  CD2', ' L  99  PHE  HB3', -0.439, (28.175, 8.839, -11.132)), (' L  50  ILE HD11', ' L  64  PHE  HB3', -0.435, (14.487, -5.052, -19.2)), (' A 397  ALA  HA ', ' A 512  VAL  O  ', -0.434, (9.153, 19.821, 27.442)), (' H 160  ASP  OD1', ' H 187  GLN  NE2', -0.429, (24.238, 31.101, -42.583)), (' A 417  LYS  O  ', ' A 422  ASN  ND2', -0.429, (15.857, 8.701, 14.905)), (' H  36  TRP  HB3', ' H  48  MET  HE2', -0.428, (25.452, 16.509, -14.433)), (' L 114  LYS  HE2', ' L 201  HIS  HE1', -0.426, (18.027, 2.73, -50.228)), (' L  22  CYS  HB2', ' L  37  TRP  CH2', -0.426, (25.23, -4.964, -19.559)), (' H 182  PHE  CE2', ' L 139  LEU  HB3', -0.425, (13.473, 18.49, -46.5)), (' A 436  TRP  O  ', ' A 509  ARG  N  ', -0.424, (1.634, 17.421, 16.375)), (' A 437  ASN  HA ', ' A 508  TYR  CG ', -0.421, (-0.419, 15.951, 14.291)), (' L 124  PRO  HG2', ' L 189  TRP  CD2', -0.421, (20.145, 30.539, -58.51)), (' H  33  TYR  H  ', ' H 100  GLY  HA3', -0.415, (18.981, 9.827, -4.162)), (' L 148  VAL HG22', ' L 168  PRO  HG3', -0.412, (22.275, 11.137, -44.968)), (' H  60  TYR  CE2', ' H  70  MET  HE2', -0.41, (29.878, 17.872, -8.735)), (' H  72  ARG  HA ', ' H  79  VAL  HA ', -0.408, (19.899, 23.123, -6.559)), (' A 434  ILE  HB ', ' A 511  VAL  HB ', -0.405, (2.861, 19.228, 24.655)), (' A 497  PHE  O  ', ' A 498  GLN  HG3', -0.404, (5.469, 17.112, 1.908)), (' A 409  GLN  HB2', ' A 410  ILE HD12', -0.403, (9.238, 8.907, 19.078)), (' H  71  THR  O  ', ' H  80  TYR  N  ', -0.403, (21.728, 23.601, -8.033)), (' H  37  VAL  HA ', ' H  48  MET  HG3', -0.402, (26.937, 13.428, -15.823)), (' L 184  LEU HD21', ' L 195  TYR  CZ ', -0.402, (25.063, 28.497, -58.719)), (' H 166  VAL HG12', ' H 216  HIS  CD2', -0.4, (16.565, 31.408, -34.284))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
