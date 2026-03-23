from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user, profile):
    """
    Sends a secure HTML verification email utilizing the configured SMTP backend (Resend).
    """
    subject = 'Verify your Obsidian Account'
    verification_link = f"http://localhost:5173/verify-email/{profile.verification_token}"
    
    message = f"Welcome to Obsidian.\n\nPlease verify your account by clicking the link below:\n{verification_link}\n\nStay dark."
    html_message = f"""
    <div style="font-family: monospace; background: #000; color: #fff; padding: 40px; text-align: center;">
        <h1 style="color: #8B5CF6; letter-spacing: 0.2em;">OBSIDIAN</h1>
        <p style="color: #a1a1aa;">Welcome to the Drop.</p>
        <p>Verify your access protocol to continue.</p>
        <a href="{verification_link}" style="display: inline-block; padding: 15px 30px; background: #fff; color: #000; text-decoration: none; font-weight: bold; margin-top: 20px;">VERIFY ACCOUNT</a>
    </div>
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
            html_message=html_message
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
