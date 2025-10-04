from xglcd_font import XglcdFont
from st7789 import color565
from machine import Pin, Timer
from esp32 import PCNT
from time import sleep
import math

@micropython.native
def init_display():
    from machine import Pin, SoftSPI
    from st7789 import ST7789
    SCLK_Pin = 18  #clock pin
    MOSI_Pin = 19  #mosi pin
    MISO_Pin = 2   #miso pin
    RESET_Pin = 23 #reset pin
    DC_Pin = 16    #data/command pin
    CS_Pin = 5     #chip select pin
    BL_Pin = 4     # backlight
    BLK = Pin(BL_Pin, Pin.OUT)
    BLK.value(1)
    spi = SoftSPI(baudrate=40000000, miso=Pin(MISO_Pin), mosi=Pin(MOSI_Pin, Pin.OUT), sck=Pin(SCLK_Pin, Pin.OUT))
    display = ST7789(spi, 135, 240, cs=Pin(CS_Pin), dc=Pin(DC_Pin), rst=None)
    display.fill(0)
    return display

def print_text(x, y, testo, colore=color565(255,255,255)):
    global font, display
    display.draw_text(y, 240-x, testo, font, colore, landscape=True)    

def rettangolo(x, y, larghezza, lunghezza, colore):
    global display
    display.fill_rectangle(y, 240-x, lunghezza, larghezza, colore)

@micropython.native
def draw_radioactive_symbol(cx, cy, size, colore):
    """Disegna il simbolo di radioattività"""
    global display
    
    # Raggio esterno e interno
    outer_radius = size // 2
    inner_radius = size // 6
    blade_width = 50  # Larghezza angolare delle pale in gradi
    
    # Disegna il cerchio centrale
    for x in range(-inner_radius, inner_radius + 1):
        for y in range(-inner_radius, inner_radius + 1):
            if x*x + y*y <= inner_radius * inner_radius:
                px = cx + x
                py = cy + y
                if 0 <= px < 135 and 0 <= py < 240:
                    display.pixel(py, 240 - px, colore)
    
    # Disegna le tre pale a 0°, 120° e 240°
    for base_angle in [90, 210, 330]:  # Angoli delle pale
        for r in range(inner_radius + 2, outer_radius + 1):
            for angle_offset in range(-blade_width//2, blade_width//2 + 1):
                angle = math.radians(base_angle + angle_offset)
                x = int(cx + r * math.cos(angle))
                y = int(cy + r * math.sin(angle))
                if 0 <= x < 135 and 0 <= y < 240:
                    display.pixel(y, 240 - x, colore)

font = XglcdFont('fonts/Unispace12x24.c', 12, 24)
display = init_display()
print_text(0,0,'Contatore GEIGER', color565(255,0,255))

# Disegna il simbolo di radioattività in basso a sinistra (giallo)
draw_radioactive_symbol(25, 80, 50, color565(255, 255, 0))

contatore_imp = 0
cont_imp_min = 0

@micropython.native
def impulso(pin):
    global contatore_imp
    global cont_imp_min
    contatore_imp += 1
    cont_imp_min += 1

imp = Pin(26, mode=Pin.IN, pull=None)
imp.irq(trigger=Pin.IRQ_FALLING, handler = impulso)

timer = Timer(0)
timer_min = Timer(1)

radiazione = 0
radiazione_min = 0
cpm = 0

@micropython.native
def on5sec(timer):
    global radiazione, contatore_imp, cpm
    cpm = contatore_imp * 12
    contatore_imp = 0
    radiazione = cpm * 0.00332;
    
@micropython.native
def on1min(timer):
    global radiazione_min, cont_imp_min
    radiazione_min = cont_imp_min * 0.00332
    cont_imp_min = 0

timer.init(mode=Timer.PERIODIC, period = 5000, callback = on5sec)
timer_min.init(mode=Timer.PERIODIC, period = 60000, callback = on1min)

colore = color565(0,0,0)

while True:
    print (round(radiazione, 2), 'µSv/h', round(radiazione_min, 2), 'µSv/h (media)')
    print_text(50,24, f'{round(radiazione, 2)} uSv/ora   ')
    print_text(50,48, f'{round(radiazione_min, 2)} uSv/ora   ')
    
    # Pixel lampeggiante
    display.pixel(239, 1, colore)
    if colore == color565(0,0,0):
        colore = color565(255,255,255)
    else:
        colore = color565(0,0,0)
    sleep(5)
    