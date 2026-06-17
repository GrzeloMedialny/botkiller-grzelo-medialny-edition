# 🛡️ BotKiller v0.2 – Grzelo Medialny Edition

Program do monitorowania połączeń sieciowych i blokowania podejrzanych adresów IP w systemie Windows.

## 🔧 Funkcje
- Graficzny interfejs (Tkinter)
- Ręczne i automatyczne skanowanie (co 5 min)
- Wykrywanie połączeń do krajów: **RU, CN, KP, IR**
- Blokowanie IP w zaporze systemowej (`netsh advfirewall`)
- Eksport wyników do pliku `botkiller_log.txt`

## 📦 Wymagania
- Python 3.9+
- Moduły: `psutil`, `requests`, `tkinter` (standardowy)

Instalacja zależności (jeśli potrzeba):

```bash
pip install psutil requests










