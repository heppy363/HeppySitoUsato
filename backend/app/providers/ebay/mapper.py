from app.providers.ebay.schemas import EbaySearchItem
from app.providers.models import SearchResult


class EbayResultMapper:
    platform = "ebay"

    def map_item(self, item: EbaySearchItem) -> SearchResult:
        location_parts = [
            part
            for part in (
                item.item_location.city if item.item_location else None,
                item.item_location.country if item.item_location else None,
            )
            if part
        ]
        location = ", ".join(location_parts) or None

        return SearchResult(
            id=f"{self.platform}:{item.item_id}",
            external_id=item.item_id,
            title=item.title,
            description=item.short_description,
            price=float(item.price.value),
            currency=item.price.currency,
            platform=self.platform,
            location=location,
            url=item.item_web_url,
            image_url=item.image.image_url if item.image is not None else None,
            seller_name=item.seller.username if item.seller is not None else None,
            seller_rating=item.seller.feedback_percentage if item.seller is not None else None,
            condition=item.condition,
            published_at=item.item_creation_date,
        )
