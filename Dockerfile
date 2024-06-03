# Etap 1: Budowanie obrazu z zależnościami
FROM python:3.12-alpine AS builder

# Ustawienie katalogu roboczego
WORKDIR /app

# Instalacja narzędzi pomocniczych
RUN apk add --no-cache gcc musl-dev libffi-dev

# Kopiowanie plików konfiguracyjnych i zależności
COPY requirements.txt ./

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Etap 2: Budowanie finalnego obrazu
FROM python:3.12-alpine

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie zbudowanych zależności z etapu 1
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Kopiowanie kodu źródłowego
COPY . .

# Informacje o autorze
LABEL maintainer="Patryk Pawelec"

# Otwieranie portu 5000 (jeśli aplikacja nasłuchuje na tym porcie)
EXPOSE 5000

# Definiowanie polecenia startowego
CMD ["python", "main.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1

