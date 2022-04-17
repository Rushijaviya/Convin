import datetime
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import os
import google_apis_oauth

# Insecure Transport Error
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import google_apis_oauth
from googleapiclient.discovery import build

from rest_framework.views import APIView
from rest_framework.response import Response


class ConvinCalender(APIView):
    """ In this Convin Assignment the given task is to fetch the list of event from user's Google calender using Google API.  """

    def get(self,request,format=None):
        try:
            # Get user credentials
            credentials = google_apis_oauth.get_crendentials_from_callback(
                request,
                JSON_FILEPATH,
                SCOPES,
                REDIRECT_URI
            )
            print(1)
            print(credentials)
            # Stringify credentials for storing them in the DB
            stringified_token = google_apis_oauth.stringify_credentials(credentials)
        except Exception as e:
            # This exception is raised when there is an inavlid
            # request to this callback uri.
            print("come")
            print(e)
            print("come2")

        # Load the credentials object using the stringified token.
        creds, refreshed = google_apis_oauth.load_credentials(stringified_token)

        # Using credentials to access Events
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary',timeZone="Asia/Kolkata").execute()
        events = events_result.get('items', [])


        if not events:
            print('No upcoming events found.')
        # for event in events:
        #     del event['etag']
        #     del event['id']
        #     # del event['htmlLink']
        #     del event['iCalUID']
        #     del event['sequence']
        #     del event['eventType']            

        # return HttpResponse(context)
        return Response(events)
        # return render(request,'data.html',context)


def home(request):
    # return HttpResponse("<h1>Hello</h1>")
    return render(request,'home.html')


# The url where the google oauth should redirect
# after a successful login.
# REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect/'
REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect/'

# Authorization scopes required
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Path of the "client_id.json" file
JSON_FILEPATH = os.path.join(os.getcwd(), 'cs.json')

def GoogleCalendarInitView(request):
    oauth_url = google_apis_oauth.get_authorization_url(
        JSON_FILEPATH, SCOPES, REDIRECT_URI)
    return HttpResponseRedirect(oauth_url)