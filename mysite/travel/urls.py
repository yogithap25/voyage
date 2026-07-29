from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home route to fix the 404
    path('trip-planner/', views.trip_planner, name='trip_planner'),
    path('transport-booking/', views.transport_booking, name='transport_booking'),
    path('hotel-booking/', views.hotel_booking, name='hotel_booking'),
    path('food-spots/', views.food_spots, name='food_spots'),
    path('budget-split/', views.budget_split, name='budget_split'),
    path('safety/', views.safety, name='safety'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    #path('trip_planner/day_by_day_itinerary/', views.day_by_day_itinerary, name='day_by_day_itinerary'),
    #path('trip_planner/auto_generated_plans/', views.auto_generated_plans, name='auto_generated_plans'),
    #path('trip_planner/cost_estimator/', views.cost_estimator, name='cost_estimator'),
    #path('trip_planner/weather_forecast/', views.weather_forecast, name='weather_forecast'),
    #path('trip_planner/packing_checklist/', views.packing_checklist, name='packing_checklist'),
    #path('trip_planner/reminder_alerts/', views.reminder_alerts, name='reminder_alerts'),
    path('search/', views.search_results, name='search_results'),
    path('hotel-details/<str:city>/<str:hotel_name>/', views.hotel_details, name='hotel_details'),
    path('confirm-booking/<str:city>/<str:hotel_name>/', views.confirm_booking, name='confirm_booking'),
    path('booking-success/', views.booking_success, name='booking_success'),

]
