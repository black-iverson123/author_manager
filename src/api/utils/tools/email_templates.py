subject = "Please confirm your email"

confirmation_email_html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Confirm your email</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f6f8;font-family:Helvetica,Arial,sans-serif;">
  <!-- Preheader (hidden but shown in inbox preview) -->
  <div style="display:none;max-height:0px;overflow:hidden;mso-hide:all;">
    Confirm your email address to activate your account.
  </div>

  <table width="100%" cellpadding="0" cellspacing="0" role="presentation">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table width="600" cellpadding="0" cellspacing="0" role="presentation" style="background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 6px rgba(0,0,0,0.06);">
          <!-- Header -->
          <tr>
            <td style="padding:24px;text-align:center;background: #0f172a;color:#ffffff;">
              <h1 style="margin:0;font-size:20px;font-weight:600;">Splash Library</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:28px 32px;color:#0f172a;">
              <p style="margin:0 0 16px 0;font-size:16px;line-height:1.5;">
                Hi {{name}},
              </p>

              <p style="margin:0 0 20px 0;font-size:15px;line-height:1.5;color:#555;">
                Thanks for creating an account. Please confirm your email address by clicking the button below. This helps us keep your account secure.
              </p>

              <p style="text-align:center;margin:28px 0;">
                <!-- Button -->
                <a href="{{confirm_url}}" target="_blank" style="display:inline-block;padding:12px 22px;border-radius:6px;background:#2563eb;color:#fff;text-decoration:none;font-weight:600;">
                  Confirm my email
                </a>
              </p>

              <p style="margin:0 0 12px 0;font-size:13px;color:#666;">
                If the button doesn't work, copy and paste this link into your browser:
              </p>
              <p style="word-break:break-all;margin:0 0 20px 0;color:#2563eb;font-size:13px;">
                <a href="{{confirm_url}}" style="color:#2563eb;text-decoration:none;">{{confirm_url}}</a>
              </p>

              <p style="margin:0;font-size:13px;color:#666;">If you didn't create an account, you can ignore this email or contact support at <a href="mailto:{{support_email}}" style="color:#2563eb;">{{support_email}}</a>.</p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:18px 24px;background:#f7fafc;color:#9aa3ad;font-size:13px;text-align:center;">
              <div style="max-width:520px;margin:0 auto;">
                <p style="margin:0 0 8px 0;">Thanks — The Splash Team</p>
                <p style="margin:0;color:#9aa3ad;font-size:12px;">&copy; {{year}} splash. All rights reserved.</p>
              </div>
            </td>
          </tr>
        </table>

        <!-- Small legal / unsubscribe -->
        <table width="600" cellpadding="0" cellspacing="0" role="presentation" style="max-width:600px;margin-top:12px;">
          <tr>
            <td style="text-align:center;color:#9aa3ad;font-size:11px;padding:8px 6px;">
              You received this email because you signed up for splash library. If you don't want to receive these emails, update your preferences in your account.
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
