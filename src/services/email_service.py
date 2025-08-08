import logging
from flask_mail import Message
from src import mail

class EmailService:
    @staticmethod
    def envoyer_email_affectation(utilisateur, equipement, caracteristiques, recipient_email=None):
        if not utilisateur or not equipement:
            logging.warning("Utilisateur ou équipement manquant, email non envoyé")
            return

        recipient = recipient_email or utilisateur.get("email")
        if not recipient:
            logging.warning("Adresse email destinataire manquante, email non envoyé")
            return

        caracteristiques_str = ""
        for c in caracteristiques:
            caracteristiques_str += f"""
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc;">{c['caracteristique']}</td>
                    <td style="padding: 8px; border: 1px solid #ccc;">{c['valeur']}</td>
                </tr>
            """

        html = f"""
        <div style="font-family: Arial, sans-serif; color: #333; padding: 20px; background-color: #f9f9f9;">
            <h2 style="color: #0053ba;">Nouvelle Affectation d'Équipement</h2>
            <p>Bonjour <strong>{utilisateur.get('nom')}</strong>,</p>
            <p>Vous avez été affecté à l'équipement suivant :</p>

            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr style="background-color: #e6f0ff;">
                    <th style="text-align: left; padding: 8px; border: 1px solid #ccc;">Détail</th>
                    <th style="text-align: left; padding: 8px; border: 1px solid #ccc;">Valeur</th>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc;">Nom</td>
                    <td style="padding: 8px; border: 1px solid #ccc;">{equipement.get('nom')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc;">Numéro de série</td>
                    <td style="padding: 8px; border: 1px solid #ccc;">{equipement.get('numero_serie')}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ccc;">Date d'acquisition</td>
                    <td style="padding: 8px; border: 1px solid #ccc;">{equipement.get('date_acquisition')}</td>
                </tr>
            </table>

            <p><strong>Caractéristiques :</strong></p>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background-color: #e6f0ff;">
                    <th style="text-align: left; padding: 8px; border: 1px solid #ccc;">Caractéristique</th>
                    <th style="text-align: left; padding: 8px; border: 1px solid #ccc;">Valeur</th>
                </tr>
                {caracteristiques_str}
            </table>
        </div>
        """

        try:
            msg = Message(
                subject="Nouvelle Affectation d'Équipement",
                recipients=[recipient],
                html=html
            )
            mail.send(msg)
            logging.info(f"Email envoyé à {recipient} avec succès")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi d'email : {str(e)}")
