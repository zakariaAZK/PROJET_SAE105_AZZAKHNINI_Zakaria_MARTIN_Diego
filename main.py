#AZZAKHNINI Zakaria & MARTIN Diego - SAE15 Traitement des données, Projet 18 : aider un enseignant à partir en week-end

#Importation des modules nécessaires
import os, sys
import csv
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

#Vérifie si le fichier csv existe, sinon ca converti le fichier cis en csv
if os.path.isfile("Calendar.csv")==False:
    from csv_ical import Convert
    convert=Convert()
    convert.CSV_FILE_LOCATION='Calendar.csv'
    convert.SAVE_LOCATION='ADECal.ics'
    convert.read_ical(convert.SAVE_LOCATION)
    convert.make_csv()
    convert.save_csv(convert.CSV_FILE_LOCATION)

#Programme principal

#On créer une liste calendrier vide dans lequel seront les données du fichier csv à analyser
calendrier=[]
#Demande à l'utilisateur d'entrée le nom de l'enseignant et la date à partir de laquelle faire les recherches
nomEnseignant=input("Entrez le nom de l'enseignant pour lequel effectuer les recherches (sous la forme NOM (PRENOM)) : ")
dateInput=input("Entrez la date à partir de laquelle vous voulez effectuer les recherches sous la forme (JJ MM AAAA) : ")

#Converti la date d'entrée en objet datetime
try:
    userDate=datetime.strptime(dateInput, "%d %m %Y")
except ValueError:
    print("Format de date incorrect.")
    sys.exit()

#On ajoute maitenant dans le calendrier uniquement les cours de l'enseignant après la date renseignée
with open("Calendar.csv", newline='\n', encoding='utf-8') as Calendar:
    reader=csv.reader(Calendar, delimiter=',')
    for row in reader:
        if nomEnseignant in row[3]:
            date_debut=datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S+00:00')
            date_fin=datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S+00:00')
            if date_debut>userDate:
                calendrier.append([row[0], row[3], date_debut, date_fin, row[4]])

if calendrier==[]:
    print("Nom de l'enseignant incorrect ou date en dehors du champs d'analyse")
    sys.exit()

#On trie les jours de la semaine du plus ancien au plus récent
calendrier.sort(key=lambda x: x[2]) #indice 2=date_debut

#Création d'une liste vide weekendTroisJours
weekendTroisJours=[]
#On parcourt les jours du calendrier pour trouver les week-ends de 3 jours ou plus qu'on ajoutera dans la liste weekendTroisJours
for jour in range(1, len(calendrier)):
    duree=calendrier[jour][2]-calendrier[jour-1][3]  #Entre le début du prochain cours [2] et la fin du précédent [3]
    if duree.days>=3:  #Si la durée est supérieure ou égale à trois jours
        debutWeekend=calendrier[jour-1][3]
        finWeekend=calendrier[jour][2]
        dureeWeekendJours=duree.days
        dureeEnHeure=duree.total_seconds()
        dureeWeekendHeure=str(int(dureeEnHeure//3600)) + ":" + str(int((dureeEnHeure%3600)/60))
        weekendTroisJours.append([debutWeekend, finWeekend, dureeWeekendJours, dureeWeekendHeure])

#Affiche les weekend de trois trouvés
for element in weekendTroisJours:
    print(f"Week-end de {element[2]} jours : Du {element[0].strftime('%d/%m/%Y %H:%M')} au {element[1].strftime('%d/%m/%Y %H:%M')}")

#On rentre les résultats dans un fichier .csv et affiche les résultats sous forme d'une frise chronologique
fig, ax=plt.subplots()
fig.set_size_inches(18, 10)
plt.get_current_fig_manager().full_screen_toggle()
#Ecrit les résultats dans un fichier CSV
with open(nomEnseignant+'_Week-end.csv', 'w', newline='', encoding='utf-8') as fichiercsv:
    writer=csv.writer(fichiercsv)
    writer.writerow(['Du', 'Au', 'Durée (jours)', 'Durée (heures)'])
    #Affiche le résultat sous forme de frise chronologique
    for element in weekendTroisJours:
        dateDebutFormat=element[0].strftime("%d/%m/%y %H:%M")
        dateFinFormat=element[1].strftime("%d/%m/%y %H:%M")
        writer.writerow([dateDebutFormat, dateFinFormat, element[2], element[3]])
        ax.plot([element[0], element[1]], [0, 0], color="blue", linewidth=10)
        ax.annotate(element[0].strftime("%d"), (element[0], 0), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)
        ax.annotate(element[1].strftime("%d"), (element[1], 0), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)
fichiercsv.close()
ax.set_xlim(calendrier[0][3], calendrier[-1][2])
ax.xaxis_date()
ax.xaxis.set_major_formatter(DateFormatter("%B %Y"))  
ax.grid(which='both', axis='x', linestyle='--', color='gray', linewidth=1)
ax.set_title(f"Frise chronologique des week-end de 3 jours ou plus de {nomEnseignant}")
ax.set_xlabel("Temps")
ax.set_yticks([])
plt.savefig(nomEnseignant+"_Week-end.png")
plt.show()
