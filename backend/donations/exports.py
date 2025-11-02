# Exports module for generating downloadable donation reports in CSV format
# Provides an example endpoint that returns mock donation data as a CSV file

import csv
from django.http import HttpResponse

def donations_csv(request):
    # generates and returns a CSV file of donation records
    # used to demostrate data export functionality for organisers or auditors
    rows = [
        {"id": 1, "amount": "25.00", "currency": "EUR", "date": "2025-10-20"},
        {"id": 2, "amount": "50.00", "currency": "EUR", "date": "2025-10-20"},
    ]

    # prepare HTTP response as downloadable CSV
    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="donations.csv"'

    # write donation data to CSV
    writer = csv.DictWriter(resp, fieldnames=["id", "amount", "currency", "date"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return resp
