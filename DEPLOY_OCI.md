# Despliegue en Oracle Cloud (OCI) — Always Free

Guía paso a paso para correr `alura-agente` de forma persistente en una
instancia gratuita de Oracle Cloud Compute.

> ⚠️ Nota: durante 2026 Oracle ha modificado varias veces los límites del
> Always Free tier para instancias Ampere A1 (algunos reportes hablan de
> 4 OCPU/24 GB, otros de 2 OCPU/12 GB). Revisa en tu consola de OCI, sección
> **Governance & Administration → Tenancy Details → Always Free**, cuánto
> tienes disponible exactamente. Para esta app (ligera) con **1 OCPU y 6 GB
> de RAM sobra de sobra**.

## 1. Crear la instancia de cómputo

1. En la consola de OCI: **Compute → Instances → Create Instance**.
2. **Image:** Canonical Ubuntu (24.04), arquitectura según el shape que elijas.
3. **Shape:** elige `VM.Standard.A1.Flex` (Ampere/ARM) o `VM.Standard.E2.1.Micro`
   (AMD) — cualquiera de los dos "Always Free" funciona para esta app.
4. **Add SSH keys:** selecciona "Generate a key pair for me" y descarga la
   llave privada (`.pem`). Guárdala, no se puede volver a descargar.
5. Deja el resto en valores por defecto (VCN nueva, IP pública asignada) y
   crea la instancia. Anota la **IP pública** una vez que esté "Running".

## 2. Abrir el puerto de la app (8501)

Por defecto solo el puerto 22 (SSH) está abierto. Hay que abrir dos capas:

**A) Security List / Network Security Group (firewall de OCI):**
1. Ve a la VCN de tu instancia → **Security Lists** → la lista por defecto.
2. **Add Ingress Rule:**
   - Source CIDR: `0.0.0.0/0`
   - IP Protocol: TCP
   - Destination Port Range: `8501`

**B) Firewall del sistema operativo (dentro de la VM, más abajo en el paso 4).**

## 3. Conectarte por SSH

```bash
chmod 400 ruta/a/tu-llave.pem
ssh -i ruta/a/tu-llave.pem ubuntu@<IP_PUBLICA>
```

## 4. Instalar dependencias en la instancia

```bash
sudo apt update && sudo apt install -y python3-pip python3-venv git

# Abrir el puerto también en el firewall interno de Ubuntu (iptables)
sudo iptables -I INPUT -p tcp --dport 8501 -j ACCEPT
sudo netfilter-persistent save   # si no existe, instala con: sudo apt install -y iptables-persistent
```

## 5. Clonar el repo y preparar el entorno

```bash
git clone <url-de-tu-repo>
cd alura-agente

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Sube tus archivos CSV reales a la carpeta `data/` (por ejemplo con `scp`
desde tu computadora, o `git clone` si ya los subiste al repo).

## 6. Configurar tu API Key de Groq

```bash
mkdir -p .streamlit
nano .streamlit/secrets.toml
```

Pega dentro:
```toml
GROQ_API_KEY = "tu_api_key_de_groq"
```

Guarda con `Ctrl+O`, `Enter`, `Ctrl+X`.

## 7. Probar que corre

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Abre en tu navegador: `http://<IP_PUBLICA>:8501`. Si carga el chat, funciona.
Detén la prueba con `Ctrl+C`.

## 8. Dejarlo corriendo de forma persistente (systemd)

Para que la app siga viva aunque cierres la sesión SSH o se reinicie el
servidor:

```bash
sudo nano /etc/systemd/system/alura-agente.service
```

Pega (ajusta las rutas según tu usuario/carpeta):

```ini
[Unit]
Description=Alura Agente - Streamlit
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/alura-agente
ExecStart=/home/ubuntu/alura-agente/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Actívalo:

```bash
sudo systemctl daemon-reload
sudo systemctl enable alura-agente
sudo systemctl start alura-agente
sudo systemctl status alura-agente   # debe decir "active (running)"
```

Desde ahora, `http://<IP_PUBLICA>:8501` queda disponible de forma
permanente, y se reinicia solo si el servidor se reinicia o la app falla.

## 9. (Opcional) Dominio propio + HTTPS

Si más adelante quieres una URL bonita con `https://` en vez de
`http://IP:8501`, se hace con **Nginx como proxy inverso + Certbot** apuntando
un dominio propio al puerto 443 → 8501. Es un paso adicional, no
indispensable para que el agente funcione y sea accesible.

## Comandos útiles para mantenimiento

```bash
sudo systemctl restart alura-agente   # reiniciar la app
sudo systemctl status alura-agente    # ver estado
journalctl -u alura-agente -f         # ver logs en vivo
```
