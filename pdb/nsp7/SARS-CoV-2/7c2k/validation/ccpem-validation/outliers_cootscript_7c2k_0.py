
from __future__ import division
import cPickle
try :
  import gobject
except ImportError :
  gobject = None
import sys

dict_residue_prop_objects = {}
class coot_extension_gui (object) :
  def __init__ (self, title) :
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

  def finish_window (self) :
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window (self, *args) :
    self.window.destroy()
    self.window = None

  def confirm_data (self, data) :
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists (self, data) :
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
        ##save property list frame object
        dict_residue_prop_objects[data_key] = list_obj
# Molprobity result viewer
class coot_molprobity_todo_list_gui (coot_extension_gui) :
  data_keys = [ "clusters","rama", "rota", "cbeta", "probe", "smoc", "fdr",
               "fsc","diffmap","cablam",
               "jpred"]
  data_titles = { "clusters"  : "Outlier residue clusters",
                  "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes",
                  "smoc"  : "Local density fit (SMOC)",
                  "fdr": "Backbone position score (FDR)",
                  "fsc": "Local density fit (FSC)",
                  "diffmap": "Model-map difference",
                  "cablam": "Ca geometry (CaBLAM)",
                  "jpred":"SS prediction"}
  data_names = { "clusters"  : ["Chain","Residue","Cluster","Outlier types"],
                 "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"],
                 "smoc" : ["Chain", "Residue", "Name", "Score"],
                 "fdr" : ["Chain", "Residue", "Name", "Score"],
                 "fsc" : ["Chain", "Residue", "Name", "Score"],
                 "diffmap" : ["Chain", "Residue", "Name", "Score"],
                 "cablam" : ["Chain", "Residue","Name","recommendation","DSSP"],
                 "jpred" : ["Chain", "Residue","Name","predicted SS","current SS"]}
  if (gobject is not None) :
    data_types = {  "clusters" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_INT, gobject.TYPE_STRING,
                             gobject.TYPE_PYOBJECT],
                    "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "smoc" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "fdr" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "fsc" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "diffmap" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cablam" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_STRING,
                             gobject.TYPE_STRING,gobject.TYPE_PYOBJECT],
                   "jpred" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_STRING,
                             gobject.TYPE_STRING,gobject.TYPE_PYOBJECT]}
  else :
    data_types = dict([ (s, []) for s in ["clusters","rama","rota","cbeta","probe","smoc",
                                          "fdr","fsc","diffmap","cablam","jpred"] ])

  def __init__ (self, data_file=None, data=None) :
    assert ([data, data_file].count(None) == 1)
    if (data is None) :
      data = load_pkl(data_file)
    if not self.confirm_data(data) :
      return
    coot_extension_gui.__init__(self, "Validation To-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets (self, data_key, box) :
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

  def toggle_probe_dots (self, *args) :
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots (self, *args) :
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui (coot_extension_gui) :
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list (object) :
  def __init__ (self, columns, column_types, rows, box,
      default_size=(380,200)) :
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)) :
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    ##adding a column type for checkbox (bool) before atom coordinate
    if gobject is not None:
        column_types = column_types[:-1]+[bool]+[column_types[-1]]
    
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns) :
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    ##add a cell for checkbox
    cell1 = gtk.CellRendererToggle()
    cell1.connect ("toggled", self.on_selected_toggled)
    column = gtk.TreeViewColumn('Dealt with',cell1,active=i+1)
    self.listctrl.append_column(column)
    #column.set_sort_column_id(i+1)
    #column.pack_start(cell1, True)
    
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      row = row[:-1] + (False,)+(row[-1],)
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

  def OnChange (self, treeview) :
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
  ##check box toggle
  def on_selected_toggled(self,renderer,path):
    if path is not None:
      model = self.listmodel.get_model()
      it = model.get_iter(path)
      #set toggle
      model[it][-2] = not model[it][-2]
      #set checkboxes for same residues in other lists
      try:
        chain = model[it][0]
        residue = model[it][1]
        for data_key in dict_residue_prop_objects:
          prop_obj = dict_residue_prop_objects[data_key]
          for row in prop_obj.listmodel.get_model():
            if data_key == 'probe':
              atom1_split = row[0].split()
              atom2_split = row[1].split()
              if atom1_split[0] == chain and atom1_split[1] == residue:
                row[-2] = model[it][-2]
              elif atom2_split[0] == chain and atom2_split[1] == residue:
                row[-2] = model[it][-2]
            elif row[0] == chain and row[1] == residue:
              row[-2] = model[it][-2]
      except IndexError: pass

  def check_chain_residue(self,chain,residue):
      pass
  
def show_probe_dots (show_dots, overlaps_only) :
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects) :
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects) :
      set_display_generic_object(object_number, 0)

def load_pkl (file_name) :
  pkl = open(file_name, "rb")
  data = cPickle.load(pkl)
  pkl.close()
  return data
data = {}
data['rama'] = []
data['rota'] = []
data['cbeta'] = []
data['fdr'] = []
data['fsc'] = []
data['diffmap'] = []
data['jpred'] = []
data['clusters'] = [('A', '305', 1, 'side-chain clash', (150.344, 132.728, 114.209)), ('A', '466', 1, 'side-chain clash', (145.763, 131.953, 114.86)), ('A', '468', 1, 'side-chain clash', (138.614, 138.973, 116.528)), ('A', '470', 1, 'side-chain clash\ncablam Outlier', (150.344, 132.728, 114.209)), ('A', '473', 1, 'side-chain clash', (148.489, 134.036, 118.448)), ('A', '698', 1, 'side-chain clash', (138.471, 135.966, 124.048)), ('A', '701', 1, 'smoc Outlier', (140.261, 140.416, 120.657)), ('A', '705', 1, 'side-chain clash', (138.614, 138.973, 116.528)), ('A', '731', 1, 'side-chain clash', (143.759, 136.977, 113.861)), ('A', '789', 1, 'side-chain clash', (138.471, 135.966, 124.048)), ('A', '356', 2, 'side-chain clash', (153.991, 111.973, 132.807)), ('A', '358', 2, 'side-chain clash', (164.074, 110.44, 132.23)), ('A', '373', 2, 'smoc Outlier', (154.83200000000002, 111.21400000000001, 143.40800000000002)), ('A', '530', 2, 'side-chain clash', (157.614, 114.097, 138.824)), ('A', '531', 2, 'side-chain clash', (156.38, 116.582, 138.879)), ('A', '533', 2, 'side-chain clash', (164.074, 110.44, 132.23)), ('A', '534', 2, 'side-chain clash', (157.729, 109.798, 133.352)), ('A', '535', 2, 'side-chain clash', (153.991, 111.973, 132.807)), ('A', '536', 2, 'side-chain clash', (157.614, 114.097, 138.824)), ('A', '567', 2, 'side-chain clash', (157.217, 119.223, 140.189)), ('A', '161', 3, 'smoc Outlier', (116.784, 135.546, 128.371)), ('A', '162', 3, 'side-chain clash', (116.863, 131.446, 126.295)), ('A', '164', 3, 'backbone clash\nsmoc Outlier', (120.323, 132.615, 129.482)), ('A', '166', 3, 'side-chain clash', (125.111, 129.4, 134.792)), ('A', '167', 3, 'backbone clash\nDihedral angle:CB:CG:CD:OE1\nsmoc Outlier', (120.029, 131.46200000000002, 132.197)), ('A', '168', 3, 'side-chain clash', (116.863, 131.446, 126.295)), ('A', '170', 3, 'side-chain clash', (115.008, 124.38, 123.816)), ('A', '171', 3, 'smoc Outlier', (119.765, 127.728, 123.68499999999999)), ('A', '173', 3, 'side-chain clash', (115.008, 124.38, 123.816)), ('A', '458', 3, 'side-chain clash', (125.111, 129.4, 134.792)), ('A', '119', 4, 'side-chain clash\ncablam Outlier\nsmoc Outlier', (119.794, 127.903, 99.673)), ('A', '120', 4, 'side-chain clash\nsmoc Outlier', (119.794, 127.903, 99.673)), ('A', '121', 4, 'cablam Outlier', (117.9, 133.6, 101.8)), ('A', '123', 4, 'side-chain clash\nbackbone clash', (127.984, 134.269, 102.002)), ('A', '125', 4, 'side-chain clash', (127.704, 133.207, 103.824)), ('A', '207', 4, 'smoc Outlier', (132.147, 132.42800000000003, 103.426)), ('A', '208', 4, 'side-chain clash', (127.984, 134.269, 102.002)), ('A', '210', 4, 'backbone clash', (126.829, 131.772, 101.615)), ('A', '211', 4, 'Dihedral angle:CA:CB:CG:OD1\nsmoc Outlier', (124.553, 128.85500000000002, 100.82199999999999)), ('A', '101', 5, 'side-chain clash', (126.87, 133.908, 83.889)), ('A', '114', 5, 'side-chain clash', (126.87, 133.908, 83.889)), ('A', '115', 5, 'smoc Outlier', (121.059, 133.49200000000002, 87.343)), ('A', '53', 5, 'smoc Outlier', (121.21300000000001, 141.22299999999998, 92.15299999999999)), ('A', '54', 5, 'side-chain clash', (117.928, 142.844, 87.052)), ('A', '72', 5, 'smoc Outlier', (120.35499999999999, 137.035, 89.154)), ('A', '74', 5, 'side-chain clash', (117.928, 142.844, 87.052)), ('A', '84', 5, 'smoc Outlier', (130.777, 131.125, 82.277)), ('A', '99', 5, 'cablam Outlier', (123.9, 129.1, 86.9)), ('A', '414', 6, 'side-chain clash', (131.596, 136.991, 165.801)), ('A', '416', 6, 'side-chain clash', (130.334, 141.227, 169.253)), ('A', '440', 6, 'smoc Outlier', (126.359, 139.303, 156.415)), ('A', '836', 6, 'side-chain clash\nDihedral angle:CD:NE:CZ:NH1', (130.953, 146.634, 154.042)), ('A', '839', 6, 'smoc Outlier', (129.20399999999998, 144.72899999999998, 158.478)), ('A', '840', 6, 'side-chain clash', (134.217, 143.676, 156.273)), ('A', '842', 6, 'smoc Outlier', (129.161, 144.167, 163.43)), ('A', '844', 6, 'side-chain clash', (131.596, 136.991, 165.801)), ('A', '850', 6, 'side-chain clash', (130.334, 141.227, 169.253)), ('A', '462', 7, 'side-chain clash', (132.91, 127.951, 125.144)), ('A', '625', 7, 'smoc Outlier', (133.311, 129.36200000000002, 132.05200000000002)), ('A', '627', 7, 'smoc Outlier', (137.626, 128.065, 127.96000000000001)), ('A', '631', 7, 'side-chain clash', (143.264, 125.892, 132.054)), ('A', '663', 7, 'side-chain clash', (143.264, 125.892, 132.054)), ('A', '677', 7, 'cablam Outlier', (136.3, 120.1, 133.0)), ('A', '678', 7, 'cablam CA Geom Outlier', (138.2, 123.4, 133.1)), ('A', '791', 7, 'side-chain clash', (132.91, 127.951, 125.144)), ('A', '837', 8, 'side-chain clash', (135.425, 151.868, 157.584)), ('A', '862', 8, 'smoc Outlier', (138.791, 149.001, 159.70499999999998)), ('A', '865', 8, 'smoc Outlier', (140.034, 151.344, 155.38800000000003)), ('A', '866', 8, 'side-chain clash', (135.425, 151.868, 157.584)), ('A', '876', 8, 'smoc Outlier', (126.519, 159.435, 157.07399999999998)), ('A', '880', 8, 'smoc Outlier', (131.02800000000002, 156.012, 159.79899999999998)), ('A', '601', 9, 'side-chain clash', (146.246, 154.573, 136.059)), ('A', '602', 9, 'smoc Outlier', (144.76399999999998, 156.485, 137.82500000000002)), ('A', '605', 9, 'side-chain clash', (146.246, 154.573, 136.059)), ('A', '606', 9, 'Dihedral angle:CA:C', (144.761, 158.459, 131.90200000000002)), ('A', '607', 9, 'Dihedral angle:N:CA\ncablam CA Geom Outlier', (148.14, 158.76999999999998, 130.23299999999998)), ('A', '608', 9, 'cablam Outlier', (147.6, 160.7, 127.0)), ('A', '29', 10, 'cablam Outlier', (119.7, 145.9, 97.2)), ('A', '31', 10, 'smoc Outlier', (119.69, 144.89800000000002, 103.485)), ('A', '32', 10, 'smoc Outlier', (123.221, 144.567, 104.834)), ('A', '35', 10, 'side-chain clash', (126.305, 141.79, 99.483)), ('A', '50', 10, 'side-chain clash', (126.305, 141.79, 99.483)), ('A', '180', 11, 'side-chain clash', (126.144, 115.01, 108.4)), ('A', '183', 11, 'side-chain clash\nsmoc Outlier', (126.144, 115.01, 108.4)), ('A', '258', 11, 'side-chain clash\ncablam Outlier\nsmoc Outlier', (124.677, 103.782, 110.089)), ('A', '260', 11, 'smoc Outlier', (124.17499999999998, 109.49900000000001, 110.478)), ('A', '263', 11, 'side-chain clash', (124.677, 103.782, 110.089)), ('A', '614', 12, 'side-chain clash', (134.837, 156.56, 132.823)), ('A', '615', 12, 'side-chain clash', (134.962, 152.948, 128.395)), ('A', '766', 12, 'side-chain clash', (134.962, 152.948, 128.395)), ('A', '802', 12, 'side-chain clash', (134.837, 156.56, 132.823)), ('A', '757', 13, 'smoc Outlier', (144.339, 145.131, 134.51399999999998)), ('A', '758', 13, 'side-chain clash\nbackbone clash', (143.093, 140.928, 139.256)), ('A', '759', 13, 'side-chain clash\nbackbone clash\ncablam Outlier\nsmoc Outlier', (143.093, 140.928, 139.256)), ('A', '760', 13, 'Dihedral angle:CA:CB:CG:OD1\nsmoc Outlier', (139.618, 139.64499999999998, 135.671)), ('A', '388', 14, 'side-chain clash', (132.587, 110.731, 144.671)), ('A', '397', 14, 'side-chain clash', (131.607, 110.356, 141.298)), ('A', '399', 14, 'smoc Outlier', (135.311, 107.019, 142.63299999999998)), ('A', '672', 14, 'side-chain clash', (132.587, 110.731, 144.671)), ('A', '57', 15, 'side-chain clash', (109.127, 132.802, 97.468)), ('A', '65', 15, 'side-chain clash\nsmoc Outlier', (109.127, 132.802, 97.468)), ('A', '66', 15, 'side-chain clash\nbackbone clash', (112.023, 127.714, 100.329)), ('A', '67', 15, 'backbone clash', (112.023, 127.714, 100.329)), ('A', '497', 16, 'smoc Outlier', (152.89600000000002, 130.678, 155.08)), ('A', '499', 16, 'side-chain clash', (155.198, 127.245, 160.585)), ('A', '513', 16, 'side-chain clash', (155.198, 127.245, 160.585)), ('A', '484', 17, 'smoc Outlier', (161.92200000000003, 139.186, 133.99)), ('A', '575', 17, 'side-chain clash', (158.291, 136.258, 132.426)), ('A', '641', 17, 'side-chain clash', (158.291, 136.258, 132.426)), ('A', '715', 18, 'side-chain clash', (138.332, 156.236, 104.487)), ('A', '717', 18, 'Dihedral angle:CA:CB:CG:OD1', (141.617, 158.546, 108.477)), ('A', '721', 18, 'side-chain clash', (138.332, 156.236, 104.487)), ('A', '268', 19, 'side-chain clash', (134.238, 107.045, 121.88)), ('A', '320', 19, 'smoc Outlier', (133.662, 112.785, 119.41900000000001)), ('A', '322', 19, 'side-chain clash', (134.238, 107.045, 121.88)), ('A', '914', 20, 'Dihedral angle:CD:NE:CZ:NH1', (147.354, 158.154, 168.255)), ('A', '920', 20, 'smoc Outlier', (147.375, 158.57899999999998, 161.698)), ('A', '924', 20, 'smoc Outlier', (148.23, 156.60999999999999, 155.724)), ('A', '312', 21, 'side-chain clash', (140.515, 122.721, 119.224)), ('A', '315', 21, 'side-chain clash', (140.515, 122.721, 119.224)), ('A', '464', 21, 'side-chain clash', (139.226, 127.256, 118.854)), ('A', '107', 22, 'cablam Outlier\nsmoc Outlier', (117.7, 148.9, 78.9)), ('A', '109', 22, 'side-chain clash\nDihedral angle:CA:C\ncablam Outlier', (120.70700000000001, 146.23499999999999, 74.383)), ('A', '110', 22, 'Dihedral angle:N:CA\ncablam Outlier', (121.35499999999999, 142.726, 75.66499999999999)), ('A', '519', 23, 'smoc Outlier', (163.05800000000002, 117.30499999999999, 151.46800000000002)), ('A', '520', 23, 'backbone clash', (168.432, 119.172, 149.902)), ('A', '521', 23, 'backbone clash', (168.432, 119.172, 149.902)), ('A', '846', 24, 'side-chain clash', (137.866, 134.148, 169.061)), ('A', '848', 24, 'side-chain clash', (137.866, 134.148, 169.061)), ('A', '899', 24, 'side-chain clash', (136.782, 132.891, 171.863)), ('A', '18', 25, 'backbone clash', (103.55, 126.526, 94.329)), ('A', '60', 25, 'side-chain clash\nbackbone clash', (103.55, 126.526, 94.329)), ('A', '62', 25, 'cablam Outlier\nsmoc Outlier', (99.5, 125.6, 97.4)), ('A', '501', 26, 'Bond length:CA:C', (148.026, 122.46600000000001, 154.35000000000002)), ('A', '502', 26, 'side-chain clash', (151.866, 119.428, 150.562)), ('A', '562', 26, 'side-chain clash', (151.866, 119.428, 150.562)), ('A', '10', 27, 'backbone clash\nside-chain clash\nDihedral angle:CD:NE:CZ:NH1', (113.482, 133.95600000000002, 81.287)), ('A', '12', 27, 'backbone clash\ncablam Outlier', (111.282, 129.774, 83.14)), ('A', '13', 27, 'backbone clash', (111.282, 129.774, 83.14)), ('A', '681', 28, 'Bond length:C', (142.065, 126.88499999999999, 140.35200000000003)), ('A', '682', 28, 'Bond length:C\nBond length:N', (141.56, 129.136, 143.561)), ('A', '683', 28, 'Bond length:N', (144.58700000000002, 127.62899999999999, 145.412)), ('A', '149', 29, 'side-chain clash', (120.033, 129.243, 107.325)), ('A', '212', 29, 'side-chain clash', (120.033, 129.243, 107.325)), ('A', '540', 30, 'side-chain clash', (143.466, 119.532, 141.037)), ('A', '665', 30, 'side-chain clash', (143.466, 119.532, 141.037)), ('A', '755', 31, 'side-chain clash', (141.325, 148.684, 128.812)), ('A', '764', 31, 'side-chain clash\nsmoc Outlier', (141.325, 148.684, 128.812)), ('A', '24', 32, 'side-chain clash\ncablam CA Geom Outlier', (110.25, 145.436, 88.751)), ('A', '25', 32, 'side-chain clash\nsmoc Outlier', (110.25, 145.436, 88.751)), ('A', '450', 33, 'smoc Outlier', (128.309, 119.781, 145.478)), ('A', '669', 33, 'smoc Outlier', (134.67399999999998, 117.333, 146.87)), ('A', '816', 34, 'side-chain clash', (138.268, 155.177, 146.011)), ('A', '830', 34, 'side-chain clash', (138.268, 155.177, 146.011)), ('A', '711', 35, 'side-chain clash', (131.332, 151.701, 106.062)), ('A', '714', 35, 'side-chain clash', (131.332, 151.701, 106.062)), ('A', '17', 36, 'side-chain clash', (110.39, 127.882, 91.727)), ('A', '58', 36, 'side-chain clash', (110.39, 127.882, 91.727)), ('A', '823', 37, 'cablam Outlier', (147.3, 170.0, 150.7)), ('A', '824', 37, 'cablam Outlier', (146.9, 172.3, 147.6)), ('A', '136', 38, 'side-chain clash', (122.191, 140.671, 125.647)), ('A', '793', 38, 'side-chain clash', (122.191, 140.671, 125.647)), ('A', '583', 39, 'backbone clash', (153.154, 147.175, 144.778)), ('A', '590', 39, 'backbone clash', (153.154, 147.175, 144.778)), ('A', '279', 40, 'side-chain clash', (140.843, 114.759, 121.558)), ('A', '318', 40, 'side-chain clash', (140.843, 114.759, 121.558)), ('A', '194', 41, 'smoc Outlier', (138.647, 118.754, 95.315)), ('A', '196', 41, 'smoc Outlier', (138.894, 123.05499999999999, 91.988)), ('A', '116', 42, 'side-chain clash\nsmoc Outlier', (145.189, 107.167, 148.383)), ('A', '98', 42, 'side-chain clash', (145.189, 107.167, 148.383)), ('A', '333', 43, 'side-chain clash', (156.47, 99.151, 135.844)), ('A', '361', 43, 'side-chain clash', (156.47, 99.151, 135.844)), ('A', '634', 44, 'side-chain clash', (122.814, 140.85, 171.967)), ('A', '693', 44, 'side-chain clash', (122.814, 140.85, 171.967)), ('A', '303', 45, 'side-chain clash', (156.172, 125.342, 117.568)), ('A', '306', 45, 'smoc Outlier', (152.10399999999998, 125.071, 116.82799999999999)), ('A', '239', 46, 'side-chain clash', (140.08, 128.727, 111.528)), ('A', '241', 46, 'smoc Outlier', (133.944, 129.375, 110.65899999999999)), ('A', '238', 47, 'side-chain clash', (146.217, 98.252, 139.271)), ('A', '242', 47, 'side-chain clash', (146.217, 98.252, 139.271)), ('A', '783', 48, 'smoc Outlier', (129.523, 141.51899999999998, 124.67599999999999)), ('A', '784', 48, 'smoc Outlier', (129.92700000000002, 139.89600000000002, 121.251)), ('A', '573', 49, 'side-chain clash', (158.175, 135.759, 142.145)), ('A', '577', 49, 'side-chain clash', (158.175, 135.759, 142.145)), ('A', '572', 50, 'side-chain clash', (142.466, 140.192, 175.009)), ('A', '576', 50, 'side-chain clash\nsmoc Outlier', (142.466, 140.192, 175.009)), ('A', '202', 51, 'side-chain clash', (145.899, 128.27, 93.923)), ('A', '231', 51, 'side-chain clash', (145.899, 128.27, 93.923)), ('A', '746', 52, 'side-chain clash', (152.365, 148.622, 124.592)), ('A', '750', 52, 'side-chain clash', (152.365, 148.622, 124.592)), ('A', '225', 53, 'side-chain clash', (148.094, 125.14, 85.505)), ('A', '226', 53, 'side-chain clash', (148.094, 125.14, 85.505)), ('A', '726', 54, 'side-chain clash', (150.713, 150.486, 109.803)), ('A', '744', 54, 'side-chain clash', (150.713, 150.486, 109.803)), ('A', '274', 55, 'cablam Outlier', (144.9, 106.6, 121.6)), ('A', '275', 55, 'cablam Outlier', (142.4, 107.9, 119.0)), ('A', '153', 56, 'backbone clash\nsmoc Outlier', (108.604, 130.381, 116.217)), ('A', '154', 56, 'backbone clash', (108.604, 130.381, 116.217)), ('A', '894', 57, 'smoc Outlier', (137.16899999999998, 150.258, 179.20899999999997)), ('A', '895', 57, 'smoc Outlier', (140.281, 148.13, 178.64899999999997)), ('A', '76', 58, 'backbone clash', (131.116, 142.994, 81.411)), ('A', '77', 58, 'backbone clash', (131.116, 142.994, 81.411)), ('A', '476', 59, 'smoc Outlier', (149.626, 140.05200000000002, 124.687)), ('A', '477', 59, 'Dihedral angle:CA:CB:CG:OD1\nsmoc Outlier', (153.268, 138.95600000000002, 124.637)), ('B', '130', 1, 'smoc Outlier', (124.77499999999999, 106.007, 144.33200000000002)), ('B', '132', 1, 'side-chain clash', (119.983, 104.865, 142.953)), ('B', '134', 1, 'smoc Outlier', (115.019, 113.20100000000001, 144.318)), ('B', '138', 1, 'side-chain clash', (116.637, 108.264, 144.215)), ('B', '142', 1, 'side-chain clash\nsmoc Outlier', (119.983, 104.865, 142.953)), ('B', '161', 2, 'Dihedral angle:CA:CB:CG:OD1', (119.87499999999999, 109.07799999999999, 154.134)), ('B', '180', 2, 'side-chain clash', (115.744, 109.153, 151.624)), ('B', '184', 2, 'side-chain clash', (115.744, 109.153, 151.624)), ('B', '103', 3, 'side-chain clash', (143.948, 97.797, 140.915)), ('B', '98', 3, 'side-chain clash\nsmoc Outlier', (143.948, 97.797, 140.915)), ('B', '99', 3, 'cablam Outlier', (145.3, 93.7, 143.7)), ('B', '154', 4, 'side-chain clash', (124.757, 97.292, 143.159)), ('B', '188', 4, 'side-chain clash', (124.757, 97.292, 143.159)), ('B', '111', 5, 'Dihedral angle:CD:NE:CZ:NH1', (147.627, 95.989, 123.924)), ('B', '112', 5, 'side-chain clash', (148.835, 98.309, 125.125)), ('B', '102', 6, 'side-chain clash', (140.147, 93.337, 135.429)), ('B', '106', 6, 'side-chain clash', (140.147, 93.337, 135.429)), ('B', '76', 7, 'smoc Outlier', (164.42200000000003, 117.479, 159.76999999999998)), ('B', '77', 7, 'Dihedral angle:CB:CG:CD:OE1', (165.883, 113.976, 160.005)), ('C', '1', 1, 'backbone clash', (114.076, 149.447, 161.336)), ('C', '2', 1, 'side-chain clash\nbackbone clash', (114.076, 149.447, 161.336)), ('C', '3', 1, 'side-chain clash', (112.587, 141.163, 156.483)), ('C', '44', 1, 'Dihedral angle:CA:CB:CG:OD1', (110.09100000000001, 144.74299999999997, 153.446)), ('C', '45', 1, 'cablam Outlier', (109.6, 144.3, 157.2)), ('C', '47', 1, 'Dihedral angle:CB:CG:CD:OE1', (107.542, 138.963, 155.38000000000002)), ('C', '48', 1, 'side-chain clash', (112.587, 141.163, 156.483)), ('C', '6', 1, 'side-chain clash', (113.312, 144.036, 162.552)), ('C', '10', 2, 'smoc Outlier', (117.785, 136.218, 162.89600000000002)), ('C', '13', 2, 'smoc Outlier', (118.54100000000001, 132.795, 166.267)), ('C', '30', 2, 'smoc Outlier', (118.007, 123.24000000000001, 155.42100000000002)), ('C', '33', 2, 'smoc Outlier', (119.187, 128.098, 156.631)), ('C', '34', 2, 'smoc Outlier', (116.616, 129.036, 153.98800000000003)), ('C', '36', 2, 'side-chain clash', (120.704, 131.335, 159.09)), ('C', '14', 3, 'side-chain clash', (105.508, 132.679, 165.074)), ('C', '32', 3, 'side-chain clash', (107.136, 130.814, 170.026)), ('C', '58', 3, 'side-chain clash', (107.136, 130.814, 170.026)), ('C', '70', 3, 'side-chain clash\nsmoc Outlier', (105.155, 132.699, 164.939)), ('C', '66', 4, 'side-chain clash', (115.558, 127.934, 182.129)), ('C', '69', 4, 'side-chain clash', (115.558, 127.934, 182.129)), ('C', '64', 5, 'cablam Outlier', (116.4, 122.0, 175.1)), ('D', '101', 1, 'Dihedral angle:CA:CB:CG:OD1', (102.44400000000002, 140.88800000000003, 168.35200000000003)), ('D', '105', 1, 'side-chain clash', (100.025, 132.994, 168.236)), ('D', '106', 1, 'side-chain clash\nsmoc Outlier', (105.508, 132.679, 165.074)), ('D', '120', 1, 'side-chain clash', (103.373, 128.837, 166.269)), ('D', '125', 1, 'smoc Outlier', (96.87299999999999, 126.117, 152.751)), ('D', '132', 1, 'side-chain clash\nsmoc Outlier', (93.229, 123.789, 174.789)), ('D', '135', 1, 'side-chain clash', (86.066, 123.91, 180.375)), ('D', '136', 1, 'side-chain clash', (92.91, 130.275, 178.233)), ('D', '138', 1, 'side-chain clash', (93.229, 123.789, 174.789)), ('D', '139', 1, 'smoc Outlier', (89.438, 128.23499999999999, 176.71599999999998)), ('D', '140', 1, 'side-chain clash', (92.91, 130.275, 178.233)), ('D', '142', 1, 'side-chain clash', (89.99, 125.842, 168.208)), ('D', '143', 1, 'smoc Outlier', (86.576, 129.596, 170.541)), ('D', '147', 1, 'side-chain clash', (93.655, 127.669, 164.052)), ('D', '149', 1, 'side-chain clash', (103.373, 128.837, 166.269)), ('D', '150', 1, 'side-chain clash', (100.025, 132.994, 168.236)), ('D', '151', 1, 'side-chain clash', (98.347, 138.014, 163.633)), ('D', '152', 1, 'smoc Outlier', (96.63799999999999, 134.41299999999998, 162.69)), ('D', '154', 1, 'side-chain clash', (93.655, 127.669, 164.052)), ('D', '155', 1, 'side-chain clash', (91.118, 123.413, 160.323)), ('D', '156', 1, 'side-chain clash', (89.99, 125.842, 168.208)), ('D', '157', 1, 'side-chain clash', (91.118, 123.413, 160.323)), ('D', '159', 1, 'side-chain clash', (93.165, 119.136, 170.334)), ('D', '161', 1, 'Dihedral angle:CA:CB:CG:OD1', (94.508, 113.157, 173.153)), ('D', '162', 1, 'side-chain clash', (97.417, 114.055, 176.593)), ('D', '163', 1, 'smoc Outlier', (96.693, 108.307, 173.771)), ('D', '173', 1, 'side-chain clash', (86.233, 120.967, 179.747)), ('D', '174', 1, 'side-chain clash', (86.066, 123.91, 180.375)), ('D', '176', 1, 'smoc Outlier', (83.889, 117.412, 181.47)), ('D', '177', 1, 'side-chain clash', (86.233, 120.967, 179.747)), ('D', '178', 1, 'cablam Outlier', (89.4, 117.1, 184.1)), ('D', '181', 1, 'side-chain clash\ncablam Outlier', (96.934, 114.938, 179.025)), ('D', '182', 1, 'Dihedral angle:CA:C', (95.253, 116.94400000000002, 178.577)), ('D', '183', 1, 'side-chain clash\nDihedral angle:N:CA\ncablam CA Geom Outlier', (98.225, 117.069, 176.286)), ('D', '184', 1, 'smoc Outlier', (95.595, 117.718, 173.58700000000002)), ('D', '186', 1, 'side-chain clash', (93.165, 119.136, 170.334)), ('D', '190', 1, 'Dihedral angle:CD:NE:CZ:NH1', (95.374, 129.12800000000001, 158.73)), ('D', '109', 2, 'side-chain clash', (100.712, 130.522, 175.444)), ('D', '112', 2, 'Dihedral angle:CA:CB:CG:OD1', (102.856, 128.71899999999997, 179.33800000000002)), ('D', '113', 2, 'side-chain clash\nsmoc Outlier', (103.878, 124.338, 174.872)), ('D', '114', 2, 'side-chain clash\nbackbone clash\nsmoc Outlier', (100.515, 124.333, 173.71)), ('D', '115', 2, 'side-chain clash', (103.878, 124.338, 174.872)), ('D', '131', 2, 'backbone clash\nsmoc Outlier', (100.515, 124.333, 173.71)), ('D', '133', 2, 'side-chain clash', (101.771, 124.448, 177.92)), ('D', '83', 3, 'side-chain clash\nBond angle:C', (128.85800000000003, 130.95600000000002, 175.415)), ('D', '84', 3, 'side-chain clash\nBond angle:N:CA\ncablam Outlier\nsmoc Outlier', (125.604, 128.984, 174.736)), ('D', '87', 3, 'smoc Outlier', (123.779, 133.93, 173.46200000000002)), ('D', '91', 3, 'smoc Outlier', (118.561, 136.472, 171.85100000000003)), ('D', '94', 3, 'smoc Outlier', (116.68299999999999, 141.48700000000002, 171.541)), ('D', '95', 3, 'smoc Outlier', (113.479, 139.52200000000002, 170.903)), ('D', '122', 4, 'side-chain clash', (137.75, 128.918, 169.42)), ('D', '80', 4, 'side-chain clash', (136.782, 132.891, 171.863)), ('D', '90', 4, 'side-chain clash', (137.638, 128.684, 169.154)), ('D', '64', 5, 'side-chain clash', (150.362, 144.097, 179.465)), ('D', '68', 5, 'side-chain clash', (150.362, 144.097, 179.465)), ('D', '168', 6, 'smoc Outlier', (85.49700000000001, 115.897, 169.696)), ('D', '171', 6, 'Dihedral angle:CB:CG:CD:OE1', (83.227, 117.296, 174.415)), ('D', '55', 7, 'smoc Outlier', (167.138, 147.918, 181.70899999999997)), ('D', '57', 7, 'Dihedral angle:CD:NE:CZ:NH1\nsmoc Outlier', (162.24399999999997, 150.32000000000002, 181.68800000000002)), ('D', '72', 8, 'side-chain clash', (142.466, 140.192, 175.009)), ('F', '-1', 1, 'Bond length:P', (148.646, 145.107, 150.08700000000002)), ('F', '-2', 1, "Bond angle:O2':C2':C1'\nBond angle:C3':C2':O2'\nBond angle:C4':C3':O3'\nBond angle:O3':C3':C2'\nBond length:O3'\nBond length:P", (148.80800000000002, 141.029, 146.841)), ('F', '-3', 1, "Bond length:P\nBond length:O3'", (148.20399999999998, 135.786, 145.641)), ('F', '-4', 1, "Bond length:O3'", (146.315, 130.86700000000002, 147.191)), ('F', '-17', 2, 'smoc Outlier', (135.76399999999998, 122.886, 166.309)), ('F', '-18', 2, 'side-chain clash', (137.638, 128.684, 169.154)), ('F', '0', 3, 'side-chain clash', (150.234, 147.452, 157.608)), ('F', '1', 3, 'side-chain clash', (150.234, 147.452, 157.608)), ('F', '3', 4, 'side-chain clash', (156.801, 142.584, 169.461)), ('F', '4', 4, 'side-chain clash', (156.801, 142.584, 169.461)), ('F', '5', 5, 'side-chain clash', (166.905, 142.104, 166.022)), ('F', '6', 5, 'side-chain clash\nBackbone torsion suites: ', (168.32600000000002, 141.45200000000003, 163.811)), ('F', '-20', 6, 'smoc Outlier', (150.126, 127.974, 168.82000000000002)), ('G', '1', 1, 'side-chain clash', (141.533, 143.352, 155.425)), ('G', '2', 1, 'side-chain clash', (141.533, 143.352, 155.425)), ('G', '-4', 2, 'Backbone torsion suites: ', (162.376, 137.51, 159.405)), ('G', '-5', 2, 'side-chain clash', (164.476, 140.992, 160.664)), ('G', '0', 3, 'smoc Outlier', (144.94, 141.266, 162.526)), ('G', '4', 3, 'side-chain clash', (142.295, 138.054, 144.23))]
data['probe'] = [(' A 312  ASN HD21', ' A 464  CYS  H  ', -0.798, (139.226, 127.256, 118.854)), (' D 147  PHE  HB3', ' D 154  TRP  HB2', -0.772, (93.655, 127.669, 164.052)), (' A 758  LEU HD23', ' A 759  SER  H  ', -0.764, (143.043, 141.338, 139.64)), (' D 162  ALA  HB2', ' D 183  PRO  HD2', -0.762, (97.417, 114.055, 176.593)), (' A 170  ASP  OD2', ' A 173  ARG  NH2', -0.692, (115.008, 124.38, 123.816)), (' A  60  ASP  HB3', ' A  66  ILE HD11', -0.652, (107.734, 124.474, 96.483)), (' A 279  ARG  NH2', ' A 318  SER  OG ', -0.647, (140.843, 114.759, 121.558)), (' A  12  CYS  SG ', ' A  13  GLY  N  ', -0.636, (111.282, 129.774, 83.14)), (' A 576  LEU HD11', ' A 686  THR HG22', -0.622, (152.46, 131.893, 139.104)), (' A 358  ASP  H  ', ' A 534  ASN HD21', -0.616, (159.331, 109.788, 133.262)), (' A 242  MET  HE1', ' A 466  ILE HG22', -0.608, (141.942, 128.238, 112.994)), (' A 416  ASN  HA ', ' A 850  THR HG23', -0.605, (130.334, 141.227, 169.253)), (' A  24  THR HG22', ' A  25  GLY  H  ', -0.6, (110.25, 145.436, 88.751)), (' D 136  ASN  O  ', ' D 140  ASN  ND2', -0.599, (92.91, 130.275, 178.233)), (' A 239  SER  HA ', ' A 242  MET  HE2', -0.589, (140.08, 128.727, 111.528)), (' A 614  LEU  HB2', ' A 802  GLU  HB3', -0.588, (134.837, 156.56, 132.823)), (' A  54  CYS  SG ', ' A  74  ARG  NH2', -0.587, (117.928, 142.844, 87.052)), (' F   5    G  N2 ', ' G  -5    C  O2 ', -0.587, (164.476, 140.992, 160.664)), (' A 225  THR HG22', ' A 226  THR  H  ', -0.587, (148.094, 125.14, 85.505)), (' A 746  TYR  CZ ', ' A 750  ARG  HD2', -0.578, (152.365, 148.622, 124.592)), (' A 755  MET  HG2', ' A 764  VAL HG22', -0.577, (141.325, 148.684, 128.812)), (' A 180  GLU  OE2', ' A 183  ARG  NH1', -0.571, (126.144, 115.01, 108.4)), (' A 116  ARG  HG3', ' A 119  LEU HD11', -0.571, (122.876, 131.936, 93.786)), (' A  57  GLN  HG2', ' A  65  LEU HD12', -0.57, (109.127, 132.802, 97.468)), (' A 540  THR HG23', ' A 665  GLU  HG3', -0.568, (143.466, 119.532, 141.037)), (' A 119  LEU  O  ', ' A 120  THR HG23', -0.568, (119.794, 127.903, 99.673)), (" F   5    G  H2'", ' F   6    U  C6 ', -0.568, (166.142, 142.123, 165.724)), (' D  83  VAL  O  ', ' D  84  THR HG22', -0.567, (127.163, 128.494, 176.372)), (' A  10  ARG  NH2', ' A  10  ARG  O  ', -0.564, (115.967, 132.209, 81.324)), (' B 180  LEU HD13', ' B 184  LEU HD21', -0.563, (115.744, 109.153, 151.624)), (' A 258  ASP  HB2', ' A 263  LYS  HD2', -0.557, (124.677, 103.782, 110.089)), (' A 726  ARG  NH1', ' A 744  GLU  OE2', -0.553, (150.713, 150.486, 109.803)), (' D 132  ILE HG21', ' D 138  TYR  HB2', -0.55, (93.229, 123.789, 174.789)), (' A 601  MET  O  ', ' A 605  VAL HG23', -0.54, (146.246, 154.573, 136.059)), (' A 356  ASN  ND2', ' A 535  VAL  H  ', -0.539, (154.569, 112.488, 132.661)), (' A 109  ASP  N  ', ' A 109  ASP  OD1', -0.538, (120.356, 147.92, 75.101)), (' A  18  ARG  NH1', ' A  60  ASP  O  ', -0.537, (103.55, 126.526, 94.329)), (' D 142  CYS  SG ', ' D 156  ILE HD11', -0.532, (89.99, 125.842, 168.208)), (' A 470  LEU  HA ', ' A 473  VAL HG12', -0.527, (148.489, 134.036, 118.448)), (' A 573  GLN  O  ', ' A 577  LYS  HG2', -0.527, (158.175, 135.759, 142.145)), (' A 356  ASN  HB3', ' A 534  ASN HD22', -0.525, (157.729, 109.798, 133.352)), (' A 388  LEU HD23', ' A 397  SER  HB2', -0.523, (131.607, 110.356, 141.298)), (' D 135  TYR  CZ ', ' D 174  MET  HA ', -0.522, (86.066, 123.91, 180.375)), (" G   1    A  H2'", ' G   2    G  H8 ', -0.517, (141.082, 143.488, 155.867)), (' A 468  GLN  HA ', ' A 731  LEU HD22', -0.516, (143.759, 136.977, 113.861)), (' A 631  ARG  HG2', ' A 663  LEU HD13', -0.513, (143.264, 125.892, 132.054)), (' B 112  ASP  N  ', ' B 112  ASP  OD1', -0.511, (148.835, 98.309, 125.125)), (' A 466  ILE  O  ', ' A 470  LEU  HG ', -0.507, (145.763, 131.953, 114.86)), (' A 238  TYR  O  ', ' A 242  MET  HG3', -0.507, (137.768, 127.597, 110.918)), (' A 341  VAL HG21', ' B 103  LEU HD21', -0.506, (146.217, 98.252, 139.271)), (' D 109  ASN  HB3', ' D 114  CYS  HB2', -0.506, (100.966, 128.823, 173.179)), (' A 468  GLN  NE2', ' A 705  ASN  OD1', -0.504, (138.614, 138.973, 116.528)), (' C  66  VAL HG11', ' C  69  ASN HD22', -0.499, (115.558, 127.934, 182.129)), (' D 122  LEU  H  ', ' D 122  LEU HD23', -0.497, (105.142, 129.803, 155.548)), (' A 388  LEU HD22', ' A 672  SER  HB3', -0.493, (132.587, 110.731, 144.671)), (' A 575  LEU HD13', ' A 641  LYS  HG3', -0.491, (158.291, 136.258, 132.426)), (' D  80  ARG  NH1', " F -18    A  H4'", -0.49, (137.75, 128.918, 169.42)), (" F   5    G  H2'", ' F   6    U  H6 ', -0.488, (166.905, 142.104, 166.022)), (' C  14  LEU HD22', ' C  36  HIS  CG ', -0.484, (120.704, 131.335, 159.09)), (' D 105  ASN HD22', ' D 150  ALA  H  ', -0.483, (100.449, 133.233, 168.028)), (' D 155  GLU  O  ', ' D 157  GLN  NE2', -0.482, (91.118, 123.413, 160.323)), (' A 758  LEU HD23', ' A 759  SER  N  ', -0.481, (143.093, 140.928, 139.256)), (' A  76  THR  OG1', ' A  77  PHE  N  ', -0.478, (131.116, 142.994, 81.411)), (' A 356  ASN HD21', ' A 535  VAL  H  ', -0.476, (153.991, 111.973, 132.807)), (' A 698  GLN  NE2', ' A 789  GLN  OE1', -0.475, (138.471, 135.966, 124.048)), (' B 132  ILE HG21', ' B 138  TYR  HB2', -0.475, (116.637, 108.264, 144.215)), (' A 123  THR HG22', ' A 125  ALA  H  ', -0.475, (127.704, 133.207, 103.824)), (' A 615  MET  HB2', ' A 766  PHE  HE1', -0.474, (134.962, 152.948, 128.395)), (' D 151  SER  O  ', ' D 151  SER  OG ', -0.472, (98.347, 138.014, 163.633)), (' A 502  ALA  HB1', ' A 562  ILE  HB ', -0.47, (151.866, 119.428, 150.562)), (' A 462  THR  OG1', ' A 791  ASN  ND2', -0.47, (132.91, 127.951, 125.144)), (' A 499  ASP  OD2', ' A 513  ARG  NH1', -0.468, (155.198, 127.245, 160.585)), (' B  98  LEU HD11', ' B 103  LEU HD22', -0.467, (143.948, 97.797, 140.915)), (" F   4    C  H2'", ' F   4    C  O2 ', -0.466, (159.584, 140.735, 168.071)), (" F   0    G  H2'", ' F   1    U  H6 ', -0.465, (150.38, 147.768, 157.209)), (' D 114  CYS  HA ', ' D 131  VAL  O  ', -0.465, (100.515, 124.333, 173.71)), (' A  17  ALA  HB1', ' A  58  GLU  HG3', -0.463, (110.39, 127.882, 91.727)), (' A 711  ASP  HB3', ' A 714  LYS  HD2', -0.462, (131.332, 151.701, 106.062)), (' F   4    C  C6 ', " F   4    C H5''", -0.462, (158.571, 144.421, 168.523)), (' A 531  THR HG21', ' A 567  THR HG21', -0.461, (157.217, 119.223, 140.189)), (' A 136  GLU  HG2', ' A 793  PHE  HZ ', -0.46, (121.833, 141.078, 125.539)), (' A 520  SER  OG ', ' A 521  TYR  N  ', -0.459, (168.432, 119.172, 149.902)), (' C  32  CYS  SG ', ' C  58  VAL HG11', -0.458, (115.0, 125.481, 162.303)), (' A 123  THR HG23', ' A 210  GLN  O  ', -0.458, (126.829, 131.772, 101.615)), (' A 312  ASN  O  ', ' A 315  VAL HG12', -0.457, (140.515, 122.721, 119.224)), (' D  64  ASP  O  ', ' D  68  THR HG23', -0.456, (150.362, 144.097, 179.465)), (' A 358  ASP  OD1', ' A 533  ARG  NH1', -0.454, (164.074, 110.44, 132.23)), (' A 572  HIS  O  ', ' A 576  LEU  HG ', -0.453, (155.543, 133.333, 138.997)), (' D 113  GLY  HA3', ' D 133  PRO  HG2', -0.453, (101.771, 124.448, 177.92)), (' A 854  LEU HD22', ' D  72  LYS  HG2', -0.452, (142.466, 140.192, 175.009)), (' A 583  ARG  NH2', ' A 590  GLY  O  ', -0.45, (153.154, 147.175, 144.778)), (' A 268  TRP  CD1', ' A 322  PRO  HD3', -0.45, (134.238, 107.045, 121.88)), (' A 634  ALA  HA ', ' A 693  VAL HG11', -0.449, (147.954, 134.202, 128.916)), (' B 154  TRP  HB3', ' B 188  ALA  HB1', -0.448, (124.757, 97.292, 143.159)), (' A 417  LYS  HD2', ' D  90  MET  HG3', -0.447, (122.814, 140.85, 171.967)), (' A 836  ARG  NH2', ' A 840  ALA  HB2', -0.446, (134.217, 143.676, 156.273)), (' D  80  ARG HH12', " F -18    A  H4'", -0.446, (137.638, 128.684, 169.154)), (" G   1    A  H2'", ' G   2    G  C8 ', -0.445, (141.533, 143.352, 155.425)), (' C  60  LEU HD12', ' D 106  ILE HG22', -0.445, (107.136, 130.814, 170.026)), (' D 173  SER  O  ', ' D 177  SER  OG ', -0.443, (86.233, 120.967, 179.747)), (' A 208  ASP  N  ', ' A 208  ASP  OD1', -0.442, (131.721, 135.201, 101.191)), (' A 715  ILE  O  ', ' A 721  ARG  NH2', -0.441, (138.332, 156.236, 104.487)), (' C  70  LYS  HA ', ' C  70  LYS  HD3', -0.441, (116.433, 133.688, 180.078)), (' A 899  MET  HE3', ' A 906  MET  SD ', -0.439, (147.509, 145.303, 182.03)), (' A 848  VAL HG13', ' D  80  ARG  HE ', -0.439, (136.782, 132.891, 171.863)), (' A  66  ILE HG22', ' A  67  ASP  N  ', -0.438, (112.023, 127.714, 100.329)), (' G   4  F86  C8 ', ' G   4  F86  N2 ', -0.438, (142.295, 138.054, 144.23)), (' A 101  PHE  CD2', ' A 114  ILE HG12', -0.437, (126.87, 133.908, 83.889)), (' B 102  ALA  O  ', ' B 106  ILE HG23', -0.434, (140.147, 93.337, 135.429)), (' D 105  ASN  ND2', ' D 150  ALA  H  ', -0.434, (100.025, 132.994, 168.236)), (' A 303  ASP  N  ', ' A 303  ASP  OD1', -0.433, (156.172, 125.342, 117.568)), (' A 333  ILE HD13', ' A 361  LEU  HG ', -0.432, (156.47, 99.151, 135.844)), (' D 120  ILE HD11', ' D 149  TYR  HE2', -0.432, (103.373, 128.837, 166.269)), (' A 164  ASP  HB3', ' A 167  GLU  O  ', -0.431, (120.323, 132.615, 129.482)), (' A 531  THR HG22', ' A 536  ILE HD12', -0.43, (156.38, 116.582, 138.879)), (' D 159  VAL HG13', ' D 186  VAL HG12', -0.43, (93.165, 119.136, 170.334)), (' A 123  THR HG21', ' A 208  ASP  HA ', -0.429, (127.984, 134.269, 102.002)), (' A 153  ASP  OD1', ' A 154  ASP  N  ', -0.428, (108.604, 130.381, 116.217)), (' D 113  GLY  O  ', ' D 115  VAL HG23', -0.427, (103.878, 124.338, 174.872)), (' C  53  VAL HG13', ' D 106  ILE HD11', -0.424, (105.155, 132.699, 164.939)), (' D 109  ASN  HA ', ' D 109  ASN HD22', -0.422, (100.712, 130.522, 175.444)), (" F   3    U  H2'", " F   4    C  O4'", -0.422, (156.801, 142.584, 169.461)), (' A 305  ARG  NH2', ' A 470  LEU HD13', -0.421, (150.344, 132.728, 114.209)), (' C   2  LYS  O  ', ' C   6  VAL HG13', -0.421, (113.312, 144.036, 162.552)), (" F   0    G  H2'", ' F   1    U  C6 ', -0.42, (150.234, 147.452, 157.608)), (' A 906  MET  HB3', ' A 906  MET  HE2', -0.419, (148.759, 148.914, 182.292)), (' A  35  PHE  HZ ', ' A  50  LYS  HB2', -0.418, (126.035, 141.981, 99.191)), (' B 139  LYS  HB3', ' B 139  LYS  HE2', -0.418, (110.711, 107.874, 139.685)), (' A  10  ARG  HA ', ' A  10  ARG  HD2', -0.417, (113.953, 132.759, 79.686)), (' A  91  LYS  HB3', ' A  91  LYS  HE2', -0.416, (130.191, 121.95, 83.236)), (' A 166  VAL HG13', ' A 458  TYR  CZ ', -0.416, (125.111, 129.4, 134.792)), (' A 136  GLU  HG2', ' A 793  PHE  CZ ', -0.413, (122.191, 140.671, 125.647)), (' A 837  ILE HG21', ' A 866  ALA  HB2', -0.412, (135.425, 151.868, 157.584)), (' B 132  ILE HD11', ' B 142  CYS  SG ', -0.412, (119.983, 104.865, 142.953)), (' A  35  PHE  CZ ', ' A  50  LYS  HB2', -0.411, (126.305, 141.79, 99.483)), (' A 846  ASP  OD1', ' A 848  VAL HG22', -0.41, (137.866, 134.148, 169.061)), (' A 162  TRP  HA ', ' A 168  ASN HD22', -0.409, (116.863, 131.446, 126.295)), (' C   3  MET  HE1', ' C  48  ALA  HB2', -0.409, (112.587, 141.163, 156.483)), (' A 202  VAL HG13', ' A 231  VAL HG13', -0.408, (145.899, 128.27, 93.923)), (' D 181  ALA  C  ', ' D 183  PRO  HD3', -0.408, (96.934, 114.938, 179.025)), (' A 445  ASP  N  ', ' A 445  ASP  OD1', -0.408, (123.2, 124.522, 152.879)), (' C  14  LEU  HA ', ' C  14  LEU HD12', -0.407, (119.611, 129.363, 163.448)), (' A 816  HIS  O  ', ' A 830  PRO  HA ', -0.406, (138.268, 155.177, 146.011)), (' A 414  ASN  HB2', ' A 844  VAL HG23', -0.406, (131.596, 136.991, 165.801)), (' A  98  LYS  O  ', ' A 116  ARG  HA ', -0.405, (122.856, 129.222, 89.3)), (' A 381  HIS  ND1', ' B  94  MET  HE1', -0.405, (145.189, 107.167, 148.383)), (' C  53  VAL HG13', ' D 106  ILE  CD1', -0.403, (105.508, 132.679, 165.074)), (' A 149  TYR  HE2', ' A 212  LEU HD13', -0.402, (120.033, 129.243, 107.325)), (' C   1  SER  OG ', ' C   2  LYS  N  ', -0.401, (114.076, 149.447, 161.336)), (' A 530  TYR  CD1', ' A 536  ILE HD11', -0.401, (157.614, 114.097, 138.824))]
data['omega'] = [('A', ' 505 ', 'PRO', None, (147.01999999999998, 113.64600000000002, 149.449)), ('B', ' 183 ', 'PRO', None, (119.939, 113.85400000000001, 150.132)), ('D', ' 183 ', 'PRO', None, (97.372, 116.503, 177.338))]
data['cablam'] = [('A', '12', 'CYS', 'check CA trace,carbonyls, peptide', 'helix\nHHHTT', (112.7, 130.5, 85.4)), ('A', '29', 'ASP', 'check CA trace,carbonyls, peptide', ' \n----S', (119.7, 145.9, 97.2)), ('A', '62', 'ASP', 'check CA trace,carbonyls, peptide', 'helix-3\n-GGG-', (99.5, 125.6, 97.4)), ('A', '99', 'HIS', ' beta sheet', ' \n----E', (123.9, 129.1, 86.9)), ('A', '107', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\n-SSSS', (117.7, 148.9, 78.9)), ('A', '109', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\nSSS-E', (120.7, 146.2, 74.4)), ('A', '110', 'MET', ' beta sheet', ' \nSS-EE', (121.4, 142.7, 75.7)), ('A', '119', 'LEU', 'check CA trace,carbonyls, peptide', ' \n-S--S', (120.1, 129.1, 96.8)), ('A', '121', 'LYS', 'check CA trace,carbonyls, peptide', 'bend\n--SSB', (117.9, 133.6, 101.8)), ('A', '139', 'CYS', 'check CA trace,carbonyls, peptide', ' \nTS-HH', (119.5, 139.8, 116.3)), ('A', '218', 'ASP', 'check CA trace,carbonyls, peptide', ' \nB---S', (130.7, 133.7, 92.4)), ('A', '258', 'ASP', 'check CA trace,carbonyls, peptide', 'turn\nBTTSS', (127.4, 105.2, 110.0)), ('A', '274', 'ASP', 'check CA trace,carbonyls, peptide', ' \n----H', (144.9, 106.6, 121.6)), ('A', '275', 'PHE', 'check CA trace,carbonyls, peptide', ' \n---HH', (142.4, 107.9, 119.0)), ('A', '470', 'LEU', ' alpha helix', 'helix\nHHHHH', (147.8, 133.4, 117.3)), ('A', '504', 'PHE', 'check CA trace,carbonyls, peptide', 'beta bridge\n--BTG', (145.5, 115.6, 149.6)), ('A', '509', 'TRP', 'check CA trace,carbonyls, peptide', 'turn\nGGT--', (150.8, 113.7, 158.1)), ('A', '608', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\nTSS-S', (147.6, 160.7, 127.0)), ('A', '677', 'PRO', 'check CA trace,carbonyls, peptide', ' \nE--S-', (136.3, 120.1, 133.0)), ('A', '733', 'ARG', ' alpha helix', 'bend\nHHS--', (147.2, 136.1, 105.1)), ('A', '759', 'SER', 'check CA trace,carbonyls, peptide', 'turn\nEETTE', (142.7, 139.4, 137.9)), ('A', '823', 'GLY', 'check CA trace,carbonyls, peptide', 'bend\nE-SSS', (147.3, 170.0, 150.7)), ('A', '824', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\n-SSSE', (146.9, 172.3, 147.6)), ('A', '904', 'SER', 'check CA trace,carbonyls, peptide', 'bend\nHSS--', (146.7, 146.1, 190.8)), ('A', '24', 'THR', 'check CA trace', ' \nSS-SS', (111.1, 144.3, 91.1)), ('A', '151', 'CYS', 'check CA trace', 'bend\nTTS--', (115.5, 124.8, 115.2)), ('A', '326', 'PHE', 'check CA trace', ' \nTS-EE', (140.8, 110.9, 129.0)), ('A', '607', 'SER', 'check CA trace', 'bend\nHTSS-', (148.1, 158.8, 130.2)), ('A', '678', 'GLY', 'check CA trace', 'bend\n--S--', (138.2, 123.4, 133.1)), ('B', '99', 'ASP', 'check CA trace,carbonyls, peptide', ' \nTT-SH', (145.3, 93.7, 143.7)), ('B', '151', 'SER', 'check CA trace,carbonyls, peptide', 'bend\n-SSSE', (127.1, 96.9, 132.2)), ('C', '45', 'THR', 'check CA trace,carbonyls, peptide', 'turn\n-STTH', (109.6, 144.3, 157.2)), ('C', '64', 'GLY', 'check CA trace,carbonyls, peptide', 'bend\nSSSS-', (116.4, 122.0, 175.1)), ('D', '84', 'THR', ' alpha helix', 'turn\nHTTTH', (125.6, 129.0, 174.7)), ('D', '178', 'PRO', ' three-ten', 'turn\nT-TTS', (89.4, 117.1, 184.1)), ('D', '181', 'ALA', 'check CA trace,carbonyls, peptide', ' \nTS---', (95.1, 113.5, 180.3)), ('D', '183', 'PRO', 'check CA trace', ' \n---EE', (98.2, 117.1, 176.3))]
data['smoc'] = [('A', 25, u'GLY', 0.7148443596071318, (112.55, 143.942, 87.621)), ('A', 31, u'VAL', 0.6523296684254148, (119.69, 144.89800000000002, 103.485)), ('A', 32, u'TYR', 0.6935341249811451, (123.221, 144.567, 104.834)), ('A', 53, u'CYS', 0.6826092209126623, (121.21300000000001, 141.22299999999998, 92.15299999999999)), ('A', 62, u'ASP', 0.7671657504053128, (99.485, 125.648, 97.43400000000001)), ('A', 65, u'LEU', 0.787880284541712, (106.7, 130.642, 99.74700000000001)), ('A', 72, u'VAL', 0.7338669238190766, (120.35499999999999, 137.035, 89.154)), ('A', 84, u'GLU', 0.7460839922789387, (130.777, 131.125, 82.277)), ('A', 107, u'ASP', 0.768585873081457, (117.7, 148.889, 78.87899999999999)), ('A', 115, u'SER', 0.7313016761116049, (121.059, 133.49200000000002, 87.343)), ('A', 116, u'ARG', 0.7161919085432817, (122.04400000000001, 131.025, 90.05199999999999)), ('A', 119, u'LEU', 0.7093953131511105, (120.139, 129.075, 96.818)), ('A', 120, u'THR', 0.65812619150168, (118.74600000000001, 130.304, 100.18799999999999)), ('A', 153, u'ASP', 0.7546405186729435, (109.837, 128.88800000000003, 116.842)), ('A', 161, u'ASP', 0.757985572897323, (116.784, 135.546, 128.371)), ('A', 164, u'ASP', 0.7494483279757325, (121.583, 133.694, 127.609)), ('A', 167, u'GLU', 0.7673807073241882, (120.029, 131.46200000000002, 132.197)), ('A', 171, u'ILE', 0.7412790486442871, (119.765, 127.728, 123.68499999999999)), ('A', 183, u'ARG', 0.7392246651208815, (128.631, 119.758, 108.76400000000001)), ('A', 194, u'ASP', 0.7328512882901248, (138.647, 118.754, 95.315)), ('A', 196, u'MET', 0.7446250503353872, (138.894, 123.05499999999999, 91.988)), ('A', 207, u'LEU', 0.6935914695692386, (132.147, 132.42800000000003, 103.426)), ('A', 211, u'ASP', 0.6117211373993369, (124.553, 128.85500000000002, 100.82199999999999)), ('A', 241, u'LEU', 0.6834133299231279, (133.944, 129.375, 110.65899999999999)), ('A', 258, u'ASP', 0.7544870654987291, (127.402, 105.17499999999998, 109.95400000000001)), ('A', 260, u'ASP', 0.770153687525821, (124.17499999999998, 109.49900000000001, 110.478)), ('A', 306, u'CYS', 0.6386011404853756, (152.10399999999998, 125.071, 116.82799999999999)), ('A', 320, u'VAL', 0.7510271353469319, (133.662, 112.785, 119.41900000000001)), ('A', 329, u'LEU', 0.6901824174982664, (146.894, 106.397, 131.99800000000002)), ('A', 373, u'VAL', 0.7023397843652739, (154.83200000000002, 111.21400000000001, 143.40800000000002)), ('A', 399, u'ALA', 0.7231239840552983, (135.311, 107.019, 142.63299999999998)), ('A', 440, u'PHE', 0.7053722771807164, (126.359, 139.303, 156.415)), ('A', 450, u'ILE', 0.7337598468679024, (128.309, 119.781, 145.478)), ('A', 476, u'VAL', 0.6909205524801716, (149.626, 140.05200000000002, 124.687)), ('A', 477, u'ASP', 0.6572317635524456, (153.268, 138.95600000000002, 124.637)), ('A', 484, u'ASP', 0.6931525898737122, (161.92200000000003, 139.186, 133.99)), ('A', 490, u'ALA', 0.711308261779853, (165.499, 125.383, 145.32700000000003)), ('A', 497, u'ASN', 0.7939127272391371, (152.89600000000002, 130.678, 155.08)), ('A', 519, u'MET', 0.7320727707192126, (163.05800000000002, 117.30499999999999, 151.46800000000002)), ('A', 576, u'LEU', 0.6787507593222587, (155.436, 136.46800000000002, 139.42000000000002)), ('A', 602, u'LEU', 0.7240070633789552, (144.76399999999998, 156.485, 137.82500000000002)), ('A', 618, u'ASP', 0.7477763923260073, (132.718, 142.061, 134.11399999999998)), ('A', 625, u'ALA', 0.7245774059661079, (133.311, 129.36200000000002, 132.05200000000002)), ('A', 627, u'PRO', 0.7046957284422433, (137.626, 128.065, 127.96000000000001)), ('A', 656, u'ALA', 0.6609495535726668, (151.30100000000002, 119.289, 130.499)), ('A', 669, u'CYS', 0.7086813656489184, (134.67399999999998, 117.333, 146.87)), ('A', 701, u'THR', 0.6614050948820515, (140.261, 140.416, 120.657)), ('A', 749, u'LEU', 0.6975757035705547, (146.181, 150.256, 121.41000000000001)), ('A', 757, u'ILE', 0.6634728074173551, (144.339, 145.131, 134.51399999999998)), ('A', 759, u'SER', 0.6962104310397147, (142.70499999999998, 139.42700000000002, 137.946)), ('A', 760, u'ASP', 0.7091510745126145, (139.618, 139.64499999999998, 135.671)), ('A', 764, u'VAL', 0.7438977364101078, (139.97299999999998, 151.316, 130.415)), ('A', 783, u'LYS', 0.7474721415059273, (129.523, 141.51899999999998, 124.67599999999999)), ('A', 784, u'SER', 0.6916391600241709, (129.92700000000002, 139.89600000000002, 121.251)), ('A', 839, u'GLY', 0.643852976054906, (129.20399999999998, 144.72899999999998, 158.478)), ('A', 842, u'CYS', 0.6951488367826261, (129.161, 144.167, 163.43)), ('A', 862, u'LEU', 0.6556785937111024, (138.791, 149.001, 159.70499999999998)), ('A', 865, u'ASP', 0.6896378014049512, (140.034, 151.344, 155.38800000000003)), ('A', 876, u'GLU', 0.6937483366049418, (126.519, 159.435, 157.07399999999998)), ('A', 880, u'VAL', 0.6772344865626256, (131.02800000000002, 156.012, 159.79899999999998)), ('A', 887, u'TYR', 0.725102143084867, (134.463, 153.19299999999998, 169.444)), ('A', 894, u'GLU', 0.7431705529118395, (137.16899999999998, 150.258, 179.20899999999997)), ('A', 895, u'LEU', 0.7633998231534679, (140.281, 148.13, 178.64899999999997)), ('A', 920, u'PHE', 0.7014143551855395, (147.375, 158.57899999999998, 161.698)), ('A', 924, u'MET', 0.6395472589709541, (148.23, 156.60999999999999, 155.724)), ('A', 1002, u'ZN', 0.607371747311077, (162.272, 127.02799999999999, 132.36)), ('B', 76, u'SER', 0.793957570385527, (164.42200000000003, 117.479, 159.76999999999998)), ('B', 87, u'MET', 0.7326658431829718, (153.433, 107.27199999999999, 153.181)), ('B', 98, u'LEU', 0.7768101638212906, (143.389, 96.71100000000001, 145.071)), ('B', 118, u'ASN', 0.7544572555000323, (138.49200000000002, 106.29700000000001, 134.653)), ('B', 130, u'VAL', 0.7440315812623435, (124.77499999999999, 106.007, 144.33200000000002)), ('B', 134, u'ASP', 0.7448902253947356, (115.019, 113.20100000000001, 144.318)), ('B', 142, u'CYS', 0.770522852008452, (117.94100000000002, 102.118, 141.565)), ('C', 10, u'SER', 0.6613679353591455, (117.785, 136.218, 162.89600000000002)), ('C', 13, u'LEU', 0.6788773834122384, (118.54100000000001, 132.795, 166.267)), ('C', 30, u'ALA', 0.6920131246557724, (118.007, 123.24000000000001, 155.42100000000002)), ('C', 33, u'VAL', 0.6918536071057112, (119.187, 128.098, 156.631)), ('C', 34, u'GLN', 0.7000130315278252, (116.616, 129.036, 153.98800000000003)), ('C', 70, u'LYS', 0.7777725440448963, (114.804, 133.208, 179.82800000000003)), ('D', 55, u'MET', 0.7688420448824832, (167.138, 147.918, 181.70899999999997)), ('D', 57, u'ARG', 0.7537005794404065, (162.24399999999997, 150.32000000000002, 181.68800000000002)), ('D', 84, u'THR', 0.7631046229582586, (125.604, 128.984, 174.736)), ('D', 87, u'MET', 0.7558405958323945, (123.779, 133.93, 173.46200000000002)), ('D', 91, u'LEU', 0.6797222830013175, (118.561, 136.472, 171.85100000000003)), ('D', 94, u'MET', 0.761522032458657, (116.68299999999999, 141.48700000000002, 171.541)), ('D', 95, u'LEU', 0.7574426624298144, (113.479, 139.52200000000002, 170.903)), ('D', 106, u'ILE', 0.7167434568344586, (104.248, 132.64499999999998, 170.43)), ('D', 113, u'GLY', 0.7311385792672171, (102.89, 125.433, 177.416)), ('D', 114, u'CYS', 0.6836946805897898, (101.17699999999999, 125.91000000000001, 174.034)), ('D', 125, u'ALA', 0.8200163914700294, (96.87299999999999, 126.117, 152.751)), ('D', 131, u'VAL', 0.7398897960130404, (100.245, 121.17599999999999, 172.21299999999997)), ('D', 132, u'ILE', 0.7360783288489013, (97.526, 122.408, 174.596)), ('D', 139, u'LYS', 0.7770117786516414, (89.438, 128.23499999999999, 176.71599999999998)), ('D', 143, u'ASP', 0.808852116703791, (86.576, 129.596, 170.541)), ('D', 152, u'ALA', 0.8148940050877017, (96.63799999999999, 134.41299999999998, 162.69)), ('D', 163, u'ASP', 0.8221965258337474, (96.693, 108.307, 173.771)), ('D', 168, u'GLN', 0.798851086821781, (85.49700000000001, 115.897, 169.696)), ('D', 176, u'ASN', 0.6954916666021218, (83.889, 117.412, 181.47)), ('D', 184, u'LEU', 0.7485764238628628, (95.595, 117.718, 173.58700000000002)), ('F', -20, u'G', 0.7636621519643293, (150.126, 127.974, 168.82000000000002)), ('F', -17, u'G', 0.713294199981843, (135.76399999999998, 122.886, 166.309)), ('G', 0, u'C', 0.8332343996006408, (144.94, 141.266, 162.526))]
handle_read_draw_probe_dots_unformatted("/Users/agnel/testdata/map_model/sars2/validation/statistics/structure_data/emdb/EMD-30275/7c2k/Model_validation_1/validation_cootdata/molprobity_probe7c2k_0.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
