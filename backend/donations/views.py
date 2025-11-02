# Views for generating downloadable donation receipts in PDF format
# Combines stored donation data, QR verification, and PDF rendering

from django.http import HttpResponse, Http404
from django.utils.timezone import now
from core.pdf import build_receipt_pdf
from core.qr import make_qr

# mock function to simulate fetching a donation record
def get_donation(donation_id: int):
    # retrieves donation details for receipt generation
    # In production this would query the database
    return {
        "donation_id": donation_id,
        "donor_name": "Alex Donor",
        "amount": "25.00",
        "currency": "EUR",
        "date": now().strftime("%Y-%m-%d %H:%M"),
        "allocations": [{"beneficiary_name": "Irish Cancer Society", "percent": 60},
                        {"beneficiary_name": "Pieta House", "percent": 40}],
        "note": "Online donation via Stripe",
    }

# generate and return a PDF receipt
def receipt_pdf(request, donation_id: int):
    # builds a PDF receipt for the given donation
    # includes beneficiary allocations and a QR code for verification
    data = get_donation(donation_id)
    if not data:
        raise Http404("Donation not found")

    # create a QR code linking to the donation verification page
    qr = make_qr(f"https://charityconnect.local/verify/{data['donation_id']}")

    # generate the PDF receipt using the prepared data
    pdf_bytes = build_receipt_pdf(data, qr_image=qr)

    # return the PDF inline in the browser
    resp = HttpResponse(pdf_bytes, content_type="application/pdf")
    resp["Content-Disposition"] = f'inline; filename="receipt-{donation_id}.pdf"'
    return resp
