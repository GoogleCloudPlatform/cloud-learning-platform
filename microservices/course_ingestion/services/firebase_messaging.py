"""Mudule to send firebase messages"""
import firebase_admin
from firebase_admin import messaging
from common.utils.logging_handler import Logger

def send_to_token(registration_token,title,body):
  # [START send_to_token]
  # This registration token comes from the client FCM SDKs.
  firebase_admin.initialize_app()
  # See documentation on defining a message payload.
  message = messaging.Message(
      notification=messaging.Notification(title=title,body=body),
      token=registration_token
  )

  # Send a message to the device corresponding to the provided
  # registration token.
  response = messaging.send(message)
  # Response is a message ID string.
  Logger.info("Successfully sent message:")
  Logger.info(response)
