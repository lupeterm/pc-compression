#import "slides/slides.typ": *
#import "@preview/drafting:0.2.2": *
#set text(lang: "DE")
#let arrowList =  [#hide("  ")#sym.arrow]
#show: titleSlide.with(
  [],
  authors: ("Lukas Petermann"),
  date: datetime.today() // konkretes Datum mit: datetime(year: 2025, month: 01, day: 22)
)

/* ------------------------ */
#place(horizon + center, dy:-17%)[
    = Abschlusspräsentation Wissenschaftliches Individualprojekt:
    = "Evaluation of Point Cloud Geometry Compression on Sparse and Non-uniform Data"
]
---
#show: slides.with(
  [],
  chapter: "Einleitung",
  authors: ("Lukas Petermann"),
)
= 1 Einleitung und Motivation

- Punktwolken sind flexibel, vielseitige Anwendungsfälle
  -  zB. Autonomes fahren, AR/VR, Ditigales Modellieren 

- Größe der übertragenen Daten wächst schnell mit Aufnahmedauer
  - z.B. FIN Hörsaal: #sym.tilde 2M Punkte nach 300s

  #arrowList Kompression der Punktwolken notwendig

  
#place(horizon+end,dx: 5%,dy:-10%,
  figure(
    caption: [Kompressionsworkflow @wiesmann2021ral],
    image("figures/compression.png")
  )
)  
---
#show: slides.with(
  [],
  chapter: "Einleitung",
  subchapter: "Kompression",
  authors: ("Lukas Petermann"),
)
= 1.1 Punktwolkenkompression

- Übliche Datensätze:
  - Kitti#footnote[Dünnbesetzt, Outdoor]@behley2019iccv, Shapenet#footnote[Dichtbesetzt, Objekte]<d>@Chang2015ShapeNetAI, 8iVFB#footnote(<d>)@JPEG
  
- Lücke in aktueller Literatur:
  - Dünnbesetzte, ungleichmässig dichte Daten #linebreak()von Innenräumen#linebreak()
    
    // #sym.arrow FIN Datensatz @Petermann2023ComparisonOR
#place(horizon+end,dy: -4.5%, dx: 4%,
  align(horizon + end)[
    #figure(  caption: [Oben nach unten: Kitti@behley2019iccv,Shapenet@Chang2015ShapeNetAI, 8iVFB@JPEG ],[
      #image("figures/kitti.png", height: 30%) 
      #image("figures/shapenet.png", width: 15%)
      #image("figures/8iVFB.png", height: 33%) 
    ])

  ]
)

---
= 2 Ziel des Projekts
- Evaluierung von Punktwolkenkompression auf bisher unerforschter Art von Daten
  - Einheitlicher Vergleich von Algorithmen
  - "Welcher Algorithmus ist am besten geeignet?"
- Fokus:
  - Innenräume
  - Dünnbesetzt und ungleichmässige Dichte
  - Veröffentlichter Quellcode
  - verlustfreie ("lossless") Algorithmen
---
#show: slides.with(
  [],
  chapter: "Konzept",
  authors: ("Lukas Petermann"),
)
= 3 Konzept
- Kompression sollte zeitlich effizient sein

- Schnelle Übermittlung, aber langsame Kompression ist nicht zielführend

- Rekonstruierte Punktwolke sollte möglichst ähnlich sein
  // - Abhängig von benötigter Präzision der Daten bei Verarbeitung

- *Problem*: 
  
  - Bisher wurde keine Evaluation auf dieser Art Daten ausgeführt

  #arrowList Auswahl des Algorithmus nicht trivial

--- 
= 3 Konzept
- Erster, einheitlicher Vergleich von Kompressionsalgorithmen auf dieser Art von Daten

- Dafür benötigt:

  1. Auswahl von Algorithmen

  2. Auswahl des Datensatzes 
  
  3. Bewertungsmetriken

---
#show: slides.with(
  [],
  chapter: "Konzept",
  subchapter: "Auswahl der Algorithmen",
  authors: ("Lukas Petermann"),
)
= 3.1 Algorithmen in der Literatur
  - Quellcode muss verfügbar sein
    - KI-basierte Verfahren: Inkl. Vortrainiertes Modell   
  - Muss auf Punktwolken im `.ply` Dateiformat mit 32bit Präzision arbeiten

#place(center,dy: 5%,table(
    columns: 4,
    table.header(
      [Algorithmus],
      [Quellcode (& Modell) vorhanden?],
      [Dateiformat],
      [Präzision]
    ),
    [*`draco`*@google],[#sym.checkmark], [PLY, OBJ, STL],[float32],
    [*`pccomp`*@Szppaks],[#sym.checkmark], [PLY, OBJ, STL,PCD],[Numpy#footnote[Alle Präzisionen (inkl. float32)]<p>],
    [*`tmc3`*@MPEGGroup],[#sym.checkmark], [PLY],[PLY#footnote(<p>)],
    [*`sparsePCGC`*@Ding_Li_Feng_Cao_Ma_2022],[#sym.checkmark], [PLY, H5, BIN],[float32],
    [`DPCC`@He_2022_CVPR],[#sym.crossmark], [PLY, XYZ, BIN],[float32],
    [`Unicorn`@10682571@10682566],[#sym.crossmark], [PLY, H5, BIN],[float32],
    [`Depoco`@wiesmann2021ral],[#sym.crossmark], [PLY, BIN],[float32],
    [`Mpeg Anchor`@7434610],[#sym.crossmark], [?], [?]
  ))
  --- 
#show: slides.with(
  [],
  chapter: "Konzept",
  subchapter: "Auswahl der Algorithmen",
  authors: ("Lukas Petermann"),
)
= 3.1.1 Auswahl der Algorithmen
- Exkludiert:
  - `DPCC`: 
    - Trainieren des Modells notwendig
    - Datenvorbereitung erwartet KITTI oder ShapeNet
  - `Unicorn`:
    - Kein Quellcode, keine Modelle
  - `Depoco`: 
    - Trainieren des Modells notwendig
  - `Mpeg Anchor`: 
    - Kein Quellcode
    
- Inkludiert: `draco, pccomp, tmc3, sparsePCGC`
--- 
#show: slides.with(
  [],
  chapter: "Konzept",
  subchapter: "Auswahl der Algorithmen",
  authors: ("Lukas Petermann"),
)
= 3.1.2 Benutzung der ausgewählten Algorithmen
- `Draco`:
  - Binaries aus Evaluationsskript aufrufen
  
- `pccomp`:
  - Python Funktionen aus Evaluationsskript aufrufen
- `tmc3`:
  - Binaries aus Evaluationsskript aufrufen 
  - Benutzter Datensatz zu klein, setze `--inputScale=100` und `--outputUnitLength=100`
- `sparsePCGC`:
  - Docker Entwicklungsumgebung der Autoren
  - Benutzter Datensatz zu klein, manuelle Skalierung nötig (open3D@zhou2018open3dmodernlibrary3d)
  - Verschieben des Mittelpunktes

---
#show: slides.with(
  [],
  chapter: "Konzept",
  subchapter: "Ausgewählter Datensatz",
  authors: ("Lukas Petermann"),
)
= 3.2 Ausgewählter Datensatz: FIN@Petermann2023ComparisonOR
- Aufnahmen in der Fakultät für Informatik der OvGU

- Vier Szenen:
  - Hörsaal (307)
  - Flur
  - Büro (425)
  - Konferenzraum (333)
  
- Konvertierung: `.pcd` #sym.arrow `.ply` und 64bit #sym.arrow 32bit 

#place(top + end,dx: 6%,dy:10%,
  figure(
    caption: [FIN Datensatz, Hörsaal Szene @Petermann2023ComparisonOR],
    image(width:50%,"figures/FIN307.png")
  )
) 
---
#show: slides.with(
  [],
  chapter: "Evaluation",
  subchapter: "Hardware & Metriken",
  authors: ("Lukas Petermann"),
)
= 4 Evaluierung
#grid(gutter:1fr,
  columns: 2,
  [
- Hardware:
  - Intel Core i7-12700KF CPU
  - Nvidia 4070 RTX GPU
  - 32 GB DDR5 RAM
- Bewertungsmetriken
  - Berechnungsdauer
    - Enkodierung, Dekodierung   
  - Kompressionsrate `bpp` (bits per point) 
  - Enkodierte Dateigröße
  - Qualität der Rekonstruierten Punktwolke
  
    - Strukturelle Ähnlichkeitsmetrik `PointSSIM` @9106005 
    
  ],
  [ 
  #move( dy: 40%,
      stack( spacing: 15%,
        $t_"enc/dec"=frac("Berechnungszeit",|"Points in Original Cloud"|)$,
        $"bpp" =frac("Encoded File size (bits)",|"Points in Original Cloud"|)$
      
      )
    )
  ]
)
---
#show: slides.with(
  [],
  chapter: "Evaluation",
  subchapter: "PointSSIM",
  authors: ("Lukas Petermann"),
)
= 4.1 Strukturelle Ähnlichkeitsmetrik `PointSSIM`#footnote[#link("https://github.com/mmspg/pointssim")]
- Feature Extrahierung: 

   - Nutze lokale Nachbarschaften um jeden punkt
   - Quantitäten: Euklidische Distanz & Krümmung
   - Wende Streuungsschätzer#footnote[u.a. median, Varianz, MAD] auf Quantitäten an
   
- Strukturelle Ähnlichkeit:
  - Berechne relativen Unterschied zwischen Features
  - Berechne Gesamtwert über Fehler Pooling:#linebreak()#linebreak()#hide("fffffffffffffff")$S_Y=frac(1, N) sum_(p=1)^N S_Y (p)$
#place(
    horizon+end,dx:4%, 
  stack(spacing: 5%,
    figure(
      caption: [Feature Extrahierung #cite(<9106005>,supplement: "Fig. 1")],
        image(width: 50%,"figures/pssim1.png")
    ),
    figure(
      caption: [Strukturelle Ähnlichkeitsberechnung #cite(<9106005>,supplement: "Fig. 2")],
        image(width: 50%,"figures/pssim2.png")
    ),
  )
)
---
#show: figureSlide.with(
  [],
  chapter: "Evaluation",
  subchapter: "Kompressionsrate & Berechnungszeiten",
  authors: ("Lukas Petermann"),
)
#place(top, dy: 2%,
 [= 4.2 Kompressionsrate & Berechnungszeiten]
) 
#place(center+top,dy: 5.8%,
 figure(
    caption: "Kompressionsrate & Berechnungszeiten",
    image(width:92%,"figures/all_scenes_all_algos_wide.svg")
  )
) 
---
#show: figureSlide.with(
  [],
  chapter: "Evaluation",
  subchapter: "Strukturelle Ähnlichkeit",
  authors: ("Lukas Petermann"),
)
#place(top,dy: 2%,
 [= 4.3 Strukturelle Ähnlichkeit]
) 
#place(center,dy: 5.8%,
 figure(
    caption: "Strukturelle Ähnlichkeit",
    image(width:92%,"figures/similarity_wide.svg")
  )
) 
---
#show: slides.with(
  [],
  chapter: "Fazit",
  subchapter: "Fazit",
  authors: ("Lukas Petermann"),
)
= 5 Fazit
- `tmc3, sparsePCGC`: 
  - Im Vergleich deutlich langsamer
  - niedrigste Ähnlichkeit
  - Datensatzskalierung ist ein Faktor
- `pccomp`: 
  - Höchste Ähnlichkeit, geringste Berechnungszeiten
  - *aber*: geringste Kompressionsrate
- `draco`: 
  - Knapp schlechter als `pccomp` in Ähnlichkeit und Berechnungszeit
  - *aber*: deutlich bessere Kompressionsrate
- `draco` überzeugt insgesamt am meisten
- Quellcode und Ergebnisse: #link("https://github.com/lupeterm/pc-compression")

#show table.cell.where(y: 0): strong
#set table(
  stroke: (x, y) => if y == 0 and x==0 {
    (bottom: 0.7pt + black,right:0.7pt+black )
  } else if y == 0 and x!= 0 {
    (bottom: 0.7pt + black )
  } else if x<= 0 {(right: 0.7pt + black)},
  align: center
)
#place(dx: 57%,dy:-75%,
  table(
    columns: 5,
    table.header(
      [Algorithmus],
      [`PSSIM`],
      [`bpp`],
      [Enk.-Zeit#super[1]] ,
      [Dek.-Zeit#super[1]],
    ),
    [`tmc3`],[0.882], [*3.31*],[1925ns],[938ns],
    [`sparsePCGC`],[0.885], [9.86],[6238ns],[5780ns],
    [`pccomp`],[*0.997*], [13.54],[*281ns*],[*173ns*],
    [`draco`],[0.903], [4.025],[396ns],[220ns],
  )
)
#move(
  dy:5%, dx: 3%,
  overline(offset: -16pt,[#super[1]Durchschnittliche Zeit pro Punkt])
)
---

#set par(justify: true) // -> sieht besser aus, imo.
#bibliography("bibliography/refs.bib", full: true)

---
#show: titleSlide.with(
  [],
  authors: ("Lukas Petermann"),
  date: datetime.today() // konkretes Datum mit: datetime(year: 2025, month: 01, day: 22)
)
// #move(dx: 30%,dy: 40%,
#place(horizon + center, dy:-18%)[
  = Danke für ihre Aufmerksamkeit!
  = Fragen?
]
// )
---
#show: titleSlide.with(
  [],
  authors: ("Lukas Petermann"),
  date: datetime.today() // konkretes Datum mit: datetime(year: 2025, month: 01, day: 22)
)
#place(horizon + center, dy:-18%)[
    = Appendix
  ]
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Datensatz Dichte",
  authors: ("Lukas Petermann"),
)
= Vergleich: Datensatz Dichte
#place(horizon,
grid(
  columns: 2,
   [ #figure(caption:[2D3DS @armeni2017joint2d3dsemanticdataindoor Hörsaal Dichte],
      image("figures/2D3DS.png", width: 95%)
    )],
  [
#figure(
  image("figures/FIN.png"),
  caption: [FIN @Petermann2023ComparisonOR Hörsaal Dichte]
)
    
  ]
)
)
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "PointSSIM Gleichungen",
  authors: ("Lukas Petermann"),
)
= `PointSSIM` Gleichungen
#place(horizon,
grid(
  columns: 3,gutter: 1fr,
   [ #figure(caption:[Streuungsschätzer #cite(<9106005>, supplement: "Eqs.1-4")],
      image("figures/dispersion.png")
    )],
  [
#figure(
  image("figures/pointssimRelFe.png"),
  caption: [Berechnung Relativer Fehler der Features #cite(<9106005>, supplement: "Eq. 5")]
)
    
  ],[
    #figure(
      image("figures/pointssimErrpo.png"),
      caption: [Berechnung Fehler der Ganzen Punktwolke. $k in {1,2}$ #cite(<9106005>, supplement: "Eq. 6")]
    )
    
  ],
)
)
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Ähnlichkeitswert Flur",
  authors: ("Lukas Petermann"),
)
#place(center+top,dy: -7%,
 figure(
    caption: "Ähnlichkeitswert Flur",
    image(width:90%,"figures/similarity-hallway.svg")
  )
) 
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Ähnlichkeitswert Büro",
  authors: ("Lukas Petermann"),
)
#place(center+top,dy: -5%,
 figure(
    caption: "Ähnlichkeitswert Büro",
    image(width:90%,"figures/similarity-office.svg")
  )
) 
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Ähnlichkeitswert Hörsaal",
  authors: ("Lukas Petermann"),
)
#place(center+top,dy:-5%,
 figure(
    caption: "Ähnlichkeitswert Hörsaal",
    image(width:90%,"figures/similarity-auditorium.svg")
  )
) 
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Ähnlichkeitswert Konferenzraum",
  authors: ("Lukas Petermann"),
)
#place(center+top, dy:-5%, 
 figure(
    caption: "Ähnlichkeitswert Konferenzraum",
    image(width:90%,"figures/similarity-conferenceRoom.svg")
  )
)
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Enkodierungszeit",
  authors: ("Lukas Petermann"),
)
#place(center+top,dy: -7%,
 figure(
    caption: "Enkodierungszeit",
    image(width:90%,"figures/time_enc_ns.svg")
  )
) 
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Dekodierungszeit",
  authors: ("Lukas Petermann"),
)
#place(center+top,dy: -5%,
 figure(
    caption: "Dekodierungszeit",
    image(width:90%, "figures/time_dec_ns.svg")
  )
) 
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Bits pro Punkt",
  authors: ("Lukas Petermann"),
)
#place(center+top,dy:-5%,
 figure(
    caption: "Bits pro Punkt",
    image(width:90%,"figures/bpp.svg")
  )
) 
---
#show: appendix.with(
  [],
  chapter: "Appendix",
  subchapter: "Enk. Dateigröße",
  authors: ("Lukas Petermann"),
)
#place(center+top, dy:-5%, 
 figure(
    caption: "Enk. Dateigröße",
    image(width:90%, "figures/enc_file_size_bits.svg")
  )
) 