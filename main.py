import time
from datetime import datetime, timedelta
from collections import defaultdict

class User:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

class Event:
    def __init__(self, event_type, timestamp, user, data):
        self.event_type = event_type
        self.timestamp = timestamp
        self.user = user
        self.data = data

class NotificationService:
    def __init__(self):
        # Stores events waiting to be batched, keyed by user_id
        self.pending_batched_events = defaultdict(list)
        print("Notification Service initialized.")

    def _send_email(self, user, subject, body):
        """Simulates sending an email."""
        print(f"--- Sending Email to {user.email} ---")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}\n")
        print(f"-------------------------------------\n")

    def trigger_instant_notification(self, user: User, event_data: str):
        """
        Problematic approach: Sends an email immediately for each event.
        This can lead to an 'inbox explosion' if many events occur rapidly.
        """
        subject = f"New Event: {event_data}"
        body = f"Hi {user.user_id},\n\nA new event just occurred: {event_data} at {datetime.now().strftime('%H:%M:%S')}.\n\nEnjoy your treasure hunt!"
        self._send_email(user, subject, body)
        # INLINE COMMENT: This simulates sending an individual email for every single event,
        # leading to an overwhelming number of notifications if events fire rapidly.

    def add_for_batch_notification(self, user: User, event_data: str):
        """
        Adds an event to a queue to be processed later in a batch.
        """
        event = Event("treasure_found", datetime.now(), user, event_data)
        self.pending_batched_events[user.user_id].append(event)
        print(f"Event '{event_data}' added to batch for {user.user_id}.")
        # INLINE COMMENT: Events are queued here instead of triggering immediate emails.

    def process_batched_notifications(self):
        """
        Solution approach: Processes all queued events and sends a single digest email per user.
        This prevents an 'inbox explosion' by aggregating multiple events.
        """
        if not self.pending_batched_events:
            print("No batched events to process.")
            return

        print("\n--- Processing Batched Notifications ---")
        for user_id, events in self.pending_batched_events.items():
            if not events:
                continue

            # Assuming all events in a batch are for the same user
            user = events[0].user
            subject = f"Your Treasure Hunt Summary ({len(events)} New Events!)"
            
            body_lines = [f"Hi {user.user_id},\n\nHere's a summary of your recent activities:"]
            for i, event in enumerate(events):
                body_lines.append(f"- {i+1}. You {event.data} at {event.timestamp.strftime('%H:%M:%S')}.")
            body_lines.append("\nKeep hunting!")
            
            self._send_email(user, subject, "\n".join(body_lines))
            # INLINE COMMENT: A single, aggregated email is sent for all events collected for a user,
            # significantly reducing notification volume compared to individual emails.
        
        self.pending_batched_events.clear() # Clear processed events
        print("--- Batched Notifications Processed ---\n")

# --- Main Simulation ---
if __name__ == "__main__":
    user_john = User("john_doe", "john.doe@example.com")
    notification_service = NotificationService()

    print("--- Scenario 1: Inbox Explosion (Problematic Approach) ---")
    print("Simulating user finding 3 treasures rapidly, each triggering an instant email.")
    notification_service.trigger_instant_notification(user_john, "found a golden coin")
    time.sleep(0.5) # Simulate a small delay between actions
    notification_service.trigger_instant_notification(user_john, "discovered a hidden map")
    time.sleep(0.5)
    notification_service.trigger_instant_notification(user_john, "unlocked a secret chest")
    print("End of Scenario 1.\n" + "="*50 + "\n")

    # Reset service for the next scenario (in a real app, this would be a new instance or state reset)
    notification_service = NotificationService() 

    print("--- Scenario 2: Batched Notifications (Solution Approach) ---")
    print("Simulating user finding 3 treasures rapidly, events are queued for batching.")
    notification_service.add_for_batch_notification(user_john, "found a silver key")
    time.sleep(0.5)
    notification_service.add_for_batch_notification(user_john, "deciphered an ancient riddle")
    time.sleep(0.5)
    notification_service.add_for_batch_notification(user_john, "claimed a rare artifact")
    
    print("\n(Simulating a delay, e.g., 2 seconds later, when the batch processor runs...)")
    time.sleep(2) # Simulate waiting for the batching interval to pass

    notification_service.process_batched_notifications()
    print("End of Scenario 2.\n" + "="*50 + "\n")
