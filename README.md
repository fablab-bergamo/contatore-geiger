# Contatore Geiger per BergamoScienza

Progetto di contatore Geiger basato su ESP32 con display TFT per la rilevazione di radiazioni ionizzanti, sviluppato per BergamoScienza.

![Contatore Geiger Completo](images/rilevatore-con-battery-pack-1024x768.jpg)
*Dispositivo completo assemblato: LILYGO T-Display ESP32, modulo CAJOE RadiationD v1.1 in case trasparente, e battery pack per utilizzo portatile*

## Panoramica

Questo sistema implementa un contatore Geiger digitale che visualizza in tempo reale le misurazioni di radiazioni su un display TFT colorato. Il progetto è progettato per funzionare con il modulo rilevatore di radiazioni CAJOE (RadiationD v1.1) equipaggiato con tubo Geiger-Müller J305.

### Contesto Educativo

Questo progetto nasce nell'ambito di **[BergamoScienza](https://www.fablabbergamo.it/2025/10/05/caccia-alla-radioattivita-un-progetto-scolastico-per-bergamoscienza/)**, un'iniziativa educativa sviluppata da **FabLab Bergamo**, con l'obiettivo di creare un rilevatore di radioattività economico e accessibile per scopi didattici.

**Obiettivi del progetto:**
- Dimostrare tecniche di misurazione della radioattività in modo pratico
- Fornire esperienza hands-on con elettronica, programmazione e fisica
- Spiegare principi di schermatura dalle radiazioni e legge dell'inverso del quadrato
- Creare strumento riproducibile per educazione scientifica STEM
- Rendere accessibile la misurazione di radiazioni con hardware economico (<€50)

**Risultati sul campo:**
Durante i test nell'area mineraria di Novazza, il dispositivo ha rilevato con successo campioni di minerali contenenti uranio, misurando livelli di radiazione da **0.08 a 7 µSv/h**, dimostrando efficacia per applicazioni didattiche reali e ricerca geologica di base.

### Due Implementazioni Disponibili

Il progetto offre **due implementazioni** complementari:
- **MicroPython**: Implementazione standalone con display base e funzionalità essenziali, utilizzata per sviluppo iniziale e validazione
- **ESPHome**: Versione avanzata con integrazione Home Assistant, grafico a barre e display migliorato

![Sviluppo MicroPython](images/thonny-2-1-1024x629.jpg)
*Versione MicroPython in sviluppo con Thonny IDE, mostrando il codice sorgente e il plotter in tempo reale delle misurazioni*

## Hardware

### Componenti Principali

- **Microcontrollore**: ESP32 LILYGO T-Display (~€9) - [Sito ufficiale](https://lilygo.cc/products/lilygo%C2%AE-ttgo-t-display-1-14-inch-lcd-esp32-control-board)
- **Display**: ST7789 TFT 240x135 pixel (integrato nella board T-DISPLAY)
- **Rilevatore di radiazioni**: CAJOE RadiationD v1.1 (~€30)
- **Tubo Geiger**: J305β (incluso nel kit CAJOE)
- **Battery pack**: 10000mAh raccomandato per uso portatile
- **Case**: Custodia stampabile 3D (file STL incluso)

**Costo totale stimato:** ~€40-50 (escluso case e battery pack)

### Collegamento Pin ESP32

#### Display ST7789 (pin nativi LILYGO T-DISPLAY)
- SCLK: Pin 18
- MOSI: Pin 19  
- MISO: Pin 2
- CS: Pin 5
- DC: Pin 16
- RST: Pin 23
- BL (Backlight): Pin 4

*Nota: I pin del display corrispondono alla configurazione nativa della board LILYGO T-DISPLAY, rendendo il collegamento plug-and-play.*

#### Rilevatore CAJOE
- Segnale impulsi: Pin 26 (interrupt fronte di discesa)

![Forma impulso Geiger](images/impulso_geiger.png)
*Forma d'onda tipica dell'impulso dal tubo Geiger misurata con oscilloscopio. Il segnale mostra un impulso negativo con durata ~338µs utilizzato per il conteggio degli eventi di radiazione.*

### Alimentazione

Il kit contatore può essere alimentato a 5V dall'ESP32 a sua volta alimentato tramite USB. Per trasportare il contatore si può utilizzare un battery pack per telefono collegato all'ESP32.

#### Connessioni tra ESP32 e Kit Contatore
Sono necessari 3 fili di connessione dai morsetti P3:
- **+5V**: Alimentazione positiva
- **GND**: Massa/Ground
- **IMPULSO**: Segnale impulsi (VIN sul circuito PCB)

## Specifiche Tubo Geiger J305β

- **Produttore**: North Optic
- **Rilevazione**: Radiazioni β e γ
- **Dimensioni**: 111mm x 11mm (diametro)
- **Tensione operativa**: 350V (raccomandato), plateau 360-440V
- **Sensibilità γ (Co-60)**: 65 cps/(μR/s)
- **Sensibilità equivalente Sievert**: 108 cpm/(μSv/h)
- **CPM massimo**: 30.000
- **Rumore di fondo**: ~12 CPM

### Fattore di Conversione per Dose Assorbita

Il fattore di conversione utilizzato nel codice è **0.00332 µSv/h per CPM**, specificamente per la **dose assorbita** di radiazioni gamma. Questo valore è derivato dalle specifiche tecniche del tubo J305β e rappresenta la conversione da conteggi per minuto (CPM) alla dose equivalente assorbita in microsievert per ora (µSv/h).

## Funzionalità Software

### Caratteristiche Principali

- **Misurazione in tempo reale**: Aggiornamento ogni 5 secondi
- **Media a lungo termine**: Calcolo su base di 1 minuto
- **Display grafico**: 
  - Letture attuali e mediate in µSv/h
  - Simbolo di radioattività animato
  - Indicatore di attività (pixel lampeggiante)
- **Ottimizzazione prestazioni**: Funzioni critiche ottimizzate con `@micropython.native`

### Algoritmo di Misurazione

1. **Conteggio impulsi**: Interrupt hardware su fronte di discesa dal tubo J305
2. **Calcolo CPM**: Conteggio impulsi × 12 (per intervalli di 5 secondi)
3. **Conversione dose assorbita**: CPM × 0.00332 = µSv/h
4. **Display**: Visualizzazione simultanea di valori istantanei e mediati

### Timers

- **Timer 0**: Aggiornamento display ogni 5 secondi
- **Timer 1**: Calcolo media ogni 60 secondi

## Struttura del Progetto

```
contatore-geiger/
├── boot.py                    # Script di avvio MicroPython
├── geiger.py                  # Applicazione principale MicroPython
├── lib/                       # Librerie hardware per MicroPython
│   ├── st7789.py             # Driver display ST7789
│   ├── xglcd_font.py         # Sistema font X-GLCD
│   └── sysfont.py            # Font di sistema
├── esphome/                   # Implementazione ESPHome ⭐
│   ├── esphome-lilygo-tdisplay-cajoe-geiger.yaml  # Config ESPHome
│   └── README.md             # Documentazione ESPHome dettagliata
├── fonts/                     # File font
│   └── Unispace12x24.c       # Font Unispace 12x24
├── images/                    # Immagini documentazione
│   ├── rilevatore-con-battery-pack-1024x768.jpg
│   ├── impulso_geiger.png
│   └── thonny-2-1-1024x629.jpg
├── 3d-enclosure/             # Custodia stampabile 3D
│   ├── Case.stl              # File STL per stampa 3D
│   └── LICENCE.MD            # Licenza custodia (by @nick_375545)
├── doc/                      # Documentazione tecnica
│   ├── fonts/                # Font di backup
│   │   └── Unispace12x24.c
│   └── scheda BergamoScienza.pdf  # Scheda tecnica completa
├── measurements/             # Dati sperimentali
│   └── grafico radiazione - distanza.pdf  # Grafici validazione
├── README.md                 # Questo file (documentazione principale)
├── CLAUDE.md                 # Guida per Claude Code AI
└── LICENSE                   # Licenza del progetto
```

**⭐ Raccomandato**: Per la maggior parte degli utenti, l'implementazione **ESPHome** è consigliata per la sua facilità d'uso, integrazione con Home Assistant, e funzionalità avanzate. Vedere [esphome/README.md](esphome/README.md) per documentazione completa.

## Implementazioni

### Versione MicroPython
L'implementazione MicroPython (`boot.py`, `geiger.py`) offre:
- Funzionamento standalone senza dipendenze esterne
- Display base con valori numerici e simbolo radioattivo
- Algoritmo di misurazione ottimizzato per performance
- Ideale per uso educativo e dimostrativo

### Versione ESPHome
L'implementazione ESPHome (`esphome/`) aggiunge:
- **Integrazione Home Assistant**: Sensori automatici e dashboard
- **Display avanzato**: Grafico a barre tempo reale con cronologia
- **OTA Updates**: Aggiornamenti firmware wireless
- **Scala logaritmica**: Visualizzazione ottimizzata per range radiazioni
- **Media mobile**: Buffer circolare per stabilità delle letture

Per dettagli completi vedere: [`esphome/README.md`](esphome/README.md)

## Custodia 3D

Il progetto include una custodia stampabile in 3D progettata per contenere l'elettronica del contatore Geiger:

- **File**: `3d-enclosure/Case.stl`
- **Autore**: @nick_375545
- **Fonte**: [Printables - Geiger Counter Kit Case](https://www.printables.com/model/635037-giger-counter-kit-case)
- **Attribuzione**: Custodia 3D creata da @nick_375545, disponibile su Printables.com
- **Licenza**: Consultare il file `3d-enclosure/LICENCE.MD` per i dettagli sulla licenza

## Documentazione e Misurazioni

### Documentazione Tecnica
- `doc/scheda BergamoScienza - BRUNOT.pdf`: Scheda tecnica completa del progetto per BergamoScienza

### Dati Sperimentali
- `measurements/grafico radiazione - distanza.pdf`: Grafici delle misurazioni sperimentali che mostrano la relazione tra intensità di radiazione e distanza dalla sorgente

## Installazione e Configurazione

### Prerequisiti

1. **Firmware MicroPython** installato su ESP32
2. **File font** nella directory `fonts/`:
   - `fonts/Unispace12x24.c`

### Procedura di Deploy

1. Collegare l'hardware secondo lo schema pin
2. Caricare tutti i file Python sul filesystem ESP32:
   - `boot.py`
   - `geiger.py`  
   - `lib/st7789.py`
   - `lib/xglcd_font.py`
   - `lib/sysfont.py`
3. Caricare i file font nella directory `fonts/`
4. Riavviare il dispositivo

### Calibrazione

Il fattore di conversione per dose assorbita (0.00332) è derivato dalle specifiche del tubo J305β e può richiedere calibrazione con sorgenti note per massima precisione nelle misurazioni di dose.

## Compatibilità CAJOE

Questo progetto è specificamente progettato per il modulo CAJOE RadiationD v1.1 con tubo J305, basato sul progetto:
- **Repository GitHub**: [SensorsIot/Geiger-Counter-RadiationD-v1.1-CAJOE-](https://github.com/SensorsIot/Geiger-Counter-RadiationD-v1.1-CAJOE-)
- **Video tutorial**: https://youtu.be/K28Az3-gV7E

## Sicurezza e Uso Educativo

### Protocolli di Sicurezza

**Sicurezza elettrica:**
- Il tubo Geiger J305 opera ad alta tensione (350-450V)
- Seguire sempre le precauzioni di sicurezza per alta tensione
- Non aprire il modulo CAJOE se non si è competenti con alta tensione

**Sicurezza radiologica:**
Quando si lavora con materiali radioattivi, anche a bassa intensità:
- Mantenere sempre la distanza massima possibile dalle sorgenti
- La distanza è il metodo primario di protezione dalle radiazioni
- Seguire le linee guida per la manipolazione di campioni minerali
- Non raccogliere o conservare materiali radioattivi senza adeguate precauzioni e autorizzazioni

### Applicazioni Didattiche

Il dispositivo è ideale per:
- Dimostrazioni in classe di fisica delle radiazioni
- Progetti STEM di elettronica e programmazione
- Misurazioni ambientali di radiazioni di fondo naturali
- Studio pratico della legge dell'inverso del quadrato
- Esperimenti su schermatura dalle radiazioni (piombo, alluminio, etc.)
- Ricerca geologica di base e mineralogica

### Range Tipici di Misurazione

- **Radiazione di fondo naturale**: 0.08-0.30 µSv/h
- **Materiali da costruzione (granito, tufo)**: 0.10-0.50 µSv/h
- **Minerali contenenti uranio (campioni geologici)**: 1.0-20+ µSv/h
- **Limite raccomandato esposizione pubblica**: <1 mSv/anno (equivalente a ~0.11 µSv/h continua)

**Nota importante:** Per misurazioni critiche di dose in ambito professionale o dosimetria personale, utilizzare strumentazione certificata e calibrata.

## Note Tecniche

### Dose Assorbita vs Altri Tipi di Misurazione

Il fattore di conversione 0.00332 è specificamente calibrato per la **dose assorbita** (absorbed dose) in tessuti biologici. Altri fattori di conversione potrebbero essere necessari per:
- Dose equivalente (equivalent dose)
- Rateo di dose nell'aria (air kerma rate)
- Intensità di sorgente radioattiva

### Riferimenti

1. IoT-devices LLC - "Geiger tube J305: How to calculate the conversion factor"
2. GitHub - SensorsIot Geiger Counter project  
3. J305 Geiger Tube Specification datasheet
4. RadMon.org - Conversion factors database

## Riproducibilità e Open Source

Questo progetto è completamente **open source e riproducibile**:

- **Codice sorgente completo**: Tutte le implementazioni (MicroPython ed ESPHome) sono disponibili in questo repository
- **Lista materiali dettagliata**: Tutti i componenti sono facilmente reperibili online a basso costo
- **Documentazione completa**: Istruzioni passo-passo per assemblaggio, configurazione e calibrazione
- **File 3D inclusi**: Case stampabile per protezione hardware
- **Dati sperimentali**: Misurazioni reali e grafici per validazione
- **Community support**: Contributi, miglioramenti e issue benvenuti

### Risorse Aggiuntive

- **Articolo completo**: [Caccia alla radioattività - FabLab Bergamo](https://www.fablabbergamo.it/2025/10/05/caccia-alla-radioattivita-un-progetto-scolastico-per-bergamoscienza/)
- **BergamoScienza**: Iniziativa educativa che ha ispirato questo progetto
- **FabLab Bergamo**: Laboratorio di fabbricazione digitale che supporta progetti STEM

### Contributi

Il progetto accoglie contributi dalla community:
- Miglioramenti al codice
- Ottimizzazioni hardware
- Nuove funzionalità
- Traduzioni documentazione
- Report di misurazioni sul campo

## Crediti e Licenza

**Progetto educativo per BergamoScienza**
- **Sviluppatore principale**: Alex Brunot
- **Organizzazione**: FabLab Bergamo
- **Iniziativa**: BergamoScienza

**Ringraziamenti:**
- @nick_375545 per il design della custodia 3D
- SensorsIot per il progetto base CAJOE
- Community MicroPython ed ESPHome

**Licenza:** Il codice è basato su librerie open source per MicroPython. Consultare il file LICENSE per dettagli.