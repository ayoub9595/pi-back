import logging
from flask_mail import Message
from flask import render_template
from src import mail
from datetime import datetime


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
            if action == "creation":
                subject = "Nouvelle Affectation d'Équipement"
            elif action == "suppression":
                subject = "Suppression d'une Affectation"
            elif action == "modification":
                subject = "Modification d'une Affectation"
            else:
                subject = "Notification d'Affectation"

            msg = Message(
                subject=subject,
                recipients=[recipient],
                html=html_content
            )
            mail.send(msg)
            logging.info(f"Email '{action}' envoyé à {recipient}")

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email ({action}) : {str(e)}")

    @staticmethod
    def envoyer_email_reclamation_pour_admins(reclamation, recipient_email, action="creation"):
        try:
            if not recipient_email:
                logging.warning("Adresse email destinataire manquante, email non envoyé")
                return

            utilisateur = reclamation.get("utilisateur", {})
            equipement = reclamation.get("equipement", {})
            caracteristiques = equipement.get("caracteristiques", [])

            current_date = datetime.now().strftime("%d/%m/%Y à %H:%M")

            html_content = render_template(
                "email_reclamation_admins.html",
                reclamation=reclamation,
                utilisateur=utilisateur,
                equipement=equipement,
                caracteristiques=caracteristiques,
                action=action,
                current_date=current_date
            )

            if action == "creation":
                subject = "Nouvelle Réclamation à Traiter"
            elif action == "update":
                subject = "Mise à Jour d'une Réclamation"
            elif action == "resolved":
                subject = "Réclamation Résolue"
            else:
                subject = "Notification de Réclamation"

            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                html=html_content
            )
            mail.send(msg)
            logging.info(f"Email de réclamation '{action}' envoyé à {recipient_email}")

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email de réclamation ({action}) : {str(e)}")

    @staticmethod
    def envoyer_email_reclamation_pour_utilisateur(reclamation, recipient_email, action="creation"):
        try:
            if not recipient_email:
                logging.warning("Adresse email destinataire manquante, email non envoyé")
                return

            utilisateur = reclamation.get("utilisateur", {})
            equipement = reclamation.get("equipement", {})
            caracteristiques = equipement.get("caracteristiques", [])

            current_date = datetime.now().strftime("%d/%m/%Y à %H:%M")

            html_content = render_template(
                "email_reclamation_users.html",
                reclamation=reclamation,
                utilisateur=utilisateur,
                equipement=equipement,
                caracteristiques=caracteristiques,
                action=action,
                current_date=current_date
            )

            if action == "creation":
                subject = "✅ Réclamation Enregistrée - Confirmation"
            elif action == "update":
                subject = "📝 Mise à Jour de votre Réclamation"
            elif action == "resolved":
                subject = "✅ Votre Réclamation a été Résolue"
            elif action == "accepted":
                subject = "✅ Votre Réclamation a été Acceptée"
            elif action == "rejected":
                subject = "❌ Mise à Jour de votre Réclamation"
            else:
                subject = "📬 Notification concernant votre Réclamation"

            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                html=html_content
            )
            mail.send(msg)
            logging.info(f"Email de confirmation de réclamation '{action}' envoyé à {recipient_email}")

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email de confirmation de réclamation ({action}) : {str(e)}")

    @staticmethod
    def envoyer_email_modification_utilisateur(utilisateur, recipient_email=None):
        try:
            recipient = recipient_email or utilisateur.get("email")
            if not recipient:
                logging.warning("Adresse email destinataire manquante, email non envoyé")
                return

            html_content = render_template(
                "email_modification_utilisateur.html",
                utilisateur=utilisateur
            )

            subject = "Modification de vos Informations"

            msg = Message(
                subject=subject,
                recipients=[recipient],
                html=html_content
            )
            mail.send(msg)
            logging.info(f"Email de modification d'utilisateur envoyé à {recipient}")

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email de modification d'utilisateur : {str(e)}")

    @staticmethod
    def envoyer_email_confirmation_inscription_user(data):
        try:
            recipient = data.get('email')
            if not recipient:
                logging.warning("Adresse email destinataire manquante pour confirmation inscription")
                return

            html_content = render_template(
                "email_inscription_confirmation_user.html",
                nom=data.get('nom')
            )

            msg = Message(
                subject="Confirmation de votre inscription",
                recipients=[recipient],
                html=html_content
            )
            mail.send(msg)
            logging.info(f"Email de confirmation d'inscription envoyé à {recipient}")

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email de confirmation d'inscription : {str(e)}")

    @staticmethod
    def envoyer_email_nouvelle_inscription_admins(data, admin_emails):
        if not admin_emails:
            logging.warning("Aucun email d'admin fourni pour la notification d'inscription")
            return

        try:
            html_content = render_template(
                "email_inscription_notification_admin.html",
                nom=data.get('nom'),
                email=data.get('email'),
                cin=data.get('cin'),
                telephone=data.get('telephone'),
                role=data.get('role', 'Utilisateur')
            )

            msg = Message(
                subject="Nouvelle demande d'inscription",
                recipients=admin_emails,
                html=html_content
            )
            mail.send(msg)
            logging.info(f"Email de notification d'inscription envoyé aux admins : {admin_emails}")

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email de notification aux admins : {str(e)}")