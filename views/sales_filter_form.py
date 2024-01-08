from tkinter import *
from tkinter import ttk
from customs import *

from tkcalendar import *

from constants import BUTTON_EVENT, DATE_ENTRY_EVENT


class SalesFilterForm(Toplevel):

    def __init__(self, master, root_x, root_y, _filter_succeed_event):
        Toplevel.__init__(self, master)
        self._filter_succeed_event = _filter_succeed_event
        self._de_sff_from = DateEntry(self, date_pattern="dd-mm-yyyy", width=20, state="readonly")
        self._de_sff_to = DateEntry(self, date_pattern="dd-mm-yyyy", width=20, state="readonly", mindate=self._de_sff_from.get_date())
        self._btn_filter = Button(self, text='FILTER')
        self._create_views(master, root_x, root_y)
        self._bind_views()

    def _create_views(self, master, root_x, root_y):
        self.wm_title("Sale Filter")
        self.grid_anchor(CENTER)
        self.wm_geometry(f"+{root_x}+{root_y}")
        self.wm_transient(master)
        self.grab_set()

        Label(self, text='From').pack()
        self._de_sff_from.pack()
        Label(self, text='To').pack()
        self._de_sff_to.pack()
        self._btn_filter.pack()


    def _bind_views(self):
        self._btn_filter.bind(BUTTON_EVENT, self._btn_filter_click_event)
        self._de_sff_from.bind(DATE_ENTRY_EVENT, self._de_sff_from_selection_event)

    def _btn_filter_click_event(self, event):
        self._filter_succeed_event(self._de_sff_from.get(), self._de_sff_to.get())
        self.destroy()

    def _de_sff_from_selection_event(self, event):
        self._de_sff_to['mindate'] = event.widget.get_date()

