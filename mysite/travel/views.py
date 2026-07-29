from urllib.parse import unquote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import BookingForm, SignupForm
from .models import Booking

def home(request):
    return render(request, "travel/home.html")

def get_mock_weather_forecast(city, days):
    city = city.lower()
    weather_data = {
        'mumbai': ["Sunny, 32°C", "Cloudy, 30°C", "Rainy, 28°C", "Sunny, 33°C"],
        'hyderabad': ["Partly cloudy, 31°C", "Sunny, 34°C", "Thunderstorms, 29°C", "Cloudy, 30°C"],
        'bangalore': ["Cool and cloudy, 25°C", "Rainy, 23°C", "Mild sun, 26°C", "Rain showers, 24°C"],
        'mysore': ["Sunny, 28°C", "Cloudy, 27°C", "Rainy, 25°C", "Sunny intervals, 29°C"]}
    forecast = {}
    default_weather = ["Sunny, 30°C"] * 10
    selected_weather = weather_data.get(city, default_weather)

    for i in range(1, days + 1):
        forecast[i] = selected_weather[(i - 1) % len(selected_weather)]

    return forecast

def trip_planner(request):
    """Generate a travel itinerary, estimated cost, and packing checklist."""
    context = {}

    if request.method == 'POST':
        source = request.POST.get("source", "").strip().lower()
        destination = request.POST.get("destination", "").strip().lower()
        try:
            days = max(1, int(request.POST.get("days", 1)))
        except (TypeError, ValueError):
            days = 1

        route = f"{source}_{destination}"

        itineraries = {
            'hyderabad_mumbai': [
                "Travel to Mumbai & visit Gateway of India",
                "Explore Marine Drive & Juhu Beach",
                "Elephanta Caves & shopping",
                "Siddhivinayak Temple & Haji Ali",
                "Local street food tour"
            ],
            'chennai_hyderabad': [
                "Travel to Hyderabad & Charminar visit",
                "Golconda Fort & Biryani trail",
                "Ramoji Film City",
                "Salar Jung Museum & Hussain Sagar",
                "Shopping at Laad Bazaar"
            ],
            'kochi_bangalore': [
                "Arrive in Bangalore & visit MG Road",
                "Lalbagh, Cubbon Park, Vidhana Soudha",
                "Day trip to Nandi Hills",
                "Explore UB City & Brigade Road",
                "Visit ISKCON Temple"
            ],
            'bangalore_mysore': [
                "Drive to Mysore & Mysore Palace",
                "Chamundi Hills & Brindavan Gardens",
                "St. Philomena's Church",
                "Shopping at Devaraja Market",
                "Local cuisine exploration"
            ],
        }

        default_plan = [f"Day {i + 1}: Explore local attractions." for i in range(days)]

        selected_plan = itineraries.get(route, default_plan)

        full_itinerary = {
            day: selected_plan[(day - 1) % len(selected_plan)]
            for day in range(1, days + 1)
            }

        base_cost = {
            'hyderabad_mumbai': 6000,
            'chennai_hyderabad': 5000,
            'kochi_bangalore': 5500,
            'bangalore_mysore': 4000
        }
        estimated_cost = base_cost.get(route, 4500) + (days - 1) * 500

        weather = get_mock_weather_forecast(destination, days)

        checklist = [
            "Travel tickets",
            "Clothing (based on weather)",
            "ID Proof",
            "Power bank",
            "Phone charger",
            "Snacks & water",
            "Medications",
            "Sunglasses / umbrella"
        ]
        reminders = [
            "Book accommodation in advance",
            "Carry digital and physical copies of ID",
            "Keep emergency contacts handy",
            "Charge electronics the night before travel"
        ]
        context = {
            "source": source.title(),
            "destination": destination.title(),
            "days": days,
            "itinerary": full_itinerary,
            "cost": estimated_cost,
            "weather": weather,
            "checklist": checklist,
            "reminders": reminders,
            }
    return render(request, 'travel/trip_planner.html', context)

def transport_booking(request):
    cost_data = None
    if request.method == 'POST':
        source = request.POST.get('source').strip().lower()
        destination = request.POST.get('destination').strip().lower()

        routes = {
            ('hyderabad', 'mumbai'): {
                'bus': 1200,
                'train': 800,
                'flight': 3000,
                'links': {
                    'bus': 'https://www.redbus.in/bus-tickets/hyderabad-to-mumbai',
                    'train': 'https://www.irctc.co.in/nget/train-search',
                    'flight': 'https://www.makemytrip.com/flights/hyderabad-mumbai-flight-tickets.html'
                }
            },
            ('chennai', 'hyderabad'): {
                'bus': 900,
                'train': 700,
                'flight': 2500,
                'links': {
                    'bus': 'https://www.redbus.in/bus-tickets/chennai-to-hyderabad',
                    'train': 'https://www.irctc.co.in/nget/train-search',
                    'flight': 'https://www.makemytrip.com/flights/chennai-hyderabad-flight-tickets.html'
                }
            },
            ('kochi', 'bangalore'): {
                'bus': 700,
                'train': 600,
                'flight': 2300,
                'links': {
                    'bus': 'https://www.redbus.in/bus-tickets/ernakulam-to-bangalore',
                    'train': 'https://www.irctc.co.in/nget/train-search',
                    'flight': 'https://www.makemytrip.com/flights/kochi-bangalore-flight-tickets.html'
                }
            },
            ('bangalore', 'mysore'): {
                'bus': 600,
                'train': 200,
                'flight': None,  # No flight generally
                'links': {
                    'bus': 'https://www.redbus.in/bus-tickets/bangalore-to-mysore',
                    'train': 'https://www.irctc.co.in/nget/train-search',
                    'flight': None
                }
            },
        }
        key = (source, destination)
        if key in routes:
            route = routes[key]
            cost_data = {
                'bus': route['bus'],
                'train': route['train'],
                'flight': route['flight'],
                'links': route['links']
            }
        else:
            cost_data = {'error': "This route is not supported."}
    return render(request, 'travel/transport_booking.html', {'cost_data': cost_data})
HOTELS = {
    'Hyderabad': [
        {'name': 'Taj Krishna', 'price': '₹6,000/night', 'rating': 4.5, 'location': 'Banjara Hills'},
        {'name': 'Hotel Novotel', 'price': '₹5,000/night', 'rating': 4.3, 'location': 'Hitech City'},
        {'name': 'ITC Kohenur', 'price': '₹7,200/night', 'rating': 4.6, 'location': 'Hitec City'},
        {'name': 'Marriott Hotel', 'price': '₹6,500/night', 'rating': 4.4, 'location': 'Gachibowli'},
    ],
    'Mumbai': [
        {'name': 'The Oberoi', 'price': '₹10,000', 'rating': 4.7, 'location': 'Nariman Point'},
        {'name': 'Trident Hotel', 'price': '₹8,000', 'rating': 4.6, 'location': 'Bandra Kurla'},
        {'name': 'Taj Mahal Palace', 'price': '₹12,500', 'rating': 4.8, 'location': 'Gateway of India'},
        {'name': 'Novotel Mumbai', 'price': '₹7,200', 'rating': 4.5, 'location': 'Juhu Beach'},
    ],
    'Chennai': [
        {'name': 'ITC Grand Chola', 'price': '₹9,000', 'rating': 4.8, 'location': 'Guindy'},
        {'name': 'The Park Chennai', 'price': '₹5,500', 'rating': 4.2, 'location': 'Nungambakkam'},
        {'name': 'Radisson Blu', 'price': '₹6,800', 'rating': 4.4, 'location': 'GST Road'},
        {'name': 'Hyatt Regency', 'price': '₹7,200', 'rating': 4.5, 'location': 'Anna Salai'},
    ],
    'Kochi': [
        {'name': 'Taj Malabar', 'price': '₹7,000', 'rating': 4.6, 'location': 'Willingdon Island'},
        {'name': 'Grand Hyatt', 'price': '₹9,500', 'rating': 4.7, 'location': 'Bolgatty'},
        {'name': 'Le Meridien', 'price': '₹6,200', 'rating': 4.5, 'location': 'Marine Drive'},
        {'name': 'Radisson Blu', 'price': '₹5,800', 'rating': 4.4, 'location': 'Kakkanad'},
    ],
    'Bangalore': [
        {'name': 'The Leela Palace', 'price': '₹12,000', 'rating': 4.8, 'location': 'Old Airport Rd'},
        {'name': 'Taj West End', 'price': '₹11,000', 'rating': 4.7, 'location': 'Race Course Rd'},
        {'name': 'ITC Windsor', 'price': '₹8,200', 'rating': 4.5, 'location': 'Ashok Nagar'},
        {'name': 'Hilton Garden Inn', 'price': '₹6,500', 'rating': 4.4, 'location': 'MG Rd'},
    ],
    'Mysore': [
        {'name': 'Radisson Blu Plaza', 'price': '₹5,500', 'rating': 4.5, 'location': 'MG Road'},
        {'name': 'Royal Orchid Metropole', 'price': '₹4,800', 'rating': 4.3, 'location': 'JLB Road'},
        {'name': 'Fortune JP Palace', 'price': '₹5,200', 'rating': 4.4, 'location': 'Nanjaraja Bahadur Circle'},
        {'name': 'Hotel Pai Vista', 'price': '₹4,200', 'rating': 4.2, 'location': 'Chamundi Hill Rd'},
    ],
}
def hotel_booking(request):
    selected_city = request.GET.get('city', 'Hyderabad')
    hotels = HOTELS.get(selected_city, [])
    cities = list(HOTELS.keys())
    return render(request, 'travel/hotel_booking.html', {
        'hotels': hotels,
        'cities': cities,
        'selected_city': selected_city
    })

def hotel_details(request, city, hotel_name):
    hotel_name = unquote(hotel_name).strip().lower()
    city_hotels = HOTELS.get(city)
    if not city_hotels:
        raise Http404("City not found")
    for hotel in city_hotels:
        if hotel["name"].strip().lower() == hotel_name:
            if request.method == "POST":
                messages.success(request, f"✅ Booking confirmed for {hotel['name']} in {city}!")
            return render(request, "travel/hotel_details.html", {
                "hotel": hotel,
                "city": city,
            })
    raise Http404("No Hotel matches the given query")

def confirm_booking(request, city, hotel_name):
    """Store a hotel booking and send a confirmation email."""
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.city = city
            booking.hotel_name = hotel_name
            booking.status = "Confirmed"
            booking.save()

            subject = "Hotel Booking Confirmation"

            message = f"""
Hello {booking.name},

Your booking has been confirmed!

Hotel: {hotel_name}
City: {city}

Check-in: {booking.check_in}
Check-out: {booking.check_out}

Thank you for choosing Tourify.
Have a wonderful trip!
"""

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [booking.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, "Booking confirmed successfully!")
            return redirect("booking_success")

    else:
        form = BookingForm()

    return render(
        request,
        "travel/confirm_booking.html",
        {
            "form": form,
            "city": city,
            "hotel_name": hotel_name,
        },
    )

def booking_success(request):
    return render(request, 'travel/booking_success.html')
from django.shortcuts import render, redirect, get_object_or_404

def food_spots(request):
    return render(request, "travel/food_spots.html")

def budget_split(request):
    """Split trip expenses among group members."""
    if request.method == "POST":
        try:
            group_name = request.POST.get("group_name", "Trip Group")
            num_members = int(request.POST.get("num_members"))
            names = request.POST.getlist("names[]")
            raw_expenses = request.POST.getlist("expenses[]")

            if len(names) != num_members or len(raw_expenses) != num_members:
                return render(request, "travel/budget_split.html", {"error": "Mismatch in number of members and inputs!"})

            expenses = []
            for x in raw_expenses:
                x = x.strip()
                if not x.replace('.', '', 1).isdigit():
                    return render(request, "travel/budget_split.html", {"error": "Invalid expense input! Use only numbers."})
                expenses.append(float(x))

            total_spent = sum(expenses)
            share = total_spent / num_members
            balance = [round(x - share, 2) for x in expenses]
            result = list(zip(names, expenses, balance))

            owes = []
            debtors = [(i, -bal) for i, bal in enumerate(balance) if bal < 0]
            creditors = [(i, bal) for i, bal in enumerate(balance) if bal > 0]

            while debtors and creditors:
                debtor_idx, amt_owed = debtors.pop(0)
                creditor_idx, amt_due = creditors.pop(0)
                settle = min(amt_owed, amt_due)
                owes.append((names[debtor_idx], names[creditor_idx], round(settle, 2)))
                if amt_owed - settle > 0:
                    debtors.insert(0, (debtor_idx, amt_owed - settle))
                if amt_due - settle > 0:
                    creditors.insert(0, (creditor_idx, amt_due - settle))

            summary_lines = [f"{name} spent ₹{exp:.2f}, balance: ₹{bal:.2f}" for name, exp, bal in result]
            summary_lines.append(f"\nTotal: ₹{total_spent:.2f}, Equal share: ₹{share:.2f}\n")
            for debtor, creditor, amt in owes:
                summary_lines.append(f"{debtor} owes ₹{amt:.2f} to {creditor}")
            summary_text = "\n".join(summary_lines)

            context = {
                "group_name": group_name,
                "result": result,
                "total": round(total_spent, 2),
                "share": round(share, 2),
                "submitted": True,
                "owe": owes,
                "summary_text": summary_text,
            }
            return render(request, "travel/budget_split.html", context)

        except Exception as e:
            return render(request, "travel/budget_split.html", {"error": f"Invalid input! Error: {e}"})

    return render(request, "travel/budget_split.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'travel/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'travel/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def search_results(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        locations = ['delhi', 'mumbai', 'goa', 'hyderabad', 'bangalore', 'chennai']
        results = [location for location in locations if query.lower() in location.lower()]

    return render(request, 'travel/search_results.html', {'results': results, 'query': query})
def safety(request):
    return render(request, "travel/safety.html")