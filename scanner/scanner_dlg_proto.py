# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 16 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class icScannerDlgProto
###########################################################################

class icScannerDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Сканирование", pos = wx.DefaultPosition, size = wx.Size( 633,432 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.option_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		option_notebookImageSize = wx.Size( 16,16 )
		option_notebookIndex = 0
		option_notebookImages = wx.ImageList( option_notebookImageSize.GetWidth(), option_notebookImageSize.GetHeight() )
		self.option_notebook.AssignImageList( option_notebookImages )
		self.option_panel = wx.Panel( self.option_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.option_panel.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText8 = wx.StaticText( self.option_panel, wx.ID_ANY, u"Сканнер:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer9.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.scanner_comboBox = wx.adv.BitmapComboBox( parent=self.option_panel, id=wx.ID_ANY, name=wx.EmptyString, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.CB_READONLY )
		self.scanner_comboBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer9.Add( self.scanner_comboBox, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer9, 0, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.option_panel, wx.ID_ANY, u"Источник:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer5.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.source_comboBox = wx.adv.BitmapComboBox( parent=self.option_panel, id=wx.ID_ANY, name=u"Combo!", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.CB_READONLY )
		self.source_comboBox.SetSelection( 0 )
		self.source_comboBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer5.Add( self.source_comboBox, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText14 = wx.StaticText( self.option_panel, wx.ID_ANY, u"Режим сканирования:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		self.m_staticText14.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer17.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.mode_comboBox = wx.adv.BitmapComboBox( parent=self.option_panel, id=wx.ID_ANY, name=u"Combo!", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.CB_READONLY )
		self.mode_comboBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer17.Add( self.mode_comboBox, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer17, 0, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.multiscan_checkBox = wx.CheckBox( self.option_panel, wx.ID_ANY, u"Многостраничное сканирование", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.multiscan_checkBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.multiscan_checkBox, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.preview_checkBox = wx.CheckBox( self.option_panel, wx.ID_ANY, u"Просмотр результата сканирования", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.preview_checkBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer8.Add( self.preview_checkBox, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer8, 0, wx.EXPAND, 5 )
		
		
		self.option_panel.SetSizer( bSizer4 )
		self.option_panel.Layout()
		bSizer4.Fit( self.option_panel )
		self.option_notebook.AddPage( self.option_panel, u"Параметры сканирования", True )
		self.area_panel = wx.Panel( self.option_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer161 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText61 = wx.StaticText( self.area_panel, wx.ID_ANY, u"Размер страницы:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		self.m_staticText61.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer61.Add( self.m_staticText61, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pagesize_comboBox = wx.adv.BitmapComboBox( parent=self.area_panel, id=wx.ID_ANY, name=u"Combo!", pos=wx.DefaultPosition, size=wx.Size( 100,-1 ), style=wx.CB_READONLY )
		self.pagesize_comboBox.SetSelection( 0 )
		self.pagesize_comboBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer61.Add( self.pagesize_comboBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer161.Add( bSizer61, 0, wx.EXPAND, 5 )
		
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmap1 = wx.StaticBitmap( self.area_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_NORMAL_FILE, wx.ART_CMN_DIALOG ), wx.DefaultPosition, wx.Size( 128,128 ), 0 )
		gbSizer1.Add( self.m_bitmap1, wx.GBPosition( 2, 2 ), wx.GBSpan( 2, 2 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.left_spinCtrl = wx.SpinCtrl( self.area_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0 )
		self.left_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.left_spinCtrl, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.left_text = wx.StaticText( self.area_panel, wx.ID_ANY, u"Слева (мм):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.left_text.Wrap( -1 )
		self.left_text.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.left_text, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		self.right_text = wx.StaticText( self.area_panel, wx.ID_ANY, u"Справа (мм):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.right_text.Wrap( -1 )
		self.right_text.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.right_text, wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		self.right_spinCtrl = wx.SpinCtrl( self.area_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0 )
		self.right_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.right_spinCtrl, wx.GBPosition( 3, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		self.top_text = wx.StaticText( self.area_panel, wx.ID_ANY, u"Сверху (мм):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.top_text.Wrap( -1 )
		self.top_text.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.top_text, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.top_spinCtrl = wx.SpinCtrl( self.area_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.top_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.top_spinCtrl, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.area_panel, wx.ID_ANY, u"Снизу (мм):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.m_staticText5, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.bottom_spinCtrl = wx.SpinCtrl( self.area_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.bottom_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		gbSizer1.Add( self.bottom_spinCtrl, wx.GBPosition( 4, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer161.Add( gbSizer1, 1, wx.EXPAND, 5 )
		
		
		self.area_panel.SetSizer( bSizer161 )
		self.area_panel.Layout()
		bSizer161.Fit( self.area_panel )
		self.option_notebook.AddPage( self.area_panel, u"Область сканирования", False )
		self.extend_panel = wx.Panel( self.option_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText12 = wx.StaticText( self.extend_panel, wx.ID_ANY, u"Директория хранения:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		self.m_staticText12.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer15.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.scan_dirPicker = wx.DirPickerCtrl( self.extend_panel, wx.ID_ANY, u"/home/xhermit", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		self.scan_dirPicker.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer15.Add( self.scan_dirPicker, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText13 = wx.StaticText( self.extend_panel, wx.ID_ANY, u"Формат имени файла:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		self.m_staticText13.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer16.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.filename_textCtrl = wx.TextCtrl( self.extend_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.filename_textCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer16.Add( self.filename_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer16, 0, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText6 = wx.StaticText( self.extend_panel, wx.ID_ANY, u"Формат результирующего файла:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_staticText6, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.fileext_comboBox = wx.adv.BitmapComboBox( parent=self.extend_panel, id=wx.ID_ANY, name=u"Combo!", pos=wx.DefaultPosition, size=wx.Size( 100,-1 ), style=wx.CB_READONLY )
		self.fileext_comboBox.SetSelection( 0 )
		self.fileext_comboBox.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.fileext_comboBox, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15 = wx.StaticText( self.extend_panel, wx.ID_ANY, u"Глубина:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		self.m_staticText15.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer19.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.depth_spinCtrl = wx.SpinCtrl( self.extend_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		self.depth_spinCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer19.Add( self.depth_spinCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer19, 0, wx.EXPAND, 5 )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16 = wx.StaticText( self.extend_panel, wx.ID_ANY, u"Инструмент сканирования:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		self.m_staticText16.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer20.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.extern_cmd_textCtrl = wx.TextCtrl( self.extend_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.extern_cmd_textCtrl.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer20.Add( self.extern_cmd_textCtrl, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer14.Add( bSizer20, 0, wx.EXPAND, 5 )
		
		
		self.extend_panel.SetSizer( bSizer14 )
		self.extend_panel.Layout()
		bSizer14.Fit( self.extend_panel )
		self.option_notebook.AddPage( self.extend_panel, u"Дополнительно", False )
		
		bSizer1.Add( self.option_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cancel_button.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer2.Add( self.cancel_button, 0, wx.ALL, 5 )
		
		self.extern_button = wx.Button( self, wx.ID_ANY, u"Инструмент сканирования ...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.extern_button.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer2.Add( self.extern_button, 0, wx.ALL, 5 )
		
		self.ok_button = wx.Button( self, wx.ID_ANY, u"Сканировать", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_button.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer2.Add( self.ok_button, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.onInitDlg )
		self.multiscan_checkBox.Bind( wx.EVT_CHECKBOX, self.onMultiScanCheckBox )
		self.fileext_comboBox.Bind( wx.EVT_COMBOBOX, self.onFileTypeCombobox )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCanceButtonClick )
		self.extern_button.Bind( wx.EVT_BUTTON, self.onExternButtonClick )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onOkButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onInitDlg( self, event ):
		pass
	
	def onMultiScanCheckBox( self, event ):
		pass
	
	def onFileTypeCombobox( self, event ):
		pass
	
	def onCanceButtonClick( self, event ):
		pass
	
	def onExternButtonClick( self, event ):
		pass
	
	def onOkButtonClick( self, event ):
		pass
	

###########################################################################
## Class icLoadSheetsDlgProto
###########################################################################

class icLoadSheetsDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Загрузка листов в лоток", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Подготовьте", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		self.m_staticText14.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer18.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.sheets_spinCtrl = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 1000, 0 )
		self.sheets_spinCtrl.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer18.Add( self.sheets_spinCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"листов", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		self.m_staticText15.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer18.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer17.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"для сканирования.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		self.m_staticText16.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer19.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Загрузите листы в лоток.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		self.m_staticText17.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer19.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer17.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cancel_button.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer20.Add( self.cancel_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.next_button = wx.Button( self, wx.ID_ANY, u"Далее >>", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.next_button.SetDefault() 
		self.next_button.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer20.Add( self.next_button, 0, wx.ALL, 5 )
		
		
		bSizer17.Add( bSizer20, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer17 )
		self.Layout()
		bSizer17.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.next_button.Bind( wx.EVT_BUTTON, self.onNextButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCancelButtonClick( self, event ):
		pass
	
	def onNextButtonClick( self, event ):
		pass
	

###########################################################################
## Class icVerifyScanDlgProto
###########################################################################

class icVerifyScanDlgProto ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Проверка результата сканирования", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer22 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Проверка предварительного результата сканирования", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		self.m_staticText18.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer22.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		
		bSizer21.Add( bSizer22, 1, wx.EXPAND, 5 )
		
		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.preview_button = wx.Button( self, wx.ID_ANY, u"Предварительный просмотр ...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.preview_button.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer23.Add( self.preview_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.rescan_button = wx.Button( self, wx.ID_ANY, u"Пересканировать", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rescan_button.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer23.Add( self.rescan_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cancel_button = wx.Button( self, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cancel_button.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer23.Add( self.cancel_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.next_button = wx.Button( self, wx.ID_ANY, u"Далее >>", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.next_button.SetDefault() 
		self.next_button.SetFont( wx.Font( 14, 74, 90, 90, False, "Sans" ) )
		
		bSizer23.Add( self.next_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer21.Add( bSizer23, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer21 )
		self.Layout()
		bSizer21.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.preview_button.Bind( wx.EVT_BUTTON, self.onPreviewButtonClick )
		self.rescan_button.Bind( wx.EVT_BUTTON, self.onReScanButtonClick )
		self.cancel_button.Bind( wx.EVT_BUTTON, self.onCancelButtonClick )
		self.next_button.Bind( wx.EVT_BUTTON, self.onNextButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onPreviewButtonClick( self, event ):
		pass
	
	def onReScanButtonClick( self, event ):
		pass
	
	def onCancelButtonClick( self, event ):
		pass
	
	def onNextButtonClick( self, event ):
		pass
	

