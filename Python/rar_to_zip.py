import os
import shutil
import patoolib

# --- CONFIGURATION ---
dossier_source_rar = r"./rar"
dossier_tampon = r"./tempo"
dossier_destination_zip = r"./zip_final"
mot_de_passe_rar = "online-fix.me"  # Le mot de passe pour ouvrir les RAR

def verifier_et_creer_dossiers():
    """Vérifie et crée les dossiers nécessaires."""
    dossiers = [dossier_source_rar, dossier_tampon, dossier_destination_zip]
    for dossier in dossiers:
        if not os.path.exists(dossier):
            os.makedirs(dossier)

def nettoyer_dossier_tempo():
    """Vide le dossier tempo pour éviter les mélanges."""
    if os.path.exists(dossier_tampon):
        shutil.rmtree(dossier_tampon)
    os.makedirs(dossier_tampon)

def main():
    print("--- Démarrage du convertisseur (Avec mot de passe) ---\n")

    # 1. Création des dossiers
    verifier_et_creer_dossiers()

    # 2. Recherche des fichiers
    fichiers = [f for f in os.listdir(dossier_source_rar) if f.lower().endswith('.rar')]

    if not fichiers:
        print(f"Le dossier '{dossier_source_rar}' est vide.")
        print("Mettez vos fichiers .rar dedans et relancez.")
        return

    print(f"{len(fichiers)} fichiers trouvés avec mot de passe '{mot_de_passe_rar}'.\n")

    # 3. Traitement
    for fichier in fichiers:
        chemin_rar = os.path.join(dossier_source_rar, fichier)
        nom_sans_extension = os.path.splitext(fichier)[0]
        # Le fichier zip aura le même nom que le rar
        chemin_zip_final = os.path.join(dossier_destination_zip, nom_sans_extension)

        print(f"--> Traitement de : {fichier}")
        
        # A. Nettoyage
        nettoyer_dossier_tempo()

        try:
            # B. Extraction (AVEC le mot de passe)
            # On passe le mot de passe ici pour déverrouiller le RAR
            patoolib.extract_archive(
                chemin_rar, 
                outdir=dossier_tampon, 
                verbosity=-1, 
                password=mot_de_passe_rar
            )
            
            # C. Compression (SANS mot de passe)
            # shutil crée des ZIP standard sans mot de passe par défaut
            shutil.make_archive(chemin_zip_final, 'zip', root_dir=dossier_tampon)
            
            print(f"    [OK] Succès -> {nom_sans_extension}.zip")

        except Exception as e:
            print(f"    [ERREUR] Impossible d'extraire {fichier}. Vérifiez le mot de passe ?")
            print(f"    Détail : {e}")

    # Nettoyage final
    nettoyer_dossier_tempo()
    print("\n--- Tout est terminé ! ---")

if __name__ == "__main__":
    main()