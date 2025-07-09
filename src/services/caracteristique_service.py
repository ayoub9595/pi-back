from models import db, CaracteristiqueEquipement

def get_all_caracteristiques():
    return CaracteristiqueEquipement.query.all()

def get_caracteristique_by_id(carac_id):
    return CaracteristiqueEquipement.query.get_or_404(carac_id)

def create_caracteristique(data):
    new_carac = CaracteristiqueEquipement(
        id_equipement=data['id_equipement'],
        caracteristique=data['caracteristique']
    )
    db.session.add(new_carac)
    db.session.commit()
    return new_carac

def update_caracteristique(carac_id, data):
    carac = CaracteristiqueEquipement.query.get_or_404(carac_id)
    carac.caracteristique = data.get('caracteristique', carac.caracteristique)
    db.session.commit()
    return carac

def delete_caracteristique(carac_id):
    carac = CaracteristiqueEquipement.query.get_or_404(carac_id)
    db.session.delete(carac)
    db.session.commit()
    return True
