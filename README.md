# zzyzx

# Juhee Song - Project Pitch

A platform to track TikTok creators over time. 

## Background
cccccccccc 

TikTok is a social media app centered around short-form video with a mission to "inspire creativity and bring joy." The platform has over 1 billion monthly active users, 3.5 billion downloads, and engagement levels exceeding competitors and continuing to grow (e.g. 26 hours screen time/month on TikTok vs. 16h on Facebook and 7.9h on Instagram). This presents an opportunity for businesses to utilize the platform to build awareness for their brand via ads, hashtag challenges, brand takeovers, and partnerships.  

My friend recently launched an apparel brand [modernlove.com](modernlove.com). She wants to partner with Tiktok creators to have them review her brand and share with their followers, but *she does not know which creators to target*. Currently, trackers are available for big creators but not up-and-coming creators (more appropriate for a new brand and a modest budget). I was inspired to help her figure out which creators are growing a strong following, serving her demographic, and creating quality content. 

## MVP

- As a business, I want to see if/how creators are growing their followings over time, so I can understand if a partnership will return on the investment (i.e. will sending free merchandise for public review result in additional orders?)
- As a business, I want to know about up-and-coming creators (i.e. 1+ viral videos) so that I can track them to see if they are continuing to build a following. 
- As a business, I want to discover creators with followings that overlap with my target demographic so that I can partner with them. 


## Tech stack

- **Database:** PostgreSQL
- **Backend:** Python 3
- **Frontend:** Web browser

### Dependencies

- Python packages:
  - SQLAlchemy ORM
  - Flask
  - Jinja
- APIs/external data sources:
  - Tiktok API 
  - TikApi API 
- Browser/client-side dependencies:
  - React 
  - Bootstrap

## Roadmap

### Sprint 1

- User registration and authentication
- List read/write service: a RESTful API to create, read, update lists of creators
- List item read/write service: a RESTful API to read and update metrics for creators that appear in creator lists (i.e. # of followers, # following, # of videos, # of likes)
- Creator profile page to display all metrics for a creator, at different points in time 

### Sprint 2
- Dashboard overview of full creator list 
- Tiktok integration: return top video from Tiktok API for each creator 
- React frontend for editing lists of creators
  - drag and drop to edit order of creators
  - search and autocomplete frontend for creators 
  - generic content component: paste a hashtag and retrieve video from API