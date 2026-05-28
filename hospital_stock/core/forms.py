from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User

from .models import Inventario, Medicamento, Movil, Compra


class TransferStockForm(forms.Form):
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.all(), label='Medicamento')
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')
    fecha_vencimiento = forms.DateField(label='Fecha de vencimiento', widget=forms.DateInput(attrs={'type': 'date'}))


class AjustarStockForm(forms.Form):
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.all(), label='Medicamento')
    cantidad = forms.IntegerField(min_value=0, label='Cantidad deseada')
    fecha_vencimiento = forms.DateField(label='Fecha de vencimiento', widget=forms.DateInput(attrs={'type': 'date'}))


class MoveStockForm(forms.Form):
    movil = forms.ModelChoiceField(queryset=Movil.objects.all(), label='Móvil')
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.all(), label='Medicamento')
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')
    fecha_vencimiento = forms.DateField(label='Fecha de vencimiento', widget=forms.DateInput(attrs={'type': 'date'}))


class MovilForm(forms.ModelForm):
    class Meta:
        model = Movil
        fields = ['nombre']


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        if Medicamento.objects.filter(nombre__iexact=nombre).exists():
            raise forms.ValidationError('Ya existe un medicamento con ese nombre.')
        return nombre


class InventarioForm(forms.ModelForm):
    fecha_vencimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Inventario
        fields = ['medicamento', 'cantidad', 'fecha_vencimiento']


class TransferirStockAlMovilForm(forms.Form):
    """Formulario mejorado para transferir stock del inventario a un móvil"""
    medicamento = forms.ModelChoiceField(
        queryset=Medicamento.objects.all(),
        label='Medicamento',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_medicamento'})
    )
    fecha_vencimiento = forms.DateField(
        label='Fecha de vencimiento',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_fecha_vencimiento'}),
        required=True
    )
    cantidad = forms.IntegerField(
        min_value=1,
        label='Cantidad',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_cantidad'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo de fecha_vencimiento será dinámico via JavaScript


class AjustarStockMovilForm(forms.Form):
    """Formulario mejorado para ajustar stock en un móvil"""
    medicamento = forms.ModelChoiceField(
        queryset=Medicamento.objects.all(),
        label='Medicamento',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_medicamento'})
    )
    fecha_vencimiento = forms.DateField(
        label='Fecha de vencimiento',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_fecha_vencimiento'}),
        required=True
    )
    cantidad = forms.IntegerField(
        min_value=0,
        label='Cantidad deseada',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_cantidad'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo de fecha_vencimiento será dinámico via JavaScript


class UsuarioCreateForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Superuser', 'Superuser'),
        ('Empleado', 'Empleado'),
        ('Espectador', 'Espectador'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rol')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_active = True
        role = self.cleaned_data['role']
        if role == 'Superuser':
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
        if commit:
            user.save()
            Group.objects.get(name=role).user_set.add(user)
        return user


class StockActionForm(forms.Form):
    ACTION_CHOICES = [
        ('add', 'Agregar stock'),
        ('adjust', 'Ajustar stock a valor fijo'),
    ]
    SOURCE_CHOICES = [
        ('inventario', 'Desde inventario'),
        ('externo', 'Externo (no descuenta inventario)'),
    ]

    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.RadioSelect, initial='add')
    cantidad = forms.IntegerField(min_value=0, label='Cantidad')
    origen = forms.ChoiceField(choices=SOURCE_CHOICES, required=False, label='Origen')
    enviar_recuperado = forms.BooleanField(required=False, label='¿Enviar sobrante a recuperados?')

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        cantidad = cleaned_data.get('cantidad')
        origen = cleaned_data.get('origen')

        if action == 'add' and not origen:
            raise forms.ValidationError('Seleccione el origen del stock.')

        if cantidad is None:
            raise forms.ValidationError('La cantidad es obligatoria.')

        if action == 'add' and cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor que cero para agregar stock.')

        if action == 'adjust' and cantidad < 0:
            raise forms.ValidationError('La cantidad deseada no puede ser negativa.')

        return cleaned_data


class AgregarDesdeRecuperadosForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')


class EditarPrecioForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['precio_unitario']
        widgets = {
            'precio_unitario': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio_unitario'].required = False
        self.fields['precio_unitario'].help_text = 'Precio unitario en la moneda local. Deje vacío si no aplica.'


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['medicamento', 'cantidad', 'precio_unitario', 'descuento', 'contar_como_gasto', 'motivo_sin_gasto', 'movil']
        widgets = {
            'precio_unitario': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'descuento': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'motivo_sin_gasto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe el motivo por el cual no cuenta como gasto'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el medicamento tiene precio definido, usarlo como valor inicial
        if self.instance and self.instance.medicamento and self.instance.medicamento.precio_unitario:
            self.fields['precio_unitario'].initial = self.instance.medicamento.precio_unitario
    
    def clean(self):
        cleaned_data = super().clean()
        contar_como_gasto = cleaned_data.get('contar_como_gasto')
        motivo_sin_gasto = cleaned_data.get('motivo_sin_gasto')
        
        # Si NO cuenta como gasto, el motivo es obligatorio
        if not contar_como_gasto and not motivo_sin_gasto:
            raise forms.ValidationError('Debe proporcionar un motivo si la compra no cuenta como gasto.')
        
        return cleaned_data


class AgregarMedicamentoAlInventarioForm(forms.Form):
    """Formulario para que el cliente agregue medicamentos al inventario"""
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.all(), label='Medicamento', widget=forms.Select(attrs={'class': 'form-select'}))
    cantidad = forms.IntegerField(min_value=1, label='Cantidad', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    fecha_vencimiento = forms.DateField(label='Fecha de vencimiento', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    descuento = forms.DecimalField(min_value=0, decimal_places=2, initial=0, label='Descuento aplicado', required=False, widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': 'form-control'}))
    contar_como_gasto = forms.BooleanField(initial=True, required=False, label='Contar como gasto (este medicamento fue comprado)', widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    motivo_sin_gasto = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ej: Ganado en concurso, donación, etc', 'class': 'form-control'}), required=False, label='Motivo si no cuenta como gasto')
    
    def clean(self):
        cleaned_data = super().clean()
        contar_como_gasto = cleaned_data.get('contar_como_gasto')
        motivo_sin_gasto = cleaned_data.get('motivo_sin_gasto')
        medicamento = cleaned_data.get('medicamento')
        
        # Si NO cuenta como gasto, el motivo es obligatorio
        if not contar_como_gasto and not motivo_sin_gasto:
            raise forms.ValidationError('Debe proporcionar un motivo si el medicamento no cuenta como gasto.')
        
        # Si cuenta como gasto, el medicamento DEBE tener precio definido
        if contar_como_gasto and medicamento:
            if medicamento.precio_unitario is None or medicamento.precio_unitario == 0:
                raise forms.ValidationError(f'El medicamento "{medicamento.nombre}" no tiene precio definido. Debe asignar un precio primero.')
        
        return cleaned_data


class ConfiguracionGastosForm(forms.ModelForm):
    """Formulario para editar límites de gastos"""
    class Meta:
        model = None  # Se asignará dinámicamente en la vista
        fields = ['limite_mensual', 'porcentaje_alerta']
        widgets = {
            'limite_mensual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ej: 10000'
            }),
            'porcentaje_alerta': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'placeholder': 'Ej: 80'
            })
        }
        labels = {
            'limite_mensual': 'Límite mensual ($)',
            'porcentaje_alerta': 'Porcentaje para mostrar alerta (%)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asignar el modelo aquí
        from .models import ConfiguracionGastos
        self._meta.model = ConfiguracionGastos
        self._meta.fields = ('limite_mensual', 'porcentaje_alerta')


class ProfileEditForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Dejar en blanco para no cambiar'}),
        required=False, 
        label="Nueva contraseña"
    )
    first_name = forms.CharField(
        max_length=150, 
        required=False, 
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150, 
        required=False, 
        label="Apellido",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False, 
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    # Profile fields
    nombre_completo = forms.CharField(
        max_length=150, 
        required=False, 
        label="Nombre Completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Dr. Guillermo Pérez'})
    )
    telefono = forms.CharField(
        max_length=30, 
        required=False, 
        label="Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +54 9 11 ...'})
    )
    direccion = forms.CharField(
        max_length=255, 
        required=False, 
        label="Dirección",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Av. Rivadavia 1234'})
    )
    biografia = forms.CharField(
        required=False, 
        label="Biografía",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cuéntanos un poco sobre ti...'})
    )
    foto_perfil = forms.ImageField(
        required=False, 
        label="Foto de Perfil"
    )
    fecha_nacimiento = forms.DateField(
        required=False, 
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nombre de usuario',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate initial values for profile fields if user has a profile
        if self.instance and hasattr(self.instance, 'profile'):
            profile = self.instance.profile
            self.fields['nombre_completo'].initial = profile.nombre_completo
            self.fields['telefono'].initial = profile.telefono
            self.fields['direccion'].initial = profile.direccion
            self.fields['biografia'].initial = profile.biografia
            self.fields['foto_perfil'].initial = profile.foto_perfil
            if profile.fecha_nacimiento:
                self.fields['fecha_nacimiento'].initial = profile.fecha_nacimiento.strftime('%Y-%m-%d')
                
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
            
        # Get or create profile
        from core.models import Profile
        profile, created = Profile.objects.get_or_create(user=user)
        
        # Save profile fields
        profile.nombre_completo = self.cleaned_data.get('nombre_completo')
        profile.telefono = self.cleaned_data.get('telefono')
        profile.direccion = self.cleaned_data.get('direccion')
        profile.biografia = self.cleaned_data.get('biografia')
        
        # Handle date correctly (could be None or blank string)
        fecha_nac = self.cleaned_data.get('fecha_nacimiento')
        profile.fecha_nacimiento = fecha_nac if fecha_nac else None
        
        foto = self.cleaned_data.get('foto_perfil')
        if foto:
            profile.foto_perfil = foto
            
        profile.save()
        return user

