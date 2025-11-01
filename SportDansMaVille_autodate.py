from playwright.sync_api import sync_playwright  # A priori, pas besoin
from playwright.async_api import async_playwright
import asyncio
import nest_asyncio  # A priori, pas besoin,sauf pour notebook
import time  # A priori, pas besoin
import base64
from datetime import datetime, timedelta
# Mettre venv : source .venv/bin/activate
# Arreter venv : deactivate


def date():
    # Mapping anglais vers anglais français
    mois_fr = {
        "January": "janvier",
        "February": "février",
        "March": "mars",
        "April": "avril",
        "May": "mai",
        "June": "juin",
        "July": "juillet",
        "August": "août",
        "September": "septembre",
        "October": "octobre",
        "November": "novembre",
        "December": "décembre"
    }

    # Date de départ
    date_depart = datetime.now()

    # Ajouter 45 jours
    date_updatee = date_depart + timedelta(days=45)

    # Récupérer le mois mais en anglais et vu qu'on cherche un mois en fr dans le DOM, il faut transformer le mot
    mois_anglais = date_updatee.strftime('%B')
    jour = date_updatee.strftime('%d')

    # Convertir en français et construire la chaîne
    date_str = f"{mois_fr[mois_anglais]} {jour},"
    return date_str


nest_asyncio.apply()  # Pas obligé avec .py. Que pour note book


async def main():
    async with async_playwright() as p:
        # Lancer le navigateur Chromium en mode asynchrone car sur Jupyter il faut être asynchrone
        # headless=False pour voir le navigateur, forcer fr pour pas que Chrome traduise automatiquement
        browser = await p.chromium.launch(headless=True, args=["--lang=fr-FR"])
        # Ici : créer un contexte avec locale FR
        context = await browser.new_context(locale="fr-FR", 
                                            viewport={"width": 1280, "height": 800}, 
                                            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
        # Créer une nouvelle page dans ce contexte
        page = await context.new_page()  # Ouvre une nouvelle page avec context

        await page.goto("https://sport-dans-la-ville.doinsport.club/select-booking?guid=%221ce2c55d-6010-4f45-9b6f-1aafc04382fa%22&from=sport&activitySelectedId=%22cc4da804-1ef4-4f57-9fa4-4c203cdc06c8%22&categoryId=%22910503af-d67a-4f2b-a0df-838e0b4fb8ac%22")  # Va sur l'URL demandé
        # Click sur le logo calendrier pour ouvrir le calendrier
        await page.locator("app-svg-container").get_by_role("img").click()
        # Avancer jusqu'à trouver "mai 06"
        for _ in range(6):  # On limite à 6 essais max
            # Vérifie si la date est présente
            date_element = page.get_by_label(date())
            if await date_element.is_visible():
                await date_element.click()
                print(date())
                break
            else:
                await page.locator("ion-calendar").get_by_role("button", name="chevron forward outline").click()

        # Naviguer jusqu'à la tranche horaire 16:00 - 20:00
        for direction in ['right', 'left']:
            for _ in range(5):
                await page.wait_for_timeout(1000)
                await page.locator(f"button.btn-arrow-{direction}").click()
                creneau = await page.locator("div.value").text_content()
                if "16:00 - 20:00" in creneau.lower():
                    print(f"{creneau}, OK !")
                    await page.wait_for_timeout(1000)
                    await page.get_by_text("19:00").first.click()
                    print("Heure OK !")
                    # Prend les 7 terrains par ordre de préférence pour faire une boucle afin de trouver le 1er crénaux "Début19:0060 minA partir de100.00 €"
                    numero_terrain = [4, 5, 7, 6, 3, 2, 1]
                    for i in numero_terrain:  # Pour chaque numéro de terrain, trouver "Début19:0060 min"
                        await page.wait_for_timeout(2000)
                         # Capturer  le text...
                        text_playwriht = await page.get_by_text(f"Foot {i} Football 5vs5 - Exté").text_content()
                        await page.wait_for_timeout(2000)
                        # ... Si il y a le texte "Début19:0060 min", alors cliquer sur les pages suivantes
                        if "Début19:00" in text_playwriht and "60" in text_playwriht:
                            await page.wait_for_timeout(2000)
                            await page.locator("app-card-playground").filter(has_text=f"Foot {i} Football 5vs5 - Exté").locator("ion-label").filter(has_text="60 min").click()
                            print(f"Terrain {i} trouvé")
                            await page.wait_for_timeout(2000)
                            await page.fill('input[placeholder="john.doe@example.com"]', 'jolie.mountain@gmail.com')
                            await page.wait_for_timeout(2000)
                            await page.get_by_text("Valider mon email").click()
                             # Screenshot complet
                            #await page.screenshot(path="/app/crash_screenshot.png", full_page=True)
                            await page.wait_for_timeout(2000)
                            await page.fill('input[placeholder="******"]', 'Toulouse31')
                            await page.wait_for_timeout(2000)
                            await page.get_by_text("Valider").click()
                            await page.wait_for_timeout(2000)
                            await page.get_by_text("Suivant").click()
                            #await page.pause()
                            await page.wait_for_timeout(2000)
                            await page.get_by_text("Payer et réserverPayer et ré").click()
                            # Screenshot qui se print en base64. A copier/coller sur un site pour avoir la page
                            await page.screenshot(path="/tmp/final_screenshot.png", full_page=True)
                            with open("/tmp/final_screenshot.png", "rb") as f:
                                print("SCREENSHOT2_BASE64:", base64.b64encode(f.read()).decode())
                            print("Processus de réservation terminé.")
                            await page.wait_for_timeout(2000)
                            #await page.get_by_text("Ajouter une carte").click()
                            #await page.wait_for_timeout(2000)
                            #await page.locator("#ion-overlay-6 ion-radio").first.click()
                            #await page.wait_for_timeout(2000)
                            #await page.get_by_text("Sélectionner").click()
                            #await page.wait_for_timeout(2000)
                            #await page.get_by_text("Payer et réserver").nth(1).click()
                            await page.wait_for_timeout(1000)
                            await browser.close()  # ferme le navigateur proprement
                            return  # quitte la fonction main()
                    
                    # 👉 Si on arrive ici, c’est que le return n’a jamais été exécuté
                    print("❌ Aucun terrain dispo à 19h !")
                    await browser.close()
                    return

asyncio.run(main())
