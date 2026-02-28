from sqlalchemy.orm import Session
from app.models.provider import Provider


def list_providers(db: Session):
    return db.query(Provider).all()


def get_or_create_provider(db: Session, name: str, cif: str) -> Provider:
    provider = db.query(Provider).filter(Provider.cif == cif).first()

    if provider:
        return provider

    provider = Provider(name=name, cif=cif)
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider