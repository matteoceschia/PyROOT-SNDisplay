import numpy as np
from dataclasses import dataclass
from ROOT import TBox, TText, TLine, TCanvas, TColor, TSystem, TString, gSystem, kRed, kBlack

@dataclass() #yes, I am a lazy n00b
class Calorimeter:
    '''class for calorimeter plotting'''
    #class members
    name = 'n' #ClassVar[TString]
    range_min = 0 #ClassVar[float]
    range_max = 0 #ClassVar[float]
    content = [] #ClassVar[list[float]] #of float
    ombox = [] #ClassVar[list[TBox]] #of TBox
    omtext = [] #ClassVar[list[TText]] #of TText
    source_foil = TLine() #ClassVar[TLine]
    it_label = ''#ClassVar[TText]
    fr_label = '' #ClassVar[TText]
    canvas = None #ClassVar[TCanvas]
    palette_index = 0 #ClassVar[int]
    fiber_map_lines = np.array([TLine])
    ncalo = 712 #ClassVar[int]
    nmwall = 520
    nxwall = 128
    ngveto =  64

    #constructor of calorimeter
    for calo in range(ncalo):
        content.append(0)

    range_min = range_max = -1

    spacerx = 0.0125
    spacery = 0.0250

    mw_sizey = (1-4*spacery)/(13+2)
    gv_sizey = mw_sizey
    xw_sizey = mw_sizey*13./16.

    mw_sizex = (0.5-4*spacerx)/(20+4)
    gv_sizex = mw_sizex*20./16.
    xw_sizex = mw_sizex

    for mw0 in range(2):
        for mw1 in range(20):
            for mw2 in range(13):
                id = mw0*20*13 + mw1*13 + mw2
                x1 = spacerx + 2*xw_sizex + spacerx + 0.5*mw0 + mw_sizex*(mw1)
                if (mw0 == 1):
                    #swap french in case of internal view
                    x1 = spacerx + 2*xw_sizex + spacerx + 0.5*mw0 + mw_sizex*(19-mw1)
                y1 = spacery + gv_sizey + spacery + mw_sizey * mw2
                x2 = x1 + mw_sizex
                y2 = y1 + mw_sizey
                box = TBox(x1, y1, x2, y2)
                box.SetFillColor(0)
                box.SetLineWidth(1)
                ombox.append(box)

                text = TText(x1+0.33*mw_sizex, y1+0.33*mw_sizey, str(id).zfill(3))# "{:10.4f}".format(xid))#, TString::Form("%03d",id))
                text.SetTextSize(0.02)
                omtext.append(text)

    for xw0 in range(2):
        for xw1 in range(2):
            for xw2 in range(2):
                for xw3 in range(16):
                    id = 520 + xw0*2*2*16 + xw1*2*16 + xw2*16 + xw3
                    # x1 = 0
                    if xw0 == 0:
                        if xw1 == 0:
                            x1 = spacerx + xw_sizex*xw2
                        elif xw1 == 1:
                            x1 = spacerx + 2*xw_sizex + spacerx + 20*mw_sizex + spacerx + (1-xw2)*xw_sizex

                    elif xw0 == 1: #wall ID
                        if xw1 == 0: #side ID
                            x1 = 0.5 + spacerx + 2*xw_sizex + spacerx + 20*mw_sizex + spacerx + (1-xw2)*xw_sizex
                        elif xw1 == 1:
                            x1 = 0.5 + spacerx + xw_sizex*xw2

                    x2 = x1 + xw_sizex

                    y1 = spacery + gv_sizey + spacery + xw_sizey*(xw3)
                    y2 = spacery + gv_sizey + spacery + xw_sizey*(xw3+1)

                    box = TBox(x1, y1, x2, y2)
                    box.SetFillColor(0)
                    box.SetLineWidth(1)
                    ombox.append(box)

                    text = TText(x1+0.33*mw_sizex, y1+0.33*mw_sizey, str(id).zfill(3))
                    text.SetTextSize(0.02);
                    omtext.append(text)


    for gv0 in range(2):
        for gv1 in range(2):
            for gv2 in range(16):
                id = 520 + 128 + gv0*2*16 + gv1*16 + gv2
                # x1 = 0
                if gv0 == 0: #side ID 1
                    x1 = spacerx + 2*xw_sizex + spacerx + gv_sizex*gv2

                elif gv0 ==1: #wall ID 0
                    x1 = 0.5 + spacerx + 2*xw_sizex + spacerx + gv_sizex*(16-1-gv2)

                x2 = x1 + gv_sizex
                y1 = spacery + gv1*(gv_sizey + spacery + 13*mw_sizey + spacery)
                y2 = y1 + gv_sizey
                box = TBox(x1, y1, x2, y2)
                box.SetFillColor(0)
                box.SetLineWidth(1)
                ombox.append(box)

                text = TText(x1+0.33*gv_sizex, y1+0.33*gv_sizey, str(id).zfill(3))
                text.SetTextSize(0.02)
                omtext.append(text)

    source_foil = TLine(0.5, spacery, 0.5, 1-spacery)
    source_foil.SetLineWidth(2)

    it_label = TText(spacerx, spacery+gv_sizey+spacery+13*mw_sizey+spacery+0.25*gv_sizey, "ITALY")
    fr_label = TText(0.5+spacerx, spacery+gv_sizey+spacery+13*mw_sizey+spacery+0.25*gv_sizey, "FRANCE")

    it_label.SetTextSize(0.036)
    fr_label.SetTextSize(0.036)

    #fiber map
    line_h_IT = TLine(0.25 - 10*mw_sizex, 2*spacery + 9*mw_sizey, 0.25 + 10*mw_sizex, 2*spacery + 9*mw_sizey)
    line_v_A1A2_IT = TLine(0.25, 2*spacery + 9*mw_sizey, 0.25, 2*spacery + 14*mw_sizey)
    line_v_A3A4_IT = TLine(0.25 - 4*mw_sizex, 2*0.025+mw_sizey, 0.25 - 4*mw_sizex, 2*spacery + 9*mw_sizey)
    line_v_A4A5_IT = TLine(0.25 + 4*mw_sizex, 2*0.025+mw_sizey, 0.25 + 4*mw_sizex, 2*spacery + 9*mw_sizey)

    line_h_FR = TLine(0.75 - 10*mw_sizex, 2*spacery + 9*mw_sizey, 0.75 + 10*mw_sizex, 2*spacery + 9*mw_sizey)
    line_v_A1A2_FR = TLine(0.75, 2*0.025 + 9*mw_sizey, 0.75, 2*spacery + 14*mw_sizey)
    line_v_A3A4_FR = TLine(0.75 - 4*mw_sizex, 2*spacery+mw_sizey, 0.75 - 4*mw_sizex, 2*spacery + 9*mw_sizey)
    line_v_A4A5_FR = TLine(0.75 + 4*mw_sizex, 2*spacery+mw_sizey, 0.75 + 4*mw_sizex, 2*spacery + 9*mw_sizey)

    line_veto_top_IT = TLine(0.25, 3*spacery + 14*mw_sizey, 0.25, 3*spacery + 15*mw_sizey)
    line_veto_bottom_left_IT = TLine(0.25 - 4*gv_sizex, spacery, 0.25 - 4*gv_sizex, spacery+mw_sizey)
    line_veto_bottom_right_IT = TLine(0.25 + 4*gv_sizex, spacery, 0.25 + 4*gv_sizex, spacery+mw_sizey)
    line_veto_top_FR = TLine(0.75, 3*spacery + 14*mw_sizey, 0.75, 3*spacery + 15*mw_sizey)
    line_veto_bottom_left_FR = TLine(0.75 - 4*gv_sizex, spacery, 0.75 - 4*gv_sizex, spacery+mw_sizey)
    line_veto_bottom_right_FR = TLine(0.75 + 4*gv_sizex, spacery, 0.75 + 4*gv_sizex, spacery+mw_sizey)

    line_xw_left_IT = TLine(spacerx, 0.5 + 2*xw_sizey, spacerx+2*xw_sizex, 0.5 + 2*xw_sizey)
    line_xw_right_IT = TLine(0.5 - spacerx - 2*xw_sizex, 0.5 + 2*xw_sizey, 0.5 - spacerx, 0.5+ 2*xw_sizey)
    line_xw_left_FR = TLine(0.5 + spacerx, 0.5 + 2*xw_sizey, 0.5 + spacerx + 2*xw_sizex, 0.5+ 2*xw_sizey)
    line_xw_right_FR = TLine(1 - spacerx - 2*xw_sizex, 0.5 + 2*xw_sizey, 1 - spacerx, 0.5 + 2*xw_sizey)

    fiber_map_lines = np.array([line_h_IT, line_v_A1A2_IT, line_v_A3A4_IT, line_v_A4A5_IT, \
                                     line_h_FR, line_v_A1A2_FR, line_v_A3A4_FR, line_v_A4A5_FR, \
                                     line_veto_top_IT, line_veto_bottom_left_IT, line_veto_bottom_right_IT, \
                                     line_veto_top_FR, line_veto_bottom_left_FR, line_veto_bottom_right_FR, \
                                     line_xw_right_IT, line_xw_left_IT, \
                                     line_xw_right_FR, line_xw_left_FR])

    nRGBs = 6
    stops = np.array([ 0.00, 0.20, 0.40, 0.60, 0.80, 1.00 ])
    red = np.array([ 0.25, 0.00, 0.20, 1.00, 1.00, 0.90 ])
    green = np.array([ 0.25, 0.80, 1.00, 1.00, 0.80, 0.00 ])
    blue = np.array([ 1.00, 1.00, 0.20, 0.00, 0.00, 0.00 ])

    palette_index = TColor.CreateGradientColorTable(nRGBs, stops, red, green, blue, 100)


    def setrange(self, xmin, xmax):
        self.range_min = xmin
        self.range_max = xmax
        return 0


    def draw(self, fiber_map = False):
        if (self.canvas == None):
          self.canvas = TCanvas (self.name, "SuperNEMO calorimeter", 1750, 500)
          self.canvas.SetEditable(True)
          self.canvas.cd()

        for mw0 in range(2):
        	for mw1 in range(20):
        	  for mw2 in range(13):
        	    id = mw0*20*13 + mw1*13 + mw2

        	    self.ombox[id].Draw("l")
        	    self.omtext[id].Draw()

        for xw0 in range(2):
            for xw1 in range(2):
                for xw2 in range(2):
                    for xw3 in range(16):
                        id = 520 + xw0*2*2*16 + xw1*2*16 + xw2*16 + xw3
                        self.ombox[id].Draw("l")
                        self.omtext[id].Draw()

        for gv0 in range(2):
            for gv1 in range(2):
                for gv2 in range(16):
                    id = 520 + 128 + gv0*2*16 + gv1*16 + gv2
                    self.ombox[id].Draw("l")
                    self.omtext[id].Draw()

        self.source_foil.Draw()
        self.it_label.Draw()
        self.fr_label.Draw()

        if fiber_map == True:
            for line in self.fiber_map_lines:
                line.SetLineColor(kBlack)
                line.SetLineStyle(9)
                line.SetLineWidth(3)
                line.Draw()

        self.canvas.SetEditable(False)
        gSystem.ProcessEvents()
        return 0


    def reset(self):
        for calo in range(self.ncalo):
            self.content[calo] = 0
        # for calo=0; calo<self.ncalo; ++calo)
            self.ombox[calo].SetFillColor(0)

        self.canvas.Modified()
        self.canvas.Update()
        gSystem.ProcessEvents()

        return 0

    def setcontent (self, pmt, value):
        self.content[pmt] = value;
        return 0


    def update(self):
        content_min = self.content[0]
        content_max = self.content[0]

        if (self.range_min == -1):
            for calo in range(1, self.ncalo):
                if (self.content[calo] < content_min):
                    content_min = self.content[calo]
                if (self.content[calo] > content_max):
                    content_max = self.content[calo]
        else:
            self.range_min = 0
            content_max = self.range_max

        for calo in range(self.ncalo):
            if (self.content[calo] != 0):
                self.ombox[calo].SetFillColor(self.palette_index + (int)(99*(self.content[calo]-content_min)/(content_max-content_min)))
            else:
                self.ombox[calo].SetFillColor(0)


        self.canvas.Modified()
        self.canvas.Update()
        gSystem.ProcessEvents()
        return 0

    def save_canvas(self):
        self.canvas.SaveAs('sncalorimeter.png')
        return 0

def sndisplay_test():
    sncalo = Calorimeter()

    sncalo.draw(fiber_map=True)

    sncalo.setcontent(0, 0.001)

    for pmt in range(1, 712):
        sncalo.setcontent(pmt, pmt/7.11)

    sncalo.update()

    sncalo.save_canvas()
    return 0

sndisplay_test()
