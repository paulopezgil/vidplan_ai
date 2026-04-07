from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional

from backend.services.crud.social_media import get_project_social_media, create_social_media, update_social_media
from backend.schemas.social_media import SocialMediaUpdate

async def update_tab(
    db: AsyncSession, 
    project_id: UUID,
    youtube_title: Optional[str] = None,
    youtube_description: Optional[str] = None,
    instagram_description: Optional[str] = None,
    tiktok_description: Optional[str] = None,
    twitter_post: Optional[str] = None,
    linkedin_post: Optional[str] = None
) -> str:
    """Updates or creates the social media content in the database (Social Network Tab)."""
    sm = await get_project_social_media(db, project_id)
    
    update_data = SocialMediaUpdate(
        youtube_title=youtube_title,
        youtube_description=youtube_description,
        instagram_description=instagram_description,
        tiktok_description=tiktok_description,
        twitter_post=twitter_post,
        linkedin_post=linkedin_post
    )
    
    if sm:
        await update_social_media(db, sm, update_data)
    else:
        await create_social_media(db, project_id, update_data)
        
    return "Social Network Tab updated successfully."
