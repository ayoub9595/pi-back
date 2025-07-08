from src import db

class Equipment(db.Model):
    __tablename__ = 'equipments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    serial_number = db.Column(db.String(50), unique=True)
    purchase_date = db.Column(db.Date)
    maintenance_due = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'serial_number': self.serial_number,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'maintenance_due': self.maintenance_due.isoformat() if self.maintenance_due else None,
            'is_active': self.is_active
        }