import logging
from flask_mail import Message
from flask import render_template
from src import mail

class EmailService:
    @staticmethod
    def envoyer_email_affectation(affectation, recipient_email=None, action="creation"):
        try:
            utilisateur = affectation.get("utilisateur", {})
            equipement = affectation.get("equipement", {})
            caracteristiques = equipement.get("caracteristiques", [])

            recipient = recipient_email or utilisateur.get("email")
            if not recipient:
                logging.warning("Adresse email destinataire manquante, email non envoyé")
                return

            html_content = render_template(
                "email_affectation.html",
                utilisateur=utilisateur,
                equipement=equipement,
                caracteristiques=caracteristiques,
                date_debut=affectation.get("date_debut"),
                date_fin=affectation.get("date_fin"),
                determine=affectation.get("determine"),
                action=action
            )

            subject = "Nouvelle Affectation d'Équipement" if action == "creation" else "Suppression d'une Affectation"

            msg = Message(
                subject=subject,
                recipients=[recipient],
                html=html_content
            )
            mail.send(msg)
            logging.info(f"Email '{action}' envoyé à {recipient}")

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email ({action}) : {str(e)}")
