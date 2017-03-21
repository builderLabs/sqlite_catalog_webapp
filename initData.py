'''
   Run poopulator.py to populate the instrumentgarage database with 
   an initial set of user and instrument data as provided below.

'''


# --- users -------------------------------------------------------------------

users = {
             "user1" : { 'name' : "jane",  'email' : "janedoe@xyz.com" }
           , "user2" : { 'name' : "joe",   'email' : "joedoe@abc.com" }
           , "user3" : { 'name' : "zack",  'email' : "sandyness@jkl.com" }
           , "user4" : { 'name' : "john",  'email' : "johnbohn@mno.com" }
           , "user5" : { 'name' : "sandy", 'email' : "sandyohara@musicworld.com" }
           , "user6" : { 'name' : "ray",   'email' : "rayplay@horncenter.com" }

        }

# -----------------------------------------------------------------------------


# --- instruments -------------------------------------------------------------

instruments = {

               # ---woodwinds-------------------------------------------------

               "inst1"  : { 
                               'cat'         : "woodwinds"
                             , 'subcat'      : "clarinet"
                             , 'brand'       : "Howarth"
                             , 'model'       : "B22"
                             , 'condition'   : "used"
                             , 'price'       : "$148"
			     , 'picture'     : ""
                             , 'user_id'     : 1
                             , 'description' : 
                               """African black rosewood. Beautiful tone,
                                particularly in the higher registers."""
                          },


               "inst2"  : { 
                               'cat'         : "woodwinds"
			     , 'subcat'      : "flute"
                             , 'brand'       : "Brannen"
                             , 'model'       : "Inigo"
                             , 'condition'   : "new"
                             , 'price'       : "$750"
			     , 'picture'     : ""
                             , 'user_id'     : 5
                             , 'description' : 
                               """Broger flute Drawn Toneholes, A-442, 
                                  B Footjoint with Gizmo."""
                          },


               "inst3"  : { 
                               'cat'         : "woodwinds"
                             , 'subcat'      : "bassoon"
                             , 'brand'       : "Broger"
                             , 'model'       : "Model 214 Topas"
                             , 'condition'   : "new"
                             , 'price'       : "$14,990"
			     , 'picture'     : ""
                             , 'user_id'     : 4
                             , 'description' : 
                               """Professional basis model. Especially easy
                                  response.  Perfect for students or professionals."""
                          },


               "inst4"  : { 
                               'cat'         : "woodwinds"
                             , 'subcat'      : "piccolo"
                             , 'brand'       : "Andoer"
                             , 'model'       : "Ottavino"
                             , 'condition'   : "used"
                             , 'price'       : "$80"
			     , 'picture'     : ""
                             , 'user_id'     : 3
                             , 'description' : 
                               "Key of C. Comes with padded box."
                          },


               # ---brass-----------------------------------------------------

               "inst6"  : { 
                               'cat'         : "brass"
                             , 'subcat'      : "trumpet"
                             , 'brand'       : "Allora"
                             , 'model'       : "AATR-125"
                             , 'condition'   : "new"
                             , 'price'       : "$599.99"
			     , 'picture'     : ""
                             , 'user_id'     : 3
                             , 'description' : 
                               """Classic Silver color, key of Bb. Features a
                                0.460 inch bore with medium-large tapered bell
                                that is well-suited for any type of playing."""
                          },


               "inst7"  : { 
                               'cat'         : "brass"
                             , 'subcat'      : "french horn"
                             , 'brand'       : "Hans Hoyer"
                             , 'model'       : "Heritage 6802"
                             , 'condition'   : "new"
                             , 'price'       : "$5400"
			     , 'picture'     : ""
                             , 'user_id'     : 4
                             , 'description' : 
                               """Key of Bb/F double, string linkage with case and
                                mouthpiece."""
                          },


               "inst8"  : { 
                               'cat'         : "brass"
                             , 'subcat'      : "trumpet"
                             , 'brand'       : "Bach"
                             , 'model'       : "AB190"
                             , 'condition'   : "used"
                             , 'price'       : "$3519"
			     , 'picture'     : ""
                             , 'user_id'     : 1
                             , 'description' : 
                               """One-piece hand-hammered bell with flat rim.
                                Enhanced radius ferrules, two sets of valve 
                                guides (brass and plastic). Extended low F 3rd 
                                valve slide stop rod."""
                          },


               "inst9"  : { 
                               'cat'         : "brass"
                             , 'subcat'      : "trombone"
                             , 'brand'       : "Conn"
                             , 'model'       : "88H Symphony"
                             , 'condition'   : "new"
                             , 'price'       : "$2469"
			     , 'picture'     : ""
                             , 'user_id'     : 4
                             , 'description' : 
                               """Primary bore 0.547 inch with 0.562 inch
                                standard wrap F attachment.  Features an
                                8.5 inch bell."""
                          },


               "inst10" : { 
                               'cat'         : "brass"
                             , 'subcat'      : "tuba"
                             , 'brand'       : "Jupiter"
                             , 'model'       : "JTU700"
                             , 'condition'   : "used"
                             , 'price'       : "$2999"
			     , 'picture'     : ""
                             , 'user_id'     : 6
                             , 'description' : 
                               """Detachable leadpipe, valve body and bell for
                                cleaning/repair, 3/4-size tuba. Perfect for
                                students."""
                          },


               # ---guitars---------------------------------------------------

               "inst11" : { 
                               'cat'         : "guitars"
                             , 'subcat'      : "acoustic"
                             , 'brand'       : "Martin"
                             , 'model'       : "X1D12E-CST"
                             , 'condition'   : "new"
                             , 'price'       : "$599.99"
			     , 'picture'     : ""
                             , 'user_id'     : 2
                             , 'description' : 
                               """Acoustic/electric, 12-string guitar. Features a
                                dreadnought body for to produce a powerful,
                                well-balanced sound."""
                          },


               "inst12" : { 
                               'cat'         : "guitars"
                             , 'subcat'      : "electric"
                             , 'brand'       : "Squire"
                             , 'model'       : "Cyclone"
                             , 'condition'   : "used"
                             , 'price'       : "$240"
			     , 'picture'     : ""
                             , 'user_id'     : 1
                             , 'description' : 
                               "Blue-body electric guitar.  Like new."
                          },


               "inst13" : { 
                               'cat'         : "guitars"
                             , 'subcat'      : "electric"
                             , 'brand'       : "Fender"
                             , 'model'       : "Fender Special Edition Stratocaster"
                             , 'condition'   : "new"
                             , 'price'       : "$499.99"
			     , 'picture'     : ""
                             , 'user_id'     : 6
                             , 'description' : 
                               """Alder body with C-shape maple neck and 25.5 in
                                scale. Rosewood fretboard. Case not included."""
                          },


               "inst14" : { 
                               'cat'         : "guitars"
                             , 'subcat'      : "electric"
                             , 'brand'       : "Gibson"
                             , 'model'       : "Les Paul Deluxe IV Electric"
                             , 'condition'   : "new"
                             , 'price'       : "$1199.99"
			     , 'picture'     : ""
                             , 'user_id'     : 5
                             , 'description' : 
                               """Comes with a Burstbucker 2 Humbucker in the neck
                                position and a Burstbucker 3 Humbucker in the 
                                bridge position. Also handed down from the 
                                Trad Pro IV are the individual coil-splits for
                                each pickup and the 10dB boost. Ice tea color."""
                          },


               # ---percussion------------------------------------------------

               "inst15" : { 
                               'cat'         : "percussion"
                             , 'subcat'      : "drumkit" 
                             , 'brand'       : "Pearl"
                             , 'model'       : "Export Standard 5-Piece"
                             , 'condition'   : "new"
                             , 'price'       : "$649.00"
			     , 'picture'     : ""
                             , 'user_id'     : 1
                             , 'description' : 
                               """Blended poplar and asian mahogany shells.
                                Comes with snare, 3 toms and a bass drum and
                                hi-hat, ride, and crash cymbals."""
                          },

               "inst16" : { 
                               'cat'         : "percussion"
                             , 'subcat'      : "drumkit"
                             , 'brand'       : "Alesis"
                             , 'model'       : "DM8 Electric Kit"
                             , 'condition'   : "used"
                             , 'price'       : "$349.99"
			     , 'picture'     : ""
                             , 'user_id'     : 1
                             , 'description' : 
                               """Barely used - like new. Comes with extra bass
                                tom and mountable controller.  Seat not
                                included."""
                          },


               "inst17" : { 
                               'cat'         : "percussion"
                             , 'subcat'      : "drumkit"
                             , 'brand'       : "DW"
                             , 'model'       : "Collector Series 5-Piece"
                             , 'condition'   : "new"
                             , 'price'       : "$4277.00"
			     , 'picture'     : ""
                             , 'user_id'     : 6
                             , 'description' : 
                               """Crested with chrome hardware, flagship DW
                                line. Snare, symbals, hardware not included."""
                          },


               "inst18" : { 
                               'cat'         : "percussion"
                             , 'subcat'      : "timpani"
                             , 'brand'       : "Adams"
                             , 'model'       : "Professional Series Generation II"
                             , 'condition'   : "new"
                             , 'price'       : "$8997.99"
			     , 'picture'     : ""
                             , 'user_id'     : 1
                             , 'description' : 
                               """Set of 4. Fiberglass bowls, patented GEN2
                                action pedals with secure hold and smooth
                                extended pitch range adjustability.
                                Chrome-plated, single-flange steel suspension
                                rings and counter hoops.  Integrated locking 3rd
                                wheel assembly on inside."""
                          },




               # ---keys------------------------------------------------------

               "inst19" : { 
                               'cat'         : "keyboards"
                             , 'subcat'      : "piano"
                             , 'brand'       : "Suzuki"
                             , 'model'       : "SZV-48 Acoustic Piano"
                             , 'condition'   : "new"
                             , 'price'       : "$3995.00"
			     , 'picture'     : ""
                             , 'user_id'     : 2
                             , 'description' : 
                               """Upright 48 in acoustic piano with German-made
                                Roslau strings and 17-ply cross-grained,
                                pressure laminated pinblocks constructed out of 
                                HardRock maple."""
                          },


               "inst20" : { 
                               'cat'         : "keyboards"
                             , 'subcat'      : "organ"
                             , 'brand'       : "Hammond"
                             , 'model'       : "Heritage XK-5 electronic organ"
                             , 'condition'   : "new"
                             , 'price'       : "$3695.00"
			     , 'picture'     : ""
                             , 'user_id'     : 4
                             , 'description' : 
                               """61-keys. Four full sets of harmonic drawbars
                                featuring that vintage Hammond B3 sound.
                                Best digital Leslie emulator on the market.
                                New, enhanced keybed and crisp OLED display
                                which is readable under any lighting 
                                conditions."""
                          },


               "inst21" : { 
                               'cat'         : "keyboards"
                             , 'subcat'      : "synthesizer"
                             , 'brand'       : "Yamaha"
                             , 'model'       : "Montage M88 Synthesizer"
                             , 'condition'   : "new"
                             , 'price'       : "$3299.99"
			     , 'picture'     : ""
                             , 'user_id'     : 4
                             , 'description' : 
                               """88-key, 16-voice full workstation synth with 
                                balanced  hammer action, emulating a real 
                                piano keyboard. Thousands of voices from which 
                                to choose. Comes with vast internal sequencer 
                                memory,USB audio/midi connection, super knob, 
                                and touch screen display."""
                          },


               "inst22" : { 
                               'cat'         : "keyboards"
                             , 'subcat'      : "synthesizer"
                             , 'brand'       : "Korg"
                             , 'model'       : "Triton Taktile MIDI Controller"
                             , 'condition'   : "used"
                             , 'price'       : "$349.99"
			     , 'picture'     : ""
                             , 'user_id'     : 4
                             , 'description' : 
                               "49-key MIDI controller. Barely used - like new!"
                          },


               "inst23" : { 
                               'cat'         : "keyboards"
                             , 'subcat'      : "synthesizer"
                             , 'brand'       : "Roland"
                             , 'model'       : "Juno DS-88 Synthesizer"
                             , 'condition'   : "new"
                             , 'price'       : "$999.00"
			     , 'picture'     : ""
                             , 'user_id'     : 4
                             , 'description' : 
                               """88-key graded hammer action with aftertouch and
                                velocity sensitive keys. Features layering, over
                                1500 voices, 128-note polyphony, USB/MIDI/line
                                inputs and outputs."""
                          },


               "inst24" : { 
                               'cat'         : "keyboards"
                             , 'subcat'      : "synthesizer"
                             , 'brand'       : "Yamaha"
                             , 'model'       : "MOXF8 88-Key Weighted Synth"
                             , 'condition'   : "new"
                             , 'price'       : "$1699.99"
			     , 'picture'     : ""
                             , 'user_id'     : 4
                             , 'description' : 
                               """88-key graded hammer action full-size keyboard.
                                Features 1152 voices, reverb, chorus, delay
                                effects with internal and USB flash port storage."""
                          },


               # ---strings---------------------------------------------------


               "inst25" : { 
                               'cat'         : "strings"
                             , 'subcat'      : "violin"
                             , 'brand'       : "Otto Benjamin"
                             , 'model'       : "ML-300"
                             , 'condition'   : "new"
                             , 'price'       : "$1299.00"
			     , 'picture'     : ""
                             , 'user_id'     : 2
                             , 'description' : 
                               """Select aged-spruce with highly flamed select
                                aged maple and rosewood fittings. Despiau
                                bridge with ebony inlaid purfling.
                                Adario Helicore D strings and Pernambuco bow."""
                          },



               "inst26" : { 
                               'cat'         : "strings"
                             , 'subcat'      : "violin"
                             , 'brand'       : "Stentor"
                             , 'model'       : "Student II"
                             , 'condition'   : "new"
                             , 'price'       : "$199.99"
			     , 'picture'     : ""
                             , 'user_id'     : 2
                             , 'description' : 
                               "Perfect violin for beginning students"
                          },


               "inst27" : { 
                               'cat'         : "strings"
                             , 'subcat'      : "viola"
                             , 'brand'       : "Glaesel"
                             , 'model'       : "VA103E Student"
                             , 'condition'   : "used"
                             , 'price'       : "$950.00"
			     , 'picture'     : ""
                             , 'user_id'     : 2
                             , 'description' : 
                               """Student viola, perfect for beginners.
                                Used - like new."""
                          },


               "inst28" : { 
                               'cat'         : "strings"
                             , 'subcat'      : "cello"
                             , 'brand'       : "Bellafina"
                             , 'model'       : "Prodigy"
                             , 'condition'   : "new"
                             , 'price'       : "$999.99"
			     , 'picture'     : ""
                             , 'user_id'     : 3
                             , 'description' : 
                               """Select wood body. Ships with quality strings.
                                Bow and carry bag included."""
                          },


               "inst29" : { 
                               'cat'        : "strings"
                             , 'subcat'      : "cello"
                             , 'brand'       : "Bellafina"
                             , 'model'       : "Sonata"
                             , 'condition'   : "used"
                             , 'price'       : "$950.00"
			     , 'picture'     : ""
                             , 'user_id'     : 5
                             , 'description' : 
                               """Student viola, perfect for beginners.
                                Used - like new."""
                          },


               "inst30" : { 
                               'cat'         : "strings"
                             , 'subcat'      : "viola"
                             , 'brand'       : "Glaesel"
                             , 'model'       : "VA103E Student"
                             , 'condition'   : "used"
                             , 'price'       : "$950.00"
			     , 'picture'     : ""
                             , 'user_id'     : 5
                             , 'description' : 
                               """Student viola, perfect for beginners.
                                Used - like new."""
                          },




               # ---recording equipment---------------------------------------

               "inst31" : { 
                               'cat'         : "recording"
                             , 'subcat'      : "software"
                             , 'brand'       : "Avid"
                             , 'model'       : "Pro Tools 12.6"
                             , 'condition'   : "new"
                             , 'price'       : "$599.00"
			     , 'picture'     : ""
                             , 'user_id'     : 6
                             , 'description' : 
                               """Full version (ILok2 required, sold separately).
                                Support for 128 audio and 512 instrument tracks.
                                Free software upgrades for one year."""
                          },


               "inst32" : { 
                               'cat'         : "recording"
                             , 'subcat'      : "interface"
                             , 'brand'       : "MOTU"
                             , 'model'       : "UltraLite AVB"
                             , 'condition'   : "new"
                             , 'price'       : "$649.00"
			     , 'picture'     : ""
                             , 'user_id'     : 5
                             , 'description' : 
                               """18 in/out audio interface with DSP mixing,
                                  Wi-Fi control, and AVB audio networking.
                                  Best in class audio quality with a dynamic
                                  range spanning 117dB."""
                          },


               # ---accessories-----------------------------------------------

               "inst33" : { 
                               'cat'         : "accessories"
                             , 'subcat'      : "headphones"
                             , 'brand'       : "AKG"
                             , 'model'       : "K181DJ UE Reference Class"
                             , 'condition'   : "new"
                             , 'price'       : "$119.99"
			     , 'picture'     : ""
                             , 'user_id'     : 1
                             , 'description' : 
                               """Bass boost, detachable coiled cord,
                                  mono/stereo switch for optimum single ear 
                                  monitoring.  Sensitivity of 112 dB SPL/V
                                  with 42 Ohms rated impedance.
                                  Freq bandwidth: 5-30k Hz."""
                          },


               "inst34" : { 
                               'cat'         : "accessories"
                             , 'subcat'      : "microphone"
                             , 'brand'       : "Neumann"
                             , 'model'       : "TLM49 Cardioid Condenser Microphone"
                             , 'condition'   : "new"
                             , 'price'       : "$1699.95"
			     , 'picture'     : ""
                             , 'user_id'     : 2
                             , 'description' : 
                               """Large-diaphragm studio mike from the most
                                  respected and most experienced microphone 
                                  manufacturer. Frequency Range: 20-2OkHz.
                                  Impedance: 50 ohms (1000 ohms loaded).
                                  Signal-to-noise ratio: 71dB.
                                  Invest now in a good mike and avoid future
                                  costs/hassles."""
                          },

          }

# -----------------------------------------------------------------------------
