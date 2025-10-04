# Specifica Tecnica: Contatore Geiger ESPHome (LILYGO T-Display + CAJOE)

Questo documento è ottimizzato per la generazione automatica (one-shot) di un firmware professionale.

## 1. Architettura Hardware
*   **Device**: LILYGO T-Display (ESP32).
*   **Nome**: `geiger-tdisplay` (evitare underscore).
*   **Framework**: `esp-idf`.
*   **SPI BUS**: `clk_pin: 18`, `mosi_pin: 19`.
*   **Display**: `mipi_spi` (ST7789), `cs: 5`, `dc: 16`, `rotation: 90`.
*   **Backlight**: Configurare `output: ledc` su `GPIO4` e integrarlo come componente `light` (monochromatic).
*   **Sensore Geiger**: `pulse_counter` su `GPIO26`, `falling_edge`, aggiornamento ogni 1s.

## 2. Configurazione Servizi (ESPHome 2024+)
*   **OTA**: Deve includere la piattaforma:
    ```yaml
    ota:
      - platform: esphome
    ```
*   **API**: Abilitata per Home Assistant.
*   **Logger**: Abilitato.

## 3. Logica di Calcolo (Fondamentale)
*   **Conversione**: 1 CPM = 0.00332 µSv/h.
*   **Media Mobile 60s**:
    *   Creare un array globale `std::array<float, 60>` e una variabile `sum`.
    *   Ogni secondo: `nuova_somma = vecchia_somma - valore_vecchio + valore_nuovo`.
    *   Il sensore template `Radiation 1min` deve restituire `(sum / 60.0) * 0.00332`.
*   **Storico Grafico**: Array `std::array<float, 25>` che memorizza la media degli ultimi 5 secondi.

## 4. Interfaccia Grafica (UI Avanzata)
*   **Colori**: Sfondo Nero, Testo Bianco, Accenti Gialli.
*   **Simbolo Radioattivo**: Disegnare un cerchio giallo di sfondo, tre pale nere a 120° (usando cicli e trigonometria sin/cos per precisione) e un cerchio centrale nero.
*   **Valore Numerico**: Visualizzare la media 1min con 2 decimali e l'unità "µSv/h".
*   **Grafico a Barre**:
    *   240x70 pixel nella metà inferiore.
    *   Scala **Logaritmica** (0.08 a 20 µSv/h).
    *   Linee di riferimento orizzontali per 0.1, 1, 10 µSv/h con etichette grigie.
    *   Colori barre: Verde (<1.0), Arancione (1-5), Rosso (>5).

## 5. Prompt per l'AI
> "Genera il codice ESPHome per un contatore Geiger su LILYGO T-Display. È fondamentale che il blocco 'ota' includa '- platform: esphome'. Usa GPIO26 per gli impulsi. Implementa una vera media mobile a 60 secondi con buffer circolare e aggiornamento al secondo. Il display deve mostrare un grafico a barre logaritmico (0.1-20 uSv/h) con linee di riferimento e un simbolo radioattivo disegnato correttamente via lambda. Usa 'ledc' per il backlight su GPIO4."
