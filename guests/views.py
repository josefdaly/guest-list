from django.shortcuts import render

import qrcode

# Create your views here.
def guest_rsvp_qr_code(request, guest_id):
    # This is a placeholder view. In a real application, you would generate a QR code based on the guest's information.
    return render(request, 'guests/qr_code.html', {'guest_id': guest_id})