import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_local_events(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) LocalEventsScraper/1.0'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        event_containers = soup.select('.event-listing .event') 
        
        events = []
        
        for event in event_containers:
            title = event.select_one('.event-title').get_text(strip=True)
            date_str = event.select_one('.event-date').get_text(strip=True)
            location = event.select_one('.event-location').get_text(strip=True)
            description = event.select_one('.event-description').get_text(strip=True, separator=' ')
            
            try:
                event_date = datetime.strptime(date_str, '%B %d, %Y %I:%M %p')
                date_formatted = event_date.strftime('%Y-%m-%d %H:%M')
            except ValueError:
                date_formatted = date_str
            
            events.append({
                'title': title,
                'date': date_formatted,
                'location': location,
                'description': description
            })
        
        return events
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        return []
    except Exception as e:
        print(f"Error parsing events: {e}")
        return []

def display_events(events):
    if not events:
        print("No events found or there was an error.")
        return
    
    print("\nUPCOMING LOCAL EVENTS")
    print("=" * 50)
    for i, event in enumerate(events, 1):
        print(f"\n{i}. {event['title']}")
        print(f"   Date: {event['date']}")
        print(f"   Location: {event['location']}")
        print(f"   Description: {event['description'][:100]}...")  # Show first 100 chars

if __name__ == "__main__":
    test_url = "https://example.com/community-events"
    
    mock_html = """
    <div class="event-listing">
        <div class="event">
            <h3 class="event-title">Farmers Market</h3>
            <div class="event-date">June 15, 2024 9:00 AM</div>
            <div class="event-location">Main Street Square</div>
            <p class="event-description">Weekly farmers market featuring local produce, crafts, and live music.</p>
        </div>
        <div class="event">
            <h3 class="event-title">Summer Concert Series</h3>
            <div class="event-date">June 22, 2024 7:00 PM</div>
            <div class="event-location">Riverside Park Amphitheater</div>
            <p class="event-description">Free outdoor concert featuring local bands. Bring blankets and chairs.</p>
        </div>
        <div class="event">
            <h3 class="event-title">Library Book Sale</h3>
            <div class="event-date">June 28-30, 2024 10:00 AM</div>
            <div class="event-location">Public Library</div>
            <p class="event-description">Annual fundraiser with thousands of books at discounted prices.</p>
        </div>
    </div>
    """

    soup = BeautifulSoup(mock_html, 'html.parser')
    event_containers = soup.select('.event-listing .event')
    
    events = []
    for event in event_containers:
        title = event.select_one('.event-title').get_text(strip=True)
        date_str = event.select_one('.event-date').get_text(strip=True)
        location = event.select_one('.event-location').get_text(strip=True)
        description = event.select_one('.event-description').get_text(strip=True, separator=' ')
        
        events.append({
            'title': title,
            'date': date_str,
            'location': location,
            'description': description
        })
    
    display_events(events)
