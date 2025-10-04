# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Panoramica del Progetto

Questo è un progetto MicroPython per un sistema di visualizzazione di contatore Geiger basato su ESP32 per BergamoScienza. Il progetto implementa un rilevatore di radiazioni con capacità di visualizzazione in tempo reale utilizzando un display TFT ST7789.

## Architettura

Il codebase è composto da:

- `boot.py` - Script di avvio semplice che importa il modulo principale geiger
- `geiger.py` - Applicazione principale contenente la logica del contatore Geiger, gestione del display e misurazione delle radiazioni
- `lib/` - Moduli libreria per interfacce hardware:
  - `st7789.py` - Driver display TFT ST7789
  - `xglcd_font.py` - Utilità di rendering font per il testo del display
  - `sysfont.py` - Definizioni font di sistema

## Configurazione Hardware

Il progetto è configurato per ESP32 con assegnazioni pin specifiche:
- Display SPI: SCLK=18, MOSI=19, MISO=2, CS=5, DC=16, RST=23, BL=4
- Input rilevatore Geiger: Pin 26 (interrupt fronte di discesa)

## Componenti Principali

### Sistema Display
- Utilizza display TFT ST7789 240x135 con orientamento landscape
- Funzioni di disegno personalizzate: `print_text()`, `rettangolo()`, `draw_radioactive_symbol()`
- Display letture radiazioni in tempo reale con simbolo radioattivo

### Misurazione Radiazioni
- Conteggio impulsi guidato da interrupt dal tubo Geiger
- Modalità di misurazione duale:
  - Intervalli di 5 secondi per calcolo CPM in tempo reale
  - Intervalli di 1 minuto per letture mediate
- Fattore di conversione: 0.00332 µSv/h per CPM

### Timer
- Timer 0: Aggiornamenti periodici di 5 secondi per display tempo reale
- Timer 1: Aggiornamenti periodici di 1 minuto per calcoli medi

## Note di Sviluppo

Questo è un progetto MicroPython progettato per funzionare direttamente su microcontrollori ESP32. Non ci sono comandi tradizionali di build, test o lint poiché si tratta di codice firmware embedded.

Per il deployment:
1. Flash del firmware MicroPython su ESP32
2. Upload di tutti i file Python sul filesystem del dispositivo
3. Assicurarsi che i file font siano disponibili in una directory `fonts/` (referenziati come `fonts/Unispace12x24.c`)
4. Reset del dispositivo per eseguire l'applicazione

Il codice utilizza decoratori nativi MicroPython (`@micropython.native`) per ottimizzazione delle prestazioni su funzioni time-critical.