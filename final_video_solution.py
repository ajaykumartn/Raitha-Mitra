#!/usr/bin/env python3
"""
Final comprehensive solution for creating AI Raitha Mitra demo video.
This creates both the video assets and provides multiple recording options.
"""

import os
import sys
from pathlib import Path
import json
import subprocess

def create_video_assets():
    """Create all necessary assets for the demo video."""
    
    print("🎨 Creating video assets...")
    
    # Create directories
    video_dir = Path("static/videos")
    assets_dir = video_dir / "assets"
    screenshots_dir = assets_dir / "screenshots"
    
    for dir_path in [video_dir, assets_dir, screenshots_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create sample disease images for demo
    create_sample_disease_images()
    
    # Create video storyboard
    create_video_storyboard()
    
    # Create recording instructions
    create_comprehensive_recording_guide()
    
    # Create video metadata
    create_video_metadata()
    
    print("✅ Video assets created successfully!")

def create_sample_disease_images():
    """Create realistic sample disease images for the demo."" main()__":
   ain"__m== __name__ ")

if e}"  - {filprint(f         file():
    file.is_
        if("*"):eo_dir.rglobn vid for file ideos")
   tic/vith("stair = Pa video_d
   reated:") Files c\n📁print("   )
    
 "tssseall a folder for ic/videos/ Check statint("4.   prion")
 l productfessiona for proe guidesivrehenompthe ct("3. Use ")
    priningiate recordimmed for start scriptk  the quiclow Fol print("2.  app.py")
 app: python ur Flask . Start yo("1print:")
     Steps"\n🚀 Nextnt(   
    priscript")
 recording art ick stnt("✅ Quri)
    pnfo"and SEO ita Video metadaint("✅   pre")
  ng guidordisive recmprehenrint("✅ Co    pard")
torybo svideoetailed rint("✅ Dmo")
    pes for deease imagisample dt("✅ S")
    prinated: been crehat'snt("\nW
    pri")Created!age ction PackProduVideo te omple("🎉 Crint0)
    p=" * 5" + "int("\n
    pr)
    rt_script(_staquick  create_ipt
  scrart e quick stat   # Cre    
 ssets()
video_acreate_assets
    ideo all v   # Create  
 " * 50)
   nt("=pri")
     SolutionFinal Video Mitra - tha Rai("🎬 AIprint    
    
"sets."" video as create all ton function""Mai    " main():


def")ript_path}ed: {sccript creatuick start s Qt(f"✅ prin
    
   ript)rite(sc
        f.was f:='utf-8') encoding', , 'wt_pathen(scripth op  wi
  ")_script.mdtarts/quick_stic/video"staath = Path(  script_p 
  
   """ feedback
team forre with Shaw
   - for reviebe uTu Yo privateUpload to- ad**
   *Uploe

3. *te usdia for immeExportreen
   - e sce titld simpl - Add end
  ning anegin  - Trim bt**
 di E2. **Quickts

formae  in multipl Exportn
   -fe locatiog to saincordy re
   - Copate Backup**edi
1. **Imm
ActionsQuick -Recording 
## Postity only
functionalus on core eded
4. Focreen if ne scto recordone rtphUse smater
3.  combine lants andn segmerd i
2. Reco Win+G) (Windows: softwareecordingse screen r1. Ur:
ccual issues otechnic

If ckup Planncy Ba## Emergele

vailabp storage a] Backughting
- [ ood li[ ] Get
- nt quivironmeed
- [ ] Enicpractcript [ ] Sd
- BS configure] Oeady
- [ s rmple image Sa[ ]ing
- app runnk Flas
- [ ] )
dingfore Recorklist (Bel Demo Chec## Fulations"

nt recommendides treatme and prov% accuracye with 94 diseasntifies theI ide   - "A seconds)
 (10w results**
4. **Sho"
 leafffectedf the aoto ophd a t uploauss)
   - "Jcondse (10 mage**e ioad sampl

3. **Upl"s instantlyiseasean detect dFarmers c"
   -  seconds)tection** (5isease de2. **Click d"

tha MitraI Rais A"This inds)
   - 5 secome page** (how ho

1. **Ssting)For Quick Te (mo Scriptecond De

## 30-Sneededs if ust setting Adjality
   - qu audiondeck video ands
   - Chrd 10 seco  - Reco*
 rding**Test Reco. *

4op audio)ure (desktut CaptutpAudio O Add  -e)
  e (microphont Capturd Audio Inpu  - Aden)
 (full screpture play Ca- Add Dis
    new scene - Createudio**
  tart OBS St

3. **SDelete)Ctrl+Shift+ache (   - Clear c:5000
 localhostavigate to)
   - NF11en (crelsome in ful**
   - Chrowser*Open Br``

2. *.py
   `python app``bash
   *
   `p*lask Ap **Start F
1.etup)
 s minutesms (5IteAction  Immediate t

##g Scripordinrt Reck Sta# Quic"
"cript = " 
    s"
   rding.""e recofor immediatrt script quick state a "Crea):
    ""pt(_scrick_starte_qui createfath}")

d{metadata_pted: etadata creaeo m(f"✅ Vid
    printnt=2)
    f, indedata, mp(meta.du        jsons f:
tf-8') aing='u', encodh, 'wmetadata_paten(th op")
    winetadata.jso/video_mosideatic/v"stath = Path(ta_p
    metada   
   }
    }    itions"
  ibxhl eraturiculat ag: "Display "de_shows "tra         
  ,ls"and proposantations  prese"Use ins": aterial  "sales_m    ",
      ouncementst annand producletters wslude in ne"Incing": etail_mark       "em   ],
  ter", "Twit"Instagram"imeo", ms": ["Vplatfory_"secondar           ],
 LinkedIn"Tube", "", "Youebsite["W": tforms"primary_pla     
       ": {on_planutidistrib  " 
             },
      }
             ]
 Farming""#ion", "#Innovatogy", chnol"#Te", ulture", "#Agric, "#AIrming"artFa"#Smgs": [ashta    "h    
        ", instantly!sesp diseat croarmers detecing fhelpy is ow technolog"See h": tiondescrip    "     ",
       h AI 🌱🤖rming wit Fart "Smae":"titl               m": {
 "instagra             },
          
 riculture"]Ag", "#on "#Innovatiming",Far", "#SmartAI", "#ch": ["#AgTe"hashtags              ",
  detection.ease  disntelligentrough i thuce losseslds and redse yiecreamers inng farpi- helha Mitra  AI Raitonal demo ofrofessi"P": on"descripti              on",
  e Detecti Crop DiseasAI-Poweredure: gricult Ae ofe Futur": "Thitle"t          
      din": {  "linke    ,
             }     rming"]
"smart fadisease",  "crop hnology",re", "tectuul", "agricingI", "farm": ["A     "tags         ",
   in action.genceet intelli mark, andmendationst recomentreatmtection,  disease denstant cropee ie! Sgriculturforming atranschnology is how AI tetch ": "Wadescription          "   
   ion",sease Detectp Di Crotionaryevoluemo - Rha Mitra DAI Rait"title": "       
         be": {utu"yo           
 iants": {_varal_media     "soci   
   
       ],"
      ovationltural innicuagr"        ",
     farming  "digital
          riculture",  "AI in ag    
      ing",lth monitorheaop   "cr      app",
    ing farm   "      ogy",
   hnolral tectu"agricul      ",
      ingion farm"precis            ,
culture"agri  "smart 
           ",ctionisease dete d "crop
           ", farming   "AI         s": [
eo_keyword"s         
         },
    "
  : "16:9tio""aspect_ra        
    -120 MB",et": "80e_size_targ     "fil       Mbps",
-10 te": "8"bitra            "AAC",
: rmat"_fodio"au          )",
  H.264MP4 ( " "format":          
 : 30,frame_rate"      "",
      0x1080": "192solution       "re": {
     cal_specschni"te    
     
       
        },   ]        e"
 rfac inte-friendlyUser       "      
   tion",egraeather int    "W      ",
      tuppor-language sulti  "M              nce",
intelligerice  "Market p          ",
     mmendationsecoatment re treivomprehens"C                ",
curacy% ac with 94ime analysiseal-t      "R          tion",
etecisease dowered dI-p      "A       : [
   onstrated"es_demturey_fea"k      
      ts"],asthusinology en, "Technvestors"onals", "Ial professi"Agriculturs", "Farmernce": [audiearget_  "t
          ration)",stpp demonual aingultillish (with mge": "Engangua      "l      ",
nutes4:00 mi "3:30 - ion":  "durat
          gy.",lochnoming te smart farinted ne interesnyod aals, ansional profes agriculturfor farmers,. Perfect telligence inketmar and mmendations,ment recoeattion, trease detecnt crop disth instag winizes farminevolutio Mitra rI Raitha how A"Seeon": scripti "de       emo",
    Detection De op Diseas Critra - Smartha M Rait "AI"title":   {
         o_info":     "vide = {
    metadata
    
    ation."""d configurtadata ano meCreate vide":
    ""ta()ada_metreate_videof ch}")

dede_patted: {guiea guide crve recordingComprehensiint(f"✅   pr 
  ide)
   .write(gu  ff:
      -8') as ding='utf, encopath, 'w'n(guide_   with oped")
 ng_guide.mrdisive_recoomprehens/cvideoic/"statath = Path(  guide_p
  """
    grounds.
 backalechnic of all t to farmersiblebeing access while raitha Mit AI Ravalue ofhe  tmonstratest clearly deideo tha, engaging vsionales a prof to create goal isember**: The*Rem
*---
eo views

vidm acking froersion trsis
- Convalyanfeedback ments and ints
- Comf podrop-of viewer ics onAnalytons
- rent versidiffe/B testing arity
- A video cloutabr surveys ction
- Use Colle Feedback##

#ntions meandedia shares  meo
- Socialrom vid fgeneration
- Lead  to websiterough rate- Click-thmments)
, shares, cokesnt rate (liemegag70%)
- En: > (targetion rateew complet
- Vince KPIsrmaideo Perfocs

### Vuccess Metri

## 📈 SshopPhotoobe , AdMP (free)va, GIics: Can- Graphon
iti Adobe Aude),ity (freudaco Editing: Audiurses
- Aemy co UdTube,ials: YouTutoreo Editing 
- Vidt.com/help://obsprojec: httpstionumentao DocudiOBS StSupport
- l echnica Tng

###ordissless rece loate, ustrncrease biting, i lighion**: Checkity
**Soluto qualider voblem**: PooPrction

**rodut-pos pnc insyy, o separatelcord audion**: Re*Solutissues
*dio sync i*: Au**Problem*
trate
le bi use variab settings,ratebit*: Adjust ion***Solutzes
e siLarge fil*Problem**: y apps

* unnecessaroseo 24fps, cl rate ter frame*: Low*Solution*recording
***: Laggy *Problem
*suesg IsRecordinCommon 

### ingeshoot🔧 Troubl
## bility
or accessi fdd subtitlesaptions: Aage
- Cimtching  eye-cagh-quality,il: Hina- Thumbogy
ase, technolseding, crop rmifa,  AIre,gricultu
- Tags: agriculture"art an", "smectioe det diseasg", "cropinAI farmike "ds lclude keyworion: In
- Descript"n Demotectiose Det Crop DiseaSmara - ha Mitr"AI Raitle: n
- TitioimizatEO Opt

### Snewsletters Include in keting**:l MarEmai
5. **Inram, Linkeds for InstagShorter clipl Media**: ia **Socation
4.onal presentrofessi: For pimeo**
3. **Vch and SEO rea For broader*YouTube**:modal
2. *me page d in hotion**: Embe IntegraWebsite. **
1latformsad P
### Uplos/
```
ogo   └── lics/
  ├── graph
   eenshots/── scr   ├
 
└── assets/c.mp3round_musi─ backg.wav
│   └─rration── namp4
│   ├_recording.  ├── screen── raw/
│ 
├.jpgail_640x360  └── thumbn20.jpg
│ l_1280x7thumbnaipg
│   ├── x1080.jbnail_1920um  ├── thails/
│ thumbnwebm
├── _mitra_demo.─ ai_raitha   └─480p.mp4
│demo_tha_mitra_─ ai_rai├─  4
│ .mpdemo_720pha_mitra_─ ai_rait.mp4
│   ├─o_1080pdemra_itha_mai_rait   ├── /
│─ finalideos/
├─static/vn
```
ioanizatrgFile O

### egyn Stratributio
## 🚀 Distpropriate
ence aprget audi [ ] Taent
-sting consi- [ ] Brandsible
ation viformitive inNo senshout
- [ ] hrougesentation tfessional pr
- [ ] Prois clearon ll-to-acti
- [ ] Cads highlightey benefit
- [ ] Keentsual contches vion matati] Narr- [ 
 clearlytratedtures demons feaAllist
- [ ] ty Checklontent Quali

### Cwebtimized for File size op- [ ] intained
mact ratio oper aspe ] Prvisible
- [ glitches chnicalo te- [ ] N pacing
nt Consiste
- [ ]ovementse m Smooth mous
- [ ]bleeadatext is rAll 
- [ ] e noisndkgrou bacear withoutclo is Audi)
- [ ] imum1080p mind clear (rp ans sha[ ] Video icklist
- ity Checal Qual## Technice

# Assuranlity
## 📊 Quarration
rb to nabtle reve Add sus
-ent levelor consistession fompr
- Use cuctionise redpply no -12dB
- As: -18dB toSound Effect8dB
- B to -124dsic: -und MuB
- Backgroto -6dB ion: -12dng
- Narrat# Audio Mixi

##ionm narratfrostract  doesn't diure musicEns tracks
- ssionaleat, profese upbChootion
- % of narrae at 20-30Keep volumccount)
- ith at (wapspla
  - Zsound.org Freeary
  - Librube AudioouT  - Ym:
music frooyalty-free 
- Use rMusicckground 

### Baty qualikes for bestmultiple tard coRets
- isual elemenpauses for v- Leave 
rate paceodey and at mSpeak clearle
- ent volumtain consist- Maint)
1kHz, 16-biat (44.n WAV form it
- Recordt environmen
- Use quieon Recordingratiar

### Nionroduct Audio P# 🎵

#ibilityompatetter web c**: For bion VersWebMices
4. **evr mobile d**: Fop)timized (480e OpMobil
3. **streamingb  faster we0p)**: For (72lity Qua*Mediumloads
2. *downd  antions presenta80p)**: Fory (10*High Qualitxports
1. *Format Eultiple 
### M`
20 MB
``rget: 80-1Tale Size bps
Fi8-192 k AAC, 12dio:)
Au qualitys (high 8-10 MbpPS
Bitrate: F30e Rate: 80
Framn: 1920x10esolutioH.264)
R: MP4 (Formatgs
```
 SettinExport
### iew
ity revinal qual] F[ - ntegration
sic id muun[ ] Backgrotion
- l normaliza] Audio leve
- [ nttmes adjusd brightnesn aniorrector co [ ] Colts
-I elemenor Um effects foo [ ] Add z
-formationkey inrlays for vetext o Insert 
- [ ]nsitionsmooth tra Add senes
- [ ]nge scd arra Cut ano
- [ ] videio and ] Sync audage
- [ raw foot[ ] Import-  Checklist
tingdieo E

### Vidroductionost-P
## 🎨 P"
tra. MiRaithath AI ey wir journstart you today to ct use or contabsitVisit our weAI. e with griculturr ang thei transformieadyo are alr whrmers fart smasands ofJoin thouion:**
"

**Narratd with logos
5. Enia linkmedsocial Show ons
4. oad opti downl. Displayon
3informatit tacShow con
2. e pageo homurn tRets:**
1. *Action
*45)30-3:ction (3:1: Call to Acene 1."

### S decisionsoved farmingicantly imprifgn, and siesoss l in cropon% reductilds, 40 higher yie report 25%ha MitraAI Raitusing mers 
"Fararration:**

**Nnialsestimoght farmer t Highliisons
4.comparfter w before/aho3. Sss stories
ay succeplcs
2. Dis metriatistics and st
1. Show*:*Actions
**(3:15-3:30)cess Impact ene 10: Suc# Sces."

##uagegional langr multiple rrt fouppo, and sptionsn oioonsultatg, expert cry trackinistoion h, predictationntegrher iatlude wees incal featur
"Additionon:***Narratifeature

*sultation  conert5. Show exphing
guage switcate lan. Demonstrons
4e opti profilow usertory
3. Shn his predictioisplay. Didget
2r wweathehow . S
1ctions:**-3:15)
**A2:55s (l Featureitiona Addene 9:"

### Scprofit.imum ps for maxeir croe to sell thnd wherout when as absiond deciformeke inrs mafarmelp ia hes Indis acrosor mandaj from mrket priceseal-time mation:**
"RNarration

**optimizaight profit  Highliations
4.price varw Shons
3. t locatioarkefferent my diDisplaion
2. s sectricearket p
1. Show m***Actions:)
*5-2:55ce (2:3genliet Intel: Mark## Scene 8

#"s.fection inavoid futuretegies to ention straprevns, and tructiolication insailed apptions, detemical opanic and ch orguding both incltionsmmenda recotmenteatrensive eive comprehmers rec
"Farration:**
**Narng
ation timiow applicSh
5. nstructionsdetailed ight 
4. Highlin tipsentiolay prev
3. Dispernativesl altchemica
2. Show mentsanic treat through org1. Scroll:**
**Actions5-2:35)
ions (2:0ommendatent Receatmcene 7: Tr S

###lysis." anaptom symtailedides deld and proviep yt on crol impace potentiaicts thpredt also nce. Iide94% confwith ight e Blato Latomidentifies The AI n seconds, t"I:**
**Narration

ctionoms septthrough symoll Scr5. on
redictild impact pay yie Displnce: 94%
4.ide3. Show conf"
e Blighto Latatomse name: "Thlight disealts
2. Higesue analysis rplet1. Show com:**
nstio05)
**Ac(1:35-2:y ispla Results D 6:Scene# s."

##e imageiseas of crop dusandshoed on trainhms toritearning alg le using deepagyzes the imlogy, analchnoemini te's Gd by Googleere system, powdvanced AI"Our ation:**
rra

**Nagynologht AI techli
4. Highionnimatsing aprocesShow . dicators
3progress in. Display essage
2 AI" mwith Gemininalyzing how "A
1. SActions:**15-1:35)
**tion (1: in Acalysis 5: AI An
### Scene"
mmediately. analysis igins itsr AI beoto, and ouphds the ly uploarmer simpe. The fa of diseasns showing sigtomato leafle - a mpeal exaa ranalyze "Let's 
:**ion
**Narratn
atioing animload6. Show utton
ze Image" b"Analy Click  preview
5.w imagepg
4. Shoe_blight.jato_latomlect ter
3. Seoldimages fo demo_te tgaon
2. Naviutt bage"pload Imlick "U
1. CActions:**
**15)-1:45cess (0: Upload Proage: Imcene 4# S##."

hotosng pxistiupload eor hone camera their puse an s c Farmerl languages.ple locaultiailable in mive, and avuitple, intd - sim minfarmers inwith is designed rface ion inteecte dete diseas"Thion:**
at

**Narrtooltipshelp 
5. Show ndly design user-frieighlightn
4. Helectioguage slanemonstrate 
3. Dad optionsuplocamera and w 2. Shoage
 detection pseeao disvigate t
1. Na*ions:***Act:25-0:45)
terface (0 Inse Detectioneae 3: Dis
### Scenre."
 and secus is simple processtratione. The regiimlth over trop hear c theid trackns anmendatiorecomized  personalss acceaccount tore a secuers create rm fa"First,n:**

**Narratiol login
fuessucc sShowlogin
6. 
5. Click mo123password: deype 
4. Tra.comraithamitpe: demo@Tyn form
3. how logi Stion"
2.ease Detectart Dis Click "Sons:**
1.
**Acti5)(0:10-0:2ntication utheser Acene 2: U S"

###one photo.t a smartphith jusy wtantliseases ins crop d detecters can how farmow youe shce. Let mlligenificial intere with arttuing agriculs transformt'thaform latonary pvoluti the re Mitra -ha AI Raitme to*
"Welco*Narration:*
*" button
ctionse Detet DiseaStarcus on "s
4. Foret key featuigh Highlnterface
3.s the ipan acroslow oaded
2. Spage lith home rt w1. Sta*
**Actions:*00-0:10)
ction (0:ntrodu# Scene 1: I

##triprding Sc
## 🎭 Recon
ean sessiofor clde ncognito mo
- Use iokmarks baride bons
- Hatio notificsable Dikies
-d coo cache an%
- Clear Zoom: 100F11)
- (en moden fullscrerome ie Ch Setup
- Us
### Browser
```
hone: 70-80%Micropo: 100%
- ktop Auditereo
- Desannels: S1 kHz
- Chte: 44.Rae gs:
- Sampl Settink)

Audio: (blantions4 Opx26: (none)
- gh
- Tuneile: hi Prof
-t: veryfastPrese CPU Usage val: 2
-nterrame Ieyfs
- Kte: 8000 Kbp- Bitratrol: CBR

- Rate Coner: x264MP4
- Encodat:  Formgs:
-rding Settinment

Recoadjustn, Gain suppressiors: Noise e
- FilteMicrophondio +  Desktop audio Input:0)
- Auen (1920x108ree: Full scsplay Capturetup:
- DiScene S`

``igurationtudio Conf

### OBS Sng Setup🎬 Recordi## nd music

grouelect back [ ] S script
-onpare narrati[ ] Preng
- s are workifeatureall  ] Verify 
- [mple imagesn with saectioase detse] Test di.com)
- [ amitra@raithed (demoount creat accple user- [ ] Samracticed
d and pwept reviescriemo on
- [ ] Dt Preparati
### Conten
st 5GB free)e (at lea spacstoragep ckuBament
- [ ] g environecordin Quiet rding
- [ ]een recor scrforghting  [ ] Good lionment
-irtop envean deskClges/
- [ ] ads/demo_imalotatic/upeady in sse images rple disea Sam- [ ]d
igure conftalled and insOBS Studio0
- [ ] ocalhost:500on lunning tion rlask applica ] F Setup
- [# Technicalcklist

##Chection re-Produa.

## 📋 Paitha Mitrs of Rpabilitietection caI disease deng the Ahowcasiideo smo vde 3-4 minute alprofessionw
Create a ie Overvctroje
## 🎯 Pion Guide
ct ProduVideoe pletitra - ComAI Raitha M
# ""ide = "   gu
   "
  guide."" recording iveomprehenshe most cate t"""Cre():
    _guiderdinghensive_recoeate_compre)

def crth}"_paoardybated: {stor creoryboarddeo st"✅ Viint(f
    prt=2)
    rd, f, indenyboaon.dump(stor     js
   ') as f:tf-8ing='uod enc_path, 'w',rdn(storyboa opewith  json")
  ryboard.tos/video_s/videostatic = Path("ard_pathstorybo
    }
       }
   
      s" and overlay animationsimple, cleanhics": "Sgrap "      ",
     onar narratinal, cle"Professio": ce_over    "voi    ,
    y"o LibrardiAuom YouTube lty-free frRoyaource": "c_smusi  "        ",
  lityuatter qtrack for bete audio ": "Separangio_recordi  "aud
          ",o Premiere PrAdobe or solve (free)i Re "DaVinctware":_sof "editing         
  Studio",S  with OBrecordingreen d": "Scording_metho     "rec   
    _notes": {"production   
      },
           "
    utes4:00 min"3:30 - ration":    "du
         b", for we100 MBize": "< "file_s      ",
       kbps, 128": "AAC"audio            (H.264)",
4 MPt": "orma         "f   :9",
: "16ect_ratio"   "asp       FPS",
  ": "30 e_rate"fram       ",
     Full HD) ("1920x1080lution":   "reso
          s": {irementical_requtechn "     
              ],
  }
   
           "]epsext stsy ntion", "Ea acall toear c"Cls": [key_point    "   ,
         logy." AI technoming withur farnsform yoy and traa todaitha MitrI RaDownload Aers. smart farmousands of  "Join thn":tio     "narra     
      music",action to- call-nal,vatio"Motiaudio":  "                   ],
            ia links"
cial med  "So                  e URL",
 "Websit           ,
        ormation"ntact inf     "Co             
  ns",ad butto  "Downlo                  ts": [
men"visual_ele                0",
4:05 - "3:4duration":       "     n",
     all to Actiotle": "C  "ti       
       r": 12,_numbe"scene             {
           
         
                },]
   fits"enentify bf", "Quaal proo": ["Sociey_points "k      
         .",ossesn in crop lductio and 40% reovements impryieldeeing 25%  already s aress Indiamers acro": "Farionnarrat  "           
   music",estimonial  tpiring, "Ins":  "audio              ],
               rics"
 etss m"Succe                   istics",
 tatment sd improve"Yiel                  ",
  gesimacrop fter fore/a  "Be                
  ",monialsesti t    "Farmer            s": [
    lementual_e     "vis           5",
:40 - 3": "3:3"duration                ories",
ess StSucc": "title       "    11,
     e_number":       "scen             {
            
 
         },       
    lity"]sibit accesighlighres", "Hatuve fesiw comprehen": ["Shopoints"key_              
  ution.",g solinfarm a complete  this makeconsultationexpert ges, and languae ion, multiplater integr "Weath":"narration             ic",
   musre-rich e, featuhensivpre"Com ":odi  "au             ],
                ptions"
 ion ort consultat     "Expe              story",
 ction hi"Predi                  ,
  ort" suppage-langu  "Multi            ",
      ntegration "Weather i                    [
lements": "visual_e      
         30",0 - 3:: "3:1on"ati   "dur          s",
   l Featureona"Additi":    "title           ": 10,
  numbere_"scen                       {
  
         
           },"]
       luerket va mamonstrateits", "De benefnomic["Show eco": y_points    "ke            profit.",
or maximum e to sell fhen and wherdecide wfarmers mandis help m major rices fro pketime marl-tRean": " "narratio       
        ble tone",itad, prof-focuse "Business":     "audio         
    ],            "
  tipson izatirofit optim  "P           ",
       lysisnarend aice t    "Pr             ns",
   ioarket locatMultiple m      "             rts",
 ce chaeal-time pri "R                : [
   lements"ual_e  "vis        ,
      0 - 3:10"": "2:5ation      "dur        ,
  telligence" Inket": "Maritle  "t       ,
       : 9e_number""scen          {
         
           
              },       
 ess"]etenate compl"Demonstr, vice"e adtionabl"Show acpoints": [ "key_           s.",
     instructionlication appaileddetth options, wihemical and ch organic lans - botreatment psive teneheceive comprrmers r: "Farration"       "na       ne",
  tional to instruc: "Helpful, "audio"            
             ],      egies"
n strattio    "Preven                ions",
uctstep instrep-by-St       "             ",
ativesl altern   "Chemica                ptions",
  treatment oOrganic     "         [
      ": ntsl_eleme "visua           ,
    50" - 2:"2:20ration":      "du
           dations",ent RecommeneatmTrtitle": "   "           
  r": 8,ne_numbe       "sce
         {                   

            },    
 lue"]vaemonstrate sults", "Date reccur["Show a": tskey_poin     "          nt.",
 ity assessmes severand provideact impd elial yi potentctsediem prhe systdence. Tfiith 94% con wifiedidentlight  BTomato Lateration": "     "nar           t music",
chievemens, a: "Succes   "audio"       
       ],             ion"
  dictimpact pre  "Yield              
     sessment",Severity as "               ",
    ge displayntance perce  "Confide                 
 s",tion resultificae ident"Diseas          
          : [lements"sual_e  "vi             ",
 20 - 2:on": "1:50urati       "d         ",
 & DiagnosisResults": "title"            ,
    : 7ber"_num  "scene        {
         
                          },
       nce"]
 confide"Buildation", isticShow AI sophints": ["y_po   "ke        y.",
     ccurac 94% atterns withease paof disusands st tho image againhees tompar cGemini,oogle's owered by Gnced AI, padvaon": "Our    "narrati          
   ds",ing sounh, process "High-tecaudio":   "    
              ],          
 n"matioson aniompariabase c  "Dat                 
 ing up",ter buildmenfidence     "Co         
       s",icnition graphrn recog"Patte                   zation",
 k visualieural networ     "N          [
      s":entemsual_el       "vi,
         0 - 1:50"": "1:3  "duration      
        cess",alysis ProAn "AI le":"tit           ,
     r": 6_numbescene     "                {
 
                 },
    
         usage"] real howo", "Sy demctionalit"Core fun": [_points   "key            ",
 onds.just seckes e process taptoms. Thsymight te blaf with lato lelyzes a tomaAI anach as our at": "Wation     "narr     ",
      cmusial , analytic-focusedech": "Tudio         "a
         ],              ation"
ualiz visnalysis"AI a              n",
      ess animatioogr pr    "Upload         ",
       phedotograg phinf beeased leal dis       "Rea       ,
      action"nterface in  iamera      "C        : [
      ments"ual_eleis"v        ,
        5 - 1:30""0:5ration": "du             ",
    Demoectionsease Dettle": "Di     "ti          5,
 : ne_number"      "sce               {
    
                },
           "]
e securityiz, "Emphasding" onboarw user ["Shoey_points":"k          
      ",tory.health hisop crack their ons and trndatid recommezeliersonas pto accesount secure acc a terea"Farmers c": n  "narratio            und",
  hy backgrotrustwort": "Calm, "audio           
             ],
        d"oardashbized Personal   "                 lighted",
eatures high"Security f             
       process",istration "User reg                  
  ",in interface"Clean log                  
  ": [slement_eual"vis             :55",
   :40 - 0: "0tion""dura             
   in", - Logrneyer Jou"Us": tle      "ti          ,
umber": 4cene_n "s              {
             
            },
        e"]
    usow ease of "Shion", lutPresent soints": ["  "key_po       ",
       osis.isease diagn accurate dinstant,get o, farmers  photmartphoneust a sWith jverything. s eitra changeaitha M"AI Rrration":     "na          ic",
  nted musolution-orie"Hopeful, saudio":           "],
                     ogy"
 hnol using tecfarmer    "Happy                 zation",
ults visualint res     "Insta         n",
      ain animatioI br       "A      
       erface",ith app intone w   "Smartph           [
       lements":visual_e        "     
   25 - 0:40","0:n": tio "dura              ,
 troduction""Solution In": "title       ,
         er": 3"scene_numb                {
          
             ,
       }"]
      onnectionional create emot "Cem",problstablish ": ["E"key_points            ",
    rmers lack. many faertise thatd expes time anagnosis takaditional diTrdiseases. cted crop e to undetellions dubise rmers loar, faEvery yeation": "     "narr           one",
hetic trned, empatConceudio": "       "a,
           ]    
          "challengesing tional farm  "Tradi           
        losses",ics on cropatist"St                    ",
onssiarmer expresorried f"W                    ",
agesed crop im    "Diseas              
   [lements":al_e"visu                 0:25",
 "0:10 -uration": "d     
          t",m Statemen"Proble: le"      "tit
          er": 2,e_numben  "sc                  {
         
         },
            e"]
  nal tonrofessioet p", "SontroductiBrand in": ["key_points    "          ,
  ce."ligenintelartificial re with ricultug aginionizrevoluttha Mitra - cing AI Rai"Introduation":   "narr          
    c",o musiintrrofessional at, p"Upbeio":     "aud              ],
            
  with AI'"t Farming : 'Smar"Tagline                  ",
  atingicons flo "Farming             ,
       ckground"t bagradieneen        "Gr            ",
  animationa logoa MitrRaith "AI                    ments": [
sual_ele      "vi          - 0:10",
 "0:00 ":on"durati           ,
     ing Title"pen": "O     "title         1,
  : er"ene_numb  "sc   
             {      
    "scenes": [        
   ,
     ble"profitaer and more artg smrmins fa maketectionded disease "AI-powere": essage"key_m       stors",
 nveessionals, I proficulturalarmers, Agrce": "Fget_audien    "tares",
    4 minut": "3-_duration   "totalo",
     emection Dease Dettra - Dis Raitha Mi"AI"title":    
     yboard = {    stor
    
""yboard."d video store a detaile""Creat  "ard():
  eo_storybo create_vid")

defath}ated: {img_p✅ Cref"rint(     p  y=95)
  qualitG",th, "JPEsave(img_pa       img."]
 name"ase[ diseir /s_dmage_path = i   imgmage
       # Save i 
      )
       ntont=fohtgray", f="ligll fioms"],"sympte[iseas20, 45), daw.text((dr      
  tle_font)nt=tiite", fo"whll=, fi"]itleisease["t((20, 20), d.text draw
       28)) 1 0, 0,l=(0, fil],, 8010, 10, 390.rectangle([aw dr   t
    nd for texAdd backgrou  #           
  fault()
  .load_deageFont Im_font =title         )
   d_default(.loa ImageFont      font =:
         except0)
     .ttf", 2ale("ari.truetyp = ImageFontnttitle_fo           
  16).ttf",ype("arialruetmageFont.tont = I         f  y:
       trd info
  itle an   # Add t  
     "])
      ot_color"spl=disease[+15], fil, y, x+20+10, y+5lipse([xelw.       dra  )
   r"]olopot_c["sl=disease, fil5]5, x+5, y-([x-5, y-1raw.ellipse         dts
   ing spoler surround   # Smal       )
  t_color"]["spofill=disease15, y+10], 5, y-10, x+ellipse([x-1  draw.        t
   Main spo         #s"]:
   e["spot diseasfor x, y in       
 e spotsasse Add di #     
        =2)
  0), width40, 120, 4fill=(160)], (200, ,  180)([(280,  draw.line   h=2)
   ), widt0, 40 12], fill=(40,160)180), (200, , 120draw.line([(       idth=2)
  w0, 40),fill=(40, 12, 120)] (200, , 100),([(280w.line     dra  2)
 idth=, w0) 40,ill=(40, 1220)], f), (200, 1120, 100e([(draw.lin    vein
     Main h=3)  #idt, w, 120, 40))], fill=(40 (200, 25050),00, (2line([ draw.    
   leaf veins     # Add 
          
 ])"leaf_color=disease["fill0],  50, 350, 25llipse([50,.e draw      ed oval)
 (elongatshape leaf    # Draw 
         img)
    .Draw( = ImageDraw    draw   
 r"])bg_coloease["), dis0, 30040 (e.new('RGB', img = Imag
       reate image        # Cses:
 in diseaseaser di    
    fo
    ]
 }      65, 205)]
 ), (1, (185, 1755) (155, 1875, 155),, (1 [(145, 135)spots":         "ange
   Deep or# , 34),   87": (255,pot_color     "s
       een  # Light gr),187, 106": (102, eaf_color     "l
       0), 6 142,or": (56,ol     "bg_c   
     ",cefaurf sles on leatupused : "Orange-rtoms"   "symp,
          Rust"eate": "Wh   "titl  
       ",at_rust.jpg"whe "name":        
          {,
      }    0, 220)]
 (1570),, 1 (200 190), 150), (160,, (180,30, 130): [(1   "spots"  
       0),  # Tan180, 14: (210, spot_color"       "    n
 ),  # Gree 80, 175,r": (76colo "leaf_        ),
    125, 50": (46,color"bg_           s",
 an centerpots with tall oval s: "Smmptoms"       "sy", 
     SpotLeaf : "Corn tle"  "ti          .jpg",
_spot"corn_leafame":    "n              {

     },      190)]
 (210,  210),, (170,, (190, 170)(140, 140)"spots": [          n
  browaddle 5),  # S2, 4: (160, 8lor"t_co       "spo    sea green
 um 3),  # Medi79, 11: (60, 1eaf_color" "l           25),
 0,": (25, 10  "bg_color     
      rings",concentricwith ts ar brown spo"Circul": tomssymp  "         ,
 t"rly BlighPotato Ea": "   "title      pg", 
   ht.j_bligtato_early": "poe"nam       {
       
        },)]
      , (160, 240, (220, 180)180, 200)00, 160), (120), (2: [(150,    "spots"       rown
  e b Saddl9, 19),  #r": (139, 6colospot_        " green
    0),  # Lime05, 550, 2f_color": (       "lea   st green
  34),  # Fore4, 139, or": (3"bg_col          owth",
   gre fuzzyhit with wrown spots"Dark btoms":      "symp      ght",
 e Blio Latmate": "To      "titl
      jpg",ight.te_blomato_laame": "t        "n         {

   ases = [ses
    ditic symptomealisth res wiamplDisease s# 
    
    rue)k=Txist_o, ents=Truearer(p.mkdiges_dir ima   ")
emo_imagesploads/dtic/uPath("sta= ages_dir    
    imn
    returw")
     ll pillo: pip instaall withstInle. availab not IL print("P      
 tError:Impor  except t
  Fonage Imaw, ImageDrmage, Iortmprom PIL i  f
          try:    
"
