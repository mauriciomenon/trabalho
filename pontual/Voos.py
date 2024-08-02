import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

flights = [
    {"type": "ida", "companhia": "LATAM", "saida": "9:50", "origem": "IGU",
        "chegada": "12:25", "destino": "SDU", "status": ""},
    {"type": "ida", "companhia": "LATAM", "saida": "9:50", "origem": "IGU",
        "chegada": "13:20", "destino": "SDU", "status": ""},
    {"type": "ida", "companhia": "AZUL", "saida": "9:55", "origem": "IGU",
        "chegada": "13:55", "destino": "SDU", "status": ""},
    {"type": "ida", "companhia": "AZUL", "saida": "11:05", "origem": "IGU",
        "chegada": "16:20", "destino": "SDU", "status": ""},
    {"type": "ida", "companhia": "GOL", "saida": "11:40", "origem": "IGU",
        "chegada": "15:15", "destino": "SDU", "status": ""},
    {"type": "volta", "companhia": "LATAM", "saida": "10:55",
        "origem": "SDU", "chegada": "15:00", "destino": "IGU", "status": ""},
    {"type": "volta", "companhia": "GOL", "saida": "10:30", "origem": "SDU",
        "chegada": "14:40", "destino": "IGU", "status": ""},
    {"type": "volta", "companhia": "AZUL", "saida": "08:00",
        "origem": "SDU", "chegada": "14:15", "destino": "IGU", "status": ""},
]

# Converting departure times to minutes from midnight
for flight in flights:
    departure_time = datetime.strptime(flight["saida"], "%H:%M")
    flight["saida_min"] = departure_time.hour * 60 + departure_time.minute

df = pd.DataFrame(flights)
df["Rota"] = df["origem"] + " -> " + df["destino"]

plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")
sns.barplot(x="Rota", y="saida_min", hue="companhia", data=df)
plt.title("Horários de Saída dos Voos")
plt.xlabel("Rota")
plt.ylabel("Horário de Saída (minutos desde a meia-noite)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
