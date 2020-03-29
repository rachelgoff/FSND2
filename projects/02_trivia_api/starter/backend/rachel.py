#!/usr/bin/env python3

from app import db, Artist, Venue, Show
db.create_all()
art=Artist(name="Adel", city="San Francisco", state="CA", genres="Classical", image_link="https://i.ytimg.com/vi/YQHsXMglC9A/maxresdefault.jpg")
ven=Venue(name="Starbucks", city="San Francisco", state="CA", genres="Classical", image_link="https://i.ytimg.com/vi/YQHsXMglC9A/maxresdefault.jpg")
# art.venues=[ven]
# ven.artists=[art]
db.session.add(art, ven)
db.session.commit()
# art.venues
# ven.artists