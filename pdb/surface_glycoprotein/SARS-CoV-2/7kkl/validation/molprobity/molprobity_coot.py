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
data['rota'] = [('A', '  61 ', 'ASN', 0.04491214600439816, (184.942, 116.808, 158.256)), ('A', ' 603 ', 'ASN', 0.08072606209060254, (184.384, 130.648, 182.873)), ('A', ' 657 ', 'ASN', 0.1144232698964255, (161.317, 118.337, 191.941)), ('A', '1134 ', 'ASN', 0.18242600491502867, (148.898, 138.692, 240.931)), ('C', '  61 ', 'ASN', 0.08213566647992494, (110.17099999999998, 160.314, 158.265)), ('C', ' 603 ', 'ASN', 0.08012093794914689, (122.47099999999998, 153.86100000000005, 182.872)), ('C', ' 657 ', 'ASN', 0.1113374922942137, (123.34799999999997, 179.99800000000005, 191.94)), ('C', '1134 ', 'ASN', 0.19177773644175028, (147.20100000000005, 180.566, 240.929)), ('D', '  61 ', 'ASN', 0.08211008841483426, (185.268, 203.297, 158.264)), ('D', ' 603 ', 'ASN', 0.08049478286892195, (173.53, 195.869, 182.875)), ('D', ' 657 ', 'ASN', 0.1099125100545276, (195.724, 182.047, 191.941)), ('D', '1134 ', 'ASN', 0.18424369310538177, (184.30500000000006, 161.115, 240.93000000000006))]
data['cbeta'] = []
data['probe'] = [(' D 715  PRO  HA ', ' D1071  GLN  O  ', -0.889, (174.723, 177.913, 221.66)), (' A 715  PRO  HA ', ' A1071  GLN  O  ', -0.883, (168.175, 138.579, 221.618)), (' C 715  PRO  HA ', ' C1071  GLN  O  ', -0.852, (137.193, 163.958, 221.78)), (' C 557  LYS  NZ ', ' C 574  ASP  OD2', -0.554, (148.679, 193.915, 162.742)), (' D 557  LYS  NZ ', ' D 574  ASP  OD2', -0.551, (195.616, 153.2, 162.832)), (' A 557  LYS  NZ ', ' A 574  ASP  OD2', -0.55, (136.454, 132.799, 162.793)), (' D 715  PRO  CA ', ' D1071  GLN  O  ', -0.54, (174.351, 177.539, 222.101)), (' D 811  LYS  NZ ', ' D 820  ASP  OD2', -0.532, (147.384, 193.079, 197.626)), (' D 725  GLU  OE2', ' D1028  LYS  NZ ', -0.53, (161.672, 170.856, 199.576)), (' A 908  GLY  O  ', ' A1038  LYS  NZ ', -0.523, (165.2, 156.554, 217.31)), (' C 908  GLY  O  ', ' C1038  LYS  NZ ', -0.522, (154.486, 157.507, 217.294)), (' A 811  LYS  NZ ', ' A 820  ASP  OD2', -0.521, (194.89, 154.415, 197.8)), (' A 340  GLU  OE1', ' A 356  LYS  NZ ', -0.52, (131.048, 136.906, 123.657)), (' C 725  GLU  OE2', ' C1028  LYS  NZ ', -0.517, (150.05, 156.078, 199.669)), (' A 725  GLU  OE2', ' A1028  LYS  NZ ', -0.517, (168.66, 153.399, 199.665)), (' D 908  GLY  O  ', ' D1038  LYS  NZ ', -0.517, (160.559, 166.42, 217.244)), (' D 656  VAL  HA ', ' D1305  NAG  H81', -0.514, (196.109, 185.134, 188.903)), (' C 656  VAL  HA ', ' C1305  NAG  H81', -0.513, (119.977, 178.761, 188.756)), (' A 715  PRO  CA ', ' A1071  GLN  O  ', -0.51, (168.019, 139.071, 222.155)), (' A 656  VAL  HA ', ' A1305  NAG  H81', -0.51, (164.336, 116.048, 188.933)), (' D 340  GLU  OE1', ' D 356  LYS  NZ ', -0.509, (194.848, 146.959, 123.356)), (' C 360  ASN  H  ', ' C 523  THR HG22', -0.5, (152.051, 197.394, 136.892)), (' D 360  ASN  H  ', ' D 523  THR HG22', -0.5, (196.426, 148.672, 136.496)), (' A 360  ASN  H  ', ' A 523  THR HG22', -0.493, (131.928, 134.602, 136.883)), (' C 811  LYS  NZ ', ' C 820  ASP  OD2', -0.481, (137.948, 132.593, 197.527)), (' C 340  GLU  OE1', ' C 356  LYS  NZ ', -0.479, (154.402, 196.978, 123.752)), (' C 138  ASP  N  ', ' C 138  ASP  OD2', -0.469, (99.264, 154.527, 133.509)), (' C 393  THR  OG1', ' C 394  ASN  N  ', -0.46, (156.336, 191.235, 138.965)), (' D 393  THR  OG1', ' D 394  ASN  N  ', -0.457, (188.993, 148.135, 139.115)), (' A 138  ASP  N  ', ' A 138  ASP  OD2', -0.456, (195.399, 110.174, 133.552)), (' A 393  THR  OG1', ' A 394  ASN  N  ', -0.455, (134.867, 141.409, 139.395)), (' C 535  LYS  NZ ', ' C 554  GLU  OE2', -0.451, (134.94, 200.781, 158.336)), (' D 535  LYS  NZ ', ' D 554  GLU  OE2', -0.444, (207.906, 161.507, 158.215)), (' A 386  LYS  NZ ', ' C 985  ASP  OD1', -0.438, (156.184, 139.647, 138.611)), (' C 386  LYS  NZ ', ' D 985  ASP  OD1', -0.434, (144.759, 173.55, 138.424)), (' D 202  LYS  NZ ', ' D 228  ASP  OD2', -0.429, (163.012, 196.872, 144.507)), (' D 138  ASP  N  ', ' D 138  ASP  OD2', -0.423, (185.871, 215.705, 133.436)), (' A 535  LYS  NZ ', ' A 554  GLU  OE2', -0.422, (137.452, 118.289, 158.16)), (' A  60  SER  HA ', ' A1301  NAG  H81', -0.416, (181.078, 118.336, 160.023)), (' F  32  ASN  OD1', ' F  33  ALA  N  ', -0.409, (165.15, 133.426, 108.898)), (' B  32  ASN  OD1', ' B  33  ALA  N  ', -0.406, (134.564, 169.043, 108.878)), (' D 745  ASP  N  ', ' D 745  ASP  OD1', -0.404, (141.957, 175.558, 156.034)), (' D 758  SER  O  ', ' D 759  PHE  C  ', -0.404, (147.249, 159.534, 165.041)), (' C 758  SER  O  ', ' C 759  PHE  C  ', -0.404, (167.462, 149.259, 165.194))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
