from rest_framework import serializers
from c19_server.models import Form, UserID, User


class FormSerializer(serializers.ModelSerializer):
    kategori = serializers.ReadOnlyField()

    class Meta:
        model = Form
        fields = ['id', 'gejala_demam', 'usia', 'kontak',
                  'aktivitas', 'gejala_lain', 'kategori']


class UserIDSerializer(serializers.ModelSerializer):
    forms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def validate_nik(self, value):
        """
        Memastikan NIK memiliki panjang 16 digit
        """
        if len(value) != 16:
            raise serializers.ValidationError("Panjang NIK tidak sama 16 digit")
        return value

    class Meta:
        model = UserID
        fields = ['id', 'owner', 'nama', 'nik', 'alamat', 'tanggal_lahir', 'forms']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile']
