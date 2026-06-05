# Laboratorio 2: Ataque Man-in-the-Middle mediante ARP Spoofing

## 🎥 Enlace del Video Demostrativo
[Haz clic aquí para ver la demostración del laboratorio en Google Drive](https://drive.google.com/file/d/133WZwU5Wd1kbzju3D_GaxZqj-_GbuN90/view?usp=sharing)

---

## 1. Objetivo del Laboratorio
El propósito de esta práctica es demostrar cómo un atacante puede interceptar de forma transparente el tráfico de red local entre dos nodos legítimos aprovechando la ausencia de mecanismos de autenticación inherentes al protocolo ARP (Address Resolution Protocol), analizando su impacto y estudiando las tecnologías de mitigación correspondientes.

---

## 2. Objetivo del Script
El script automatiza un envenenamiento ARP bidireccional enviando tramas falsas (ARP Reply) de manera periódica. El objetivo es alterar la tabla caché de la víctima para que asocie la IP del Gateway con la dirección MAC del atacante, y simultáneamente alterar la tabla del Router para que asocie la IP de la víctima con la MAC del atacante. Adicionalmente, el script habilita el reenvío de IPs (`ip_forward`) en el kernel de Linux para garantizar que la comunicación fluya sin interrupciones, permitiendo el espionaje pasivo.

### Parámetros Configurados:
* **IP de la Víctima (PC1):** `10.24.21.3`
* **MAC de la Víctima (PC1):** `00:50:79:66:68:00`
* **IP del Router (Gateway R1):** `10.24.21.1`
* **MAC del Router (Gateway R1):** `ca:01:53:fc:00:00`
* **Interfaz de Red:** `eth0`

---

## 3. Documentación de la Red
* **Matrícula del Estudiante:** 2024-2421
* **Segmento de Red:** `10.24.21.0/24`
* **Router R1:** Interfaz FastEthernet0/0, dirección IP `10.24.21.1`.
* **Atacante (Kali Linux):** Interfaz eth0, dirección IP `10.24.21.2`.
* **Víctima (PC1 - VPCS):** Dirección IP `10.24.21.3`.

---

## 4. Capturas de Pantalla / Evidencias
<img width="938" height="679" alt="image" src="https://github.com/user-attachments/assets/0a2bd3e6-1374-4648-82ea-fb81e4d56e0d" />

<img width="735" height="618" alt="image" src="https://github.com/user-attachments/assets/43a317f6-3c4d-42f2-b6f2-bceba58c6a66" />



---

## 5. Medidas Técnicas de Mitigación (Hardening)
Para neutralizar ataques de suplantación ARP en redes empresariales, es obligatorio implementar seguridad de Capa 2 en los switches de distribución y acceso:

1. **DHCP Snooping:** El switch analiza los mensajes DHCP legítimos y construye una tabla de base de datos vinculando de forma segura las direcciones MAC con las direcciones IP asignadas dinámicamente, catalogando los puertos de usuarios como "no confiables".
2. **Dynamic ARP Inspection (DAI):** Utilizando la base de datos de DHCP Snooping, el switch intercepta e inspecciona cada paquete ARP que transita por sus puertos. Si una respuesta ARP intenta suplantar una IP o contiene una MAC que no coincide con el registro legítimo, el switch descarta la trama inmediatamente e incrementa el contador de alertas de seguridad.

### Comandos de Configuración en Equipos Cisco:
```text
Switch(config)# ip dhcp snooping
Switch(config)# ip dhcp snooping vlan 1
Switch(config)# ip arp inspection vlan 1
