#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
version 0.1
10 august 2012
Program for LCMSMS data Analysis
"""
#
ICON = """AAABAAEAICAAAAEACACoCAAAFgAAACgAAAAgAAAAQAAAAAEACAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAA4t3sAAAA/wAlJf8AKir/ACIi/wAVD8gASUHbABcX/wASEv8AGxv/ABMT/wAQEP8A
Bgb/AAIC/wAEBP0AFRX/AM6+xAAPD/8ACQn/AP/+/QABAf8AlJT1ACcn/wAEBv8AAADoAA0N/gAI
CP4A+/n2AA0N/wADA/8ABAT/AAYG/gDl1cYA9/f+AAcH/wC6rs8AFBT/AAYG+ACysvwAg4P3AAUF
/wD8/P0AmJX4AIyM/wCQkP8AlJT/AJmZ/wC1s/gAKCr/ACMj8wD+/v8Ai4r9AIqK/wCOjv8AkpL/
AJeX/wCcnP8AoKD/AKWl/wCpqf8Asq/9ACAg/wDj3OMAvbnvAIeH/wCNjf8AkZH/AJWV/wCenv8A
o6P/AKen/wCrq/8AsbH/ALW1/wC5uf8A9vb6AA4O/wCin/UAi4v/AKyp+AC4uP8AvLz/AMHB/wDF
xf8A3dv5AAkJ/gAMCOwAGBj/AAYG+wCbm/8A6OX2AMfH/wDMzP8A0ND/ANzb/ADLxu8Anp7+AP7+
/gDT0/8A2Nj/ANzc/wDn5vwAqJCeAPPw9wCGhv0Ak5P/AJqZ/gCqqv4Ar6//ALOz/wC3t/8A39//
AOPj/wDp6f8A+Pf9AAUF/AAMDP8AmJX2AImJ/wCWlv8A4t/1ALW1/gC6uv8Avr7/AMLC/wDr6/8A
7+//APPz/wC2su8Avrv1AMHB/gDGxv8Aysr/AM7O/wD19f4A9/f/APz8/wDk4fQAj4//AJiY/wCd
nf8A+fj8AM3N/wDS0v8A1tb/ANvb/wCkofYAmpr/AJ+f/wCrq/0A9PL5ANnZ/wDe3v8A4uL/AOfn
/wDa1vMAoqL/ALCw/wC0tP8Avb3/ANnX+ADl5f8A6ur/AO7u/wDy8v8AxML4ALa2/wC/v/8AxMT/
AMnJ/wDv7voA8fH/APb2/wD7+/8A6ej5AMvL/wDV1f8A2tr/APDw/ADo5fsA4OD/APX1/wD6+v8A
/f3/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/
//8AAAAAAAAAAAC4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAApKy2twAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAALS1onKkpQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK+wXrGymZqzAAAA
ADMAAAAAAAAAAAAAAAAAAAAAAKanUqipql2QqwAAAAAArK2uAAAAAAAAAAAAAAAAAJydR0ien1Gg
oQAAAAAAAACio6SlAAAAAAAAAAAAAAAAk3iUlUaWlwAAAAAAAAAAAJiZmpsAAAAAAAAAAAAAAACK
NYtqjI2OAAAAAAAAAAAAj5CRkgAAAAAAAAAAAAAAAAAAgUEsQ0QvggAAAAAAAACDhIWGAAAAAAAA
AIeIiQAAdAkJdQB2d0I3eFp5AAAAAHp7fH0AAAAAAAAAAH5/gABnCQkJCSMzaGlPLWprAAAAbG1u
bwAAAAAAAAAAcHFycwAeCQkJCQkJAgBgQUIAAABhRkdIAAAAAAAAAGJjZGVmAABWCQlXWAkJCQtZ
AAAAADc4WjoAAAAAAAAAW1xdXl8AAAAJCU0AAAIJCQkJAAAATk8tLi9QAAAAAABRUlNUVQAAAAAJ
CSkAAAAAHj4AAAA/AEBBQkNEL0VGR0hJSktMAAAAADEJCSMAAAAAAAAAABAJCTIzNDU2Nzg5Ojs8
PQAAAAAAAA0JCSgAAAAAAAAAEAkJCQkpACorLC0uLzAAAAAAAAAAACYJCQAAAAAAAAAQCQkLCQkJ
CScAAAAAAAAAAAAAAAAAAAkJCQAAAAAAABAJCQsAJCUJCQkAAAAAAAAAIgAAAAAAIwkJDQAAAAAA
EAkJCwAAAAAdCQkCAAAAAAAJIAAAAAAhCQkJAAAAAAAQCQkLAAAAAAAVCQkfAAAAAAwJDAAAABwJ
CQkdAAAAABAJCQsAAAAAAAAeCQkfAAAAABoJCQsOEwkJCQkAAAAAEAkJCwAAAAAAAAAbCQkAAAAA
ABgJCQkJCQkJCQAAAAAQCQkLAAAAAAAAABkJCRIAAAAAAAACCQkJCQkXAAAAABAJCQsAAAAAAAAA
AAkJCQAAAAAAAAAAFAINFQAAAAAAEAkJCwAAAAAAAAAACQkJFgAAAAAAAAAAAAAAAAAAAAAQCQkL
AAAAAAAAAAAJCQkTAAAAAAAAAAAAAAAAAAAAABAJCQsAAAAAAAAAEQkJCRIAAAAAAAAAAAAAAAAA
AAAAAAgJCQkNAAAAAAAOCQkJDwAAAAAAAAAAAAAAAAAAAAAAAAACCQkJCQsMCQkJCQkAAAAAAAAA
AAAAAAAAAAAAAAAAAAAABwgJCQkJCQkJCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAgMEBQYA
AP9////+H////A////APf//AHx//AH8P/wH/D/8B/w//wH8P4wgPD/EABw/wgEcP4MAPD+DjBwPg
8edAAPD/AAH4fwID/H8Af/4/CD++Hw8Pnh8Ph44PD8PADw/j4A8P4fgPD/H+Hw/w//8P8P//D+D/
/4Pg///gAf//+AH///8D"""
#
#
if __name__ == "__main__":
    import wx
    from commons.iconic import MyIconTest

    class MyApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            my_frame = MyIconTest(None, icon=ICON)
            my_frame.Show()
            return 1
    #
    #
    app = MyApp(0)
    app.MainLoop()