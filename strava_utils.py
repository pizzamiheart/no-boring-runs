import os
from stravalib.client import Client
from flask import url_for, redirect, request
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_strava_client():
    return Client()

def strava_auth_url(client):
    return client.authorization_url(
        client_id=os.environ.get('STRAVA_CLIENT_ID'),
        redirect_uri=url_for('strava_callback', _external=True),
        scope=['read', 'activity:read_all']
    )

def strava_callback(client, code):
    token_response = client.exchange_code_for_token(
        client_id=os.environ.get('STRAVA_CLIENT_ID'),
        client_secret=os.environ.get('STRAVA_CLIENT_SECRET'),
        code=code
    )
    return token_response

def refresh_strava_token(client, refresh_token):
    token_response = client.refresh_access_token(
        client_id=os.environ.get('STRAVA_CLIENT_ID'),
        client_secret=os.environ.get('STRAVA_CLIENT_SECRET'),
        refresh_token=refresh_token
    )
    return token_response

def get_strava_activities(client, access_token, after=None):
    client.access_token = access_token
    activities = client.get_activities(after=after)
    return activities

# Add more Strava-related functions as needed
