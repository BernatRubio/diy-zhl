import pprint
import re

import diyzhl

class Dive( object ) :
    
    # ctor
    #
    def __init__( self, verbose = False ) :

        self._verbose = bool( verbose )
        self._timepat = re.compile( r"(\d{1,3}):(\d{1,2})" )
        
# air, sea level, USN RQ. S is surface pressure (const), P is current pressure (var)
        self._T = 0
        self._S = 1.0
        self._P = self._S
        self._Q = 0.79
        self._RQ = 1.0
        self._GFHi = 0.8
        self._GFLo = 0.3
        self._TCs = []
        self._FSD = None

# starting Pt (same for all TCs)
        sp = diyzhl.palv( Pamb = self._P, Q = self._Q, RQ = self._RQ )

# use ZH-L16Cb (skip over 4-minute TC)
        for tc in diyzhl.ZHL16N.keys() :
            if tc == 1 : continue
            self._TCs.append( { 
                "t" : diyzhl.ZHL16N[tc]["t"], 
                "a" : diyzhl.ZHL16N[tc]["a"]["C"],
                "b" : diyzhl.ZHL16N[tc]["b"],
                "P" : sp
            } )

# init. ceiling
        for i in range( len( self._TCs ) ) :
            self._TCs[i]["F"] = diyzhl.buhlmann( Pn = self._TCs[i]["P"],
                                        an = self._TCs[i]["a"],
                                        bn = self._TCs[i]["b"],
                                        gf = self._GFLo )
        for i in range( len( self._TCs ) ) :
            self._TCs[i]["C"] = diyzhl.buhlmann( Pn = self._TCs[i]["P"],
                                         an = self._TCs[i]["a"],
                                         bn = self._TCs[i]["b"],
                                         gf = self._GFLo )
            
        if self._verbose :
            pprint.pprint( self._TCs )
            
    # helpers for plotting
    # (could actually do this in a more "pythonic" way but this is more obvious)
    #
    @property
    def compartments( self ) :
        rc = []
        for i in range( len( self._TCs ) ) :
            rc.append( self._TCs[i]["t"] )
        return rc
    
    @property
    def loadings( self ) :
        rc = []
        for i in range( len( self._TCs ) ) :
            rc.append( self._TCs[i]["P"] )
        return rc
    
    @property
    def ceilings( self ) :
        rc = []
        for i in range( len( self._TCs ) ) :
            rc.append( self._TCs[i]["C"] )
        return rc
    
    @property
    def fsd( self ) :
        rc = []
        for i in range( len( self._TCs ) ) :
            rc.append( self._TCs[i]["F"] )
        fsd = self._FSD
        if fsd:
            if fsd <= self._P:
                rc = max(rc)
                self._FSD = rc
            elif fsd > self._P:
                return fsd
        else:
            rc = max(rc)
            self._FSD = rc
        return rc

    # helper function: takes human-readable time string like "1:30" and returns minutes: 1.5
    #
    def _time( self, t = "0:0" ) :
        if t is None : return 0
        m = self._timepat.search( str( t ).strip() )
        if not m : raise Exception( "Invalid time string %s" % (t,) )
        rc = 0.0
        rc += float( m.group( 1 ) )
        rc += float( m.group( 2 ) ) / 60.0
        return round( rc, 1 )

    # newdepth is new depth in bar
    # timestr is time as [hours:]minutes:seconds string. *it is the total elapsed* time
    #
    def segment( self, newdepth = 0.0, newtimestr = "1:0" ) :
        FINAL_STOP_DEPTH = 1.0 # In atm
        SURFACE_PRESSURE = 1.0
        assert float( newdepth ) >= 0.0
        if float( newdepth ) == 0.0 :
            newP = self._S
        else :
            newP = round( self._S + float( newdepth ), 1 )
        t = self._time( newtimestr ) - self._T
    
        for i in range( len( self._TCs ) ) :
            p = diyzhl.schreiner( Pi = self._TCs[i]["P"], 
                          Palv = diyzhl.palv( Pamb = newP, Q = self._Q, RQ = self._RQ ), 
                          t = t, 
                          R = diyzhl.arr( d0 = self._P, dt = newP, t = t, Q = self._Q ),
                          k = diyzhl.kay( Th = self._TCs[i]["t"] ) )
            self._TCs[i]["P"] = p
            
            if newP >= self._TCs[i]["F"]:
                self._TCs[i]["F"] = diyzhl.buhlmann( Pn = self._TCs[i]["P"],
                                            an = self._TCs[i]["a"],
                                            bn = self._TCs[i]["b"],
                                            gf = self._GFLo )
            gf_slope = (self._GFHi - self._GFLo) / (FINAL_STOP_DEPTH - self.fsd)
            val = self.fsd
            gf = (gf_slope * (newP - SURFACE_PRESSURE)) + self._GFHi
            gf = gf if gf > self._GFLo else self._GFLo
            #print(f"Gradient factor at depth {newP} with fsd {val}: {gf}") 
            self._TCs[i]["C"] = diyzhl.buhlmann( Pn = self._TCs[i]["P"],
                                         an = self._TCs[i]["a"],
                                         bn = self._TCs[i]["b"],
                                         gf = gf )

        self._P = newP
        self._T += t
    
        if self._verbose :
            import sys
            sys.stdout.write( "* At time %f, P %f:\n" % (self._T, self._P,) )
            pprint.pprint( self._TCs )
    
    def ndl(self, rate):
        import copy
        tmp_object = copy.deepcopy(self)
        exit_while = False
        iter_minutes = 0
        iter_seconds = 0
        step = 0
        obj_minutes = int(tmp_object._T)
        obj_seconds = int((tmp_object._T % 1) * 60)
        
        while True:
            step+=15
            iter_minutes = int(step / 60)
            iter_seconds = step % 60
            pressure = tmp_object._P - tmp_object._S
            # print(f"minutes: {iter_minutes}")
            # print(f"seconds: {iter_seconds}")
            
            if (iter_minutes >= 100):
                return 100
            
            tmp_object.segment(pressure + rate*0.2, f"{obj_minutes + iter_minutes}:{obj_seconds + iter_seconds}")
            
            for ceiling in tmp_object.ceilings:
                if ceiling > 1:
                    exit_while = True
                    break
            if exit_while:
                break
        return ((step - 15) / 60.0)
    
    def safety_stop(self):
        import math
        print(self.ceilings)
        max_ceiling = max(self.ceilings)
        
        # Adjust max_ceiling to the closest multiple of 0.3 from 1.3 upwards
        # Ensure that the smallest possible value is 1.3 (i.e., the base multiple)
        if max_ceiling < 1.3:
            max_ceiling = 1.3
        else:
            max_ceiling = math.ceil((max_ceiling - 1.3) / 0.3) * 0.3 + 1.3
        
        max_ceiling = round(max_ceiling, 2)  # Ensure precision to two decimal places
        
        return max_ceiling




