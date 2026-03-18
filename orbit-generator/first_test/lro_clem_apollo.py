import spiceypy as spice
import plotly.express as px
import pandas as pd

# --- 1. CHARGEMENT DES KERNELS ---
spice.furnsh('../kernels/LSK/naif0012.tls')
spice.furnsh('../kernels/SPK/de432s.bsp')
spice.furnsh('../kernels/SPK/lrorg_2025166_2025258_v01.bsp')   # mission LRO
spice.furnsh('../kernels/SPK/clem_ask020625.bsp')      # mission CLEMENTINE
spice.furnsh('../kernels/SPK/a16_subsat_ssd_lp150q.bsp') # mission APOLLO 16

# --- 2. CONFIGURATION DE LA BOUCLE ---

# ---2.1 Pour LRO ---

lro_date_depart = '2025-07-01T12:00:00'
lro_et_debut = spice.str2et(lro_date_depart)

# --- 2.2 Pour CLEMENTINE ---
# on cherche ID de CLEMENTINE 
ids = spice.stypes.SPICEINT_CELL(100)
spice.spkobj('../kernels/SPK/clem_ask020625.bsp', ids)
id_clem = ids[0]

# On va chercher dans le fichier les dates correspondantes aux données enregistrées
cover = spice.stypes.SPICEDOUBLE_CELL(2000)
spice.spkcov('../kernels/SPK/clem_ask020625.bsp', id_clem, cover)
clem_et_debut, clem_et_fin = spice.wnfetd(cover, 0)
clem_date_depart = spice.timout(clem_et_debut, "YYYY-MON-DD HR:MN:SC")

# --- 2.3 Pour APOLLO ---
# on cherche ID de APOLLO 16 Subsatellite
ids = spice.stypes.SPICEINT_CELL(100)
spice.spkobj('../kernels/SPK/a16_subsat_ssd_lp150q.bsp', ids)
id_apollo = ids[0]

# On va chercher dans le fichier les dates correspondantes aux données enregistrées
cover = spice.stypes.SPICEDOUBLE_CELL(2000)
spice.spkcov('../kernels/SPK/a16_subsat_ssd_lp150q.bsp', id_apollo, cover)
apollo_et_debut, apollo_et_fin = spice.wnfetd(cover, 0)
apollo_date_depart = spice.timout(apollo_et_debut, "YYYY-MON-DD HR:MN:SC")

# --- 2.4 Paramètres de la boucle ---
nombre_de_points = 200
# Intervalle entre chaque point en secondes
pas_en_secondes = 60 

# listes pour enregistrer les données 
lro_data_list = []
clem_data_list = []
apollo_data_list = []

print(f"--- Calcul de trajectoire pour LRO (départ : {lro_date_depart}) ---")
print(f"{'DATE UTC':<25} | {'ALTITUDE (km)':<15} | {'X':<10} | {'Y':<10} | {'Z'}")
print("-" * 80)

# --- 3. BOUCLE DE CALCUL ---
for i in range(nombre_de_points):
    
    # CALCUL DU TEMPS : On ajoute 'i' fois l'intervalle au temps de départ
    lro_et_actuel = lro_et_debut + (i * pas_en_secondes)
    
    try:
        # Calcul de la position
        lro_position, _ = spice.spkpos('-85', lro_et_actuel, 'J2000', 'NONE', 'MOON')
        
        # Calcul distance et altitude
        lro_distance = spice.vnorm(lro_position)
        lro_altitude = lro_distance - 1737.4
        
        # On reconvertit le temps machine en texte lisible pour l'affichage
        lro_date_lisible = spice.timout(lro_et_actuel, "YYYY-MON-DD HR:MN:SC")

        lro_data_list.append({
            'Date': lro_date_lisible,
            'X': lro_position[0],
            'Y': lro_position[1],
            'Z': lro_position[2],
            'Altitude': lro_altitude
        })
        
        print(f"{lro_date_lisible:<25} | {lro_altitude:<15.2f} | {lro_position[0]:<10.0f} | {lro_position[1]:<10.0f} | {lro_position[2]:.0f}")

    except spice.stypes.SpiceyError:
        print("Données manquantes pour ce point précis.")

print(f"--- Calcul de trajectoire pour CLEMENTINE (départ : {clem_date_depart}) ---")
print(f"{'DATE UTC':<25} | {'ALTITUDE (km)':<15} | {'X':<10} | {'Y':<10} | {'Z'}")
print("-" * 80)

nombre_de_points = 500

for i in range(nombre_de_points):
    
    # CALCUL DU TEMPS : On ajoute 'i' fois l'intervalle au temps de départ
    clem_et_actuel = clem_et_debut + (i * pas_en_secondes)
    
    try:
        # Calcul de la position
        clem_position, _ = spice.spkpos(str(id_clem), clem_et_actuel, 'J2000', 'NONE', 'MOON')
        
        # Calcul distance et altitude
        clem_distance = spice.vnorm(clem_position)
        clem_altitude = clem_distance - 1737.4
        
        # On reconvertit le temps machine en texte lisible pour l'affichage
        clem_date_lisible = spice.timout(clem_et_actuel, "YYYY-MON-DD HR:MN:SC")

        clem_data_list.append({
            'Date': clem_date_lisible,
            'X': clem_position[0],
            'Y': clem_position[1],
            'Z': clem_position[2],
            'Altitude': clem_altitude
        })
        
        print(f"{clem_date_lisible:<25} | {clem_altitude:<15.2f} | {clem_position[0]:<10.0f} | {clem_position[1]:<10.0f} | {clem_position[2]:.0f}")

    except spice.stypes.SpiceyError:
        print("Données manquantes pour ce point précis.")

print(f"--- Calcul de trajectoire pour APOLLO (départ : {apollo_date_depart}) ---")
print(f"{'DATE UTC':<25} | {'ALTITUDE (km)':<15} | {'X':<10} | {'Y':<10} | {'Z'}")
print("-" * 80)

nombre_de_points = 500

for i in range(nombre_de_points):
    
    # CALCUL DU TEMPS : On ajoute 'i' fois l'intervalle au temps de départ
    apollo_et_actuel = apollo_et_debut + (i * pas_en_secondes)
    
    try:
        # Calcul de la position
        apollo_position, _ = spice.spkpos(str(id_apollo), apollo_et_actuel, 'J2000', 'NONE', 'MOON')
        
        # Calcul distance et altitude
        apollo_distance = spice.vnorm(apollo_position)
        apollo_altitude = apollo_distance - 1737.4
        
        # On reconvertit le temps machine en texte lisible pour l'affichage
        apollo_date_lisible = spice.timout(apollo_et_actuel, "YYYY-MON-DD HR:MN:SC")

        apollo_data_list.append({
            'Date': apollo_date_lisible,
            'X': apollo_position[0],
            'Y': apollo_position[1],
            'Z': apollo_position[2],
            'Altitude': apollo_altitude
        })

        print(f"{apollo_date_lisible:<25} | {apollo_altitude:<15.2f} | {apollo_position[0]:<10.0f} | {apollo_position[1]:<10.0f} | {apollo_position[2]:.0f}")

    except spice.stypes.SpiceyError:
        print("Données manquantes pour ce point précis.")



# On transforme la liste en DataFrame Pandas
lro_df = pd.DataFrame(lro_data_list)
clem_df = pd.DataFrame(clem_data_list)
apollo_df = pd.DataFrame(apollo_data_list)

# On vérifie qu'on a bien des données
if not lro_df.empty and not clem_df.empty and not apollo_df.empty:
    print(f"Génération du graphique avec {len(lro_df)} points de LRO, {len(clem_df)} points de CLEMENTINE et {len(apollo_df)} points d'APOLLO...")

    # Création du graphique 3D
    fig = px.scatter_3d(
        lro_df, 
        x='X', 
        y='Y', 
        z='Z',
        color='Altitude',        # La couleur change selon l'altitude (très utile pour les orbites)
        hover_data=['Date'],     # Affiche la date quand on passe la souris sur un point
        title='Trajectoire LRO, CLEMENTINE et APOLLO autour de la Lune (J2000)',
        labels={'Altitude': 'Alt (km)'}
    )
    # Ajout des données de CLEMENTINE au même graphique
    fig.add_trace(
        px.scatter_3d(
            clem_df, 
            x='X', 
            y='Y', 
            z='Z',
            color='Altitude',
            hover_data=['Date']
        ).data[0]
    )

    fig.add_trace(
        px.scatter_3d(
            apollo_df, 
            x='X', 
            y='Y', 
            z='Z',
            color='Altitude',
            hover_data=['Date']
        ).data[0]
    )

    # Pour garder les proportions réelles (sinon l'orbite peut paraître écrasée)
    # Note : Cela force les axes X, Y, Z à avoir la même échelle
    fig.update_layout(scene=dict(aspectmode='data'))

    fig.show()
else:
    print("Aucune donnée n'a été calculée, vérifiez les dates ou les kernels.")

# --- 4. NETTOYAGE ---
spice.kclear()