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
data['rama'] = [('A', ' 830 ', 'ASP', 0.017412318026778513, (24.018, 33.541, 23.562)), ('A', ' 830 ', 'ASP', 0.019346499767537047, (23.674999999999986, 34.182, 23.626999999999992)), ('A', ' 830 ', 'ASP', 0.006554337693705072, (23.950999999999997, 34.019, 23.573999999999998)), ('A', ' 830 ', 'ASP', 0.047811671255231385, (23.960999999999988, 35.01, 23.477)), ('A', ' 830 ', 'ASP', 0.02476442151287527, (24.137999999999995, 33.93, 23.261999999999993)), ('A', ' 830 ', 'ASP', 0.01865031555694091, (23.61499999999999, 34.044, 24.022)), ('A', ' 830 ', 'ASP', 0.03722920194134038, (23.589999999999993, 33.372, 23.686999999999998)), ('A', ' 844 ', 'VAL', 0.07621685682657896, (34.968, 22.344, 21.011)), ('A', ' 838 ', 'GLY', 0.09678589191036009, (27.199999999999985, 24.389999999999997, 17.64)), ('A', ' 844 ', 'VAL', 0.043593002495325064, (35.205, 21.85999999999999, 21.028999999999996)), ('A', ' 830 ', 'ASP', 0.0016664612042504817, (22.987, 33.997, 23.066999999999997)), ('A', ' 856 ', 'ASN', 0.012972323540320426, (19.311, 23.700999999999993, 30.816)), ('A', ' 830 ', 'ASP', 0.04495460883263101, (23.845999999999986, 32.782, 23.562)), ('A', ' 830 ', 'ASP', 0.041117494688054305, (23.405, 34.198, 23.762)), ('A', ' 840 ', 'CYS', 0.027576362050023024, (28.033, 18.955, 18.987)), ('A', ' 830 ', 'ASP', 0.002368072018577157, (24.504, 33.738, 23.393)), ('A', ' 830 ', 'ASP', 0.04876230859390631, (23.197, 34.237, 23.114))]
data['omega'] = []
data['rota'] = [('A', ' 821 ', 'LEU', 0.14383327266196447, (27.419, 27.251, 34.77)), ('A', ' 822 ', 'LEU', 0.029882480262896437, (25.707, 27.001, 31.411999999999995)), ('A', ' 823 ', 'PHE', 0.16418897452114448, (24.59200000000001, 30.667, 31.632)), ('A', ' 839 ', 'ASP', 0.10919536687962295, (26.321999999999985, 20.883, 15.480999999999998)), ('A', ' 828 ', 'LEU', 0.10307278246972082, (27.569999999999997, 37.09, 25.89999999999999)), ('A', ' 854 ', 'LYS', 0.10557147471042369, (21.222, 19.438999999999993, 26.820999999999998)), ('A', ' 856 ', 'ASN', 0.07468844817097217, (19.041000000000015, 21.392, 30.971)), ('A', ' 834 ', 'ILE', 0.16214959166978005, (25.414, 28.304999999999993, 20.61)), ('A', ' 854 ', 'LYS', 0.00445936050863501, (21.259, 19.033, 26.613999999999997)), ('A', ' 837 ', 'TYR', 0.09729110902085172, (26.495999999999988, 28.612, 15.381)), ('A', ' 853 ', 'GLN', 0.0890536824314067, (22.776999999999994, 19.492, 29.002)), ('A', ' 835 ', 'LYS', 0.02011664028136162, (23.06699999999999, 25.652, 18.192)), ('A', ' 848 ', 'ASP', 0.220590023109196, (29.080999999999985, 21.756, 23.126)), ('A', ' 850 ', 'ILE', 0.01690325689978997, (23.878, 21.587999999999997, 24.59499999999999)), ('A', ' 825 ', 'LYS', 0.0, (30.05, 30.23, 28.916)), ('A', ' 849 ', 'LEU', 0.18865716955471715, (27.998, 22.610999999999994, 26.163)), ('A', ' 850 ', 'ILE', 0.10526059730990829, (24.315, 22.895999999999994, 24.894)), ('A', ' 816 ', 'SER', 0.25730208114467734, (20.802999999999987, 21.458, 38.501)), ('A', ' 850 ', 'ILE', 0.05803256341323725, (25.648999999999987, 22.381, 26.947999999999997)), ('A', ' 849 ', 'LEU', 0.12962804804067682, (27.074999999999992, 22.07999999999999, 27.342)), ('A', ' 818 ', 'ILE', 0.005054819990851214, (24.81, 22.955000000000002, 36.011)), ('A', ' 850 ', 'ILE', 0.0555476698414855, (24.15399999999999, 23.002999999999997, 24.646))]
data['cbeta'] = [('A', ' 827 ', 'THR', ' ', 0.2788425032088228, (27.771000000000015, 35.289, 30.067999999999998)), ('A', ' 830 ', 'ASP', ' ', 0.27232159989470245, (23.212, 34.577, 22.712)), ('A', ' 834 ', 'ILE', ' ', 0.31906911978048097, (25.583999999999985, 28.3, 21.161)), ('A', ' 816 ', 'SER', ' ', 0.28486054753404294, (18.669999999999987, 23.759999999999998, 37.85)), ('A', ' 823 ', 'PHE', ' ', 0.2894521736360611, (23.47, 31.41, 32.56)), ('A', ' 826 ', 'VAL', ' ', 0.2712786823255747, (25.220000000000013, 31.08, 26.48)), ('A', ' 830 ', 'ASP', ' ', 0.42404371092623183, (22.969999999999995, 34.75, 22.709999999999994)), ('A', ' 849 ', 'LEU', ' ', 0.4605280611587898, (27.45, 24.039999999999992, 27.41)), ('A', ' 850 ', 'ILE', ' ', 0.2500265746060084, (23.51, 23.31999999999999, 23.83)), ('A', ' 853 ', 'GLN', ' ', 0.27681665820154433, (24.510000000000016, 20.11999999999999, 30.619999999999997)), ('A', ' 827 ', 'THR', ' ', 0.25360172926059765, (26.356, 35.99, 29.814)), ('A', ' 830 ', 'ASP', ' ', 0.44006394039946223, (23.152, 34.999, 22.610999999999994)), ('A', ' 837 ', 'TYR', ' ', 0.2529460843668563, (27.202999999999985, 27.31099999999999, 15.98)), ('A', ' 844 ', 'VAL', ' ', 0.26862425496420766, (35.075, 22.697999999999997, 19.782)), ('A', ' 855 ', 'PHE', ' ', 0.25889812365005993, (19.736, 23.889, 26.586)), ('A', ' 816 ', 'SER', ' ', 0.2568943399879367, (20.381, 21.552, 37.528)), ('A', ' 818 ', 'ILE', ' ', 0.33964183365071104, (24.141999999999985, 21.349000000000014, 34.554)), ('A', ' 827 ', 'THR', ' ', 0.27921520320721593, (26.707000000000004, 35.774, 30.153)), ('A', ' 835 ', 'LYS', ' ', 0.2769905948006624, (20.874999999999986, 26.313, 20.982)), ('A', ' 837 ', 'TYR', ' ', 0.3301344430050503, (26.993999999999993, 27.515, 16.328)), ('A', ' 844 ', 'VAL', ' ', 0.34733953964184217, (35.197, 23.299, 20.215)), ('A', ' 846 ', 'ALA', ' ', 0.2782165745118224, (33.245, 26.597, 25.008)), ('A', ' 847 ', 'ARG', ' ', 0.27706844714139967, (30.69099999999999, 25.533999999999995, 20.059)), ('A', ' 848 ', 'ASP', ' ', 0.3000911886294557, (30.229, 20.477999999999998, 21.99)), ('A', ' 856 ', 'ASN', ' ', 0.2706646343254813, (19.083, 22.285999999999994, 31.940999999999992)), ('A', ' 816 ', 'SER', ' ', 0.25862765122999876, (21.281, 20.992999999999988, 41.161999999999985)), ('A', ' 827 ', 'THR', ' ', 0.3659715372490265, (26.926, 35.504, 29.56299999999999)), ('A', ' 833 ', 'PHE', ' ', 0.2978308399443415, (22.627, 33.35899999999997, 18.044)), ('A', ' 840 ', 'CYS', ' ', 0.4121004441129573, (26.883, 20.3, 20.149)), ('A', ' 856 ', 'ASN', ' ', 0.4607184259653934, (19.45, 25.163, 31.439)), ('A', ' 817 ', 'PHE', ' ', 0.3230134799637766, (27.034999999999986, 24.147, 41.403)), ('A', ' 819 ', 'GLU', ' ', 0.28840123464832707, (21.293, 25.413, 36.622)), ('A', ' 830 ', 'ASP', ' ', 0.36825845523750894, (22.885999999999996, 33.66, 22.692)), ('A', ' 839 ', 'ASP', ' ', 0.39190430948681015, (26.336, 20.787, 13.178)), ('A', ' 844 ', 'VAL', ' ', 0.426232973627958, (36.165, 22.98099999999999, 21.316)), ('A', ' 849 ', 'LEU', ' ', 0.2549881116123926, (29.005, 22.582, 27.864999999999995)), ('A', ' 855 ', 'PHE', ' ', 0.300886348486194, (17.731, 23.047, 25.46)), ('A', ' 816 ', 'SER', ' ', 0.26302518206893355, (18.96, 23.977, 37.668)), ('A', ' 820 ', 'ASP', ' ', 0.2601057066183466, (24.808, 29.018, 37.577)), ('A', ' 834 ', 'ILE', ' ', 0.25977016170247325, (25.438, 28.919999999999998, 22.264)), ('A', ' 844 ', 'VAL', ' ', 0.2792099651129859, (34.775, 23.242, 20.337999999999997)), ('A', ' 854 ', 'LYS', ' ', 0.28247081206044966, (20.24, 17.093, 27.349999999999998)), ('A', ' 856 ', 'ASN', ' ', 0.32346700694281005, (19.335999999999988, 21.88799999999999, 32.183)), ('A', ' 818 ', 'ILE', ' ', 0.30295912492771454, (24.43099999999999, 22.687, 35.73)), ('A', ' 827 ', 'THR', ' ', 0.2960019772038047, (27.019, 36.13300000000001, 29.792999999999996)), ('A', ' 834 ', 'ILE', ' ', 0.2648768088893923, (25.256999999999987, 28.067999999999987, 21.525)), ('A', ' 844 ', 'VAL', ' ', 0.4178944374885663, (34.52, 23.965, 19.815)), ('A', ' 856 ', 'ASN', ' ', 0.4293587947710667, (19.326999999999988, 23.282, 32.043)), ('A', ' 819 ', 'GLU', ' ', 0.3017430970311186, (22.366999999999987, 25.418, 36.141)), ('A', ' 837 ', 'TYR', ' ', 0.2523855975646882, (26.907, 29.439999999999994, 15.098999999999998)), ('A', ' 850 ', 'ILE', ' ', 0.25359071911974385, (24.766, 22.40499999999999, 22.647)), ('A', ' 851 ', 'CYS', ' ', 0.2652720598542702, (26.299999999999986, 17.336, 23.519999999999996)), ('A', ' 854 ', 'LYS', ' ', 0.41634856677541554, (19.222, 17.261, 25.021)), ('A', ' 817 ', 'PHE', ' ', 0.27448522049474045, (23.431999999999984, 22.65, 40.198)), ('A', ' 825 ', 'LYS', ' ', 0.2610417758961896, (30.4, 28.769, 28.558999999999997)), ('A', ' 839 ', 'ASP', ' ', 0.29434892951863195, (26.391, 21.451, 14.683)), ('A', ' 847 ', 'ARG', ' ', 0.26148547650606235, (30.868, 25.669, 20.603999999999996)), ('A', ' 853 ', 'GLN', ' ', 0.29088874818746946, (24.4, 20.867, 30.102)), ('A', ' 856 ', 'ASN', ' ', 0.4172079833146167, (18.811, 23.22399999999999, 31.968)), ('A', ' 830 ', 'ASP', ' ', 0.3710066575040606, (23.172999999999988, 35.137, 22.817999999999998)), ('A', ' 840 ', 'CYS', ' ', 0.2899711433930987, (26.725, 19.059, 19.898)), ('A', ' 855 ', 'PHE', ' ', 0.585459718851225, (20.272999999999996, 23.12799999999999, 24.11)), ('A', ' 856 ', 'ASN', ' ', 0.25295850383440943, (19.071, 23.059, 30.343)), ('A', ' 824 ', 'ASN', ' ', 0.28964887074394957, (27.367999999999988, 32.089000000000006, 34.017)), ('A', ' 839 ', 'ASP', ' ', 0.2598674234898705, (25.835999999999984, 19.97899999999999, 14.015999999999996)), ('A', ' 840 ', 'CYS', ' ', 0.3114076153399241, (26.82599999999999, 19.75299999999999, 19.522)), ('A', ' 848 ', 'ASP', ' ', 0.2848235676644671, (31.808, 19.045, 25.528)), ('A', ' 818 ', 'ILE', ' ', 0.29682248038985604, (22.985, 22.232000000000003, 35.663)), ('A', ' 823 ', 'PHE', ' ', 0.32663516597626524, (23.615999999999985, 31.515, 32.742)), ('A', ' 827 ', 'THR', ' ', 0.280013791200386, (28.097, 35.466, 30.009)), ('A', ' 840 ', 'CYS', ' ', 0.30119685282764663, (26.672, 18.557, 19.331)), ('A', ' 844 ', 'VAL', ' ', 0.26440496351825254, (33.832, 23.733, 20.047)), ('A', ' 818 ', 'ILE', ' ', 0.45122041365579674, (26.492999999999984, 22.010000000000016, 34.407)), ('A', ' 824 ', 'ASN', ' ', 0.27209367329308004, (29.084999999999987, 32.051, 33.529)), ('A', ' 830 ', 'ASP', ' ', 0.34581179785092336, (22.462999999999987, 34.78, 23.298999999999996)), ('A', ' 836 ', 'GLN', ' ', 0.28090468161404486, (21.636999999999997, 28.495, 14.785999999999998)), ('A', ' 837 ', 'TYR', ' ', 0.2926287146192709, (26.8, 28.105, 15.654999999999998)), ('A', ' 840 ', 'CYS', ' ', 0.2723984180263854, (26.595999999999986, 18.051, 18.346)), ('A', ' 844 ', 'VAL', ' ', 0.4335931361335002, (34.695, 23.414, 20.906)), ('A', ' 854 ', 'LYS', ' ', 0.43876856517304713, (19.655, 17.268999999999995, 26.658999999999995)), ('A', ' 856 ', 'ASN', ' ', 0.2848580294261959, (20.820999999999998, 22.51499999999999, 31.4)), ('A', ' 844 ', 'VAL', ' ', 0.4105822442522895, (34.533, 23.442, 20.042)), ('A', ' 851 ', 'CYS', ' ', 0.2757947910985678, (24.692, 18.760999999999996, 22.147)), ('A', ' 856 ', 'ASN', ' ', 0.26332573223644146, (19.674, 23.20699999999999, 32.472))]
data['probe'] = [(' A 826  VAL HG12', ' A 834  ILE HD12', -0.538, (26.815, 29.702, 24.038)), (' A 822  LEU  HA ', ' A 849  LEU HD12', -0.425, (26.662, 26.238, 29.738))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
