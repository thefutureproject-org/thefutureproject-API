import requests
import re
import json


def get_pnr_status(pnr: str):
    url = f"https://www.confirmtkt.com/pnr-status?pnr={pnr}"
    response = requests.get(url)

    pattern = re.compile(r'data\s*=\s*(\{.*?\});', re.DOTALL)
    match = pattern.search(response.text)

    if match:
        json_str = match.group(1)
        data = json.loads(json_str)

        if data['Error']:
            return data['Error']

        result = {
            "Pnr": data.get("Pnr"),
            "TrainNo": data.get("TrainNo"),
            "TrainName": data.get("TrainName"),
            "InformationMessage": data.get("InformationMessage"),
            "Doj": data.get("Doj"),
            "BookingDate": data.get("BookingDate"),
            "Quota": data.get("Quota"),
            "DestinationDoj": data.get("DestinationDoj"),
            "SourceDoj": data.get("SourceDoj"),
            "From": data.get("From"),
            "To": data.get("To"),
            "ReservationUpto": data.get("ReservationUpto"),
            "BoardingPoint": data.get("BoardingPoint"),
            "Class": data.get("Class"),
            "ChartPrepared": data.get("ChartPrepared"),
            "BoardingStationName": data.get("BoardingStationName"),
            "TrainStatus": data.get("TrainStatus"),
            "TrainCancelledFlag": data.get("TrainCancelledFlag"),
            "ReservationUptoName": data.get("ReservationUptoName"),
            "PassengerCount": data.get("PassengerCount"),
            "DepartureTime": data.get("DepartureTime"),
            "ArrivalTime": data.get("ArrivalTime"),
            "ExpectedPlatformNo": data.get("ExpectedPlatformNo"),
            "BookingFare": data.get("BookingFare"),
            "TicketFare": data.get("TicketFare"),
            "CoachPosition": data.get("CoachPosition"),
            "Rating": data.get("Rating"),
            "FoodRating": data.get("FoodRating"),
            "PunctualityRating": data.get("PunctualityRating"),
            "CleanlinessRating": data.get("CleanlinessRating"),
            "SourceName": data.get("SourceName"),
            "DestinationName": data.get("DestinationName"),
            "Duration": data.get("Duration"),
            "PassengerStatus": [
                {
                    "Number": passenger.get("Number"),
                    "Coach": passenger.get("Coach"),
                    "Berth": passenger.get("Berth"),
                    "BookingStatus": passenger.get("BookingStatus"),
                    "CurrentStatus": passenger.get("CurrentStatus"),
                    "CurrentBerthNo": passenger.get("CurrentBerthNo"),
                    "CurrentCoachId": passenger.get("CurrentCoachId"),
                    "CurrentBerthCode": passenger.get("CurrentBerthCode"),
                    "CurrentStatusNew": passenger.get("CurrentStatusNew")
                } for passenger in data.get("PassengerStatus", [])
            ]
        }

        return result
    else:
        return "No data found."
