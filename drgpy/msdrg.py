
import drgpy._mdcsrdr as mdcsrdr
import drgpy._appndxrdr as appndxrdr
import drgpy._mdcs0007 as mdcs0007
from collections import defaultdict
from collections import Counter

class DRGEngine:

    def __init__(self):
        dxmap = defaultdict(list)
        prmap = defaultdict(list)
        dxmap, prmap = mdcsrdr.read("data/mdcs_00_07.txt", dxmap, prmap)
        dxmap, prmap = mdcsrdr.read("data/mdcs_08_11.txt", dxmap, prmap)
        dxmap, prmap = mdcsrdr.read("data/mdcs_12_21.txt", dxmap, prmap)
        dxmap, prmap = mdcsrdr.read("data/mdcs_22_25.txt", dxmap, prmap)
        self.dxmap = dxmap
        self.prmap = prmap
        
        ccmap, exmap = appndxrdr.read_c()
        self.ccmap = ccmap
        self.exmap = exmap

        orpcsmap = appndxrdr.read_e()
        self.orpcsmap = orpcsmap

        uormap = appndxrdr.read_f()
        self.uormap = uormap

    def get_features(self, dx_lst, pr_lst):

        x = [] # MDC, DRG, etc.
        z = [] # CC/MCC
       
        if len(dx_lst) > 0:
            # dx_lst[0]: primary/principal diagnosis
            # dx_lst[1:]: secondary diagnoses
            pdx = dx_lst[0]
            for j, dx in enumerate(dx_lst):
                is_pdx = j==0
                for x_i in self.dxmap[dx]:
                    if is_pdx:
                        if ("PDX" in x_i or 
                            "PSDX" in x_i or 
                            "_MDC" in x_i):
                            x.append(x_i)
                    else:
                        if ("PDX" not in x_i and 
                            "_MDC" not in x_i):
                            x.append(x_i)
                if dx in self.ccmap and not is_pdx:
                    cc_info = self.ccmap[dx]
                    if pdx not in self.exmap[cc_info["pdx"]]:
                        x.append("_" + cc_info["level"])

        for pr in pr_lst:
            for x_i in self.prmap[pr]:
                tokens = x_i.split("|")
                if len(tokens) > 2:
                    if tokens[2] in pr_lst:
                        x.append(tokens[0] + "|" + tokens[1])
                else:
                    x.append(x_i)
                
            if pr in self.orpcsmap:
                x.append("_ORPCS")
            if pr in self.uormap:
                x.append("_UNREALTED_ORPCS")
    
        # TODO: need to identify if the patient is live at discharge
        # For now, we just assume all patients are alive
        x.append("_ALIVE")

        return Counter(x)

    def get_drg_all(self, dx_lst, pr_lst):

        y = []
        x = self.get_features(dx_lst, pr_lst)
        y += mdcs0007.mdc00(x)
        y += mdcs0007.mdc01(x)
        y += mdcs0007.mdc02(x)
        y += mdcs0007.mdc03(x)
        y += mdcs0007.mdc04(x)
        y += mdcs0007.mdc05(x)
        y += mdcs0007.mdc06(x)
        y += mdcs0007.mdc07(x)

        return y
        
         


    





