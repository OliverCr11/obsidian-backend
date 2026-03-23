import resend
from django.conf import settings
from .models import Order

def send_order_confirmation(order_id):
    """
    Constructs and dispatches a 'Dark Luxury' themed HTML confirmation email natively using the Resend API.
    Fails safely absorbing arbitrary SMTP timeouts shielding physical Order Database commits.
    """
    resend.api_key = getattr(settings, 'RESEND_API_KEY', '')
    
    try:
        order = Order.objects.get(order_id=order_id)
        items = order.items.all()
        
        # Build strict tabular structural grids explicitly formatted for arbitrary client parsing
        items_html = ""
        for item in items:
            items_html += f"""
            <tr style="border-bottom: 1px solid #27272a;">
                <td style="padding: 16px 0; color: #e4e4e7; font-size: 14px; font-weight: 500;">{item.quantity}x {item.glove.name}</td>
                <td style="padding: 16px 0; text-align: right; color: #a1a1aa; font-family: monospace; font-size: 14px;">${item.price}</td>
            </tr>
            """
        
        # Inline global aesthetics adhering to strict 'Dark Luxury' parameters requested
        html_content = f"""
        <div style="background-color: #000000; color: #fafafa; font-family: 'Helvetica Neue', Arial, sans-serif; padding: 40px 20px; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #121214; border: 1px solid #3f3f46; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);">
                <div style="padding: 40px 30px; border-bottom: 1px solid #27272a; text-align: center; background: linear-gradient(180deg, #18181b 0%, #121214 100%);">
                    <h1 style="margin: 0; font-size: 28px; font-weight: 900; letter-spacing: 6px; text-transform: uppercase; color: #ffffff;">
                        O B S I D I A N
                    </h1>
                    <p style="color: #a78bfa; font-size: 13px; margin-top: 12px; font-weight: 700; letter-spacing: 2px;">SECURE ORDER CONFIRMATION</p>
                </div>
                
                <div style="padding: 40px 30px;">
                    <p style="color: #e4e4e7; font-size: 16px; margin-bottom: 24px;">Greetings {order.full_name},</p>
                    <p style="color: #a1a1aa; font-size: 15px; margin-bottom: 32px;">Your tactical gear requisition has been authenticated and is being provisioned for immediate deployment. Below are your mission parameters.</p>
                    
                    <div style="margin: 0 0 32px 0; background-color: #09090b; border: 1px solid #27272a; border-radius: 8px; padding: 24px; text-align: center;">
                        <p style="margin: 0 0 8px 0; color: #71717a; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 700;">Clearance Code (Order ID)</p>
                        <p style="margin: 0; font-family: monospace; color: #ffffff; font-size: 20px; font-weight: bold; letter-spacing: 1px;">{str(order.order_id).split('-')[0].upper()}</p>
                    </div>
                    
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 32px;">
                        {items_html}
                    </table>
                    
                    <div style="display: table; width: 100%; margin-bottom: 48px; border-top: 1px solid #27272a; padding-top: 24px;">
                        <div style="display: table-cell; text-align: right; font-size: 20px; font-weight: bold;">
                            <span style="color: #71717a; margin-right: 16px; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Total Authorized</span>
                            <span style="color: #d8b4fe; font-family: monospace;">${order.total_paid} <span style="font-size: 12px; color: #71717a;">USD</span></span>
                        </div>
                    </div>
                    
                    <a href="http://localhost:5173/dashboard" style="display: block; width: 100%; text-align: center; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: #ffffff; padding: 18px 0; text-decoration: none; border-radius: 8px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; font-size: 14px; box-shadow: 0 4px 14px rgba(139, 92, 246, 0.4);">Access Dashboard</a>
                </div>
                
                <div style="padding: 24px; background-color: #09090b; text-align: center; border-top: 1px solid #27272a;">
                    <p style="color: #52525b; font-size: 11px; margin: 0; letter-spacing: 1px; text-transform: uppercase;">&copy; 2026 Obsidian Tactical Division.</p>
                </div>
            </div>
        </div>
        """

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Obsidian <onboarding@resend.dev>')
        
        params = {
            "from": from_email,
            "to": [order.email],
            "subject": f"Obsidian Protocol Confirmed: // {str(order.order_id).split('-')[0].upper()}",
            "html": html_content,
        }

        email_response = resend.Emails.send(params)
        print(f"Mission briefing dispatched asynchronously to {order.email}. Tracker ID: {email_response.get('id')}")
        return True

    except Exception as e:
        print(f"CRITICAL SMTP ABORT for Order {order_id}: {str(e)}")
        # Returns false ensuring upstream transactions DO NOT rollback
        return False
