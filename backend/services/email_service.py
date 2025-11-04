"""
Email Service - Envío de correos electrónicos
Usa Gmail SMTP para enviar correos de recuperación de contraseña
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from utils.logger import log_info, log_error, log_success


class EmailService:
    """Servicio de envío de correos electrónicos"""

    def __init__(self):
        self.smtp_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_PORT", "587"))
        self.smtp_username = os.getenv("EMAIL_USERNAME", "")
        self.smtp_password = os.getenv("EMAIL_PASSWORD", "")
        self.from_email = os.getenv("EMAIL_FROM", self.smtp_username)
        self.from_name = os.getenv("EMAIL_FROM_NAME", "Nutrition Intelligence")
        self.app_url = os.getenv("APP_URL", "https://nutrition-intelligence.scram2k.com")

    def _create_connection(self) -> smtplib.SMTP:
        """Crea una conexión SMTP con Gmail"""
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            log_success("Conexión SMTP establecida exitosamente")
            return server
        except Exception as e:
            log_error(f"Error al conectar con SMTP: {str(e)}")
            raise

    def _create_password_reset_html(self, reset_url: str, user_name: str) -> str:
        """Crea el contenido HTML para el correo de recuperación de contraseña"""
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperación de Contraseña</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table role="presentation" style="width: 600px; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 40px 40px 20px 40px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">
                                🔐 Recuperación de Contraseña
                            </h1>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin: 0 0 20px 0; color: #333333; font-size: 16px; line-height: 1.6;">
                                Hola <strong>{user_name}</strong>,
                            </p>
                            <p style="margin: 0 0 20px 0; color: #666666; font-size: 15px; line-height: 1.6;">
                                Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en <strong>Nutrition Intelligence</strong>.
                            </p>
                            <p style="margin: 0 0 30px 0; color: #666666; font-size: 15px; line-height: 1.6;">
                                Haz clic en el botón de abajo para crear una nueva contraseña:
                            </p>

                            <!-- Button -->
                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td align="center" style="padding: 0;">
                                        <a href="{reset_url}" style="display: inline-block; padding: 16px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 16px; font-weight: 600; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);">
                                            Restablecer Contraseña
                                        </a>
                                    </td>
                                </tr>
                            </table>

                            <p style="margin: 30px 0 0 0; color: #999999; font-size: 13px; line-height: 1.6;">
                                O copia y pega este enlace en tu navegador:
                            </p>
                            <p style="margin: 10px 0 0 0; word-break: break-all;">
                                <a href="{reset_url}" style="color: #667eea; text-decoration: none; font-size: 13px;">
                                    {reset_url}
                                </a>
                            </p>

                            <!-- Warning -->
                            <div style="margin-top: 30px; padding: 20px; background-color: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                                <p style="margin: 0; color: #856404; font-size: 14px; line-height: 1.6;">
                                    ⚠️ <strong>Importante:</strong> Este enlace expirará en <strong>1 hora</strong> por razones de seguridad.
                                </p>
                            </div>

                            <p style="margin: 30px 0 0 0; color: #999999; font-size: 14px; line-height: 1.6;">
                                Si no solicitaste restablecer tu contraseña, puedes ignorar este correo de forma segura. Tu contraseña no será cambiada.
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px 40px; background-color: #f8f9fa; border-radius: 0 0 8px 8px; text-align: center;">
                            <p style="margin: 0 0 10px 0; color: #666666; font-size: 14px;">
                                Este correo fue enviado por <strong>Nutrition Intelligence</strong>
                            </p>
                            <p style="margin: 0; color: #999999; font-size: 12px;">
                                © {2024} Nutrition Intelligence. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

    def send_password_reset_email(
        self,
        to_email: str,
        user_name: str,
        reset_token: str,
        reset_url: Optional[str] = None
    ) -> bool:
        """
        Envía un correo de recuperación de contraseña

        Args:
            to_email: Email del destinatario
            user_name: Nombre del usuario
            reset_token: Token de recuperación
            reset_url: URL completa de recuperación (opcional)

        Returns:
            bool: True si se envió exitosamente, False en caso contrario
        """
        try:
            # Construir URL de reset
            if not reset_url:
                reset_url = f"{self.app_url}/auth/reset-password?token={reset_token}"

            log_info(f"Preparando email de recuperación para: {to_email}")

            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = '🔐 Recuperación de Contraseña - Nutrition Intelligence'
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email

            # Contenido en texto plano (fallback)
            text_content = f"""
Hola {user_name},

Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en Nutrition Intelligence.

Para restablecer tu contraseña, visita el siguiente enlace:
{reset_url}

Este enlace expirará en 1 hora por razones de seguridad.

Si no solicitaste restablecer tu contraseña, puedes ignorar este correo.

Saludos,
Nutrition Intelligence
"""

            # Contenido HTML
            html_content = self._create_password_reset_html(reset_url, user_name)

            # Adjuntar ambas versiones
            part1 = MIMEText(text_content, 'plain', 'utf-8')
            part2 = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part1)
            msg.attach(part2)

            # Enviar email
            server = self._create_connection()
            server.send_message(msg)
            server.quit()

            log_success(f"Email de recuperación enviado exitosamente a: {to_email}")
            return True

        except Exception as e:
            log_error(f"Error al enviar email de recuperación a {to_email}: {str(e)}")
            return False

    def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """
        Envía un correo de bienvenida al nuevo usuario

        Args:
            to_email: Email del destinatario
            user_name: Nombre del usuario

        Returns:
            bool: True si se envió exitosamente
        """
        try:
            log_info(f"Preparando email de bienvenida para: {to_email}")

            msg = MIMEMultipart('alternative')
            msg['Subject'] = '🎉 Bienvenido a Nutrition Intelligence'
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email

            text_content = f"""
Hola {user_name},

¡Bienvenido a Nutrition Intelligence!

Tu cuenta ha sido creada exitosamente. Ahora puedes acceder a todas nuestras funcionalidades.

Para comenzar, visita: {self.app_url}

Saludos,
Nutrition Intelligence
"""

            html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table role="presentation" style="width: 600px; border-collapse: collapse; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="padding: 40px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 32px;">🎉 ¡Bienvenido!</h1>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 40px;">
                            <p style="margin: 0 0 20px 0; color: #333333; font-size: 16px;">
                                Hola <strong>{user_name}</strong>,
                            </p>
                            <p style="margin: 0 0 20px 0; color: #666666; font-size: 15px; line-height: 1.6;">
                                ¡Bienvenido a <strong>Nutrition Intelligence</strong>! Tu cuenta ha sido creada exitosamente.
                            </p>
                            <p style="margin: 0 0 30px 0; color: #666666; font-size: 15px; line-height: 1.6;">
                                Ahora puedes acceder a todas nuestras funcionalidades para gestionar tu nutrición de forma inteligente.
                            </p>
                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td align="center">
                                        <a href="{self.app_url}" style="display: inline-block; padding: 16px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 16px; font-weight: 600;">
                                            Comenzar Ahora
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 30px 40px; background-color: #f8f9fa; border-radius: 0 0 8px 8px; text-align: center;">
                            <p style="margin: 0; color: #999999; font-size: 12px;">
                                © 2024 Nutrition Intelligence. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

            part1 = MIMEText(text_content, 'plain', 'utf-8')
            part2 = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part1)
            msg.attach(part2)

            server = self._create_connection()
            server.send_message(msg)
            server.quit()

            log_success(f"Email de bienvenida enviado a: {to_email}")
            return True

        except Exception as e:
            log_error(f"Error al enviar email de bienvenida a {to_email}: {str(e)}")
            return False


# Instancia global del servicio
email_service = EmailService()
