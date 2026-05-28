from django.test import TestCase
from django.contrib.auth.models import User, Group
from core.models import Profile, Movimiento, Medicamento, Movil, StockMovil, Inventario
from core.services import transferir_stock_a_movil, ajustar_stock_movil, log_movimiento
from django.utils import timezone
import datetime


class UserProfileAndMovementTests(TestCase):
    def setUp(self):
        # Create groups
        self.superuser_group, _ = Group.objects.get_or_create(name='Superuser')
        self.empleado_group, _ = Group.objects.get_or_create(name='Empleado')
        self.espectador_group, _ = Group.objects.get_or_create(name='Espectador')

        # Create users
        self.super_user = User.objects.create_superuser(username='admin', password='password123')
        self.regular_user = User.objects.create_user(username='guillermo', password='password123')
        self.other_user = User.objects.create_user(username='juan', password='password123')

        # Add groups
        self.empleado_group.user_set.add(self.regular_user)
        self.espectador_group.user_set.add(self.other_user)

        # Create basic stock objects
        self.medicamento = Medicamento.objects.create(nombre='Ibuprofeno', precio_unitario=10.00)
        self.movil = Movil.objects.create(nombre='Ambulancia A')
        self.fecha_venc = timezone.now().date() + datetime.timedelta(days=90)
        
        # Create inventory stock
        self.inventario = Inventario.objects.create(
            medicamento=self.medicamento,
            cantidad=100,
            fecha_vencimiento=self.fecha_venc
        )

    def test_profile_auto_creation_signal(self):
        """Verify that profile is automatically created when a user is saved"""
        self.assertIsNotNone(self.regular_user.profile)
        self.assertEqual(self.regular_user.profile.user, self.regular_user)
        self.assertEqual(self.regular_user.profile.nombre_completo, "")

    def test_log_movimiento_with_user(self):
        """Verify that log_movimiento associates the correct user with the movement"""
        mov = log_movimiento(
            tipo='ajuste',
            medicamento=self.medicamento,
            cantidad=5,
            movil=self.movil,
            descripcion='Ajuste de prueba',
            usuario=self.regular_user
        )
        self.assertEqual(mov.usuario, self.regular_user)
        self.assertEqual(mov.medicamento, self.medicamento)

    def test_service_attributes_user(self):
        """Verify that stock manipulation services associate the user with the logged movement"""
        stock = transferir_stock_a_movil(
            movil=self.movil,
            medicamento=self.medicamento,
            cantidad=10,
            fecha_vencimiento=self.fecha_venc,
            usuario=self.regular_user
        )
        
        # Check that stock was created/updated
        self.assertEqual(stock.cantidad, 10)
        
        # Check logged movement
        mov = Movimiento.objects.filter(tipo='entrada', movil=self.movil).first()
        self.assertIsNotNone(mov)
        self.assertEqual(mov.usuario, self.regular_user)
        self.assertIn('Transferido', mov.descripcion)

    def test_profile_permissions(self):
        """Verify that a user can see their own profile, and superuser can see other profiles"""
        # We can test the view permissions using Django test client
        self.client.login(username='guillermo', password='password123')
        
        # Access own profile
        response = self.client.get(f'/perfil/{self.regular_user.pk}/')
        self.assertEqual(response.status_code, 200)

        # Try to access other profile (juan) -> Should raise PermissionDenied (403)
        response = self.client.get(f'/perfil/{self.other_user.pk}/')
        self.assertEqual(response.status_code, 403)
        
        self.client.logout()

        # Login as superuser
        self.client.login(username='admin', password='password123')
        
        # Access Juan's profile as superuser -> Should succeed (200)
        response = self.client.get(f'/perfil/{self.other_user.pk}/')
        self.assertEqual(response.status_code, 200)
