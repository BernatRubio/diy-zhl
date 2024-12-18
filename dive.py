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
        self._N = 0.79
        self._He = 0.79 - self._N
        self._RQ = 1.0
        self._GFHi = 0.8
        self._GFLo = 0.3
        self._GF = self._GFLo
        self._TCs = []
        self._FSD = None
        self._Deco_Stops = []

# starting Pt (same for all TCs)
        sp = diyzhl.palv( Pamb = self._P, Q = 0.79, RQ = self._RQ )

# use ZH-L16Cb (skip over 4-minute TC)
        for tc in diyzhl.ZHL16N.keys() :
            if tc == 1 : continue
            self._TCs.append( { 
                'n': { 
                    "t" : diyzhl.ZHL16N[tc]["t"], 
                    "a" : diyzhl.ZHL16N[tc]["a"]["C"],
                    "b" : diyzhl.ZHL16N[tc]["b"],
                    "P" : sp
                },
                
                'h': {
                    "t" : diyzhl.ZHL16He[tc]["t"], 
                    "a" : diyzhl.ZHL16He[tc]["a"]["B"],
                    "b" : diyzhl.ZHL16He[tc]["b"],
                    "P" : 0
                }
            } )

# init. ceiling
        for i in range( len( self._TCs ) ) :
            self._TCs[i]["C"] = diyzhl.buhlmann( Pn = self._TCs[i]["n"]["P"],
                                         an = self._TCs[i]["n"]["a"],
                                         bn = self._TCs[i]["n"]["b"],
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
        assert float( newdepth ) >= 0.0
        if float( newdepth ) == 0.0 :
            newP = self._S
        else :
            newP = round( self._S + float( newdepth ), 1 )
        t = self._time( newtimestr ) - self._T
    
        for i in range( len( self._TCs ) ) :
            pn = diyzhl.schreiner( Pi = self._TCs[i]["n"]["P"], 
                          Palv = diyzhl.palv( Pamb = newP, Q = self._N, RQ = self._RQ ), 
                          t = t, 
                          R = diyzhl.arr( d0 = self._P, dt = newP, t = t, Q = self._N ),
                          k = diyzhl.kay( Th = self._TCs[i]["n"]["t"] ) )
            
            self._TCs[i]["n"]["P"] = pn
            
            ph = diyzhl.schreiner( Pi = self._TCs[i]["h"]["P"], 
                          Palv = diyzhl.palv( Pamb = newP, Q = self._He, RQ = self._RQ ), 
                          t = t, 
                          R = diyzhl.arr( d0 = self._P, dt = newP, t = t, Q = self._He ),
                          k = diyzhl.kay( Th = self._TCs[i]["h"]["t"] ) )
            
            self._TCs[i]["h"]["P"] = ph
             
            self._TCs[i]["C"] = diyzhl.buhlmann( Pn = self._TCs[i]["n"]["P"],
                                         an = self._TCs[i]["n"]["a"],
                                         bn = self._TCs[i]["n"]["b"],
                                         Phe = self._TCs[i]["h"]["P"],
                                         ahe = self._TCs[i]["h"]["a"],
                                         bhe = self._TCs[i]["h"]["b"],
                                         gf = self._GF )

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
        step_time = 0.25
        obj_minutes = int(tmp_object._T)
        obj_seconds = int((tmp_object._T % 1) * 60)
        
        while True:
            step+=15
            iter_minutes = int(step / 60)
            iter_seconds = step % 60
            pressure = tmp_object._P - tmp_object._S
            
            if (iter_minutes >= 100):
                return 100
            
            tmp_object.segment(pressure + (rate*step_time), f"{obj_minutes + iter_minutes}:{obj_seconds + iter_seconds}")
            
            for ceiling in tmp_object.ceilings:
                if ceiling > 1:
                    exit_while = True
                    break
            if exit_while:
                break
        return ((step - 15) / 60.0)
    
    def safety_stop(self):
        import math
        max_ceiling = max(self.ceilings)
        deco_stops = self._Deco_Stops
        final_stop_depth = 1.0
        surface_pressure = 1.0
        
        # Adjust max_ceiling to the closest multiple of 0.3 from 1.3 upwards
        # Ensure that the smallest possible value is 1.3 (i.e., the base multiple)
        if max_ceiling <= surface_pressure:
            max_ceiling = surface_pressure
        else:
            max_ceiling = math.ceil((max_ceiling - 1.3) / 0.3) * 0.3 + 1.3
        
        max_ceiling = round(max_ceiling, 2)  # Ensure precision to two decimal places
        
        if (self._P <= max_ceiling):
            if max_ceiling not in self._Deco_Stops and max_ceiling != 1.0:
                self._Deco_Stops.append(max_ceiling)
            
            first_stop_depth = deco_stops[0]
            gf_slope = (self._GFHi - self._GFLo) / (final_stop_depth - first_stop_depth)
            gf = (gf_slope * (max_ceiling - final_stop_depth)) + self._GFHi
            self._GF = round(gf,3)
        
        return max_ceiling




