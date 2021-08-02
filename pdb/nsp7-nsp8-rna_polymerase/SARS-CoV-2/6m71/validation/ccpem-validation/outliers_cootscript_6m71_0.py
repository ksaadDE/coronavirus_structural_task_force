
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
  data_keys = [ "clusters","rama", "rota", "cbeta", "probe", "smoc", "cablam",
               "jpred"]
  data_titles = { "clusters"  : "Outlier residue clusters",
                  "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes",
                  "smoc"  : "Local density fit (SMOC)",
                  "cablam": "Ca geometry (CaBLAM)",
                  "jpred":"SS prediction"}
  data_names = { "clusters"  : ["Chain","Residue","Cluster","Outlier types"],
                 "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"],
                 "smoc" : ["Chain", "Residue", "Name", "Score"],
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
                   "cablam" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_STRING,
                             gobject.TYPE_STRING,gobject.TYPE_PYOBJECT],
                   "jpred" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING,gobject.TYPE_STRING,
                             gobject.TYPE_STRING,gobject.TYPE_PYOBJECT]}
  else :
    data_types = dict([ (s, []) for s in ["clusters","rama","rota","cbeta","probe","smoc",
                                          "cablam","jpred"] ])

  def __init__ (self, data_file=None, data=None) :
    assert ([data, data_file].count(None) == 1)
    if (data is None) :
      data = load_pkl(data_file)
    if not self.confirm_data(data) :
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
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
data['jpred'] = []
data['clusters'] = [('A', '376', 1, 'smoc Outlier', (110.792, 140.74699999999999, 139.583)), ('A', '502', 1, 'cablam Outlier\nsmoc Outlier', (106.9, 131.1, 141.2)), ('A', '504', 1, 'cablam CA Geom Outlier', (112.6, 134.5, 143.0)), ('A', '506', 1, 'side-chain clash', (105.289, 134.638, 143.124)), ('A', '507', 1, 'side-chain clash', (112.363, 131.228, 145.017)), ('A', '509', 1, 'cablam Outlier', (105.2, 134.6, 149.9)), ('A', '515', 1, 'side-chain clash', (105.289, 134.638, 143.124)), ('A', '516', 1, 'side-chain clash', (101.305, 132.017, 137.304)), ('A', '536', 1, 'smoc Outlier', (110.94400000000002, 142.48800000000003, 131.846)), ('A', '538', 1, 'smoc Outlier', (112.91300000000001, 138.43800000000002, 135.42700000000002)), ('A', '539', 1, 'smoc Outlier', (114.818, 136.15200000000002, 137.81)), ('A', '540', 1, 'side-chain clash', (115.694, 133.41, 134.606)), ('A', '541', 1, 'side-chain clash', (112.363, 131.228, 145.017)), ('A', '562', 1, 'side-chain clash', (101.305, 132.017, 137.304)), ('A', '665', 1, 'side-chain clash', (115.694, 133.41, 134.606)), ('A', '125', 2, 'smoc Outlier', (137.47299999999998, 124.955, 102.17299999999999)), ('A', '180', 2, 'side-chain clash', (143.084, 136.486, 112.537)), ('A', '183', 2, 'side-chain clash', (143.084, 136.486, 112.537)), ('A', '185', 2, 'smoc Outlier', (142.007, 135.82000000000002, 105.932)), ('A', '186', 2, 'side-chain clash', (137.559, 136.882, 105.745)), ('A', '189', 2, 'smoc Outlier', (138.85500000000002, 138.94299999999998, 101.67699999999999)), ('A', '205', 2, 'side-chain clash', (133.844, 137.209, 98.259)), ('A', '207', 2, 'side-chain clash', (135.412, 130.353, 104.26)), ('A', '214', 2, 'smoc Outlier', (144.781, 134.48700000000002, 103.05199999999999)), ('A', '234', 2, 'side-chain clash', (133.844, 137.209, 98.259)), ('A', '236', 2, 'smoc Outlier', (128.472, 130.977, 99.962)), ('A', '237', 2, 'smoc Outlier', (131.92700000000002, 132.062, 101.16799999999999)), ('A', '241', 2, 'side-chain clash', (135.412, 130.353, 104.26)), ('A', '483', 3, 'side-chain clash', (100.4, 118.398, 115.344)), ('A', '568', 3, 'smoc Outlier', (104.485, 132.937, 127.921)), ('A', '569', 3, 'side-chain clash\nsmoc Outlier', (98.92, 129.948, 126.703)), ('A', '572', 3, 'side-chain clash', (101.753, 127.071, 123.189)), ('A', '573', 3, 'side-chain clash', (98.92, 129.948, 126.703)), ('A', '575', 3, 'side-chain clash', (105.435, 126.402, 118.572)), ('A', '576', 3, 'side-chain clash', (101.753, 127.071, 123.189)), ('A', '577', 3, 'side-chain clash', (97.615, 121.826, 124.34)), ('A', '578', 3, 'smoc Outlier', (96.94600000000001, 122.3, 119.24300000000001)), ('A', '579', 3, 'side-chain clash', (100.829, 123.263, 119.044)), ('A', '582', 3, 'side-chain clash', (100.4, 118.398, 115.344)), ('A', '638', 3, 'side-chain clash', (105.435, 126.402, 118.572)), ('A', '686', 3, 'side-chain clash', (104.651, 126.288, 125.132)), ('A', '613', 4, 'side-chain clash', (113.362, 103.991, 109.885)), ('A', '615', 4, 'side-chain clash\nsmoc Outlier', (118.187, 104.901, 110.948)), ('A', '699', 4, 'side-chain clash', (118.012, 115.607, 108.168)), ('A', '703', 4, 'side-chain clash\nsmoc Outlier', (118.012, 115.607, 108.168)), ('A', '753', 4, 'side-chain clash', (116.041, 109.869, 109.485)), ('A', '764', 4, 'side-chain clash', (116.041, 109.869, 109.485)), ('A', '765', 4, 'side-chain clash', (113.362, 103.991, 109.885)), ('A', '766', 4, 'side-chain clash', (118.187, 104.901, 110.948)), ('A', '203', 5, 'side-chain clash', (134.364, 136.861, 89.741)), ('A', '206', 5, 'side-chain clash', (136.552, 129.508, 94.063)), ('A', '209', 5, 'side-chain clash', (136.552, 129.508, 94.063)), ('A', '218', 5, 'cablam Outlier\nsmoc Outlier', (141.9, 131.0, 90.2)), ('A', '220', 5, 'cablam Outlier', (138.5, 132.0, 85.6)), ('A', '222', 5, 'side-chain clash', (134.364, 136.861, 89.741)), ('A', '86', 5, 'side-chain clash', (137.303, 137.292, 86.127)), ('A', '382', 6, 'side-chain clash', (121.125, 141.583, 139.512)), ('A', '400', 6, 'side-chain clash', (124.901, 136.795, 146.001)), ('A', '666', 6, 'side-chain clash', (121.125, 141.583, 139.512)), ('A', '668', 6, 'backbone clash', (121.431, 134.02, 142.72)), ('A', '672', 6, 'backbone clash\nside-chain clash', (124.901, 136.795, 146.001)), ('A', '673', 6, 'smoc Outlier', (122.60499999999999, 136.117, 141.73899999999998)), ('A', '412', 7, 'side-chain clash', (115.822, 110.237, 149.907)), ('A', '546', 7, 'side-chain clash', (115.822, 110.237, 149.907)), ('A', '844', 7, 'backbone clash\nside-chain clash', (108.801, 107.442, 148.06)), ('A', '845', 7, 'backbone clash\nside-chain clash\nDihedral angle:CA:CB:CG:OD1\ncablam Outlier', (110.40400000000001, 109.84100000000001, 148.553)), ('A', '846', 7, 'Dihedral angle:CA:CB:CG:OD1', (108.998, 109.952, 152.12800000000001)), ('A', '848', 7, 'side-chain clash\nsmoc Outlier', (105.784, 106.562, 149.485)), ('A', '595', 8, 'backbone clash', (91.183, 104.151, 128.499)), ('A', '927', 8, 'side-chain clash', (88.943, 101.332, 122.054)), ('A', '929', 8, 'backbone clash\nside-chain clash', (90.458, 99.771, 126.522)), ('A', '930', 8, 'side-chain clash\nBond angle:N:CA:C', (89.52799999999999, 103.273, 124.85199999999999)), ('A', '931', 8, 'backbone clash', (91.183, 104.151, 128.499)), ('A', '932', 8, 'smoc Outlier', (90.405, 106.71100000000001, 130.73)), ('A', '618', 9, 'Dihedral angle:CA:CB:CG:OD1', (120.801, 111.48100000000001, 121.986)), ('A', '619', 9, 'side-chain clash', (120.372, 117.551, 123.949)), ('A', '622', 9, 'side-chain clash', (120.372, 117.551, 123.949)), ('A', '758', 9, 'backbone clash\nside-chain clash', (109.476, 115.115, 124.169)), ('A', '759', 9, 'backbone clash\nside-chain clash\ncablam Outlier\nsmoc Outlier', (109.476, 115.115, 124.169)), ('A', '760', 9, 'Dihedral angle:CA:CB:CG:OD1\nsmoc Outlier', (114.846, 116.10799999999999, 122.49400000000001)), ('A', '196', 10, 'smoc Outlier', (137.24599999999998, 143.727, 92.12499999999999)), ('A', '200', 10, 'smoc Outlier', (135.23899999999998, 146.04299999999998, 87.143)), ('A', '201', 10, 'side-chain clash\nsmoc Outlier', (134.401, 144.4, 88.893)), ('A', '226', 10, 'side-chain clash', (130.706, 149.045, 85.938)), ('A', '229', 10, 'side-chain clash', (130.706, 149.045, 85.938)), ('A', '230', 10, 'side-chain clash', (134.401, 144.4, 88.893)), ('A', '100', 11, 'side-chain clash\nbackbone clash', (152.476, 131.972, 88.332)), ('A', '115', 11, 'side-chain clash\nbackbone clash', (152.476, 131.972, 88.332)), ('A', '116', 11, 'smoc Outlier', (150.583, 130.146, 91.31400000000001)), ('A', '117', 11, 'side-chain clash\nsmoc Outlier', (153.379, 128.828, 94.118)), ('A', '69', 11, 'smoc Outlier', (153.20299999999997, 125.169, 97.866)), ('A', '70', 11, 'side-chain clash', (153.379, 128.828, 94.118)), ('A', '601', 12, 'side-chain clash', (105.004, 105.967, 114.397)), ('A', '605', 12, 'side-chain clash', (105.004, 105.967, 114.397)), ('A', '606', 12, 'Dihedral angle:CA:C', (106.37199999999999, 102.974, 109.40400000000001)), ('A', '607', 12, 'Dihedral angle:N:CA\ncablam Outlier', (103.74000000000001, 104.423, 107.04700000000001)), ('A', '608', 12, 'smoc Outlier', (105.27799999999999, 104.21400000000001, 103.535)), ('A', '756', 12, 'smoc Outlier', (108.795, 110.65499999999999, 115.43900000000001)), ('A', '131', 13, 'side-chain clash', (136.246, 124.914, 113.63)), ('A', '146', 13, 'side-chain clash', (140.996, 121.092, 116.182)), ('A', '171', 13, 'smoc Outlier', (140.484, 121.867, 122.87799999999999)), ('A', '175', 13, 'side-chain clash', (140.996, 121.092, 116.182)), ('A', '247', 13, 'side-chain clash', (136.246, 124.914, 113.63)), ('A', '717', 14, 'backbone clash', (116.766, 110.754, 89.236)), ('A', '718', 14, 'backbone clash', (116.766, 110.754, 89.236)), ('A', '720', 14, 'side-chain clash', (119.028, 110.346, 96.056)), ('A', '721', 14, 'smoc Outlier', (120.242, 115.027, 91.49600000000001)), ('A', '775', 14, 'side-chain clash', (119.028, 110.346, 96.056)), ('A', '879', 15, 'Dihedral angle:CA:CB:CG:OD1\nsmoc Outlier', (107.577, 87.436, 137.379)), ('A', '882', 15, 'smoc Outlier', (103.1, 88.93700000000001, 138.942)), ('A', '885', 15, 'side-chain clash', (96.145, 89.309, 139.554)), ('A', '889', 15, 'side-chain clash\nsmoc Outlier', (94.666, 89.362, 139.045)), ('A', '918', 15, 'side-chain clash', (94.666, 89.362, 139.045)), ('A', '38', 16, 'side-chain clash', (121.872, 126.199, 91.296)), ('A', '39', 16, 'side-chain clash', (123.925, 122.804, 88.555)), ('A', '40', 16, 'side-chain clash\nsmoc Outlier', (126.28, 123.281, 84.993)), ('A', '725', 16, 'side-chain clash', (119.918, 124.413, 92.451)), ('A', '729', 16, 'side-chain clash\nsmoc Outlier', (121.872, 126.199, 91.296)), ('A', '127', 17, 'side-chain clash', (142.656, 124.018, 109.71)), ('A', '145', 17, 'side-chain clash', (142.656, 124.018, 109.71)), ('A', '149', 17, 'side-chain clash', (146.331, 126.198, 107.553)), ('A', '212', 17, 'side-chain clash', (146.331, 126.198, 107.553)), ('A', '631', 18, 'side-chain clash', (116.006, 130.363, 124.362)), ('A', '658', 18, 'side-chain clash\nsmoc Outlier', (113.431, 133.235, 127.152)), ('A', '662', 18, 'side-chain clash', (115.238, 131.389, 126.491)), ('A', '663', 18, 'side-chain clash', (115.238, 131.389, 126.491)), ('A', '598', 19, 'side-chain clash', (107.063, 100.658, 121.502)), ('A', '816', 19, 'side-chain clash', (107.513, 99.095, 124.279)), ('A', '817', 19, 'side-chain clash', (107.063, 100.658, 121.502)), ('A', '829', 19, 'side-chain clash', (102.234, 97.989, 122.816)), ('A', '257', 20, 'side-chain clash', (145.864, 148.854, 121.073)), ('A', '258', 20, 'side-chain clash\ncablam Outlier', (145.864, 148.854, 121.073)), ('A', '259', 20, 'smoc Outlier', (143.646, 145.497, 117.478)), ('A', '266', 20, 'side-chain clash', (141.931, 148.82, 122.444)), ('A', '419', 21, 'smoc Outlier', (108.187, 95.393, 149.618)), ('A', '420', 21, 'side-chain clash', (112.844, 91.385, 149.112)), ('A', '424', 21, 'side-chain clash', (112.844, 91.385, 149.112)), ('A', '428', 21, 'smoc Outlier', (113.76700000000001, 87.763, 143.568)), ('A', '701', 22, 'side-chain clash', (123.522, 120.431, 108.625)), ('A', '705', 22, 'side-chain clash', (123.522, 120.431, 108.625)), ('A', '785', 22, 'side-chain clash\nsmoc Outlier', (125.411, 121.404, 114.221)), ('A', '789', 22, 'side-chain clash', (125.411, 121.404, 114.221)), ('A', '439', 23, 'side-chain clash', (115.62, 104.939, 140.209)), ('A', '548', 23, 'side-chain clash', (115.62, 104.939, 140.209)), ('A', '836', 23, 'smoc Outlier', (113.897, 100.84100000000001, 137.266)), ('A', '837', 23, 'smoc Outlier', (110.41400000000002, 99.77, 138.347)), ('A', '335', 24, 'side-chain clash', (107.988, 156.866, 145.994)), ('A', '336', 24, 'side-chain clash', (107.988, 156.866, 145.994)), ('A', '531', 24, 'side-chain clash', (112.974, 154.809, 148.218)), ('A', '657', 24, 'side-chain clash', (112.974, 154.809, 148.218)), ('A', '486', 25, 'smoc Outlier', (97.708, 132.70399999999998, 117.877)), ('A', '487', 25, 'side-chain clash', (100.116, 135.232, 119.73)), ('A', '642', 25, 'side-chain clash', (100.116, 135.232, 119.73)), ('A', '645', 25, 'side-chain clash', (98.796, 136.428, 118.399)), ('A', '459', 26, 'smoc Outlier', (127.193, 126.953, 126.689)), ('A', '677', 26, 'cablam Outlier', (125.0, 132.2, 129.7)), ('A', '678', 26, 'cablam CA Geom Outlier', (122.3, 130.3, 127.8)), ('A', '475', 27, 'smoc Outlier', (111.329, 123.49300000000001, 106.319)), ('A', '476', 27, 'side-chain clash', (112.819, 120.865, 111.455)), ('A', '696', 27, 'side-chain clash\nsmoc Outlier', (112.819, 120.865, 111.455)), ('A', '436', 28, 'side-chain clash', (120.048, 95.091, 138.104)), ('A', '437', 28, 'smoc Outlier', (117.99000000000001, 96.99100000000001, 141.88700000000003)), ('A', '438', 28, 'side-chain clash', (120.048, 95.091, 138.104)), ('A', '532', 29, 'side-chain clash\nsmoc Outlier', (101.557, 143.348, 120.803)), ('A', '647', 29, 'side-chain clash', (102.699, 145.497, 116.964)), ('A', '650', 29, 'side-chain clash', (101.557, 143.348, 120.803)), ('A', '369', 30, 'side-chain clash\nsmoc Outlier', (132.453, 142.019, 145.227)), ('A', '373', 30, 'side-chain clash', (132.453, 142.019, 145.227)), ('A', '387', 30, 'smoc Outlier', (129.271, 142.61399999999998, 145.768)), ('A', '290', 31, 'side-chain clash', (123.048, 139.63, 106.009)), ('A', '293', 31, 'smoc Outlier', (121.085, 145.678, 105.337)), ('A', '309', 31, 'side-chain clash', (123.048, 139.63, 106.009)), ('A', '139', 32, 'smoc Outlier', (139.654, 113.37499999999999, 110.8)), ('A', '140', 32, 'side-chain clash', (144.327, 113.045, 111.792)), ('A', '143', 32, 'side-chain clash\nsmoc Outlier', (144.327, 113.045, 111.792)), ('A', '892', 33, 'side-chain clash', (91.957, 98.926, 146.396)), ('A', '915', 33, 'side-chain clash', (91.957, 98.926, 146.396)), ('A', '916', 33, 'side-chain clash', (90.275, 96.87, 145.553)), ('A', '301', 34, 'side-chain clash\ncablam Outlier', (115.997, 141.885, 110.743)), ('A', '306', 34, 'side-chain clash', (115.997, 141.885, 110.743)), ('A', '308', 34, 'smoc Outlier', (117.689, 135.88500000000002, 112.669)), ('A', '469', 35, 'side-chain clash', (117.169, 128.493, 112.96)), ('A', '630', 35, 'smoc Outlier', (118.98700000000001, 128.025, 117.603)), ('A', '633', 35, 'side-chain clash\nsmoc Outlier', (117.169, 128.493, 112.96)), ('A', '498', 36, 'side-chain clash', (98.96, 127.284, 142.486)), ('A', '513', 36, 'side-chain clash', (98.96, 127.284, 142.486)), ('A', '136', 37, 'side-chain clash', (132.058, 108.579, 115.856)), ('A', '783', 37, 'side-chain clash', (132.058, 108.579, 115.856)), ('A', '490', 38, 'smoc Outlier', (93.612, 135.759, 129.843)), ('A', '525', 38, 'smoc Outlier', (95.87199999999999, 141.476, 129.961)), ('A', '547', 39, 'side-chain clash', (116.599, 113.096, 139.551)), ('A', '555', 39, 'side-chain clash', (116.599, 113.096, 139.551)), ('A', '366', 40, 'side-chain clash\nsmoc Outlier', (104.788, 151.11, 139.674)), ('A', '370', 40, 'side-chain clash', (104.788, 151.11, 139.674)), ('A', '299', 41, 'side-chain clash', (114.323, 145.186, 119.439)), ('A', '652', 41, 'side-chain clash', (114.323, 145.186, 119.439)), ('A', '824', 42, 'cablam Outlier', (94.3, 87.8, 117.0)), ('A', '826', 42, 'smoc Outlier', (99.971, 91.581, 116.15599999999999)), ('A', '599', 43, 'side-chain clash', (100.424, 99.233, 113.555)), ('A', '603', 43, 'side-chain clash\nsmoc Outlier', (100.424, 99.233, 113.555)), ('A', '893', 44, 'Dihedral angle:CA:CB:CG:OD1', (93.532, 93.509, 151.571)), ('A', '894', 44, 'Dihedral angle:CB:CG:CD:OE1\nsmoc Outlier', (95.21400000000001, 95.786, 154.122)), ('A', '274', 45, 'backbone clash\ncablam Outlier', (127.526, 151.595, 122.289)), ('A', '275', 45, 'backbone clash\ncablam Outlier', (127.526, 151.595, 122.289)), ('A', '113', 46, 'side-chain clash', (148.656, 123.642, 82.765)), ('A', '74', 46, 'side-chain clash', (148.656, 123.642, 82.765)), ('A', '830', 47, 'side-chain clash', (129.001, 154.272, 136.876)), ('A', '868', 47, 'side-chain clash', (129.001, 154.272, 136.876)), ('A', '242', 48, 'side-chain clash', (128.658, 134.598, 110.023)), ('A', '463', 48, 'side-chain clash', (128.658, 134.598, 110.023)), ('A', '32', 49, 'side-chain clash', (138.314, 114.45, 99.94)), ('A', '47', 49, 'side-chain clash', (138.314, 114.45, 99.94)), ('A', '291', 50, 'side-chain clash\nsmoc Outlier', (123.274, 140.81, 98.586)), ('A', '735', 50, 'side-chain clash', (123.274, 140.81, 98.586)), ('A', '452', 51, 'side-chain clash', (122.673, 122.443, 136.912)), ('A', '624', 51, 'side-chain clash', (122.673, 122.443, 136.912)), ('A', '44', 52, 'smoc Outlier', (127.024, 121.301, 96.61)), ('A', '708', 52, 'smoc Outlier', (124.82799999999999, 118.436, 99.543)), ('A', '468', 53, 'side-chain clash', (120.78, 126.971, 104.111)), ('A', '731', 53, 'side-chain clash', (120.78, 126.971, 104.111)), ('A', '151', 54, 'cablam CA Geom Outlier', (147.8, 125.4, 117.7)), ('A', '152', 54, 'smoc Outlier', (148.86100000000002, 122.203, 119.501)), ('A', '558', 55, 'side-chain clash', (111.797, 125.961, 136.247)), ('A', '683', 55, 'side-chain clash', (111.797, 125.961, 136.247)), ('A', '611', 56, 'smoc Outlier', (113.363, 100.12499999999999, 102.57499999999999)), ('A', '768', 56, 'smoc Outlier', (118.099, 102.364, 104.003)), ('A', '76', 57, 'side-chain clash', (141.107, 127.558, 78.886)), ('A', '79', 57, 'side-chain clash', (141.107, 127.558, 78.886)), ('A', '350', 58, 'smoc Outlier', (122.01400000000001, 138.70499999999998, 120.23700000000001)), ('A', '352', 58, 'smoc Outlier', (121.44600000000001, 144.635, 120.643)), ('A', '357', 59, 'smoc Outlier', (108.68599999999999, 152.407, 125.67199999999998)), ('A', '358', 59, 'smoc Outlier', (106.49400000000001, 152.93200000000002, 128.76299999999998)), ('C', '10', 1, 'side-chain clash', (124.291, 99.912, 154.15)), ('C', '11', 1, 'side-chain clash', (121.336, 104.622, 151.452)), ('C', '14', 1, 'side-chain clash', (124.034, 108.145, 156.623)), ('C', '3', 1, 'side-chain clash', (125.496, 96.317, 145.326)), ('C', '32', 1, 'smoc Outlier', (129.2, 110.187, 154.64499999999998)), ('C', '36', 1, 'side-chain clash', (125.129, 107.999, 151.795)), ('C', '5', 1, 'backbone clash', (123.046, 93.82, 151.025)), ('C', '52', 1, 'side-chain clash', (124.291, 99.912, 154.15)), ('C', '6', 1, 'backbone clash', (123.046, 93.82, 151.025)), ('C', '7', 1, 'side-chain clash', (125.496, 96.317, 145.326)), ('C', '47', 2, 'side-chain clash', (134.963, 97.285, 150.502)), ('C', '49', 2, 'smoc Outlier', (131.141, 95.689, 153.138)), ('C', '50', 2, 'side-chain clash', (134.169, 97.645, 155.55)), ('C', '53', 2, 'side-chain clash', (134.169, 97.645, 155.55)), ('C', '23', 3, 'Dihedral angle:CB:CG:CD:OE1', (124.57799999999999, 117.303, 158.032)), ('C', '26', 3, 'smoc Outlier', (130.07, 119.90700000000001, 156.333)), ('C', '34', 4, 'side-chain clash', (133.864, 107.566, 146.69)), ('C', '38', 4, 'side-chain clash', (133.864, 107.566, 146.69)), ('C', '17', 5, 'side-chain clash', (116.403, 100.773, 158.711)), ('C', '22', 5, 'side-chain clash', (116.403, 100.773, 158.711)), ('C', '65', 6, 'cablam CA Geom Outlier', (123.9, 109.3, 169.3)), ('D', '87', 1, 'smoc Outlier', (114.715, 103.35, 162.732)), ('D', '88', 1, 'side-chain clash', (120.517, 104.459, 165.844)), ('D', '90', 1, 'side-chain clash', (116.403, 100.773, 158.711)), ('D', '91', 1, 'side-chain clash', (120.406, 100.992, 157.823)), ('D', '92', 1, 'side-chain clash', (122.208, 97.791, 162.592)), ('D', '95', 1, 'side-chain clash', (122.208, 97.791, 162.592)), ('D', '101', 2, 'side-chain clash', (132.732, 89.493, 158.704)), ('D', '102', 2, 'side-chain clash', (133.494, 95.169, 162.601)), ('D', '106', 2, 'side-chain clash', (133.494, 95.169, 162.601)), ('D', '114', 3, 'smoc Outlier', (135.155, 100.292, 173.165)), ('D', '115', 3, 'smoc Outlier', (134.37800000000001, 102.636, 170.271)), ('D', '118', 4, 'backbone clash', (140.987, 106.494, 164.516)), ('D', '129', 4, 'backbone clash', (140.987, 106.494, 164.516)), ('B', '103', 1, 'smoc Outlier', (125.651, 155.463, 143.32200000000003)), ('B', '105', 1, 'side-chain clash', (129.631, 159.545, 137.735)), ('B', '106', 1, 'side-chain clash', (129.001, 154.272, 136.876)), ('B', '107', 1, 'smoc Outlier', (124.783, 157.254, 137.475)), ('B', '109', 1, 'side-chain clash', (129.631, 159.545, 137.735)), ('B', '120', 1, 'side-chain clash', (127.503, 149.817, 142.766)), ('B', '124', 1, 'side-chain clash', (127.503, 149.817, 142.766)), ('B', '125', 1, 'side-chain clash', (132.606, 149.886, 147.127)), ('B', '190', 1, 'side-chain clash', (132.606, 149.886, 147.127)), ('B', '99', 1, 'cablam Outlier', (121.6, 155.3, 147.9)), ('B', '132', 2, 'side-chain clash', (140.938, 130.766, 149.976)), ('B', '134', 2, 'side-chain clash', (139.488, 126.539, 147.047)), ('B', '138', 2, 'side-chain clash', (140.938, 130.766, 149.976)), ('B', '142', 2, 'smoc Outlier', (142.43200000000002, 137.094, 149.931)), ('B', '158', 2, 'smoc Outlier', (135.429, 138.18800000000002, 159.202)), ('B', '159', 2, 'side-chain clash', (138.036, 135.859, 155.2)), ('B', '186', 2, 'side-chain clash', (138.036, 135.859, 155.2)), ('B', '160', 3, 'side-chain clash', (130.406, 130.465, 158.987)), ('B', '161', 3, 'smoc Outlier', (133.64, 128.567, 157.015)), ('B', '164', 3, 'side-chain clash', (130.406, 130.465, 158.987)), ('B', '180', 3, 'side-chain clash', (138.061, 127.484, 156.09)), ('B', '182', 3, 'cablam CA Geom Outlier', (136.1, 124.7, 153.4)), ('B', '184', 3, 'side-chain clash', (138.061, 127.484, 156.09)), ('B', '111', 4, 'cablam Outlier\nsmoc Outlier', (124.6, 159.4, 128.5)), ('B', '112', 4, 'cablam Outlier', (121.1, 160.1, 129.9)), ('B', '113', 4, 'backbone clash', (118.964, 156.078, 133.399)), ('B', '87', 5, 'smoc Outlier', (106.55799999999999, 143.33100000000002, 147.996)), ('B', '90', 5, 'side-chain clash', (112.639, 143.176, 147.73)), ('B', '94', 5, 'side-chain clash', (112.639, 143.176, 147.73)), ('B', '177', 6, 'side-chain clash', (144.909, 122.601, 154.75)), ('B', '178', 6, 'side-chain clash', (144.909, 122.601, 154.75))]
data['probe'] = [(' A 487  CYS  SG ', ' A 642  HIS  ND1', -0.897, (100.369, 135.744, 119.034)), (' A 335  VAL  O  ', ' A 336  ASP  OD1', -0.83, (107.988, 156.866, 145.994)), (' A 487  CYS  SG ', ' A 645  CYS  SG ', -0.781, (98.796, 136.428, 118.399)), (' A 927  PRO  O  ', ' A 930  VAL  CG2', -0.74, (90.073, 101.431, 121.2)), (' A 844  VAL HG12', ' A 845  ASP  N  ', -0.734, (108.613, 107.736, 148.582)), (' A 844  VAL HG11', ' A 848  VAL HG22', -0.707, (105.784, 106.562, 149.485)), (' A 301  CYS  SG ', ' A 306  CYS  SG ', -0.696, (115.997, 141.885, 110.743)), (' A 844  VAL HG12', ' A 845  ASP  H  ', -0.669, (108.683, 108.347, 148.041)), (' A 291  ASP  HB3', ' A 735  ARG HH22', -0.645, (123.274, 140.81, 98.586)), (' A 701  THR  O  ', ' A 705  ASN  ND2', -0.642, (123.16, 119.694, 107.157)), (' B 132  ILE HG21', ' B 138  TYR  HB2', -0.636, (140.938, 130.766, 149.976)), (' A  32  TYR  HB3', ' A  47  LYS  HE2', -0.622, (138.314, 114.45, 99.94)), (' A 699  ALA  O  ', ' A 703  ASN  ND2', -0.622, (118.012, 115.607, 108.168)), (' A 531  THR  O  ', ' A 657  ASN  ND2', -0.612, (107.243, 142.043, 125.635)), (' A 338  VAL HG11', ' B  95  LEU HD21', -0.612, (112.974, 154.809, 148.218)), (' A 844  VAL  CG1', ' A 845  ASP  H  ', -0.612, (108.673, 107.552, 148.008)), (' A 930  VAL  O  ', ' A 930  VAL HG12', -0.606, (90.096, 105.422, 124.098)), (' B 105  ASN  O  ', ' B 109  ASN  ND2', -0.606, (129.631, 159.545, 137.735)), (' A  39  ASN  O  ', ' A 725  HIS  NE2', -0.605, (123.925, 122.804, 88.555)), (' B  90  MET  HG2', ' B  94  MET  HE2', -0.604, (112.639, 143.176, 147.73)), (' A 576  LEU HD11', ' A 686  THR HG22', -0.603, (104.651, 126.288, 125.132)), (' B 180  LEU HD13', ' B 184  LEU HD21', -0.595, (138.061, 127.484, 156.09)), (' B 159  VAL HG22', ' B 186  VAL HG22', -0.594, (138.036, 135.859, 155.2)), (' A 206  THR  OG1', ' A 209  ASN  ND2', -0.592, (136.552, 129.508, 94.063)), (' A 149  TYR  HE2', ' A 212  LEU HD13', -0.59, (146.251, 125.83, 107.131)), (' A 412  PRO  HG3', ' C  14  LEU HD23', -0.59, (122.414, 109.577, 152.06)), (' A 725  HIS  O  ', ' A 729  GLU  HG3', -0.589, (119.918, 124.413, 92.451)), (' A 885  LEU HD21', ' A 889  ARG  NH2', -0.585, (96.145, 89.309, 139.554)), (' A 816  HIS  O  ', ' A 830  PRO  HA ', -0.585, (107.513, 99.095, 124.279)), (' A 507  ASN  ND2', ' A 541  GLN  OE1', -0.581, (112.363, 131.228, 145.017)), (' A 598  TRP  NE1', ' A 817  THR  OG1', -0.58, (107.063, 100.658, 121.502)), (' A 498  LEU  O  ', ' A 513  ARG  HB2', -0.578, (98.96, 127.284, 142.486)), (' A 927  PRO  HA ', ' A 930  VAL HG22', -0.577, (91.357, 101.286, 122.113)), (' A 615  MET  HB2', ' A 766  PHE  HE2', -0.571, (118.187, 104.901, 110.948)), (' A 844  VAL  CG1', ' A 845  ASP  N  ', -0.57, (108.801, 107.442, 148.06)), (' A 412  PRO  O  ', ' A 546  TYR  OH ', -0.562, (115.822, 110.237, 149.907)), (' A 487  CYS  SG ', ' A 642  HIS  CE1', -0.561, (100.116, 135.232, 119.73)), (' A 717  ASP  OD1', ' A 718  LYS  N  ', -0.557, (116.766, 110.754, 89.236)), (' A 127  LEU HD13', ' A 145  ILE HG21', -0.552, (142.656, 124.018, 109.71)), (' A 257  VAL  HA ', ' A 266  ILE HG12', -0.548, (141.931, 148.82, 122.444)), (' C  66  VAL HG11', ' D  88  GLN  HG2', -0.546, (120.517, 104.459, 165.844)), (' A 100  ASP  HB2', ' A 115  SER  HB2', -0.544, (153.994, 129.718, 86.912)), (' D 118  ASN  OD1', ' D 129  MET  N  ', -0.534, (140.987, 106.494, 164.516)), (' A 516  TYR  OH ', ' A 569  ARG  NH1', -0.533, (100.128, 130.78, 134.06)), (' A 515  TYR  HE1', ' B  83  VAL HG21', -0.533, (102.776, 137.509, 145.253)), (' A 547  ALA  HB3', ' A 555  ARG  HD3', -0.531, (116.599, 113.096, 139.551)), (' A 532  LYS  HD2', ' A 650  HIS  HD2', -0.528, (101.388, 142.879, 120.981)), (' A 785  VAL  O  ', ' A 789  GLN  HB2', -0.523, (125.411, 121.404, 114.221)), (' B 160  VAL HG13', ' B 164  SER  HA ', -0.523, (130.406, 130.465, 158.987)), (' A 436  GLU  HB2', ' A 438  LYS  HE2', -0.523, (120.048, 95.091, 138.104)), (' A 242  MET  HG2', ' A 463  MET  HE2', -0.522, (128.658, 134.598, 110.023)), (' A 468  GLN  HA ', ' A 731  LEU HD22', -0.519, (120.78, 126.971, 104.111)), (' A 595  TYR  CE1', ' A 929  THR  O  ', -0.519, (91.202, 101.825, 126.866)), (' A 476  VAL HG22', ' A 696  ILE HG22', -0.516, (112.819, 120.865, 111.455)), (' A 420  TYR  O  ', ' A 424  VAL HG23', -0.515, (112.844, 91.385, 149.112)), (' A 506  PHE  O  ', ' A 515  TYR  OH ', -0.511, (105.948, 135.167, 145.414)), (' A 927  PRO  O  ', ' A 930  VAL HG23', -0.509, (88.943, 101.332, 122.054)), (' A 226  THR HG23', ' A 229  SER  HB3', -0.509, (130.706, 149.045, 85.938)), (' A 701  THR HG22', ' A 705  ASN HD21', -0.508, (123.033, 120.813, 108.722)), (' A 506  PHE  HB3', ' A 515  TYR  CE2', -0.506, (105.289, 134.638, 143.124)), (' A  38  TYR  HE1', ' A 729  GLU  HG2', -0.502, (121.383, 126.064, 91.393)), (' A 540  THR HG23', ' A 665  GLU  HG3', -0.501, (115.694, 133.41, 134.606)), (' A 304  ASP  N  ', ' A 304  ASP  OD1', -0.5, (110.456, 137.569, 110.165)), (' A 647  SER  OG ', ' A 650  HIS  ND1', -0.498, (102.699, 145.497, 116.964)), (' A 369  LYS  O  ', ' A 373  VAL HG23', -0.497, (103.913, 144.887, 136.998)), (' A 387  LEU  HG ', ' B 128  LEU HD13', -0.496, (132.453, 142.019, 145.227)), (' B 120  ILE  O  ', ' B 124  THR  HB ', -0.495, (127.503, 149.817, 142.766)), (' A 758  LEU HD23', ' A 759  SER  N  ', -0.491, (109.569, 114.802, 123.961)), (' A  86  ILE HD13', ' A 222  PHE  HB2', -0.49, (137.303, 137.292, 86.127)), (' A 483  TYR  CE1', ' A 582  THR HG21', -0.49, (100.072, 118.575, 115.145)), (' A 483  TYR  HE1', ' A 582  THR HG21', -0.487, (100.4, 118.398, 115.344)), (' A  74  ARG  HA ', ' A 113  HIS  HD1', -0.483, (148.656, 123.642, 82.765)), (' A 572  HIS  O  ', ' A 576  LEU  HG ', -0.483, (101.753, 127.071, 123.189)), (' B 134  ASP  N  ', ' B 134  ASP  OD1', -0.482, (139.488, 126.539, 147.047)), (' B 125  ALA  O  ', ' B 190  ARG  NE ', -0.482, (132.606, 149.886, 147.127)), (' A 668  MET  HA ', ' A 672  SER  O  ', -0.48, (121.431, 134.02, 142.72)), (' A 658  GLU  O  ', ' A 662  VAL HG12', -0.479, (113.431, 133.235, 127.152)), (' A 892  HIS  NE2', ' A 916  TRP  CZ3', -0.474, (89.772, 96.866, 145.637)), (' A  38  TYR  CE1', ' A 729  GLU  HG2', -0.472, (121.872, 126.199, 91.296)), (' A 290  TRP  HE1', ' A 309  HIS  CE1', -0.47, (123.048, 139.63, 106.009)), (' A 257  VAL HG23', ' A 258  ASP  H  ', -0.469, (145.864, 148.854, 121.073)), (' A 149  TYR  CE2', ' A 212  LEU HD13', -0.467, (146.331, 126.198, 107.553)), (' A 146  LEU HD11', ' A 175  TYR  HE1', -0.466, (140.996, 121.092, 116.182)), (' B 177  SER  OG ', ' B 178  PRO  HD3', -0.463, (144.909, 122.601, 154.75)), (' A 207  LEU HD21', ' A 241  LEU  HG ', -0.459, (135.412, 130.353, 104.26)), (' A 595  TYR  CD1', ' A 929  THR  O  ', -0.459, (91.034, 101.224, 126.359)), (' A 892  HIS  NE2', ' A 916  TRP  CE3', -0.458, (90.275, 96.87, 145.553)), (' A 100  ASP  N  ', ' A 115  SER  O  ', -0.457, (152.476, 131.972, 88.332)), (' A 758  LEU HD23', ' A 759  SER  H  ', -0.456, (109.476, 115.115, 124.169)), (' A 601  MET  O  ', ' A 605  VAL HG23', -0.455, (105.004, 105.967, 114.397)), (' A 889  ARG HH21', ' A 918  PRO  HD3', -0.455, (94.666, 89.362, 139.045)), (' A  40  ASP  N  ', ' A  40  ASP  OD1', -0.454, (126.28, 123.281, 84.993)), (' C  17  LEU HD22', ' C  22  VAL HG21', -0.454, (126.038, 110.934, 161.109)), (' C  12  VAL HG13', ' D  91  LEU HD13', -0.453, (120.406, 100.992, 157.823)), (' C  12  VAL HG21', ' D  90  MET  SD ', -0.452, (116.403, 100.773, 158.711)), (' A 577  LYS  HA ', ' A 577  LYS  HD3', -0.452, (97.615, 121.826, 124.34)), (' C  47  GLU  HA ', ' C  50  GLU  HG2', -0.45, (134.963, 97.285, 150.502)), (' A 830  PRO  O  ', ' A 868  PRO  HG2', -0.448, (104.241, 97.669, 127.924)), (' A 271  LEU HD11', ' B 106  ILE HG23', -0.447, (129.001, 154.272, 136.876)), (' C  34  GLN  NE2', ' C  38  ASP  OD2', -0.447, (133.864, 107.566, 146.69)), (' A 929  THR  O  ', ' A 929  THR  OG1', -0.443, (90.458, 99.771, 126.522)), (' A 619  TYR  HB3', ' A 622  CYS  HB2', -0.442, (120.372, 117.551, 123.949)), (' A 274  ASP  OD1', ' A 275  PHE  N  ', -0.439, (127.526, 151.595, 122.289)), (' A 595  TYR  CZ ', ' A 931  LEU  O  ', -0.437, (91.183, 104.151, 128.499)), (' A 201  ILE HG23', ' A 222  PHE  HB3', -0.436, (136.178, 139.181, 87.572)), (' A 331  ARG  HG2', ' B 113  GLY  O  ', -0.435, (118.964, 156.078, 133.399)), (' A  50  LYS  HA ', ' A  50  LYS  HD2', -0.433, (142.068, 114.996, 91.257)), (' C  50  GLU  HA ', ' C  53  VAL HG12', -0.432, (134.169, 97.645, 155.55)), (' C   5  ASP  OD1', ' C   6  VAL  N  ', -0.432, (123.046, 93.82, 151.025)), (' A 599  HIS  CE1', ' A 603  LYS  HG3', -0.432, (100.424, 99.233, 113.555)), (' D 102  ALA  O  ', ' D 106  ILE HG12', -0.43, (133.494, 95.169, 162.601)), (' D  92  PHE  HA ', ' D  95  LEU HD12', -0.43, (122.208, 97.791, 162.592)), (' A 205  LEU HD22', ' A 234  VAL HG12', -0.429, (133.844, 137.209, 98.259)), (' A 516  TYR  CE2', ' A 562  ILE HD11', -0.429, (101.305, 132.017, 137.304)), (' A 452  ASP  OD2', ' A 624  ARG  NH2', -0.428, (122.673, 122.443, 136.912)), (' A 720  VAL HG11', ' A 775  LEU HD13', -0.427, (119.028, 110.346, 96.056)), (' A 140  ASP  HA ', ' A 143  LYS  HE2', -0.427, (144.327, 113.045, 111.792)), (' A 892  HIS  HD2', ' A 915  TYR  OH ', -0.427, (91.957, 98.926, 146.396)), (' A 631  ARG  HG2', ' A 663  LEU HD11', -0.426, (116.006, 130.363, 124.362)), (' A  76  THR HG22', ' A  79  ASN  H  ', -0.423, (140.783, 128.852, 76.889)), (' A 384  SER  O  ', ' A 384  SER  OG ', -0.423, (120.193, 146.309, 148.643)), (' A 569  ARG  O  ', ' A 573  GLN  HB2', -0.422, (98.92, 129.948, 126.703)), (' A 575  LEU  O  ', ' A 579  ILE HG13', -0.421, (100.829, 123.263, 119.044)), (' A 136  GLU  OE2', ' A 783  LYS  NZ ', -0.42, (132.058, 108.579, 115.856)), (' A 203  GLY  HA3', ' A 222  PHE  CD2', -0.419, (134.364, 136.861, 89.741)), (' A 753  PHE  CE1', ' A 764  VAL HG11', -0.419, (116.041, 109.869, 109.485)), (' A 131  LEU HD13', ' A 247  LEU HD23', -0.418, (136.246, 124.914, 113.63)), (' A 575  LEU HD21', ' A 638  LEU HD22', -0.417, (105.435, 126.402, 118.572)), (' A 613  HIS  O  ', ' A 765  CYS  HA ', -0.417, (113.362, 103.991, 109.885)), (' A 201  ILE  H  ', ' A 230  GLY  HA3', -0.417, (134.401, 144.4, 88.893)), (' A 400  ALA  HA ', ' A 672  SER  HB2', -0.416, (124.901, 136.795, 146.001)), (' A 186  LEU  HA ', ' A 186  LEU HD23', -0.416, (137.559, 136.882, 105.745)), (' C   3  MET  SD ', ' C   7  LYS  HE3', -0.416, (125.496, 96.317, 145.326)), (' A 469  LEU HD11', ' A 633  MET  HG3', -0.416, (117.169, 128.493, 112.96)), (' A 180  GLU  O  ', ' A 183  ARG  HG2', -0.416, (143.084, 136.486, 112.537)), (' C  11  VAL  HA ', ' C  36  HIS  HE1', -0.416, (121.336, 104.622, 151.452)), (' A 439  HIS  HB3', ' A 548  ILE  CG2', -0.415, (115.62, 104.939, 140.209)), (' C  14  LEU HD22', ' C  36  HIS  CB ', -0.415, (125.129, 107.999, 151.795)), (' A 366  LEU HD22', ' A 370  GLU  HG2', -0.414, (104.788, 151.11, 139.674)), (' C  10  SER  N  ', ' C  52  MET  HE1', -0.414, (124.291, 99.912, 154.15)), (' A 662  VAL HG13', ' A 663  LEU HD12', -0.413, (115.238, 131.389, 126.491)), (' A 701  THR HG22', ' A 705  ASN  ND2', -0.411, (123.522, 120.431, 108.625)), (' A 558  ALA  O  ', ' A 683  GLY  HA3', -0.41, (111.797, 125.961, 136.247)), (' A 382  ALA  HB2', ' A 666  MET  HE1', -0.41, (121.125, 141.583, 139.512)), (' A 532  LYS  HD2', ' A 650  HIS  CD2', -0.408, (101.557, 143.348, 120.803)), (' A 829  LEU  HA ', ' A 829  LEU HD23', -0.408, (102.234, 97.989, 122.816)), (' A 299  VAL HG22', ' A 652  PHE  CE2', -0.407, (114.323, 145.186, 119.439)), (' A  76  THR  HB ', ' A  79  ASN  HB3', -0.406, (141.107, 127.558, 78.886)), (' C  14  LEU  HA ', ' C  14  LEU HD12', -0.403, (124.034, 108.145, 156.623)), (' A  70  PHE  HA ', ' A 117  GLN  HA ', -0.403, (153.379, 128.828, 94.118)), (' D 101  ASP  N  ', ' D 101  ASP  OD1', -0.401, (132.732, 89.493, 158.704))]
data['omega'] = [('A', ' 505 ', 'PRO', None, (111.85800000000009, 136.76800000000003, 143.35399999999996)), ('B', ' 183 ', 'PRO', None, (134.172, 125.546, 152.087))]
data['cablam'] = [('A', '167', 'GLU', 'check CA trace,carbonyls, peptide', 'bend\nSSS-T', (135.5, 116.2, 128.4)), ('A', '218', 'ASP', 'check CA trace,carbonyls, peptide', ' \nB----', (141.9, 131.0, 90.2)), ('A', '220', 'GLY', 'check CA trace,carbonyls, peptide', ' \n---S-', (138.5, 132.0, 85.6)), ('A', '258', 'ASP', 'check CA trace,carbonyls, peptide', 'turn\nBTTS-', (144.7, 149.0, 118.5)), ('A', '274', 'ASP', 'check CA trace,carbonyls, peptide', ' \n----H', (125.6, 150.8, 123.3)), ('A', '275', 'PHE', 'check CA trace,carbonyls, peptide', ' \n---HH', (128.7, 149.9, 121.2)), ('A', '301', 'CYS', 'check CA trace,carbonyls, peptide', ' \nTS-SS', (114.3, 144.6, 111.2)), ('A', '502', 'ALA', 'check CA trace,carbonyls, peptide', ' \nS---T', (106.9, 131.1, 141.2)), ('A', '509', 'TRP', 'check CA trace,carbonyls, peptide', 'turn\nGGT--', (105.2, 134.6, 149.9)), ('A', '607', 'SER', 'check CA trace,carbonyls, peptide', 'bend\nHTSS-', (103.7, 104.4, 107.0)), ('A', '677', 'PRO', 'check CA trace,carbonyls, peptide', ' \nE--S-', (125.0, 132.2, 129.7)), ('A', '759', 'SER', 'check CA trace,carbonyls, peptide', 'turn\nEETTE', (111.2, 116.7, 123.5)), ('A', '824', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\n-SSSE', (94.3, 87.8, 117.0)), ('A', '845', 'ASP', 'check CA trace,carbonyls, peptide', ' \nEE-SS', (110.4, 109.8, 148.6)), ('A', '151', 'CYS', 'check CA trace', 'bend\nTTSS-', (147.8, 125.4, 117.7)), ('A', '326', 'PHE', 'check CA trace', 'bend\nGGSEE', (125.2, 143.5, 128.8)), ('A', '504', 'PHE', 'check CA trace', 'turn\n--TTG', (112.6, 134.5, 143.0)), ('A', '678', 'GLY', 'check CA trace', 'bend\n--S--', (122.3, 130.3, 127.8)), ('A', '733', 'ARG', 'check CA trace', 'bend\nHSS--', (121.1, 132.0, 95.9)), ('C', '65', 'ALA', 'check CA trace', 'bend\nSSSS-', (123.9, 109.3, 169.3)), ('B', '99', 'ASP', 'check CA trace,carbonyls, peptide', ' \nTT-SH', (121.6, 155.3, 147.9)), ('B', '111', 'ARG', 'check CA trace,carbonyls, peptide', 'bend\nTSSSS', (124.6, 159.4, 128.5)), ('B', '112', 'ASP', 'check CA trace,carbonyls, peptide', 'bend\nSSSSE', (121.1, 160.1, 129.9)), ('B', '151', 'SER', 'check CA trace,carbonyls, peptide', 'bend\n-SSS-', (139.9, 148.5, 141.1)), ('B', '182', 'TRP', 'check CA trace', 'bend\nS-S-E', (136.1, 124.7, 153.4))]
data['smoc'] = [('A', 40, u'ASP', 0.8079739145572987, (124.553, 123.14, 85.24600000000001)), ('A', 44, u'GLY', 0.7340965508628196, (127.024, 121.301, 96.61)), ('A', 69, u'TYR', 0.7426080690487253, (153.20299999999997, 125.169, 97.866)), ('A', 84, u'GLU', 0.7729565660895305, (145.9, 136.395, 82.393)), ('A', 90, u'LEU', 0.7623505591288989, (143.82000000000002, 142.444, 89.812)), ('A', 116, u'ARG', 0.778522360406929, (150.583, 130.146, 91.31400000000001)), ('A', 117, u'GLN', 0.7352548293961194, (153.16, 130.553, 94.062)), ('A', 125, u'ALA', 0.6923652303774518, (137.47299999999998, 124.955, 102.17299999999999)), ('A', 139, u'CYS', 0.6983377350990861, (139.654, 113.37499999999999, 110.8)), ('A', 143, u'LYS', 0.6818898744053482, (144.72, 117.118, 113.007)), ('A', 152, u'CYS', 0.7245190495597245, (148.86100000000002, 122.203, 119.501)), ('A', 171, u'ILE', 0.7242252834941709, (140.484, 121.867, 122.87799999999999)), ('A', 185, u'ALA', 0.681837792710537, (142.007, 135.82000000000002, 105.932)), ('A', 189, u'THR', 0.7252789352352828, (138.85500000000002, 138.94299999999998, 101.67699999999999)), ('A', 196, u'MET', 0.7033015501782637, (137.24599999999998, 143.727, 92.12499999999999)), ('A', 200, u'GLY', 0.6067741342221981, (135.23899999999998, 146.04299999999998, 87.143)), ('A', 201, u'ILE', 0.6171077344562718, (135.208, 142.312, 87.90400000000001)), ('A', 214, u'GLY', 0.6716059433236301, (144.781, 134.48700000000002, 103.05199999999999)), ('A', 218, u'ASP', 0.682849670844906, (141.923, 130.95600000000002, 90.198)), ('A', 236, u'SER', 0.6523747464330389, (128.472, 130.977, 99.962)), ('A', 237, u'TYR', 0.7046130018403433, (131.92700000000002, 132.062, 101.16799999999999)), ('A', 259, u'THR', 0.7809433680357611, (143.646, 145.497, 117.478)), ('A', 291, u'ASP', 0.7483280513905441, (124.85799999999999, 142.68, 100.381)), ('A', 293, u'THR', 0.8406060615339869, (121.085, 145.678, 105.337)), ('A', 308, u'LEU', 0.7687225203856909, (117.689, 135.88500000000002, 112.669)), ('A', 331, u'ARG', 0.6899879928052628, (117.912, 154.14399999999998, 135.502)), ('A', 350, u'GLU', 0.6796421618311855, (122.01400000000001, 138.70499999999998, 120.23700000000001)), ('A', 352, u'GLY', 0.6989384454029056, (121.44600000000001, 144.635, 120.643)), ('A', 357, u'GLN', 0.7461309592805738, (108.68599999999999, 152.407, 125.67199999999998)), ('A', 358, u'ASP', 0.6383605911977137, (106.49400000000001, 152.93200000000002, 128.76299999999998)), ('A', 362, u'HIS', 0.7038517640465404, (107.651, 160.937, 139.137)), ('A', 366, u'LEU', 0.7289537101992489, (102.084, 151.959, 142.20899999999997)), ('A', 369, u'LYS', 0.7060905741723917, (101.10199999999999, 144.997, 138.054)), ('A', 376, u'ALA', 0.7399402531682094, (110.792, 140.74699999999999, 139.583)), ('A', 387, u'LEU', 0.7230036476294684, (129.271, 142.61399999999998, 145.768)), ('A', 393, u'THR', 0.6730449888709573, (132.61599999999999, 128.877, 139.39800000000002)), ('A', 419, u'PHE', 0.6830723363927494, (108.187, 95.393, 149.618)), ('A', 428, u'PHE', 0.7069660833882452, (113.76700000000001, 87.763, 143.568)), ('A', 437, u'LEU', 0.664766611705823, (117.99000000000001, 96.99100000000001, 141.88700000000003)), ('A', 459, u'ASN', 0.768078530403413, (127.193, 126.953, 126.689)), ('A', 475, u'VAL', 0.7557140263095469, (111.329, 123.49300000000001, 106.319)), ('A', 486, u'GLY', 0.7769447819686613, (97.708, 132.70399999999998, 117.877)), ('A', 490, u'ALA', 0.7720008971210189, (93.612, 135.759, 129.843)), ('A', 496, u'ASN', 0.73376604217969, (98.38, 123.20400000000001, 134.915)), ('A', 502, u'ALA', 0.7495803154881712, (106.938, 131.097, 141.227)), ('A', 525, u'ASP', 0.665392986057447, (95.87199999999999, 141.476, 129.961)), ('A', 532, u'LYS', 0.7589605987021839, (104.418, 143.35000000000002, 124.076)), ('A', 536, u'ILE', 0.7369744287694621, (110.94400000000002, 142.48800000000003, 131.846)), ('A', 538, u'THR', 0.6692325696738504, (112.91300000000001, 138.43800000000002, 135.42700000000002)), ('A', 539, u'ILE', 0.7267832506765491, (114.818, 136.15200000000002, 137.81)), ('A', 568, u'ASN', 0.7191049951590855, (104.485, 132.937, 127.921)), ('A', 569, u'ARG', 0.7252262941440641, (101.27199999999999, 130.97899999999998, 128.46800000000002)), ('A', 578, u'SER', 0.7851135384834157, (96.94600000000001, 122.3, 119.24300000000001)), ('A', 603, u'LYS', 0.7464034453918318, (102.70100000000001, 102.229, 112.224)), ('A', 608, u'ASP', 0.7621053829936109, (105.27799999999999, 104.21400000000001, 103.535)), ('A', 611, u'ASN', 0.7337695762571994, (113.363, 100.12499999999999, 102.57499999999999)), ('A', 615, u'MET', 0.7727867169713043, (117.504, 104.877, 114.038)), ('A', 630, u'LEU', 0.7719726155899937, (118.98700000000001, 128.025, 117.603)), ('A', 633, u'MET', 0.7860137220129316, (115.146, 130.266, 115.843)), ('A', 655, u'LEU', 0.7543367168472126, (110.973, 137.61399999999998, 121.452)), ('A', 658, u'GLU', 0.7145258578640898, (111.539, 135.595, 126.202)), ('A', 673, u'LEU', 0.7294748852547058, (122.60499999999999, 136.117, 141.73899999999998)), ('A', 696, u'ILE', 0.6750755481596583, (113.642, 118.88799999999999, 113.815)), ('A', 703, u'ASN', 0.7677672930189035, (119.631, 115.89, 105.763)), ('A', 708, u'LEU', 0.7683381035831935, (124.82799999999999, 118.436, 99.543)), ('A', 721, u'ARG', 0.7618973449882878, (120.242, 115.027, 91.49600000000001)), ('A', 729, u'GLU', 0.7300929954763327, (120.11999999999999, 127.18599999999999, 94.273)), ('A', 744, u'GLU', 0.7699938362293803, (109.15599999999999, 119.561, 97.394)), ('A', 750, u'ARG', 0.7926944419976154, (108.304, 112.774, 104.57799999999999)), ('A', 756, u'MET', 0.7125362771131137, (108.795, 110.65499999999999, 115.43900000000001)), ('A', 759, u'SER', 0.7111468577918978, (111.18599999999999, 116.71000000000001, 123.472)), ('A', 760, u'ASP', 0.6693738778461363, (114.846, 116.10799999999999, 122.49400000000001)), ('A', 768, u'SER', 0.7502704975164504, (118.099, 102.364, 104.003)), ('A', 785, u'VAL', 0.6932939960171645, (126.046, 118.616, 112.77199999999999)), ('A', 802, u'GLU', 0.7738371593493351, (117.502, 98.592, 114.12299999999999)), ('A', 826, u'TYR', 0.606878911222019, (99.971, 91.581, 116.15599999999999)), ('A', 836, u'ARG', 0.6787657209535373, (113.897, 100.84100000000001, 137.266)), ('A', 837, u'ILE', 0.7227880841786168, (110.41400000000002, 99.77, 138.347)), ('A', 848, u'VAL', 0.7299942571563234, (103.395, 108.03, 151.195)), ('A', 858, u'ARG', 0.694613026536675, (102.15499999999999, 104.468, 143.127)), ('A', 865, u'ASP', 0.6691691437611368, (103.777, 100.356, 133.57)), ('A', 879, u'ASP', 0.8133920435257724, (107.577, 87.436, 137.379)), ('A', 882, u'HIS', 0.7508096980170996, (103.1, 88.93700000000001, 138.942)), ('A', 889, u'ARG', 0.7214281947705306, (96.44100000000002, 92.474, 146.265)), ('A', 894, u'GLU', 0.7489783417388526, (95.21400000000001, 95.786, 154.122)), ('A', 932, u'GLN', 0.6193897962310427, (90.405, 106.71100000000001, 130.73)), ('C', 26, u'SER', 0.7409811257572594, (130.07, 119.90700000000001, 156.333)), ('C', 32, u'CYS', 0.662062299637712, (129.2, 110.187, 154.64499999999998)), ('C', 49, u'PHE', 0.7323652080443024, (131.141, 95.689, 153.138)), ('D', 87, u'MET', 0.7355919390495157, (114.715, 103.35, 162.732)), ('D', 114, u'CYS', 0.5204105551722358, (135.155, 100.292, 173.165)), ('D', 115, u'VAL', 0.6023110018830329, (134.37800000000001, 102.636, 170.271)), ('B', 80, u'ARG', 0.7599067073146852, (96.533, 140.123, 147.31)), ('B', 87, u'MET', 0.7487324221222013, (106.55799999999999, 143.33100000000002, 147.996)), ('B', 103, u'LEU', 0.6687641628948516, (125.651, 155.463, 143.32200000000003)), ('B', 107, u'ILE', 0.7376935697016362, (124.783, 157.254, 137.475)), ('B', 111, u'ARG', 0.7141406650448737, (124.569, 159.39000000000001, 128.45600000000002)), ('B', 128, u'LEU', 0.6634657489684279, (132.691, 142.189, 149.26999999999998)), ('B', 142, u'CYS', 0.6775076793160222, (142.43200000000002, 137.094, 149.931)), ('B', 158, u'GLN', 0.6833458646909009, (135.429, 138.18800000000002, 159.202)), ('B', 161, u'ASP', 0.7071937545177316, (133.64, 128.567, 157.015))]
handle_read_draw_probe_dots_unformatted("/home/ccpem/agnel/gisaid/countries_seq/structure_data/emdb/EMD-30127/6m71/Model_validation_1/validation_cootdata/molprobity_probe6m71_0.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
