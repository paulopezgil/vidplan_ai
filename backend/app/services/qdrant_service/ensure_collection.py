from qdrant_client.models import Distance, VectorParams

from app.core.config import settings
from app.services.qdrant_service.client import qdrant


def ensure_collection() -> None:
    """Create the employees collection if it doesn't already exist."""
    collections = [c.name for c in qdrant.get_collections().collections]
    if settings.collection_name not in collections:
        qdrant.create_collection(
            collection_name=settings.collection_name,
            vectors_config=VectorParams(
                size=settings.embed_dim, distance=Distance.COSINE
            ),
        )
