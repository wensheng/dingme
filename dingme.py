# Wensheng Wang @2018

# run pep8 with:
#   "flake8 --max-line-length=100 dingme.py"

import sys
import os

import wx
import wx.adv


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(350, 300),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetBackgroundColour('white')

        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.counter = 0
        self.alarmed = 0
        self.counting = False

        self.sound = wx.adv.Sound(resource_path("winForeground.wav"))

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(resource_path("alarm.ico"), wx.BITMAP_TYPE_ICO))
        self.SetIcon(icon)

        panel = wx.Panel(self, -1)
        title = wx.StaticText(panel, -1, "Ding Me", pos=(105, 10))
        title.SetFont(wx.Font(24, wx.DECORATIVE, wx.NORMAL, wx.BOLD))

        self.m5Button = wx.Button(panel, 1, '5 Min.', size=(55, 28), pos=(35, 65))
        self.m10Button = wx.Button(panel, 2, '10 Min.', size=(55, 28), pos=(105, 65))
        self.m25Button = wx.Button(panel, 3, '25 Min.', size=(55, 28), pos=(175, 65))
        self.m60Button = wx.Button(panel, 4, '60 Min.', size=(55, 28), pos=(245, 65))
        self.Bind(wx.EVT_BUTTON, self.On5, id=1)
        self.Bind(wx.EVT_BUTTON, self.On10, id=2)
        self.Bind(wx.EVT_BUTTON, self.On25, id=3)
        self.Bind(wx.EVT_BUTTON, self.On60, id=4)
        self.txt1 = wx.TextCtrl(panel, size=(80, 40), pos=(130, 100))
        self.txt1.SetFont(wx.Font(24, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        self.txt1.SetValue("25")
        self.txt1.SetFocus()

        self.doButton = wx.Button(panel, 5, 'SET', (126, 160))
        self.Bind(wx.EVT_BUTTON, self.DoIt, id=5)
        self.txt3 = wx.TextCtrl(panel,
                                size=(315, 50),
                                pos=(10, 200),
                                style=wx.TE_READONLY | wx.TE_RICH | wx.BORDER_NONE)
        self.txt3.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.txt3.SetValue("")

    def OnTimer(self, event):
        if not self.counting:
            return

        if self.counter:
            self.counter -= 1
            mins = self.counter // 60
            secs = self.counter % 60
            if mins < 2:
                minu = "minute"
            else:
                minu = "minutes"
            if secs < 2:
                secu = "second"
            else:
                secu = "seconds"
            self.txt3.SetValue("%d %s %d %s" % (mins, minu, secs, secu))
        else:
            self.alarmed += 1
            if self.alarmed % 2:
                self.txt3.SetForegroundColour(wx.RED)
            else:
                self.txt3.SetForegroundColour(wx.BLACK)
            self.txt3.SetValue("Time's up!")
            self.sound.Play()

    def ResetDoButton(self):
        self.doButton.Enable()
        self.deleted = 0

    def On5(self, event):
        self.txt1.SetValue("5")

    def On10(self, event):
        self.txt1.SetValue("10")

    def On25(self, event):
        self.txt1.SetValue("25")

    def On60(self, event):
        self.txt1.SetValue("60")

    def DoIt(self, event):
        self.txt3.SetValue("")
        self.alarmed = 0

        if self.counting:
            self.counter = 0
            self.counting = False
            self.doButton.SetLabel("SET")
            self.m5Button.Enable()
            self.m10Button.Enable()
            self.m25Button.Enable()
            self.m60Button.Enable()
            self.txt1.Enable()
            return

        try:
            self.counter = int(self.txt1.GetValue())
        except ValueError:
            self.counter = 0

        if self.counter <= 0 or self.counter > 9999:
            self.txt3.SetValue("Invalid number of minutes")
            return

        self.counter *= 60
        self.m5Button.Disable()
        self.m10Button.Disable()
        self.m25Button.Disable()
        self.m60Button.Disable()
        self.txt1.Disable()
        self.doButton.SetLabel("STOP")
        self.counting = True


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'dingme')
        frame.Show(True)
        frame.Centre()
        return True


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
